# 从一次调用扩展到一个可靠任务

## 停止由程序与状态共同决定

claw-analog 的 run 使用 max_turns 限定循环，收不到合适的 tool_use 就离开循环。
这可以阻止无限执行，但退出循环并不证明补丁正确。课程中的 model_finished 也是“模型结束”，
任务成功必须另外由工作区之外的评分测试判定。

Codex 的 [session/turn.rs](https://github.com/openai/codex/blob/e6ebdfe00b520e21ed50ac0362656f32dd64d2fc/codex-rs/core/src/session/turn.rs#L173)
包含 run_turn。579—621 行的路径先运行 sampling，再合并模型是否要继续与是否有待处理输入，
得到 needs_follow_up；735 行开始处理无需继续后的停止钩子。真实实现的停止逻辑比“没有 tool_calls 就成功”复杂。
本课只观察这些分支，不把它简化成完整 Codex 状态机。

作业：给自己的循环画出 model_finished、step_limit、invalid_response、interrupted 的迁移。
在只有两次模型调用预算时，第三次请求必须在调用前被拒绝。

## 写了日志与能够恢复不是同一件事

claw 文件中 persist_conversation_sessions（471—486）只在配置会话路径时保存，
SessionFile 保存 version、workspace、model、preset、messages。
run 的退出分支和每批工具结果回传后调用保存。
session_load_messages 校验版本并取回消息；这不等于任何副作用都能恰好执行一次。

Codex 的 [rollout/src/recorder.rs](https://github.com/openai/codex/blob/e6ebdfe00b520e21ed50ac0362656f32dd64d2fc/codex-rs/rollout/src/recorder.rs#L1079)
把 record_canonical_items 送进写入队列，persist 和 flush 通过确认通道等待写入任务。
“成功排队”和“已收到写入确认”是不同边界；也不能仅凭 flush 名字推断断电时全部存储设备行为。

对照 lesson04 与 lesson09：前者是运行后 JSONL 导出；后者保存可恢复的消息和已提交计数。
如果工具完成后、提交检查点前崩溃，恢复仍可能重复执行工具。
当前演示仅用只读工具。未来写文件或产生费用时，要另外设计 intent/result 记录、
幂等标识或保守费用预留，不能宣称已有 exactly-once。

作业：在纸上列出五个中断点，分别预测“消息有没有、结果有没有、预算算没算、是否会重放”。
用现有故障注入测试核对，保留不满足的保证。

## 上下文与完整历史分开

Codex 的 [compact.rs](https://github.com/openai/codex/blob/e6ebdfe00b520e21ed50ac0362656f32dd64d2fc/codex-rs/core/src/compact.rs#L697)
有 build_compacted_history，内部按预算选择用户消息并组合摘要。
这是读过的一个局部构造函数；自动压缩、远端压缩与其他配置分支需要另追入口，
不能把此函数当成所有压缩行为。

自己的项目保留完整事件轨迹，再从中构造给模型看的受预算约束视图。
lesson05 的字符裁剪不是 token 计费；摘要中出现的“测试通过”也不是原始测试证据。
要让摘要带证据 id，并能回查对应事件。

随后进入 [Hermes 专题](../hermes_memory/README.md)：长期记忆、历史检索和上下文压缩分别解决什么问题。
记忆保存“以后仍有用的少量事实”，检查点保存“这项任务如何继续”，不应混为一个大字典。
