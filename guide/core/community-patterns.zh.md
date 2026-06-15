---
title: "Community Patterns & Reference"
description: "Community-coined patterns, AI engineering concepts, workflow terms, and Claude Code configuration reference"
tags: [reference, community, patterns, ai-engineering]
---

# 社区模式与参考

Claude Code 社区模式、工作流术语和 AI 工程词汇的快速参考。标准 CS/DevOps 术语（JWT、CI/CD、REST）不在此列；这些请另行查阅。

**格式**：术语 | 定义 | 类别 | 子类别

---

| 术语 | 定义 | 类别 | 子类别 |
|------|-----------|----------|-------------|
| ! (shell prefix) | 用于直接运行 shell 命令而无需 Claude 介入的前缀，例如 `! git status`。输出会落入对话中。 | Claude Code | 交互 |
| @ (file reference) | 在提示词中引用特定文件的语法，例如 `@src/auth.tsx`。Claude 会立即将该文件加载进上下文。 | Claude Code | 交互 |
| .claude/ folder | 项目级目录，包含 agents、skills、commands、hooks、rules 和 settings。按约定 `settings.local.json` 会被 gitignore。 | Claude Code | 配置 |
| .mcp.json | 项目级的 MCP server 配置文件，会提交到仓库中，使整个团队共享相同的 server 设置。 | Claude Code | 配置 |
| /clear | 完全重置会话的 slash command，丢弃所有对话历史。上下文降至 0%。 | Claude Code | 命令 |
| /compact | 通过总结此前的对话来压缩会话上下文的 slash command，在不丢失状态的情况下释放上下文余量。 | Claude Code | 命令 |
| 150K ceiling | 实际有效的上下文上限，即便名义窗口更大，超过此处输出质量也会下降。参见 [context-engineering.md](./context-engineering.md)。 | 架构 | 上下文 |
| ACE pipeline | Assemble、Check、Execute：跨会话进行有意识上下文管理的三阶段配置持久化循环。与 arXiv:2510.04618（同一首字母缩写，但指推理时上下文演化，概念不同）有别。ACE-v2 增加了信号分类法、基于 PR 的循环闭合以及剔除机制。参见 [context-engineering.md §§10-14](./context-engineering.md#10-signal-taxonomy-and-causal-attribution)。 | AI 工程 | 上下文 |
| Act Mode | 正常执行模式，Claude 可以读取、写入和运行命令。与 Plan Mode 相对。 | Claude Code | 模式 |
| Adaptive thinking | Opus 4.6+ 特性：根据检测到的任务复杂度动态调整推理深度，无需手动配置。 | 模型 | 思考 |
| Agent | 在 markdown 文件中定义的专用 AI 人格，带有角色、工具列表和行为指令。存放于 `.claude/agents/`。 | Claude Code | 可扩展性 |
| Agent teams | 实验性特性（v2.1.32+），可在单个 Claude Code 会话内实现多 agent 协调与消息传递。 | Claude Code | 多 Agent |
| Agentic coding | 一种开发风格，AI agent 在每一步几乎无需人工介入的情况下自主执行多步任务。 | AI 工程 | 范式 |
| AI traceability | 用于记录和披露代码、提交及内容中 AI 参与情况的实践（git trailer、PR 标签、审计日志）。参见 [ops/ai-traceability.md](../ops/ai-traceability.md)。 | 运维 | 合规 |
| allowedTools | 提供细粒度工具权限控制的设置键：可按单个工具或参数模式进行允许或拒绝。 | Claude Code | 配置 |
| Annotation cycle | Boris Tane 的工作流模式：在 Claude 执行之前，给自定义 markdown 计划标注实现备注，从而形成一份持续演进的规格说明。 | 工作流 | 规划 |
| Anti-hallucination protocol | 要求 Claude 在将主张陈述为事实之前，先对照实际代码或文档进行核实的明确指令。 | AI 工程 | 安全 |
| Artifact Paradox | Anthropic 研究发现（AI Fluency Index，2026）：产出 AI 产物的用户更不倾向于质疑其背后的推理。 | AI 工程 | 研究 |
| Auto-accept Mode | 一种权限模式（`acceptEdits`），自动批准文件编辑，但仍会对 shell 命令进行提示。是受信任会话的良好折中方案。 | Claude Code | 权限 |
| Auto-compaction | 内置机制，自动压缩会话上下文（VS Code 扩展中约 75% 阈值，CLI 中约 95%）。除非先使用 `/compact`，否则会被静默触发。 | 架构 | 上下文 |
| Auto-memories | 一项特性（v2.1.32+），Claude 跨会话将学到的项目上下文自动存入持久化的 memory 文件。 | Claude Code | 记忆 |
| autoApproveTools | 列出无需交互式提示即可自动批准的工具的设置数组。比权限模式更细粒度。 | Claude Code | 配置 |
| awesome-claude-code | 社区精选的 Claude Code 资源、工具和示例清单，在 GitHub 上拥有 20K+ stars。 | 生态 | 社区 |
| BMAD | Business-driven, Methodical AI Development：面向 agentic AI 项目的结构化规划框架（社区方法论）。 | 方法论 | 规划 |
| Boris Cherny pattern | 水平扩展方法：并行运行多个 Claude Code 实例，每个实例在一个 git worktree 上，然后合并。以 Boris Cherny 命名，他是 Claude Code 的创造者，也是 Anthropic 的 Claude Code 负责人。 | 工作流 | 多 Agent |
| Bypass Permissions Mode | 通过 `--dangerously-skip-permissions` 实现的最大自主模式：自动批准所有工具。仅可在隔离/沙箱环境中使用。 | Claude Code | 权限 |
| Capability Uplift | 一种 skill 类型，教会 Claude 它本身不具备的新能力，而非强制某种风格偏好。 | Claude Code | Skills |
| ccusage | 社区 CLI 工具，用于跟踪 Claude Code 的 token 消耗、每会话成本以及按模型的细分。 | 生态 | 工具 |
| Chain of Verification (CoVe) | 独立验证者模式：由第二个 agent 重新核查第一个 agent 的输出，以防止确认偏误。arXiv:2309.11495。 | 工作流 | 验证 |
| Checkpoint | 一种已保存的会话状态，可通过 Esc x2 再 /rewind 恢复。会在风险操作之前自动创建。 | Claude Code | 会话 |
| Claude Haiku 4.5 | Anthropic 最快且最便宜的模型。最适合高吞吐量任务、简单查询以及对成本敏感的 CI 工作流。 | 模型 | 档位 |
| Claude Opus 4.8 | Anthropic 当前的旗舰 Opus 模型。最适合深度推理、架构决策和复杂的多步分析。 | 模型 | 档位 |
| Claude Fable 5 | Mythos 级模型，超越此前任何已正式发布（GA）的 Anthropic 模型。规格参见 anthropic.com/pricing。 | 模型 | 档位 |
| Claude Sonnet 4.6 | Anthropic 均衡的默认模型。在日常开发工作中兼具速度与能力的最佳组合。 | 模型 | 档位 |
| CLAUDE.md | 会话开始时自动加载的持久化 memory 文件。包含项目规则、约定和上下文。是 Claude Code 配置的基石。 | Claude Code | 记忆 |
| Co-Authored-By | Git trailer 约定（`Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`），用于标注 AI 协助的提交。 | 运维 | 署名 |
| Comprehension debt | AI 产出的代码与开发者对其实际作用及原因的真实理解之间不断扩大的差距。 | AI 工程 | 风险 |
| Config hierarchy | CLAUDE.md 的三层优先级：Local（`.claude/`，被 gitignore）> Project（已提交）> Global（`~/.claude/CLAUDE.md`）。越具体的总是优先于越通用的。 | Claude Code | 配置 |
| Constitutional AI | Anthropic 的价值框架（依据已发布的系统提示词），定义 Claude 的优先级顺序：安全 > 伦理 > Anthropic 原则 > 用户效用。 | AI 工程 | 框架 |
| Context budget | 有限的 token 配额，必须在单个会话中分配给指令、代码、对话历史和工具结果。 | AI 工程 | 上下文 |
| Context engineering | 有意识地设计进入 AI 模型上下文窗口内容的学科，以最大化输出质量。参见 [context-engineering.md](./context-engineering.md)。 | AI 工程 | 上下文 |
| Context maturity model | 衡量团队上下文工程实践演进程度的框架，从临时性提示词到可度量的流水线。 | AI 工程 | 上下文 |
| Context packing | 密集编码信息（结构化 markdown、符号、表格）的技术，以最大化每个 token 的有用信号。 | AI 工程 | 上下文 |
| Context rot | 在长时间运行的会话中，随着相关上下文被挤出或淹没，Claude 情境感知逐步退化的现象。 | AI 工程 | 上下文 |
| Context triage | 关于哪些信息值得预先放入上下文、哪些通过工具按需加载的刻意决策。 | AI 工程 | 上下文 |
| Context window | Claude 在单个会话中可处理的文本总量（以 token 计）。Claude Sonnet 4.6：200K；扩展 API：1M。 | 模型 | 容量 |
| Ctrl+B | 用于将正在运行的任务转入后台的键盘快捷键，使其在你于会话中继续其他工作时保持存活。 | Claude Code | 快捷键 |
| dangerouslyDisableSandbox | 绕过 Claude Code 原生 OS 级沙箱的标志。只应在已隔离的环境中使用。 | 安全 | 配置 |
| Default Mode | 基础权限模式，对所有文件编辑、shell 命令和提交都要求用户明确批准。 | Claude Code | 权限 |
| Desloppify | 社区工具（[@peteromaller](https://github.com/peteromaller)，2026 年 2 月），将一个工作流 skill 安装到 Claude Code 中，并运行扫描-修复-评分循环以提升代码质量。[github.com/peteromaller/desloppify](https://github.com/peteromaller/desloppify) | 生态 | 工具 |
| Diff review | 在接受或拒绝之前阅读 Claude 提议的文件变更的实践。五条黄金法则之一。 | Claude Code | 工作流 |
| disallowedTools | 用于在会话中或全局阻止特定工具被调用的设置键。 | Claude Code | 配置 |
| Docker sandbox | 基于容器的隔离，用于在严格的资源和文件系统限制下运行 Claude Code。参见 [security/sandbox-isolation.md](../security/sandbox-isolation.md)。 | 安全 | 沙箱 |
| Don't Ask Mode | 一种权限模式（`dontAsk`），对不在预批准列表中的工具静默拒绝，不进行提示。 | Claude Code | 权限 |
| Dual-instance planning | Jon Williams 提出的模式：一个 Claude 实例创建详细计划，另一个独立实例执行它，从而防止上下文污染。 | 工作流 | 规划 |
| Encoded Preference | 一种 skill 类型，强制执行 Claude 默认不会应用的特定约定、风格选择或约束。 | Claude Code | Skills |
| Enterprise AI governance | 面向 AI 工具使用的组织级策略：使用章程、MCP server 注册表、护栏分级和审计追踪。参见 [security/enterprise-governance.md](../security/enterprise-governance.md)。 | 安全 | 企业 |
| Eval harness | 用于系统化衡量 agent 行为、输出质量和 skill 有效性是否符合既定标准的测试框架。 | 方法论 | 测试 |
| Event-driven agents | 一种模式，外部事件（Linear 工单、GitHub PR、Jira webhook）自动触发 Claude Code agent 工作流。 | 工作流 | 架构 |
| Extended thinking | 一种模型特性，通过在可见响应之前处理专门的「thinking token」来实现更深入的推理。用 `--thinking` 激活。 | 模型 | 思考 |
| Fast Mode | 一种模式（v2.1.36+），在相同底层模型上以 2.5 倍速度运行，token 成本为 6 倍。用 `/fast` 切换。 | Claude Code | 模式 |
| FIRE framework | Find、Isolate、Remediate、Evaluate：一套用于配合 Claude Code 进行事件响应的 DevOps/SRE 故障排查方法论。参见 [ops/devops-sre.md](../ops/devops-sre.md)。 | 方法论 | 运维 |
| Fresh context pattern | 当当前会话积累了无关上下文或其输出质量下降时，刻意开启一个新会话。 | 工作流 | 上下文 |
| Gas Town | Steve Yegge 的多 agent 工作区管理器，用于运行多个协调的 Claude Code 实例并共享一个任务队列。 | 生态 | 编排 |
| Git worktree | 从同一仓库创建并行工作目录的 Git 特性。用于无需切换分支的多实例 Claude Code 工作流。 | 工作流 | 基础设施 |
| GSD (Get Shit Done) | 务实、以结果为导向的开发方法论：快速发布、用真实使用验证、基于反馈迭代。 | 方法论 | 范式 |
| gstack | Garry Tan 的 6-skill 工作流套件：策略门 + 架构评审 + 代码评审 + 发布说明 + 浏览器 QA + 复盘。 | 工作流 | 框架 |
| Guardrail tiers | 四个企业安全执行等级：Starter（意识）、Standard（评审门）、Strict（审批流程）、Regulated（完整审计）。 | 安全 | 企业 |
| Hallucination | 当 AI 模型生成听起来合理但事实错误的信息时，通常带有很高的表面自信。 | AI 工程 | 风险 |
| Hook | 由 Claude Code 生命周期事件触发的自动化脚本。在 `settings.json` 中定义。在工具执行之前或之后同步运行。 | Claude Code | 可扩展性 |
| Hook types | 五种执行类型：`command`（shell 脚本）、`http`（POST webhook）、`mcp_tool`（MCP server 工具）、`prompt`（单轮 LLM 调用）、`agent`（完整的多轮 sub-agent）。 | Claude Code | Hooks |
| Infisical | 开源密钥管理器，用于将凭据注入 Claude Code 会话，而无需将其存储在 CLAUDE.md 或 env 文件中。 | 生态 | 安全 |
| JSONL transcript | 以 JSON Lines 文件形式存储在 `~/.claude/projects/` 中的会话历史。可被以编程方式搜索、回放和分析。 | 架构 | 存储 |
| llms.txt | 用于 AI 优化文档的标准文件格式（放置在站点根目录）。Claude Code 会读取项目根目录中的 `llms.txt` 文件。 | AI 工程 | 标准 |
| Master loop | Claude Code 的核心执行循环：接收输入 → 选择工具 → 执行 → 观察结果 → 响应。重复直到任务完成。 | 架构 | 内部机制 |
| MCP (Model Context Protocol) | 由 Anthropic 开发的开放协议，用于以标准化方式将 AI 模型连接到外部工具、数据库和 API。 | 架构 | 协议 |
| Mechanic Stacking | 在关键决策上层叠多种 Claude Code 机制（Plan Mode + extended thinking + MCP）以实现最大推理的模式。 | 工作流 | 模式 |
| Memory hierarchy | CLAUDE.md 的三层优先级：Local > Project > Global。每一层扩展其下一层，并可在自身作用域内覆盖它。 | Claude Code | 记忆 |
| Model aliases | 解析为当前模型版本的简写名称：`default`、`sonnet`、`opus`、`haiku`、`sonnet[1m]`、`opusplan`。 | 模型 | 配置 |
| Modular context architecture | 将 CLAUDE.md 拆分为通过路径作用域规则动态加载的聚焦模块的模式，从而降低每会话的 token 开销。 | AI 工程 | 上下文 |
| multiclaude | 社区自托管的多 agent 生成器，使用 tmux + git worktrees。并行运行 N 个 Claude Code 实例。 | 生态 | 编排 |
| Native sandbox | Claude Code 内置的 OS 级沙箱：macOS 上为 Seatbelt，Linux 上为 bubblewrap。限制文件系统和网络访问。 | 安全 | 沙箱 |
| OpusPlan | 混合模式：Opus 4.8 负责规划（带 thinking），Sonnet 负责执行。用 `/model opusplan` 激活。 | 模型 | 配置 |
| Packmind | 将编码标准以 `CLAUDE.md` 文件、slash commands 和 skills 的形式跨仓库及 AI 工具（Claude Code、Cursor、Copilot）分发的工具。 | 生态 | 工具 |
| Permission modes | 五个自主等级：Default、Auto-accept、Plan、Don't Ask、Bypass Permissions。可按会话或在 `settings.json` 中设置。 | Claude Code | 权限 |
| Plan Mode | 只读模式，Claude 可以分析、搜索和提议，但不能修改文件。用 Shift+Tab 或 `/plan` 激活。 | Claude Code | 模式 |
| Plugin | 在 `plugin.json` 清单下打包 agents、skills、commands 和 hooks 的可分发包。可从 marketplace 安装。 | Claude Code | 可扩展性 |
| PostToolUse | 工具完成执行后触发的 hook 事件。用于后处理、格式化、验证和日志记录。 | Claude Code | Hooks |
| PreToolUse | Claude 执行工具之前触发的 hook 事件。可根据参数阻止、允许或修改工具调用。 | Claude Code | Hooks |
| Prompt injection | 一种攻击，文件或外部输入中的恶意文本试图覆盖 Claude 的指令或窃取信息。 | 安全 | 攻击 |
| Ralph Loop | 又称「Ralph Wiggum Loop」（Geoffrey Huntley）。迭代式精炼循环：生成 → 评审 → 纠正 → 重复，直到输出达到质量标准。 | 工作流 | 质量 |
| Recovery ladder | 三个层级的撤销：内联拒绝变更、/rewind 到会话 checkpoint、`git restore` 作为核弹级重置。 | Claude Code | 安全 |
| Rev the Engine | 在执行之前运行多轮深度分析和规划的模式，以便尽早暴露边界情况和失败模式。 | 工作流 | 模式 |
| Rewind | Claude Code 的撤销机制。将文件变更和/或对话状态回退到先前的 checkpoint。触发：Esc x2。 | Claude Code | 会话 |
| RTK (Rust Token Killer) | 一种 CLI 代理，在命令输出到达 Claude 之前进行过滤和压缩，将 token 消耗降低 60-90%。 | 生态 | 工具 |
| Rules (.claude/rules/) | 自动加载的 markdown 文件，提供始终生效的指令。在每次会话开始时加载，与哪些 skills 处于激活状态无关。 | Claude Code | 配置 |
| SE-CoVe (Software Engineering Chain-of-Verification) | 一个社区插件，通过独立评审 agent 实现 Chain-of-Verification 以进行自动化输出验证。基于 Meta 的 CoVe 研究（arXiv:2309.11495）。 | 生态 | 插件 |
| Semantic anchors | CLAUDE.md 中命名的引用模式（例如 `## Architecture`），Claude 能在跨会话中可靠地找到并遵循。 | AI 工程 | 上下文 |
| Session | 一次 Claude Code 对话，拥有自己的上下文窗口、历史、checkpoints 和工具状态。 | Claude Code | 核心 |
| Session handoff | 手动开启一个新会话，并从一个已耗尽或退化的先前会话传入一份总结性的上下文文档。 | 工作流 | 上下文 |
| SessionStart / SessionEnd | 会话开始或关闭时触发的 hook 事件。用于设置脚本、日志记录和清理自动化。 | Claude Code | Hooks |
| Shift+Tab | 在 Plan Mode 和 Act Mode 之间切换的键盘快捷键。 | Claude Code | 快捷键 |
| Skeleton project | 由 Claude 生成的最小但完全可运行的项目模板，用于在完整实现开始之前确立架构模式。 | 工作流 | 脚手架 |
| Skill | 一个可复用的知识模块（文件夹 + SKILL.md 入口点），按需提供领域专长或行为指令。 | Claude Code | 可扩展性 |
| Skill evals | 自动化的评估标准，衡量 skill 质量、调用可靠性和输出一致性。Skills 2.0 的一部分。 | Claude Code | Skills |
| Skills 2.0 | skills 系统的演进，引入了 Capability Uplift 类型、Encoded Preference 类型、evals 和生命周期管理。 | Claude Code | Skills |
| Slash command | 定义为 `.claude/commands/` 中 markdown 文件的自定义命令，用 `/command-name` 调用。支持 `$ARGUMENTS` 替换。 | Claude Code | 可扩展性 |
| Slop | 不想要的、未经评审的 AI 生成内容：相当于 AI 版的垃圾信息。该术语由 Simon Willison 在 2024 年 5 月提出。 | AI 工程 | 质量 |
| SonnetPlan | 社区对 OpusPlan 的重新映射：Sonnet 负责规划，Haiku 负责执行。对于较轻的任务比 OpusPlan 更便宜。 | 模型 | 配置 |
| Spec-first development | Addy Osmani 的模式：在任何实现开始之前先写一份详细的规格说明文档。减少范围蔓延并厘清边界情况。 | 工作流 | 规划 |
| Stop | Claude 即将停止响应时触发的 hook 事件。用于质量门、清理任务和完成通知。 | Claude Code | Hooks |
| Strategic gate | gstack 工作流中实现前的产品评审步骤。确保在写任何代码之前该功能值得构建。 | 工作流 | 质量 |
| Sub-agent | 由主会话生成的子 Claude 实例，用于在隔离环境中处理一个被委派的任务，拥有自己的上下文。 | Claude Code | 多 Agent |
| Supply chain attack | 利用受信任的依赖（MCP servers、插件、社区 skills）来注入恶意行为或窃取数据。 | 安全 | 攻击 |
| Tasks API | 内置任务管理系统（v2.1.16+），具备依赖跟踪、状态管理和跨会话持久化。取代 TodoWrite。 | Claude Code | 核心 |
| The 20% Rule | 决策框架：出现在 >20% 会话中的模式 → CLAUDE.md 规则；5-20% → skills；<5% → commands。 | Claude Code | 决策 |
| The 56% Reliability Warning | Vercel 工程博客发现（Gao，2026）：agent 仅在 56% 的时候调用按需 skills，其余情况下默认回退到原生知识。 | AI 工程 | 研究 |
| The 80% Problem | Addy Osmani 的观察：AI 可靠地处理一项任务的 80%；剩下的 20% 正是人类专长与判断决定成败之处。 | AI 工程 | 研究 |
| The Trinity | 结合 Plan Mode + Extended Thinking + Sequential MCP 的核心高级模式，用于在关键决策上实现最大推理深度。 | 工作流 | 模式 |
| Thinking tokens | 在 extended thinking 期间消耗的内部推理 token。在 Claude 的响应中不可见，但计入上下文预算。 | 模型 | 思考 |
| Token | 语言模型处理的文本基本单位。大致相当于 3/4 个英文单词，或约 4 个字符。1K tokens ≈ 750 个单词。 | 模型 | 核心 |
| Token efficiency | 在保持输出质量的同时最小化 token 消耗。对于成本管理、上下文余量和会话寿命至关重要。 | AI 工程 | 优化 |
| Tool shadowing | 一种攻击，恶意 MCP server 注册名称与 Claude Code 内置工具相同的工具，以拦截或劫持调用。 | 安全 | 攻击 |
| Tool-qualified deny | 一种基于参数值阻止工具的权限模式，例如 `Read(file_path:*.env*)` 以防止读取密钥文件。 | 安全 | 权限 |
| Trust calibration | 用于使验证投入与 AI 生成代码的实际风险等级相匹配的框架，避免盲目接受和偏执评审两个极端。 | AI 工程 | 质量 |
| UserPromptSubmit | 用户提交提示词、Claude 开始处理之前触发的 hook 事件。用于提示词增强、日志记录和验证。 | Claude Code | Hooks |
| Verification debt | 在创建时未经评审的 AI 生成代码所累积的风险，会在连续多个会话中复合叠加。 | AI 工程 | 风险 |
| Verification paradox | 既需要对 AI 代码进行严格验证，又日益依赖 AI 工具来执行该验证之间的张力。 | AI 工程 | 风险 |
| Vertical slice | 范围限定于一个面向用户的行为、贯穿所有架构层（UI → API → DB）的任务。是 AI 辅助实现的首选单元。 | 方法论 | 架构 |
| Vibe coding | 一种开发风格，你描述高层意图并对 AI 输出快速迭代，优先考虑发布速度而非精确度。 | 工作流 | 范式 |
| Vibe Review | 介于盲目接受和完整逐行评审之间的中间验证层。对低风险变更更快，仍能捕获明显问题。 | 工作流 | 质量 |
| Vitals | 通过 git 变动率 x 复杂度 x 模块耦合中心性的综合评分来进行代码库热点检测的社区插件。 | 生态 | 插件 |
| WHAT/WHERE/HOW/VERIFY | 结构化提示词格式：做什么、在代码库何处、如何着手、如何验证成功。减少 agentic 任务中的歧义。 | AI 工程 | 提示 |

---

*本参考涵盖约 130 个术语。官方 Claude Code 术语请参见 [glossary.md](./glossary.md)。完整指南请参见 [ultimate-guide.md](../ultimate-guide.md)。如需建议补充缺失的术语，请在 [GitHub](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/issues) 上提交 issue。*
