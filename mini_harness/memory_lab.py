"""Hermes 机制的自编内存实验；无网络、无落盘，不导入或运行 Hermes。"""

from __future__ import annotations

from copy import deepcopy
import json


class LabError(ValueError):
    """教学实验的可预期操作错误。"""


class MemoryLab:
    """只模拟快照、唯一片段修改与最终预算事务，不是完整记忆存储。"""

    separator = "\n§\n"

    def __init__(self, entries: list[str], limit: int = 2200):
        if type(limit) is not int or limit <= 0:
            raise LabError("limit 必须为正整数")
        if not isinstance(entries, list):
            raise LabError("entries 必须为列表")
        self.limit = limit
        self._entries = [self._text(entry) for entry in entries]
        self._check_budget(self._entries)
        self.reload()

    @staticmethod
    def _text(value: object) -> str:
        if not isinstance(value, str) or not value.strip():
            raise LabError("文本必须是非空字符串")
        if MemoryLab.separator in value:
            raise LabError("本实验条目不能包含分隔符")
        return value

    @property
    def entries(self) -> list[str]:
        return list(self._entries)

    @property
    def snapshot(self) -> tuple[str, ...]:
        return self._snapshot

    def reload(self) -> None:
        """显式边界：从当前活跃条目重新生成提示快照。"""
        self._snapshot = tuple(self._entries)

    def _check_budget(self, entries: list[str]) -> None:
        if len(self.separator.join(entries)) > self.limit:
            raise LabError("超过字符预算")

    @staticmethod
    def _locate(entries: list[str], old: str) -> int:
        exact = [i for i, entry in enumerate(entries) if entry == old]
        matches = exact or [i for i, entry in enumerate(entries) if old in entry]
        if len(matches) != 1:
            raise LabError("目标必须唯一匹配一条")
        return matches[0]

    def apply(self, operations: list[dict]) -> dict:
        """在副本上验证，全部成功且最终预算满足后提交；失败不改变任何状态。"""
        before = self.entries
        try:
            if not isinstance(operations, list) or not operations:
                raise LabError("operations 必须是非空列表")
            working = deepcopy(before)
            for op in operations:
                if not isinstance(op, dict):
                    raise LabError("每个操作必须为对象")
                action = op.get("action")
                if action == "add":
                    content = self._text(op.get("content"))
                    if content not in working:
                        working.append(content)
                elif action in ("patch", "remove"):
                    old = self._text(op.get("old_text"))
                    index = self._locate(working, old)
                    if action == "remove":
                        working.pop(index)
                    else:
                        content = self._text(op.get("content"))
                        if working[index].count(old) != 1:
                            raise LabError("同一条内的匹配片段必须只出现一次")
                        working[index] = working[index].replace(old, content, 1)
                else:
                    raise LabError("动作仅支持 add、patch、remove")
            self._check_budget(working)
        except LabError as error:
            return {"ok": False, "error": str(error)}
        self._entries = working
        return {"ok": True, "characters": len(self.separator.join(working))}


def main() -> None:
    lab = MemoryLab(["项目语言是 Python"])
    print("初始快照：", lab.snapshot)
    print("写入结果：", json.dumps(lab.apply([
        {"action": "add", "content": "用户偏好中文"},
    ]), ensure_ascii=False))
    print("写入后的活跃条目：", lab.entries)
    print("写入后仍冻结的快照：", lab.snapshot)
    lab.reload()
    print("显式重新加载后的快照：", lab.snapshot)
    lab.apply([{"action": "add", "content": "另一项目也使用 Python"}])
    print("模糊 patch：", lab.apply([
        {"action": "patch", "old_text": "Python", "content": "其他语言"},
    ]))
    before = lab.entries
    print("故意失败的批次：", lab.apply([
        {"action": "remove", "old_text": "用户偏好中文"},
        {"action": "patch", "old_text": "不存在的事实", "content": "新事实"},
    ]))
    print("失败后活跃状态完整保留：", lab.entries == before)


if __name__ == "__main__":
    main()
