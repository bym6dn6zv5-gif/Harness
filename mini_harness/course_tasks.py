"""准备教学任务，或校准可信教材；不会运行 Agent 修改后的源码。"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
from uuid import uuid4

from mini_harness.course_task_data import TASKS


def material_hash() -> str:
    encoded = json.dumps(TASKS, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_materials() -> None:
    if [row["id"] for row in TASKS] != [f"T{i:02}" for i in range(1, 31)]:
        raise ValueError("任务 id 必须固定为 T01—T30")
    for index, row in enumerate(TASKS):
        if row["split"] != ("dev" if index < 20 else "holdout"):
            raise ValueError("任务划分变化")
        if len(row["cases"]) < 3:
            raise ValueError("每个任务至少需要三个评分案例")
        for entry in row["cases"]:
            if not isinstance(entry["args"], list) or (("expected" in entry) == ("error" in entry)):
                raise ValueError("案例必须含 args，且 expected/error 恰有一个")
            if "error" in entry and entry["error"] != "ValueError":
                raise ValueError("教材仅定义 ValueError 异常案例")


def equivalent(actual, expected) -> bool:
    """布尔值不等于 0/1；浮点数允许极小舍入误差；其他结构递归比较。"""
    if type(expected) is float:
        return (type(actual) in (int, float)
                and math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9))
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(equivalent(a, b) for a, b in zip(actual, expected))
    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(equivalent(actual[key], expected[key]) for key in expected)
    return actual == expected


def check_case(function, entry: dict) -> bool:
    args = deepcopy(entry["args"])
    try:
        result = function(*args)
    except ValueError:
        return entry.get("error") == "ValueError" and args == entry["args"]
    except Exception:
        return False
    return "expected" in entry and equivalent(result, entry["expected"]) and args == entry["args"]


def verify_authored_materials() -> dict:
    """仅执行模块内固定自编源码；不是补丁运行器或通用沙箱。"""
    validate_materials()
    rows = []
    for task in TASKS:
        outcomes = {}
        for variant in ("buggy_source", "reference_source"):
            namespace = {}
            exec(compile(task[variant], f"<authored-{task['id']}-{variant}>", "exec"), namespace)
            outcomes[variant] = [check_case(namespace["solve"], entry) for entry in task["cases"]]
        passed = not all(outcomes["buggy_source"]) and all(outcomes["reference_source"])
        rows.append({"id": task["id"], "split": task["split"], "passed": passed,
                     "cases": len(task["cases"]),
                     "buggy_passes": sum(outcomes["buggy_source"]),
                     "reference_passes": sum(outcomes["reference_source"])})
    return {"kind": "authored_fixture_calibration", "real_model_evaluation": False,
            "material_sha256": material_hash(), "total": len(rows),
            "passed": sum(row["passed"] for row in rows), "cases": rows}


# 生成的测试完全独立，不从主项目导入评分函数，也不依赖其中的参考答案。
TEST_HELPERS = '''
def equivalent(actual, expected):
    if type(expected) is float:
        return type(actual) in (int, float) and math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9)
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(equivalent(a, b) for a, b in zip(actual, expected))
    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(equivalent(actual[key], expected[key]) for key in expected)
    return actual == expected

@pytest.mark.parametrize("entry", CASES)
def test_contract(entry):
    args = copy.deepcopy(entry["args"])
    if "error" in entry:
        with pytest.raises(ValueError):
            solution.solve(*args)
    else:
        assert equivalent(solution.solve(*args), entry["expected"])
    assert args == entry["args"], "task inputs must remain unchanged"
'''


def render_tests(cases: list[dict], *, public: bool) -> str:
    location = ('Path(__file__).with_name("task.py")' if public
                else 'Path(os.environ["HARNESS_TASK_WORKSPACE"]) / "task.py"')
    return (
        "import copy\nimport importlib.util\nimport json\nimport math\nimport os\n"
        "from pathlib import Path\nimport pytest\n\n"
        f"TASK_PATH = {location}\n"
        'spec = importlib.util.spec_from_file_location("course_task_solution", TASK_PATH)\n'
        "solution = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(solution)\n"
        f"CASES = json.loads({json.dumps(cases, ensure_ascii=False)!r})\n"
        + TEST_HELPERS
    )


def prepare_task(task_id: str, *, allow_holdout: bool = False, output_root: Path | None = None) -> dict:
    validate_materials()
    task = next((row for row in TASKS if row["id"] == task_id), None)
    if task is None:
        raise ValueError("未知 task_id")
    if task["split"] == "holdout" and not allow_holdout:
        raise ValueError("保留集尚未开放；冻结实现后显式使用 --allow-holdout")
    base = (Path(output_root) if output_root is not None else
            Path(__file__).resolve().parents[1] / ".harness/course-tasks")
    job = base.resolve() / f"{task_id}-{uuid4().hex}"
    workspace, grading = job / "workspace", job / "grading"
    workspace.mkdir(parents=True, exist_ok=False)
    grading.mkdir()
    (workspace / "task.py").write_text(task["buggy_source"], encoding="utf-8")
    (workspace / "README.md").write_text(
        f"# {task_id}: {task['title']}\n\n{task['instruction']}\n\n"
        "仅修改 task.py，保留 solve 入口。不修改传入容器。公开测试只覆盖一个案例。\n",
        encoding="utf-8",
    )
    (workspace / "test_public.py").write_text(render_tests(task["cases"][:1], public=True), encoding="utf-8")
    scoring_path = grading / "test_grading.py"
    scoring_path.write_text(render_tests(task["cases"], public=False), encoding="utf-8")
    metadata = {"id": task_id, "split": task["split"], "workspace": str(workspace),
                "grading": str(grading), "material_sha256": material_hash(),
                "grading_sha256": hashlib.sha256(scoring_path.read_bytes()).hexdigest()}
    (job / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list")
    listing.add_argument("--split", choices=["dev", "holdout"], default="dev")
    preparing = commands.add_parser("prepare")
    preparing.add_argument("--id", required=True, choices=[row["id"] for row in TASKS])
    preparing.add_argument("--allow-holdout", action="store_true")
    commands.add_parser("verify", help="只执行自编材料，不加载任何已准备工作区")
    args = parser.parse_args()
    try:
        validate_materials()
        if args.command == "list":
            for row in TASKS:
                if row["split"] == args.split:
                    print(row["id"], row["title"])
        elif args.command == "prepare":
            print(json.dumps(prepare_task(args.id, allow_holdout=args.allow_holdout), ensure_ascii=False, indent=2))
        else:
            report = verify_authored_materials()
            print(json.dumps(report, ensure_ascii=False, indent=2))
            if report["passed"] != 30:
                parser.exit(1, "材料校准未通过\n")
    except (OSError, ValueError) as error:
        parser.exit(1, f"课程任务操作失败：{error}\n")


if __name__ == "__main__":
    main()
