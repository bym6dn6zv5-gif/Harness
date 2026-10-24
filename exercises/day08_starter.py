"""第 8 天：把进程观察结果变成工具状态，不负责启动进程。"""


def classify_process_result(timed_out: bool, returncode: int | None) -> str:
    """超时优先；未超时且退出码为 0 才成功，其他为 tool_failed。"""
    raise NotImplementedError("请完成第 8 天的进程结果分类")
