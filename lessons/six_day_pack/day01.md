# 第 1 天：成功与失败都要回传

目标：能用自己的话描述一次调用，区分未知工具、错误参数和文件不存在，并写一个结果分类函数。
前置：已运行过第一课；知道字典、函数和 `if` 的基本含义。

## 25 分钟：建立四个概念

模型提出工具名和参数；执行程序检查请求并执行工具；结果通过消息交回模型。
本课用代码写死的请求代替真实模型输出，所以运行成功只说明教学程序按预期工作。

工具结果采用两种结构：

```python
{"ok": True, "data": {"content": "文件内容"}}
{"ok": False, "error": {"code": "file_not_found", "message": "未找到文件"}}
```

`ok` 表示这次工具调用是否成功；`code` 是便于程序处理的错误类别；`message` 是给人阅读的说明。
工具失败后仍应把错误反馈交回模型，让后续步骤有依据。

先预测下面四种输入。检查顺序是工具名、参数、路径与文件、读取：

| 场景 | 输入变化 | 预期 |
| --- | --- | --- |
| normal | `read_file`，`path="note.txt"` | 成功 |
| missing | `path="missing.txt"` | `file_not_found` |
| invalid | `path=123` | `invalid_arguments` |
| unknown | `name="delete_file"` | `unknown_tool` |

`missing.txt` 是合法字符串，通过类型检查，随后才发现文件不存在。这里没有注册删除工具。

## 55 分钟：观察和动手

先进入正确目录：

```powershell
Set-Location -LiteralPath 'D:\python\File of python\Harness开发'
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson01_cases --case normal
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson01_cases --case missing
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson01_cases --case invalid
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson01_cases --case unknown
```

这些命令只读取本学习包 `workspace/note.txt`，不用修改原来的 `lesson01.py`。
每次都会显示模拟请求、工具结果、回传消息和模拟回答。
三个错误场景应有 `ok: false`，最后的模拟回答说明工具调用失败。

在 `mini_harness/lesson01_cases.py` 中读 `run_case()`，只跟踪下面四项：

1. `call` 保存工具名、参数和调用标识。
2. `execute_tool(...)` 返回工具结果。
3. `role="tool"` 的消息把结果放进 `content`，用 `tool_call_id` 对应请求。
4. `MockModel().reply(messages)` 根据这条反馈给出预先规定的回答。

`json.dumps()` 把字典转为 JSON 文本，`json.loads()` 把文本还原成数据。
看到 `\n` 或 `\"` 是 JSON 的转义显示，不表示文件内容损坏。

现在打开 `exercises/day01_starter.py`，补上 `classify_result(result)`：

- 成功时返回字符串 `"success"`。
- 失败时返回实际错误码，不能所有错误都返回同一个常量。

先用 `if` 写出来即可；卡住时看 [第 1 天提示](hints-and-answers.md#第-1-天)。

## 20 分钟：验证

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m pytest .\exercises\check_day01.py -q
```

填写前会提示 `NotImplementedError`；完成后应有 **2 passed**，其中一个测试会循环检查多个错误码。

再看原测试文件 `test_lesson01.py` 的 `test_invalid_arguments_are_rejected_before_reading`：
它临时替换 `open()`，一被调用就抛出 `AssertionError`。两条 `assert` 检查错误返回值，
临时替换则检查当前实现有没有走到这条文件打开路径。

只有返回值检查时，“先读文件再报错”的实现仍可能通过；检查执行过程可以补上这个观察角度。
这项检查覆盖的是当前测试中的打开方式，不能自动证明所有读取方式都被禁止。

## 20 分钟：基础与复盘

在纸上写出消息角色顺序：`user → assistant → tool → assistant`。
解释字典中 `result["error"]["code"]` 的两次取值分别在取什么。

完成标准：

- [ ] 四种场景的错误类别与预测一致。
- [ ] 自己填写的分类函数通过当天检查。
- [ ] 能指出谁真正打开文件，说明为什么错误也要回传。

回来聊天可以说：

```text
我在第 1 天。四种场景的结果是……
我的 classify_result 检查结果是……
我理解“参数错误”和“文件不存在”的区别是……
请一次问我一个问题，确认我是否理解结果回传。
```
