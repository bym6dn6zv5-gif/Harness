"""第 7—9 天参考答案。先自己写，再按讲义中的提示逐级查看。"""


def permission_code(name: str, known_tools: set[str], allowed_tools: set[str]) -> str:
    if name not in known_tools:
        return "unknown_tool"
    if name not in allowed_tools:
        return "permission_denied"
    return "allowed"


def classify_process_result(timed_out: bool, returncode: int | None) -> str:
    if timed_out:
        return "tool_timeout"
    return "success" if returncode == 0 else "tool_failed"


def remaining_steps(max_steps: int, used_steps: int) -> int:
    if type(max_steps) is not int or type(used_steps) is not int or max_steps < 1 or used_steps < 0:
        raise ValueError("需要正整数上限和非负整数已用步数")
    return max(0, max_steps - used_steps)


def can_resume(saved_hash: str, current_hash: str, status: str) -> bool:
    return status == "checkpointed" and saved_hash == current_hash
