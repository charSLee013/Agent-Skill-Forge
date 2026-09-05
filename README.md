# Agent Skill Forge

用于需求澄清、代码交付、任务规划、写作、交接和论文学习的 30 个 Agent 技能。

日常工作主要使用 `grilling` 和 `implement`。模型根据请求选择适用技能；需要规格、任务拆分或跨会话决策记录时，再使用对应工具。技能切换沿用当前授权，单纯的审查或讨论不会自行变成代码修改。

## 安装

安装当前 checkout：

```bash
bash scripts/install.sh
```

远程安装最新 `master`：

```bash
curl -fsSL https://raw.githubusercontent.com/charSLee013/Agent-Skill-Forge/master/scripts/install.sh | bash
```

安装器将全部完整技能目录复制到 `~/.agents/skills`，不安装运行工具或项目 hooks。重新运行会替换当前提供的同名技能；文件不会自动更新。避免通过多个渠道安装同名入口。

### 升级到 2.0

`grill-me`、`grill-with-docs` 已合并到 `grilling`；`evidence-first`、`ponytail` 的必要原则已并入 `implement` 及其证据参考。新技能安装验证成功后，安装器会直接删除目标目录下这四个旧入口，包含用户修改过的同名目录，不保留备份或别名。其他技能保留。

持续实现模式、开启和关闭口令及项目 hooks 已退役。普通安装器从未向其他项目安装 hooks；曾自行复制适配器的项目需要移除自己配置的旧注册，安装器不扫描其他项目。

## 从一个任务开始

| 你要做的事 | 可以直接这样说 | 工作如何推进 |
|---|---|---|
| 明确的小改动 | “修复空输入时的异常，并验证已有行为。” | `implement` 直接处理，不要求先写 PRD 或初始化工作区。 |
| 需要澄清后执行 | “帮我确定这个缓存方案，关键问题问我，确定后实现。” | `grilling` 只解决重要选择，然后继续已授权的实现。 |
| 需要规划产物 | “把刚才确定的需求写成 PRD，先不要实现。” | `to-prd` 交付规格后结束。需要拆分时可直接请求 `to-issues`；跨会话还有未决选择时使用 `wayfinder`。 |

请求“检查这个配置是否生效”只产生检查结论。请求“拆好任务并完成”可以继续逐项实现。耗时长不代表需要建决策地图；已经明确的任务不必走完所有规划工具。

`wait-what` 保留为手动入口，用你的语言重新解释上一条回复。日常回复也以连贯、易理解的表达为默认，不要求用户熟悉工作流术语。

### 本地规划文件

规格、任务和决策地图位于使用项目的 `.codex/agents/work/<feature>/`。已有配置优先；缺少配置时使用随技能提供的默认约定，仅创建当前任务需要的文件。Git 项目通过本地 exclude 保持这些文件私有，不自动改写项目 Agent 指令。

部分运行环境会保护 `.git` 或 `.codex`。写入受限时需通过该环境的正常授权机制开放所需路径；运行 setup 不能替代权限授权。

`setup-agent-skills` 是显式定制配置或迁移旧决策布局的可选工具。它会展示对 Agent 指令文件的完整改动草稿，因此普通规划不会自动调用它。

技能的发现规则与动作授权分别说明在 [docs/invocation.md](./docs/invocation.md)。共享参考按技能位置查找，既支持仓库分类布局，也支持安装后的同层布局。

## 技能清单

“按意图选用”表示模型或用户可以调用，具体操作仍须符合当前任务授权。“手动”表示用户需要明确选择该技能。

### Engineering

| 技能 | 调用 | 用途 |
|---|---|---|
| [implement](./skills/engineering/implement/SKILL.md) | 按意图选用 | 完成明确的代码修改、修复或重新设计；直接接受自然语言任务。 |
| [to-prd](./skills/engineering/to-prd/SKILL.md) | 按意图选用 | 将已有共识写成规格；仅在任务需要规格时使用。 |
| [to-issues](./skills/engineering/to-issues/SKILL.md) | 按意图选用 | 将清楚的计划拆成可独立验证的任务；不要求先有 PRD。 |
| [wayfinder](./skills/engineering/wayfinder/SKILL.md) | 按意图选用 | 保存跨会话尚未解决的决策及调查结果；耗时长本身不触发。 |
| [diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md) | 按意图选用 | 调查困难或不确定的故障；只诊断的请求保持只读。 |
| [real-path-verification](./skills/engineering/real-path-verification/SKILL.md) | 按意图选用 | 通过已授权的实际运行路径核实明确的验收条件。 |
| [domain-modeling](./skills/engineering/domain-modeling/SKILL.md) | 按意图选用 | 处理实际的领域术语或架构决策，按授权维护已有记录。 |
| [codebase-design](./skills/engineering/codebase-design/SKILL.md) | 按意图选用 | 为明确的接口或架构设计提供模块设计方法。 |
| [resolving-merge-conflicts](./skills/engineering/resolving-merge-conflicts/SKILL.md) | 按意图选用 | 处理已经发生的 merge 或 rebase 冲突。 |
| [triage](./skills/engineering/triage/SKILL.md) | 手动 | 筛选本地待办并更新分诊状态，保留独立的实现完成状态。 |
| [improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md) | 手动 | 生成架构改进报告，再按用户授权探索或实现选定方案。 |
| [find-simplifications](./skills/engineering/find-simplifications/SKILL.md) | 手动 | 只读寻找有证据支持的删除、合并或替换机会。 |
| [setup-agent-skills](./skills/engineering/setup-agent-skills/SKILL.md) | 手动 | 显式定制工作区、领域文档配置或迁移旧决策布局。 |
| [issues-to-execution-brief](./skills/engineering/issues-to-execution-brief/SKILL.md) | 手动 | 将选定的可执行任务整理成供新会话使用的执行简报。 |
| [prototype](./skills/engineering/prototype/SKILL.md) | 手动 | 用可运行的临时原型回答具体逻辑或界面问题。 |
| [zoom-out](./skills/engineering/zoom-out/SKILL.md) | 手动 | 查看陌生代码区域及其调用方在系统中的位置。 |

### Productivity

| 技能 | 调用 | 用途 |
|---|---|---|
| [grilling](./skills/productivity/grilling/SKILL.md) | 按意图选用 | 澄清目标、重要选择和约束，再继续用户已授权的工作。 |
| [humanizer](./skills/productivity/humanizer/SKILL.md) | 按意图选用 | 重写已有文字中的 AI 写作模式，保留事实、引用和原作者语气。 |
| [teach](./skills/productivity/teach/SKILL.md) | 按意图选用 | 制作完整的静态 HTML 课程及配套 Markdown。 |
| [wait-what](./skills/productivity/wait-what/SKILL.md) | 手动 | 用用户的语言重新解释上一条回复，只影响这一次回复。 |
| [handoff](./skills/productivity/handoff/SKILL.md) | 手动 | 将当前状态和未完成事项整理成交接文档。 |
| [to-questionnaire](./skills/productivity/to-questionnaire/SKILL.md) | 手动 | 为一位知情者编写用于补齐信息的问卷。 |
| [i-have-adhd](./skills/productivity/i-have-adhd/SKILL.md) | 手动 | 手动开启行动优先、降低启动阻力的会话表达模式。 |
| [prepare-goals](./skills/productivity/prepare-goals/SKILL.md) | 手动 | 将已明确的长时间工作整理为 Goal 启动指令。 |
| [prose-standard](./skills/productivity/prose-standard/SKILL.md) | 手动 | 检查或编辑技术文字，保留行为、条件和失败契约。 |
| [trim-cot-leakage](./skills/productivity/trim-cot-leakage/SKILL.md) | 手动 | 清理依赖设计会话、草稿或评审背景才能理解的文字残留。 |
| [doc-standards](./skills/productivity/doc-standards/SKILL.md) | 手动 | 审查文档位置、归属及其与实际行为的一致性。 |
| [writing-great-skills](./skills/productivity/writing-great-skills/SKILL.md) | 手动 | 编写或维护职责清楚、调用可预测的技能与 Agent 文档。 |

### Research

| 技能 | 调用 | 用途 |
|---|---|---|
| [arxiv-lookup](./skills/research/arxiv-lookup/SKILL.md) | 按意图选用 | 查询 arXiv 论文身份、元数据和期刊 DOI。 |
| [arxiv-doc-builder](./skills/research/arxiv-doc-builder/SKILL.md) | 按意图选用 | 获取论文 source/PDF 并转成供阅读使用的 Markdown。 |

## 课程与论文工具

`teach` 交付静态 HTML 课程和配套 Markdown，包含能力目标、例题、练习、反馈及课程成果评价。Standard 为默认；用户接受额外研究与独立审阅工作后才启用 Ultra。模板和交互组件随技能提供。

论文流程可按需要组合 `arxiv-lookup`、`arxiv-doc-builder` 和 `teach`。查询和转换需要网络及相应工具，安装技能本身不会安装 `uv`、`pandoc` 或 Python 依赖。PDF 回退的排版、公式和双栏转换结果需要检查，不能仅凭命令成功认定内容完整。

## 可选 CTF 包

CTF 包面向授权竞赛、安全研究和教育，不计入本仓库的 30 个技能：

```bash
bash scripts/install-with-ctf.sh
```

远程安装：

```bash
curl -fsSL https://raw.githubusercontent.com/charSLee013/Agent-Skill-Forge/master/scripts/install-with-ctf.sh | bash
```

锁定 `ljagiello/ctf-skills` 提交 `d6662d26b5ed3caa56f5eaf6eb887964f3747162` 的 11 个目录，不运行上游工具安装器。核心技能沿用上述升级清理逻辑；外部 CTF 目录保留已有归属检查和失败回滚。

## 来源与许可

本项目使用 [MIT License](./LICENSE)。继承内容的许可随相应技能保留：

- 最小正确实现原则来自 [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)，授权位于 [implement/LICENSE](./skills/engineering/implement/LICENSE)。
- `humanizer` 保留上游 2.11.2，固定于 [blader/humanizer 的 e2e92e7](https://github.com/blader/humanizer/commit/e2e92e7b4b8229253ed5c8e81dc65463fdeddda5)，见 [LICENSE](./skills/productivity/humanizer/LICENSE)。
- `find-simplifications`、`prose-standard`、`trim-cot-leakage` 和 `doc-standards` 的方法源自 [deepseek-ai/deepseek-harness 的 b150a551](https://github.com/deepseek-ai/deepseek-harness/commit/b150a551b8d465e31e418e1b2eaf5e79bbb7d28e)，各技能目录保留上游许可。

## 验证

```bash
./scripts/list-skills.sh
bash scripts/test-skill-registry.sh
bash scripts/test-install-shape.sh
bash scripts/test-ctf-bundle-install.sh
git diff --check
```

这些检查验证发布清单和安装行为，不代表实际任务中的模型行为已经得到验证。
