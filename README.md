# Agent Skill Forge

面向工程协作、任务规划、长期学习和知识交接的 Agent Skills 集合。

本项目提供一组可直接安装到 Agent 运行环境中的技能包，覆盖工程开发、计划澄清、任务交接、长期学习和 skill 写作。仓库内容保持精简，只包含当前可维护、可验证、可组合使用的 skill 与配套文档。

## 特性

- **工程工作流完整**：覆盖需求澄清、PRD、issue 拆分、实现、调试、TDD、架构改进、领域建模和本地 triage。
- **规划与交接能力**：提供 `grill-me`、`grilling`、`grill-with-docs` 和 `handoff`，适合多轮计划、跨会话协作和上下文压缩。
- **学习系统能力**：支持概念学习、技能训练、论文深读、仓库课程、科研路线和长线课程 proof loop。
- **精简项目结构**：正式 skill 只分为 `engineering` 和 `productivity` 两类，入口、文档和插件清单保持一致。
- **可验证的 skill 包**：提供脚本检查 skill 清单、学习系统结构、source matrix、manifest 和 HTML 教学模板。

## 快速开始

列出当前仓库中的全部 skill：

```bash
./scripts/list-skills.sh
```

安装全部 skill 到默认 Agent skill 目录：

```bash
bash scripts/install.sh
```

远程安装：

```bash
curl -fsSL https://raw.githubusercontent.com/charSLee013/Agent-Skill-Forge/master/scripts/install.sh | bash
```

只安装指定 skill：

```bash
bash scripts/install.sh teach handoff grill-me
```

默认安装位置是：

```text
~/.agents/skills
```

安装到 Codex：

```bash
AGENT=codex bash scripts/install.sh
```

安装到 Claude Code：

```bash
AGENT=claude bash scripts/install.sh
```

安装到 OpenCode：

```bash
AGENT=opencode bash scripts/install.sh
```

项目仓库：

```text
https://github.com/charSLee013/Agent-Skill-Forge
```

Claude 插件清单位于：

```text
.claude-plugin/plugin.json
```

## Skill 清单

### Engineering

工程类 skill 面向代码仓库中的真实开发流程，包括规划、拆分、实现、调试、测试、架构和本地 issue 工作区。

#### 用户显式调用

| Skill | 作用 |
|---|---|
| [ask-skills](./skills/engineering/ask-skills/SKILL.md) | 根据当前任务选择合适的 skill 或工作流。 |
| [grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md) | 对计划进行高强度访谈，同时沉淀项目语言、`CONTEXT.md` 和 ADR。 |
| [triage](./skills/engineering/triage/SKILL.md) | 在本地 `.codex/agents/` 工作区中推进 issue triage 状态机。 |
| [improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md) | 扫描代码库的架构深化机会，并输出 HTML 报告。 |
| [setup-agent-skills](./skills/engineering/setup-agent-skills/SKILL.md) | 初始化工程类 skill 依赖的本地 `.codex/agents/`、triage 标签和领域文档配置。 |
| [to-issues](./skills/engineering/to-issues/SKILL.md) | 将计划、规格或 PRD 拆成可独立执行的实现 issue。 |
| [to-prd](./skills/engineering/to-prd/SKILL.md) | 将当前对话整理成 PRD，并写入 `.codex/agents/work/`。 |
| [prototype](./skills/engineering/prototype/SKILL.md) | 为状态机、业务逻辑或 UI 方案构建一次性原型。 |

#### 模型可自动调用

| Skill | 作用 |
|---|---|
| [diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md) | 用复现、最小化、假设、插桩、修复、回归测试的闭环诊断问题。 |
| [tdd](./skills/engineering/tdd/SKILL.md) | 使用 red-green-refactor 循环开发功能或修复 bug。 |
| [domain-modeling](./skills/engineering/domain-modeling/SKILL.md) | 建立和修正项目领域语言，维护 `CONTEXT.md` 与 ADR。 |
| [codebase-design](./skills/engineering/codebase-design/SKILL.md) | 提供深模块、小接口、clean seam 和可测试边界的设计词汇。 |
| [implement](./skills/engineering/implement/SKILL.md) | 按既定计划执行实现任务。 |
| [resolving-merge-conflicts](./skills/engineering/resolving-merge-conflicts/SKILL.md) | 解决 merge/rebase 冲突，同时保留两侧意图。 |

### Productivity

生产力类 skill 面向非代码规划、访谈、学习、交接和 skill 写作。

#### 用户显式调用

| Skill | 作用 |
|---|---|
| [grill-me](./skills/productivity/grill-me/SKILL.md) | 对计划或设计进行逐分支访谈，直到关键决策被澄清。 |
| [handoff](./skills/productivity/handoff/SKILL.md) | 将当前对话压缩成交接文档，便于另一个 Agent 或新会话继续。 |
| [teach](./skills/productivity/teach/SKILL.md) | 构建概念、技能、论文深读、仓库课程、科研路线和长线课程学习系统。 |
| [writing-great-skills](./skills/productivity/writing-great-skills/SKILL.md) | 编写和维护可预测 skill 的参考规范。 |

#### 模型可自动调用

| Skill | 作用 |
|---|---|
| [grilling](./skills/productivity/grilling/SKILL.md) | `grill-me` 和 `grill-with-docs` 背后的可复用访谈循环。 |

## Teach

`teach` 是面向长期学习任务的 Learning Course Runner，支持多种学习场景：

- `concept`：单概念学习
- `skill`：技能训练与反馈循环
- `deep-paper`：单/多论文深读、Figure/Table/benchmark 证据链
- `repo-course`：代码仓库 truth map 到学生课程的转换
- `research-route`：科研路线、阅读路径、开放问题和迁移边界
- `long-course`：多阶段课程、manifest、misconception audit 和 final proof loop

核心约束：

- 复杂课程必须先建立 `artifacts/source-matrix.md`，再写学生页。
- 强判断必须分为 `paper_fact`、`lineage_context`、`course_reconstruction`、`engineering_transfer` 或 `unknown`。
- 学生页默认不暴露本地路径、行号、Agent 日志、phase review 或 backstage governance。
- 长线课程必须维护 manifest、误解审计和最终 artifact survival proof。

相关验证脚本：

```bash
python3 skills/productivity/teach/scripts/validate_teaching_workspace.py \
  --skill-root skills/productivity/teach \
  --check-skill-package
```

```bash
python3 skills/productivity/teach/scripts/check_source_matrix.py \
  --matrix skills/productivity/teach/templates/source-matrix.md \
  --template-mode
```

```bash
python3 skills/productivity/teach/scripts/check_manifest.py \
  --manifest skills/productivity/teach/templates/manifest.json \
  --base skills/productivity/teach \
  --template-mode
```

```bash
python3 skills/productivity/teach/scripts/verify_html_artifacts.py \
  --root skills/productivity/teach/templates \
  --template-mode
```

## 项目结构

```text
.
├── .claude-plugin/          # Agent skill plugin manifest
├── .out-of-scope/           # triage 拒绝项和边界记录
├── docs/                    # invocation 规则和 ADR
├── scripts/                 # 安装、列表和验证脚本
└── skills/
    ├── engineering/         # 工程类 skill
    └── productivity/        # 规划、交接、教学和 skill 写作
```

## 维护约束

- 每个正式保留的 skill 必须出现在 `.claude-plugin/plugin.json`、顶层 `README.md` 和对应 bucket README 中。
- 每个 README 中的 skill 名称必须链接到对应 `SKILL.md`。
- `skills/engineering/` 和 `skills/productivity/` 是当前唯一正式 bucket。
- `.codex/` 和 `artifacts/` 用于本地运行输出，默认由 `.gitignore` 忽略。
- 新增或重命名 skill 后，应运行：

```bash
./scripts/list-skills.sh
```

并确认 plugin manifest 与实际 `SKILL.md` 文件一致。

## 验证

常用验证命令：

```bash
./scripts/list-skills.sh
```

```bash
bash scripts/test-install-shape.sh
```

```bash
python3 skills/productivity/teach/scripts/validate_teaching_workspace.py \
  --skill-root skills/productivity/teach \
  --check-skill-package
```

```bash
git diff --check
```

## 许可证

本项目基于 MIT License 分发。版权信息见 [LICENSE](./LICENSE)。
