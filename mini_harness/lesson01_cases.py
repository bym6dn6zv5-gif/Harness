"""第 1 天：不修改原实验，观察四种固定的工具请求。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from mini_harness.lesson01 import MockModel, execute_tool


CASES = {
    "normal": ("read_file", {"path": "note.txt"}),
    "missing": ("read_file", {"path": "missing.txt"}),
    "invalid": ("read_file", {"path": 123}),
    "unknown": ("delete_file", {"path": "note.txt"}),
}


def classify_result(result: dict) -> str:
    """把工具结果概括为 success 或具体错误码。"""
    if result["ok"]:
        return "success"
    return result["error"]["code"]


def run_case(case: str, workspace: str | Path) -> dict:
    name, arguments = CASES[case]
    call = {"id": "case_001", "name": name, "arguments": arguments.copy()}
    messages = [
        {"role": "user", "content": "请读取 note.txt。"},
        {"role": "assistant", "tool_call": call},
    ]
    result = execute_tool(name, arguments, workspace)
    messages.append({
        "role": "tool",
        "tool_call_id": call["id"],
        "content": json.dumps(result, ensure_ascii=False),
    })
    final_reply = MockModel().reply(messages)
    messages.append(final_reply)
    return {"case": case, "tool_result": result, "messages": messages}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=CASES, default="normal")
    parser.add_argument(
        "--workspace", type=Path,
        default=Path(__file__).resolve().parents[1] / "lessons/six_day_pack/workspace",
    )
    args = parser.parse_args()
    result = run_case(args.case, args.workspace)
    print("[模拟请求]", json.dumps(result["messages"][1]["tool_call"], ensure_ascii=False))
    print("[工具结果]", json.dumps(result["tool_result"], ensure_ascii=False))
    print("[回传消息]", json.dumps(result["messages"][2], ensure_ascii=False))
    print("[模拟回答]", result["messages"][3]["content"])


if __name__ == "__main__":
    main()
