from exercises.day08_starter import classify_process_result


def test_zero_exit_is_success():
    assert classify_process_result(False, 0) == "success"


def test_nonzero_exit_is_failure():
    assert classify_process_result(False, 1) == "tool_failed"
    assert classify_process_result(False, -9) == "tool_failed"


def test_timeout_has_priority():
    assert classify_process_result(True, None) == "tool_timeout"
    assert classify_process_result(True, 0) == "tool_timeout"


def test_no_exit_code_cannot_be_called_success():
    assert classify_process_result(False, None) == "tool_failed"
