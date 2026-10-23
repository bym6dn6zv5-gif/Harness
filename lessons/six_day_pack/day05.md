# 第 5 天：完整历史与上下文副本

目标：理解“保存下来的全部消息”和“为下一次请求整理的数据”可以分开，观察裁剪会丢失什么。
前置：JSON 文本、消息列表，以及函数返回两个值的基本用法。

## 25 分钟：先理解取舍

长文件可以产生很长的工具反馈。如果每次都完整携带，后续请求会更大。
今天在消息的副本里裁剪读取到的文本，原始历史保持完整，方便回看。

本课只处理工具结果里的 `data.content`，保留消息顺序、调用 id 和合法 JSON 结构。
它还没有删除整组消息、生成摘要，也没有实现整个请求的 token 预算。

```python
shortened = text[:max_chars]
was_truncated = len(text) > max_chars
```

第二行用 `>`：文字长度正好等于上限时，没有丢失内容，应返回 `False`。
本课统计的是 Python 字符数。字符数、UTF-8 字节数和模型 token 数不是同一个量，不能直接换算费用。

## 55 分钟：运行与比较

```powershell
Set-Location -LiteralPath 'D:\python\File of python\Harness开发'
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson05 --max-tool-chars 12
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson05 --max-tool-chars 2000
```

第一个命令会显示裁剪前后序列化消息的字符数。读取结果里应出现：

```json
{"content_truncated": true, "original_chars": 100}
```

上面只示意两个字段，100 是示例数字；实际 `content` 还会保留前 12 个字符，`original_chars` 是原始文字长度。
第二个命令的上限大于本课文件长度，应没有裁剪标志，前后字符数相同。

不要把工具结果的整段 JSON 文本直接切成前 12 个字符，那会切掉引号或括号，导致无法解析。
参考实现先 `json.loads()`，只修改内部文本，再 `json.dumps()`。

打开 `mini_harness/lesson05.py`：

1. `deepcopy(messages)` 建立嵌套数据副本。
2. 找到 `role="tool"` 的消息，解析里面的 JSON。
3. 只在存在长字符串 `data.content` 时裁剪，注明原始长度和裁剪标记。
4. 保留其他结果，如统计行数和错误反馈。

附加标记本身也占空间；对很短的文字，裁剪未必让最终 JSON 更短。先观察实测数字，再解释原因。
截断会丢失信息。这里没有再次调用真实模型，不能据此声称答案质量提升。

打开 `exercises/day05_starter.py`，补 `truncate_text(text, max_chars)`。
本小题已约定上限是正整数，返回 `(文字前缀, 是否截断)`，先把边界写对。

## 20 分钟：验证

```powershell
& .\.venv\Scripts\python.exe -X utf8 -m pytest .\exercises\check_day05.py -q
```

完成后应有 **3 passed**，覆盖短文字、正好等长、长文字、中文和空字符串。

主项目参考测试另行检查：裁剪后 JSON 仍能解析、调用标识未变、原始消息没被修改。
这是数据处理检查，还没有评测真实模型受裁剪后的表现。

## 20 分钟：基础与复盘

解释 `text[:3]` 的结果，写出 `("abc", True)` 中两项分别代表什么。
再看完整 `workspace/note.txt`，指出裁成 12 个字符后哪条信息消失了。

完成标准：

- [ ] 能解释两种上限的输出差异。
- [ ] 自己的裁剪函数通过边界检查。
- [ ] 能说明为什么保留完整记录，以及为什么字符数不能当作 token 费用。

聊天模板：

```text
我在第 5 天。上限 12 与 2000 的输出分别是……
我认为被丢掉的信息有……
我的练习检查是……
请先检查我是否理解副本和原数据，再讨论更复杂的压缩。
```
