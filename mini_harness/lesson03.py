"""第 3 天：给模拟 Agent 一个明确的模型调用次数上限。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from mini_harness.lesson02 import ToolRegistry, build_registry


def tool_request(call_id: str, name: str, arguments: dict) -> dict:
    return {"role": "assistant", "tool_call": {
        "id": call_id, "name": name, "arguments": arguments,
    }}


class ReadThenCountModel:
    """固定脚本：读文件、统计行数、回答。用来观察 Harness，不是真实推理。"""

    def reply(self, messages: list[dict]) -> dict:
        results = [message for message in messages if message["role"] == "tool"]
        if not results:
            return tool_request("read_001", "read_file", {"path": "note.txt"})
        latest = json.loads(results[-1]["content"])
        if not latest["ok"]:
            return {"role": "assistant", "content": "工具失败：" + latest["error"]["message"]}
        if len(results) == 1:
            return tool_request("count_002", "count_lines", {"path": "note.txt"})
        return {"role": "assistant", "content": f"已读取 note.txt，工具统计为 {latest['data']['line_count']} 行。"}


class RepeatingModel:
    """每次都请求读取，用来检验次数上限是否真的生效。"""

    def reply(self, messages: list[dict]) -> dict:
        number = 1 + sum(message["role"] == "assistant" for message in messages)
        return tool_request(f"repeat_{number}", "read_file", {"path": "note.txt"})


def run_agent(model, workspace: str | Path, max_steps: int = 4,
              registry: ToolRegistry | None = None) -> dict:
    """一个 step 等于一次 model.reply；最终回答也占一次。"""
    if type(max_steps) is not int or max_steps < 1:
        raise ValueError("max_steps 必须是正整数")
    registry = build_registry() if registry is None else registry
    messages = [{"role": "user", "content": "读取 note.txt 并统计行数。"}]
    model_calls = 0
    tool_calls = 0
    seen_ids: set[str] = set()

    def finish(status: str, detail: str = "") -> dict:
        return {"status": status, "model_calls": model_calls,
                "tool_calls": tool_calls, "detail": detail, "messages": messages}

    for _ in range(max_steps):
        reply = model.reply(messages)
        model_calls += 1
        if not isinstance(reply, dict) or reply.get("role") != "assistant":
            return finish("invalid_response", "回复必须是 assistant 消息字典")
        messages.append(reply)

        if "tool_call" not in reply:
            content = reply.get("content")
            if not isinstance(content, str) or not content.strip():
                return finish("invalid_response", "最终回答必须包含非空文本")
            return finish("model_finished", content)

        call = reply["tool_call"]
        if (not isinstance(call, dict)
                or not isinstance(call.get("id"), str) or not call["id"].strip()
                or not isinstance(call.get("name"), str) or not call["name"].strip()
                or "arguments" not in call):
            return finish("invalid_response", "工具请求缺少有效的 id、name 或 arguments")
        if call["id"] in seen_ids:
            return finish("invalid_response", "工具调用 id 重复")
        seen_ids.add(call["id"])

        result = registry.dispatch(call["name"], call["arguments"], workspace)
        tool_calls += 1
        messages.append({"role": "tool", "tool_call_id": call["id"],
                         "content": json.dumps(result, ensure_ascii=False)})

    return finish("step_limit", "模型调用次数已达到上限")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=["normal", "repeat"], default="normal")
    parser.add_argument("--max-steps", type=int, default=4)
    parser.add_argument("--show-messages", action="store_true")
    parser.add_argument(
        "--workspace", type=Path,
        default=Path(__file__).resolve().parents[1] / "lessons/six_day_pack/workspace",
    )
    args = parser.parse_args()
    model = ReadThenCountModel() if args.scenario == "normal" else RepeatingModel()
    result = run_agent(model, args.workspace, args.max_steps)
    print("[停止状态]", result["status"])
    print("[模型调用次数]", result["model_calls"])
    print("[工具调用次数]", result["tool_calls"])
    print("[说明或回答]", result["detail"])
    if args.show_messages:
        print(json.dumps(result["messages"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
