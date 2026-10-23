"""第一课的边界检查；这里只使用临时目录中的测试文件。"""

import json

import pytest

from mini_harness.lesson01 import MockModel, execute_tool, run_demo


@pytest.mark.parametrize("content", ["你好，Harness！\n", "你好，Harness！\r\n"])
def test_read_file_returns_content_without_changing_file(tmp_path, content):
    note = tmp_path / "note.txt"
    note.write_bytes(content.encode("utf-8"))
    before = note.read_bytes()

    result = execute_tool("read_file", {"path": "note.txt"}, tmp_path)

    assert result == {"ok": True, "data": {"path": "note.txt", "content": content}}
    assert note.read_bytes() == before


@pytest.mark.parametrize("arguments", [
    {"path": 123},
    {},
    {"path": ""},
    {"path": "note.txt", "unexpected": True},
])
def test_invalid_arguments_are_rejected_before_reading(tmp_path, monkeypatch, arguments):
    def must_not_open(*args, **kwargs):
        raise AssertionError("错误参数不应触发文件读取")

    monkeypatch.setattr(type(tmp_path), "open", must_not_open)
    result = execute_tool("read_file", arguments, tmp_path)
    assert result["ok"] is False
    assert result["error"]["code"] == "invalid_arguments"


def test_unknown_tool_is_rejected(tmp_path):
    result = execute_tool("delete_file", {"path": "note.txt"}, tmp_path)
    assert result["ok"] is False
    assert result["error"]["code"] == "unknown_tool"


def test_path_cannot_escape_workspace(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (tmp_path / "outside.txt").write_text("只供测试使用的目录外内容", encoding="utf-8")

    result = execute_tool("read_file", {"path": "../outside.txt"}, workspace)
    assert result["error"]["code"] == "path_not_allowed"


def test_missing_file_returns_structured_error(tmp_path):
    result = execute_tool("read_file", {"path": "missing.txt"}, tmp_path)
    assert result["error"]["code"] == "file_not_found"


def test_large_file_is_rejected(tmp_path):
    (tmp_path / "large.txt").write_bytes(b"a" * 4097)
    result = execute_tool("read_file", {"path": "large.txt"}, tmp_path)
    assert result["error"]["code"] == "file_too_large"


def test_non_utf8_file_is_rejected(tmp_path):
    (tmp_path / "binary.txt").write_bytes(b"\xff\xfe")
    result = execute_tool("read_file", {"path": "binary.txt"}, tmp_path)
    assert result["error"]["code"] == "read_failed"


def test_demo_passes_tool_result_back_to_model(tmp_path, capsys):
    (tmp_path / "note.txt").write_text("工具反馈必须回传。", encoding="utf-8")
    messages = run_demo(tmp_path)

    assert [message["role"] for message in messages] == ["user", "assistant", "tool", "assistant"]
    assert messages[2]["tool_call_id"] == messages[1]["tool_call"]["id"]
    assert json.loads(messages[2]["content"])["data"]["content"] == "工具反馈必须回传。"
    assert "工具反馈必须回传。" in messages[3]["content"]
    assert "[5 模型给出回答]" in capsys.readouterr().out


def test_model_can_report_tool_error():
    messages = [{
        "role": "tool",
        "tool_call_id": "call_001",
        "content": json.dumps({"ok": False, "error": {"code": "file_not_found", "message": "未找到文件"}}),
    }]
    assert MockModel().reply(messages)["content"] == "工具调用失败：未找到文件"
