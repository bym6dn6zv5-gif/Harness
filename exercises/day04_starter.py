"""第 4 天：从导出的记录中统计工具反馈消息。"""


def count_tool_messages(records: list[dict]) -> int:
    """只计入 type=message 且 message.role=tool 的记录，忽略 summary。"""
    raise NotImplementedError("请补记录筛选与计数")
