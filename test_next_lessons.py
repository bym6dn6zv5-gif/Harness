"""六天课程参考实现的行为检查；不要求学习者先填写练习。"""

import importlib
import json

import pytest

from exercises import answers
from mini_harness.lesson01_cases import classify_result, run_case
from mini_harness.lesson02 import PathArgs, ToolRegistry, build_registry
from mini_harness.lesson03 import ReadThenCountModel, RepeatingModel, run_agent, tool_request
from mini_harness.lesson04 import load_trace, save_trace
from mini_harness.lesson05 import compact_context, serialized_chars, truncate_text
from mini_harness.lesson06 import evaluate


@pytest.fixture
def workspace(tmp_path):
    (tmp_path / "note.txt").write_bytes(b"alpha\nbeta\ngamma\n")
    return tmp_path


@pytest.mark.parametrize("case,expected", [
    ("normal", "success"), ("missing", "file_not_found"),
    ("invalid", "invalid_arguments"), ("unknown", "unknown_tool"),
])
def test_cases_return_results_and_keep_call_association(workspace, case, expected):
    result = run_case(case, workspace)
    assert classify_result(result["tool_result"]) == expected
    messages = result["messages"]
    assert messages[2]["tool_call_id"] == messages[1]["tool_call"]["id"]
    assert json.loads(messages[2]["content"]) == result["tool_result"]
    assert messages[-1]["role"] == "assistant"


def test_registry_exposes_two_descriptions():
    definitions = build_registry().definitions()
    assert [definition["name"] for definition in definitions] == ["read_file", "count_lines"]
    assert definitions[0]["parameters"]["properties"]["path"]["type"] == "string"
    assert definitions[0]["parameters"]["additionalProperties"] is False


@pytest.mark.parametrize("arguments", [None, {}, {"path": 123}, {"path": ""}, {"path": " "}, {"path": "a", "extra": 1}])
def test_registry_validates_before_running_handler(workspace, arguments):
    calls = []
    registry = ToolRegistry()
    registry.register("watched", PathArgs, lambda *args: calls.append(args))
    result = registry.dispatch("watched", arguments, workspace)
    assert result["error"]["code"] == "invalid_arguments"
    assert calls == []


def test_registry_rejects_unknown_and_duplicate_names(workspace):
    registry = build_registry()
    assert registry.dispatch("delete_file", {}, workspace)["error"]["code"] == "unknown_tool"
    with pytest.raises(ValueError, match="重复"):
        registry.register("read_file", PathArgs, lambda *args: {})


@pytest.mark.parametrize("content,expected", [
    (b"", 0), (b"one", 1), (b"one\n", 1), (b"one\r\ntwo\r\n", 2), (b"\n", 1),
])
def test_count_lines_respects_empty_files_and_line_endings(workspace, content, expected):
    (workspace / "note.txt").write_bytes(content)
    result = build_registry().dispatch("count_lines", {"path": "note.txt"}, workspace)
    assert result["data"]["line_count"] == expected


def test_second_tool_keeps_file_error_and_path_boundary(workspace):
    registry = build_registry()
    assert registry.dispatch("count_lines", {"path": "absent.txt"}, workspace)["error"]["code"] == "file_not_found"
    assert registry.dispatch("count_lines", {"path": "../outside.txt"}, workspace)["error"]["code"] == "path_not_allowed"


def test_normal_loop_includes_final_reply_in_budget(workspace):
    result = run_agent(ReadThenCountModel(), workspace, max_steps=3)
    assert result["status"] == "model_finished"
    assert result["model_calls"] == 3
    assert result["tool_calls"] == 2
    assert "3 行" in result["detail"]
    assert [message["role"] for message in result["messages"]] == ["user", "assistant", "tool", "assistant", "tool", "assistant"]


@pytest.mark.parametrize("limit", [1, 2])
def test_loop_stops_before_an_extra_model_call(workspace, limit):
    result = run_agent(ReadThenCountModel(), workspace, max_steps=limit)
    assert result["status"] == "step_limit"
    assert result["model_calls"] == limit
    assert result["tool_calls"] == limit
    assert result["messages"][-1]["role"] == "tool"


def test_repeating_model_cannot_exceed_limit(workspace):
    result = run_agent(RepeatingModel(), workspace, max_steps=3)
    assert result["status"] == "step_limit"
    assert result["model_calls"] == result["tool_calls"] == 3


@pytest.mark.parametrize("limit", [0, -1, True, 2.5, "3"])
def test_invalid_step_limits_are_rejected(workspace, limit):
    with pytest.raises(ValueError, match="max_steps"):
        run_agent(ReadThenCountModel(), workspace, max_steps=limit)


@pytest.mark.parametrize("reply", ["not a message", {"role": "assistant", "content": " "}, {"role": "assistant", "tool_call": {"id": 3}}])
def test_malformed_response_stops_without_tools(workspace, reply):
    class BadModel:
        def reply(self, messages):
            return reply
    result = run_agent(BadModel(), workspace)
    assert result["status"] == "invalid_response"
    assert result["tool_calls"] == 0


def test_duplicate_call_id_is_not_executed_twice(workspace):
    class DuplicateModel:
        def reply(self, messages):
            return tool_request("same-id", "read_file", {"path": "note.txt"})
    result = run_agent(DuplicateModel(), workspace)
    assert result["status"] == "invalid_response"
    assert result["model_calls"] == 2
    assert result["tool_calls"] == 1


def test_file_error_is_returned_to_model(workspace):
    (workspace / "note.txt").unlink()
    result = run_agent(ReadThenCountModel(), workspace)
    assert result["status"] == "model_finished"
    assert result["tool_calls"] == 1
    assert "失败" in result["detail"]
    assert json.loads(result["messages"][2]["content"])["error"]["code"] == "file_not_found"


def test_jsonl_exports_messages_and_summary_without_overwriting(workspace):
    result = run_agent(ReadThenCountModel(), workspace)
    first = save_trace(result, workspace / "logs")
    second = save_trace(result, workspace / "logs")
    assert first != second
    records = load_trace(first)
    assert len(records) == 7
    assert records[0]["sequence"] == 1
    assert records[-1]["type"] == "summary"
    assert records[-1]["status"] == "model_finished"
    assert [row["message"] for row in records[:-1]] == result["messages"]


def test_context_trimming_preserves_original_and_valid_json(workspace):
    (workspace / "note.txt").write_text("学习" * 100, encoding="utf-8")
    messages = run_agent(ReadThenCountModel(), workspace)["messages"]
    original = json.dumps(messages, ensure_ascii=False)
    context = compact_context(messages, 12)
    assert json.dumps(messages, ensure_ascii=False) == original
    assert serialized_chars(context) < serialized_chars(messages)
    assert [row["role"] for row in context] == [row["role"] for row in messages]
    payload = json.loads(context[2]["content"])
    assert payload["data"]["content"] == "学习" * 6
    assert payload["data"]["content_truncated"] is True
    assert payload["data"]["original_chars"] == 200
    assert context[2]["tool_call_id"] == messages[2]["tool_call_id"]
    assert json.loads(context[4]["content"])["data"]["line_count"] == 1


@pytest.mark.parametrize("text,limit,expected", [("ab", 3, ("ab", False)), ("abc", 3, ("abc", False)), ("abcd", 3, ("abc", True))])
def test_truncation_boundary(text, limit, expected):
    assert truncate_text(text, limit) == expected


@pytest.mark.parametrize("limit", [0, -1, True])
def test_invalid_context_limits_fail_even_with_no_messages(limit):
    with pytest.raises(ValueError):
        compact_context([], limit)


def test_fixed_evaluation_detects_simulated_bug(workspace):
    good = evaluate(workspace)
    faulty = evaluate(workspace, simulate_bug=True)
    assert good["total"] == good["passed"] == 7
    assert good["real_model_evaluation"] is False
    assert faulty["passed"] == 6
    assert [row["id"] for row in faulty["cases"] if not row["passed"]] == ["unknown"]


@pytest.mark.parametrize("day,names", [
    (1, ["classify_result"]),
    (2, ["choose_handler", "validate_arguments"]),
    (3, ["should_continue", "make_tool_message"]),
    (4, ["count_tool_messages"]),
    (5, ["truncate_text"]),
    (6, ["grade_case"]),
])
def test_exercise_checks_accept_reference_answers(monkeypatch, day, names):
    checker = importlib.import_module(f"exercises.check_day{day:02}")
    for name in names:
        monkeypatch.setattr(checker, name, getattr(answers, name))
    for name, function in vars(checker).items():
        if name.startswith("test_") and callable(function):
            function()
