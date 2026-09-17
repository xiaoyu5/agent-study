# agent-study

以学习为目的，从 0 到 1 开发教育 Agent，帮助普通人理解复杂理论，并应用到自己的领域。

首课：**新证据如何改变判断——贝叶斯更新与基准率**。技术栈：Python 3.11+。人类与 AI 共同担任 Lead，一个或多个 AI 担任 Develop。

当前是 **M0 基础骨架**：支持离线课程包结构校验与查看。课程内容为草稿；尚无模型调用、Agent 循环、教学对话、自动评分或 Web 界面。

本轮验证和待审事项见 [M0 交接记录](docs/engineering/m0-handoff.md)。

## 从这里阅读

1. [产品与首课范围](docs/product/education-agent.md)：为谁做、学什么、最小学习闭环。
2. [学习效果评估](docs/product/evaluation.md)：如何区分听懂、有提示做对与独立应用。
3. [架构与骨架](docs/engineering/architecture.md)：当前模块、未来边界与选型理由。
4. [开发与学习路线](docs/engineering/development-plan.md)：每个里程碑做什么、如何验收。
5. [Git 分支规范](docs/engineering/git-workflow.md)与[Lead / Develop 协作规范](docs/engineering/collaboration.md)。

调研背景见 [learn-claude-code 研究记录](docs/research/learn-claude-code.md)；方向选择过程见 [讨论记录](docs/discovery/vertical-options.md)。

## 运行 M0

在仓库根目录运行，无需安装依赖或配置 API key：

```sh
PYTHONPATH=src python3 -m education_agent validate-course courses/bayes-intro/course.json
PYTHONPATH=src python3 -m education_agent inspect-course courses/bayes-intro/course.json
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

校验通过仅表示课程结构和引用有效，不能替代教学内容审核。后续模型 SDK、依赖锁定与 CI 随对应里程碑加入。

下一步是一起核验首课例题，并手写第一个“模型 → 工具 → 结果 → 模型”的循环。每次只增加一个可解释、可验证的能力。
