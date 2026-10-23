"""第 2 天：工具查找与参数校验；所需导入已经提供。"""

from pydantic import ValidationError
from mini_harness.lesson02 import PathArgs


def choose_handler(registry: dict, name: str):
    """返回已注册的函数本身；工具不存在时返回 None，不执行函数。"""
    raise NotImplementedError("请补工具查找逻辑")


def validate_arguments(arguments: object) -> bool:
    """用 PathArgs 检查参数；有效返回 True，ValidationError 时返回 False。"""
    raise NotImplementedError("请补参数校验逻辑")
