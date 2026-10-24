# 第 8 天：工具一直不返回，Harness 怎样停止等待

目标：观察一个固定子进程的完成、超时和参数错误，学会把这些情况转换为结构化工具结果。
前置：异常处理、工具错误。今天先不运行测试命令或模型生成的代码。

## 25 分钟：步数限制不能约束单次等待

第 3 天的 `max_steps` 只能限制请求次数。如果一次工具调用永远不返回，
循环也到不了下一步。时间上限和次数上限解决不同的问题。

本课分成两个程序：父进程是 `lesson08.py`，固定子进程是 `timeout_worker.py`。
子进程只等待 0—10 秒，再输出固定 JSON，不读取任务文件。
父进程给等待设置上限，超时则得到 `tool_timeout`。

`subprocess.run(..., timeout=...)` 超时后会终止并等待直接子进程，然后抛出异常；
进程创建本身可能不能立即中断，所以总耗时不保证恰好等于 timeout。
依据：[Python subprocess 官方文档](https://docs.python.org/3.14/library/subprocess.html#subprocess.run)。

给线程的等待设置 timeout，通常只代表调用者停止等待，不能据此断言线程已经停止。
今天使用固定子进程来观察终止行为，不把“返回了超时错误”和“工作已经停止”混为一谈。
关于已运行任务的取消限制，见 [Python Future.cancel 文档](https://docs.python.org/3.14/library/concurrent.futures.html#concurrent.futures.Future.cancel)。

## 55 分钟：完成、超时、参数错误

```powershell
Set-Location -LiteralPath 'D:\python\File of python\Harness开发'
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson08 --scenario normal
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson08 --scenario timeout
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson08 --scenario invalid
```

| 场景 | 等待时间 / 上限 | 预期工具结果 |
| --- | --- | --- |
| normal | 0 秒 / 5 秒 | ok: true，completed: true |
| timeout | 3 秒 / 0.1 秒 | tool_timeout |
| invalid | -1 秒 / 5 秒 | invalid_arguments，不启动子进程 |

超时场景可能在子进程开始等待之前就结束；输出不足以证明 worker 已进入 `sleep()`。
`elapsed_ms` 是父进程测得的耗时，包含启动与清理开销，每次可以不同。
这些演示命令正常执行后退出 0，错误状态放在工具结果中。

打开 `mini_harness/lesson08.py`，这次只找四个位置：

1. `valid_seconds()`：先拒绝无效值，包括 bool、负数和无限值。
2. 参数列表中的 `sys.executable` 和固定 worker 路径：不能由模型换成任意命令。
3. `subprocess.run()`：`shell=False`，并设置 `timeout`。
4. `except subprocess.TimeoutExpired`：构造错误结果，而不是让程序只打印一长串异常。

父进程只传入少量系统环境变量，避免把宿主的 API 密钥传给这个实验进程。
这不等于容器隔离：子进程仍以当前用户身份运行。本实验只执行教材中的固定程序。
它也没有处理任意程序创建的后代进程、无限输出或强制 CPU/内存配额。

现在填写 `exercises/day08_starter.py` 的 `classify_process_result()`。
它不负责启动或终止进程，只根据已有观察分类：超时优先；没有超时且退出码为 0 才成功；
非零退出码或未得到退出码均不能记为成功。

## 20 分钟：检查结果与边界

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m pytest .\exercises\check_day08.py -q
& .\.venv\Scripts\python.exe -X utf8 -m pytest .\test_lessons07_09.py -k fixed_child_process -q
```

自己的函数完成后，第一条应为 **4 passed**；第二条应为 **2 passed**，分别启动正常和超时实验。
测试不比较精确毫秒数，因为系统负载可能改变实际耗时。

注意：没有抛 Python 异常不一定代表工具成功。子进程可能退出 1，或者退出 0 却输出无效 JSON。
参考实现分别返回 `tool_failed`、`invalid_tool_result`。
本课不会自动重试：对有副作用的工具，超时也可能发生在修改已经完成之后，重试需要额外设计。

## 20 分钟：基础与聊天复盘

画出父进程和子进程两个框：谁在等待，谁在做事，谁负责将异常转换为结果？
复习 `try/except` 和退出码。回答：

- 为什么限制 3 次调用，仍可能等待很久？
- 为什么 `tool_timeout` 不能直接推出“文件完全没改过”？
- 为什么只把等待放进线程，还不能证明工具被终止？

完成标准：

- [ ] 留下正常、超时两次工具输出，解释 elapsed_ms 的含义。
- [ ] 自己的分类函数通过 4 项检查。
- [ ] 能区分参数错误、超时、非零退出和返回格式错误。
- [ ] 能说出这个实验与 Docker 隔离之间还差什么。

聊天入口：“我在第 8 天。超时输出是……我觉得父进程此时做了……请检查。”
