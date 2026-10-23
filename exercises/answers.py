"""六天练习的参考答案。先尝试 starter，再来对照。"""

import json

from pydantic import ValidationError
from mini_harness.lesson02 import PathArgs


def classify_result(result: dict) -> str:
    if result["ok"]:
        return "success"
    return result["error"]["code"]


def choose_handler(registry: dict, name: str):
    return registry.get(name)


def validate_arguments(arguments: object) -> bool:
    try:
        PathArgs.model_validate(arguments)
    except ValidationError:
        return False
    return True


def should_continue(model_calls: int, max_steps: int, has_final_answer: bool) -> bool:
    return not has_final_answer and model_calls < max_steps


def make_tool_message(call_id: str, result: dict) -> dict:
    return {"role": "tool", "tool_call_id": call_id,
            "content": json.dumps(result, ensure_ascii=False)}


def count_tool_messages(records: list[dict]) -> int:
    count = 0
    for record in records:
        if record.get("type") == "message" and record["message"].get("role") == "tool":
            count += 1
    return count


def truncate_text(text: str, max_chars: int) -> tuple[str, bool]:
    return text[:max_chars], len(text) > max_chars


def grade_case(case_id: str, expected: str, observed: str) -> dict:
    return {"id": case_id, "expected": expected, "observed": observed, "passed": expected == observed}
