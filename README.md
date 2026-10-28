# Agent Skill Forge

本仓库收录 40 个 Agent 技能，涵盖代码工作、需求澄清、任务规划、写作、交接和论文学习。

明确的代码修改直接使用 `implement`；只有重要选择尚未确定时，才使用 `grilling`。需要规格、任务拆分或跨会话决策记录时，再使用相应技能。模型可以根据请求选择技能，但只读请求仍不能变成代码修改。

## 安装

安装当前 checkout：

```bash
bash scripts/install.sh
```

远程安装最新 `master`：

```bash
curl -fsSL https://raw.githubusercontent.com/charSLee013/Agent-Skill-Forge/master/scripts/install.sh | bash
```

安装器把完整技能目录复制到 `~/.agents/skills`，不安装技能依赖的运行工具，也不向项目添加 hooks。重新运行会覆盖同名目录，其中的个人修改不会保留。安装后的文件不会自动更新；不要通过多个渠道安装同名技能。

### 重新安装时的清理

复制并检查完当前技能后，安装器会删除 `grill-me`、`grill-with-docs`、`evidence-first`、`ponytail` 和 `resolving-merge-conflicts`。旧目录即使经过修改也会删除，不留备份或别名。安装器不会删除既非当前技能、也非上述旧入口的其他目录。

需求澄清由 `grilling` 处理；`evidence-first` 和 `ponytail` 的适用原则在 `implement` 及其证据参考中。合并冲突由普通代码工作处理。持续实现模式及其开启、关闭口令不再提供。曾手动配置旧 hooks 的项目需要自行移除相关注册；安装器不会扫描其他项目。

## 从一个任务开始

| 你要做的事 | 可以直接这样说 | 工作如何推进 |
|---|---|---|
| 明确的小改动 | “修复空输入时的异常，并验证已有行为。” | `implement` 直接处理，不要求先写 PRD 或初始化工作区。 |
| 需要澄清后执行 | “帮我确定这个缓存方案，关键问题问我，确定后实现。” | `grilling` 只解决重要选择，然后继续已授权的实现。 |
| 需要规划产物 | “把刚才确定的需求写成 PRD，先不要实现。” | `to-prd` 交付规格后结束。需要拆分时可直接请求 `to-issues`；跨会话还有未决选择时使用 `wayfinder`。 |

请求“检查这个配置是否生效”时，只检查并报告结果；请求“拆好任务并完成”时，可以继续逐项实现。任务耗时长，本身不是创建决策地图的理由。

日常回答也用清楚的语言说明结果，不要求用户先记住技能名称。需要重新解释上一条回复时，可以手动调用 `wait-what`。

普通代码修改不要求 TDD、测试先行、PRD、代码审查或提交。验证随变更风险调整；SHA-256 可以核对文件完整性，不能证明程序按要求运行。

### 本地规划文件

需要保存 PRD、任务或决策地图时，技能才会在使用项目的 `.codex/agents/work/<feature>/` 下创建相应文件。有现成配置就沿用；没有则使用随技能提供的约定。Git 项目通过本地 exclude 排除这些私人文件，不自动改写项目 Agent 指令。

如果运行环境限制写入 `.git` 或 `.codex`，需要通过该环境的正常授权机制开放路径；运行 setup 不能代替权限授权。

只有明确要求定制配置或迁移旧决策布局时，才使用 `setup-agent-skills`。它会先展示拟对 Agent 指令文件作出的完整修改；普通规划不会自动调用它。

[调用规则](./docs/invocation.md) 区分技能是否可被模型选用，以及当前任务允许它做什么。安装后各技能位于同一层目录，跨技能参考不能依赖仓库中的分类路径。

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
| [course-correction](./skills/engineering/course-correction/SKILL.md) | 按意图选用 | 发现范围漂移或代理失控时立即止损、清理代理产物并如实报告。 |
| [real-path-verification](./skills/engineering/real-path-verification/SKILL.md) | 按意图选用 | 通过已授权的实际运行路径核实明确的验收条件。 |
| [domain-modeling](./skills/engineering/domain-modeling/SKILL.md) | 按意图选用 | 处理实际的领域术语或架构决策，按授权维护已有记录。 |
| [codebase-design](./skills/engineering/codebase-design/SKILL.md) | 按意图选用 | 为明确的接口或架构设计提供模块设计方法。 |
| [code-review](./skills/engineering/code-review/SKILL.md) | 按意图选用 | 只读审查实际变更与需求、失败路径和维护风险。 |
| [error-handling](./skills/engineering/error-handling/SKILL.md) | 按意图选用 | 判断失败后的状态、恢复条件和可见结果。 |
| [test-reliability](./skills/engineering/test-reliability/SKILL.md) | 按意图选用 | 在异步或共享资源测试有风险时核对隔离与清理。 |
| [pr](./skills/engineering/pr/SKILL.md) | 按意图选用 | 用实际变更和证据撰写已请求的 PR 文案。 |
| [triage](./skills/engineering/triage/SKILL.md) | 手动 | 筛选本地待办并更新分诊状态，保留独立的实现完成状态。 |
| [improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md) | 手动 | 生成架构改进报告，再按用户授权探索或实现选定方案。 |
| [find-simplifications](./skills/engineering/find-simplifications/SKILL.md) | 手动 | 只读寻找有证据支持的删除、合并或替换机会。 |
| [setup-agent-skills](./skills/engineering/setup-agent-skills/SKILL.md) | 手动 | 显式定制工作区、领域文档配置或迁移旧决策布局。 |
| [issues-to-execution-brief](./skills/engineering/issues-to-execution-brief/SKILL.md) | 手动 | 将选定的可执行任务整理成供新会话使用的执行简报。 |
| [prototype](./skills/engineering/prototype/SKILL.md) | 手动 | 用可运行的临时原型回答具体逻辑或界面问题。 |
| [zoom-out](./skills/engineering/zoom-out/SKILL.md) | 手动 | 查看陌生代码区域及其调用方在系统中的位置。 |
| [implement-spec](./skills/engineering/implement-spec/SKILL.md) | 手动 | 按依赖顺序交付明确选定的整份规格。 |
| [retro](./skills/engineering/retro/SKILL.md) | 手动 | 从已发生的执行问题中提出有证据的环境改进。 |
| [wizard](./skills/engineering/wizard/SKILL.md) | 手动 | 为确需人工完成的操作生成受限引导脚本。 |

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
| [research](./skills/research/research/SKILL.md) | 按意图选用 | 按范围调查来源并默认在对话中交付结果。 |
| [research-loop](./skills/research/research-loop/SKILL.md) | 手动 | 为明确的改进目标设计并运行可审计的研究循环；包含裁判、变异面、账本与退化诊断。 |
| [antidetect-browser-lab](./skills/research/antidetect-browser-lab/SKILL.md) | 手动 | 安装或操作用户自有的 Donut/Wayfern 浏览器 profile；使用显式代理与本地 CDP。 |

## 课程与论文工具

`teach` 生成静态 HTML 课程和配套 Markdown，包含能力目标、例题、练习、反馈和成果评价。默认使用 Standard；只有用户接受额外的研究与独立审阅工作时才使用 Ultra。模板和交互组件随技能安装。

阅读论文时，可用 `arxiv-lookup` 查找论文，再用 `arxiv-doc-builder` 转为 Markdown；需要课程时再用 `teach`。查询和转换需要网络及相应工具，安装技能不会安装 `uv`、`pandoc` 或 Python 依赖。PDF 回退转换后还要检查排版、公式和双栏内容，命令成功不代表文档完整。

## 可选 CTF 包

可选 CTF 包面向授权竞赛、安全研究和教育，所含技能不计入上述 40 个：

```bash
bash scripts/install-with-ctf.sh
```

远程安装：

```bash
curl -fsSL https://raw.githubusercontent.com/charSLee013/Agent-Skill-Forge/master/scripts/install-with-ctf.sh | bash
```

CTF 包从 `ljagiello/ctf-skills` 的提交 `d6662d26b5ed3caa56f5eaf6eb887964f3747162` 安装 11 个目录，不运行上游工具安装器。核心技能仍按上文规则覆盖与清理；外部 CTF 目录有独立的归属检查和失败回滚。

## 来源与许可

本项目使用 [MIT License](./LICENSE)。借鉴上游内容的技能在各自目录保留适用的许可：

- 最小正确实现原则来自 [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)，授权位于 [implement/LICENSE](./skills/engineering/implement/LICENSE)。
- `humanizer` 保留上游 2.11.2，固定于 [blader/humanizer 的 e2e92e7](https://github.com/blader/humanizer/commit/e2e92e7b4b8229253ed5c8e81dc65463fdeddda5)，见 [LICENSE](./skills/productivity/humanizer/LICENSE)。
- `find-simplifications`、`prose-standard`、`trim-cot-leakage` 和 `doc-standards` 的方法源自 [deepseek-ai/deepseek-harness 的 b150a551](https://github.com/deepseek-ai/deepseek-harness/commit/b150a551b8d465e31e418e1b2eaf5e79bbb7d28e)，各技能目录保留上游许可。
- `error-handling`、`test-reliability`、`code-review`、`writing-great-skills` 和文档记录治理参照 [DeepSeek Harness 的 22ddee3](https://github.com/deepseek-ai/deepseek-harness/commit/22ddee3792402c3e70ec5f86a63c3e3e895a2f60)。这些技能不依赖 DSH 框架、hooks、Agent Notes 体系或文档站。
- `implement-spec`、`code-review`、`pr`、`retro`、`research`、`wizard` 参考 [mattpocock/skills](https://github.com/mattpocock/skills) 的对应技能，但不设强制 setup，也不自动提交或交给子代理实现。

## 验证

修改技能说明或文档后，直接审读改动及相关引用，核对事实、前后含义和适用范围，并用具体任务检查指令是否合理。新增、删除或重命名技能时，同时检查 README、调用元数据和插件登记。

安装逻辑有变更时，运行 `bash scripts/test-install-shape.sh`；涉及 CTF 包安装时，运行 `bash scripts/test-ctf-bundle-install.sh`。它们检查安装行为。`git diff --check` 只检查空白错误。文字质量靠审读判断，模型执行效果需要实际任务验证。
