# Hermes 记忆机制：从文件到下一轮回答

[回仓库首页](../../README.md) · [按时间查课](../../docs/study-calendar.md) · [按主题查资料](../../docs/reference-index.md)

教材对象已由学习者确认：[NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)。
本专题锁定提交 **d764d0c7e20f33bac869b6ebd34570de0cb6e069**，核对日期 2026-10-24。
接口发展很快，下面“当前”均指这个版本，不保证其他版本一致。

先用一句话理解：Hermes 把少量值得长期保留的事实写到文件，
把会话保存在数据库，再在合适时机把相关内容送进模型的输入。
模型回答依赖它当时看到了什么；这些机制没有把你的个人事实训练进模型权重。

## 学习次序

| 课 | 解决的问题 | 留下的证据 |
| --- | --- | --- |
| [1：六类状态与读取路径](01-storage-and-read.md) | 记忆、历史、摘要、技能、检查点有什么区别 | 一张分层图与逐字段表 |
| [2：写入、容量与一致性](02-write-and-consistency.md) | 怎样保存，修改为什么会失败 | patch、歧义、预算、批次反例 |
| [3：检索与 provider](03-recall-and-providers.md) | 历史怎样找回来，是否需要向量库 | 搜索→阅读→定位原证据的练习 |
| [4：后台复盘、压缩与安全](04-review-and-compression.md) | 谁决定保存，什么时候会花钱或刷新 | 两条时序图和故障定位表 |
| [5：实验、评测与口头验收](05-labs-and-assessment.md) | 怎样验证记忆有没有帮助 | 离线实验、对照表、独立修改 |

按每课约 2 小时推进，可以拆成多天。第一课先读分类；写入实验放在学过第 7—9 天后。
当前没有安装 Hermes，没有读取你机器的 Hermes 个人记忆，没有调用模型，没有产生 API 费用。
Python 实验是本课程自编的机制缩影；它没有冒充 Hermes 的实现或运行结果。

## 源码导航

以固定提交为准，文件链接集中于 [版本索引](../source_mastery/source-index.json)：

- agent/agent_init.py：_init_memory，初始化文件记忆与可选外部 provider。
- agent/system_prompt.py：_memory_parts、invalidate_system_prompt，注入与刷新。
- tools/memory_tool.py：模型工具入口、参数、审批与后台修改门。
- tools/memory_tool_store.py：MemoryStore、load_from_disk、_mutate、patch、apply_batch。
- tools/session_search_tool.py：历史发现、阅读、围绕消息滚动。
- hermes_state_search.py、hermes_state_fts.py：本地检索路线与索引降级。
- agent/memory_manager.py、memory_provider.py：扩展接口与生命周期。
- agent/turn_finalizer.py、background_review.py：回合结束后的条件复盘。
- agent/conversation_compression_checkpoint.py：要求可靠检查点时的压缩拒绝。

已读范围是这些职责及讲义引用的分支；未逐一审核全部 provider、数据库迁移、
所有压缩分支和模型服务。碰到未核对的问题，先记录未知再追代码。
