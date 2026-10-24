import pytest

from exercises.day09_starter import can_resume, remaining_steps


def test_resume_keeps_used_budget():
    assert remaining_steps(3, 1) == 2


def test_budget_never_becomes_negative():
    assert remaining_steps(3, 3) == 0
    assert remaining_steps(3, 5) == 0


def test_invalid_budget_values_raise():
    for limit, used in [(0, 0), (3, -1), (True, 0), (3, False), (3.0, 1), (3, "1")]:
        with pytest.raises(ValueError):
            remaining_steps(limit, used)


def test_matching_input_and_paused_task_can_resume():
    assert can_resume("abc", "abc", "checkpointed") is True


def test_changed_input_or_terminal_status_cannot_resume():
    assert can_resume("abc", "def", "checkpointed") is False
    for status in ["model_finished", "step_limit", "workspace_conflict", "unknown"]:
        assert can_resume("abc", "abc", status) is False
