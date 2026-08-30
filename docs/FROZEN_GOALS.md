# FROZEN GOALS — GitHub Repo Health Auditor

冻结时间：2026-08-30（协调者：Kimi）
冻结对象：本轮唯一产品目标。除 Direction Challenge 提出真实问题后修订外，任何角色不得扩大范围。

## 目标

实现一个小而完整、可运行、可测试的命令行工具：**给定一个本地 Git 仓库目录，检查其基本工程健康状态，并生成结构化报告。**

## 必须满足的验收项（可客观判定）

1. 检查目标仓库根目录是否存在 README 类文件（README / README.md / README.rst 等大小写不敏感）。
2. 检查是否存在测试（测试目录或测试文件的常见约定，如 `test/`、`tests/`、`__tests__/`、`*_test.go`、`test_*.py`、`*.test.*`、`*.spec.*` 等）。
3. 检查是否存在 CI 配置（如 `.github/workflows/` 下有非空 yaml/yml，或 `.gitlab-ci.yml`、`.circleci/config.yml`、`Jenkinsfile` 等常见 CI 文件）。
4. 检查常见项目元数据文件是否存在（按可识别的生态判断，如 `package.json`、`pyproject.toml`、`setup.py`、`go.mod`、`Cargo.toml`、`pom.xml` 等）；全部缺失时应标记为"元数据缺失"。
5. 依赖/项目结构基本可识别：输出识别到的生态/语言栈（可以是"未识别"）。
6. 输出机器可读结果：stdout 或文件的 JSON，含每项检查的布尔/枚举结果与汇总。
7. 输出人类可读摘要：纯文本或 Markdown 摘要，与 JSON 内容一致。
8. 自带自动化测试，覆盖上述关键行为；测试在干净环境中一条命令可跑通。
9. 工具自身 README 与实际行为一致（用法、参数、输出格式）。

## 边界（明确排除）

- 不访问网络、不调用 GitHub API；输入仅为本地目录。
- 不做代码质量分析、不做安全扫描、不做依赖漏洞检查。
- 不做 GUI / Web 服务。
- 技术栈、CLI 参数形式、目录结构由 Executor 独立决定。

## 裁决

由独立 Amazon Q Reviewer 对冻结证据给出 PASS / REWORK / BLOCKED / REJECT。任何人（含 Kimi）不得自审 PASS。
