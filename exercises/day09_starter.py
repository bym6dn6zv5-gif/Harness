"""第 9 天：预算计算与恢复条件。这里只写纯函数，不操作数据库。"""


def remaining_steps(max_steps: int, used_steps: int) -> int:
    """仅接受整数（不含 bool），上限 >=1，已用 >=0；剩余数最低为 0。"""
    raise NotImplementedError("请完成第 9 天的剩余预算计算")


def can_resume(saved_hash: str, current_hash: str, status: str) -> bool:
    """仅 checkpointed 且输入指纹一致时允许继续；假设指纹字符串已校验。"""
    raise NotImplementedError("请完成第 9 天的恢复条件")
