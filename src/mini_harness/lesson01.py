"""第一课：用模拟模型观察一次工具调用。直接运行本文件即可。"""

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class ReadFileArgs(BaseModel):
    """工具接受什么参数，由程序明确规定。"""

    model_config = ConfigDict(strict=True, extra="forbid")
    path: str = Field(min_length=1)


def error_result(code: str, message: str) -> dict:
    return {"ok": False, "error": {"code": code, "message": message}}


def execute_tool(name: str, arguments: dict, workspace: Path) -> dict:
    """这是程序的工具入口：查工具、验参数、执行、返回结果。"""

    # 第一道检查：工具存在吗？模型不能凭空添加一个可执行的工具。
    if name != "read_file":
        return error_result("unknown_tool", f"没有注册这个工具：{name}")

    # 第二道检查：参数符合约定吗？严格模式不会把数字自动变成字符串。
    try:
        args = ReadFileArgs.model_validate(arguments)
    except ValidationError:
        return error_result("invalid_arguments", "path 必须是非空字符串，且不能包含其他参数。")

    # 第三道检查：文件必须在指定实验目录内，不能通过 ../ 越界读取。
    root = workspace.resolve()
    target = (root / args.path).resolve()
    if not target.is_relative_to(root):
        return error_result("path_not_allowed", "只能读取当前实验目录中的文件。")
    if not target.is_file():
        return error_result("file_not_found", "实验目录中没有找到这个文件。")

    try:
        # 只读模式；最多读取 4096 字节，避免把大文件全部装入内存。
        with target.open("rb") as file:
            raw = file.read(4097)
        if len(raw) > 4096:
            return error_result("file_too_large", "第一课只读取不超过 4096 字节的文本。")
        content = raw.decode("utf-8")
    except (OSError, UnicodeError):
        return error_result("read_failed", "文件无法读取，或不是 UTF-8 文本。")

    return {"ok": True, "data": {"path": args.path, "content": content}}


class MockModel:
    """预先写好的两种回复，用来观察数据流；这里没有真实大模型。"""

    def reply(self, messages: list[dict]) -> dict:
        latest = messages[-1]
        if latest["role"] == "user":
            # 模拟模型提出请求。它不调用 open()，也不接触文件路径对象。
            return {
                "role": "assistant",
                "tool_call": {
                    "id": "call_001",
                    "name": "read_file",
                    "arguments": {"path": "note.txt"},
                },
            }

        if latest["role"] == "tool":
            result = json.loads(latest["content"])
            if result["ok"]:
                text = "我收到的文件内容是：" + result["data"]["content"].strip()
            else:
                text = "工具调用失败：" + result["error"]["message"]
            return {"role": "assistant", "content": text}

        raise ValueError("本课只演示用户请求和工具反馈这两种输入。")


def run_demo(workspace: Path) -> list[dict]:
    model = MockModel()
    messages = [{"role": "user", "content": "请读取 note.txt，告诉我里面写了什么。"}]
    print("[1 用户请求]", messages[-1]["content"])

    first_reply = model.reply(messages)
    messages.append(first_reply)
    call = first_reply["tool_call"]
    print("[2 模型提出调用]", json.dumps(call, ensure_ascii=False))

    result = execute_tool(call["name"], call["arguments"], workspace)
    print("[3 程序执行工具]", json.dumps(result, ensure_ascii=False))

    tool_message = {
        "role": "tool",
        "tool_call_id": call["id"],
        "content": json.dumps(result, ensure_ascii=False),
    }
    messages.append(tool_message)
    print("[4 结果交回模型]", json.dumps(tool_message, ensure_ascii=False))

    final_reply = model.reply(messages)
    messages.append(final_reply)
    print("[5 模型给出回答]", final_reply["content"])
    return messages


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[2]
    demo_workspace = project_dir / "lessons" / "01_tool_call" / "workspace"
    run_demo(demo_workspace)
