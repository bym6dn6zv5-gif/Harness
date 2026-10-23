# 第 3 天：给 Agent 循环一个上限

目标：看懂“继续请求模型”这一步，能区分最终回答、次数耗尽和格式错误。
今天先体验一个小循环，后续周路线会继续学习恢复、超时和更完整的运行管理。

## 25 分钟：循环为什么需要停止条件

前两天由程序写好单次流程。今天模拟模型先要求读文件，再要求统计行数，最后回答。
每次工具结果都加入历史，然后再次调用模型。

```text
请求模型 → 得到最终回答？是：停止
    ↓ 否，得到工具请求
检查并执行工具 → 反馈加入历史 → 检查次数上限 → 再请求模型
```

本课规定：**一次 step 等于一次 `model.reply()`，最终回答也占一次。**
正常脚本需要 3 次模型调用：提出读取、提出统计、给出回答；工具调用为 2 次。

| 状态 | 含义 |
| --- | --- |
| `model_finished` | 模型给出了最终文本，循环结束 |
| `step_limit` | 达到模型调用次数上限 |
| `invalid_response` | 回复结构不符合本课约定，或调用 id 重复 |

`model_finished` 只表示拿到最终文本。它不证明答案正确、代码修好了，或外部评分通过。
工具返回错误后，模拟模型也可以报告失败并结束。

## 55 分钟：预测三个实验

```powershell
Set-Location -LiteralPath 'D:\python\File of python\Harness开发'
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson03 --scenario normal --max-steps 3 --show-messages
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson03 --scenario normal --max-steps 2
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson03 --scenario repeat --max-steps 3
```

| 实验 | 停止状态 | 模型调用 | 工具调用 |
| --- | --- | --- | --- |
| normal，上限 3 | `model_finished` | 3 | 2 |
| normal，上限 2 | `step_limit` | 2 | 2 |
| repeat，上限 3 | `step_limit` | 3 | 3 |

第二个实验虽然做完了两次工具调用，但预算里没有第三次模型调用，不能凭空添加最终回答。
第三个实验的模拟模型总想继续读，程序仍必须按上限停止。

打开 `mini_harness/lesson03.py`，第一遍只找：

1. `for _ in range(max_steps)`：允许多少次模型请求。
2. `messages.append(reply)`：保存模型回复。
3. 没有 `tool_call` 时的最终回答分支。
4. `registry.dispatch(...)` 和追加工具反馈的代码。
5. 循环用完后的 `step_limit`。

`model_calls` 和 `tool_calls` 是不同计数，返回错误的工具调用也计入尝试次数。
格式校验和重复 id 检查可以第二遍再看；暂时不用重写整个参考文件。

打开 `exercises/day03_starter.py`，补停止条件和消息构造两个小函数。
已有最终回答，或 `model_calls >= max_steps` 时，`should_continue` 返回 `False`。
`make_tool_message` 要保留调用 id，并用 `json.dumps` 把工具结果放进文本字段。

## 20 分钟：验证与对照真实循环

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m pytest .\exercises\check_day03.py -q
```

完成后应有 **3 passed**。

可选看 [claw-code 循环定位](source-reading.md#第-3-天claw-code-循环)。
先找轮次上限、收集工具请求、分发和结果回传。真实工程的消息协议与教学字典可能不同，
重点跟踪调用标识和反馈进入历史的位置。

本课的次数限制只在调用之间生效；若单次模型或工具调用一直阻塞，单靠 `max_steps` 无法打断它。
调用超时会在之后的运行约束课程中学习。

## 20 分钟：基础与复盘

手算 `range(3)` 有几次迭代；说明 `return` 为什么能立刻退出函数。
再解释正常场景为什么是 3 次模型调用、2 次工具调用。

完成标准：

- [ ] 三个场景的状态和计数与预测一致。
- [ ] 自己的停止条件与反馈消息通过检查。
- [ ] 能区分“模型结束回答”和“任务得到验证”。

聊天模板：

```text
我在第 3 天。三个场景的状态和计数是……
我把一次 step 理解为……
练习检查是……
请带我跟踪一次循环，先不要扩展到多 Agent。
```
