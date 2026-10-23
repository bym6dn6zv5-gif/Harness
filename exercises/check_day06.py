from exercises.day06_starter import grade_case


def test_matching_result_passes():
    assert grade_case("missing", "file_not_found", "file_not_found") == {
        "id": "missing", "expected": "file_not_found", "observed": "file_not_found", "passed": True,
    }


def test_wrong_observation_fails():
    assert grade_case("unknown", "unknown_tool", "success")["passed"] is False


def test_preserve_expected_and_observed():
    row = grade_case("case-3", "step_limit", "model_finished")
    assert row["id"] == "case-3"
    assert row["expected"] == "step_limit"
    assert row["observed"] == "model_finished"
