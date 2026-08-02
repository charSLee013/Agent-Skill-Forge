# Agent Skill Forge

面向工程协作、任务规划、长期学习和知识交接的 Agent Skills 集合。

本项目提供一组可直接安装到 Agent 运行环境中的技能包，覆盖工程开发、计划澄清、任务交接、长期学习、科研论文摄取和 skill 写作。仓库内容保持精简，只包含当前可维护、可验证、可组合使用的 skill 与配套文档。

## 特性

- **工程工作流完整**：覆盖需求澄清、PRD、issue 拆分、实现、调试、跨层证据校验、真实路径验收、架构改进、领域建模和本地 triage。
- **规划与交接能力**：提供 `grill-me`、`grilling`、`grill-with-docs`、`handoff` 和 `prepare-goals`，适合多轮计划、跨会话协作、上下文压缩和长期 Goal 准备。
- **学习系统能力**：把主题、资料和学习目标组合成 HTML 课程与 supporting Markdown。
- **科研摄取能力**：提供 arXiv 查询、论文 source/PDF 获取和 Markdown reference doc 生成工具。
- **精简项目结构**：正式 skill 分为 `engineering`、`productivity` 和 `research` 三类，入口、文档和插件清单保持一致。
- **可复用的课程产物**：提供 course map、lesson、reference、source notes 和结构规划模板。

## 安装

本地安装当前 checkout：

```bash
bash scripts/install.sh
```

远程安装最新 `master`：

```bash
curl -fsSL https://raw.githubusercontent.com/charSLee013/Agent-Skill-Forge/master/scripts/install.sh | bash
```

安装器把每个完整 skill 目录复制到 `~/.agents/skills`。安装后的文件由用户持有，不会自动更新；更新时重新运行安装器。

重新安装会替换本仓库当前提供的同名 skill，其他 skill 目录保持不变。不要同时通过其他渠道安装同名 skill，避免同一入口被重复发现。

### 可选 CTF 包

CTF 包用于授权竞赛、安全研究和教育，不属于本仓库的正式 skill 集合。本地安装核心 skills 与锁定版本的 11 个外部 CTF skills：

```bash
bash scripts/install-with-ctf.sh
```

远程安装：

```bash
curl -fsSL https://raw.githubusercontent.com/charSLee013/Agent-Skill-Forge/master/scripts/install-with-ctf.sh | bash
```

安装器固定使用 `ljagiello/ctf-skills` 的提交 `d6662d26b5ed3caa56f5eaf6eb887964f3747162`，只复制锁文件列出的 skill 目录，不运行上游工具安装器。安装后的文件由用户持有，不会自动更新；重新运行命令会替换本包拥有的同名目录并保留其他 skills。若目标目录已存在但不属于本包，安装器会中止而不是覆盖。

## Skill 清单

### Engineering

工程类 skill 面向代码仓库中的真实开发流程，包括决策地图、规划、拆分、实现、调试、架构和本地 issue 工作区。

#### 如何组合使用

工程类 skill 不是并列菜单，而是一条从“想法”到“可交付改动”的工作流。用户通常只需要显式调用用户类 skill；模型类 skill 会在实现、调试、测试、设计时作为支撑纪律被调用。

```text
第一次接入仓库
  setup-agent-skills
        |
        v
新想法 / 新功能 / 重构方向
  判断需求主干和路线
        |
        +-- 清晰 bounded request -> implement
        |
        +-- 一次会话仍需厘清 -> grill-with-docs -> implement 或 to-prd/to-issues
        |
        +-- 需要运行信号 -> prototype -> handoff -> 回到主线
        |
        +-- 跨会话且有决策迷雾 -> wayfinder -> 路线清晰后选择 to-prd / to-issues / implement
        |
        +-- 路线已清晰的长线改动 -> to-prd -> to-issues -> prepare-goals -> 每个 Goal 独立执行

已有 bug / 性能问题
  diagnosing-bugs -> implement

跨配置 / prompt / tool / permission / runtime 的行为声明
  evidence-first -> 回到当前 task-specific workflow

已有外部请求或待办堆积
  triage -> ready-for-agent -> implement

代码库健康治理
  improve-codebase-architecture -> grill-with-docs -> implement 或 to-prd/to-issues
```

#### 什么时候用哪个

| 你现在的情况 | 首选 skill | 后续组合 |
|---|---|---|
| 需求主干不清 | `grill-with-docs` | 只在目标、范围或验收真的不清楚时澄清。 |
| 第一次在一个仓库使用工程类 skill | `setup-agent-skills` | 建立 `.codex/agents/`、triage 标签和领域文档配置。 |
| 有一个模糊想法、产品需求或重构方向 | `grill-with-docs` | 一次会话能厘清就直接进入后续流程；跨会话且仍有决策迷雾才进入 `wayfinder`。 |
| 规模很大、预计跨多个会话且路线不清 | `wayfinder` | 建立本地决策地图，逐个解决 decision issue；路线清晰后选择 `to-prd`、`to-issues` 或 `implement`。 |
| 需要先验证状态机、业务逻辑或 UI 方案 | `prototype` | 原型结论用 `handoff` 带回主线，再进入 `to-prd` 或 `implement`。 |
| 不熟悉一片代码，需要先看它在系统里的位置 | `zoom-out` | 让 agent 上升一层抽象，按领域语言梳理相关模块和调用方。 |
| 已经讨论清楚，需要沉淀成规格 | `to-prd` | 生成带内联验收证据的 PRD 后用 `to-issues` 拆成可独立执行的 issue。 |
| PRD 或计划已经清楚，需要拆给 agent 执行 | `to-issues` | 每个 issue 开新会话，继承 PRD 的验收条件和证据；未决策问题先回到 `wayfinder`。 |
| 已批准的工作预计持续数小时或数天 | `prepare-goals` | 将现有 PRD、ADR 和 issue 整理成可直接启动的 `/goal`；普通小任务仍直接执行。 |
| 已经有明确 issue 或 PRD，要开始做 | `implement` | 只执行已批准范围和内联证据；明确要求真实路径时联动 `real-path-verification`。 |
| 一个行为声明跨配置、prompt、tool、权限或 runtime | `evidence-first` | 先冻结最小契约并逐层确认因果链，再把结论交还当前工程流程；单层明确检查直接执行。 |
| 困难或不确定的故障 | `diagnosing-bugs` | 先建立根因反馈循环，再修复；不自动创建测试。 |
| 明确的架构、接口或模块深化工作 | `codebase-design` | 只在架构任务中提供设计词汇，不作为普通实现前置。 |
| 术语混乱、领域概念不清、需要 ADR | `domain-modeling` | 通常由 `grill-with-docs` 或架构类流程带起，沉淀 `CONTEXT.md` 和 ADR。 |
| issue、需求、bug 报告堆积，需要筛选 | `triage` | 输出 `ready-for-agent` 后交给 `implement`。 |
| 想主动改善代码库结构 | `improve-codebase-architecture` | 先生成 HTML 架构报告，再选择一个机会进入 `grill-with-docs` 或 `implement`。 |
| merge/rebase 冲突 | `resolving-merge-conflicts` | 专注保留两边意图，解决后跑相关验证。 |

#### 推荐工作流

| 工作流 | 使用顺序 | 适合场景 |
|---|---|---|
| 快速小改 | `implement` | 需求、范围和验收已经清晰，不需要额外访谈。 |
| 标准功能交付 | `setup-agent-skills` -> `to-prd` -> `to-issues` -> `implement` | 路线清晰、多步骤功能、需要可追踪规格和可拆 issue；只有主干仍不清时才先 `grill-with-docs`。 |
| 长期 Goal 执行 | `to-prd` / `to-issues` -> `prepare-goals` -> `/goal` | 范围和验收已批准，但执行预计持续数小时或数天；每个 Goal 保持单一结果和停止条件。 |
| 超大且决策未定的工作 | `setup-agent-skills` -> `wayfinder` -> `to-prd` / `to-issues` / `implement` | 预计跨多个会话，先解决会改变范围、架构、风险或验收的决策，再选择最小交付流程。 |
| 原型驱动决策 | `grill-with-docs` -> `handoff` -> `prototype` -> `handoff` -> `to-prd` 或 `implement` | 讨论无法替代运行验证，例如复杂交互、状态机、算法取舍。 |
| Bug 修复 | `diagnosing-bugs` -> `implement` | 先定位根因；真实路径验收只在已批准验收证据要求时运行。 |
| 请求池治理 | `triage` -> `grill-with-docs` -> `ready-for-agent` -> `implement` | 从原始 issue、反馈、需求池中筛出可执行任务。 |
| 架构治理 | `improve-codebase-architecture` -> `grill-with-docs` -> `to-prd/to-issues` 或 `implement` | 主动降低耦合、补测试边界、改善 Agent 可维护性。 |

#### 用户类和模型类的区别

| 类型 | 谁来调用 | 应该如何理解 |
|---|---|---|
| 用户显式调用 | 由用户点名，例如 `grill-with-docs`、`wayfinder`、`to-prd`、`triage`、`implement` | 这些是工作流入口，会改变任务阶段或产出文档。 |
| 模型可自动调用 | 用户可以点名，模型也可以在明确条件成立时使用 | 这些是当前工作流的支持纪律，例如跨层证据校验、困难诊断、真实路径验收、领域建模、模块设计、冲突解决。 |

如果只记一条规则：**清晰需求直接进入 `implement`；一次会话能厘清的需求进入 `grill-with-docs`；只有跨会话且存在决策迷雾时才进入 `wayfinder`；需要本地工作区时才运行 `setup-agent-skills`。**

#### 用户显式调用

| Skill | 定义性约束与使用路径 |
|---|---|
| [grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md) | 在一次会话内澄清计划主干并记录领域语言和决策；用于目标、范围或验收仍不清时，区别于跨会话决策地图；需可读的仓库上下文，出口是 `implement`、`to-prd` 或 `to-issues`。 |
| [triage](./skills/engineering/triage/SKILL.md) | 推进本地 issue 池的 triage 状态机；用于筛选待办集合，区别于直接实现单个已批准 issue；需先完成本地 workspace 配置，出口是 `ready-for-agent` 或其他终态。 |
| [improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md) | 扫描架构深化机会并生成 HTML 报告；用于显式代码库治理，区别于直接重构；需仓库和领域上下文，出口是选定机会后的 `grill-with-docs` 或 `implement`。 |
| [setup-agent-skills](./skills/engineering/setup-agent-skills/SKILL.md) | 初始化 `.codex/agents/`、triage 标签和领域文档配置；用于仓库首次接入，区别于功能工作；需仓库写权限，出口是其他工程 skill 可用的本地 workspace。 |
| [wayfinder](./skills/engineering/wayfinder/SKILL.md) | 为跨会话且存在决策迷雾的工作建立本地决策地图；区别于一次会话澄清或已清晰的交付计划；需已配置 workspace，出口是路线清晰后的 `to-prd`、`to-issues` 或 `implement`。 |
| [to-issues](./skills/engineering/to-issues/SKILL.md) | 将已批准计划拆成可独立验证的实现 issue；用于路线已清晰时，不负责解决未决策问题；需 PRD、计划或明确规格，出口是逐个 `implement`。 |
| [to-prd](./skills/engineering/to-prd/SKILL.md) | 将已讨论清楚的当前对话整理成 PRD；用于规格沉淀，区别于需求访谈和决策探索；需可确认的范围与验收证据，出口是 `to-issues` 或直接 `implement`。 |
| [prototype](./skills/engineering/prototype/SKILL.md) | 用一次性可运行原型回答状态、逻辑或 UI 决策；用于讨论不足以验证的具体问题，区别于生产实现；需明确问题和停止条件，出口是 `handoff` 后回到主线。 |
| [zoom-out](./skills/engineering/zoom-out/SKILL.md) | 按领域语言梳理陌生模块及调用方；用于实现前定位系统位置，区别于架构重设计；需可读代码库，出口是边界清晰的计划或实现上下文。 |
| [implement](./skills/engineering/implement/SKILL.md) | 执行已批准 PRD 或 issue 并关闭验收条件；用于范围和证据已明确时，区别于发现、访谈和路线规划；需明确工作项，出口是验证过的完成结论。 |

#### 模型可自动调用

| Skill | 定义性约束与使用路径 |
|---|---|
| [evidence-first](./skills/engineering/evidence-first/SKILL.md) | 为跨配置、prompt、tool、权限或 runtime 的请求冻结最小契约并逐层验证声明；区别于困难 bug 诊断和已选定的真实路径验收；需可观察的验收声明，出口是交还当前流程的证据边界与结论。 |
| [diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md) | 用复现、最小化、假设和插桩定位困难或不确定故障；区别于已知路径的机械修复；需可观察的失败信号，出口是可证伪根因和交给 `implement` 的修复边界。 |
| [domain-modeling](./skills/engineering/domain-modeling/SKILL.md) | 建立或修正领域语言并维护 `CONTEXT.md` 与 ADR；用于真实领域决策，区别于被动读取术语；需具体概念冲突或决策，出口是稳定词汇和记录。 |
| [codebase-design](./skills/engineering/codebase-design/SKILL.md) | 为显式模块、接口或架构深化提供设计词汇；区别于普通实现、测试规划和诊断；需明确设计对象，出口是可执行的边界与约束。 |
| [real-path-verification](./skills/engineering/real-path-verification/SKILL.md) | 在真实或生产等价路径上验证已批准验收条件；区别于常规单元或 smoke 检查；需父验收条件明确选择该证据及清理方案，出口是传回 `implement` 的结论。 |
| [resolving-merge-conflicts](./skills/engineering/resolving-merge-conflicts/SKILL.md) | 解决进行中的 merge/rebase 冲突并保留两侧意图；区别于主动重构；需真实冲突状态和双方语义，出口是已验证的冲突解决。 |

### Productivity

生产力类 skill 面向非代码规划、访谈、学习、交接和 skill 写作。

#### 用户显式调用

| Skill | 定义性约束与使用路径 |
|---|---|
| [grill-me](./skills/productivity/grill-me/SKILL.md) | 用少量主干问题明确计划或设计并回填可逆细节；用于通用单会话澄清，区别于写项目文档的 `grill-with-docs`；需一个可陈述目标，出口是可执行计划。 |
| [handoff](./skills/productivity/handoff/SKILL.md) | 将当前对话压缩成交接文档；用于换 Agent 或新会话，区别于重新规划或实现；需当前状态、决策和未完成项，出口是下一会话可直接读取的文档。 |
| [prepare-goals](./skills/productivity/prepare-goals/SKILL.md) | 将已批准的长期工作整理成边界清晰的 Codex Goal launcher；用于预计持续数小时或数天的执行，区别于普通任务和未决规划；需明确结果与验证路径，出口是不自动启动的 `/goal` 指令。 |
| [writing-great-skills](./skills/productivity/writing-great-skills/SKILL.md) | 提供编写和维护可预测 skill 的规范；用于 skill 设计或评审，区别于安装和业务实现；需目标 skill 或行为契约，出口是边界清晰的 skill 文本。 |

#### 模型可自动调用

| Skill | 定义性约束与使用路径 |
|---|---|
| [grilling](./skills/productivity/grilling/SKILL.md) | 为调用方运行高杠杆访谈循环并回填可逆默认；用于存在关键决策时，区别于用户显式工作流入口；需调用方提供目标与边界，出口是确定的决策主干。 |
| [teach](./skills/productivity/teach/SKILL.md) | 构建编辑完整、领域原生视觉驱动的静态 HTML 课程与 supporting Markdown；用于完整学习交付，区别于普通摘要或文档页；需学习目标、读者起点和来源，出口是 Standard 或 Ultra 课程。 |

### Research

科研类 skill 面向论文材料摄取、arXiv 元数据查询和可供后续深读/教学使用的 Markdown reference doc 生成。

#### 模型可自动调用

| Skill | 定义性约束与使用路径 |
|---|---|
| [arxiv-lookup](./skills/research/arxiv-lookup/SKILL.md) | 查询 arXiv 元数据、ID 和 journal DOI；用于定位论文身份，区别于下载或转换正文；需查询词或已有 ID 及网络，出口是交给 builder 或研究流程的稳定标识。 |
| [arxiv-doc-builder](./skills/research/arxiv-doc-builder/SKILL.md) | 获取 arXiv source/PDF 并生成 Markdown reference doc；用于论文材料摄取，区别于元数据查找和课程编排；需 arXiv ID、网络及转换工具，出口是供深读或 `teach` 使用的文档。 |

推荐组合：

```text
找论文 ID / DOI
  arxiv-lookup
        |
        v
下载 source/PDF 并转 Markdown
  arxiv-doc-builder
        |
        v
深读、课程或研究材料整理
  teach
```

## Teach

`teach` 是一个单一的 `course` skill：根据学习目标、读者起点、领域证据和目标能力，构建经过编辑、具有领域原生视觉系统且可静态发布的 HTML 课程与 supporting Markdown。

Standard 与 Ultra 共享编辑、视觉、交互、可访问性和内容保真的专业底线。Ultra 面向顶级、全面、研究级或高知识密度课程，通过用户确认后增加多 Agent 阶段编排、完整知识图谱、领域原生 Capstone、Tracer 校准和独立审阅。

课程路径覆盖先修补桥、机制重建、worked examples、故障诊断、领域原生练习、分级反馈、Capstone 和专家标准审阅。视觉系统从领域对象、证据类型和学习动作推导；动画只用于解释序列、因果、状态或同步关系，并保留静态与 reduced-motion 等价物。

Teach 按 Publication、Learning, Editorial and Fidelity、Visual System、Interaction and Motion 的顺序审阅最终产物。Supporting Markdown 记录来源、证据角色、教学用途、公式或数据保真和适用范围。

多轮学习可以启用 `MISSION.md`、`RESOURCES.md`、`GLOSSARY.md` 和 `learning-records/`，这些文件记录学习状态，HTML 与 Markdown 仍然是课程交付物。

## 项目结构

```text
.
├── .claude-plugin/          # Agent skill plugin manifest
├── .out-of-scope/           # triage 拒绝项和边界记录
├── docs/                    # invocation 规则和 ADR
├── scripts/                 # 安装、列表和验证脚本
└── skills/
    ├── engineering/         # 工程类 skill
    ├── productivity/        # 规划、交接、教学和 skill 写作
    └── research/            # arXiv 查询和论文材料摄取
```

## 维护约束

- 每个正式保留的 skill 必须具有 `SKILL.md` 和 `agents/openai.yaml`，并出现在 `.claude-plugin/plugin.json`、顶层 `README.md` 和对应 bucket README 中。
- 每个 README 中的 skill 名称必须链接到对应 `SKILL.md`。
- `skills/engineering/`、`skills/productivity/` 和 `skills/research/` 是当前正式 bucket。
- `.codex/` 和 `artifacts/` 用于本地运行输出，默认由 `.gitignore` 忽略。
- 新增或重命名 skill 后，应运行：

```bash
./scripts/list-skills.sh
```

并运行注册表校验，确认 plugin manifest、README、Codex sidecar 与实际 `SKILL.md` 文件一致。

## 验证

常用验证命令：

```bash
./scripts/list-skills.sh
```

```bash
bash scripts/test-skill-registry.sh
```

```bash
bash scripts/test-install-shape.sh
```

```bash
bash scripts/test-ctf-bundle-install.sh
```

```bash
git diff --check
```

## 许可证

本项目基于 MIT License 分发。版权信息见 [LICENSE](./LICENSE)。
