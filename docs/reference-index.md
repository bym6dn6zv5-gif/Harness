# 按主题查资料

[回仓库首页](../README.md) · [按学习时间查课](study-calendar.md) · [按日期查更新](updates.md)

不知道文件放哪里时，先按关键词找一行。讲义解释概念，参考代码帮助观察，练习需要自己填写。
W 为 12 周主线，E 为入门实验，H 为 Hermes 专题，S 为源码对照。

## Harness 核心概念

| 想查的内容 | 主线位置 | 小实验或源码讲义 | 相关代码 / 记录 |
| --- | --- | --- | --- |
| 模型、工具、程序谁在执行 | [W01-D06](../lessons/12_week_course/week01.md#w01-d06) | [P00](../lessons/01_tool_call/README.md)、[S01](../lessons/source_mastery/tool-call.md) | [lesson01.py](../mini_harness/lesson01.py) |
| JSON、字典、序列化 | [W01-D03](../lessons/12_week_course/week01.md#w01-d03) | [E01](../lessons/six_day_pack/day01.md) | [第一课测试](../test_lesson01.py) |
| 参数校验、Pydantic、未知工具 | [W02-D02](../lessons/12_week_course/week02.md#w02-d02) | [E02](../lessons/six_day_pack/day02.md) | [lesson02.py](../mini_harness/lesson02.py) |
| call_id、工具结果和消息协议 | [W02-D01](../lessons/12_week_course/week02.md#w02-d01) | [S01](../lessons/source_mastery/tool-call.md) | [lesson03.py](../mini_harness/lesson03.py) |
| 路径越界、工作区 | [W02-D03](../lessons/12_week_course/week02.md#w02-d03) | [第一课测试](../test_lesson01.py) | [工程契约](../lessons/12_week_course/engineering-contracts.md) |
| 工具注册与运行许可 | [W04](../lessons/12_week_course/week04.md) | [E07](../lessons/days07_09/day07.md) | [lesson07.py](../mini_harness/lesson07.py) |
| 循环、状态机、停止 | [W03-D01](../lessons/12_week_course/week03.md#w03-d01) | [E03](../lessons/six_day_pack/day03.md)、[S02](../lessons/source_mastery/state-and-context.md) | [lesson03.py](../mini_harness/lesson03.py) |
| 步数、调用预算、重复动作 | [W03-D04](../lessons/12_week_course/week03.md#w03-d04)、[W03-D05](../lessons/12_week_course/week03.md#w03-d05) | [E03](../lessons/six_day_pack/day03.md) | [工程契约](../lessons/12_week_course/engineering-contracts.md) |
| 文件补丁、测试执行、Docker | [W04-D02](../lessons/12_week_course/week04.md#w04-d02)、[W04-D05](../lessons/12_week_course/week04.md#w04-d05) | [实验约定](../lessons/12_week_course/lab-guide.md) | 完整实现为本周任务 |
| 超时、子进程、清理 | [W04-D04](../lessons/12_week_course/week04.md#w04-d04) | [E08](../lessons/days07_09/day08.md) | [lesson08.py](../mini_harness/lesson08.py)、[固定 worker](../mini_harness/timeout_worker.py) |
| JSONL、轨迹、事件 | [W07-D01](../lessons/12_week_course/week07.md#w07-d01) | [E04](../lessons/six_day_pack/day04.md) | [lesson04.py](../mini_harness/lesson04.py) |
| SQLite、检查点、恢复冲突 | [W05](../lessons/12_week_course/week05.md) | [E09](../lessons/days07_09/day09.md)、[S02](../lessons/source_mastery/state-and-context.md) | [lesson09.py](../mini_harness/lesson09.py) |
| 上下文、字符与 token | [W06-D01](../lessons/12_week_course/week06.md#w06-d01)、[W06-D02](../lessons/12_week_course/week06.md#w06-d02) | [E05](../lessons/six_day_pack/day05.md) | [lesson05.py](../mini_harness/lesson05.py) |
| 长输出、检索、摘要 | [W06-D03](../lessons/12_week_course/week06.md#w06-d03) 至 [W06-D05](../lessons/12_week_course/week06.md#w06-d05) | [S02](../lessons/source_mastery/state-and-context.md) | [工程契约](../lessons/12_week_course/engineering-contracts.md) |
| 100 元预算、用量、重试 | [W07-D03](../lessons/12_week_course/week07.md#w07-d03) 至 [W07-D05](../lessons/12_week_course/week07.md#w07-d05) | [实验报告模板](../lessons/12_week_course/experiment-template.md) | 实际调用前核对服务价格 |
| 工具协议 MCP | [W10-D05](../lessons/12_week_course/week10.md#w10-d05) | [W10-D06](../lessons/12_week_course/week10.md#w10-d06) | 接入实验为本周任务 |

## Hermes 记忆机制

| 想查的内容 | 直接阅读 | 配套 |
| --- | --- | --- |
| MEMORY.md、USER.md、profile、状态分类 | [H01 保存与读取](../lessons/hermes_memory/01-storage-and-read.md) | [专题总入口](../lessons/hermes_memory/README.md) |
| 冻结快照、写入后何时可见 | [H01 快照时序](../lessons/hermes_memory/01-storage-and-read.md) | [memory_lab.py](../mini_harness/memory_lab.py) |
| add / patch / remove、容量、批次回滚 | [H02 写入与一致性](../lessons/hermes_memory/02-write-and-consistency.md) | [test_memory_lab.py](../test_memory_lab.py) |
| staged、pending、审批与后台修改 | [H02 写入许可](../lessons/hermes_memory/02-write-and-consistency.md) | [H04 故障定位](../lessons/hermes_memory/04-review-and-compression.md) |
| session_search、FTS5、中文检索 | [H03 检索](../lessons/hermes_memory/03-recall-and-providers.md) | [固定源码索引](../lessons/source_mastery/source-index.json) |
| 外部 provider、生命周期与超时 | [H03 扩展接口](../lessons/hermes_memory/03-recall-and-providers.md) | [S02 状态边界](../lessons/source_mastery/state-and-context.md) |
| 后台复盘、压缩、提示刷新、成本 | [H04 复盘与压缩](../lessons/hermes_memory/04-review-and-compression.md) | [W07 轨迹与预算](../lessons/12_week_course/week07.md) |
| 错误记忆、失忆排查、记忆评测 | [H04](../lessons/hermes_memory/04-review-and-compression.md)、[H05](../lessons/hermes_memory/05-labs-and-assessment.md) | [实验模板](../lessons/12_week_course/experiment-template.md) |

## 任务、评测、项目交付

| 想查的内容 | 直接阅读 | 对应材料 |
| --- | --- | --- |
| 固定案例报告与回归 | [E06](../lessons/six_day_pack/day06.md) | [lesson06.py](../mini_harness/lesson06.py) |
| 30 题、开发集 / 保留集、独立评分 | [任务目录](../lessons/12_week_course/task-catalog.md)、[W08](../lessons/12_week_course/week08.md) | [任务材料](../mini_harness/course_task_data.py)、[准备与校准工具](../mini_harness/course_tasks.py) |
| 基线、两项改进、消融与失败分析 | [W09](../lessons/12_week_course/week09.md) | [实验报告模板](../lessons/12_week_course/experiment-template.md) |
| 重复运行、费用和复现 | [W11](../lessons/12_week_course/week11.md) | [实验操作约定](../lessons/12_week_course/lab-guide.md) |
| 架构说明、10 分钟讲解、简历 | [W12](../lessons/12_week_course/week12.md) | [架构模板](../lessons/12_week_course/architecture-template.md)、[面试练习](../lessons/12_week_course/interview-kit.md) |
| 119 项检查与材料校准证据 | [备课核验报告](../course-verification.md) | [校准 JSON](../verification/course-calibration.json) |
| 我学到哪里了 | [主线进度表](../lessons/12_week_course/progress.md) | [P00 记录](../lessons/01_tool_call/learning-log.md)、[E01—E06 日志](../lessons/six_day_pack/study-log.md)、[E07—E09 日志](../lessons/days07_09/study-log.md) |

## GitHub 上怎样快速找

1. 找课程顺序：先看 [学习时间表](study-calendar.md)，点击编号跳到当天讲义。
2. 找某个词：在本页使用浏览器“查找”，例如搜索“恢复”“token”“patch”。
3. 找源码：点击表格中的 Python 文件；想搜索整个仓库时，使用 GitHub 的仓库搜索。
4. 找新材料：看 [更新记录](updates.md) 中的日期与提交链接。
5. 判断是目标还是现成程序：看首页的状态表，以及材料页中的“目标 / 待实现 / 已核验”说明。

[回仓库首页](../README.md) · [按学习时间查课](study-calendar.md) · [按日期查更新](updates.md)
