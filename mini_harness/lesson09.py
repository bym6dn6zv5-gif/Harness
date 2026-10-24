"""第 9 天：把只读模拟任务存入 SQLite，再由另一进程恢复。"""

from __future__ import annotations

import argparse
from contextlib import closing
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, StrictInt

from mini_harness.lesson01 import execute_tool
from mini_harness.lesson02 import build_registry
from mini_harness.lesson03 import ReadThenCountModel


class Checkpoint(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: Literal[1] = 1
    workspace: str
    input_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    max_steps: StrictInt = Field(ge=1)
    model_calls: StrictInt = Field(ge=0)
    tool_calls: StrictInt = Field(ge=0)
    status: Literal["checkpointed", "model_finished", "step_limit", "workspace_conflict"]
    detail: str = ""
    messages: list[dict]


def input_fingerprint(workspace: str | Path) -> str:
    """本课任务只依赖 note.txt；不是整个仓库的指纹。"""
    result = execute_tool("read_file", {"path": "note.txt"}, workspace)
    if not result["ok"]:
        raise ValueError("note.txt 不可读取：" + result["error"]["code"])
    return hashlib.sha256(result["data"]["content"].encode("utf-8")).hexdigest()


def _connect(path: Path, mode: str) -> sqlite3.Connection:
    # mode=rw/ro 让恢复时路径写错直接报错，而不是悄悄创建空数据库。
    return sqlite3.connect(path.resolve().as_uri() + f"?mode={mode}", uri=True)


def create_checkpoint(path: Path, state: Checkpoint) -> None:
    path = Path(path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb"):
        pass  # 独占创建；已有数据库不得覆盖。
    with closing(_connect(path, "rw")) as connection, connection:
        connection.execute("CREATE TABLE checkpoint (id INTEGER PRIMARY KEY CHECK(id=1), revision INTEGER NOT NULL, payload TEXT NOT NULL)")
        connection.execute("INSERT INTO checkpoint VALUES (1, 0, ?)", (state.model_dump_json(),))


def load_checkpoint(path: Path) -> tuple[Checkpoint, int]:
    with closing(_connect(Path(path), "ro")) as connection:
        row = connection.execute("SELECT payload, revision FROM checkpoint WHERE id=1").fetchone()
    if row is None:
        raise ValueError("检查点没有任务状态")
    state = Checkpoint.model_validate_json(row[0])
    # 验证恢复所依赖的计数关系；不是不可信检查点的完整验证器。
    assistant_count = sum(message.get("role") == "assistant" for message in state.messages)
    tool_count = sum(message.get("role") == "tool" for message in state.messages)
    if (state.model_calls != assistant_count or state.tool_calls != tool_count
            or state.model_calls > state.max_steps):
        raise ValueError("检查点计数与历史不一致")
    return state, row[1]


def save_checkpoint(path: Path, state: Checkpoint, expected_revision: int) -> int:
    with closing(_connect(Path(path), "rw")) as connection, connection:
        cursor = connection.execute(
            "UPDATE checkpoint SET payload=?, revision=revision+1 WHERE id=1 AND revision=?",
            (state.model_dump_json(), expected_revision),
        )
        if cursor.rowcount != 1:
            raise ValueError("检查点版本冲突：请停止重复运行的进程")
    return expected_revision + 1


def _continue(path: Path, state: Checkpoint, revision: int, pause_after: int | None) -> Checkpoint:
    if pause_after is not None and (type(pause_after) is not int or pause_after < 1):
        raise ValueError("pause_after 必须是正整数或 None")
    model, registry = ReadThenCountModel(), build_registry()
    additional_calls = 0
    while state.status == "checkpointed":
        try:
            unchanged = input_fingerprint(state.workspace) == state.input_hash
        except ValueError:
            unchanged = False
        if not unchanged:
            state.status, state.detail = "workspace_conflict", "输入 note.txt 已改变或无法读取；请检查后新建任务。"
        elif state.model_calls >= state.max_steps:
            state.status, state.detail = "step_limit", "已用步数达到原任务上限，恢复不会重置预算。"
        elif pause_after is not None and additional_calls >= pause_after:
            return state  # 上一轮已经保存到数据库，此时是明确的暂停边界。
        else:
            reply = model.reply(state.messages)
            state.messages.append(reply)
            state.model_calls += 1
            additional_calls += 1
            if "tool_call" in reply:
                call = reply["tool_call"]
                result = registry.dispatch(call["name"], call["arguments"], state.workspace)
                state.tool_calls += 1
                state.messages.append({"role": "tool", "tool_call_id": call["id"],
                                       "content": json.dumps(result, ensure_ascii=False)})
            else:
                state.status, state.detail = "model_finished", reply["content"]
        # 一个完整回合之后才保存：不保存“工具调用尚无结果”的中间历史。
        revision = save_checkpoint(path, state, revision)
    return state


def start_task(path: Path, workspace: Path, *, max_steps: int = 3,
               pause_after: int | None = 1) -> Checkpoint:
    if type(max_steps) is not int or max_steps < 1:
        raise ValueError("max_steps 必须是正整数")
    if pause_after is not None and (type(pause_after) is not int or pause_after < 1):
        raise ValueError("pause_after 必须是正整数或 None")
    workspace = Path(workspace).resolve()
    state = Checkpoint(workspace=str(workspace), input_hash=input_fingerprint(workspace),
                       max_steps=max_steps, model_calls=0, tool_calls=0, status="checkpointed",
                       messages=[{"role": "user", "content": "读取 note.txt 并统计行数。"}])
    create_checkpoint(path, state)
    return _continue(path, state, 0, pause_after)


def resume_task(path: Path, *, pause_after: int | None = None) -> Checkpoint:
    state, revision = load_checkpoint(path)
    # 已结束、预算耗尽、输入冲突的任务都不会重新执行工具。
    return _continue(path, state, revision, pause_after)


def _show(state: Checkpoint, path: Path) -> None:
    print("[检查点]", path)
    print("[状态]", state.status)
    print("[模型调用次数]", state.model_calls)
    print("[工具调用次数]", state.tool_calls)
    print("[说明]", state.detail)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    start = commands.add_parser("start", help="创建独立三行输入，执行一回合并保存")
    start.add_argument("--max-steps", type=int, default=3)
    resume = commands.add_parser("resume", help="从指定 SQLite 数据库继续")
    resume.add_argument("--db", type=Path, required=True)
    demo = commands.add_parser("demo", help="自动展示两段运行或冲突，不修改已有练习输入")
    demo.add_argument("--scenario", choices=["normal", "conflict", "budget"], default="normal")
    args = parser.parse_args()
    try:
        if args.command == "resume":
            _show(resume_task(args.db), args.db.resolve())
            return
        root = Path(__file__).resolve().parents[1] / ".harness/day09" / uuid4().hex
        workspace = root / "workspace"
        workspace.mkdir(parents=True)
        (workspace / "note.txt").write_bytes(b"alpha\nbeta\ngamma\n")
        path = root / "checkpoint.sqlite3"
        max_steps = args.max_steps if args.command == "start" else (2 if args.scenario == "budget" else 3)
        _show(start_task(path, workspace, max_steps=max_steps), path)
        if args.command == "start":
            print("[恢复命令] & .\\.venv\\Scripts\\python.exe -X utf8 -m mini_harness.lesson09 resume --db '" + str(path) + "'")
            return
        if args.scenario == "conflict":
            (workspace / "note.txt").write_bytes(b"changed only in this fresh demo workspace\n")
        print("[继续任务]")
        _show(resume_task(path), path)
    except (OSError, ValueError, sqlite3.Error) as error:
        parser.exit(1, f"检查点操作失败：{error}\n")


if __name__ == "__main__":
    main()
