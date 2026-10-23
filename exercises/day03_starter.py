"""第 3 天：停止条件与工具反馈；暂时不用独立重写完整循环。"""

import json


def should_continue(model_calls: int, max_steps: int, has_final_answer: bool) -> bool:
    """本题输入为合法非负计数和正整数上限。已有最终回答或达到上限时停止。"""
    raise NotImplementedError("请补停止条件")


def make_tool_message(call_id: str, result: dict) -> dict:
    """返回 role、tool_call_id、content 三项；content 是 JSON 文本。"""
    raise NotImplementedError("请补工具反馈消息")
