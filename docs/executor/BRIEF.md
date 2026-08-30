# Executor Brief（给 Amazon Q Executor）

你是本阶段的 **Amazon Q Executor**，独立执行上下文。协调者（Kimi）不会替你写任何业务代码。

## 任务

在本分支上完整实现 **GitHub Repo Health Auditor**，验收标准以本仓 `docs/FROZEN_GOALS.md`（v2, @ `ff88b01`）为唯一准绳。技术栈、CLI 形式、目录结构由你独立决定。

## 必须交付

1. 可运行的 CLI 工具（输入：本地 Git 仓库目录）。
2. 全部 9 条验收项对应的功能。
3. 自动化测试，一条命令可在干净环境跑通。
4. 与实现一致的工具 README（放在 `auditor/` 或你选择的子目录，勿覆盖仓根协调 README）。
5. 实现完成后在 PR 中回复：实际 HEAD、测试命令、测试结果摘要。

## 禁止

- 不修改 `docs/FROZEN_GOALS.md`、`docs/GRAPH_LOOP_STATE.md`、`docs/direction/`、`docs/evidence/`。
- 不 merge 本 PR。
- 不自我宣布 PASS——裁决属于后续独立 Reviewer。
