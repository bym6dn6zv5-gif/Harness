# 第 2 天：工具注册与参数模型

目标：知道工具名字怎样找到函数，理解“函数本身”和“执行函数”的区别，用 Pydantic 校验参数。
前置：第 1 天；字典的 `.get()`、函数与 `try/except` 可以边读边补。

## 25 分钟：三个部分分开看

第一课只支持一个工具，用 `if name != "read_file"` 就能检查名字。
今天用一张表保存两个工具：`read_file` 读取内容，`count_lines` 统计行数。
注册表保存的内容是“名字 → 参数模型和执行函数”。

```python
registry.register("read_file", PathArgs, read_file)
registry.register("count_lines", PathArgs, count_lines)
```

这里的 `read_file` 表示函数本身；写成 `read_file(...)` 才会执行。
程序先从表中查找，再校验参数，最后调用找到的函数。

`PathArgs` 是 Pydantic 参数模型，要求：恰好有 `path`，值是非空白字符串，不能出现额外参数。
`strict=True` 启用严格类型检查，`extra="forbid"` 禁止额外参数；`field_validator` 补充纯空白检查。
文件名里的有效空格会被保留，不会为了校验而擅自改写路径。

参数结构描述与执行函数分别有用途：描述说明怎样调用；函数负责实际工作。
在真实工程中，工具是否向模型公开、是否获准执行，还可能有独立的控制层。

## 55 分钟：运行两个工具

```powershell
Set-Location -LiteralPath 'D:\python\File of python\Harness开发'
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson02 --tool read_file
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson02 --tool count_lines
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson02 --bad-args
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson02 --tool delete_file
```

预期依次为：读取成功；`line_count: 3`；`invalid_arguments`；`unknown_tool`。
行数使用 `splitlines()`：空文件为 0 行，只有 `one` 的文件为 1 行，末尾换行不额外算一行。

可选观察参数描述：

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson02 --show-schema
```

先找名字、`path`、`type: string`、`additionalProperties: false`，暂时不用读懂整个输出。
这是教学用结构描述，不是某家厂商完整 API 的请求格式。

打开 `mini_harness/lesson02.py`，依次读 `build_registry()`、`dispatch()`、`count_lines()`。
`count_lines()` 复用原来的只读文件逻辑，文件不存在、越界或过大时保留其错误结果。

打开 `exercises/day02_starter.py`，补两个函数：

1. `choose_handler(registry, name)`：找到就返回函数本身，找不到返回 `None`，不要执行函数。
2. `validate_arguments(arguments)`：调用 `PathArgs.model_validate()`；校验成功返回 `True`，捕获 `ValidationError` 后返回 `False`。

这里第二个函数只回答参数是否合法，还没有读取文件。

## 20 分钟：验证和源码对照

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m pytest .\exercises\check_day02.py -q
```

完成后应有 **4 passed**。测试把一个“执行就报错”的函数放进表里，检查查找时没有误执行它。

剩余时间可看 [源码阅读入口](source-reading.md#第-2-天codex-工具路由)。
在已记录版本的 Codex 中，先认识 `ToolCall`、`build_tool_call` 与交给注册表分发的调用。
只比较“请求带什么信息”和“谁负责分发”，不用安装或编译 Rust。

## 20 分钟：基础与复盘

用自己的话解释：`registry.get(name)` 找不到时会怎样？`handler` 与 `handler()` 差在哪里？
`try/except ValidationError` 捕获的是哪一种问题？为什么路径合法还可能读不到文件？

完成标准：

- [ ] 两个工具都能运行，错误参数被拒绝。
- [ ] 自己的两个函数通过检查。
- [ ] 能说明注册表、参数模型和执行函数各自的工作。

聊天模板：

```text
我在第 2 天。两个工具的输出是……
练习检查是……
我认为“返回函数”和“执行函数”的区别是……
请带我读 dispatch()，每次只解释一小段。
```
