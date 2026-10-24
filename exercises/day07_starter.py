"""第 7 天：只补这个判断函数，不需要修改参考工具或权限配置。"""


def permission_code(name: str, known_tools: set[str], allowed_tools: set[str]) -> str:
    """先判注册，再判许可；返回 unknown_tool、permission_denied 或 allowed。"""
    raise NotImplementedError("请完成第 7 天的许可判断")
