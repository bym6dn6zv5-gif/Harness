# 第 4 天：从终端输出走到消息记录

目标：知道 JSONL 怎样保存记录，能从消息快照里数出工具反馈并还原顺序。
前置：第 3 天的消息列表与停止状态。不需要学习数据库。

## 25 分钟：JSON 与 JSONL

终端输出便于当时观察。为了之后排错，可以把运行中的数据保存下来。
JSONL 的规则很简单：**每一行是一个完整 JSON 值**。本课每一行保存一个字典。

```json
{"type": "message", "sequence": 1, "message": {"role": "user", "content": "任务"}}
{"type": "summary", "status": "model_finished", "model_calls": 3, "tool_calls": 2}
```

第一行是消息记录；第二行是运行摘要。`type` 描述记录种类，嵌套的 `message.role` 描述消息角色。
两者不是同一层的信息。

本课在运行结束后导出 `messages` 快照，最后写摘要。它还没有实时逐步写入、每步耗时或断点恢复；
若运行中途崩溃，还不能依靠这份结束后才写的快照恢复工作。

## 55 分钟：生成与观察

```powershell
Set-Location -LiteralPath 'D:\python\File of python\Harness开发'
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson04 --scenario normal --show-trace
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson04 --scenario repeat --show-trace
```

| 场景 | 状态 | 消息数 | 加上摘要后的记录条数 | 工具反馈数 |
| --- | --- | --- | --- | --- |
| normal | `model_finished` | 6 | 7 | 2 |
| repeat | `step_limit` | 7 | 8 | 3 |

每次运行都会在 `.harness/day04` 生成一个新名字的 `.jsonl` 文件，并把完整路径打印出来。
`--show-trace` 直接在终端显示这些记录，先不必操作文件管理器。
文件名会变化，属于正常现象；数据不会上传到 GitHub。

打开 `mini_harness/lesson04.py`，先读 `save_trace()`：

1. 创建输出目录。
2. 每条消息配一个顺序号，`json.dumps(...) + "\n"` 写一行。
3. 最后写摘要。

再读 `load_trace()`：逐行读取，用 `json.loads(line)` 解析。不能把多行 JSON 对象直接当成一个 JSON 数组。
内容里的换行会由 JSON 转义，因此一条记录仍保持在文件的一行上。

打开 `exercises/day04_starter.py`，补 `count_tool_messages(records)`：

- 先检查记录的 `type` 是否为 `message`。
- 再看内部消息的 `role` 是否为 `tool`。
- 满足两个条件才加一，忽略摘要和模型的工具请求。

重点：assistant 发起工具请求，与 tool 返回执行结果，是两种消息。

## 20 分钟：验证

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m pytest .\exercises\check_day04.py -q
```

完成后应有 **2 passed**。一个测试包含 user、assistant、tool 和 summary，检查有没有数错层级。

挑 normal 的一次输出，在纸上标出：用户任务、第一次模型请求、读取反馈、第二次模型请求、统计反馈、最终回答。
检查每条工具反馈里的调用标识能否与对应请求匹配。

## 20 分钟：基础与复盘

练习 `for record in records` 和 `count += 1`。解释一个列表中的元素为什么可以是嵌套字典。
再回答：有记录是否等于支持恢复？如果缺少实时写入，运行崩溃时会少什么？

完成标准：

- [ ] normal 与 repeat 的记录条数符合表格。
- [ ] 统计函数通过检查。
- [ ] 能区分消息快照、实时日志和恢复能力。

聊天模板：

```text
我在第 4 天。normal 的记录有……条，repeat 有……条。
我数的工具反馈分别有……条。
我认为结束后导出记录还不能恢复中断，是因为……
请带我读一条嵌套记录，再让我自己解释下一条。
```
