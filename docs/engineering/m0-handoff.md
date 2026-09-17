# EDU-000：M0 交接记录

日期：2026-09-17。状态：实现与本地检查已完成，当前仍为未提交工作区；课程与方案待人类 Lead 审阅，尚未合并，不标记 done。

## 交付与基线

- 工作区：`/Users/leo/Documents/Github/agent-study`。
- 分支：`codex/discovery-vertical-agent`，沿用调研阶段分支。
- 基线：`bf28b88`（Initial commit）；本轮没有交付提交 SHA，也没有推送。
- 已确认需求：教育方向、贝叶斯首课、Python；人类与 AI 共同 Lead，Develop 为 AI。
- 已交付：产品与评估方案、架构与学习路线、Git/协作规范、课程草稿、领域校验、JSON 适配器与 CLI。
- 版本：课程 `bayes-intro@0.1.0`、schema `1`、教学状态 `draft`；rubric 为文档 v0.1，尚未实现自动评分或完整评估集。

本次属于一个 M0 任务内的分工：课程与代码、工程规范、产品架构文档分别由明确负责人写入互不重叠的路径；Lead 统一调整公共入口与最终一致性。没有为这些子步骤建立独立 worktree，不宣称具有 worktree 隔离。

## 实际验证

工作目录为仓库根目录，实际环境为 Python 3.14.2。

| 命令/检查 | 结果 |
| --- | --- |
| `PYTHONPATH=src python3 -m unittest discover -s tests -v` | 14 项通过，退出 0 |
| `PYTHONPATH=src python3 -m education_agent validate-course courses/bayes-intro/course.json` | 结构通过，明确显示 draft，退出 0 |
| `PYTHONPATH=src python3 -m education_agent inspect-course courses/bayes-intro/course.json` | 展示 3 个概念、来源与草稿状态，退出 0 |
| `git diff --check` 与文档空白检查 | 通过 |
| 本地 Markdown 相对链接检查 | 无缺失目标 |
| Python 3.11 语法解析 | 通过；不代表已在 3.11 实机运行 |

独立 AI 技术审查未发现阻塞缺陷，并复跑 14 项测试。教学设计审查核对了例题计算与教学效果表述；其提出的独立测验控制、提示等级和评分锚点问题已补入设计。

尚未验证安装后的 console script、Python 3.11 实机环境、模型接入、真实学习过程和教学有效性。尚未配置远端分支保护或 CI。

## 人类 Lead 审阅重点

1. 是否认可第一节只解决一次证据更新，并用未见题检查理解。
2. 首批中文成年学习者假设、课程难度和例题是否合适。
3. 文档中的提示策略、完成条件与领域迁移要求是否符合产品期望。

这些是本次方案的待审内容，不影响读取、运行或修改骨架。既有方向和技术栈选择无需重复确认。

## 下一步与学习重点

先完成 EDU-001 的课程/题目核验，以及 EDU-002 的消息、模型与工具契约教学。下一阶段亲手实现一个有步骤上限的模型工具循环；保留脚本模型，让不接 API 时也能观察每一轮的输入与输出。

本轮的核心认识：课程内容、教学证据、模型判断和执行控制需要分清。离线结构校验可以自动完成；“解释正确”“学习者会应用”需要不同的验收证据。
