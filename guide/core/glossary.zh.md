---
title: "术语表"
description: "Claude Code 术语定义"
---

# 术语表

本指南通篇使用的术语定义。关于模型层面的概念（tokens、temperature、RAG），请参阅 [Anthropic 平台术语表](https://platform.claude.com/docs/en/about-claude/glossary)。

---

## A

### Agent teams（智能体团队）

由团队负责人协调的多个独立 Claude Code 会话，共享一份任务清单并支持点对点消息传递。与在单个会话内运行的 subagents 不同，每个团队成员都拥有自己的 context window，你可以直接与其中任何一个交互。这是一项实验性功能，需要 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 才能启用。参见 [§4 Agents](../ultimate-guide.md#4-agents)。

### Agentic loop（智能体循环）

Claude 处理每项任务所经历的循环：收集上下文、采取行动、验证结果，如此往复直至完成。每次工具使用都会返回信息，为下一步提供依据。大多数扩展点（hooks、skills、MCP）都接入这个循环的特定阶段。参见 [§1 How Claude Code Works](../ultimate-guide.md#1-how-claude-code-works)。

### Auto memory（自动记忆）

Claude 根据你的纠正和偏好为自己写下的笔记，按 git 仓库存储在 `~/.claude/projects/` 下。`MEMORY.md` 的前 200 行或前 25 KB 会在会话开始时加载。同一仓库的所有 worktree 共享一个自动记忆目录。参见 [§3 Memory](../ultimate-guide.md#3-configuration--memory)。

### Auto mode（自动模式）

一种权限模式，由一个独立的分类器模型在后台审核每个操作，而不是向你显示批准提示。该分类器会阻止权限范围升级、不可信的基础设施以及 prompt injection 尝试。它从不查看工具结果，因此对注入的指令免疫。这是一项研究预览功能。参见 [§3 Permission Modes](../ultimate-guide.md#3-configuration--memory)。

---

## B

### Bare mode（精简模式）

一个启动标志（`--bare`），会跳过对 hooks、skills、plugins、MCP 服务器、自动记忆和 CLAUDE.md 的自动发现。只有你显式传入的标志才会生效。推荐用于 CI 和脚本调用，因为你需要在不同机器上获得完全一致的行为。自 v2.1.81 起可用。参见 [§9 Headless/Non-interactive Mode](../ultimate-guide.md#9-advanced-features)。

### Bundled skills（内置技能）

随 Claude Code 一起提供的基于提示的操作手册，例如 `/batch`、`/code-review`、`/debug` 和 `/loop`。与执行固定逻辑的内置命令不同，bundled skills 为 Claude 提供一段详细的提示，并让它来编排工作。它们可以派生 agents、读取文件并适配你的代码库。参见 [§5 Skills](../ultimate-guide.md#5-skills)。

---

## C

### Channel（通道）

一个 MCP 服务器，会将事件推送到你正在运行的会话中，使 Claude 能够对你离开终端期间发生的事情做出反应。Channels 可以是双向的：Claude 读取一个入站事件并通过同一通道回复。研究预览中包含 Telegram、Discord 和 iMessage。参见 [§8 MCP](../ultimate-guide.md#8-mcp)。

### Checkpoint（检查点）

在你发送的每个提示处创建的还原点。Claude Code 会在每次编辑前对文件进行快照，因此你可以将代码、对话或两者还原到更早的状态。按两次 `Esc` 或运行 `/rewind` 来还原。Checkpoints 仅在会话内本地有效，与 git 独立，且不会跟踪通过 Bash 工具所做的更改。参见 [§9 Checkpointing](../ultimate-guide.md#9-advanced-features)。

### `.claude` 目录

Claude Code 读取项目级配置的目录：settings、hooks、skills、subagents、rules 和自动记忆。项目的根目录下有 `.claude/`；你的用户级默认配置位于 `~/.claude/`。参见 [§3 Configuration](../ultimate-guide.md#3-configuration--memory)。

### CLAUDE.md

一个由你为 Claude 编写的持久化指令 markdown 文件，会在每个会话开始时作为系统提示之后的一条用户消息加载。把项目约定、架构说明和行为规则放在这里。CLAUDE.md 能在 compaction 后保留，并随后从磁盘重新读取。参见 [§3.1 Memory Files](../ultimate-guide.md#31-memory-files-claudemd)。

### Compaction（压缩）

当 context window 接近上限时对你的对话进行的自动摘要。较早的工具输出会先被清除，然后对话会被摘要。CLAUDE.md 和自动记忆能在 compaction 后保留并从磁盘重新加载；仅在对话中给出的指令可能会丢失。运行 `/compact` 可手动触发。参见 [§2 Context Window](../ultimate-guide.md#2-core-concepts)。

---

## D

### Dispatch（派发）

一个由手机发起的任务路由器，当你从 Claude 移动应用发送一项编码任务时，它会在 Desktop 应用中派生一个 Claude Code 会话。你的提示会自动路由到合适的工具。在 Pro 和 Max 套餐中可用。参见 [§9 Desktop Features](../ultimate-guide.md#9-advanced-features)。

---

## E

### Effort level（投入级别）

一项设置，控制 Claude 每轮使用多少自适应推理的思考预算。更高的投入意味着更多的思考 tokens 和更深入的推理；更低的投入则更快、更省钱。在 Opus 4.6+ 和 Sonnet 4.6 上受支持。Skills 可以在其 frontmatter 中覆盖会话的投入级别。参见 [§2.5 Model Selection](../ultimate-guide.md#25-model-selection--thinking-guide)。

### Extended thinking（扩展思考）

模型在回应之前进行的可见的逐步推理。你可以用 `MAX_THINKING_TOKENS` 限制思考 tokens，或调整投入级别。思考内容在终端中以灰色斜体文本显示。参见 [§2.5 Model Selection](../ultimate-guide.md#25-model-selection--thinking-guide)。

---

## H

### Hook（钩子）

一个用户定义的处理器，会在 Claude Code 生命周期的特定时刻自动执行，例如在工具运行之前、文件编辑之后或会话开始时。一个 hook 配置有三个层级：hook 事件（哪个生命周期时刻）、matcher（哪些事件触发它）以及 hook 处理器（运行什么）。处理器可以是 shell 命令、HTTP 端点、MCP 工具、LLM 提示或 subagent。Hooks 是确定性的：它们在固定的生命周期时刻触发，而非由模型自行决定。参见 [§7 Hooks](../ultimate-guide.md#7-hooks)。

---

## M

### Managed settings（托管设置）

由 IT 或 DevOps 在全组织范围内强制执行的设置文件，放置在 `~/.claude` 之外的操作系统级路径上。用户无法覆盖或排除托管设置。可用于安全策略、合规要求，或在整批机器上推行标准化工具链。参见 [§3.3 Settings](../ultimate-guide.md#33-settings--permissions)。

### MCP (Model Context Protocol)

一个用于将 AI 工具连接到外部数据源和服务的开放标准。MCP 服务器为 Claude 提供连接 Slack、Jira、数据库、浏览器以及数百种其他集成的新工具。通过 `/mcp` 连接服务器，或将其添加到 `.mcp.json` 中。参见 [§8 MCP](../ultimate-guide.md#8-mcp)。

### MCP Tool Search（MCP 工具搜索）

一种节省上下文的机制，会将 MCP 工具的 schema 推迟到需要时再加载。启动时只加载工具名称；当 Claude 决定使用某个特定工具时，它会按需获取完整的 schema。这能防止闲置的 MCP 服务器消耗上下文。参见 [§8 MCP](../ultimate-guide.md#8-mcp)。

---

## N

### Non-interactive mode（非交互模式）

一种模式，执行单个提示后退出，不进入对话式会话，通过 `-p` 或 `--print` 调用。用于 CI、脚本和管道。`--bare` 标志在此基础上为全新状态的自动化作了扩展。曾称为“headless mode”。参见 [§9 Non-interactive Mode](../ultimate-guide.md#9-advanced-features)。

---

## O

### Output style（输出风格）

一项配置，会修改 Claude 的系统提示，以改变回应的行为、语气或格式。与作为用户消息传递的 CLAUDE.md 不同，output styles 会关闭默认系统提示中针对软件工程的部分。内置风格包括 Default、Proactive、Explanatory 和 Learning。参见 [§3 Configuration](../ultimate-guide.md#3-configuration--memory)。

---

## P

### Permission mode（权限模式）

会话的基线批准行为。可用模式有 `default`、`acceptEdits`、`plan`、`auto`、`dontAsk` 和 `bypassPermissions`。在 CLI 中用 `Shift+Tab` 循环切换，或在 VS Code、Desktop 和 claude.ai 中使用模式选择器。参见 [§3.3 Settings](../ultimate-guide.md#33-settings--permissions)。

### Permission rule（权限规则）

一个设置条目，根据工具名称和参数模式对工具调用进行允许、询问或拒绝。规则按“先拒绝、再询问、后允许”的顺序求值，因此首个匹配项生效。Permission rules 是叠加在更宽泛的权限模式之上的细粒度控制。参见 [§3.3 Settings](../ultimate-guide.md#33-settings--permissions)。

### Plan mode（计划模式）

一种权限模式，Claude 在其中进行研究并提出更改建议，但不编辑你的源文件。它可以读取、搜索并运行探索命令，然后在改动任何内容之前呈现一份计划供批准。用 `/plan` 或按 `Shift+Tab` 进入计划模式。参见 [§3.3 Settings](../ultimate-guide.md#33-settings--permissions)。

### Plugin（插件）

将 skills、hooks、subagents 和 MCP 服务器打包成单个可安装单元的捆绑包。Plugin 的 skills 以 `plugin-name:skill-name` 命名空间区分，因此多个插件可以共存而不冲突。通过 marketplace 在团队间分发插件。参见 [§5 Skills](../ultimate-guide.md#5-skills)。

### Project trust（项目信任）

一个在 Claude Code 加载其配置之前接受某个目录的对话框。接受状态按项目目录保存，但你的主目录除外（在主目录中信任仅在单次会话内有效）。信任是 marketplace 插件自动安装和项目定义 hooks 执行的门槛。参见 [§3 Configuration](../ultimate-guide.md#3-configuration--memory)。

### Prompt injection（提示注入）

嵌入在文件、网页或工具结果中的恶意指令，试图把 Claude 引向你从未请求过的操作。Claude Code 的防御措施包括权限系统、命令黑名单和信任验证。Auto mode 增加了一个服务端分类器，它从不查看工具结果，因此被注入的文本无法影响其批准决策。参见 [§10 Security](../ultimate-guide.md#10-security)。

---

## R

### Remote Control（远程控制）

一种通过 claude.ai 从手机或浏览器继续本地 Claude Code 会话的方式。你的代码保留在你的机器上；只有 UI 是远程的。这与运行在云端沙箱中的 Claude Code on the web 不同。参见 [§9.22 Remote Control](../ultimate-guide.md#922-remote-control-mobile-access)。

### Rules（规则）

位于 `.claude/rules/` 中的模块化指令文件，与 CLAUDE.md 一同加载。一个 rule 可以通过 YAML 的 `paths:` frontmatter 进行路径范围限定，使其仅在 Claude 读取匹配的文件时才加载，从而在相关之前保持上下文精简。参见 [§3.1 Memory Files](../ultimate-guide.md#31-memory-files-claudemd)。

---

## S

### Sandboxing（沙箱）

针对 Bash 工具的操作系统级文件系统和网络隔离。命令在你预先定义的边界内运行，因此 Claude 可以在其中自由工作，无需逐条命令的批准提示。Sandboxing 是与 permission rules 分开的一层。参见 [§10 Security](../ultimate-guide.md#10-security)。

### Session（会话）

一个绑定到你当前目录的对话，拥有自己独立的 context window。会话可以用 `claude -c` 恢复，用 `--fork-session` 派生，或跨多个终端并行运行。每个会话的记录存储在 `~/.claude/projects/` 下。参见 [§1 How Claude Code Works](../ultimate-guide.md#1-how-claude-code-works)。

### Settings layers（设置层级）

Claude Code 读取配置的层级，按优先级从高到低排列：托管策略、命令行参数、位于 `.claude/settings.local.json` 的本地设置、位于 `.claude/settings.json` 的项目设置，然后是位于 `~/.claude/settings.json` 的用户设置。数组会跨层级合并；较高层级的标量值会覆盖较低层级的。参见 [§3.3 Settings](../ultimate-guide.md#33-settings--permissions)。

### Skill（技能）

一个 `SKILL.md` 文件，包含 Claude 添加到其工具集中的指令、知识或工作流。用 `/skill-name` 直接调用。Skills 遵循 Agent Skills 开放标准；Claude Code 在其基础上扩展了调用控制和 subagent 执行。Skills 是自定义命令的推荐继任者：`.claude/commands/` 文件仍可继续使用，但 `.claude/skills/` 是首选位置。参见 [§5 Skills](../ultimate-guide.md#5-skills)。

### Subagent（子智能体）

一个专门的 AI 助手，在自己的 context window 中运行，拥有自定义系统提示、特定的工具访问权限和独立的权限。它处理一项被委派的任务，并向主对话返回一份摘要。与 agent teams（其中每个 agent 都是一个完整的独立会话）不同，subagents 在父会话内运行并向其汇报。参见 [§4 Agents](../ultimate-guide.md#4-agents)。

### Surface（界面入口）

你访问 Claude Code 的任何场所：CLI、VS Code、JetBrains、Desktop 或 claude.ai。所有界面入口共享同一引擎，因此你的 CLAUDE.md、settings 和 skills 在它们之间的行为完全一致。Slack 和 Chrome 扩展是连接到某个界面入口的集成，而非界面入口本身。

---

## T

### Teleport（传送）

一个命令（`/teleport`），将一个云端 Claude Code 会话拉取到你的本地终端。Claude 会获取分支、加载对话历史，并从该 web 会话的最后状态恢复。反方向是 `--remote`，它会发送一项本地任务到 web 上运行。参见 [§9.16 Session Teleportation](../ultimate-guide.md#916-session-teleportation)。

### Tool（工具）

Claude 可以采取的一项行动：读取文件、编辑代码、运行 shell 命令、搜索网页、派生 subagent。工具正是让 Claude Code 具备智能体能力的关键。没有它们，Claude 只能用文本回应。每次工具使用都会返回一个结果，为 Claude 在智能体循环中的下一步决策提供依据。参见 [§1 How Claude Code Works](../ultimate-guide.md#1-how-claude-code-works)。

### Turn（轮次）

会话中 Claude 的一次完整回应。一个轮次从你发送消息时开始，到 Claude 完成回应时结束，其间可包含任意数量的工具调用。Stop hooks 会在每个轮次结束时触发。参见 [§7 Hooks](../ultimate-guide.md#7-hooks)。

---

## V

### Verification loop

一种会话模式：你给 Claude 一个它可以运行的检查项（测试套件、构建或截图对比），Claude 会持续迭代直到检查通过，而不是尝试一次就停下。verification loop 是 `/goal`、无人值守运行和动态工作流的前提条件：没有它，判断 agent 是否完成的唯一信号就只剩 agent 自己。参见 [§9 高级功能](../ultimate-guide.md#9-advanced-features)。

---

## W

### Worktree isolation

一种隔离模式，让 Claude 在 `.claude/worktrees/` 下的独立 git worktree 中运行，通过 `-w` 标志或 subagent 配置中的 `isolation: worktree` 启用。改动会保留在独立的分支和目录中，因此并行的 agent 不会覆盖彼此的文件。参见 [§4 Agents](../ultimate-guide.md#4-agents)。

---

## 已弃用和重命名的术语

这些术语出现在较旧的文档和社区内容中。在本指南中检索时请使用当前名称。

| 旧术语 | 现称 | 备注 |
|----------|-----------|-------|
| Headless mode | Non-interactive mode | 同样的 `-p` 标志，同样的行为 |
| Custom commands | Skills | `.claude/commands/` 文件仍然有效 |
| Slash commands | Commands | 产品文案中去掉了 "Slash" |
