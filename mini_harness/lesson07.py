"""第 7 天：在工具分发之前检查本次任务的许可。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from mini_harness.lesson02 import ToolRegistry, build_registry
from mini_harness.lesson03 import ReadThenCountModel, run_agent


class PolicyRegistry:
    """冻结注册名称与许可集合；权限来自宿主配置，不来自模型参数。"""

    def __init__(self, registry: ToolRegistry, allowed_tools: set[str]) -> None:
        self._registry = registry
        self._known = frozenset(row["name"] for row in registry.definitions())
        if not isinstance(allowed_tools, (set, frozenset)):
            raise ValueError("allowed_tools 必须是工具名称集合")
        if not all(isinstance(name, str) for name in allowed_tools):
            raise ValueError("工具名称必须是字符串")
        if not allowed_tools <= self._known:
            raise ValueError("许可集合包含未注册的工具")
        self._allowed = frozenset(allowed_tools)

    def definitions(self) -> list[dict]:
        return [row for row in self._registry.definitions() if row["name"] in self._allowed]

    def dispatch(self, name: str, arguments: object, workspace: str | Path) -> dict:
        if name not in self._known:
            return {"ok": False, "error": {
                "code": "unknown_tool", "message": f"未注册工具：{name}",
            }}
        if name not in self._allowed:
            return {"ok": False, "error": {
                "code": "permission_denied", "message": f"本次任务未允许工具：{name}",
            }}
        # 许可通过后，原注册表继续负责参数校验，工具继续检查文件路径。
        return self._registry.dispatch(name, arguments, workspace)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=["allowed", "denied", "unknown", "invalid", "traversal", "loop"], default="denied")
    parser.add_argument("--workspace", type=Path, default=Path(__file__).resolve().parents[1] / "lessons/six_day_pack/workspace")
    args = parser.parse_args()
    policy = PolicyRegistry(build_registry(), {"read_file"})
    if args.scenario == "loop":
        result = run_agent(ReadThenCountModel(), args.workspace, max_steps=3, registry=policy)
        print("[停止状态]", result["status"])
        print("[模型调用次数]", result["model_calls"])
        print("[工具调用尝试]", result["tool_calls"])
        print("[最终回复]", result["detail"])
        return
    name, arguments = {
        "allowed": ("read_file", {"path": "note.txt"}),
        "denied": ("count_lines", {"path": "note.txt"}),
        "unknown": ("delete_file", {"path": "note.txt"}),
        "invalid": ("read_file", {"path": 123}),
        "traversal": ("read_file", {"path": "../outside.txt"}),
    }[args.scenario]
    print("[向模型展示的工具]", [row["name"] for row in policy.definitions()])
    print("[收到的请求]", name, arguments)
    print("[工具结果]", json.dumps(policy.dispatch(name, arguments, args.workspace), ensure_ascii=False))


if __name__ == "__main__":
    main()
