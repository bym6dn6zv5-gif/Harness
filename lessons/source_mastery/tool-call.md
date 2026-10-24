# 一次工具调用：模型提出之后发生什么

先回答第一课里容易混淆的问题：模型可以输出“读取 note.txt”的请求。
真正打开文件的是宿主程序中的工具函数；只有执行成功、结果回传后，模型才有证据回答文件内容。
模型一句“我已经读取”不能证明发生了文件读取。

## claw-code：沿一条较短的路径读

打开本机 rust/crates/claw-analog/src/lib.rs。下面行号对应固定提交。

| 位置 | 观察到的动作 | 在 Python 实验中寻找 |
| --- | --- | --- |
| run，1285—1297 | 有界循环；用已有 messages、system、tools 构造请求 | lesson03 的循环与请求输入 |
| 1343—1352 | 先保存 assistant 响应，再收集工具请求；无工具或停止原因不符时退出 | 模型回复也必须进入历史 |
| 1355 起、dispatch_tool 1953 起 | 遍历工具请求，按名称分发 | ToolRegistry.dispatch |
| enforce_tool，1674—1686 | 有 enforcer 才做权限检查；没有则直接通过 | lesson07 的显式策略门 |
| read_file 分支，1967 起 | 调用权限入口后，再解析路径并读取 | 参数、路径、权限是不同检查 |
| 1385、1408—1418 | 以 error: 前缀标记错误；结果带 tool_use_id，整批作为 user 内容块回传 | 本课自定义 role=tool 与 call id |

注意：claw 的结果 role 在该接口中是 user，内容块才是 ToolResult。
第一课使用 role=tool 是教学消息协议，不能把一种 API 的消息结构硬套到另一种 API。
共同约束是每个结果必须关联原来的请求 id。

检查 runtime/src/permission_enforcer.rs 的 check。该入口委托 policy.authorize；
Prompt 情况允许继续交给调用方处理。只看到 PermissionEnforcer 的名字，不能证明已经发生交互审批。
再检查调用方是否创建并传入它、什么策略生效，以及实际执行分支是否经过它。

教学对照：当前 PolicyRegistry 每次 dispatch 都检查固定工具白名单；
它没有操作系统隔离，也没有证明原项目所有执行路径都安全。

动手：给 read_file 与 count_lines 画两条路径；把 count_lines 拒绝后，证明 handler 没被执行。
不能只断言返回了错误文本，要用计数器证明副作用次数为零。

## Codex：同一个请求经过更多层

固定源码入口：

- [tools/router.rs](https://github.com/openai/codex/blob/e6ebdfe00b520e21ed50ac0362656f32dd64d2fc/codex-rs/core/src/tools/router.rs#L257)：build_tool_call。
- [stream_events_utils.rs](https://github.com/openai/codex/blob/e6ebdfe00b520e21ed50ac0362656f32dd64d2fc/codex-rs/core/src/stream_events_utils.rs#L325)：接收工具输出项、记录、安排执行。

build_tool_call 的输入是 ResponseItem。FunctionCall 分支保留 call_id，
把名称和 namespace 转成 ToolName，把 arguments 放进 ToolPayload::Function。
CustomToolCall 和客户端 ToolSearchCall 有各自分支；其他响应项可以返回 None。
工具搜索参数解析失败会成为可反馈给模型的错误。

这里没有证明所有普通工具参数都已校验。普通 FunctionCall 的 arguments 在该函数中仍作为载荷传下去；
各工具的具体校验需要继续追 handler。把“解析为内部调用对象”和“验证所有参数”分开解释。

随后在 stream_events_utils 的工具分支中，先记录响应项，再取得取消令牌与工具运行时，
安排 handle_tool_call。延迟执行分支如果已取消，也要制造 aborted_response，
因为历史里已有调用，恢复时仍然需要一个匹配的输出。

router 的 dispatch_tool_call_with_code_mode_result_inner（359—393）把 session、step_context、
cancellation_token、tracker、call_id、tool_name 和 payload 组合为 ToolInvocation，
交给 registry.dispatch_any_with_state。路由层负责连接，不承担整个执行环境的全部职责。

~~~mermaid
flowchart LR
  A[模型响应项] --> B[build_tool_call 转成内部调用]
  B --> C[记录请求项]
  C --> D[工具运行时安排执行]
  D --> E[router 组装 ToolInvocation]
  E --> F[registry 与具体 handler]
  F --> G[关联原 call_id 的结果]
  G --> H[后续模型请求]
~~~

这张图概括核对过的调用关系，不覆盖所有 hosted tool、并行、code mode 或审批分支。

## 需要自己完成的四个解释

1. 为什么保存 assistant 调用之后，还必须补回工具结果？
2. 未知工具、参数错误、权限拒绝，分别在哪一层最适合返回？
3. 如果“记录调用之后、执行之前”中断，恢复时怎样避免悬空请求？
4. 为什么工具注册、对模型展示、运行时允许执行是三个问题？

验收：关闭讲义，写出一个最小 Python 分发器，并为上面三个错误各写一个反例。
不要把原项目字符串错误协议直接复制成新项目的最终协议；说明自己为何选择结构化错误。
