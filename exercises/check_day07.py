from exercises.day07_starter import permission_code


def test_known_and_allowed():
    assert permission_code("read_file", {"read_file", "count_lines"}, {"read_file"}) == "allowed"


def test_known_but_not_allowed():
    assert permission_code("count_lines", {"read_file", "count_lines"}, {"read_file"}) == "permission_denied"


def test_unknown_has_priority_even_if_in_allowed_set():
    assert permission_code("delete_file", {"read_file"}, {"delete_file"}) == "unknown_tool"


def test_empty_allow_set_denies_every_known_tool():
    assert permission_code("read_file", {"read_file"}, set()) == "permission_denied"
