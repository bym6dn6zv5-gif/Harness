from exercises.day04_starter import count_tool_messages


def test_empty_records():
    assert count_tool_messages([]) == 0


def test_count_only_tool_feedback_messages():
    records = [
        {"type": "message", "message": {"role": "user"}},
        {"type": "message", "message": {"role": "assistant", "tool_call": {}}},
        {"type": "message", "message": {"role": "tool"}},
        {"type": "message", "message": {"role": "tool"}},
        {"type": "summary", "tool_calls": 2},
    ]
    assert count_tool_messages(records) == 2
