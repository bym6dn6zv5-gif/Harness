# 教材来源与使用方式

## 当前第一课采用什么教材

当前第一课是助手根据本项目目标单独编写的 Python 教学实验，文件为
`src/mini_harness/lesson01.py`，对应测试为 `tests/test_lesson01.py`。

它用预先写好的模拟回复展示“提出工具调用 → 程序校验并执行 → 回传结果 → 回答”的过程。
代码和自定义消息格式是本项目的教学实现；目前没有移植 Codex 或 claw-code 的实现，
也没有用真实模型评测来验证模型能力。

课程由小实验逐步进入真实项目源码。每次源码阅读都要明确区分：原项目的行为、教学实验的简化、学习者的理解。

## 源码实例教材

| 材料 | 阅读用途 | 当前状态 |
| --- | --- | --- |
| [OpenAI Codex](https://github.com/openai/codex) | 对照学习真实编程 Agent 的工具分发、会话、执行约束与上下文管理 | 已核对官方仓库入口及 `codex-rs/` 目录；具体实现尚未按课精读 |
| 学习者本机 `D:\GitHub\claw-code` | 与另一套实现对照工具执行、权限、会话及 MCP 的设计 | 已检查本机 README 和结构；README 指明 `rust/` 为当前主实现，`src/` 为 Python 参考与移植辅助部分 |
| [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) | 辅助阅读较小的循环、模型与执行环境实现 | 已列入第 10 周的辅助阅读，尚未进行本项目内的源码练习 |

Codex 的官方仓库用于理解开源 Codex CLI 的实现。课程中对源码的结论应限定到所检查的版本和代码，
不能由此直接推断桌面应用或云端产品的全部内部实现。

进入每次源码课时，先记录仓库地址、commit、文件路径和符号，再说明它与本课实验的对应关系。
当前没有固定 Codex 源码快照，不把动态分支链接描述为已验证的具体实现。
外部项目源码不在本学习仓库中整份复制；阅读其源码时遵守相应许可证。

## 概念和工程文章

- [The Anatomy of an Agent Harness，LangChain](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness)：帮助认识模型周围的工具、状态和执行逻辑。
- [Effective harnesses for long-running agents，Anthropic](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)：后续学习跨会话进度、增量工作和验证。

这些文章提供课程的概念与设计参考。第一课的代码并非这些文章随附的官方示例。

## 学习节奏

每节先运行一个可观察的小实验，再解释对应的 Python 代码；具备基础后，对照真实项目的指定源码片段。
源码精读阶段按需要解释少量 Rust 语法，优先跟踪数据与控制流程。
