# 第 7—9 天的源码与官方接口定位

核对日期：2026-10-24。这里记录教材准备时读过的入口，不代表学习者已完成源码精读。
Python 教学实现由本项目编写；不整段复制外部项目代码。

## 第 7 天：claw-code 的权限检查与执行入口

本地教材仓库：`D:\GitHub\claw-code`。
核对提交：`08106b0c3771ef5b4a5aa176acccd460e88b7325`。
权限文件的工作区内容与该提交一致，blob 为 `82abcd0a8ee13d2c7d16acd2535dba17667a792c`。

| 固定版本位置 | 本次观察 |
| --- | --- |
| [permission_enforcer.rs](https://github.com/ultraworkers/claw-code/blob/08106b0c3771ef5b4a5aa176acccd460e88b7325/rust/crates/runtime/src/permission_enforcer.rs) 的 EnforcementResult、PermissionEnforcer::check | 允许和拒绝有独立结果，拒绝带原因 |
| [lib.rs](https://github.com/ultraworkers/claw-code/blob/08106b0c3771ef5b4a5aa176acccd460e88b7325/rust/crates/claw-analog/src/lib.rs) 的 enforce_tool（约 1674 行） | 将检查结果转换为调用方的成功或错误 |
| 同一 lib.rs 的 dispatch_tool / read_file（约 1953—1980 行） | 先处理权限拒绝，再取路径、检查工作区，最后读取 |

先只画出 read_file 分支中“检查 → 拒绝返回 / 继续读取”的两条线，
再与 `mini_harness/lesson07.py` 的 `dispatch()` 比较。

阅读限制也要记下：该版本 `check()` 在 Prompt 模式下交给调用方的交互流程处理；
`enforce_tool()` 的 enforcer 参数为空时会直接返回成功。
因此不能只看一个结构体的名字，就断言所有执行路径都经过同样的权限判断。
本课简化为宿主明确提供名称集合，不实现交互批准或完整策略引擎。

Codex 的路由入口继续沿用 [前六天固定版本定位](../six_day_pack/source-reading.md)。
这次没有据此推断 Codex 的完整权限体系，也没有把本课 SQLite 实现归因于 Codex。

## 第 8 天：Python 进程接口

- [subprocess.run](https://docs.python.org/3.14/library/subprocess.html#subprocess.run)：本课用固定参数列表启动 worker，并设置 timeout。
- [Future.cancel](https://docs.python.org/3.14/library/concurrent.futures.html#concurrent.futures.Future.cancel)：已经运行的任务不能靠此方法直接取消；不要把等待超时当成线程终止。

官方 3.14 文档会随补丁版本更新；本机实际验证环境是 Python 3.14.6。
本课没有实现任意命令执行器或后代进程管理。

## 第 9 天：SQLite 与自己的状态机

- [sqlite3 教程](https://docs.python.org/3.14/library/sqlite3.html#tutorial)：连接、提交事务和参数占位符。
- 本项目 `mini_harness/lesson09.py`：`Checkpoint`、`start_task`、`resume_task`、`_continue`。

先认识存储的内容与保存边界，再学习具体 SQL。
“版本检查”“恢复时保留计数”“输入冲突停止”来自本教学实现；其验证场景见
[备课核验](verification.md)，范围限于单任务、固定模型和只读工具。
