"""第一课：模型提出工具调用，Harness 执行工具并回传结果。

本课使用模拟模型，无需 API Key。read_file 只接受工作目录内的相对路径，
最多读取 4096 字节，按 UTF-8 解码并保留原始换行。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

MAX_FILE_BYTES = 4096


def _error(code: str, message: str) -> dict[str, Any]:
    return {"ok": False, "error": {"code": code, "message": message}}


def execute_tool(
    name: str, arguments: object, workspace: str | Path
) -> dict[str, Any]:
    """检查工具名和参数，执行读取，并返回统一格式的结果。"""
    if name != "read_file":
        return _error("unknown_tool", f"未注册工具：{name}")

    # 在访问文件之前校验参数；不接受缺失参数、额外参数或非字符串路径。
    if (
        not isinstance(arguments, dict)
        or set(arguments) != {"path"}
        or not isinstance(arguments["path"], str)
        or not arguments["path"].strip()
    ):
        return _error(
            "invalid_arguments",
            "read_file 需要且只接受一个非空字符串参数 path。",
        )

    requested_path = arguments["path"]
    try:
        relative_path = Path(requested_path)
        if relative_path.is_absolute() or relative_path.drive or relative_path.root:
            return _error("path_not_allowed", "只允许读取工作目录内的相对路径。")

        root = Path(workspace).resolve()
        target = (root / relative_path).resolve()
        # resolve 会解析 .. 和符号链接，再检查最终路径是否仍在工作目录内。
        if not target.is_relative_to(root):
            return _error("path_not_allowed", "路径超出了工作目录。")

        if not target.is_file():
            if not target.exists():
                return _error("file_not_found", "未找到文件")
            return _error("read_failed", "目标不是普通文件。")

        # 二进制读取可以保留 CRLF，同时避免将过大的文件整个载入内存。
        with target.open("rb") as source:
            data = source.read(MAX_FILE_BYTES + 1)
        if len(data) > MAX_FILE_BYTES:
            return _error("file_too_large", f"文件不能超过 {MAX_FILE_BYTES} 字节。")
        content = data.decode("utf-8")
    except FileNotFoundError:
        return _error("file_not_found", "未找到文件")
    except (OSError, UnicodeError, ValueError, RuntimeError):
        return _error("read_failed", "读取失败：请检查文件路径、权限和 UTF-8 编码。")

    return {"ok": True, "data": {"path": requested_path, "content": content}}


class MockModel:
    """用确定的回复演示工具调用，不向外部服务发送请求。"""

    def reply(self, messages: list[dict[str, Any]]) -> dict[str, Any]:
        if messages and messages[-1].get("role") == "tool":
            result = json.loads(messages[-1]["content"])
            if result["ok"]:
                content = f"文件内容：{result['data']['content']}"
            else:
                content = f"工具调用失败：{result['error']['message']}"
            return {"role": "assistant", "content": content}

        return {
            "role": "assistant",
            "content": "我需要调用 read_file 读取 note.txt。",
            "tool_call": {
                "id": "call_001",
                "name": "read_file",
                "arguments": {"path": "note.txt"},
            },
        }


def run_demo(workspace: str | Path) -> list[dict[str, Any]]:
    """演示一轮工具调用，并返回完整消息记录供观察和测试。"""
    model = MockModel()
    messages: list[dict[str, Any]] = [
        {"role": "user", "content": "请读取工作目录里的 note.txt。"}
    ]
    print("[1 用户提出请求]", messages[0]["content"])

    assistant_message = model.reply(messages)
    messages.append(assistant_message)
    tool_call = assistant_message["tool_call"]
    print("[2 模型请求工具]", tool_call["name"], tool_call["arguments"])

    result = execute_tool(tool_call["name"], tool_call["arguments"], workspace)
    print("[3 Harness 执行工具]", json.dumps(result, ensure_ascii=False))

    messages.append({
        "role": "tool",
        "tool_call_id": tool_call["id"],
        "content": json.dumps(result, ensure_ascii=False),
    })
    print("[4 工具结果回传模型]")

    final_message = model.reply(messages)
    messages.append(final_message)
    print("[5 模型给出回答]", final_message["content"])
    return messages


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="运行第一课的模拟工具调用流程。")
    parser.add_argument(
        "--workspace", type=Path, default=Path.cwd(),
        help="包含 note.txt 的工作目录，默认为当前目录。",
    )
    run_demo(parser.parse_args().workspace)
