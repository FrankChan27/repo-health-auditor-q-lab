# repo-health-auditor-q-lab

独立实验仓（非业务仓）。本轮实验：从零使用 agent-jingjing 的 Graph-Loop 方法完成一次真实开发闭环。

## 角色

- **Coordinator / Graph-Loop 状态管理 / 任务派发 / Evidence 汇总**：Kimi（不做业务实现、不做业务审查）。
- **唯一外部执行 Agent**：Amazon Q Developer（Direction Challenge / Executor / Reviewer / REWORK 各为独立执行上下文）。

## 方法继承（方法仓只读）

- `FrankChan27/agent-jingjing` PR#79：`skills/graph-loop/SKILL.md` —— Worker 不得自审 PASS；判决绑定冻结目标与冻结证据；PASS / REWORK / BLOCKED / ESCALATE（本轮扩展 REJECT）；无法合法 PASS 则诚实停止。
- `FrankChan27/agent-jingjing` PR#49：独立 Worker 原则 —— 隔离单元必须是真实、可核验的外部 Agent 身份；派发者只 launch + observe；进程内 lane / 子代理 / 同会话角色不得冒充独立执行体。

## 产品主题

**GitHub Repo Health Auditor**：给定一个本地 Git 仓库目录，检查其基本工程健康状态并生成结构化报告。详见 `docs/FROZEN_GOALS.md`。

## 规则

- 本仓 PR 一律不自动 merge。
- 完整可审计证据保留在 `docs/evidence/` 与 GitHub Issues/PRs 中。
- Graph-Loop 状态见 `docs/GRAPH_LOOP_STATE.md`。
