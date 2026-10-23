from exercises.day05_starter import truncate_text


def test_short_and_equal_length_text():
    assert truncate_text("ab", 3) == ("ab", False)
    assert truncate_text("abc", 3) == ("abc", False)


def test_long_text_and_unicode():
    assert truncate_text("abcd", 3) == ("abc", True)
    assert truncate_text("学习工具调用", 2) == ("学习", True)


def test_empty_text():
    assert truncate_text("", 2) == ("", False)
