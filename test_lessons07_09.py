"""第 7—9 天参考实验检查；学生的 starter 保持待填写。"""

import importlib
import json
from pathlib import Path
import sqlite3
import subprocess

import pytest

from exercises import answers07_09
from mini_harness.lesson02 import PathArgs, ToolRegistry, build_registry
from mini_harness.lesson03 import ReadThenCountModel, run_agent
from mini_harness.lesson07 import PolicyRegistry
from mini_harness import lesson08, lesson09


@pytest.fixture
def workspace(tmp_path):
    root = tmp_path / "workspace"
    root.mkdir()
    (root / "note.txt").write_bytes(b"alpha\nbeta\ngamma\n")
    return root


def test_denied_request_does_not_reach_handler(workspace):
    called = []
    registry = ToolRegistry()
    registry.register("read_file", PathArgs, lambda *args: called.append(args))
    policy = PolicyRegistry(registry, set())
    # 权限先于参数；即使参数无效，也应在执行分支之前停下。
    result = policy.dispatch("read_file", {"path": 123}, workspace)
    assert result["error"]["code"] == "permission_denied"
    assert called == []


def test_allowed_request_reaches_handler_once(workspace):
    called = []
    registry = ToolRegistry()
    def handler(args, root):
        called.append((args.path, root))
        return {"ok": True}
    registry.register("read_file", PathArgs, handler)
    assert PolicyRegistry(registry, {"read_file"}).dispatch("read_file", {"path": "note.txt"}, workspace)["ok"]
    assert called == [("note.txt", workspace)]


def test_policy_snapshots_host_configuration_and_filters_descriptions(workspace):
    allowed = {"read_file"}
    policy = PolicyRegistry(build_registry(), allowed)
    allowed.add("count_lines")
    assert [row["name"] for row in policy.definitions()] == ["read_file"]
    assert policy.dispatch("count_lines", {"path": "note.txt"}, workspace)["error"]["code"] == "permission_denied"
    assert policy.dispatch("delete_file", {}, workspace)["error"]["code"] == "unknown_tool"


@pytest.mark.parametrize("allowed", [{"delete_file"}, "read_file", {123}])
def test_invalid_policy_configuration_is_not_silently_accepted(allowed):
    with pytest.raises(ValueError):
        PolicyRegistry(build_registry(), allowed)


@pytest.mark.parametrize("arguments,code", [({"path": 123}, "invalid_arguments"), ({"path": "../outside.txt"}, "path_not_allowed")])
def test_permission_does_not_skip_argument_and_path_checks(workspace, arguments, code):
    policy = PolicyRegistry(build_registry(), {"read_file"})
    assert policy.dispatch("read_file", arguments, workspace)["error"]["code"] == code


def test_loop_returns_permission_error_to_model(workspace):
    result = run_agent(ReadThenCountModel(), workspace, max_steps=3,
                       registry=PolicyRegistry(build_registry(), {"read_file"}))
    assert result["status"] == "model_finished"
    assert result["model_calls"] == 3
    assert result["tool_calls"] == 2  # 尝试次数包含被拒绝的一次。
    assert json.loads(result["messages"][4]["content"])["error"]["code"] == "permission_denied"
    assert "失败" in result["detail"]


def test_fixed_child_process_completes():
    result = lesson08.run_timed_probe(0, 5)
    assert result["ok"] is True
    assert result["data"] == {"completed": True}
    assert result["elapsed_ms"] >= 0


def test_fixed_child_process_times_out():
    result = lesson08.run_timed_probe(3, 0.1)
    assert result["error"]["code"] == "tool_timeout"
    # 不断言精确毫秒数；进程启动和系统调度都有开销。


@pytest.mark.parametrize("delay,timeout", [(-1, 5), (11, 5), (True, 5), ("0", 5), (float("nan"), 5), (0, 0), (0, float("inf")), (0, 31), (10**400, 5)])
def test_bad_time_arguments_are_rejected_without_starting_child(monkeypatch, delay, timeout):
    def forbidden(*args, **kwargs):
        raise AssertionError("参数无效时不应启动进程")
    monkeypatch.setattr(lesson08.subprocess, "run", forbidden)
    assert lesson08.run_timed_probe(delay, timeout)["error"]["code"] == "invalid_arguments"


def test_worker_command_is_fixed_and_environment_does_not_include_api_key(monkeypatch):
    monkeypatch.setenv("HARNESS_EXAMPLE_API_KEY", "fake-for-test")
    calls = []
    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, '{"ok":true,"data":{"completed":true}}', "")
    monkeypatch.setattr(lesson08.subprocess, "run", fake_run)
    assert lesson08.run_timed_probe(0, 5)["ok"]
    command, settings = calls[0]
    assert isinstance(command, list)
    assert Path(command[4]).name == "timeout_worker.py"
    assert "-I" in command
    assert settings["shell"] is False
    assert settings["timeout"] == 5
    assert "HARNESS_EXAMPLE_API_KEY" not in settings["env"]


@pytest.mark.parametrize("returncode,stdout,expected", [(1, "", "tool_failed"), (0, "oops", "invalid_tool_result"), (0, "{}", "invalid_tool_result")])
def test_child_failure_or_bad_json_is_a_structured_error(monkeypatch, returncode, stdout, expected):
    monkeypatch.setattr(lesson08.subprocess, "run", lambda command, **kwargs: subprocess.CompletedProcess(command, returncode, stdout, ""))
    assert lesson08.run_timed_probe(0, 5)["error"]["code"] == expected


def test_process_launch_error_is_reported(monkeypatch):
    def fail(*args, **kwargs):
        raise OSError("simulated")
    monkeypatch.setattr(lesson08.subprocess, "run", fail)
    assert lesson08.run_timed_probe(0, 5)["error"]["code"] == "tool_failed"


def test_checkpoint_contains_completed_round_and_resumes_without_replaying_it(workspace, tmp_path):
    path = tmp_path / "checkpoint.sqlite3"
    first = lesson09.start_task(path, workspace)
    assert first.status == "checkpointed"
    assert (first.model_calls, first.tool_calls) == (1, 1)
    assert [row["role"] for row in first.messages] == ["user", "assistant", "tool"]
    loaded, revision = lesson09.load_checkpoint(path)
    assert loaded == first
    assert revision == 1
    finished = lesson09.resume_task(path)
    assert finished.status == "model_finished"
    assert (finished.model_calls, finished.tool_calls) == (3, 2)
    assert "3 行" in finished.detail
    assert [row["tool_call_id"] for row in finished.messages if row["role"] == "tool"] == ["read_001", "count_002"]
    _, revision = lesson09.load_checkpoint(path)
    assert lesson09.resume_task(path) == finished
    assert lesson09.load_checkpoint(path)[1] == revision  # 终态不重复运行，也不重写。


def test_resume_does_not_reset_step_budget(workspace, tmp_path):
    path = tmp_path / "checkpoint.sqlite3"
    lesson09.start_task(path, workspace, max_steps=2)
    result = lesson09.resume_task(path)
    assert result.status == "step_limit"
    assert (result.model_calls, result.tool_calls, result.max_steps) == (2, 2, 2)
    assert lesson09.resume_task(path) == result


@pytest.mark.parametrize("change", ["content", "missing", "encoding"])
def test_changed_input_stops_before_another_model_or_tool_call(workspace, tmp_path, change):
    path = tmp_path / "checkpoint.sqlite3"
    lesson09.start_task(path, workspace)
    note = workspace / "note.txt"
    if change == "missing":
        note.unlink()
    else:
        note.write_bytes(b"changed\n" if change == "content" else b"\xff\xfe")
    result = lesson09.resume_task(path)
    assert result.status == "workspace_conflict"
    assert (result.model_calls, result.tool_calls) == (1, 1)
    assert lesson09.resume_task(path) == result


def test_non_input_files_are_outside_this_lessons_fingerprint(workspace):
    before = lesson09.input_fingerprint(workspace)
    (workspace / "other.txt").write_bytes(b"not a task input")
    assert lesson09.input_fingerprint(workspace) == before
    (workspace / "note.txt").write_bytes(b"alpha\r\nbeta\r\ngamma\r\n")
    assert lesson09.input_fingerprint(workspace) != before


def test_existing_checkpoint_is_not_overwritten(workspace, tmp_path):
    path = tmp_path / "checkpoint.sqlite3"
    lesson09.start_task(path, workspace)
    original = path.read_bytes()
    with pytest.raises(FileExistsError):
        lesson09.start_task(path, workspace)
    assert path.read_bytes() == original


def test_missing_checkpoint_is_not_created_on_resume(tmp_path):
    path = tmp_path / "typo.sqlite3"
    with pytest.raises(sqlite3.OperationalError):
        lesson09.resume_task(path)
    assert not path.exists()


def test_stale_writer_cannot_overwrite_newer_checkpoint(workspace, tmp_path):
    path = tmp_path / "checkpoint.sqlite3"
    lesson09.start_task(path, workspace)
    state, old_revision = lesson09.load_checkpoint(path)
    lesson09.resume_task(path)
    finished, revision = lesson09.load_checkpoint(path)
    with pytest.raises(ValueError, match="版本冲突"):
        lesson09.save_checkpoint(path, state, old_revision)
    assert lesson09.load_checkpoint(path) == (finished, revision)


def test_crash_before_commit_leaves_previous_round_replayable(workspace, tmp_path, monkeypatch):
    path = tmp_path / "checkpoint.sqlite3"
    lesson09.start_task(path, workspace)
    previous, revision = lesson09.load_checkpoint(path)
    save = lesson09.save_checkpoint
    def interrupted(*args, **kwargs):
        raise RuntimeError("模拟工具完成后、保存前进程中断")
    monkeypatch.setattr(lesson09, "save_checkpoint", interrupted)
    with pytest.raises(RuntimeError, match="中断"):
        lesson09.resume_task(path)
    assert lesson09.load_checkpoint(path) == (previous, revision)
    monkeypatch.setattr(lesson09, "save_checkpoint", save)
    result = lesson09.resume_task(path)
    assert result.status == "model_finished"
    # 未提交的 count_lines 会被重做；仅因本课工具只读，重做不会重复写文件。
    assert result.tool_calls == 2  # 持久化历史中的次数，不含丢失回合的实际尝试。


@pytest.mark.parametrize("limit", [0, -1, True, 3.5])
def test_invalid_checkpoint_budget_does_not_create_database(workspace, tmp_path, limit):
    path = tmp_path / "checkpoint.sqlite3"
    with pytest.raises(ValueError):
        lesson09.start_task(path, workspace, max_steps=limit)
    assert not path.exists()


def test_corrupt_counter_is_rejected(workspace, tmp_path):
    path = tmp_path / "checkpoint.sqlite3"
    lesson09.start_task(path, workspace)
    state, revision = lesson09.load_checkpoint(path)
    state.model_calls = 0
    lesson09.save_checkpoint(path, state, revision)
    with pytest.raises(ValueError, match="计数"):
        lesson09.resume_task(path)


@pytest.mark.parametrize("day,names", [(7, ["permission_code"]), (8, ["classify_process_result"]), (9, ["remaining_steps", "can_resume"])])
def test_new_exercise_checkers_accept_reference_answers(monkeypatch, day, names):
    checker = importlib.import_module(f"exercises.check_day{day:02}")
    for name in names:
        monkeypatch.setattr(checker, name, getattr(answers07_09, name))
    for name, function in vars(checker).items():
        if name.startswith("test_") and callable(function):
            function()
