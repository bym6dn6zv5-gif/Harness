import json

from exercises.day03_starter import make_tool_message, should_continue


def test_continue_before_limit():
    assert should_continue(0, 3, False) is True
    assert should_continue(2, 3, False) is True


def test_stop_at_limit_or_after_final_answer():
    assert should_continue(3, 3, False) is False
    assert should_continue(4, 3, False) is False
    assert should_continue(1, 3, True) is False


def test_tool_message_keeps_call_id_and_json_content():
    result = {"ok": True, "data": {"content": "中文反馈"}}
    message = make_tool_message("call_007", result)
    assert message["role"] == "tool"
    assert message["tool_call_id"] == "call_007"
    assert json.loads(message["content"]) == result
