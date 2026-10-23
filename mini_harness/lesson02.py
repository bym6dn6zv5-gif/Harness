"""第 2 天：注册两个只读工具，用 Pydantic 校验参数。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from mini_harness.lesson01 import execute_tool


class PathArgs(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    path: str = Field(min_length=1)

    @field_validator("path")
    @classmethod
    def reject_blank_path(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("path 不能只包含空白")
        return value  # 保留真实文件名里的空格，不擅自改写路径。


class ToolRegistry:
    """把工具名字映射到参数模型和可执行函数。"""

    def __init__(self) -> None:
        self._tools: dict[str, tuple[type[BaseModel], Callable]] = {}

    def register(self, name: str, schema: type[BaseModel], handler: Callable) -> None:
        if name in self._tools:
            raise ValueError(f"重复注册工具：{name}")
        self._tools[name] = (schema, handler)

    def dispatch(self, name: str, arguments: object, workspace: str | Path) -> dict:
        entry = self._tools.get(name)
        if entry is None:
            return {"ok": False, "error": {"code": "unknown_tool", "message": f"未注册工具：{name}"}}
        schema, handler = entry
        try:
            validated = schema.model_validate(arguments)
        except ValidationError:
            return {"ok": False, "error": {"code": "invalid_arguments", "message": "path 必须是非空白字符串，且只能提供 path。"}}
        return handler(validated, Path(workspace))

    def definitions(self) -> list[dict]:
        """教学用描述：名字与参数结构；不绑定某家模型 API。"""
        return [
            {"name": name, "parameters": schema.model_json_schema()}
            for name, (schema, _) in self._tools.items()
        ]


def read_file(args: PathArgs, workspace: Path) -> dict:
    return execute_tool("read_file", args.model_dump(), workspace)


def count_lines(args: PathArgs, workspace: Path) -> dict:
    result = read_file(args, workspace)
    if not result["ok"]:
        return result
    return {"ok": True, "data": {
        "path": args.path,
        "line_count": len(result["data"]["content"].splitlines()),
    }}


def build_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register("read_file", PathArgs, read_file)
    registry.register("count_lines", PathArgs, count_lines)
    return registry


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", default="count_lines")
    parser.add_argument("--path", default="note.txt")
    parser.add_argument("--bad-args", action="store_true", help="模拟把 path 错填为数字")
    parser.add_argument("--show-schema", action="store_true")
    parser.add_argument(
        "--workspace", type=Path,
        default=Path(__file__).resolve().parents[1] / "lessons/six_day_pack/workspace",
    )
    args = parser.parse_args()
    registry = build_registry()
    if args.show_schema:
        print(json.dumps(registry.definitions(), ensure_ascii=False, indent=2))
        return
    arguments = {"path": 123 if args.bad_args else args.path}
    print("[工具请求]", args.tool, arguments)
    print("[工具结果]", json.dumps(registry.dispatch(args.tool, arguments, args.workspace), ensure_ascii=False))


if __name__ == "__main__":
    main()
