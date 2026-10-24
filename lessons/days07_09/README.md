# 第 7—9 天：给 Harness 加上执行边界和恢复能力

[回仓库首页](../../README.md) · [按时间查课](../../docs/study-calendar.md) · [按主题查资料](../../docs/reference-index.md)

每天约 2 小时，不绑定日期。先完成 [前六天](../six_day_pack/README.md) 中对应的基础，
再进入这里。教材已准备并验证，学习者进度仍为 **待学习**。

| 学习日 | 主题 | 前置知识 | 本次留下的成果 |
| --- | --- | --- | --- |
| 7 | [工具权限](day07.md) | 注册表、参数校验、结构化错误 | 许可判断函数；证明拒绝请求没有执行工具 |
| 8 | [工具超时](day08.md) | 异常、函数返回值、进程的基本概念 | 结果分类函数；正常与超时两次运行记录 |
| 9 | [检查点与恢复](day09.md) | 消息历史、步数预算、JSON | 剩余预算和恢复判断函数；两次进程运行的恢复记录 |

第 9 天是后续状态持久化课程的入门实验，先处理固定模拟模型和只读工具。
这三天没有实现补丁执行、Docker、真实模型接入或完整的编程 Agent。

## 打开项目

```powershell
Set-Location -LiteralPath 'D:\python\File of python\Harness开发'
& .\.venv\Scripts\python.exe --version
```

全部 Python 文件保存在这个项目的 `mini_harness` 和 `exercises` 内。
不需要新增依赖，不调用付费模型 API。第 8 天会启动本教材的固定子进程；
第 9 天会在项目 `.harness/day09` 中创建新的演示输入和 SQLite 数据库，均被 Git 忽略。

## 每天怎样用

先预测输出，再运行参考实验，接着打开当天的 `exercises/dayXX_starter.py` 填写函数。
每次只替换自己的 `raise NotImplementedError(...)`，前六天的练习不需要修改。

```powershell
# 教材参考实现的检查；不会要求你先写完练习
& .\.venv\Scripts\python.exe -X utf8 -m pytest -q

# 自己填写第 7 天练习之后，显式运行对应检查
& .\.venv\Scripts\python.exe -X utf8 -m pytest .\exercises\check_day07.py -q
```

第 7、8、9 天独立检查分别为 **4、4、5 项**。starter 未填时会提示 `NotImplementedError`，
说明练习还没有实现。默认 `pytest` 通过只说明参考实现通过检查，不代表你完成了练习。
参考答案通过了同一批检查，代码另存于 `exercises/answers07_09.py`。

卡住时先看 [分级提示](hints-and-answers.md)，或直接与我聊天。
每天最后记录在 [学习日志](study-log.md)；备课检查见 [verification.md](verification.md)。

## 与我聊天时的用法

你可以只说“我开始第 7 天”，我会先问你一个预测问题，再带你运行一小步。
也可以这样发来：

```text
我在第 X 天，做到讲义的……部分。
运行的命令是：……
结果或错误的最后几行是：……
我认为它表示：……
请先检查我的理解，一次给一个提示。
```

遇到错误保留命令、错误码和你原来的判断，不需要为了通过检查而把代码换成参考答案。
一天没学完就停在原处，下次从那里继续。

## 源码教材的位置

这三天的 Python 实验是为本课程编写的教学代码。第 7 天增加了 claw-code 权限分支的
[固定版本阅读入口](source-reading.md)，继续与 [之前的 Codex 路由阅读](../six_day_pack/source-reading.md) 对照。
第 8、9 天先依据 Python 官方接口完成实验；没有把简化实现说成 Codex 的内部实现。
