# 项目协作入口

本项目用于学习如何从零开发教育 Agent。先阅读 README、docs/product/education-agent.md、docs/engineering/development-plan.md 和当前任务，再决定实现范围。用户当次明确指令优先。

## 工作方式

- 人类与 AI 共同担任 Lead；Develop 是一个或多个 AI。详见 docs/engineering/collaboration.md。
- 每次任务先明确学习目标、允许修改路径、依赖和验收条件；小步实现并解释设计原因。
- 只实现当前任务需要的能力，不为未来可能的需求提前铺开框架或多 Agent 系统。
- 领域规则与外部模型 SDK、界面和存储分离；课程、题目、评分与提示词变化必须记录版本。
- 独立任务按 docs/engineering/git-workflow.md 使用短期分支与 worktree。同任务子代理共享目录时必须分配互斥写入范围，由 Lead 统一管理 Git。
- Develop 自检不替代 Lead 审核；重要需求、学习目标和评分标准的变更交 Lead 决策。已授权范围内的编辑与验证自主完成，不逐步重复请求确认。
- 未完成的能力、未执行的检查和草稿内容必须明确标识。结构测试通过不代表教学正确，更不代表学习效果已验证。

## 当前验证

从仓库根目录、Python 3.11+ 运行：

```sh
PYTHONPATH=src python3 -m education_agent validate-course courses/bayes-intro/course.json
PYTHONPATH=src python3 -m education_agent inspect-course courses/bayes-intro/course.json
PYTHONPATH=src python3 -m unittest discover -s tests -v
git diff --check
```

当前测试覆盖 M0 课程骨架。新增能力应补充有实际意义的行为验证；不要为纯文案调整编写镜像测试。交接记录需包含实际命令、结果、限制和下一步学习重点。
