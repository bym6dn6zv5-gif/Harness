# Harness Engineering 学习资料库

从零实现、排错、评测一个小型编程 Agent，目标是具备实习项目所需的实现与讲解能力。
学习顺序按 **12 周、每天约 2 小时** 编排；claw-code 与开源 Codex 为主教材，Hermes 记忆机制另设五课专题。

**找当天课程 → [完整学习时间表](docs/study-calendar.md)**
· **找某个知识点 → [资料速查表](docs/reference-index.md)**
· **找最近新增 → [按日期查看更新](docs/updates.md)**

## 第一次来，从这里开始

| 你要做什么 | 直接打开 |
| --- | --- |
| 继续已经运行过的第一课 | [P00：一次工具调用](lessons/01_tool_call/README.md) |
| 按顺序开始 12 周主线 | [W01-D01：目录和解释器](lessons/12_week_course/week01.md#w01-d01) |
| 查第几周、第几天学什么 | [72 次动手课 + 12 次复盘逐日表](docs/study-calendar.md#daily) |
| 先用小实验理解概念 | [E01—E09 入门实验](docs/study-calendar.md#experiments) |
| 学 Hermes 的记忆机制 | [H01—H05 专题安排](docs/study-calendar.md#hermes) |
| 看 Codex 和 claw-code 对照源码 | [S01—S03 阅读入口](docs/study-calendar.md#sources) |
| 找安装、解释器和 PowerShell 命令 | [本机环境说明](docs/environment.md) |

**编号约定：** W03-D04 表示主线第 3 周第 4 天；E04 表示入门小实验第 4 次；H04 表示 Hermes 第 4 课。
入门实验与主线有内容重叠，按需预习和复习。聊天时用完整编号，便于准确接着学。

## 12 周学习顺序

每周前 6 天动手，第 7 天复盘。点击周次可查看当周逐日安排；完成验收后再进入下一周。

| 时间 | 本周内容 | 验收成果 | 讲义 |
| --- | --- | --- | --- |
| [W01 · 第 1 周](docs/study-calendar.md#w01) | 环境、Git、JSON、参数校验、工具回传 | 跑通离线工具调用并解释测试 | [进入第 1 周](lessons/12_week_course/week01.md) |
| [W02 · 第 2 周](docs/study-calendar.md#w02) | 消息协议、参数模型、工作区、代码搜索、客户端 | 实现受限 read_file 与 search_code | [进入第 2 周](lessons/12_week_course/week02.md) |
| [W03 · 第 3 周](docs/study-calendar.md#w03) | 状态机、有界循环、预算、错误回传、去重 | 能定位问题并明确停止原因 | [进入第 3 周](lessons/12_week_course/week03.md) |
| [W04 · 第 4 周](docs/study-calendar.md#w04) | 补丁、测试进程、超时、Docker、修改闭环 | 在隔离工作区完成一次修复 | [进入第 4 周](lessons/12_week_course/week04.md) |
| [W05 · 第 5 周](docs/study-calendar.md#w05) | SQLite、检查点、恢复、冲突、中断 | 中断后继续并报告工作区冲突 | [进入第 5 周](lessons/12_week_course/week05.md) |
| [W06 · 第 6 周](docs/study-calendar.md#w06) | 上下文计量、长输出、检索、摘要、对照 | 比较上下文策略及信息遗漏 | [进入第 6 周](lessons/12_week_course/week06.md) |
| [W07 · 第 7 周](docs/study-calendar.md#w07) | 事件、耗时、token、费用、重试、排错 | 从轨迹定位失败并控制调用预算 | [进入第 7 周](lessons/12_week_course/week07.md) |
| [W08 · 第 8 周](docs/study-calendar.md#w08) | 30 个任务、20/10 划分、外部评分、基线 | 建立固定任务与独立评分流程 | [进入第 8 周](lessons/12_week_course/week08.md) |
| [W09 · 第 9 周](docs/study-calendar.md#w09) | 失败分析、两项改进、对照、消融 | 用开发集实验解释改进效果 | [进入第 9 周](lessons/12_week_course/week09.md) |
| [W10 · 第 10 周](docs/study-calendar.md#w10) | Codex、claw-code、MCP、provider | 讲清源码数据流并接入只读工具 | [进入第 10 周](lessons/12_week_course/week10.md) |
| [W11 · 第 11 周](docs/study-calendar.md#w11) | 冻结版本、重复评测、统计、复现 | 形成可复现结果表和限制说明 | [进入第 11 周](lessons/12_week_course/week11.md) |
| [W12 · 第 12 周](docs/study-calendar.md#w12) | 架构讲解、现场修改、简历、模拟面试 | 交付项目并完成独立讲解 | [进入第 12 周](lessons/12_week_course/week12.md) |

完整说明：[12 周课程总入口](lessons/12_week_course/README.md)；
记录进度：[学习进度表](lessons/12_week_course/progress.md)。

## 已可运行的入门实验

下面按原学习包的顺序排列。每一行的练习文件与检查器可在 [详细时间表](docs/study-calendar.md#experiments) 一起打开。

| 顺序 | 主题与讲义 | Python 参考实现 |
| --- | --- | --- |
| E01 | [工具成功与失败](lessons/six_day_pack/day01.md) | [lesson01_cases.py](mini_harness/lesson01_cases.py) |
| E02 | [工具注册与参数模型](lessons/six_day_pack/day02.md) | [lesson02.py](mini_harness/lesson02.py) |
| E03 | [有上限的 Agent 循环](lessons/six_day_pack/day03.md) | [lesson03.py](mini_harness/lesson03.py) |
| E04 | [消息轨迹与 JSONL](lessons/six_day_pack/day04.md) | [lesson04.py](mini_harness/lesson04.py) |
| E05 | [上下文副本与裁剪](lessons/six_day_pack/day05.md) | [lesson05.py](mini_harness/lesson05.py) |
| E06 | [固定案例与回归报告](lessons/six_day_pack/day06.md) | [lesson06.py](mini_harness/lesson06.py) |
| E07 | [工具权限](lessons/days07_09/day07.md) | [lesson07.py](mini_harness/lesson07.py) |
| E08 | [工具进程超时](lessons/days07_09/day08.md) | [lesson08.py](mini_harness/lesson08.py) |
| E09 | [SQLite 检查点与恢复](lessons/days07_09/day09.md) | [lesson09.py](mini_harness/lesson09.py) |

每次先预测输出、运行实验，再填写自己的 starter。提示与答案留在课程提示页，
练习需显式运行对应 check；默认测试通过不能替代练习验收。

## 源码与记忆专题

| 顺序 | 内容 | 入口 |
| --- | --- | --- |
| S01 | 模型请求 → 工具分发 → 执行 → 回传 | [Codex / claw-code 工具路径](lessons/source_mastery/tool-call.md) |
| S02 | 停止、持久化、恢复、上下文 | [状态与上下文](lessons/source_mastery/state-and-context.md) |
| S03 | 每周读哪些源码、怎样验收 | [贯穿 12 周的源码任务](lessons/source_mastery/curriculum-map.md) |
| H01 | 长期记忆、历史、摘要、技能、检查点 | [保存与读取](lessons/hermes_memory/01-storage-and-read.md) |
| H02 | add、patch、remove、容量、批次与审批 | [写入与一致性](lessons/hermes_memory/02-write-and-consistency.md) |
| H03 | session_search、文本检索、provider | [检索与扩展](lessons/hermes_memory/03-recall-and-providers.md) |
| H04 | 后台复盘、提示刷新、压缩、成本 | [复盘与压缩](lessons/hermes_memory/04-review-and-compression.md) |
| H05 | 离线实验、对照评测与独立修改 | [实验与验收](lessons/hermes_memory/05-labs-and-assessment.md) |

固定提交及已读范围：[源码版本索引](lessons/source_mastery/source-index.json)。
claw-code 教材原仓库在本机 D:\GitHub\claw-code，本学习仓库保存讲义、实验与版本链接。
教材代码、教学简化和实际学习者掌握情况分别记录。

## 经常查的资料

| 用途 | 入口 |
| --- | --- |
| 工具接口、错误、状态、预算约束 | [工程契约](lessons/12_week_course/engineering-contracts.md) |
| 工作目录、命令和每课提交物 | [实验操作约定](lessons/12_week_course/lab-guide.md) |
| 30 个任务、20/10 划分、外部评分 | [任务目录](lessons/12_week_course/task-catalog.md) |
| 基线、改进、成本和失败案例 | [实验报告模板](lessons/12_week_course/experiment-template.md) |
| 解释模块、数据流和取舍 | [架构说明模板](lessons/12_week_course/architecture-template.md) |
| 10 分钟讲解、现场改动与简历 | [面试练习](lessons/12_week_course/interview-kit.md) |
| 模型循环、恢复、记忆等关键词 | [按主题速查](docs/reference-index.md) |

## 当前学习与程序状态

| 项目 | 已有记录 |
| --- | --- |
| 学习者进度 | 已亲自运行第一课五步演示和原始 13 项测试；后续待学习 |
| 教材准备 | 12 周讲义、入门实验、源码对照、Hermes 五课、30 个微型任务及模板 |
| 最近程序核验 | 2026-10-24：119 项单元测试通过；30 任务材料校准与 60 次生成评分检查，详见报告 |
| 真实模型评测 | 尚未运行；材料校准不等于模型修复成绩 |
| 完整 Agent 目标 | 统一 run / resume / eval、Docker 执行器、真实模型接入等按课程逐步实现 |

查看 [教材核验报告](course-verification.md) 和 [机器可读校准记录](verification/course-calibration.json)。
本次导航整理只修改文档，没有重新运行上述程序测试；保留其原核验日期。

## 本地运行第一课

所有 Python 教学文件位于 D:\python\File of python\Harness开发。
已有环境记录为 Python 3.14.6；Git 和 Node.js 使用电脑原有安装。
在 PowerShell 中执行：

~~~powershell
Set-Location -LiteralPath 'D:\python\File of python\Harness开发'
& .\.venv\Scripts\python.exe -X utf8 -m mini_harness.lesson01 --workspace .\lessons\01_tool_call\workspace
& .\.venv\Scripts\python.exe -X utf8 -m pytest -q
~~~

解释器、依赖版本、检查和恢复命令见 [环境说明](docs/environment.md)。
第一课和已准备入门实验使用离线教学数据；模型 API、Docker 等按对应课程配置。
学习仓库保留讲义、代码、测试和学习记录，虚拟环境与临时运行数据按忽略规则留在本机。

## 按日期看资料更新

| 日期（北京时间） | 新增内容 | 直接查阅 |
| --- | --- | --- |
| 2026-10-23 | 第一课、学习路线、六次入门实验 | [P00](lessons/01_tool_call/README.md)、[E01—E06](lessons/six_day_pack/README.md) |
| 2026-10-24 | E07—E09、12 周课程、源码主教材、Hermes 五课、任务与报告 | [12 周课程](lessons/12_week_course/README.md)、[Hermes](lessons/hermes_memory/README.md) |
| 2026-10-24 | 首页排课表、逐日直达链接、资料速查与提交时间线 | [学习时间表](docs/study-calendar.md)、[完整更新记录](docs/updates.md) |

更新日期来自 Git 提交；表示材料何时加入仓库，不是你何时学完。
以后回来可以直接说“继续 W03-D04”或“讲 H01”，带上命令输出和自己的理解即可。
