# 以 claw-code 与开源 Codex 为主教材

学习目标是能沿着一次真实调用解释数据变化、定位失败点，再独立修改自己的 Python 实现。
“吃透”按可检查的能力验收：找到入口，追到执行与回传，解释一个异常分支，设计反例，修改后给出测试。
不能以读完说明、运行参考答案或助手准备完课程代替这些能力。

## 固定版本与阅读边界

- claw-code：本机 D:\GitHub\claw-code，提交 08106b0c3771ef5b4a5aa176acccd460e88b7325。
- [Codex 源码](https://github.com/openai/codex/tree/e6ebdfe00b520e21ed50ac0362656f32dd64d2fc)：提交 e6ebdfe00b520e21ed50ac0362656f32dd64d2fc。
- [Hermes 记忆专题](../hermes_memory/README.md)：提交 d764d0c7e20f33bac869b6ebd34570de0cb6e069。

本轮已核对下面讲义明确引用的调用路径。庞大的仓库还有许多未读模块，
“教材已准备”不等于“整库逐行读完”。未深入审核的执行器、安全策略、并行调度等列入后续阅读，
不根据类名推断实现。我们不运行或修改教材仓库，也不把 Codex 开源代码等同于桌面应用全部内部实现。
版本证据见 [source-index.json](source-index.json)。

## 三份主讲义

1. [一次工具调用：两套真实实现与 Python 对照](tool-call.md)。
2. [会话、停止条件、持久化与上下文](state-and-context.md)。
3. [贯穿 12 周的源码任务与能力验收](curriculum-map.md)。

初学者先完成现有第一课；先解释“模型提出，程序执行”，再看真实源码中的同一条线。
Rust 语法按需讲：struct 是一组字段，enum 表示不同情况，Option 表示有或没有，
Result 区分成功与错误，await 等待异步结果。先看输入、输出、分支，不要求现在编译 Rust。

每次笔记都保留五项：提交、文件与符号；原实现观察；Python 对应；失败反例；尚未确认。
每周聊天时带一张数据流图和一个失败日志，我会根据你能否解释并修改来验收。
