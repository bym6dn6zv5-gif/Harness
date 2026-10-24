# 第 9 天：结束进程以后，任务怎样继续

目标：保存一个完整回合的消息与计数，启动另一个进程继续；输入改变或预算耗尽时停止。
前置：第 3 天循环，第 4 天记录，第 6 天固定案例。今天的模型仍是固定模拟模型。

## 25 分钟：日志与检查点的区别

第 4 天结束后导出的 JSONL 方便回看。检查点还要告诉程序：任务使用哪个工作区、
已经执行到哪里、用掉多少步、接下来是否允许继续。

本课把一个任务的状态存入 SQLite 的一行记录：

| 字段 | 作用 |
| --- | --- |
| version | 检查点格式版本，本课为 1 |
| workspace | 本任务工作区的绝对路径 |
| input_hash | 输入 note.txt 内容的指纹 |
| messages | 已完成回合的消息，包括工具结果与调用 id |
| model_calls / tool_calls | 已持久化的调用计数 |
| max_steps | 原任务的模型调用上限，最终回答也占一次 |
| status / detail | 暂停、结束、预算耗尽或输入冲突及说明 |

数据库额外存 `revision`，每次成功保存就加 1。较旧版本的写入不能覆盖较新状态。
SQLite 连接需要提交事务才能保存更改；本例用参数占位符写入 JSON。
接口依据：[Python sqlite3 官方文档](https://docs.python.org/3.14/library/sqlite3.html#tutorial)。

恢复时重新创建模拟模型对象，但给它已有消息。不要从一条全新的用户消息重跑，
也不要把 `model_calls` 清零。今天先理解这个数据流，不要求背会全部 SQL。

## 55 分钟：真正分两次运行

```powershell
Set-Location -LiteralPath 'D:\python\File of python\Harness开发'
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson09 start
```

程序新建 `.harness/day09/<唯一编号>/workspace/note.txt` 和同级 `checkpoint.sqlite3`。
输入是固定三行英文。它不会改你前几天的 note.txt 或练习代码。

预期输出：`checkpointed`，模型调用 1 次、工具调用 1 次；此时完整保存了“请求读取 → 读取结果”。
程序正常退出。复制输出中的 **整条 `[恢复命令]` 后面的命令**，在 PowerShell 再执行。
也可以关闭后重新打开终端，先进入项目目录，再执行那条命令。

命令形状如下；`这里换成实际路径` 是说明文字，不能原样运行：

```text
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson09 resume --db '这里换成实际路径'
```

恢复后预期：`model_finished`，模型调用总计 **3** 次，工具调用总计 **2** 次，回答是 3 行。
第一次的读取结果被保留，第二次继续统计行数，然后给出最终回答。
同一个恢复命令再执行一次，计数不增加，因为任务已结束。

不想复制命令时，可先看自动串起两段调用的演示；它在同一进程中展示状态变化：

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson09 demo --scenario normal
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson09 demo --scenario conflict
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson09 demo --scenario budget
```

| 场景 | 恢复后的预期状态 | 模型 / 工具计数 | 原因 |
| --- | --- | --- | --- |
| normal | model_finished | 3 / 2 | 完成后续回合 |
| conflict | workspace_conflict | 1 / 1 | 演示输入改变，停止继续调用 |
| budget | step_limit | 2 / 2 | 总上限为 2，已无法再请求最终回答 |

conflict 只修改本次新建的演示输入。冲突、预算耗尽均是本课终态，不提供强制绕过；
检查原因后可以重新 `start`，创建另一份任务，不会覆盖旧检查点。
三种演示流程本身正常执行时退出码为 0。数据库路径不存在或损坏时则报错，退出 1。

打开 `mini_harness/lesson09.py`，先看 `start_task()`、`resume_task()` 与 `_continue()`：
创建初始状态 → 做一个完整回合 → 保存 → 返回暂停状态 → 重新载入 → 检查输入和预算 → 继续。
`create_checkpoint()` 等存储函数可以先当成黑盒，下次聊天再逐行讲。

然后填写 `exercises/day09_starter.py`：

1. `remaining_steps()`：用原上限减已用步数，最低为 0；拒绝负数、bool 等不合约定的值。
2. `can_resume()`：只在状态为 `checkpointed` 且输入指纹相同时返回 True。

## 20 分钟：运行检查，辨认中断窗口

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m pytest .\exercises\check_day09.py -q
& .\.venv\Scripts\python.exe -X utf8 -m pytest .\test_lessons07_09.py -k checkpoint -q
```

自己的函数完成后，第一条应为 **5 passed**。第二条检查参考实现的检查点行为。
参考测试另有“工具完成后、保存前中断”的模拟：保存失败时，数据库仍保留上一回合；
下一次恢复会重做未保存的只读调用。

这意味着本课不保证工具恰好执行一次。恢复预算保留的是**已保存的计数**，
中断窗口里实际发生却尚未保存的尝试可能没有计入。付费 API 的严格账单预算，
还需要预留调用额度、记录请求和对账；这份离线示例没有实现这些机制。

## 20 分钟：复盘限制，准备讲给别人听

本课只追踪 note.txt 的内容，最多沿用第一课的 4096 字节读取上限，
并未检测其他文件的改变。检查输入与执行工具之间也没有文件系统快照或锁，
因此不能保证并发修改期间输入始终一致。

检查点只从本机教材生成的文件读取；有格式与计数检查，但没有实现不可信状态的完整验证。
版本检查避免旧状态覆盖新状态，却不能保证两个同时运行的进程不重复调用工具。
今天只运行一个恢复进程，工具都是只读的，模型也是固定脚本；任意写入、并发执行和 API 恢复属于后续课程。

口头复述三件事：保存了什么、恢复前检查什么、在哪个中断窗口可能重做。
复习 Python 对象与磁盘文件的区别，以及事务的提交与回滚。

完成标准：

- [ ] 两次独立进程运行，得到 1/1 → 3/2 的计数。
- [ ] 看到输入冲突保持 1/1，预算演示停止于 2/2。
- [ ] 自己的两个函数通过 5 项检查。
- [ ] 能说明为什么只读调用的恢复经验不能直接照搬到写文件。

聊天入口：“我在第 9 天。start 输出……resume 输出……我觉得保存边界是……请检查。”
