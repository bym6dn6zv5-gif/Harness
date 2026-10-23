"""第 5 天：在消息副本里裁剪文件内容，保留原始记录与调用关系。"""

import argparse
import json
from copy import deepcopy
from pathlib import Path

from mini_harness.lesson03 import ReadThenCountModel, run_agent


def truncate_text(text: str, max_chars: int) -> tuple[str, bool]:
    if type(max_chars) is not int or max_chars < 1:
        raise ValueError("max_chars 必须是正整数")
    return text[:max_chars], len(text) > max_chars


def compact_context(messages: list[dict], max_tool_chars: int) -> list[dict]:
    truncate_text("", max_tool_chars)
    context = deepcopy(messages)
    for message in context:
        if message["role"] != "tool":
            continue
        payload = json.loads(message["content"])
        data = payload.get("data", {})
        text = data.get("content")
        if not isinstance(text, str):
            continue
        shortened, was_truncated = truncate_text(text, max_tool_chars)
        if was_truncated:
            data["content"] = shortened
            data["content_truncated"] = True
            data["original_chars"] = len(text)
            message["content"] = json.dumps(payload, ensure_ascii=False)
    return context


def serialized_chars(messages: list[dict]) -> int:
    return len(json.dumps(messages, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-tool-chars", type=int, default=12)
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[1]
    original = run_agent(ReadThenCountModel(), project / "lessons/six_day_pack/workspace")["messages"]
    context = compact_context(original, args.max_tool_chars)
    print("[原消息字符数]", serialized_chars(original))
    print("[裁剪副本字符数]", serialized_chars(context))
    print("[裁剪后的工具结果]")
    for message in context:
        if message["role"] == "tool":
            print(message["content"])


if __name__ == "__main__":
    main()
