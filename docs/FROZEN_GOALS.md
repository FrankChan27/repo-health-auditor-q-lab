# FROZEN GOALS v2 — GitHub Repo Health Auditor

冻结时间：2026-08-30（协调者：Kimi）
修订记录：v1 @ `2c6aacc` 经 Amazon Q Direction Challenge（PR#3, review `5060507710`）裁决 **REVISE GOAL**，按 3 条 inline 意见修订为本版（只修订目标，未提前施工）。修订后本文件重新冻结。

## 目标

实现一个小而完整、可运行、可测试的命令行工具：**给定一个本地 Git 仓库目录，检查其基本工程健康状态，并生成结构化报告。**

## 必须满足的验收项（可客观判定）

1. 检查目标仓库根目录是否存在 README 类文件（README / README.md / README.rst 等大小写不敏感）。
2. 检查是否存在测试，仅依据以下封闭约定：`test/`、`tests/`、`__tests__/` 目录，或文件名匹配 `*_test.go`、`test_*.py`、`*.test.*`、`*.spec.*`。
3. 检查是否存在 CI 配置，仅依据以下封闭集合：`.github/workflows/` 下存在至少一个非空 `.yml`/`.yaml` 文件，或根目录存在 `.gitlab-ci.yml`、`.circleci/config.yml`、`Jenkinsfile`。
4. 检查项目元数据文件，**封闭清单**（不再使用"等"）：`package.json`、`pyproject.toml`、`setup.py`、`go.mod`、`Cargo.toml`、`pom.xml`。逐项报告存在与否；全部缺失时标记为"元数据缺失"。
5. 生态/语言栈识别**只做基于第 4 项封闭清单的查表映射**（例如 `package.json` → Node.js，`go.mod` → Go）；命中几个报几个，全部未命中输出"未识别"。不做任何更深入的分析。
6. 输出机器可读结果：JSON（stdout 或文件），含每项检查的布尔/枚举结果与汇总。
7. 输出人类可读摘要：纯文本或 Markdown 摘要，与 JSON 内容一致。
8. 自带自动化测试，覆盖上述关键行为；测试在干净环境中一条命令可跑通。
9. README 一致性的**可度量标准**：README 中记录的每个 CLI 参数都必须真实可用；README 声称的每种输出格式都必须真实产出；README 中的用法示例命令必须能成功运行。

## 边界（明确排除）

- 不访问网络、不调用 GitHub API；输入仅为本地目录。
- 不做代码质量分析、不做安全扫描、不做依赖漏洞检查。
- 不做 GUI / Web 服务。
- 技术栈、CLI 参数形式、目录结构由 Executor 独立决定。

## 裁决

由独立 Amazon Q Reviewer 对冻结证据给出 PASS / REWORK / BLOCKED / REJECT。任何人（含 Kimi）不得自审 PASS。
