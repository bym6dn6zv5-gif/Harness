# 按学习时间查课

[回仓库首页](../README.md) · [按主题查资料](reference-index.md) · [按更新日期查新增](updates.md)

每天约 2 小时，每周 6 天动手、第 7 天复盘。这里的时间是相对学习顺序，
没有把备课日期当成你已经上课的日期。验收未通过就留在当前课。

## 编号怎样读

| 编号 | 表示什么 | 怎样使用 |
| --- | --- | --- |
| P00 | 你已经运行过的第一课 | 从这里复盘一次工具调用 |
| W01-D01 | 12 周主线的第 1 周第 1 天 | 正式进度统一用 W周-D天 |
| E01—E09 | 原入门包的第 1—9 天小实验 | 配合主线预习或复习，不是主线的连续第 1—9 天 |
| H01—H05 | Hermes 记忆专题的五课 | 在主线第 5—10 周分次穿插 |
| S01—S03 | Codex / claw-code 源码讲义与阅读表 | 从第 1 周起随主线对照 |

推荐先打开 P00，再从 W01 开始；遇到抽象概念时，用对应 E 实验观察一次。
E、H、S 是配套材料，与主线有重叠，不额外虚构一套日历进度。
当前只有第一课演示与原始 13 项测试有学习者本人运行证据，后续均待学习。

<a id="p00"></a>

## 第一课

| 顺序 | 讲义 | 演示源码 | 测试 | 学习记录 |
| --- | --- | --- | --- | --- |
| P00 | [一次工具调用](../lessons/01_tool_call/README.md) | [lesson01.py](../mini_harness/lesson01.py) | [test_lesson01.py](../test_lesson01.py) | [第一课记录](../lessons/01_tool_call/learning-log.md) |

<a id="experiments"></a>

## 入门实验 E01—E09

每行按“读讲义 → 跑参考实现 → 自己填练习 → 运行检查 → 留下解释”使用。
默认测试通过不等于你已完成 starter；练习需显式运行相应检查器。

| 顺序 | 讲义 | 参考实现 | 你的练习 | 练习检查 | 本次验收 |
| --- | --- | --- | --- | --- | --- |
| E01 | [工具成功与失败](../lessons/six_day_pack/day01.md) | [源码](../mini_harness/lesson01_cases.py) | [starter](../exercises/day01_starter.py) | [check](../exercises/check_day01.py) | 区分成功、参数错误和未知工具 |
| E02 | [工具注册与参数模型](../lessons/six_day_pack/day02.md) | [源码](../mini_harness/lesson02.py) | [starter](../exercises/day02_starter.py) | [check](../exercises/check_day02.py) | 理解名称分发与参数校验 |
| E03 | [有上限的 Agent 循环](../lessons/six_day_pack/day03.md) | [源码](../mini_harness/lesson03.py) | [starter](../exercises/day03_starter.py) | [check](../exercises/check_day03.py) | 解释继续、停止与调用标识 |
| E04 | [消息轨迹与 JSONL](../lessons/six_day_pack/day04.md) | [源码](../mini_harness/lesson04.py) | [starter](../exercises/day04_starter.py) | [check](../exercises/check_day04.py) | 用记录还原一次运行 |
| E05 | [上下文副本与裁剪](../lessons/six_day_pack/day05.md) | [源码](../mini_harness/lesson05.py) | [starter](../exercises/day05_starter.py) | [check](../exercises/check_day05.py) | 区分完整历史和模型输入视图 |
| E06 | [固定案例与回归报告](../lessons/six_day_pack/day06.md) | [源码](../mini_harness/lesson06.py) | [starter](../exercises/day06_starter.py) | [check](../exercises/check_day06.py) | 分清期望、观测和评分 |
| E07 | [工具权限](../lessons/days07_09/day07.md) | [源码](../mini_harness/lesson07.py) | [starter](../exercises/day07_starter.py) | [check](../exercises/check_day07.py) | 证明拒绝后没有执行工具 |
| E08 | [工具进程超时](../lessons/days07_09/day08.md) | [源码](../mini_harness/lesson08.py) | [starter](../exercises/day08_starter.py) | [check](../exercises/check_day08.py) | 观察正常、超时和无效参数 |
| E09 | [SQLite 检查点与恢复](../lessons/days07_09/day09.md) | [源码](../mini_harness/lesson09.py) | [starter](../exercises/day09_starter.py) | [check](../exercises/check_day09.py) | 保留预算并处理恢复冲突 |

前六次的 [分级提示](../lessons/six_day_pack/hints-and-answers.md) 与 [学习日志](../lessons/six_day_pack/study-log.md)；
后三次的 [分级提示](../lessons/days07_09/hints-and-answers.md) 与 [学习日志](../lessons/days07_09/study-log.md)。
答案链接留在提示页，先完成自己的尝试。

## 12 周主线总表

先用总表选周，再用下方逐日表直接跳到当天段落。

| 时间 | 内容 | 周成果 | 进入逐日表 |
| --- | --- | --- | --- |
| W01 · 第 1 周 | 环境、Git、JSON、参数校验、工具回传 | 跑通离线工具调用并解释测试 | [第 1 周](#w01) |
| W02 · 第 2 周 | 消息协议、参数模型、工作区、代码搜索、客户端 | 实现受限 read_file 与 search_code | [第 2 周](#w02) |
| W03 · 第 3 周 | 状态机、有界循环、预算、错误回传、去重 | 能定位问题并明确停止原因 | [第 3 周](#w03) |
| W04 · 第 4 周 | 补丁、测试进程、超时、Docker、修改闭环 | 在隔离工作区完成一次修复 | [第 4 周](#w04) |
| W05 · 第 5 周 | SQLite、检查点、恢复、冲突、中断 | 中断后继续并报告工作区冲突 | [第 5 周](#w05) |
| W06 · 第 6 周 | 上下文计量、长输出、检索、摘要、对照 | 比较上下文策略及信息遗漏 | [第 6 周](#w06) |
| W07 · 第 7 周 | 事件、耗时、token、费用、重试、排错 | 从轨迹定位失败并控制调用预算 | [第 7 周](#w07) |
| W08 · 第 8 周 | 30 个任务、20/10 划分、外部评分、基线 | 建立固定任务与独立评分流程 | [第 8 周](#w08) |
| W09 · 第 9 周 | 失败分析、两项改进、对照、消融 | 用开发集实验解释改进效果 | [第 9 周](#w09) |
| W10 · 第 10 周 | Codex、claw-code、MCP、provider | 讲清源码数据流并接入只读工具 | [第 10 周](#w10) |
| W11 · 第 11 周 | 冻结版本、重复评测、统计、复现 | 形成可复现结果表和限制说明 | [第 11 周](#w11) |
| W12 · 第 12 周 | 架构讲解、现场修改、简历、模拟面试 | 交付项目并完成独立讲解 | [第 12 周](#w12) |

<a id="daily"></a>

## 逐日安排：72 次动手课与 12 次复盘

按周验收后再推进。表中列出的功能为课程实现任务，不代表完整项目已经实现。

<a id="w01"></a>

### W01 · 第 1 周

配套：[P00](#p00)、[E01](../lessons/six_day_pack/day01.md)、[数据流](../lessons/source_mastery/tool-call.md)。

| 时间 | 当天主题 | 进入讲义 |
| --- | --- | --- |
| W01-D01 | 认清目录和解释器 | [打开当天](../lessons/12_week_course/week01.md#w01-d01) |
| W01-D02 | Git 记录一次变化 | [打开当天](../lessons/12_week_course/week01.md#w01-d02) |
| W01-D03 | JSON 是传输格式，字典是运行时对象 | [打开当天](../lessons/12_week_course/week01.md#w01-d03) |
| W01-D04 | 类型提示与运行时检查 | [打开当天](../lessons/12_week_course/week01.md#w01-d04) |
| W01-D05 | 理解测试观察什么 | [打开当天](../lessons/12_week_course/week01.md#w01-d05) |
| W01-D06 | 完整的数据流 | [打开当天](../lessons/12_week_course/week01.md#w01-d06) |
| W01-D07 · 复盘 | 复盘与周验收 | [打开当天](../lessons/12_week_course/week01.md#w01-d07) |

<a id="w02"></a>

### W02 · 第 2 周

配套：[E02](../lessons/six_day_pack/day02.md)、[源码路由](../lessons/source_mastery/tool-call.md)。

| 时间 | 当天主题 | 进入讲义 |
| --- | --- | --- |
| W02-D01 | 消息不是任意拼接的字符串 | [打开当天](../lessons/12_week_course/week02.md#w02-d01) |
| W02-D02 | 参数模型与工具描述 | [打开当天](../lessons/12_week_course/week02.md#w02-d02) |
| W02-D03 | 工作区边界 | [打开当天](../lessons/12_week_course/week02.md#w02-d03) |
| W02-D04 | 实现 search_code | [打开当天](../lessons/12_week_course/week02.md#w02-d04) |
| W02-D05 | 模型客户端适配层 | [打开当天](../lessons/12_week_course/week02.md#w02-d05) |
| W02-D06 | 契约检查 | [打开当天](../lessons/12_week_course/week02.md#w02-d06) |
| W02-D07 · 复盘 | 周验收 | [打开当天](../lessons/12_week_course/week02.md#w02-d07) |

<a id="w03"></a>

### W03 · 第 3 周

配套：[E03](../lessons/six_day_pack/day03.md)、[停止与状态](../lessons/source_mastery/state-and-context.md)。

| 时间 | 当天主题 | 进入讲义 |
| --- | --- | --- |
| W03-D01 | 先画状态机 | [打开当天](../lessons/12_week_course/week03.md#w03-d01) |
| W03-D02 | 独立重写循环 | [打开当天](../lessons/12_week_course/week03.md#w03-d02) |
| W03-D03 | 工具失败也要回传 | [打开当天](../lessons/12_week_course/week03.md#w03-d03) |
| W03-D04 | 步数和调用预算 | [打开当天](../lessons/12_week_course/week03.md#w03-d04) |
| W03-D05 | 重复与协议错误 | [打开当天](../lessons/12_week_course/week03.md#w03-d05) |
| W03-D06 | 命令入口与问题定位 | [打开当天](../lessons/12_week_course/week03.md#w03-d06) |
| W03-D07 · 复盘 | 周验收 | [打开当天](../lessons/12_week_course/week03.md#w03-d07) |

<a id="w04"></a>

### W04 · 第 4 周

配套：[E07 权限](../lessons/days07_09/day07.md)、[E08 超时](../lessons/days07_09/day08.md)。

| 时间 | 当天主题 | 进入讲义 |
| --- | --- | --- |
| W04-D01 | 创建一次性任务工作区 | [打开当天](../lessons/12_week_course/week04.md#w04-d01) |
| W04-D02 | 先做受限补丁工具 | [打开当天](../lessons/12_week_course/week04.md#w04-d02) |
| W04-D03 | 测试工具的输入不是任意命令 | [打开当天](../lessons/12_week_course/week04.md#w04-d03) |
| W04-D04 | 超时与清理 | [打开当天](../lessons/12_week_course/week04.md#w04-d04) |
| W04-D05 | Docker 执行环境 | [打开当天](../lessons/12_week_course/week04.md#w04-d05) |
| W04-D06 | 串起一次闭环 | [打开当天](../lessons/12_week_course/week04.md#w04-d06) |
| W04-D07 · 复盘 | 周验收 | [打开当天](../lessons/12_week_course/week04.md#w04-d07) |

<a id="w05"></a>

### W05 · 第 5 周

配套：[E09 恢复](../lessons/days07_09/day09.md)、[H01 状态分类](../lessons/hermes_memory/01-storage-and-read.md)。

| 时间 | 当天主题 | 进入讲义 |
| --- | --- | --- |
| W05-D01 | 定义恢复需要的状态 | [打开当天](../lessons/12_week_course/week05.md#w05-d01) |
| W05-D02 | SQLite 保存与读取 | [打开当天](../lessons/12_week_course/week05.md#w05-d02) |
| W05-D03 | 选择保存边界 | [打开当天](../lessons/12_week_course/week05.md#w05-d03) |
| W05-D04 | 实现 resume | [打开当天](../lessons/12_week_course/week05.md#w05-d04) |
| W05-D05 | 工作区冲突 | [打开当天](../lessons/12_week_course/week05.md#w05-d05) |
| W05-D06 | 注入中断，整理恢复矩阵 | [打开当天](../lessons/12_week_course/week05.md#w05-d06) |
| W05-D07 · 复盘 | 周验收 | [打开当天](../lessons/12_week_course/week05.md#w05-d07) |

<a id="w06"></a>

### W06 · 第 6 周

配套：[E05](../lessons/six_day_pack/day05.md)、[H03 检索](../lessons/hermes_memory/03-recall-and-providers.md)、[H04 压缩](../lessons/hermes_memory/04-review-and-compression.md)。

| 时间 | 当天主题 | 进入讲义 |
| --- | --- | --- |
| W06-D01 | 分清完整历史与发送视图 | [打开当天](../lessons/12_week_course/week06.md#w06-d01) |
| W06-D02 | 测量与预算 | [打开当天](../lessons/12_week_course/week06.md#w06-d02) |
| W06-D03 | 工具长输出 | [打开当天](../lessons/12_week_course/week06.md#w06-d03) |
| W06-D04 | 按需检索 | [打开当天](../lessons/12_week_course/week06.md#w06-d04) |
| W06-D05 | 进度摘要 | [打开当天](../lessons/12_week_course/week06.md#w06-d05) |
| W06-D06 | 配对实验 | [打开当天](../lessons/12_week_course/week06.md#w06-d06) |
| W06-D07 · 复盘 | 周验收 | [打开当天](../lessons/12_week_course/week06.md#w06-d07) |

<a id="w07"></a>

### W07 · 第 7 周

配套：[E04 轨迹](../lessons/six_day_pack/day04.md)、[H04 后台复盘](../lessons/hermes_memory/04-review-and-compression.md)。

| 时间 | 当天主题 | 进入讲义 |
| --- | --- | --- |
| W07-D01 | 运行事件 | [打开当天](../lessons/12_week_course/week07.md#w07-d01) |
| W07-D02 | 耗时与错误归因 | [打开当天](../lessons/12_week_course/week07.md#w07-d02) |
| W07-D03 | 真实用量 | [打开当天](../lessons/12_week_course/week07.md#w07-d03) |
| W07-D04 | 人民币 100 元上限 | [打开当天](../lessons/12_week_course/week07.md#w07-d04) |
| W07-D05 | 有界重试 | [打开当天](../lessons/12_week_course/week07.md#w07-d05) |
| W07-D06 | 排错演练 | [打开当天](../lessons/12_week_course/week07.md#w07-d06) |
| W07-D07 · 复盘 | 周验收 | [打开当天](../lessons/12_week_course/week07.md#w07-d07) |

<a id="w08"></a>

### W08 · 第 8 周

配套：[E06 评分](../lessons/six_day_pack/day06.md)、[30 任务目录](../lessons/12_week_course/task-catalog.md)。

| 时间 | 当天主题 | 进入讲义 |
| --- | --- | --- |
| W08-D01 | 任务规格 | [打开当天](../lessons/12_week_course/week08.md#w08-d01) |
| W08-D02 | 冻结划分 | [打开当天](../lessons/12_week_course/week08.md#w08-d02) |
| W08-D03 | 外部评分 | [打开当天](../lessons/12_week_course/week08.md#w08-d03) |
| W08-D04 | 批量运行入口 | [打开当天](../lessons/12_week_course/week08.md#w08-d04) |
| W08-D05 | 失败分类 | [打开当天](../lessons/12_week_course/week08.md#w08-d05) |
| W08-D06 | 建立基线 | [打开当天](../lessons/12_week_course/week08.md#w08-d06) |
| W08-D07 · 复盘 | 周验收 | [打开当天](../lessons/12_week_course/week08.md#w08-d07) |

<a id="w09"></a>

### W09 · 第 9 周

配套：[实验模板](../lessons/12_week_course/experiment-template.md)、[H05 记忆评测](../lessons/hermes_memory/05-labs-and-assessment.md)。

| 时间 | 当天主题 | 进入讲义 |
| --- | --- | --- |
| W09-D01 | 从失败分布选问题 | [打开当天](../lessons/12_week_course/week09.md#w09-d01) |
| W09-D02 | 预先写实验卡 | [打开当天](../lessons/12_week_course/week09.md#w09-d02) |
| W09-D03 | 改进一——让模型拿到可用证据 | [打开当天](../lessons/12_week_course/week09.md#w09-d03) |
| W09-D04 | 改进二——让错误更可恢复 | [打开当天](../lessons/12_week_course/week09.md#w09-d04) |
| W09-D05 | 合并与消融 | [打开当天](../lessons/12_week_course/week09.md#w09-d05) |
| W09-D06 | 写 5 个失败案例 | [打开当天](../lessons/12_week_course/week09.md#w09-d06) |
| W09-D07 · 复盘 | 周验收 | [打开当天](../lessons/12_week_course/week09.md#w09-d07) |

<a id="w10"></a>

### W10 · 第 10 周

配套：[源码总入口](../lessons/source_mastery/README.md)、[H02 写入](../lessons/hermes_memory/02-write-and-consistency.md)、[H03 provider](../lessons/hermes_memory/03-recall-and-providers.md)。

| 时间 | 当天主题 | 进入讲义 |
| --- | --- | --- |
| W10-D01 | 建立源码阅读方法 | [打开当天](../lessons/12_week_course/week10.md#w10-d01) |
| W10-D02 | Codex 工具路由 | [打开当天](../lessons/12_week_course/week10.md#w10-d02) |
| W10-D03 | claw-code 循环与权限 | [打开当天](../lessons/12_week_course/week10.md#w10-d03) |
| W10-D04 | mini-swe-agent 的模型与环境边界 | [打开当天](../lessons/12_week_course/week10.md#w10-d04) |
| W10-D05 | MCP 最小实验 | [打开当天](../lessons/12_week_course/week10.md#w10-d05) |
| W10-D06 | 接回自己的 Harness | [打开当天](../lessons/12_week_course/week10.md#w10-d06) |
| W10-D07 · 复盘 | 周验收 | [打开当天](../lessons/12_week_course/week10.md#w10-d07) |

<a id="w11"></a>

### W11 · 第 11 周

配套：[实验模板](../lessons/12_week_course/experiment-template.md)、[工程契约](../lessons/12_week_course/engineering-contracts.md)。

| 时间 | 当天主题 | 进入讲义 |
| --- | --- | --- |
| W11-D01 | 冻结实验方案 | [打开当天](../lessons/12_week_course/week11.md#w11-d01) |
| W11-D02 | 离线演练 | [打开当天](../lessons/12_week_course/week11.md#w11-d02) |
| W11-D03 | 运行基线 | [打开当天](../lessons/12_week_course/week11.md#w11-d03) |
| W11-D04 | 运行改进版 | [打开当天](../lessons/12_week_course/week11.md#w11-d04) |
| W11-D05 | 统计和限制 | [打开当天](../lessons/12_week_course/week11.md#w11-d05) |
| W11-D06 | 复现文档 | [打开当天](../lessons/12_week_course/week11.md#w11-d06) |
| W11-D07 · 复盘 | 周验收 | [打开当天](../lessons/12_week_course/week11.md#w11-d07) |

<a id="w12"></a>

### W12 · 第 12 周

配套：[架构模板](../lessons/12_week_course/architecture-template.md)、[面试练习](../lessons/12_week_course/interview-kit.md)。

| 时间 | 当天主题 | 进入讲义 |
| --- | --- | --- |
| W12-D01 | 整理架构和证据 | [打开当天](../lessons/12_week_course/week12.md#w12-d01) |
| W12-D02 | 10 分钟项目讲解 | [打开当天](../lessons/12_week_course/week12.md#w12-d02) |
| W12-D03 | 代码追问 | [打开当天](../lessons/12_week_course/week12.md#w12-d03) |
| W12-D04 | 现场修改 | [打开当天](../lessons/12_week_course/week12.md#w12-d04) |
| W12-D05 | 写简历 | [打开当天](../lessons/12_week_course/week12.md#w12-d05) |
| W12-D06 | 模拟面试与交付 | [打开当天](../lessons/12_week_course/week12.md#w12-d06) |
| W12-D07 · 复盘 | 结课验收 | [打开当天](../lessons/12_week_course/week12.md#w12-d07) |

<a id="hermes"></a>

## Hermes 专题 H01—H05

| 顺序 | 建议穿插时间 | 讲义 | 必须留下的理解证据 |
| --- | --- | --- | --- |
| H01 | 第 5 周状态与恢复后 | [保存与读取](../lessons/hermes_memory/01-storage-and-read.md) | 画出六类状态和提示快照 |
| H02 | 第 5—6 周 | [写入与一致性](../lessons/hermes_memory/02-write-and-consistency.md) | 解释 patch、歧义、容量与回滚 |
| H03 | 第 6 周；第 10 周再看 provider | [检索与扩展](../lessons/hermes_memory/03-recall-and-providers.md) | 从搜索结果找到原文证据 |
| H04 | 第 6—7 周 | [复盘与压缩](../lessons/hermes_memory/04-review-and-compression.md) | 说明刷新边界与后台调用成本 |
| H05 | 第 9 周实验设计 | [实验与验收](../lessons/hermes_memory/05-labs-and-assessment.md) | 运行机制缩影并独立修改 |

完整入口：[Hermes 五课](../lessons/hermes_memory/README.md)。
离线缩影：[memory_lab.py](../mini_harness/memory_lab.py)；
对应测试：[test_memory_lab.py](../test_memory_lab.py)。

<a id="sources"></a>

## 源码对照 S01—S03

| 顺序 | 时间 | 讲义 | 用途 |
| --- | --- | --- | --- |
| S01 | 第 1—3 周起持续复习 | [一次工具调用](../lessons/source_mastery/tool-call.md) | claw 与 Codex 的请求、分发与回传 |
| S02 | 第 3—6 周 | [状态与上下文](../lessons/source_mastery/state-and-context.md) | 停止、持久化、恢复与压缩 |
| S03 | 每周 | [12 周源码任务表](../lessons/source_mastery/curriculum-map.md) | 明确本周阅读和独立解释要求 |

固定提交与所读范围：[source-index.json](../lessons/source_mastery/source-index.json)。
源码阅读记录与 Python 小实验进度分别验收。

## 学完后更新哪里

统一记录在 [12 周进度表](../lessons/12_week_course/progress.md)，
入门实验的详细过程保留在各自 study-log。
告诉助手完整编号，例如“W03-D04”或“E08”，这样不会把两套“第 8 天”混在一起。

[回仓库首页](../README.md) · [按主题检索](reference-index.md) · [按日期查看更新](updates.md)
