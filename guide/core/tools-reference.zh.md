# 内置工具参考

Claude Code 自带一组内置工具，用于读取、修改和执行你环境中的内容。你无需安装或配置它们，它们始终存在。

工具名称就是你在权限规则（`allow`/`deny`）、子代理的 `tools` 与 `disallowedTools` frontmatter、hook 的 `matcher` 字段，以及 CLI 标志 `--allowedTools`/`--disallowedTools` 中使用的确切字符串。要添加自定义工具，请连接一个 [MCP server](../ecosystem/mcp-servers-ecosystem.md)。要构建可复用的提示驱动工作流，请编写一个 [skill](../../examples/skills/)；它们通过现有的 `Skill` 工具运行，而不会新增一个工具条目。

---

## 所有内置工具

下表涵盖了 Claude Code 自带的每一个内置工具。"需要权限"表示在工具运行前会出现一次首次提示（在默认模式和 `acceptEdits` 模式下）。标记为"否"的工具运行时不会提示。

### 文件操作

| 工具 | 说明 | 需要权限 |
|------|-------------|:-------------------:|
| `Read` | 读取文件内容（文本、图片、PDF、Jupyter notebook） | 否 |
| `Write` | 创建或覆盖文件（若文件已存在则需先读取） | 是 |
| `Edit` | 在已有文件中进行精确的字符串替换 | 是 |
| `NotebookEdit` | 按 `cell_id` 修改 Jupyter notebook 单元格 | 是 |
| `Glob` | 按名称模式查找文件（`**/*.ts`、`src/**`） | 否 |
| `Grep` | 用 ripgrep 正则搜索文件内容 | 否 |
| `LSP` | 通过 language server 实现代码智能：跳转到定义、查找引用、类型错误 | 否 |

### 执行

| 工具 | 说明 | 需要权限 |
|------|-------------|:-------------------:|
| `Bash` | 在你的环境中运行 shell 命令 | 是 |
| `PowerShell` | 原生运行 PowerShell 命令（Windows 上一等支持，其他平台需手动启用） | 是 |
| `Monitor` | 在后台运行命令，并将每一行输出回传给 Claude（v2.1.98+） | 是 |

### Web

| 工具 | 说明 | 需要权限 |
|------|-------------|:-------------------:|
| `WebSearch` | 搜索网络并返回结果标题和 URL | 是 |
| `WebFetch` | 获取 URL，将 HTML 转换为 Markdown，并对其运行一个提取提示 | 是 |

### 代理与编排

| 工具 | 说明 | 需要权限 |
|------|-------------|:-------------------:|
| `Agent` | 派生一个拥有自己上下文窗口的子代理来处理任务 | 否 |
| `Workflow` | 运行动态工作流：一个编排众多子代理并返回单一结果的脚本 | 是 |
| `TeamCreate` | 创建一个包含多个队友的代理团队（`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`） | 否 |
| `TeamDelete` | 解散代理团队并清理队友进程 | 否 |
| `SendMessage` | 向代理团队的队友发送消息，或按 ID 恢复已停止的子代理 | 否 |

### 任务管理

| 工具 | 说明 | 需要权限 |
|------|-------------|:-------------------:|
| `TaskCreate` | 在会话任务列表中创建任务（v2.1.16+） | 否 |
| `TaskGet` | 获取某个特定任务的完整详情 | 否 |
| `TaskList` | 列出所有任务及其当前状态 | 否 |
| `TaskUpdate` | 更新任务状态、依赖关系或详情；也可删除任务 | 否 |
| `TaskStop` | 按 ID 终止一个正在运行的后台任务 | 否 |
| `TaskOutput` | 获取后台任务的输出（已弃用；建议改用对任务输出路径的 `Read`） | 否 |
| `TodoWrite` | 管理会话检查清单（自 v2.1.142 起默认禁用；设置 `CLAUDE_CODE_ENABLE_TASKS=0` 可重新启用） | 否 |

### 调度

| 工具 | 说明 | 需要权限 |
|------|-------------|:-------------------:|
| `CronCreate` | 在会话内调度一个周期性或一次性提示 | 否 |
| `CronDelete` | 按 ID 取消一个已调度的任务 | 否 |
| `CronList` | 列出会话中所有已调度的任务 | 否 |
| `ScheduleWakeup` | 为自定节奏的 `/loop` 重新调度下一次迭代（由 Claude 调用，而非你） | 否 |
| `RemoteTrigger` | 在 claude.ai 上创建、更新、运行并列出 Routines（Pro/Max/Team/Enterprise） | 否 |
| `PushNotification` | 在连接了 Remote Control 时发送桌面通知和手机推送 | 否 |

### MCP 集成

| 工具 | 说明 | 需要权限 |
|------|-------------|:-------------------:|
| `ToolSearch` | 当启用工具搜索时，为延迟加载的 MCP 工具加载 schema | 否 |
| `WaitForMcpServers` | 在使用 MCP server 的工具前等待仍在连接的 server（当工具搜索禁用时出现） | 否 |
| `ListMcpResourcesTool` | 列出已连接 MCP server 暴露的资源 | 否 |
| `ReadMcpResourceTool` | 按 URI 读取某个特定的 MCP 资源 | 否 |

### Worktree 与控制流

| 工具 | 说明 | 需要权限 |
|------|-------------|:-------------------:|
| `EnterWorktree` | 创建一个隔离的 git worktree 并切换进去（或用 `path` 切换进一个已有的） | 否 |
| `ExitWorktree` | 退出 worktree 会话并返回原目录 | 否 |
| `EnterPlanMode` | 切换到 plan mode，在编码前设计方案 | 否 |
| `ExitPlanMode` | 提交方案以供批准并退出 plan mode | 是 |
| `AskUserQuestion` | 提出多选问题以收集需求或澄清歧义 | 否 |
| `Skill` | 在主对话中执行一个 skill | 是 |
| `ShareOnboardingGuide` | 上传 `ONBOARDING.md` 并返回分享链接（Pro/Max/Team/Enterprise） | 是 |

---

## 权限规则格式

工具名称出现在权限规则中，可带一个可选的限定符：

| 规则格式 | 适用于 | 匹配内容 |
|-------------|------------|-----------------|
| `Bash(npm run *)` | `Bash`、`Monitor` | 按前缀/glob 匹配 shell 命令 |
| `PowerShell(Get-ChildItem *)` | `PowerShell` | PowerShell 命令 |
| `Read(~/secrets/**)` | `Read`、`Grep`、`Glob`、`LSP` | 文件路径 |
| `Edit(/src/**)` | `Edit`、`Write`、`NotebookEdit` | 文件路径 |
| `Skill(deploy *)` | `Skill` | Skill 名称前缀 |
| `Agent(Explore)` | `Agent` | 子代理类型名 |
| `WebFetch(domain:example.com)` | `WebFetch` | 域名 |
| `WebSearch` | `WebSearch` | 无限定符；对整个工具允许或拒绝 |

一条 `Edit(...)` 允许规则同时会授予对相同路径的读取权限，因此你无需在旁边再配一条匹配的 `Read(...)` 规则。

完整语法（包括路径前缀形式 `//`、`~/`、`/`、`./` 以及 Bash 通配符语义）请参见 [settings-reference.md 中的权限规则语法](./settings-reference.md#permission-rule-syntax)。

---

## 各工具的具体行为

### Bash

每条命令在独立的进程中运行。用 `cd` 做出的工作目录更改会延续到主会话中后续的 Bash 调用（但在子代理中不会），只要目标停留在项目目录或某个 `--add-dir` 路径之内。用 `export` 设置的环境变量不会在命令之间持久保留。请使用 `CLAUDE_ENV_FILE` 或一个 `SessionStart` hook 来传递环境状态。

默认超时为 2 分钟；Claude 每条命令最多可请求 10 分钟。输出默认上限为 30,000 个字符（可通过 `BASH_MAX_OUTPUT_LENGTH` 配置，上限为 150,000）。当命令超出上限时，完整输出会被保存到会话目录中的一个文件，Claude 会得到该路径外加一段简短预览。

对于长时间运行的进程，Claude 会设置 `run_in_background: true` 以将其作为后台任务启动。用 `/tasks` 列出并停止后台任务。

### Edit

执行精确的字符串替换。`old_string` 必须与所写内容完全一致地出现（逐字符一致，包括空白字符），且只能出现一次。如果它出现了不止一次，请提供一个更长的字符串，带上足够的上下文以锁定唯一一处，或使用 `replace_all: true`。Claude 在编辑前必须已在当前对话中读取过该文件，且自那次读取以来文件在磁盘上未发生变化。

### Glob

按名称模式查找文件，支持 `**` 递归匹配。结果按修改时间排序，上限为 100 个文件。Glob 默认不遵循 `.gitignore`（与 Grep 不同，Grep 会遵循）。

### Grep

使用 ripgrep 搜索文件内容。模式遵循 ripgrep 的正则语法，它与 POSIX grep 并不相同。像 `{` 和 `}` 这样的元字符需要转义（例如，用 `interface\{\}` 来查找 Go 的 `interface{}`）。Grep 遵循 `.gitignore` 并跳过被 gitignore 的文件；直接传入一个路径即可搜索被 gitignore 的文件。三种输出模式：`files_with_matches`（默认，仅路径）、`content`（带行号的匹配行）、`count`（每个文件的匹配数）。

### LSP

在你为所用语言安装代码智能插件之前处于非激活状态。每次文件编辑后，它会自动报告类型错误和警告。也可直接调用它来跳转到定义、查找引用、列出符号、追踪调用层次结构，以及获取某个位置的类型信息。

### Monitor（v2.1.98+）

让 Claude 在后台监视某些东西，并在其变化时做出反应。Claude 编写一个监视脚本，在后台运行，并在每行输出到达时接收它。适用于跟踪日志、轮询 CI 状态、监视目录的文件变化，或追踪长时间运行脚本的输出。使用与 Bash 相同的权限规则。在 Amazon Bedrock、Google Vertex AI 或 Microsoft Foundry 上不可用，且在设置了 `DISABLE_TELEMETRY` 或 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 时也不可用。

```text
# Ask Claude to set up a monitor like this:
"Tail /var/log/app.log and alert me when you see any ERROR line."
"Watch CI on PR #42 and tell me when it passes or fails."
```

### NotebookEdit

按 `cell_id` 一次修改一个 Jupyter notebook 单元格。三种模式：`replace`（覆盖单元格源代码，默认）、`insert`（在目标后添加一个新单元格）、`delete`（移除目标单元格）。它不会像 Edit 在普通文件上那样在整个 notebook 范围内执行字符串替换。

### PowerShell

在 Windows 上原生可用；在 Linux/macOS 上通过 `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` 手动启用（需要 `pwsh` 在 `PATH` 中）。Claude Code 仅在进程作用域内以 `-ExecutionPolicy Bypass` 启动 PowerShell，因此企业的 `MachinePolicy` 或 `UserPolicy` 锁定仍然生效。完整设置细节请参见 [PowerShell 原生工具一节](../ultimate-guide.md#powershell-native-tool)。

### Read

返回带行号的文件内容。可处理图片（PNG 和 JPG，作为可视内容返回）、PDF（短文件整体读取；对于超过 10 页的 PDF，使用 `pages` 参数按每次最多 20 页的范围读取），以及 Jupyter notebook（所有带输出的单元格）。当整文件读取会超出 token 上限时，Read 会返回第一页及一条提示，并给出读取更多内容所需的偏移量。

### WebFetch

接收一个 URL 和一个提取提示。获取页面，将 HTML 转换为 Markdown，并使用一个小而快的模型对内容运行该提取提示。Claude 收到的是该模型的回答，而非原始页面。这使得 WebFetch 在设计上就是有损的。提取提示决定了什么内容会到达 Claude。HTTP URL 会被自动升级为 HTTPS。响应会缓存 15 分钟。当某个 URL 重定向到不同主机时，WebFetch 会返回一个同时指明两个 URL 的文本结果，而不是跟随重定向；Claude 会针对新 URL 再发起一次调用。要获取原始未处理的页面，请通过 Bash 使用 `curl`。

### WebSearch

运行查询并返回结果标题和 URL。它不会获取结果页面；Claude 会用 WebFetch 跟进读取它找到的某个页面。每次调用最多可发起 8 次后端搜索以在内部优化结果。

### Write

创建一个新文件或覆盖一个已有文件。如果目标路径已存在，Claude 在覆盖前必须已在当前对话中至少读取过它一次。对于局部更改，Claude 会使用 Edit 而非 Write。

### Workflow（动态工作流，v2.1.154+）

运行一个 JavaScript 脚本，在后台编排众多子代理，并返回一个合并的结果。Claude 使用 `ultracode` 关键字（v2.1.160 中由 `workflow` 重命名而来，是一项破坏性变更）来触发多代理扇出。用 `/workflows` 监视运行中的工作流。需要用户显式选择启用：除非被要求，Claude 不会启动工作流。

---

## 高级工具：如何触发它们

### `/loop` 与 ScheduleWakeup

`/loop [interval] [prompt]` 命令以周期性间隔运行一个提示。省略间隔可让 Claude 自定节奏；每次迭代后它会调用 `ScheduleWakeup` 来决定下一次何时触发（介于 1 分钟到 1 小时之间）。待执行的唤醒会出现在 Stop hook 输入的 `session_crons` 中。用 Esc 或 Ctrl+C 取消。

```text
/loop 5m /ci-status        # check CI every 5 minutes
/loop /monitor-deploys     # self-paced monitoring loop
```

### 已调度任务：CronCreate / CronList / CronDelete

这些工具在当前会话内调度提示。任务的作用域限于会话，并在 `--resume` 或 `--continue` 时（若未过期）恢复。用 `CronList` 查看活动任务，用 `CronDelete` 按 ID 取消其中一个。你通过要求 Claude 调度某事来与它们交互：

```text
"Remind me to run the test suite in 30 minutes."
"Schedule a deploy check every hour until I cancel it."
```

### 远程 routine：RemoteTrigger 与 /schedule

`RemoteTrigger` 支撑着 `/schedule` 命令，并在 claude.ai 上创建 Routines。Routines 在当前会话之外按计划、通过 API 或在 GitHub 事件上运行。需要 Pro、Max、Team 或 Enterprise 套餐；在 Bedrock、Vertex AI 或 Foundry 上不可用。完整功能指南请参见 [Routines](../ultimate-guide.md#routines-cloud-automation)。

### 推送通知：PushNotification

Claude 调用 `PushNotification` 来发送桌面通知，并在连接了 Remote Control 且启用了"Push when Claude decides"时，发送手机推送。适用于你需要离开的长任务。投递通过 Anthropic 托管的基础设施运行，因此在 Bedrock、Vertex AI 或 Foundry 上不可用。参见 [Remote Control](../ultimate-guide.md#remote-control)。

### 代理团队：TeamCreate / TeamDelete / SendMessage

位于 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 之后的实验性功能。`TeamCreate` 派生一个由具名队友组成的团队；`SendMessage` 向某个队友发送消息，或按其代理 ID 恢复一个已停止的子代理；`TeamDelete` 解散团队。设置、模式和示例请参见专门的 [代理团队指南](../workflows/agent-teams.md)。

### Tasks API：TaskCreate 到 TaskStop

现代的任务管理系统（v2.1.16+，自 v2.1.142 起为默认）。完整工具集：

- `TaskCreate`：添加一个任务
- `TaskList`：列出所有任务（状态概览；不包含完整详情）
- `TaskGet`：获取某一个任务的完整详情
- `TaskUpdate`：更改状态、依赖关系或详情；也可删除
- `TaskStop`：按 ID 终止一个正在运行的后台任务

`TodoWrite` 是遗留的替代方案；它在 v2.1.142 被默认禁用。设置 `CLAUDE_CODE_ENABLE_TASKS=0` 可改为重新启用它。模式与跨会话持久化请参见 [Tasks API 一节](../ultimate-guide.md#tasks-api)。

---

## 提供商可用性

部分工具仅在 Claude Code 通过 Anthropic 自有基础设施连接时才可用：

| 工具 | 不可用于 |
|------|-----------------|
| `Monitor` | Amazon Bedrock、Google Vertex AI、Microsoft Foundry |
| `PushNotification` | Amazon Bedrock、Google Vertex AI、Microsoft Foundry |
| `ScheduleWakeup` | Amazon Bedrock、Google Vertex AI、Microsoft Foundry |
| `RemoteTrigger` | Amazon Bedrock、Google Vertex AI、Microsoft Foundry |
| `WebSearch` | Amazon Bedrock（未暴露） |

`Workflow`（`ultracode` 关键字）在不同提供商之间存在行为差异；请查阅发布说明了解当前状态。

---

## 另请参阅

- [架构内部机制](./architecture.md)：主循环、工具选择逻辑、上下文预算
- [权限规则语法](./settings-reference.md#permission-rule-syntax)：完整的 `allow`/`deny` 规则格式及所有指定符形式
- [子代理](../ultimate-guide.md#sub-agents)：`Agent` 如何派生工作、工具继承、前台与后台
- [Skills](../ultimate-guide.md#skills)：如何使用 `Skill` 工具构建可复用的提示词工作流
- [MCP 服务器](../ecosystem/mcp-servers-ecosystem.md)：如何通过 MCP 添加自定义工具
- [Hooks](../ultimate-guide.md#hooks)：在工具执行前后运行命令
