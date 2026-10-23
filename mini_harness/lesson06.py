"""第 6 天：固定输入与预期，生成离线行为检查报告。"""

import argparse
import json
from pathlib import Path
from uuid import uuid4

from mini_harness.lesson01_cases import classify_result, run_case
from mini_harness.lesson02 import build_registry
from mini_harness.lesson03 import ReadThenCountModel, RepeatingModel, run_agent


def grade_case(case_id: str, expected: str, observed: str) -> dict:
    return {"id": case_id, "expected": expected, "observed": observed, "passed": expected == observed}


def evaluate(workspace: Path, simulate_bug: bool = False) -> dict:
    rows = []
    expected_codes = {"normal": "success", "missing": "file_not_found",
                      "invalid": "invalid_arguments", "unknown": "unknown_tool"}
    for case, expected in expected_codes.items():
        observed = classify_result(run_case(case, workspace)["tool_result"])
        if simulate_bug and case == "unknown":
            observed = "success"  # 人为模拟错误版本，不执行额外工具。
        rows.append(grade_case(case, expected, observed))
    count_result = build_registry().dispatch("count_lines", {"path": "note.txt"}, workspace)
    observed_count = str(count_result["data"]["line_count"]) if count_result["ok"] else count_result["error"]["code"]
    rows.append(grade_case("three_line_fixture", "3", observed_count))
    normal = run_agent(ReadThenCountModel(), workspace, max_steps=3)
    repeated = run_agent(RepeatingModel(), workspace, max_steps=3)
    rows.append(grade_case("normal_loop", "model_finished", normal["status"]))
    rows.append(grade_case("bounded_repeat", "step_limit", repeated["status"]))
    passed = sum(row["passed"] for row in rows)
    return {"kind": "offline_contract_checks", "real_model_evaluation": False,
            "simulated_bug": simulate_bug, "fixture": "three-line-v1",
            "total": len(rows), "passed": passed, "pass_rate": passed / len(rows), "cases": rows}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--simulate-bug", action="store_true")
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[1]
    job = project / ".harness/day06" / uuid4().hex
    workspace = job / "workspace"
    workspace.mkdir(parents=True)
    (workspace / "note.txt").write_bytes(b"alpha\nbeta\ngamma\n")
    report = evaluate(workspace, args.simulate_bug)
    path = job / "report.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    for row in report["cases"]:
        print("PASS" if row["passed"] else "FAIL", row["id"], "expected=", row["expected"], "observed=", row["observed"])
    print(f"[通过数] {report['passed']}/{report['total']}")
    print("[报告文件]", path)
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
