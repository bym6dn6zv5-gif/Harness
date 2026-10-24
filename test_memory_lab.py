"""验证教学记忆机制的边界；不需要 Hermes、模型服务或个人记忆。"""

import pytest

from mini_harness.memory_lab import LabError, MemoryLab


def test_write_changes_live_state_but_not_snapshot_until_explicit_reload():
    lab = MemoryLab(["原事实"])
    assert lab.apply([{"action": "add", "content": "新事实"}])["ok"]
    assert lab.entries == ["原事实", "新事实"]
    assert lab.snapshot == ("原事实",)
    lab.reload()
    assert lab.snapshot == ("原事实", "新事实")


def test_callers_cannot_mutate_live_state_through_returned_list():
    entries = ["原事实"]
    lab = MemoryLab(entries)
    entries.append("偷偷修改")
    lab.entries.append("另一次偷偷修改")
    assert lab.entries == ["原事实"]


def test_patch_preserves_other_facts():
    lab = MemoryLab(["路径在 D 盘，语言为 Python，每天两小时"])
    assert lab.apply([{"action": "patch", "old_text": "Python", "content": "Rust"}])["ok"]
    assert lab.entries == ["路径在 D 盘，语言为 Rust，每天两小时"]


@pytest.mark.parametrize("entries,old", [
    (["Python 教学", "Python 项目"], "Python"),
    (["Python Python"], "Python"),
    (["Python 教学"], "不存在"),
])
def test_ambiguous_repeated_or_missing_patch_rolls_back(entries, old):
    lab = MemoryLab(entries)
    assert not lab.apply([{"action": "patch", "old_text": old, "content": "Rust"}])["ok"]
    assert lab.entries == entries


def test_exact_entry_wins_over_substring():
    lab = MemoryLab(["Python", "另一个 Python 项目"])
    assert lab.apply([{"action": "patch", "old_text": "Python", "content": "Rust"}])["ok"]
    assert lab.entries == ["Rust", "另一个 Python 项目"]


def test_separator_counts_against_character_budget():
    lab = MemoryLab(["甲"], limit=4)
    assert not lab.apply([{"action": "add", "content": "乙"}])["ok"]
    assert lab.entries == ["甲"]


def test_batch_can_temporarily_exceed_capacity_but_final_state_must_fit():
    lab = MemoryLab(["abc"], limit=3)
    assert lab.apply([
        {"action": "add", "content": "xyz"},
        {"action": "remove", "old_text": "abc"},
    ])["ok"]
    assert lab.entries == ["xyz"]


def test_failed_second_operation_does_not_commit_first():
    lab = MemoryLab(["abc"])
    assert not lab.apply([
        {"action": "remove", "old_text": "abc"},
        {"action": "remove", "old_text": "missing"},
    ])["ok"]
    assert lab.entries == ["abc"]


@pytest.mark.parametrize("operation", [
    {"action": "add", "content": 42},
    {"action": "patch", "old_text": "abc", "content": ""},
    {"action": "replace", "old_text": "abc", "content": "xyz"},
    {"action": "add", "content": "a\n§\nb"},
])
def test_invalid_operations_do_not_write(operation):
    lab = MemoryLab(["abc"])
    assert not lab.apply([operation])["ok"]
    assert lab.entries == ["abc"]


def test_duplicate_add_is_idempotent():
    lab = MemoryLab(["abc"])
    assert lab.apply([{"action": "add", "content": "abc"}])["ok"]
    assert lab.entries == ["abc"]


def test_invalid_initial_budget_is_rejected():
    with pytest.raises(LabError):
        MemoryLab(["abc"], limit=True)
