from exercises.day02_starter import choose_handler, validate_arguments


def test_returns_function_without_executing_it():
    def handler():
        raise AssertionError("这里只查找函数，不应执行")
    assert choose_handler({"read_file": handler}, "read_file") is handler


def test_unknown_tool():
    assert choose_handler({}, "delete_file") is None


def test_valid_arguments():
    assert validate_arguments({"path": "note.txt"}) is True


def test_invalid_arguments():
    for arguments in ({"path": 123}, {}, {"path": " "}, {"path": "note.txt", "extra": True}):
        assert validate_arguments(arguments) is False
