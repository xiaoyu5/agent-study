# learn-claude-code 调研

调研日期：2026-09-17。性质：开发前的研究记录，不代表本项目已选定技术栈或垂直方向。

参考仓库：[shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code)。本次核实的 main 提交为 [`0dcafa2ae053a1ddd6a72f265431104b08a5aa13`](https://github.com/shareAI-lab/learn-claude-code/commit/0dcafa2ae053a1ddd6a72f265431104b08a5aa13)，提交日期为 2026-08-26。以下源码链接固定到该版本。

## 结论

适合用它学习 Agent 的运行机制，再围绕一个真实业务闭环独立实现项目。上游的价值是把循环、工具、上下文、任务和协作拆开讲清楚；本项目还需要补上领域规则、评估样本、执行边界和交付要求。

上游 [CONTRIBUTING.md](https://github.com/shareAI-lab/learn-claude-code/blob/0dcafa2ae053a1ddd6a72f265431104b08a5aa13/CONTRIBUTING.md) 明确以教学可读性为目标，保留了一些有意的简化。因此，不能把章节可运行等同于产品可上线。这是对参考项目用途的判断，不是对本项目的外部约束。

## 当前课程结构

当前主线为根目录 `s01_*` 到 `s17_*`，每章有代码和中英日说明。`agents/`、`docs/` 保留旧 12 章版本，学习时应避免混用编号。见 [README-zh.md](https://github.com/shareAI-lab/learn-claude-code/blob/0dcafa2ae053a1ddd6a72f265431104b08a5aa13/README-zh.md)。

| 章节 | 机制 | 对本项目的学习价值 |
| --- | --- | --- |
| s01–s02 | 模型循环、工具定义与分发 | 亲手实现一次请求、调用工具、回传结果、继续推理的闭环 |
| s03–s04 | 权限检查、生命周期 hooks | 把“能调用”与“允许执行”分开；给日志、审计留清晰入口 |
| s05–s06 | 当前任务计划、隔离子 Agent | 理解计划与执行的关系，以及上下文隔离的用途 |
| s07–s09 | 按需加载技能、上下文压缩、跨会话记忆 | 区分业务知识、当前对话、任务状态和长期记忆 |
| s10–s12 | 持久任务、后台任务、调度 | 学习依赖、恢复和慢任务的生命周期 |
| s13 | 团队、消息协议、任务认领、worktree | 理解协作控制，以及工作目录隔离 |
| s14–s15 | 外部工具池、集成运行时 | 理解多种机制如何接入同一个主循环 |
| s16–s17 | 固定流程编排、目标完成判断 | 区分确定性流程和模型判断，并明确何时停止 |

章节并非全部按前一章累积扩展。特别是 s17 的示例基于 s04 内核，不能直接视为 s15 的完整升级版。见 [s17 源码](https://github.com/shareAI-lab/learn-claude-code/blob/0dcafa2ae053a1ddd6a72f265431104b08a5aa13/s17_goal_loop/code.py)。

## 从实际代码得到的关键认识

1. **循环根据实际工具调用继续。** s01 的 `agent_loop()` 将 assistant 响应追加到历史，提取实际 `tool_use` 块，逐个执行并用相同调用 ID 回传结果；没有工具调用时结束。s02 引入工具分发表，仍是串行执行，不能因为总览提到并发就认定这一章已经并发。见 [s01](https://github.com/shareAI-lab/learn-claude-code/blob/0dcafa2ae053a1ddd6a72f265431104b08a5aa13/s01_agent_loop/code.py#L87)、[s02](https://github.com/shareAI-lab/learn-claude-code/blob/0dcafa2ae053a1ddd6a72f265431104b08a5aa13/s02_tool_use/code.py#L153)。
2. **权限策略与系统隔离是两层问题。** s03 展示命令字符串检查、上下文规则和终端确认；它不是操作系统沙箱。s15 增强了宿主权限策略，文件越界会被拒绝，bash 需要前台确认，需要交互批准的异步操作会被拒绝。仍不能靠这些检查证明任意命令执行已被可靠隔离。见 [s03](https://github.com/shareAI-lab/learn-claude-code/blob/0dcafa2ae053a1ddd6a72f265431104b08a5aa13/s03_permission/code.py#L191)、[s15 权限入口](https://github.com/shareAI-lab/learn-claude-code/blob/0dcafa2ae053a1ddd6a72f265431104b08a5aa13/s15_integrated_harness/code.py#L1762)。
3. **上下文不是越多越好。** s07 先提供技能目录，再按需读取正文；s08 分阶段控制工具输出与历史大小；压缩仍须保留工具调用与结果的配对关系。见 [s07](https://github.com/shareAI-lab/learn-claude-code/blob/0dcafa2ae053a1ddd6a72f265431104b08a5aa13/s07_skill_loading/README.zh.md)、[s08](https://github.com/shareAI-lab/learn-claude-code/blob/0dcafa2ae053a1ddd6a72f265431104b08a5aa13/s08_context_compact/code.py)、[配对回归测试](https://github.com/shareAI-lab/learn-claude-code/blob/0dcafa2ae053a1ddd6a72f265431104b08a5aa13/tests/test_compaction_tool_pairs.py)。
4. **记忆不等于业务事实库。** s09 有选择、提取和整理机制，也区分临时任务约束与持久信息。本项目仍应让关键业务结论指向原始证据，并处理版本和失效问题。见 [s09](https://github.com/shareAI-lab/learn-claude-code/blob/0dcafa2ae053a1ddd6a72f265431104b08a5aa13/s09_memory/README.zh.md)。
5. **工具协议示例不等于真实连接器。** s15 的 `MCPClient` 明确是进程内替代实现，用于演示工具发现和调用；真实 MCP 传输、鉴权和连接生命周期需另外实现。见 [MCPClient](https://github.com/shareAI-lab/learn-claude-code/blob/0dcafa2ae053a1ddd6a72f265431104b08a5aa13/s15_integrated_harness/code.py#L2600)。
6. **“模型停止回答”与“业务任务完成”需要区分。** s17 展示独立完成判断和续轮，但产品验收还需要可核实证据、确定性检查及预算上限。见 [s17](https://github.com/shareAI-lab/learn-claude-code/blob/0dcafa2ae053a1ddd6a72f265431104b08a5aa13/s17_goal_loop/README.zh.md)。

## 我们需要自行补齐的工程内容

以下是本项目建议，不是声称上游完全没有相应机制。应按选定场景逐项实现。

| 边界 | 需要明确的内容 |
| --- | --- |
| 业务任务 | 明确输入、输出、证据、成功条件、信息不足与转人工条件 |
| 工具契约 | 参数校验、结构化错误、超时、结果大小限制、允许操作范围 |
| 运行控制 | 最大轮次、耗时和 token/费用预算；取消、失败与结束状态 |
| 外部副作用 | 区分可重试读取和写入；需要时加入幂等键、执行记录和结果核对 |
| 状态与知识 | 将会话历史、持久任务、原始证据和可失效记忆分别管理 |
| 可观测性 | 每次运行可追踪模型调用、工具参数与结果、耗时、成本和错误 |
| 质量评估 | 固定样本、无 Agent 基线、自动校验和必要的人工评分 |
| 上线条件 | 与实际部署范围匹配的隔离、身份、数据保留和恢复策略 |

## 学习与交付如何结合

建议每一阶段只引入少量机制，并完成“原理讲解 → 小练习 → 项目实现 → 失败案例 → 验收 → 学习记录”。下表是讨论用顺序，正式里程碑和阈值在方向确定后编写。

| 阶段 | 学习重点 | 可检查的产出 |
| --- | --- | --- |
| M0 | 场景建模与基线 | 任务边界、人工核验样本、成功标准、开发规范 |
| M1 | s01–s02 | CLI 发起任务，单 Agent 调用少量领域工具，返回有证据的结果 |
| M2 | s03–s04 | 工具校验、操作范围、预算和运行记录；失败能明确结束 |
| M3 | s07–s08，必要时 s09 | 按需读取知识和长输入处理；关键证据可追溯 |
| M4 | s10–s11，必要时 s16 | 状态持久化、取消与中断恢复；副作用不被盲目重复 |
| M5 | 实际部署与评估 | 回归报告、运行说明、成本记录和一个真实使用闭环 |
| 按需扩展 | s06/s12/s13/s14/s17 | 仅在场景证明需要时加入子 Agent、调度、多 Agent、外部协议或目标续轮 |

Lead/Develop 多人开发协作从 M0 建立；产品运行时的多 Agent 属于后续可选能力。这两者不应绑定。

## 核查范围

本次核实了仓库版本、主线章节、关键源码及相关测试文件内容。未运行上游完整测试、未调用真实模型，也未进行真实 MCP 或生产部署验证。当前工作区尚未实现业务 Agent。
