from exercises.day01_starter import classify_result


def test_success():
    assert classify_result({"ok": True, "data": {"content": "hello"}}) == "success"


def test_error_codes():
    for code in ("unknown_tool", "invalid_arguments", "file_not_found"):
        result = {"ok": False, "error": {"code": code, "message": "说明"}}
        assert classify_result(result) == code
