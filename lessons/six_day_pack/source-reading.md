# 真实源码对照：每次只跟踪一条路径

源码位置于 2026-10-23 核对。这里登记版本和入口，材料已备好不等于学习者已完成源码精读。
Python 实验是本项目的教学实现，没有整份复制第三方项目。阅读原项目时遵守其许可证。

## 第 2 天：Codex 工具路由

- 官方仓库：[openai/codex](https://github.com/openai/codex)。
- 核对时 HEAD：`e6ebdfe00b520e21ed50ac0362656f32dd64d2fc`。
- 已读取该提交的文件：[codex-rs/core/src/tools/router.rs](https://github.com/openai/codex/blob/e6ebdfe00b520e21ed50ac0362656f32dd64d2fc/codex-rs/core/src/tools/router.rs)。
- 读取到的文件 blob：`36fbfe442724f9f0ae7b003f336a104713591880`。

先在文件中搜索 `build_tool_call`：它从响应项取工具名、调用标识及参数，构造内部的工具请求。
再搜索 `dispatch_tool_call_with_code_mode_result_inner`：观察请求信息如何进入 invocation，
随后交给 registry 分发。暂时只认识数据和函数的去向，复杂参数可以稍后解释。

与 `mini_harness/lesson02.py` 比较：两边都有请求描述和分发；教学注册表只提供两个工具，
Codex 还包含命名空间、工具暴露方式和运行状态等设计。本课的字典不能直接当成 Codex 的完整接口。

回来聊天时可以问：“请只带我读 build_tool_call 的一个分支，先解释输入和输出。”

## 第 3 天：claw-code 循环

- 学习者提供的本地仓库：`D:\GitHub\claw-code`。
- 已核对本地提交：`08106b0c3771ef5b4a5aa176acccd460e88b7325`。
- 所读文件与该提交内容一致。
- 文件：`rust/crates/claw-analog/src/lib.rs`。
- 对应在线入口：[固定版本的 lib.rs](https://github.com/ultraworkers/claw-code/blob/08106b0c3771ef5b4a5aa176acccd460e88b7325/rust/crates/claw-analog/src/lib.rs)。

按本地已核对版本的位置查找：

| 位置 | 观察点 |
| --- | --- |
| 第 1220 行附近 `run` | 运行入口 |
| 第 1285 行 `for turn in 0..config.max_turns` | 轮次上限 |
| 第 1348 行附近 `collect_tool_uses` | 收集请求与判断是否继续 |
| 第 1355 行之后 | 分发工具、构造带调用标识的结果 |
| 第 1410 行附近 | 结果追加回消息历史 |
| 第 1953 行 `dispatch_tool` | 根据工具名选择执行逻辑 |

先找 `for`、`break`、`messages.push` 和 `dispatch_tool` 四个名字，再画一张控制流程图。
不需要编译整个项目。实际消息协议与 Python 教学格式不同，比较的是控制流程和关联关系。

claw-code 本地 README 指定 `rust/` 为当前主实现，`src/` 为 Python 参考与移植辅助部分；
因此本次循环对照选择 Rust 的较小入口，不把 Python 辅助文件当作主运行时。

## 第 4—6 天的延伸

先完成本项目记录、裁剪和小报告三个实验。它们是入门练习，尚未对应原项目全部日志、上下文或评测系统。
后续按周路线再结合指定版本读这些子系统，避免把一个同名函数当作完整系统。

概念文章可继续参考：

- [The Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness)。
- [Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)。

核心离线练习不要求当时打开网页；之后聊天时可以一起读这些已定位的源码。
