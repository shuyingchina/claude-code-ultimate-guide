---
title: "Claude Code Release History"
description: "Condensed changelog of official Claude Code releases with highlights and breaking changes"
tags: [reference, release]
---

# Claude Code 发布历史

> Claude Code 官方发布的精简版更新日志。
> **完整详情**：[github.com/anthropics/claude-code/CHANGELOG.md](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
> **机器可读版**：[claude-code-releases.yaml](../../machine-readable/claude-code-releases.yaml)

**最新版本**：v2.1.173 | **更新时间**：2026-06-11

---

## 快速跳转

- [2.1.x 系列（2026 年 1 月-6 月）](#21x-series-january-june-2026)：bug 修复（2.1.173）、⭐ sub-agents 可派生 sub-agents + Bedrock 区域自动检测（2.1.172）、⭐ Claude Fable 5（2.1.170）、⭐ `--safe-mode` + `/cd` 命令（2.1.169）、bug 修复（2.1.168、2.1.167、2.1.165）、`fallbackModel` + deny 规则 glob + 关闭 thinking + 加固的 SendMessage（2.1.166）、`requiredMinimumVersion`/`requiredMaximumVersion` + `/plugin list` + Stop hook additionalContext（2.1.163）、更安静的启动 + agents waitingFor + slash-command 填充（2.1.162）、OTEL 自定义维度 + agents done/total + 并行 tool-call 隔离（2.1.161）、`ultracode` 关键字取代 `workflow` + 启动文件安全提示 + grep 后 Edit（2.1.160）、内部基础设施（2.1.159）、Bedrock/Vertex/Foundry 上 Opus 4.7/4.8 的 Auto 模式（2.1.158）、从 `.claude/skills` 自动加载插件 + `claude plugin init` + 20+ bug 修复（2.1.157）、Opus 4.8 thinking-blocks 崩溃修复（2.1.156）、Opus 4.8 + 动态 workflows + 默认精简系统提示（2.1.154）、/model 保存为默认（与 IDE 一致）+ modelPicker 键位重命名（2.1.153）、code-review 修复应用到工作树、disallowed-tools frontmatter、MessageDisplay hook、移除 auto 模式选择加入、35+ bug 修复（2.1.152）、内部基础设施（2.1.150）、/usage 按类别细分（skills/subagents/plugins/MCP）、GFM 任务列表复选框、PowerShell 权限绕过安全修复、sandbox worktree 写入白名单修复、allowAllClaudeAiMcps 企业设置、20+ bug 修复、固定的后台会话（Ctrl+T）、用于内联 GitHub PR 评论的 /code-review --comment、自动更新改进、Bash exit-127 热修复、带 effort 级别的 /code-review 命令（从 /simplify 重命名）、auto 模式恢复 AskUserQuestion、agents --json、安装前的 /plugin 预览、权限提示绕过安全修复、/resume 列出后台会话、/model 仅当前会话（d 设为默认）、用量积分重命名、75 秒启动挂起修复、插件依赖强制、/plugin 中的预计 context 成本、worktree.bgIsolation: "none"、fast 模式 Opus 4.7 默认、新的 claude agents 派发标志、SKILL.md 根级插件呈现、hook terminalSequence、claude agents --cwd、Rewind summarize、subagent_type 大小写不敏感、插件文件夹警告、agent 视图（研究预览）、/goal 命令、hook 参数 exec 形式 + continueOnBlock、settings.autoMode.hard_deny、CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL、MCP /clear 消失修复、40+ UI 修复、worktree.baseRef 设置、hook 中的 effort 级别、Bash 环境中的 CLAUDE_CODE_SESSION_ID、CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN、MCP 内存修复（10GB+ RSS）、subagent skills 修复、40+ bug 修复、Worktree 隔离、后台 agents、ConfigChange hook、Fast 模式 Opus 4.6、1M context、claude.ai MCP 连接器、remote-control、auto-memory、/copy 命令、HTTP hooks、worktree 配置共享、重新引入 ultrathink、InstructionsLoaded hook、4 项安全修复、恢复 Agent 模型覆盖、SDK token 成本降低 12 倍、/context 可操作建议、modelOverrides 设置、Max/Team/Enterprise 默认 1M context Opus 4.6、MCP elicitation、PostCompact hook、/effort 命令、Opus 4.6 64k/128k 输出 token、allowRead sandbox 设置、/branch 命令、StopFailure hook、逐行流式、--console 认证标志、SessionEnd 修复、企业重试修复、rate_limits 状态栏字段、skills 的 effort frontmatter、--channels MCP 研究预览、--bare 标志、worktree 会话恢复修复、MCP 查询折叠、managed-settings.d/ 嵌入式配置、CwdChanged/FileChanged hooks、transcript 搜索、凭据擦除、PowerShell 工具 Windows 预览、条件 hook if 字段、MCP headersHelper 多服务器环境变量、headless AskUserQuestion hooks、X-Claude-Code-Session-Id header、Jujutsu/Sapling VCS 排除、@ 提及 token 减少、Read 工具紧凑格式、Cowork Dispatch 修复、PermissionDenied hook、默认关闭 thinking 摘要、PreToolUse 权限的 "defer"、CLAUDE_CODE_NO_FLICKER、/powerup 交互式课程、PowerShell 加固权限、SSE 线性时间性能、MCP 500K 结果覆盖、disableSkillShellExecution、插件 bin/ 可执行文件、Edit 工具更短锚点、交互式 Bedrock 向导、forceRemoteSettingsRefresh、/cost 按模型细分、交互式 /release-notes、Linux sandbox apply-seccomp 修复、Bedrock Mantle 支持、API/企业用户默认 high effort、Bedrock 认证修复、NO_FLICKER 聚焦视图（Ctrl+O）、refreshInterval 状态栏、30+ bug 修复、Vertex AI 向导、Monitor 工具、CLAUDE_CODE_PERFORCE_MODE、Bash 安全加固、子进程 PID namespace sandbox、/team-onboarding 命令、默认信任 OS CA 证书库、/ultraplan 自动云环境、40+ bug 修复、PreCompact hook 阻塞、EnterWorktree path 参数、插件监控、/proactive 别名、WebFetch CSS/JS 剥离、/doctor 状态图标、更早的 thinking 提示、ENABLE_PROMPT_CACHING_1H、/recap 会话 context、通过 Skill 工具的内置 slash 命令、/undo 别名、旋转的 extended-thinking 指示器、/tui 全屏命令、push notification 工具、--resume 恢复定时任务、/focus 命令、autoScrollEnabled 配置、为禁用遥测的会话提供 session recap、30+ bug 修复、Opus 4.7 xhigh effort、/ultrareview 云端代码审查、/less-permission-prompts skill、Max 订阅者的 Auto 模式、以提示词命名的计划文件、只读 bash glob 模式无提示、交互式 /effort 滑块、众多 bug 修复、原生二进制派生、sandbox.network.deniedDomains、安全加固 exec 包装器、权限对话框崩溃修复、/resume 快 67%、内联 thinking 进度、sandbox dangerous-path 安全修复、通过 --agent 的 agent frontmatter hooks、众多终端和 UI bug 修复、Pro/Max 在 Opus 4.6+Sonnet 4.6 上默认 high effort、macOS/Linux 上原生 bfs/ugrep、/model 跨重启持久化、Opus 4.7 1M context 修复、15+ bug 修复、vim 可视模式、/usage 合并自 /cost+/stats、自定义命名主题、hooks 调用 MCP 工具、DISABLE_UPDATES 环境变量、wslInheritsWindowsSettings、15+ bug 修复、/config 设置持久化到 settings.json、--from-pr 多平台支持、agent frontmatter 遵守 tools+permissionMode、blockedMarketplaces 安全修复、TaskList 排序修复、30+ bug 修复、Windows 不再需要 Git Bash（PowerShell 回退）、claude ultrareview CI 子命令、skills 中的 ${CLAUDE_EFFORT}、alwaysLoad MCP 选项、plugin prune、所有工具的 PostToolUse 输出替换、ANTHROPIC_BEDROCK_SERVICE_TIER、/resume 搜索中的 PR URL、OAuth 401 热修复、/model 选择器中的 gateway /v1/models 列表、claude project purge、WSL2/SSH/容器的 OAuth 粘贴码、安全修复 allowManagedDomainsOnly/allowManagedReadPathsOnly、Windows PowerShell 7 作为主 shell、40+ bug 修复、EnterWorktree 从本地 HEAD 创建分支修复、--plugin-dir .zip 支持、--channels console 认证、每服务器 /mcp 工具计数、并行 bash 工具调用修复、sub-agent 提示缓存修复、35+ bug 修复、--plugin-url 标志、CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE、恢复 Ctrl+R 全项目历史、skillOverrides 修复、1h 缓存 TTL 修复、OAuth 刷新竞态修复、20+ bug 修复、VS Code Windows 激活修复、Mantle 认证修复
- [2.0.x 系列（2025 年 11 月 - 2026 年 1 月）](#20x-series-november-2025---january-2026) — Opus 4.5、Chrome 中的 Claude、后台 agents
- [重大变更摘要](#breaking-changes-summary)
- [里程碑功能](#milestone-features)

---

## 2.1.x 系列（2026 年 1 月-6 月）

### v2.1.173 (2026-06-11)

> Bug 修复：Fable 5 `[1m]` 后缀规范化、Windows sandbox 警告修复。

- **修复**：带 `[1m]` 后缀的 Fable 5 模型名称未被规范化（Fable 5 默认包含 1M context，现在会自动剥离后缀）
- **修复**：当设置中启用 sandbox 时，Windows 上出现的虚假 "sandbox dependencies missing" 启动警告

---

### v2.1.172 (2026-06-11)

> ⭐ Sub-agents 可派生 sub-agents（深度达 5 层）、Bedrock 区域自动检测、插件搜索栏、20+ bug 修复。

- **新增**：Sub-agents 现在可以派生自己的 sub-agents，深度最多达 5 层
- **新增**：当未设置 `AWS_REGION` 时，Amazon Bedrock 现在会从 `~/.aws` 配置文件读取 AWS 区域，与 AWS SDK 的优先级一致；`/status` 会显示区域的来源
- **新增**：在 `/plugin` 中浏览某个 marketplace 的插件时新增了搜索栏
- **新增**：为 `claude_code.lines_of_code.count` OTEL 指标添加了 `model` 属性
- **修复**：使用 1M context 但没有用量积分的会话会永久卡住；现在会话会自动 compact 回到标准 context 限制以下
- **修复**：当对话包含多张图片时，反复出现 "an image in the conversation could not be processed and was removed" 错误
- **修复**：worker 回复后，Agents 视图会让会话保持在 "Working" 状态并显示忙碌的转圈最长达 30 秒
- **修复**：派发到预热 worker 上的后台 agents 可能读取到另一个目录的项目设置
- **修复**：在守护进程自动更新后，附加到在旧版本上启动的会话时，后台会话附加因 EAUTH 而失败
- **修复**：在它派生的嵌套 agent 被停止后，后台 sub-agent 在 agent 面板中仍卡在 "active" 状态
- **修复**：`/model` 建议带有误导性的斜杠前缀，并显示对你的组织已禁用的模型
- **修复**：`availableModels` 限制未应用于 subagent 模型覆盖、agent 派发模型选择器以及 advisor 模型
- **修复**：当条目使用 `claude-opus-4-8` 这类版本特定 ID 时，`availableModels` 白名单会隐藏 `/model` 选择器中的 Opus 和 Sonnet 1M 行
- **修复**：Bedrock 上的 `/model` 选择器提供了该提供商不支持的模型——选择其中之一会静默切换会话模型，并在多行上点亮选择标记
- **修复**：当 `ANTHROPIC_DEFAULT_OPUS_MODEL` 已包含 1M-context 后缀时，模型 ID 会获得重复后缀（例如 `[1M][1m]`）
- **修复**：`opusplan` 模型设置在 plan 模式下未为有权限的用户附带 1M context；`opusplan[1m]` 变通方法现在也能在 plan 模式下正确切换到 Opus
- **修复**：`WebFetch(domain:*.example.com)` 通配符域名规则从未匹配子域名；带中间通配符的文件权限规则（例如 `Read(secrets-*/config.json)`）在启动时被拒绝
- **修复**：当 subagent 的聊天标签页打开时，上方向键提示历史显示主 agent 的提示词
- **修复**：在远程会话中，内存召回找不到挂载的团队内存存储（`CLAUDE_MEMORY_STORES`）
- **修复**：Workflow 校验拒绝其提示字符串或注释提及 `Date.now()`/`Math.random()` 的脚本
- **修复**：不完全支持鼠标追踪的 Windows 控制台上的鼠标追踪
- **修复**：退出长列表后 `/plugin` marketplace 列表丢失光标；从插件浏览器按 Esc 返回到错误的标签页
- **改进**：长对话中的性能（移除了冗余的消息规范化，减少全量消息历史转换）
- **改进**：降低空闲 CPU 占用——`/goal` 状态徽标在空闲时不再以 5 Hz 重绘终端
- **改进**：Chrome 中的 Claude 浏览器工具现在通过单次批量调用加载，而非每个工具一次
- **改进**：非交互式用量策略拒绝消息建议开始新会话或更换模型
- **改进**：未登录 claude.ai 时，`/code-review` 保持 `ultra` 选项可见并附带说明
- **改进**：Remote Control 页脚指示器缩短为 "/rc active"，在窄终端上隐藏
- **改进**：停止在远程会话中推广 `/loop`，因为待处理的循环无法保持容器存活
- **修复 [VSCode]**：PowerShell 工具调用渲染为原始 JSON 而非正确的命令显示；从显示的 shell 输出中剥离 ANSI 转义码

---

### v2.1.170 (2026-06-09)

> ⭐ Claude Fable 5（Mythos 级模型）访问、VS Code 终端会话的 transcript 修复。

- **新增**：Claude Fable 5 现已可用：这是一个 Mythos 级模型，能力超越此前任何普遍可用的 Anthropic 模型。参见[公告](https://www.anthropic.com/news/claude-fable-5-mythos-5)。
- **修复**：从 VS Code 集成终端（或任何继承了 Claude Code 环境变量的 shell）启动的会话未保存 transcript 且未出现在 `--resume` 中

---

### v2.1.169 (2026-06-09)

> ⭐ `--safe-mode` 标志、`/cd` 命令、`disableBundledSkills` 设置、15+ bug 修复。

- **新增**：`--safe-mode` 标志（以及 `CLAUDE_CODE_SAFE_MODE` 环境变量）：以禁用所有自定义项（CLAUDE.md、plugins、skills、hooks、MCP servers）的方式启动 Claude Code 用于故障排查
- **新增**：`/cd` 命令：将会话移动到新的工作目录，且不会在会话中途破坏提示缓存
- **新增**：`disableBundledSkills` 设置和 `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS` 环境变量，用于对模型隐藏内置 skills、workflows 和 slash 命令
- **修复**：方向键越过长输入行的换行行直接跳到命令历史；现在它们会先逐个视觉行移动
- **修复**：企业托管 MCP 策略（`allowedMcpServers`/`deniedMcpServers`）在重连、IDE 输入的配置、安装后首次会话期间的 `--mcp-config` 服务器或远程设置加载前未被强制执行
- **修复**：以 claude.ai 凭据登录的 macOS 用户在每个回合开始时约 30-50ms 的 UI 卡顿
- **修复**：`claude -p` 在 Windows 上等待 slash-command/skill 扫描时缓慢或挂起（自 2.1.161 起的回归）
- **修复**：会话恢复期间 OAuth token 刷新后 Remote Control 卡在 "reconnecting"
- **修复**：Windows 启动时弹出 Git Credential Manager 的 "Connect to GitHub" 弹窗
- **修复**：对于使用自定义状态栏的用户，页脚提示（例如 "esc to interrupt"）未显示
- **修复**：`claude agents --json` 遗漏被阻塞和刚派发的后台会话；新增 `--all` 以包含已完成会话以及新的 `id` 和 `state` 字段
- **修复**：派发到预热 worker 上时，后台 agents 忽略项目级 `env` 值（例如 `ANTHROPIC_MODEL`）
- **改进**：`TaskCreate` 可靠性：格式错误的输入会自动修复；未加载工具的校验错误会包含 schema
- **改进**：响应流式传输期间和转圈动画期间降低 CPU 占用
- **改进**：即使在某个回合进行中，`/workflows` 现在也会立即打开

---

### v2.1.168 (2026-06-06)

> Bug 修复和可靠性改进。

---

### v2.1.167 (2026-06-06)

> Bug 修复和可靠性改进。

---

### v2.1.166 (2026-06-06)

> `fallbackModel` 设置、deny 规则 glob 模式、在默认 thinking 模型上关闭 thinking、加固的 `SendMessage`、15+ bug 修复。

- **新增**：`fallbackModel` 设置：配置最多 3 个回退模型，在主模型过载或不可用时按顺序尝试；`--fallback-model` 在交互式会话中同样有效
- **新增**：deny 规则工具名位置支持 glob 模式（`"*"` 拒绝所有工具）；allow 规则拒绝非 MCP 的 glob；deny 规则中未知的工具名在启动时发出警告
- **安全**：加固跨会话消息传递：通过 `SendMessage` 转发的消息不再携带用户权限；接收方拒绝转发的权限请求，auto 模式将其阻止
- **变更**：`MAX_THINKING_TOKENS=0`、`--thinking disabled` 以及按模型 thinking 开关现在会通过 Claude API 在默认 thinking 的模型上关闭 thinking（第三方提供商不变）
- **变更**：当 API 拒绝意外的不可重试错误时，Claude Code 会在回退模型上重试一次该回合；认证、限速、请求大小和传输错误仍会立即浮现
- **变更**：`claude update` 现在会在下载前宣布目标版本
- **新增**：`claude agents`：在列表中输入 URL 会过滤到首个提示词包含该 URL 的会话
- **修复**：启动时 worker 注册期间发生后端中断时，后台会话会卡住
- **修复**：2026.1+ 版本上的 JetBrains IDE 终端闪烁（IntelliJ、PyCharm、WebStorm），已启用同步输出
- **修复**：使用 Kitty 键盘协议的终端（WezTerm、Ghostty、kitty）中丢失 Shift+非 ASCII 字符（例如 Shift+ä → Ä）
- **修复**：当被终止进程的子进程持有输出管道时，Windows 上 PowerShell 命令校验挂起
- **修复**：守护进程死亡后 macOS 上孤立的 `claude --bg-pty-host` 进程以 100% CPU 空转
- **修复**：带有无效条目的托管设置会静默禁用其余有效策略
- **修复**：`allowedMcpServers`/`deniedMcpServers` 谓词无法匹配带 `${VAR}` 引用的情况
- **修复**：git worktree 中的后台 agent 会话在重新打开时因 "No conversation found" 而崩溃循环
- **修复**：流式传输时 Ctrl+O transcript 视图中的 thinking 文本重复

---

### v2.1.165 (2026-06-05)

> Bug 修复和可靠性改进。

---

### v2.1.163 (2026-06-04)

> `requiredMinimumVersion`/`requiredMaximumVersion` 托管设置、`/plugin list`、Stop hook `additionalContext`、10+ bug 修复。

- **新增**：`requiredMinimumVersion` 和 `requiredMaximumVersion` 托管设置：如果 Claude Code 的版本超出允许范围，它会拒绝启动并引导用户使用获批版本
- **新增**：`/plugin list` 命令，用于列出已安装的插件，带 `--enabled`/`--disabled` 过滤器
- **新增**：为 `/btw` 添加 "c to copy" 快捷键，将原始 markdown 答案复制到剪贴板
- **变更**：Stop 和 SubagentStop hooks 现在可以返回 `hookSpecificOutput.additionalContext`，以便向 Claude 提供反馈并继续回合，而不被标记为 hook 错误
- **变更**：Skills：添加 `\$` 转义语法，以在命令体中在数字前包含字面量 `$`
- **变更**：在 `--resume` 时，stdio MCP servers 现在接收与 hooks/Bash 相同的 `CLAUDE_CODE_SESSION_ID`
- **修复**：当后台命令从不退出时，`claude -p` 在最终结果后永远挂起；现在 stdin 关闭后后台 shell 会在结果后约 5 秒停止
- **修复**：当 `CI=true` 且未设置 Anthropic API key 时，`claude -p` 在 Bedrock/Vertex/Foundry 上因 "ANTHROPIC_API_KEY required" 而失败
- **修复**：bazel 和受 EDR 保护的 Go 工作流下 Bash 命令失败：`$TMPDIR` 被对所有命令（而非仅 sandbox 命令）覆盖为 `/tmp/claude-{uid}`（自 2.1.154 起的回归）
- **修复**：在 OneDrive 内部或带只读属性时，Windows 上 Bash 命令在 session-env 目录因 "EEXIST: file already exists" 而失败
- **修复**：当托管设置获取在全新配置目录的启动期间完成时，组织托管的权限规则未应用
- **修复**：Claude Code 更新后重新附加时，后台会话丢失正在运行的后台任务
- **修复**：用 Esc 退出 agent 视图时的终端错位和数秒挂起
- **修复**：Hook `if: "Bash(...)"` 条件在每个包含 `$()` 或 `$VAR` 的 Bash 命令上触发

---

### v2.1.162 (2026-06-03)

> 更安静的启动、agents `waitingFor`、slash-command 填充、Windsurf 重命名为 Devin Desktop、25+ bug 修复。

- **新增**：`claude agents --json` 现在包含 `waitingFor`，显示一个等待中的会话被什么阻塞（例如权限提示）
- **新增**：`--tools`：现在显式列出 `Grep`/`Glob` 会在带嵌入式搜索的原生构建上提供专用的搜索工具
- **新增**：`/effort` 现在会确认你所选级别是否会作为新会话的默认值持久化
- **变更**：在自动补全菜单中点击 slash 命令会将其填入提示词，而非立即运行；按 Enter 运行
- **变更**：Remote Control 现在显示为持久的页脚药丸（带指向会话的链接），而非启动消息
- **变更**：随着编辑器更名，在 `/ide`、`/terminal-setup` 和 `/scroll-speed` 中将 Windsurf 重命名为 Devin Desktop
- **修复**：配置目录只读时的静默启动挂起；Claude Code 现在以内存中配置启动并浮现错误
- **修复**：`WebFetch` 权限规则未应用于内置预批准域名；显式的 `deny`/`ask`/`allow` 规则现在优先
- **修复**：Windows 权限规则从不匹配以反斜杠拼写的路径（`~\`、`\\server\share`）或大小写变体路径
- **修复**：低于 1000 ms 的 MCP 每服务器 `timeout` 值被向下取整到 1 秒看门狗，导致中止每次工具调用
- **修复**：LSP `workspaceSymbol` 操作返回无结果；现在接受 `query` 参数
- **修复**：`claude agents` 在宽终端上以 60-120 列截断实时状态文本；以 40 列截断会话名称
- **修复**：`claude agents` 在派发输入框和会话回复框中 Ctrl+V 粘贴图片无效
- **修复**：跨会话消息传递（`SendMessage`）在深层 `CLAUDE_CODE_TMPDIR` 或 `$TMPDIR` 路径下静默失效
- **改进**：更安静的启动：通知按严重程度分组，会话信息和公告每次启动共用一行
- **改进**：后台服务启动和 `claude update` 验证会等待端点安全扫描完成，而非在 5 秒后失败
- **移除**："Claude in Chrome enabled" 和 "marketplace installed" 启动消息；模型自动更新和 team-onboarding 提示现在显示为安静通知

---

### v2.1.161 (2026-06-02)

> OTEL 自定义维度、agents 视图中的 `done/total`、并行 tool-call 隔离、20+ bug 修复。

- **新增**：`OTEL_RESOURCE_ATTRIBUTES` 值作为标签包含在指标数据点上，用于自定义维度（团队、仓库）
- **新增**：当工作被扇出时，`claude agents` 行在详情前显示 `done/total`；peek 显示运行时间最长的项
- **新增**：`/mcp` 将你从未登录过的 claude.ai 连接器折叠在 "Show unused connectors" 行后面
- **变更**：并行工具调用：失败的 Bash 命令不再取消同一批次中的其他调用；每个工具独立返回自己的结果
- **改进**：Linux 上的全屏模式剪贴板在可用时使用 `wl-copy`/`xclip`/`xsel`；复制到剪贴板和 PRIMARY 选区以便中键粘贴
- **改进**：通过稳定布局引擎的 JIT 编译配置改进终端渲染性能；改进大文件写入的渲染性能
- **修复**：`/effort` 对话框、workflow 动画和提示词关键字微光未遵守 "Reduce motion" 设置
- **修复**：`forceLoginOrgUUID`/`forceLoginMethod` 托管设置策略阻止第三方提供商会话（2.1.146 中的回归）
- **修复**：后台 subagent 输出在 `--output-format text` 或 `json` 下损坏 `claude -p` 标准输出
- **修复**：`claude mcp` list/get/add 将密钥打印到终端；`${VAR}` 引用不再展开，凭据 header 和 URL 密钥被脱敏
- **修复**：后台会话中带 `isolation: "worktree"` 的 workflow agents 被阻止编辑其自己 worktree 内的文件
- **修复**：从 `claude agents` 派发的后台会话使用守护进程环境中的陈旧模型启动，而非 `settings.json`
- **修复**：在遥测初始化完成前发出的 OpenTelemetry 日志事件被丢弃
- **修复**：在最终确定结果时发生错误，已完成的 subagents 卡在显示为运行中
- **新增**：[VSCode] 建议禁用终端 GPU 加速（或运行 `/terminal-setup`）以修复乱码字形的提示

---

### v2.1.160 (2026-06-01)

> `ultracode` 取代 `workflow` 关键字、启动文件安全提示、grep 后 Edit、20+ bug 修复。

> **重大变更**：动态 workflow 触发关键字从 `workflow` 改为 `ultracode`。"workflow" 一词不再触发运行；用你自己的话请求仍然有效。触发关键字在提示词输入中以紫色高亮。

- **变更**：将动态 workflow 触发关键字从 `workflow` 重命名为 `ultracode`；提示词输入中的紫色微光；用你自己的话请求仍然有效
- **安全**：在写入 shell 启动文件（`.zshenv`、`.zlogin`、`.bash_login`）和 `~/.config/git/` 之前添加提示，否则可能导致意外的命令执行
- **安全**：`acceptEdits` 模式现在在写入授予代码执行权限的构建工具配置文件（`.npmrc`、`.yarnrc*`、`bunfig.toml`、`.bazelrc`、`.pre-commit-config.yaml`、`.devcontainer/`）之前会提示
- **改进**：用 `grep` 查看文件后，Edit 不再要求单独的 Read；单文件 `grep`/`egrep`/`fgrep` 命令现在满足 edit 前 read 检查
- **改进**：通过对常规操作降低推理，减少 auto 模式分类器延迟；减少 "could not evaluate this action" 阻塞
- **改进**：后台会话拆除在 SIGKILL 之前向正在运行的 shell 子进程发送 SIGTERM，以便清理处理程序运行
- **移除**：`CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE`（2.1.154 中弃用；现在为空操作）
- **移除**：启动时的 JetBrains 插件安装建议
- **修复**：20+ bug 修复：通过 PowerShell 互操作的 WSL 剪贴板、`claude agents` 中已完成会话丢失聊天历史、隔夜退役会话丢失对话、带非 ASCII 项目/分支名的语音模式、第三方提供商上的 auto 模式不可用消息、brief 模式恢复时过去回复消失、vim 模式 `p` 粘贴位置

---

### v2.1.159 (2026-05-31)

> 内部基础设施改进（无面向用户的变更）。

---

### v2.1.158 (2026-05-30)

> Bedrock、Vertex 和 Foundry 上 Opus 4.7/4.8 的 Auto 模式。

- **新增**：Auto 模式现已在 Bedrock、Vertex 和 Foundry 上对 Opus 4.7 和 Opus 4.8 可用；通过设置 `CLAUDE_CODE_ENABLE_AUTO_MODE=1` 选择加入

---

### v2.1.157 (2026-05-29)

> 从 `.claude/skills` 自动加载插件（无需 marketplace）、`claude plugin init`、会话中途切换 worktree、20+ bug 修复。

- **新增**：`.claude/skills` 目录中的插件现在会自动加载，无需 marketplace
- **新增**：`claude plugin init <name>` 直接在 `.claude/skills` 中搭建一个新插件
- **新增**：`/plugin` 参数的自动补全：子命令、已安装的插件名称以及来自已知 marketplace 的插件
- **新增**：`claude agents`：`settings.json` 中的 `agent` 字段现在对派发的会话生效；使用 `--agent <name>` 覆盖它
- **新增**：`EnterWorktree` 现在可以在会话中途切换 Claude 管理的 worktree 之间
- **新增**：当 `OTEL_LOG_TOOL_DETAILS=1` 时，`tool_decision` 遥测事件现在包含 `tool_parameters`（bash 命令、MCP/skill 名称）
- **改进**：在 agent 完成后，Claude 管理的 worktree 保持未锁定，以便 `git worktree remove`/`prune` 可以清理它们
- **改进**：由于消除了冗余的消息渲染重新计算，长对话和恢复的对话更快
- **改进**：`/terminal-setup` 现在禁用 VS Code/Cursor/Windsurf 集成终端中的 GPU 加速，以防止乱码文本渲染
- **修复**：通过粘贴、MCP 或对话框附加的无法处理的图片（零字节、损坏）不再使请求崩溃；它们变为文本占位符
- **修复**：桌面应用、IDE 扩展和 SDK 在 auto 和 bypass-permissions 模式下不再出现 sandbox 网络权限提示
- **修复**：`.claude/worktrees/` 下的后台 agent worktree 在 30 天作业保留清扫后不再被孤立
- **修复**：睡眠/唤醒后重新附加的后台会话现在向模型报告正确的日期
- **修复（回归 2.1.153）**：`claude agents` 中的选中即复制现在在带 `set-clipboard on` 的 tmux 内能到达系统剪贴板
- **修复**：`--resume` 现在报告在上一个 Claude Code 进程退出时正在运行的后台 subagents
- **修复**：`--worktree` 和 `--worktree --tmux` 现在返回到正确的链接 worktree，而非规范的仓库根目录
- **修复**：当选定模型已是其系列中最新时，`/model` 选择器不再显示错误的 "Newer version available" 提示
- **修复**：在 VS Code、Cursor 和 Windsurf 集成终端中右键粘贴不再重复剪贴板内容
- **修复（WSL）**：图片粘贴（`alt+v`）、Windows 11 上的截图粘贴以及从 Windows 资源管理器拖动图片现在能正常工作
- **修复**：若干 `claude agents` 问题：已完成会话未退役、按 Esc 未取消 "opening…"、托管设置对话框后终端冻结
- **修复**：字面量 markdown 标记（反引号、星号）不再出现在全屏模式下进行中的消息文本中

---

### v2.1.156 (2026-05-28)

> 热修复：Opus 4.8 因修改后的 thinking blocks 导致的 API 崩溃。

- **修复**：使用 Opus 4.8 时 thinking blocks 被修改，导致 API 错误的问题

---

### v2.1.154 (2026-05-28)

> Opus 4.8、编排数百个后台 agents 的动态 workflows、精简系统提示作为默认、30+ bug 修复。

- **新增（模型）**：Opus 4.8 已可用并默认为 high effort；对最难的任务使用 `/effort xhigh`
- **新增（模型）**：Opus 4.8 上的 Fast 模式，以标准费率的 2 倍换取 2.5 倍速度
- **新增**：动态 workflows：Claude 可以在一个会话中跨数十到数百个后台 agents 编排工作；运行 `/workflows` 监控运行情况
- **新增**：精简系统提示现在是除 Haiku、Sonnet 以及 Opus 4.7 及更早版本之外所有模型的默认
- **变更**：`/simplify` 现在运行仅清理的审查（复用、简化、效率、altitude）并应用修复，而非运行完整的 `/code-review --fix` bug 查找审查
- **变更**：`/effort` 滑块标签从 "Speed"/"Intelligence" 重命名为 "Faster"/"Smarter"
- **新增**：`claude agents`：输入 `! <command>` 以将 shell 命令作为可附加和分离的后台会话运行；也可通过 `claude --bg --exec '<command>'` 使用
- **新增**：`claude agents`：`/logout` 现在会将你登出，而非被发送到后台会话
- **新增**：用于打开 agents 视图的 `←←` 现在在 Bedrock、Vertex、Foundry 以及禁用遥测时也能工作
- **新增**：Chrome 中的 Claude：通过 `/chrome` → "Select browser…" 或在多个浏览器连接时在聊天中选择要使用的已连接浏览器
- **新增**：插件可以在 `plugin.json` 或 marketplace 条目中声明 `defaultEnabled: false`；通过 `/plugin` 或 `claude plugin enable` 启用
- **新增**：`/plugin` Discover 标签页将匹配当前目录的插件固定，并标注 "suggested for this directory"
- **新增**：流式工具执行始终启用，包括在 Bedrock/Vertex/Foundry 上（此前在功能标志后面）
- **新增**：Stdio MCP server 子进程在其环境中接收 `CLAUDE_CODE_SESSION_ID` 和 `CLAUDECODE=1`
- **新增**：`claude mcp list`/`get` 现在将未批准的 `.mcp.json` 服务器显示为 `⏸ Pending approval` 而非自动批准
- **改进**：Auto 模式分类器对数据外泄的检测得到改进，尤其是针对批量仓库传输
- **弃用**：`CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE`（2026-06-01 移除）；使用 `/model claude-opus-4-6[1m]` 然后 `/fast on`
- **修复（VSCode）**：在 Windows 上关闭 VS Code 时 Claude Code 进程未干净关闭
- **修复**：30+ 修复，包括守护进程退出后孤立的 `--bg-pty-host` 进程以 100% CPU 空转、选项对话框中分隔线下方的数字键快捷键不工作、从链接 worktree 内部派生 subagents 时 `worktree.baseRef: "head"` 解析到错误的 HEAD、来自 thinking 转圈颜色的 VS Code 间歇性渲染损坏、计划文件名包含 `[Image #N]`/`[Pasted text #N]` 占位符、短 ANSI 着色行上的幽灵展开提示、无效的 `allowedMcpServers`/`deniedMcpServers` 条目丢弃所有托管设置策略、设置了 `CLAUDE_CODE_ALWAYS_ENABLE_EFFORT` 时无 effort 参数的模型上的 API 400 错误、Windows 更新失败显示通用错误、安全分类器在推理时耗尽输出 token 时 auto 模式阻止操作
- **重大变更**：`CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` 已弃用（2026-06-01 移除）
- **重大变更**：`/simplify` 行为已变更：现在为仅清理审查，而非完整的 code-review 修复

---

### v2.1.153 (2026-05-28)

> `/model` 默认保存为默认（与 IDE 一致）、插件 marketplace 的 `skipLfs`、`claude agents` 自动补全改进、25+ bug 修复。

- **变更**：`/model` 现在将你的选择保存为新会话的默认（与 IDE 行为一致）；在选择器中按 `s` 仅切换当前会话，逆转了 2.1.144 中以仅会话为默认且 `d` 设置默认的行为
- **新增**：`github`/`git` 插件 marketplace 源的 `skipLfs` 选项，用于在克隆和更新期间跳过 Git LFS 下载
- **新增**：状态栏命令接收 `COLUMNS` 和 `LINES` 环境变量，以便脚本可根据终端宽度调整输出大小
- **新增**：`claude agents` 派发输入框自动补全现在建议原生 slash 命令和捆绑 skills，而不仅是项目 skills
- **新增**：`claude agents` PR 列对单个 PR 显示 `PR #N`，对多个显示 `N PRs`
- **新增**：`claude doctor` 显示你上次更新尝试的结果；当 npm 全局安装无法自动更新时显示一次性通知（`/doctor` 列出修复方法）
- **变更（macOS）**：后台 agents 现在在隐私与安全中显示为 "Claude Code"，在升级间保留权限授予
- **修复**：25+ 修复，包括没有可选 GET SSE 的有状态 MCP servers 重连循环（来自 2.1.147 的回归）、API gateway 收到用户的 Anthropic OAuth 凭据而非 gateway token、subagent `Agent` 工具 frontmatter MCP servers 忽略 `--strict-mcp-config`/企业托管策略、带 `subagent_type: 'claude'` 的 `Agent` 工具静默丢弃写入 gitignored 路径的输出、Windows PowerShell 安装程序在安装实际失败时报告成功、`claude update` 安装最新版而非配置的发布频道版本、按 transcript 文件路径恢复会话时占用过多内存、stdin 关闭但无 EOF 时 stream-json 模式挂起、格式错误的 `file://` 链接不可点击、`--help` 在窄终端上未换行、折叠视图中的 MCP 工具进度、`/bg` 响应在后台继续而非丢弃、多个后台会话修复（tmux 中的剪贴板/复制、/rename 即时更新、IME 候选窗口位置、256 色终端背景渗色、用 Remote Control 退出 `claude agents` 后的僵尸会话条目）、Windows 更新回滚恢复
- **重大变更**：`keybindings.json` 中 `modelPicker:setAsDefault` 键位重命名为 `modelPicker:thisSessionOnly`（`d` 动作被 `s` 取代）

---

### v2.1.152 (2026-05-27)

> `/code-review --fix`、skills 的 `disallowed-tools` frontmatter、`MessageDisplay` hook、移除 auto 模式选择加入、35+ bug 修复。

- **新增**：`/code-review --fix` 现在会在审查后将审查发现应用到你的工作树；`/simplify` 现在调用 `/code-review --fix`
- **新增**：Skills 和 slash 命令可以在 frontmatter 中设置 `disallowed-tools`，以在 skill 激活时从模型中移除工具
- **新增**：`/reload-skills` 命令重新扫描 skill 目录而无需重启会话
- **新增**：`SessionStart` hooks 可以返回 `reloadSkills: true` 以在同一会话中使新安装的 skills 可用，并可在启动和恢复时通过 `hookSpecificOutput.sessionTitle` 设置会话标题
- **新增**：`MessageDisplay` hook 事件让 hooks 在助手消息文本显示时对其进行转换或隐藏
- **新增**：`pluginSuggestionMarketplaces` 托管设置，以便管理员可以将其插件可通过上下文感知提示被建议的组织 marketplace 加入白名单
- **新增**：当找不到主模型时，`--fallback-model` 在会话剩余时间内切换到已配置的回退模型，而非使每个请求失败
- **新增（Vim）**：NORMAL 模式下的 `/` 打开反向历史搜索（类似 Ctrl+R），与 bash/zsh vi 模式行为一致
- **改进**：`/usage` 细分现在包含大型会话文件；文件以流式读取扫描，使内存使用保持平稳
- **改进**：折叠组中的 thinking 摘要至少保持可读 3 秒，渲染为 markdown，并限制在 10 行（Ctrl+O 显示完整 thinking）
- **改进**：全屏模式 "Thinking for Ns" 指示器在模型 thinking 时实时计数
- **变更**：Auto 模式不再要求选择加入同意
- **修复**：35+ 修复，包括长会话中终端样式退化、condensed 启动中缺少 sandbox 警告、跨工具调用的加载转圈状态、focus 模式虚假的隐藏消息计数、工具结果内点击链接折叠该部分、来自内联代码的 markdown 表格单元格边框颜色渗色、相同命令但不同环境变量的插件 MCP servers 被去重、陈旧 `enabledPlugins` 条目导致 `/doctor` 错误、插件 git 分支更新静默停止、远程 MCP servers 在出口代理下失败、无消息或相同有效 effort 时出现 effort 更改对话框、带 `--bare` 的 Agent 工具描述、陈旧权限提示取消后后台 worker 崩溃、API 使用嵌套细分时 `cache_creation_input_tokens` 报告为 0、SDK 托管会话中的 `PushNotification` 误报、模型/登录切换后卡住的会话在历史中留下陈旧的 thinking-block 签名

---

### v2.1.150 (2026-05-23)

> 内部基础设施改进——无面向用户的变更。

---

### v2.1.149 (2026-05-23)

> `/usage` 按类别细分、GFM 任务列表复选框、两项安全修复、20+ bug 修复。

- **新增**：`/usage` 现在按类别显示驱动你限额使用的因素细分——skills、subagents、plugins 以及每个 MCP server 的成本
- **新增**：Markdown 输出原生渲染 GFM 任务列表复选框（`- [ ] todo` / `- [x] done`）而非纯项目符号
- **新增（企业）**：`allowAllClaudeAiMcps` 托管设置，与 `managed-mcp.json` 一起加载 claude.ai 云端 MCP 连接器
- **安全**：修复 PowerShell 权限绕过——内置 `cd` 函数（`cd..`、`cd\`、`cd~`、`X:`）在未被检测的情况下更改工作目录，让后续命令读取工作区之外的内容
- **安全**：git worktree 中的 sandbox 写入白名单覆盖了整个主仓库根目录，而非仅共享的 `.git` 目录（其中 `hooks/` 和 `config` 被拒绝）
- **修复**：现在可以用键盘（方向键、`j`/`k`、`PgUp`/`PgDn`、`Space`、`Home`/`End`）滚动 `/diff` 详情视图
- **修复**：PowerShell 前缀/通配符 allow 规则（例如 `PowerShell(dotnet.exe build *)`）现在预批准原生可执行文件和脚本
- **修复**：权限分析漏洞，解析器在 `cd`/`pushd`/`popd` 间为 `PWD`/`OLDPWD`/`DIRSTACK` 信任陈旧的变量追踪值
- **修复**：Bash 工具中的 `find` 在大型目录树上耗尽 macOS 系统文件/vnode 表
- **修复**：在启动时接受后，托管设置批准对话框使终端冻结
- **修复**：当工作树没有真实更改时，`/ultraplan` 和远程会话创建因 "Could not capture uncommitted changes" 而失败
- **修复**：当脚本路径包含空格时，`otelHeadersHelper` 静默失败；失败现在在 `/doctor` 和调试日志中报告
- **修复**：thinking 转圈在跨工具调用和进入新的 thinking 突发时保持琥珀色
- **修复**：折叠的 Bash 输出对带许多短行的输出报告错误的隐藏行数
- **修复**：当提示溢出输入框时，slash-command 参数提示截断尾部已输入字符
- **修复**：在 Tab 补全其 frontmatter `name:` 与目录基本名不同的 skill 后，参数提示和渐进式参数建议未出现
- **修复**：状态栏显示用户的基线 `/effort` 设置，而非由 skill/agent `effort:` frontmatter 应用的 effort 级别
- **修复**：Ctrl+O transcript 视图在打开的那一刻冻结，而非跟踪新消息
- **修复**：编辑召回的提示历史条目在进一步上/下导航时丢失编辑
- **修复**：切换无关设置时，`/config` 退出摘要报告对 auto-compact 和主题的幽灵更改
- **修复**：当缓存的会话元数据文件缺少可选字段时 `/insights` 崩溃
- **修复**：从 claude.ai 或 Claude 移动应用重命名 Remote Control 会话不更新 `claude --resume` 的本地会话名
- **修复**：刚提交的提示可能在上方向键历史中出现两次的竞态
- **修复**：全屏模式中的 "Jump to bottom" 药丸在点击后未立即消失
- **改进**：`/feedback` 报告现在包含 context compaction 之前的对话，使长会话中较早出现的问题更易分类

---

### v2.1.148 (2026-05-22)

> 热修复：来自 2.1.147 的 Bash 工具退出码 127 回归。

- **修复**：Bash 工具在每个命令上返回退出码 127（2.1.147 中引入的回归）

---

### v2.1.147 (2026-05-22)

> 固定的后台会话（Ctrl+T）、用于内联 GitHub PR 评论的 /code-review --comment、改进的自动更新器、30+ bug 修复。

- **新增**：固定的后台会话——`claude agents` 中的 `Ctrl+T` 固定一个会话，使其在空闲时保持存活、就地自动重启以应用 CC 更新，且仅在非固定会话之后才在内存压力下被释放
- **新增**：`/code-review --comment`——将发现作为内联 GitHub PR 评论发布
- **改进**：自动更新器现在重试瞬时网络故障，在失败时报告具体错误类别和 OS 错误码，并在更新失败时显示当前版本
- **修复**：提示历史不再记录连续的重复条目
- **修复**：`PowerShell(git push*)` 这类 Hook `if` 条件现在正确匹配（此前仅 `PowerShell(*)` 有效）
- **修复**：粘贴的文本现在作为实际内容传递，而非 `[Pasted text #N]` 占位符
- **修复**：当路径与默认目录重叠时，`claude plugin details` 和 `/plugin` 中的插件组件计数翻倍
- **修复**：后接 tab 或换行的 slash 命令不再被视为未知命令
- **修复**：Shell 快照不再丢弃名称以单个下划线开头的用户函数
- **修复**：在 `tools:` frontmatter 中声明多个 `Agent(...)` 类型的插件 agents 现在保留所有条目
- **修复**：PowerShell 工具不再为依赖默认格式化器的命令丢弃输出
- **修复**：Windows 对 PowerShell 脚本调用的 "Yes, and don't ask again" 现在写入一条在后续运行中匹配的规则
- **修复**：流式传输时 Windows Terminal 中附加的后台会话的全屏闪烁
- **修复**：在 Windows 上，移除后台作业 worktree 不再通过 NTFS 联接进入主仓库
- **修复**：`/effort` 滑块现在在当前 effort 级别打开（此前总是从错误级别开始）
- **修复**：`/plugin`、`/status`、`/mobile`、`/sandbox`、`/permissions` 菜单中的若干间距和布局故障
- **修复**：10+ 额外修复：Windows 上 CJK 的 agent 视图中陈旧/翻倍行、被剥离的图片提示反复重读、Windows 上罕见的滚动稳定挂起、`!` 命令输出中的 `&amp;`、未知 slash 命令现在在 headless/SDK 模式下显示错误、小终端上的 `/help` 渲染

---

### v2.1.146 (2026-05-21)

> /code-review 命令（从 /simplify 重命名）、auto 模式恢复 AskUserQuestion、15+ bug 修复。

- **变更**：`/simplify` 重命名为 `/code-review`，带可选 effort 级别（例如 `/code-review high`）
- **修复**：当用户或 skill 显式依赖 `AskUserQuestion` 时，auto 模式不再抑制它
- **修复**：当 `pwsh` 通过 winget 或 Microsoft Store 安装时，Windows PowerShell 工具因 "command line is invalid" 而失败（v2.1.124 中的回归）
- **修复**：MCP `resources/list`、`resources/templates/list` 和 `prompts/list` 现在在分页服务器上返回所有页
- **修复**：`/background` 不再拒绝其唯一输入是 skill 或自定义 slash 命令的会话
- **修复**：后台会话不再为已用 "don't ask again" 授予的工具权限重新提示
- **修复**：`/theme` 颜色编辑器和 "New custom theme" 对话框现在响应 Esc
- **修复**：`CLAUDE_CODE_SUBAGENT_MODEL` 现在在多 agent 会话中转发给子进程
- **修复**：`forceLoginOrgUUID` 和 `forceLoginMethod` 托管设置策略对第三方提供商和 API-key 会话强制执行
- **修复**：10+ 额外修复：Windows GNOME Terminal 粘贴、后台守护进程派生回退、Windows 后台会话 worktree 移除、流式传输结束时 Agent SDK 未捕获异常、大文件编辑的 diff 渲染性能

---

### v2.1.145 (2026-05-20)

> 用于脚本编写的 claude agents --json、安装前的 /plugin 预览、标签标题显示等待输入计数、Bash 权限提示绕过安全修复、20+ bug 修复。

- **新增**：`claude agents --json`——将所有活动的 Claude 会话列为 JSON 以便脚本编写（tmux-resurrect、状态栏、会话选择器）
- **新增**：为 `claude_code.tool` OTEL spans 添加 `agent_id` 和 `parent_agent_id` 属性；后台 subagent spans 现在嵌套在派发的 Agent 工具 span 下
- **新增**：`/plugin` Discover 和 Browse 屏幕现在在安装前预览插件的 commands、agents、skills、hooks 以及 MCP/LSP servers
- **新增**：`claude agents` 终端标签标题显示等待输入计数，以便切换走的窗口在 agent 需要关注时给出指示
- **新增**：slash 命令和 @ 提及建议列表在全屏模式下支持鼠标悬停和点击
- **新增**：Stop 和 SubagentStop hook 输入现在包含 `background_tasks` 和 `session_crons` 字段
- **新增**：检测到时，状态栏 JSON 输入现在包含 GitHub 仓库和 PR 信息
- **安全**：修复权限提示绕过，其中 Bash 命令中对非白名单环境变量的裸赋值被自动批准
- **修复**：MCP 分页的 `resources/list`、`resources/templates/list` 和 `prompts/list` 丢弃第 1 页之后的项
- **修复**：MCP prompt slash 命令现在显示缺失的参数名和预期用法，而非原始服务器校验错误
- **修复**：当整文件读取超出 token 限制时，Read 工具现在返回带 "PARTIAL view" 通知的截断首页，而非硬错误
- **修复**：一次创建多个任务时，任务列表不再以随机顺序渲染
- **修复**：带非 ASCII 名称的 Agent Teams 队友不再使每次 API 调用失败（无效的 header 编码）
- **修复**：`/review` 不再在带 Classic Projects 的仓库上报错（移除了已弃用的 `projectCards` GraphQL 查询）
- **修复**：`claude plugin validate` 现在标记指向文件而非目录的 `skills:` 条目
- **修复**：带 `context: fork` 的 skill 不再在无限循环中反复重新调用自身

---

### v2.1.144 (2026-05-19)

> /resume 列出后台会话、/model 仅限当前会话（按 d 设为默认）、usage credits 重命名、修复 75 秒启动卡顿、终端渲染修复、40 多个 bug 修复。

- **New**: `/resume` 现在会将通过 `claude --bg` 或 agent 视图启动的后台会话与交互式会话一并列出，并标记为 `bg`
- **New**: 后台 subagent 完成通知中显示已耗时长（例如 "Agent completed · 3h 2m 5s"）
- **Changed**: `/model` 现在只更改当前会话的模型——在选择器中按 `d` 可为新会话设置默认模型
- **Changed**: CLI 文案中 "extra usage" 重命名为 "usage credits"；`/extra-usage` 现为 `/usage-credits`（旧名称仍可用）
- **Fixed**: 当 `api.anthropic.com` 不可达时，启动不再卡顿长达 75 秒——旁路 API 调用现在 15 秒后超时
- **Fixed**: 终端渲染损坏在错过窗口缩放事件时可自愈；长会话中的渐进式故障已清除；VS Code 加载动画使用更少颜色以减少故障
- **Fixed**: macOS 后台会话在受完全磁盘访问保护的文件夹下因 "exit 1 before init" 崩溃（2.1.143 引入的回归）
- **Fixed**: 带分页 `tools/list` 的 MCP 服务器现在返回所有页面（此前会静默丢弃第 1 页之后的工具）
- **Fixed**: skill 目录中的文件描述符耗尽——非 `.md` 文件不再触发 skill 重新加载
- **Fixed**: 另有 40 多个修复：worktree 进入后的 `/branch`、AskUserQuestion 备注字段中的 Escape、Bedrock/Vertex Opus 1M 上下文选择器、带 `forceLoginMethod` 的远程登录、Windows 上的后台会话滚动等

---

### v2.1.143 (2026-05-16)

> 插件依赖强制约束、/plugin marketplace 中的预计上下文成本、worktree.bgIsolation: "none"、PowerShell 默认 -ExecutionPolicy Bypass、stop hook 阻塞上限、30 多个 bug 修复。

- **New**: 插件依赖强制约束——当另一个已启用插件依赖目标插件时，`claude plugin disable` 会拒绝执行，并给出可复制粘贴的禁用链提示；`claude plugin enable` 会强制启用传递依赖
- **New**: `/plugin` marketplace 浏览面板中显示预计上下文成本（每轮和每次调用的 token 估算）
- **New**: `worktree.bgIsolation: "none"` 设置——让后台会话无需 `EnterWorktree` 即可直接编辑工作副本（适用于 worktree 不切实际的仓库）
- **New**: PowerShell 工具现在默认传入 `-ExecutionPolicy Bypass`——可通过 `CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY=1` 退出
- **Improved**: 后台会话从空闲唤醒后现在保留所设的模型和 effort 等级
- **Improved**: 附加 agent 会话中的 Shift+Tab 现在在循环中包含 auto 模式
- **Fixed**: 反复阻塞的 Stop hook 不再无限循环——连续 8 次阻塞后该轮结束并显示警告（可通过 `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` 覆盖）
- **Fixed**: 在 Claude 于迭代之间空闲时，Esc/Ctrl+C 现在可取消待执行的 `/loop` 唤醒
- **Fixed**: 当后台 shell 或委派的 subagent 仍在运行时，`/goal` 评估器不再触发
- **Fixed**: `settings.json` env 中的 `NO_COLOR`/`FORCE_COLOR` 现在只应用于子进程（不再剥离 Claude Code 自身的 UI 颜色）
- **Fixed**: `claude agents --allow-dangerously-skip-permissions` 现在让 bypass 模式在权限循环中可用（此前会错误地将会话默认设为 bypass 模式）
- **Fixed**: 另有 20 多个修复：退役/唤醒后的后台会话模型+effort 保留、网络驱动器工作目录下的 Windows 事件循环、`claude --bg --dangerously-skip-permissions` 跨退役/唤醒持续保留、256 色终端上的后台颜色渗透、Windows Terminal 上的陈旧片段渲染

---

### v2.1.142 (2026-05-15)

> Fast mode 默认升级至 Opus 4.7、新增 claude agents 派发标志、根级 SKILL.md 插件支持、/plugin 显示 LSP 服务器、MCP_TOOL_TIMEOUT 修复、25 多个 bug 修复。

- **New**: Fast mode 现在默认使用 **Opus 4.7**（此前为 Opus 4.6）——设置 `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE=1` 可固定为 Opus 4.6
- **New**: `claude agents` 新增派发标志：`--add-dir`、`--settings`、`--mcp-config`、`--plugin-dir`、`--permission-mode`、`--model`、`--effort` 和 `--dangerously-skip-permissions`，用于配置后台会话
- **New**: 拥有根级 `SKILL.md` 而无 `skills/` 子目录的插件现在会被自动呈现为一个 skill
- **New**: `/plugin` 详情面板和 `claude plugin details` 现在显示插件提供的 LSP 服务器
- **New**: `/web-setup` 在替换现有 GitHub App 连接前会发出警告
- **Fixed**: `MCP_TOOL_TIMEOUT` 现在能正确提高远程 HTTP 和 SSE MCP 服务器的每请求获取超时（此前无论配置值如何都被限制在 60 秒）
- **Fixed**: 后台会话现在能识别已存在的 git worktree（此前在 `EnterWorktree` 拒绝创建重复时会阻塞 Edit）
- **Fixed**: 守护进程现在在二进制升级（例如 `brew upgrade`）后干净退出——此前会导致已派发的 agent 在被删除路径上崩溃循环
- **Fixed**: 当 Claude-in-Chrome 扩展在没有共享标签页的情况下连接时，后台 agent 不再崩溃循环
- **Fixed**: 在附加的 `claude agents` 会话中点击链接——附加期间不再应用无头浏览器垫片
- **Fixed**: `claude agents` 的 "v 以在编辑器中打开" 现在使用你 shell 的 `$EDITOR`/`$VISUAL`，而非守护进程的默认编辑器
- **Fixed**: 网络驱动器工作目录下 Windows 上的 `claude agents` 死锁；Ctrl+C 现在在启动期间可用
- **Fixed**: `claude --bg --dangerously-skip-permissions` 现在跨退役/唤醒持续保留
- **Fixed**: 使用 `skills: ["./"]` 的插件不再显示错误的 "path escapes plugin directory" 报错
- **Fixed**: 当没有安装元数据时，插件缓存清理不再删除处于活动状态的插件版本目录
- **Improved**: 响应式 compaction：首次摘要尝试以原始请求的溢出大小为种子，避免接近满上下文的无效重试
- **Improved**: Hook 配置错误：为 `SessionStart`/`Setup`/`SubagentStart` 配置 prompt 型或 agent 型 hook 时，现在显示清晰的 "use a command-type hook instead" 消息

---

### v2.1.141 (2026-05-14)

> Hook terminalSequence 输出字段、claude agents --cwd、Rewind "Summarize up to here"、50 多个 bug 修复。

- **New**: JSON 输出中的 Hook `terminalSequence` 字段——无需控制终端即可从 hook 发出桌面通知、窗口标题和提示音
- **New**: `CLAUDE_CODE_PLUGIN_PREFER_HTTPS`——通过 HTTPS 而非 SSH 克隆 GitHub 插件源（适用于没有 GitHub SSH 密钥的环境）
- **New**: 用于工作负载身份联合的 `ANTHROPIC_WORKSPACE_ID` 环境变量——将所铸造的 token 限定到特定工作区
- **New**: `claude agents --cwd <path>`——将会话列表限定到特定目录
- **New**: `/feedback` 现在可包含近期会话（最近 24 小时或 7 天），用于跨多个会话的问题
- **New**: Rewind 菜单："Summarize up to here"——压缩较早的上下文，同时保持近期轮次完整
- **Improved**: Auto 模式权限对话框现在会说明何时是某条 `permissions.ask` 规则导致了提示
- **Improved**: 连接 IDE 时，文件编辑权限提示上恢复了 "View diff in your IDE" 选项
- **Improved**: 通过 `/bg` 或 `←←` 启动的后台 agent 现在保留当前权限模式，而非恢复为默认
- **Improved**: `claude agents`——完成工作但留有后台 shell 运行的 agent 现在移至 Completed
- **Improved**: 加载动画在 10 秒后转为琥珀色，以示意 Claude 在长时间思考期间仍在工作
- **Improved**: 插件菜单导航——`→`/Tab 切换标签页，`↑` 移至标签栏，标签页头和搜索框在全屏下可点击
- **Fixed**: Bedrock 的 `awsCredentialExport` 现在在配置时始终运行（此前在环境 AWS 凭证已解析时会被跳过），修复跨账户访问
- **Fixed**: 配置变量未设置的插件 MCP 服务器现在显示带修复提示的 "config issue" 消息，而非通用连接失败
- **Fixed**: 连接时返回 403 的 MCP HTTP/SSE 服务器现在显示 "needs auth" 而非 "failed"
- **Fixed**: 当可选的服务器事件流重连失败时，远程 MCP 服务器不再不必要地断开——工具调用通过 POST 继续
- **Fixed**: 当 worker 会话 token 在会话中途轮换时，Remote Control MCP 连接器以 401 失败
- **Fixed**: 当服务器拒绝陈旧 token 时，Remote Control 不再重新登记受信任设备——会正确地循环执行 `/login`
- **Fixed**: 另有 40 多个修复：markdown 表格单元格换行回归、vim INSERT/VISUAL 模式下的 Ctrl+C、`chat:submit` 的备用键绑定、`voice:pushToTalk` 自定义键绑定、Windows Alt+V 图像粘贴、运行中后台 shell 下的 `/tui`、`/model` 更改其他会话的 autocompact 阈值、鼠标点击后的 transcript 视图字母快捷键

---

### v2.1.140 (2026-05-13)

> Agent 工具 subagent_type 大小写不敏感匹配、插件文件夹警告、定向 bug 修复。

- **Improved**: `Agent` 工具的 `subagent_type` 匹配现在对大小写和分隔符不敏感——`"Code Reviewer"` 解析为 `code-reviewer`，`"backend_architect"` 解析为 `backend-architect`
- **Improved**: 更新了 agent 颜色调色板
- **Improved**: 当默认组件文件夹（例如 `commands/`）因 `plugin.json` 设置了匹配键而被静默忽略时，插件现在会发出警告——显示于 `/doctor`、`claude plugin list` 和 `/plugin` 中
- **Fixed**: 当设置了 `disableAllHooks` 或 `allowManagedHooksOnly` 时 `/goal` 静默挂起——现在显示清晰消息
- **Fixed**: 符号链接设置热重载回归——符号链接文件会导致变更事件归因错误以及虚假的 `ConfigChange` hook
- **Fixed**: 当后台服务即将空闲退出时，`claude --bg` 以 "connection dropped mid-request" 失败
- **Fixed**: 启用企业端点安全的机器上后台服务启动失败（现在允许更多启动时间）
- **Fixed**: 远程托管设置在 401 时不重试——现在用强制刷新的 token 重试一次
- **Fixed**: 托管的 `extraKnownMarketplaces` 自动更新策略未被持久化到 `known_marketplaces.json`
- **Fixed**: `/loop` 为已在完成时发出通知的后台任务调度冗余唤醒以进行轮询
- **Fixed**: 当缺失可执行文件（例如 `gh`）在每次检查时触发同步 `where.exe` 重新生成时，Windows 事件循环停滞
- **Fixed**: 当 `offset` 以带空白填充或 `+` 前缀的字符串传入时，`Read` 工具调用验证失败
- **Fixed**: 终端失去焦点时原生终端光标未停留在输入插入符处

---

### v2.1.139 (2026-05-12)

> Agent 视图（Research Preview）、/goal 命令、hook exec 形式 + continueOnBlock、40 多个 bug 修复。

- **New**: Agent 视图（Research Preview）——`claude agents` 打开一个包含所有会话（运行中、等待你处理或已完成）的单一列表。每行显示会话状态、最近响应预览以及距上次交互的时间。从任意会话按左箭头进入导航，或直接从终端启动。选择一个会话即可窥视上一轮内容并就地回复而无需完全附加；按 Enter 附加。用 `/bg` 将任意会话置于后台，或用 `claude --bg [task]` 直接在后台启动。在 Pro、Max、Team、Enterprise 和 API 套餐上可用。
- **New**: `/goal` 命令——设定一个完成条件；Claude 跨轮次持续工作直至满足，并配有实时已耗时/轮次/token 浮层面板
- **New**: `/scroll-speed` 命令，用实时预览调整鼠标滚轮滚动速度
- **New**: `claude plugin details <name>`——显示插件组件清单和预计每会话 token 成本
- **New**: Transcript 视图导航：`?` 查看快捷键，`{`/`}` 在用户 prompt 之间跳转，`v` 切换快捷键面板
- **New**: Hook `args: string[]` 字段（exec 形式）——直接生成命令而无需 shell，路径占位符无需引号
- **New**: 用于 `PostToolUse` 的 Hook `continueOnBlock` 配置选项——设为 `true` 可将拒绝原因反馈给 Claude 并继续该轮
- **New**: MCP stdio 服务器现在在环境中接收 `CLAUDE_PROJECT_DIR`；插件配置可在命令中引用 `${CLAUDE_PROJECT_DIR}`
- **Improved**: Compaction prompt 现在要求模型保留敏感的用户指令
- **Fixed**: `/mcp` Reconnect 无需重启即可拾取 `.mcp.json` 编辑；重连失败时显示 HTTP 状态 + URL
- **Fixed**: 过期凭证 + `forceRemoteSettingsRefresh` 阻塞 `claude auth login/logout/status` 的死锁
- **Fixed**: `autoAllowBashIfSandboxed` 未自动批准带有 `$VAR` 和 `$(cmd)` 等 shell 展开的命令
- **Fixed**: 无限制的 MCP SSE 内存增长——响应体现在限制为每个 SSE 帧 16 MB
- **Fixed**: `Skill(name *)` 通配符权限规则现在按前缀匹配工作（与 `Bash(ls *)` 行为一致）
- **Fixed**: 设置热重载未检测到对符号链接 `~/.claude/settings.json` 的编辑
- **Fixed**: 另有 30 多个修复：hook 终端损坏、插件依赖陈旧计数、Cursor/VS Code 中的鼠标滚轮速度、自动补全中来自已断开服务器的 MCP 资源、CJK/emoji 边框溢出、bash 历史上箭头、多图像粘贴

---

### v2.1.138 (2026-05-11)

> 内部修复。

- **Fixed**: 内部修复（无用户可见变更）

---

### v2.1.137 (2026-05-11)

> [VSCode] 修复扩展在 Windows 上无法激活。

- **Fixed**: VS Code 扩展在 Windows 上无法激活

---

### v2.1.136 (2026-05-11)

> settings.autoMode.hard_deny、CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL、MCP /clear 消失修复、40 多个 UI/终端 bug 修复。

- **New**: `settings.autoMode.hard_deny`——无论用户意图或 allow 例外如何都无条件阻止的 auto 模式分类器规则
- **New**: `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL`，用于为通过 OpenTelemetry 捕获响应的企业重新启用会话质量调查
- **Fixed**: 在 VS Code 扩展、JetBrains 插件和 Agent SDK 中，MCP 服务器（`.mcp.json`、插件、claude.ai 连接器）在 `/clear` 后静默消失
- **Fixed**: 多个服务器并发刷新时丢失 MCP OAuth 刷新 token——多服务器设置不再每日重新认证
- **Fixed**: 罕见的登录循环，其中并发凭证写入可能覆盖刚刚轮换的 OAuth token 并强制重新登录
- **Fixed**: 扩展思考在工具调用后发出已编辑思考块时的 API 错误（400）
- **Fixed**: 当项目路径包含下划线时，`--resume` / `--continue` 找不到会话
- **Fixed**: 当存在匹配的 `Edit(...)` allow 规则时，plan 模式未阻止文件写入
- **Fixed**: WSL2：当 xclip/wl-paste 无法读取图像数据时，从 Windows 剪贴板粘贴图像现在通过 PowerShell 回退生效
- **Fixed**: 当缓存清理删除仍在使用的版本时，插件 `Stop`/`UserPromptSubmit` hook 失败
- **Improved**: 跨 slash 命令对话框的视觉一致性——标准化页脚提示、间距、箭头键样式；对话框边框在加载期间立即出现
- **Fixed**: bash 命令输出和 markdown 代码块中颜色出现在错误位置
- **Fixed**: ReasonML diff 在词级 diff 边界处渲染损坏的 "undefined" 文本伪影
- **Fixed**: `@` 文件选择器未匹配会话中途创建的文件，且未在含 100+ 条目的目录中找到文件
- **Fixed**: 另有 30 多个 UI/终端修复：失败的工具调用在全屏中展开、Backspace/Ctrl+Backspace 互换修复、`/usage` 每周重置日期显示、CJK 终端溢出、`/insights` 在格式错误工具调用上崩溃、可折叠性变更时渲染器崩溃、shell 集成锁文件未遵循 `CLAUDE_CONFIG_DIR`、复制输出中的尾随空白、插件卸载大小写不敏感性、`AskUserQuestion` 多选数组修复、`CronList` 缺失限定符、内容块返回时 MCP 工具结果不可见

---

### v2.1.133 (2026-05-08)

> worktree.baseRef 设置、hook 中的 effort 等级、subagent skills 修复、15 多个 bug 修复。

> **Breaking**: `worktree.baseRef` 默认为 `fresh`（从 `origin/<default>` 分支），逆转了 2.1.128 中 `EnterWorktree` 使用本地 HEAD 的行为。在设置中设为 `worktree.baseRef: "head"` 可恢复先前行为。

- **New**: `worktree.baseRef` 设置（`fresh` | `head`）——`fresh`（默认）从 `origin/<default-branch>` 分支；`head` 保留包含未推送提交的本地 HEAD。适用于 `--worktree`、`EnterWorktree` 和 agent 隔离 worktree
- **New**: `sandbox.bwrapPath` / `sandbox.socatPath` 托管设置（Linux/WSL），用于指定自定义 bubblewrap 和 socat 二进制位置
- **New**: `parentSettingsBehavior` 管理员层级键（`first-wins` | `merge`），让管理员可让 SDK `managedSettings` 加入策略合并
- **New**: Hook 通过 `effort.level` JSON 字段和 Bash 子命令中的 `$CLAUDE_EFFORT` env 变量接收活动 effort 等级
- **Improved**: Focus 模式行为和内存使用（后台 worker 在内存压力下被释放）
- **Fixed**: Subagent 未通过 Skill 工具发现项目/用户/插件 skill
- **Fixed**: 刷新 token 竞争清除共享凭证后，并行会话在 401 处陷入死胡同
- **Fixed**: 完整 MCP OAuth 流程（发现、客户端注册、token 交换、刷新）未遵循 `HTTP(S)_PROXY` / `NO_PROXY` / mTLS
- **Fixed**: 通过 `--add-dir` / SDK `additionalDirectories` 在映射网络驱动器上 Read/Write/Edit 被拒绝
- **Fixed**: 来自 claude.ai 的 Remote Control stop/interrupt 未完全取消 CLI 会话（中断卡住的工具后排队消息停滞）
- **Fixed**: 一个会话中的 `/effort` 意外更改其他并发会话的 effort 等级
- **Fixed**: `claude --help` 现在列出 `--remote-control` 标志
- **Fixed**: VS Code 扩展：当扩展构建未捆绑 Claude 二进制时，`claudeCode.claudeProcessWrapper` 以 "Unsupported platform" 失败

---

### v2.1.132 (2026-05-08)

> Bash env 中的 CLAUDE_CODE_SESSION_ID、CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN 退出选项、MCP 内存修复、20 多个终端/TUI 修复。

- **New**: `CLAUDE_CODE_SESSION_ID` env 变量现在传入 Bash 工具子进程环境（与 hook JSON 输入中的 `session_id` 匹配）
- **New**: `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` 退出全屏备用屏幕渲染器，将输出保留在终端的原生回滚缓冲区中
- **New**: 在通过 Ctrl+V 从剪贴板读取图像粘贴时显示 "Pasting…" 页脚提示
- **Fixed**: 当 stdio MCP 服务器向 stdout 写入非协议数据时无限制的内存增长（10GB+ RSS）
- **Fixed**: 外部 SIGINT（`kill -INT`、IDE 停止按钮）未运行优雅关闭——现在恢复终端模式并打印 `--resume` 提示
- **Fixed**: 当工具错误截断分割了 emoji 时，`--resume` 以 `no low surrogate in string` 失败；预损坏的会话在加载时被净化
- **Fixed**: 用 `-p --continue`/`--resume` 恢复 plan 模式会话时 `--permission-mode` 标志被忽略；同一会话内 `ExitPlanMode` 后 plan 模式未重新应用
- **Fixed**: 笔记本休眠/唤醒或 Ctrl+Z/`fg` 后全屏模式显示空白屏幕，直到下一次按键
- **Fixed**: 在 Ctrl+E/A/K/U/箭头键时，对于跨行换行的印度语合字或 ZWJ emoji，光标落在字素中间
- **Fixed**: Vim 操作符用分解（NFD）重音字符损坏文本
- **Fixed**: 粘贴以 `/` 开头的文本静默吞没输入或触发未知命令回复
- **Fixed**: 当焦点事件或鼠标跟踪报告与括号粘贴交错时，prompt 中出现杂散转义序列
- **Fixed**: Cursor 和 VS Code 1.92–1.104 中鼠标滚轮滚动过快（上游 xterm.js bug）；JetBrains IDE 2025.2 中滚轮失控
- **Fixed**: 在 Linux/X11 上将统计截图复制到剪贴板时 `/usage` Ctrl+S 挂起
- **Fixed**: `/terminal-setup` 在 Windows Terminal 中显示矛盾错误（Shift+Enter 已原生支持）
- **Fixed**: `/effort` 选择器未反映 `CLAUDE_CODE_EFFORT_LEVEL` env 变量覆盖
- **Fixed**: 部分用户的 `/status` 显示错误的默认模型
- **Fixed**: Slash 命令自动补全弹窗封顶在约 3–5 个可见命令，而非随终端高度扩展
- **Fixed**: 状态栏 `context_window` token 计数显示累积会话总量，而非当前上下文使用量
- **Fixed**: 未启用 "Option as Meta" 时 Alt+T（思考切换）在 macOS 上不工作（iTerm2、Terminal.app 默认值）
- **Fixed**: 从 `claude agents` 重新打开后台会话后 Windows 上键盘输入失效
- **Fixed**: MCP 服务器 `tools/list` 失败时静默显示 0 个工具——现在重试一次并在 `/mcp` 中显示 "connected · tools fetch failed"
- **Fixed**: 未授权的 claude.ai MCP 连接器显示为 "failed" 而非 "needs auth"；无头 `-p` 模式不再重试非瞬时 4xx 失败
- **Fixed**: 设置 `ENABLE_PROMPT_CACHING_1H` 时 Bedrock 和 Vertex 的 400 错误

---

### v2.1.131 (2026-05-06)

> VS Code 扩展 Windows 激活修复、Mantle 认证修复。

- **Fixed**: VS Code 扩展因捆绑 SDK 中硬编码的构建路径而在 Windows 上无法激活（`createRequire` polyfill bug）
- **Fixed**: Mantle 端点认证因缺失 `x-api-key` 头而失败

---

### v2.1.129 (2026-05-06)

> --plugin-url 标志、CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE、Ctrl+R 全项目历史恢复、skillOverrides 修复、20 多个 bug 修复。

- **New**: `--plugin-url <url>` 标志，用于从 URL 获取插件 `.zip` 归档供当前会话使用
- **New**: `CLAUDE_CODE_FORCE_SYNC_OUTPUT=1` env 变量，用于在自动检测失败的终端上强制启用同步输出（例如 Emacs `eat`）
- **New**: `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE`：设置后，Homebrew 或 WinGet 安装会在后台运行升级命令并提示重启
- **Changed**: 插件清单 `themes` 和 `monitors` 声明现在应放在 `"experimental": { ... }` 下——顶层仍可用但 `claude plugin validate` 会警告
- **Changed**: 网关 `/v1/models` 发现现在通过 `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` 选择性启用（2.1.126–2.1.128 中为自动）
- **Improved**: Ctrl+R 历史选择器再次默认为所有项目（2.1.124 之前的行为）——按 Ctrl+S 缩窄到当前项目或会话
- **Improved**: 第三方部署（Bedrock、Vertex、Foundry、`ANTHROPIC_BASE_URL` 网关）不再看到指向第一方 Anthropic 界面的加载动画提示
- **Fixed**: `skillOverrides` 设置现在生效：`off` 对模型和 `/` 隐藏，`user-invocable-only` 仅对模型隐藏，`name-only` 折叠描述
- **Fixed**: `claude_code.pull_request.count` OTel 指标现在统计通过 MCP 工具创建的 PR/MR（不仅是 shell 命令）
- **Fixed**: 策略拒绝错误消息现在包含 API Request ID，便于支持调试
- **Fixed**: 带无法识别 400 状态码的 API 错误显示原始 JSON 而非底层错误消息
- **Fixed**: `/clear` 未在对话后重置终端标签页标题
- **Fixed**: 当权限或其他对话框处于活动状态时，来自 `/rename` 的会话标题徽标消失
- **Fixed**: subagent 运行时 prompt 下方的 agent 面板被隐藏（2.1.122 引入的回归）
- **Fixed**: 外部编辑器交接（Ctrl+G）清空 prompt 上方的对话历史
- **Fixed**: `/context` 将其渲染的 ASCII 可视化网格转储到对话中（每次调用浪费约 1.6k token）
- **Fixed**: `/agents` Library 列表箭头键导航——列表超出视口时高亮 agent 保持可见
- **Fixed**: `/branch` 成功消息未包含供 `/resume` 使用的新分支会话 id
- **Fixed**: 全屏模式下带 keycap/ZWJ/肤色 emoji 的粗体标题丢失尾随字符
- **Fixed**: 缺少 `user:inference` 范围的已存 OAuth 凭证的企业/团队用户未应用服务器托管设置策略
- **Fixed**: 唤醒后的 OAuth 刷新竞争可能登出所有运行中会话
- **Fixed**: 1 小时 prompt 缓存 TTL 被静默降级为 5 分钟
- **Fixed**: 更改 `/effort` 或 `/model` 时，`/clear` 或 compaction 后虚假出现缓存未命中警告
- **Fixed**: `Bash(mkdir *)`、`Bash(touch *)` 及类似 allow 规则未对项目内路径生效
- **Fixed**: 带 `*://` 方案通配符的 `deniedMcpServers` 模式未匹配混合大小写主机名
- **Fixed**: 语音模式下 `--debug` 中无害的 WebSocket 警告被记录为错误
- **Fixed**: [VSCode] `/clear` 未清除对话上下文和显示的 transcript

---

### v2.1.128 (2026-05-05)

> EnterWorktree 从本地 HEAD 分支、--plugin-dir .zip 支持、--channels console 认证、/mcp 工具计数、并行 bash 工具修复、sub-agent prompt 缓存修复、35 多个 bug 修复。

- **Fixed**: `EnterWorktree` 现在按文档所述从本地 HEAD 创建新分支——分支时不再丢弃未推送的提交
- **New**: `--plugin-dir` 除目录外还接受 `.zip` 插件归档
- **New**: `--channels` 现在可与 console（API key）认证配合使用——托管组织必须在托管设置中设置 `channelsEnabled: true`
- **Improved**: `/mcp` 为每个已连接服务器显示工具计数，并标记以 0 个工具连接的服务器
- **Improved**: 重连的 MCP 服务器不再在每次重连时用完整工具名列表淹没对话——重新声明的工具按服务器前缀汇总
- **Improved**: SDK 主机为 Bash 权限提示接收持久的 `localSettings` 建议，因此 "Always allow" 写入 `.claude/settings.local.json`
- **Improved**: 裸 `/color`（无参数）现在选取随机会话颜色
- **Improved**: `/model` 选择器折叠重复的 Opus 4.7 条目；当前 Opus 显示为 "Opus" 而非 "Opus 4.7"
- **Improved**: 子进程（Bash、hook、MCP、LSP）不再继承 `OTEL_*` env 变量——通过 Bash 运行的 OTEL 检测应用不再拾取 CLI 自身的 OTLP 端点
- **Fixed**: 并行 shell 工具调用——一个失败的只读命令（grep、git diff、ls）不再取消同级调用
- **Fixed**: Sub-agent 进度摘要缺失 prompt 缓存（`cache_creation` 减少约 3 倍）
- **Fixed**: 带较小 autocompact 窗口的 1M 上下文模型上的会话被错误地以 "Prompt is too long" 阻止
- **Fixed**: 当设置 `CLAUDE_CODE_SHELL_PREFIX` 且参数包含空格或 shell 元字符时，MCP stdio 服务器接收损坏的参数
- **Fixed**: `/plugin update` 从未检测到 npm 源插件的新版本
- **Fixed**: MCP：`workspace` 现在是保留服务器名——使用该名称的现有服务器会被跳过并警告
- **Fixed**: 不支持 OSC 8 超链接的终端上 Markdown 链接标签丢失——链接现在渲染为 `label (url)`
- **Fixed**: `/config` 中的 Tab 导航使焦点搁浅——标签页头保持聚焦，使箭头键和 Esc 继续工作
- **Fixed**: 列表项内的围栏代码块在复制粘贴时将前导空白带入剪贴板
- **Fixed**: 当服务器同时返回结构化内容和内容块时，MCP 工具结果丢弃图像
- **Fixed**: 工具调用之间终端进度指示器（OSC 9;4）闪烁熄灭
- **Fixed**: 另有 20 多个终端、剪贴板和会话管理 bug 修复

---

### v2.1.126 (2026-05-01)

> /model 选择器中的网关 /v1/models 列表、claude project purge、WSL2/SSH 的 OAuth 粘贴码、Windows PowerShell 7 作为主 shell、安全修复、40 多个 bug 修复。

- **New**: 当 `ANTHROPIC_BASE_URL` 指向 Anthropic 兼容网关时，`/model` 选择器现在从你网关的 `/v1/models` 端点列出模型
- **New**: `claude project purge [path]` 删除某项目的所有 Claude Code 状态（transcript、任务、文件历史、配置项）——支持 `--dry-run`、`-y/--yes`、`-i/--interactive` 和 `--all`
- **Improved**: `--dangerously-skip-permissions` 现在对写入 `.claude/`、`.git/`、`.vscode/`、shell 配置文件及其他此前受保护路径绕过提示（灾难性删除命令仍会提示作为安全网）
- **Improved**: 当浏览器回调无法到达 localhost（WSL2、SSH、容器）时，`claude auth login` 接受粘贴到终端的 OAuth 码
- **Improved**: `claude_code.skill_activated` OpenTelemetry 事件现在为用户输入的 slash 命令触发，带有新的 `invocation_trigger` 属性（`"user-slash"`、`"claude-proactive"` 或 `"nested-skill"`）
- **Improved**: 权限检查停滞时 auto 模式加载动画现在变红，而非看起来像工具在运行
- **Improved**: Windows——现在能检测通过 Microsoft Store、无 PATH 的 MSI 或 `.NET global tool` 安装的 PowerShell 7；当 PowerShell 工具启用时，Claude 将 PowerShell 视为主 shell，而非默认 Bash
- **Improved**: Read 工具——移除了导致旧模型上虚假拒绝的逐文件恶意软件评估提醒
- **Security**: 修复当更高优先级的托管设置源缺少 `sandbox` 块时 `allowManagedDomainsOnly` / `allowManagedReadPathsOnly` 被忽略
- **Fixed**: 粘贴大于 2000px 的图像不再破坏会话——图像在粘贴时被缩小，历史中的超大图像被自动移除并重试请求
- **Fixed**: 在慢速或代理连接、仅 IPv6 的 devcontainer 以及浏览器回调无法到达 localhost 时，OAuth 登录超时失败
- **Fixed**: Mac 在请求中途从休眠唤醒后的 "Stream idle timeout" 错误；后台和远程会话在长时间模型思考停顿期间不再错误中止
- **Fixed**: Windows 上无闪烁模式下日语/韩语/中文文本渲染为乱码
- **Fixed**: `Ctrl+L` 清空 prompt 输入——现在只强制重绘屏幕，与 readline 行为一致
- **Fixed**: 带 `context: fork` 的 skill 在首轮无法使用延迟工具（WebSearch、WebFetch 等）
- **Fixed**: Windows 剪贴板写入不再在 EDR/SIEM 遥测可见的进程命令行参数中暴露复制内容；同时修复 >22KB 选区无法到达剪贴板
- **Fixed**: 当模型在并行工具调用批次中发出格式错误的工具名时 Agent SDK 挂起
- **Fixed**: `/plugin` Uninstall 报告 "Enabled" 而非 "Uninstalled"

---

### v2.1.123 (2026-04-29)

> 热修复：CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1 时的 OAuth 401 重试循环。

- **Fixed**: 设置 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` 时 OAuth 认证以 401 重试循环失败

---

### v2.1.122 (2026-04-28)

> ANTHROPIC_BEDROCK_SERVICE_TIER env 变量、/resume 搜索中的 PR URL、Vertex AI/Bedrock 修复、图像缩放修复、众多 bug 修复。

- **New**: `ANTHROPIC_BEDROCK_SERVICE_TIER` 环境变量，通过 `X-Amzn-Bedrock-Service-Tier` 头选择 Bedrock 服务层级（`default`、`flex` 或 `priority`）
- **New**: 将 PR URL 粘贴到 `/resume` 搜索框现在能找到创建该 PR 的会话（GitHub、GitHub Enterprise、GitLab 和 Bitbucket）
- **Improved**: `/mcp` 现在显示被手动添加的同 URL 服务器隐藏的 claude.ai 连接器，并提示移除重复项
- **Fixed**: `/branch` 产生因回退时间线而以 "tool_use ids were found without tool_result blocks" 失败的分叉
- **Fixed**: `/model` 未为 Bedrock 应用推理配置文件 ARN 显示 Effort 选项
- **Fixed**: Vertex AI / Bedrock 在标题生成和结构化输出查询上返回 `invalid_request_error: output_config: Extra inputs are not permitted`
- **Fixed**: Vertex AI `count_tokens` 端点为代理网关后的用户返回 400 错误
- **Fixed**: bash 模式下的 `!exit` / `!quit` 终止 CLI，而非作为 shell 命令运行
- **Fixed**: 发送到较新模型的图像被缩放到 2576px 而非正确的 2000px 最大值
- **Fixed**: Remote control 会话空闲状态每秒重绘两次，淹没 `tmux -CC` 控制管道
- **Fixed**: `ToolSearch` 在非阻塞模式下缺失会话启动后才连接的 MCP 工具
- **Fixed**: `settings.json` 中格式错误的 hooks 条目不再使整个文件失效
- **Fixed**: `spinnerTipsOverride.excludeDefault` 未抑制基于时间的加载动画提示
- **Fixed**: 由于陈旧的视图偏好，部分会话中助手消息显示为空白

---

### v2.1.121 (2026-04-27)

> alwaysLoad MCP 配置、plugin prune、所有工具的 PostToolUse 输出替换、关键内存泄漏修复、众多 bug 修复。

- **New**: MCP 服务器配置中的 `alwaysLoad` 选项——当为 `true` 时，该服务器的所有工具跳过工具搜索延迟并始终可用
- **New**: `claude plugin prune` 移除孤立的自动安装插件依赖；`plugin uninstall --prune` 级联执行
- **New**: `/skills` 中的输入即筛选搜索框，无需滚动即可查找 skill
- **New**: `PostToolUse` hook 现在可通过 `hookSpecificOutput.updatedToolOutput` 为所有工具替换工具输出（此前仅限 MCP）
- **New**: Vertex AI：支持基于 X.509 证书的工作负载身份联合（mTLS ADC）
- **Improved**: 全屏模式：向上滚动后，输入 prompt 不再将滚动跳到底部
- **Improved**: 溢出终端的对话框现在可用箭头键、PgUp/PgDn、home/end 和鼠标滚轮滚动
- **Improved**: 在全屏中点击跨行换行的长 URL 任意一行现在会打开完整 URL
- **Improved**: `--dangerously-skip-permissions` 不再为写入 `.claude/skills/`、`.claude/agents/` 和 `.claude/commands/` 提示
- **Improved**: `/terminal-setup` 现在为 tmux 中的 `/copy` 启用 iTerm2 的 "Applications in terminal may access clipboard"
- **Improved**: 遇到瞬时启动错误的 MCP 服务器现在自动重试最多 3 次
- **Improved**: 终端标签页会话标题现在以你配置的 `language` 设置生成
- **Improved**: 具有相同上游 URL 的 Claude.ai 连接器现在被去重
- **Improved**: LSP 诊断摘要现在在点击/ctrl+o 时展开并显示展开提示
- **Improved**: OpenTelemetry：新增 `stop_reason`、`gen_i.response.finish_reasons` 和 `user_system_prompt`（受 `OTEL_LOG_USER_PROMPTS` 限制）
- **[VSCode]**: `/context` 现在打开原生 token 使用对话框；语音听写遵循 `accessibility.voice.speechLanguage`
- **Fixed**: 在会话中处理大量图像时的无限制内存增长（多 GB RSS）
- **Fixed**: 在拥有大量 transcript 历史的机器上 `/usage` 泄漏多达约 2GB 内存
- **Fixed**: 长时间运行的工具未能发出清晰进度事件时的内存泄漏
- **Fixed**: 当起始目录在会话中途被删除或移动时 Bash 工具永久不可用
- **Fixed**: `--resume` 在外部构建中启动时崩溃
- **Fixed**: 当 transcript 行被不干净关闭损坏时，`--resume` 在大会话上失败
- **Fixed**: Bedrock 应用推理配置文件 ARN 的 `thinking.type.enabled is not supported` 错误
- **Fixed**: Microsoft 365 MCP OAuth 因重复或不支持的 `prompt` 参数而失败
- **Fixed**: 在 tmux、GNOME Terminal、Windows Terminal、Konsole 上非全屏模式下按 Ctrl+L 时的回滚缓冲区重复
- **Fixed**: claude.ai MCP 连接器在启动时瞬时认证错误时静默消失
- **Fixed**: 远程会话中内置工具的 "Always allow" 规则在 worker 重启后未保留
- **Fixed**: 在原生构建上通过 `managed-settings.json` 设置时，所有 HTTP 客户端未遵循 `NO_PROXY`
- **Fixed**: 即使被接受，托管设置批准提示也退出会话

---

### v2.1.120 (2026-04-24)

> Windows 不再需要 Git Bash、claude ultrareview CI 子命令、skill 中的 ${CLAUDE_EFFORT}、众多 bug 修复。

- **New**: Windows：不再需要 Git for Windows（Git Bash）——缺失时，Claude Code 使用 PowerShell 作为 shell 工具
- **New**: `claude ultrareview [target]` 子命令，用于从 CI 或脚本非交互式运行 `/ultrareview`；`--json` 输出原始结果；完成时退出码 0，失败时退出码 1
- **New**: Skill 可用 `${CLAUDE_EFFORT}` 在其内容中引用当前 effort 等级
- **New**: 为子进程设置 `AI_AGENT` 环境变量，使 `gh` 能将流量归因于 Claude Code
- **Improved**: 配置了大量 claude.ai 连接器但未授权时会话启动更快
- **Improved**: `claude plugin validate` 现在接受 `marketplace.json` 顶层的 `$schema`、`version` 和 `description`
- **Improved**: Auto 模式下的自动 compact 现在显示 `auto`（小写）而非误导性的 token 值
- **Improved**: 当你已拥有桌面应用或 skill/agent 时，推荐它们的加载动画提示被隐藏
- **Improved**: 当终端发送箭头键而非滚动事件时，显示 "use PgUp/PgDn to scroll" 提示
- **Fixed**: 在 stdio MCP 工具调用期间按 Esc 关闭整个服务器连接（2.1.105 引入的回归）
- **Fixed**: `--resume` 后 `/rewind` 和其他交互式浮层不响应键盘输入
- **Fixed**: 非全屏模式下的终端回滚缓冲区重复（缩放、对话框关闭、长会话）
- **Fixed**: `DISABLE_TELEMETRY` / `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 未为 API 和企业用户抑制使用量指标遥测
- **Fixed**: auto 模式下带管道和重定向的多行 bash 出现误报的 "Dangerous rm operation" 权限提示
- **Fixed**: 全屏模式下长选择菜单被裁剪到终端下方
- **Fixed**: 在全屏中点击 "+N lines" 时 Write 工具输出折叠而非展开
- **Fixed**: 输入时 slash 命令选择器跳动；高亮现在只匹配连续子串
- **Fixed**: 当某条目使用无法识别的源格式时 `/plugin` marketplace 加载失败
- **Fixed**: Bash 工具中的 `find` 在大型目录树上耗尽打开的文件描述符，导致主机范围崩溃（macOS/Linux 原生构建）
- **[VSCode]**: `/usage` 现在打开原生 Account & Usage 对话框；语音听写遵循 `language` 设置

---

### v2.1.119 (2026-04-24)

> /config 设置以覆盖优先级持久化到 settings.json、--from-pr 支持 GitLab/Bitbucket/GitHub Enterprise、agent frontmatter 改进、blockedMarketplaces 安全修复、30 多个 bug 修复。

- **New**: `/config` 设置（主题、编辑器模式、verbose 等）现在持久化到 `~/.claude/settings.json` 并参与项目/本地/策略覆盖优先级
- **New**: `prUrlTemplate` 设置，将页脚 PR 徽标指向自定义代码审查 URL 而非 github.com
- **New**: `CLAUDE_CODE_HIDE_CWD` 环境变量，在启动 logo 中隐藏工作目录
- **New**: `--from-pr` 现在接受 GitLab 合并请求、Bitbucket 拉取请求和 GitHub Enterprise PR URL
- **Improved**: `--print` 模式现在遵循 agent 的 `tools:` 和 `disallowedTools:` frontmatter，与交互模式行为一致
- **Improved**: `--agent <name>` 现在为内置 agent 遵循 agent 定义的 `permissionMode`
- **Improved**: PowerShell 工具命令现在可在权限模式下自动批准，与 Bash 行为一致
- **Improved**: `PostToolUse` 和 `PostToolUseFailure` hook 输入现在包含 `duration_ms`（工具执行时间，不含权限提示和 PreToolUse hook）
- **Improved**: Subagent 和 SDK MCP 服务器重新配置现在并行连接服务器，而非串行
- **Improved**: 被另一个插件版本约束固定的插件现在自动更新到最高满足条件的 git 标签
- **Improved**: Vim 模式：INSERT 中的 Esc 不再将排队消息拉回输入；再次按 Esc 以中断
- **Improved**: Slash 命令建议现在高亮匹配你查询的字符；选择器换行显示长描述而非截断
- **Improved**: `owner/repo#N` 简写链接现在使用你 git 远程的主机，而非始终指向 github.com
- **Security**: `blockedMarketplaces` 现在正确强制 `hostPattern` 和 `pathPattern` 条目
- **Fixed**: 粘贴 CRLF 内容（Windows 剪贴板、Xcode 控制台）在每行之间插入额外空行
- **Fixed**: 当 Bash 工具通过权限被拒绝时，Glob 和 Grep 工具在原生 macOS/Linux 构建上消失
- **Fixed**: 全屏模式下向上滚动每次工具完成时都弹回底部
- **Fixed**: Auto 模式用冲突的 "Execute immediately" 指令覆盖 plan 模式
- **Fixed**: 带 `isolation: "worktree"` 的 `Agent` 工具复用先前会话的陈旧 worktree
- **Fixed**: `TaskList` 以任意文件系统顺序返回任务，而非按 ID 排序
- **Fixed**: 进入 plan 模式时 `/plan` 和 `/plan open` 未对现有计划起作用
- **Fixed**: 在自动 compaction 前调用的 skill 被针对下一条用户消息重新执行
- **Fixed**: Verbose 输出设置在重启后未持久化；禁用的 MCP 服务器在 `/status` 中显示为 "failed"
- **Fixed**: HTTP/SSE/WebSocket MCP 服务器 `headers` 中的 `${ENV_VAR}` 占位符未被替换
- **Fixed**: 对于 `client_secret_post` 服务器，token 交换期间未发送 MCP OAuth `--client-secret`
- **Fixed**: `/skills` Enter 键关闭对话框而非在 prompt 中预填 `/<skill-name>`
- **Fixed**: 来自提及 "rate limit" 的 PR 标题的虚假 "GitHub API rate limit exceeded" 提示
- **Fixed**: 异步 `PostToolUse` hook 不发出响应时向会话 transcript 写入空条目
- **Fixed**: 在带绝对路径的 slash 命令内使用时，`@`-文件 Tab 补全替换整个 prompt

### v2.1.118 (2026-04-23)

> Vim 可视模式、/usage 合并 /cost+/stats、自定义命名主题、hook 直接调用 MCP 工具、众多 bug 修复。

- **New**: Vim 可视模式（`v`）和可视行模式（`V`），带选择、操作符（d、y、c、>、<）和可视反馈
- **New**: `/cost` 和 `/stats` 合并入 `/usage`——两个旧命令仍作为打开相关标签页的输入快捷方式保留
- **New**: 从 `/theme` 创建并切换命名自定义主题，或手动编辑 `~/.claude/themes/` 中的 JSON 文件；插件可通过 `themes/` 目录提供主题
- **New**: Hook 现在可通过 hook 配置中的 `type: "mcp_tool"` 直接调用 MCP 工具
- **New**: `DISABLE_UPDATES` env 变量完全阻止所有更新路径，包括手动 `claude update`（比 `DISABLE_AUTOUPDATER` 更严格）
- **New**: Windows 上的 WSL 可通过 `wslInheritsWindowsSettings` 策略键继承 Windows 端的托管设置
- **Improved**: Auto 模式 `"$defaults"` 哨兵——在 `autoMode.allow`、`autoMode.soft_deny` 或 `autoMode.environment` 中包含它，可在内置列表旁添加自定义规则而非替换它
- **Improved**: auto 模式选择加入提示中新增 "Don't ask again" 选项
- **Improved**: `--continue`/`--resume` 现在能找到通过 `/add-dir` 添加当前目录的会话
- **Improved**: 连接 Remote Control 时，`/color` 将会话强调色同步到 claude.ai/code
- **Improved**: 使用自定义 `ANTHROPIC_BASE_URL` 网关时，`/model` 选择器现在遵循 `ANTHROPIC_DEFAULT_*_MODEL_NAME`/`_DESCRIPTION` 覆盖
- **Improved**: `claude plugin tag` 用于为插件创建带版本验证的发布 git 标签
- **Improved**: 因版本约束跳过的自动更新现在显示在 `/doctor` 和 `/plugin` Errors 标签页中
- **Fixed**: `/mcp` 菜单为带 `headersHelper` 的服务器隐藏 OAuth Authenticate/Re-authenticate，以及 HTTP/SSE 服务器在瞬时 401 后卡在 "needs authentication"
- **Fixed**: 响应中无 `expires_in` 的 MCP OAuth token 需每小时重新认证
- **Fixed**: 当 `insufficient_scope` 403 指明已持有的范围时，MCP 升级授权静默刷新而非提示
- **Fixed**: macOS keychain 竞争，其中并发 token 刷新可能覆盖刚刷新的 OAuth token
- **Fixed**: Linux/Windows 上凭证保存崩溃损坏 `~/.claude/.credentials.json`
- **Fixed**: 在以 `CLAUDE_CODE_OAUTH_TOKEN` env 变量启动的会话中 `/login` 无效果
- **Fixed**: Agent 型 hook 为非 Stop 事件以 "Messages are required for agent hooks" 失败
- **Fixed**: `prompt` hook 在 agent-hook 验证器 subagent 发起的工具调用上重新触发
- **Fixed**: `/fork` 为每个分叉将完整父对话写入磁盘——现在写入指针并在读取时填充
- **Fixed**: Alt+K / Alt+X / Alt+^ / Alt+_ 冻结键盘输入
- **Fixed**: 对已安装插件执行 `plugin install` 未重新解析错误版本的依赖
- **Fixed**: 通过 `SendMessage` 恢复的 subagent 未还原其显式 `cwd`

### v2.1.117 (2026-04-22)

> Pro/Max 在 Opus 4.6 + Sonnet 4.6 上的默认 effort 现为 `high`，macOS/Linux 原生 bfs/ugrep，Opus 4.7 1M context 修复，/model 持久化，15+ 项 bug 修复。

- **Changed**：Pro/Max 订阅者在 Opus 4.6 和 Sonnet 4.6 上的默认 effort 级别改为 `high`（原为 `medium`）
- **Fixed**：Opus 4.7 会话此前按 200K 窗口而非原生 1M 计算 `/context` 百分比——导致百分比虚高并过早触发 autocompact
- **New**：原生 macOS/Linux 构建现使用内嵌的 `bfs`（搜索）和 `ugrep`（grep）替代 Glob/Grep 工具——更快且无需额外的工具往返（Windows 和 npm 安装的构建不变）
- **Improved**：`/model` 选择现在可跨重启持久保留，即使项目固定了不同的模型；启动头部会显示当前活动模型是否来自项目或托管设置的固定项
- **Improved**：`/resume` 现在会在重新读取陈旧的大型会话之前提供总结选项（与现有的 `--resume` 行为一致）
- **Improved**：同时配置本地和 claude.ai MCP 服务器时启动更快（并发连接现为默认）
- **Improved**：对已安装的插件执行 `plugin install` 现在会安装任何缺失的依赖，而不是在「already installed」处停止；依赖错误会显示「not installed」并附带安装提示
- **Improved**：`cleanupPeriodDays` 保留期清理现在也覆盖 `~/.claude/tasks/`、`~/.claude/shell-snapshots/` 和 `~/.claude/backups/`
- **Improved**：通过 `--agent` 运行的主线程 agent 会话现在会加载 agent frontmatter 中的 `mcpServers`
- **Improved**：OpenTelemetry `user_prompt` 事件现在为 slash commands 包含 `command_name` 和 `command_source`；在受支持时，cost/token/API 事件包含 `effort` 属性
- **Fixed**：纯 CLI OAuth 会话在访问令牌于会话中途过期时因「Please run /login」而中断——令牌现在会在收到 401 时被动刷新
- **Fixed**：`WebFetch` 在处理超大 HTML 页面时挂起（在 HTML 转 markdown 之前截断输入）
- **Fixed**：代理返回 HTTP 204 No Content 时崩溃
- **Fixed**：使用 `CLAUDE_CODE_OAUTH_TOKEN` 环境变量启动且该令牌过期时，`/login` 无效
- **Fixed**：输入框撤销（`Ctrl+_`）在刚输入文字后无反应，且每次撤销步骤会跳过一个状态
- **Fixed**：在 Bun 下运行时远程 API 请求不遵守 `NO_PROXY`
- **Fixed**：Bedrock application-inference-profile 请求在底层为禁用 thinking 的 Opus 4.7 时报 400 失败

### v2.1.116 (2026-04-21)

> 回归修复版本：结束了为期六周的 Triple Harness Incident（2026 年 3 月 4 日至 4 月 20 日）。此外：大型会话上 /resume 最高提速 67%，行内 thinking 进度旋转图标，沙箱安全修复，以及大量 bug 修复。

- **Regression fix**：导致这次六周质量回归的全部三项 harness 级改动（effort 默认值、thinking 预算清除、verbosity 指令）已在本版本中回退或修复——完整时间线见 [Triple Harness Incident](./known-issues.md#triple-harness-incident-effort-thinking-tokens-verbosity-mar-apr-2026)
- **Improved**：`/resume` 在 40MB+ 会话上最高提速 67%，并能更高效地处理含大量 dead-fork 条目的会话
- **Improved**：配置多个 stdio 服务器时 MCP 启动更快；`resources/templates/list` 推迟到首次 `@` 提及时进行
- **Improved**：VS Code、Cursor 和 Windsurf 中的全屏滚动更流畅；`/terminal-setup` 现在会配置编辑器的滚动灵敏度
- **Improved**：thinking 旋转图标现在显示行内进度（「still thinking」「thinking more」「almost done thinking」），取代了单独的提示行
- **Improved**：`/config` 搜索现在会匹配选项值（例如搜索「vim」可找到 Editor 模式设置）
- **Improved**：`/doctor` 现在可在 Claude 响应过程中打开，无需等待当前回合结束
- **Improved**：`/reload-plugins` 和后台插件自动更新现在会从已添加的 marketplace 自动安装缺失的依赖
- **Improved**：当 `gh` 命令触发 GitHub 的 API 速率限制时，Bash 工具会显示提示，使 agent 能够退避而非重试
- **Improved**：Usage 选项卡立即显示 5 小时和每周用量，且不再在用量端点被限速时失败
- **Improved**：通过 `--agent` 作为主线程 agent 运行时，agent frontmatter 中的 `hooks:` 现在会触发
- **Improved**：当过滤结果为零时，slash command 菜单显示「No commands match」，而非直接消失
- **Security**：沙箱自动放行不再为针对 `/`、`$HOME` 或其他关键系统目录的 `rm`/`rmdir` 绕过危险路径安全检查
- **Fixed**：终端 UI 中天城文及其他印度系文字列对齐错乱
- **Fixed**：在使用 Kitty 键盘协议的终端（iTerm2、Ghostty、kitty、WezTerm、Windows Terminal）中 `Ctrl+-` 无法触发撤销
- **Fixed**：在 Kitty 协议终端（Warp 全屏、kitty、Ghostty、WezTerm）中 `Cmd+Left/Right` 无法跳到行首/行尾
- **Fixed**：通过包装进程（例如 `npx`、`bun run`）启动 Claude Code 时 `Ctrl+Z` 挂起终端
- **Fixed**：行内模式下的回滚内容重复，调整终端大小或大量输出突增时会重复之前的对话历史
- **Fixed**：在终端高度较短时模态搜索对话框溢出屏幕，遮挡搜索框和键盘提示
- **Fixed**：滚动时 VS Code 集成终端中出现零散空白单元格和消失的编辑器外框
- **Fixed**：与 cache control TTL 排序相关的间歇性 API 400 错误，可能在请求设置期间有并行请求完成时发生
- **Fixed**：`/branch` 拒绝转录文件大于 50MB 的对话
- **Fixed**：`/resume` 在大型会话文件上静默显示空对话，而非报告加载错误
- **Fixed**：当某项同时出现在 Needs attention 或 Favorites 下时，`/plugin` Installed 选项卡重复显示该项两次
- **Fixed**：会话中途进入 worktree 后 `/update` 和 `/tui` 失效

---

### v2.1.114 (2026-04-18)

> 修复了 agent teams 队友请求工具权限时权限对话框的崩溃。

- **Fixed**：agent teams 队友请求工具权限时权限对话框崩溃

---

### v2.1.113 (2026-04-18)

> 原生 Claude Code 二进制文件启动、sandbox.network.deniedDomains 设置、安全加固，以及大量 bug 修复。

- **New**：CLI 现在通过每平台的可选依赖启动原生 Claude Code 二进制文件，而非内置 JavaScript
- **New**：`sandbox.network.deniedDomains` 设置——即使更宽泛的 `allowedDomains` 通配符本会允许，也能阻断特定域名
- **Improved**：全屏模式——将选区扩展到超出可见边缘时，`Shift+↑/↓` 现在会滚动视口
- **Improved**：在多行输入中，`Ctrl+A` 和 `Ctrl+E` 现在会移到当前逻辑行的行首/行尾（readline 行为）
- **Improved**：Windows：`Ctrl+Backspace` 现在会删除前一个单词
- **Improved**：响应和 bash 输出中的长 URL 在跨行换行时仍可点击（在支持 OSC 8 超链接的终端中）
- **Improved**：`/loop`——按 Esc 现在会取消待执行的唤醒；唤醒显示为「Claude resuming /loop wakeup」以求清晰
- **Improved**：`/extra-usage` 现在可在 Remote Control（移动端/网页端）客户端中使用
- **Improved**：Remote Control 客户端现在可查询 `@`-file 自动补全建议
- **Improved**：`/ultrareview`——通过并行化检查实现更快启动，启动对话框中显示 diffstat，启动状态带动画
- **Improved**：流式过程中停滞的 subagent 现在会在 10 分钟后以清晰的错误失败，而非静默挂起
- **Improved**：Bash 工具——首行为注释的多行命令现在会在转录中显示完整命令，封堵一个 UI 欺骗向量
- **Improved**：当 `cd` 为空操作时，运行 `cd <current-directory> && git …` 不再触发权限提示
- **Security**：在 macOS 上，`/private/{etc,var,tmp,home}` 路径现在在 `Bash(rm:*)` 放行规则下被视为危险的删除目标
- **Security**：Bash 拒绝规则现在会匹配被 `env`/`sudo`/`watch`/`ionice`/`setsid` 及类似 exec 包装器包裹的命令
- **Security**：`Bash(find:*)` 放行规则不再自动批准 `find -exec`/`-delete`
- **Fixed**：MCP 并发调用超时处理中，某个工具调用的消息可能会静默解除另一个调用看门狗的问题
- **Fixed**：Cmd-backspace / `Ctrl+U` 重新可从光标删除到行首
- **Fixed**：当单元格包含带管道符的行内代码片段时 markdown 表格断裂
- **Fixed**：在输入框中编写未发送文本时会话 recap 自动触发
- **Fixed**：`/copy`「Full response」未对齐 markdown 表格列以便粘贴到 GitHub、Notion 或 Slack
- **Fixed**：查看运行中的 subagent 时输入的消息从其转录中隐藏并被错误归属到父 AI
- **Fixed**：`Bash dangerouslyDisableSandbox` 在沙箱外运行命令而不弹出权限提示
- **Fixed**：`/effort auto` 确认现在显示「Effort level set to max」以匹配状态栏标签
- **Fixed**：「copied N chars」提示对 emoji 和其他多码元字符计数过多
- **Fixed**：`/insights` 在 Windows 上以 `EBUSY` 崩溃
- **Fixed**：退出确认对话框将一次性计划任务误标为周期性——现在显示倒计时
- **Fixed**：全屏模式下 Slash/@ 补全菜单未紧贴输入框边框
- **Fixed**：`CLAUDE_CODE_EXTRA_BODY output_config.effort` 在对不支持 effort 的模型以及 Vertex AI 进行 subagent 调用时导致 400 错误
- **Fixed**：设置 `NO_COLOR` 时输入框光标消失
- **Fixed**：`ToolSearch` 排序问题，使粘贴的 MCP 工具名称浮现实际工具而非描述匹配的同类项
- **Fixed**：压缩已恢复的 long-context 会话时报「Extra usage is required for long context requests」失败
- **Fixed**：当依赖版本与已安装插件冲突时 `plugin install` 仍成功的问题——现在报告 `range-conflict`
- **Fixed**：「Refine with Ultraplan」未在转录中显示远程会话 URL
- **Fixed**：处理失败的 SDK 图像内容块导致会话崩溃——现在降级为文本占位符
- **Fixed**：Remote Control 会话未流式传输 subagent 转录
- **Fixed**：Claude Code 退出时 Remote Control 会话未被归档
- **Fixed**：通过 Bedrock Application Inference Profile ARN 使用 Opus 4.7 时出现 `thinking.type.enabled is not supported` 400 错误

---

### v2.1.111 (2026-04-16)

> Claude Opus 4.7 xhigh effort 级别、/ultrareview 云端代码审查、/less-permission-prompts skill、Max 订阅者的 Auto 模式。

- **New**：Claude Opus 4.7 `xhigh` effort 级别——介于 `high` 和 `max` 之间；可通过 `/effort`、`--effort` 及模型选择器使用；其他模型回退到 `high`
- **New**：Opus 4.7 上 Max 订阅者的 Auto 模式——不再需要 `--enable-auto-mode`
- **New**：`/ultrareview` skill——使用并行多 agent 分析在云端运行全面的代码审查；不带参数调用以审查当前分支，或 `/ultrareview <PR#>` 以审查特定的 GitHub PR
- **New**：`/less-permission-prompts` skill——扫描转录中常见的只读 Bash 和 MCP 工具调用，为 `.claude/settings.json` 提出按优先级排序的放行清单
- **New**：「Auto (match terminal)」主题选项——跟随终端的深色/浅色模式；可通过 `/theme` 选择
- **New**：不带参数调用 `/effort` 时会打开交互式滑块；方向键导航 + Enter 确认
- **Improved**：计划文件现在以你的 prompt 命名（例如 `fix-auth-race-snug-otter.md`），而非纯随机词
- **Improved**：带通配符的只读 bash 命令（例如 `ls *.ts`）以及以 `cd <project-dir> &&` 开头的命令不再触发权限提示
- **Improved**：当设置了 `CLAUDE_CONFIG_DIR` 时，`/setup-vertex` 和 `/setup-bedrock` 会显示实际的 `settings.json` 路径，在重新运行时从现有固定项填充候选模型，并提供「with 1M context」选项
- **Improved**：`/skills` 菜单现在支持按估算 token 数排序——按 `t` 切换
- **Improved**：`Ctrl+U` 清空整个输入缓冲区（`Ctrl+Y` 恢复）；`Ctrl+L` 强制全屏重绘
- **Improved**：对接近的 `claude <word>` 调用提供拼写建议（例如 `claude udpate` →「Did you mean `claude update`?」）
- **Improved**：Headless `--output-format stream-json` 在 init 事件中包含 `plugin_errors`；`OTEL_LOG_RAW_API_BODIES` 环境变量将完整的 API 主体作为 OpenTelemetry 日志事件发出
- **Fixed**：发送终端通知时 iTerm2 + tmux 配置中的终端显示撕裂（随机字符、漂移的输入）
- **Fixed**：在非 git 目录中 `@` 文件建议每回合都重新扫描整个项目；在新初始化且无跟踪文件的 git 仓库中仅显示配置文件
- **Fixed**：编辑前的 LSP 诊断在编辑后才出现，导致模型重新读取已编辑的文件
- **Fixed**：Tab 补全 `/resume` 时立即恢复某个任意命名的会话，而非显示会话选择器
- **Fixed**：`/clear` 丢弃由 `/rename` 设置的会话名，导致状态栏丢失 `session_name`
- **Fixed**：对于没有自定义 `/commit` 命令的用户，Claude 调用不存在的 `commit` skill 时显示「Unknown skill: commit」
- **Fixed**：Bedrock/Vertex/Foundry 上的 429 速率限制错误错误地引用 status.claude.com
- **Fixed**：多个其他问题——终端跨行换行时裸 URL 不可点击、反馈调查接连出现、Windows `CLAUDE_ENV_FILE` 和 SessionStart hook 环境文件现在生效、盘符路径权限规则正确地以根锚定
- **Fixed**：插件错误处理改进——依赖错误区分冲突/无效/过于复杂的版本要求；`plugin update` 后的过期已解析版本；`plugin install` 可从被中断的安装中恢复
- **Reverted**：v2.1.110 对非流式回退重试的上限——它在 API 过载期间以更多直接失败换取了更长的等待

---

### v2.1.110 (2026-04-16)

> /tui 全屏命令、推送通知工具、--resume 复活计划任务、/focus 命令，以及 30+ 项 bug 修复。

- **New**：`/tui` 命令和 `tui` 设置——运行 `/tui fullscreen` 在同一对话内切换到无闪烁渲染
- **New**：推送通知工具（`PushNotification`）——启用 Remote Control 和「Push when Claude decides」配置后，Claude 可发送移动端推送通知
- **New**：`--resume`/`--continue` 现在会复活未过期的计划任务
- **New**：`/focus` 命令——focus 视图现在单独切换；`Ctrl+O` 恢复为仅在普通和详细转录之间切换
- **New**：`autoScrollEnabled` 配置——在全屏模式下禁用对话自动滚动
- **New**：在 `Ctrl+G` 外部编辑器中将 Claude 的上一条响应显示为注释上下文的选项（通过 `/config` 启用）
- **Improved**：`/plugin` Installed 选项卡——需要关注的项和收藏项显示在顶部；禁用项隐藏在折叠后；`f` 收藏
- **Improved**：当某个 MCP 服务器在多个配置范围中以不同端点定义时，`/doctor` 会发出警告
- **Improved**：会话 recap 现在对禁用了遥测的用户启用（Bedrock、Vertex、Foundry、`DISABLE_TELEMETRY`）；可通过 `/config` 或 `CLAUDE_CODE_ENABLE_AWAY_SUMMARY=0` 退出
- **Improved**：当你在接受前于 IDE diff 中编辑了拟议内容时，Write 工具会告知模型；Bash 工具强制执行文档规定的最大超时
- **Fixed**：在 SSE/HTTP 传输上服务器连接在响应中途断开时 MCP 工具调用无限期挂起
- **Fixed**：API 不可达时非流式回退重试导致数分钟挂起
- **Fixed**：返回 `updatedInput` 的 `PermissionRequest` hook 未对照 `permissions.deny` 规则重新检查；`setMode:'bypassPermissions'` 现在遵守 `disableBypassPermissionsMode`
- **Fixed**：工具调用失败时 `PreToolUse` hook 的 `additionalContext` 被丢弃
- **Fixed**：向 stdout 打印杂散非 JSON 行的 stdio MCP 服务器在首个杂散行时即被断开（v2.1.105 中的回归）
- **Fixed**：设置了 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 或 `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` 时 Headless/SDK 自动标题触发了额外的 Haiku 请求
- **Fixed**：macOS Terminal.app 及其他不支持同步输出的终端中启动渲染乱码
- **Security**：加固了「Open in editor」操作以防来自不受信任文件名的命令注入
- **Fixed**：多个其他问题——全屏下 CPU 占用过高、重启后按键丢失、`/skills` 菜单无法滚动、Remote Control 会话重命名未持久化、会话清理未移除 subagent 转录

---

### v2.1.109 (2026-04-15)

> 改进了 extended-thinking 指示器，加入了轮换的进度提示。

- **Improved**：extended-thinking 指示器现在显示轮换的进度提示，以在长时间 thinking 阶段提供更好的可见性

---

### v2.1.108 (2026-04-15)

> 1 小时 prompt cache TTL 选项、/recap 会话上下文功能、可通过 Skill 工具发现的内置 slash commands、/undo 作为 /rewind 的别名。

- **New**：`ENABLE_PROMPT_CACHING_1H` 环境变量——在 API key、Bedrock、Vertex 和 Foundry 上选用 1 小时 prompt cache TTL（`ENABLE_PROMPT_CACHING_1H_BEDROCK` 已弃用但仍受支持）；`FORCE_PROMPT_CACHING_5M` 强制使用 5 分钟 TTL
- **New**：`/recap` 功能——在中断后返回会话时提供上下文；可在 `/config` 中配置；若禁用遥测可用 `CLAUDE_CODE_ENABLE_AWAY_SUMMARY` 强制启用
- **New**：模型现在可通过 Skill 工具发现并调用内置 slash commands，如 `/init`、`/review`、`/security-review`
- **New**：`/undo` 现在是 `/rewind` 的别名
- **New**：查看详细转录（`Ctrl+O`）时的「verbose」指示器
- **New**：当通过 `DISABLE_PROMPT_CACHING*` 环境变量禁用 prompt caching 时的启动警告
- **Improved**：`/model` 现在会在会话中途切换模型前发出警告（下一次响应会非缓存地重新读取完整历史）
- **Improved**：`/resume` 选择器默认显示当前目录的会话；按 `Ctrl+A` 显示所有项目
- **Improved**：错误消息区分服务器速率限制和套餐用量限制；5xx/529 错误链接到 status.claude.com；未知 slash commands 建议最接近的匹配
- **Improved**：通过按需加载语言语法减少了文件读取、编辑和语法高亮的内存占用
- **Fixed**：`/login` 代码提示中无法粘贴（v2.1.105 中的回归）
- **Fixed**：`DISABLE_TELEMETRY` 订阅者回退到 5 分钟 prompt cache TTL 而非 1 小时
- **Fixed**：当 `CLAUDE_ENV_FILE`（例如 `~/.zprofile`）以 `#` 注释行结尾时 Bash 工具无输出
- **Fixed**：`--resume <session-id>` 丢失通过 `/rename` 设置的会话自定义名称和颜色
- **Fixed**：配置了 `language` 设置时响应中的变音符号（重音符、变元音、软音符）被丢弃
- **Fixed**：`--teleport` 和 `--resume <id>` 的前置条件错误（git 树不干净、找不到会话）静默退出

---

### v2.1.107 (2026-04-14)

> 在长时间操作中更早显示 thinking 提示。

- **Improved**：thinking 提示现在在长时间操作中更早出现，以提供更好的实时反馈

---

### v2.1.105 (2026-04-13)

> EnterWorktree path 参数、PreCompact hook 阻断、插件后台监视器、/proactive 别名、WebFetch 剥离 CSS/JS、带状态图标和 f-to-fix 的 /doctor，以及多项 bug 修复。

- **New**：`EnterWorktree` 工具上的 `path` 参数——切换到当前仓库的现有 worktree
- **New**：PreCompact hook 支持——hook 可通过以代码 2 退出或返回 `{"decision":"block"}` 来阻断压缩
- **New**：通过顶层 `monitors` manifest 键为插件提供后台监视器支持——在会话开始或 skill 调用时自动布防
- **New**：`/proactive` 现在是 `/loop` 的别名
- **Improved**：停滞的 API 流现在会在 5 分钟无数据后中止并以非流式重试，而非无限期挂起
- **Improved**：网络错误消息立即显示重试，而非静默的旋转图标
- **Improved**：带状态图标的 `/doctor` 布局；按 `f` 让 Claude 修复报告的问题
- **Improved**：`WebFetch` 剥离 `<style>` 和 `<script>` 内容——CSS 繁重的页面不再在到达实际文本前耗尽内容预算
- **Improved**：`/skills` 列表中 skill 描述上限从 250 提高到 1,536 字符；描述被截断时发出启动警告
- **Improved**：过期 agent worktree 清理现在会移除其 PR 已被 squash-merge 的 worktree
- **Fixed**：附加到排队消息（在 Claude 工作时发送）的图像被丢弃
- **Fixed**：长对话中输入框换行到第二行时屏幕变空白
- **Fixed**：非美国区域 Bedrock 上的 `/model` 选择器在推理配置发现进行中时持久化了无效的 `us.*` 模型 ID
- **Fixed**：API-key、Bedrock 和 Vertex 用户的 429 速率限制错误显示原始 JSON 转储而非清晰消息
- **Fixed**：当 MCP 服务器异步连接时，headless/remote-trigger 会话首回合缺少 MCP 工具
- **Fixed**：多项崩溃和 `/resume` 失败，包括格式错误的文本块以及终端高度较短时的 `/help` 布局
- **Fixed**：某个项目设置中的 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 永久禁用所有项目的用量指标

---

### v2.1.101 (2026-04-10)

> 用于队友上手的 /team-onboarding 命令、默认信任 OS CA 证书库以支持企业 TLS 代理、/ultraplan 自动创建云环境，以及 40+ 项 bug 修复，包括 --resume 上下文丢失、Bedrock SigV4 认证、sub-agent worktree 文件访问，以及 Grep ENOENT 自愈。

- **New**：`/team-onboarding` 命令——根据你本地的 Claude Code 使用模式生成队友上手指南
- **New**：现在默认信任 OS CA 证书库——企业 TLS 代理无需额外配置即可工作；设置 `CLAUDE_CODE_CERT_STORE=bundled` 可恢复为仅使用内置 CA
- **New**：`/ultraplan` 及其他远程会话功能现在会自动创建默认云环境，而非要求先进行网页设置
- **Improved**：`claude -p --resume <name>` 现在接受通过 `/rename` 或 `--name` 设置的会话标题
- **Improved**：`settings.json` 中无法识别的 hook 事件名不再导致整个文件被忽略
- **Improved**：速率限制重试消息显示触发了哪个限制及其重置时间（而非不透明的倒计时）
- **Improved**：当 Claude 以纯文本而非结构化消息响应时，brief 模式会重试一次
- **Fixed**：当加载器锚定在死分支上时，`--resume`/`--continue` 在大型会话上丢失对话上下文
- **Fixed**：当 `ANTHROPIC_AUTH_TOKEN`、`apiKeyHelper` 或 `ANTHROPIC_CUSTOM_HEADERS` 设置了 Authorization 头部时，Bedrock SigV4 认证以 403 失败
- **Fixed**：在隔离 worktree 中运行的 sub-agent 被拒绝对其自身 worktree 内文件的 Read/Edit 访问
- **Fixed**：`RemoteTrigger` 工具的 `run` 操作发送空主体并被服务器拒绝
- **Fixed**：当内嵌 ripgrep 二进制路径过期时 Grep 工具报 ENOENT（VS Code 扩展自动更新、macOS App Translocation）——现在回退到系统 `rg` 并在会话中途自愈
- **Fixed**：硬编码的 5 分钟请求超时无视 `API_TIMEOUT_MS` 中止慢速后端（本地 LLM、extended thinking、慢速网关）
- **Fixed**：LSP 二进制检测使用的 POSIX `which` 回退中的命令注入漏洞
- **Fixed**：`permissions.deny` 规则未覆盖 PreToolUse hook 的 `permissionDecision: "ask"`
- **Fixed**：长会话在虚拟滚动器中保留数十份消息列表历史副本的内存泄漏
- **Fixed**：`/btw` 每次使用时都向磁盘写入完整对话副本

### v2.1.98 (2026-04-10)

> Vertex AI 交互式设置向导、用于后台脚本流式传输的 Monitor 工具、重大的 Bash 安全加固（修复 8+ 项权限绕过），以及子进程 PID 命名空间沙箱化。

- **New**：登录界面的交互式 Vertex AI 设置向导（选择「3rd-party platform」）——引导完成 GCP 认证、项目与区域配置、凭据验证以及模型固定
- **New**：用于从后台脚本流式传输事件的 Monitor 工具
- **New**：`CLAUDE_CODE_PERFORCE_MODE` 环境变量——Edit/Write/NotebookEdit 在只读文件上失败并给出 `p4 edit` 提示，而非静默覆盖
- **New**：当设置了 `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` 时在 Linux 上使用 PID 命名空间隔离的子进程沙箱化；`CLAUDE_CODE_SCRIPT_CAPS` 环境变量用于限制每会话脚本调用次数
- **New**：print 模式下的 `--exclude-dynamic-system-prompt-sections` 标志，用于改善跨用户 prompt caching
- **New**：启用 OTEL 追踪时向 Bash 工具子进程注入 W3C `TRACEPARENT` 环境变量
- **New**：LSP：Claude Code 现在在 initialize 请求中通过 `clientInfo` 标识自身
- **Security (Bash)**：修复了反斜杠转义标志可被自动放行为只读并执行任意代码的权限绕过
- **Security (Bash)**：修复了复合命令在 auto 和 bypass-permissions 模式下绕过强制权限提示的问题
- **Security (Bash)**：修复了带未知环境变量前缀的只读命令不弹出提示的问题（现在仅 `LANG`、`TZ`、`NO_COLOR` 等被列入安全名单）
- **Security (Bash)**：修复了 `/dev/tcp/...` 和 `/dev/udp/...` 重定向不弹出提示的问题
- **Security (Bash)**：修复了当 `grep -f FILE` / `rg -f FILE` 读取工作目录之外的模式文件时不弹出提示的问题
- **Fixed**：停滞的流式响应超时而非回退到非流式模式
- **Fixed**：批准受保护路径的 Bash 写入后，`--dangerously-skip-permissions` 静默降级为 accept-edits 模式
- **Fixed**：托管设置放行规则在管理员移除后仍保持活动状态，直到进程重启
- **Fixed**：`permissions.additionalDirectories` 更改未在会话中途生效；移除不影响 `--add-dir` 访问
- **Fixed**：令牌刷新时未遵守 MCP OAuth `oauth.authServerMetadataUrl`——修复了 ADFS 及类似 IdP
- **Fixed**：在 `Retry-After` 较小时 429 重试在约 13 秒内耗尽所有尝试——现在以指数退避作为最小值
- **Fixed**：在启用 kitty 键盘协议的 xterm/VS Code 集成终端中大写字母降为小写
- **Fixed**：macOS 文本替换删除触发词而非插入替换内容
- **Fixed**：使用 `--dangerously-skip-permissions` 时 agent 团队成员未继承领队的权限模式
- **Fixed**：`CLAUDE_CODE_MAX_CONTEXT_TOKENS` 现在遵守 `DISABLE_COMPACT`
- **Improved**：带选项卡布局的 `/agents`——Running 选项卡显示实时 subagent，Library 选项卡新增 Run 和 View 操作
- **Improved**：`/resume` 过滤提示标签；过滤指示器中的项目/worktree/分支名称
- **Improved**：Accept Edits 模式自动批准带安全环境变量或进程包装器前缀的文件系统命令
- **Improved**：带制表符/`&`/`$` 的文件上 Write 工具 diff 计算快 60%

### v2.1.97 (2026-04-09)

> 重大 bug 修复版本，在 NO_FLICKER 模式、/resume、权限和 MCP 方面有 30+ 项修复——外加 focus 视图切换和状态栏增强。

- **New**：NO_FLICKER 模式下的 focus 视图切换（`Ctrl+O`）——显示 prompt、带编辑 diffstat 的单行工具摘要以及最终响应
- **New**：`refreshInterval` 状态栏设置——每 N 秒重新运行状态栏命令
- **New**：在状态栏 JSON 输入中新增 `workspace.git_worktree` 字段，在位于链接的 git worktree 内时填充
- **New**：`/agents` 中在带实时 subagent 实例的 agent 类型旁显示 `● N running` 指示器
- **New**：Cedar 策略文件（`.cedar`、`.cedarpolicy`）的语法高亮
- **Fixed (permissions)**：批准对受保护路径的写入后，`--dangerously-skip-permissions` 静默降级为 accept-edits 模式
- **Fixed (permissions)**：名称匹配 JS 原型属性（例如 `toString`）的权限规则导致 `settings.json` 被静默忽略
- **Fixed (permissions)**：托管设置放行规则在管理员移除后仍保持活动状态，直到进程重启
- **Fixed (permissions)**：`permissions.additionalDirectories` 更改未在会话中途生效；移除目录现在会正确撤销访问而不影响 `--add-dir` 条目
- **Fixed (MCP)**：HTTP/SSE 连接在重连时累积约 50 MB/小时的未释放缓冲区
- **Fixed (MCP)**：重启后令牌刷新时未遵守 OAuth `oauth.authServerMetadataUrl`——修复了 ADFS 及类似 IdP
- **Fixed (rate limits)**：当服务器返回较小的 `Retry-After` 时 429 重试在约 13 秒内耗尽所有尝试——现在以指数退避作为最小值
- **Fixed (rate limits)**：上下文压缩后速率限制升级选项消失
- **Fixed (/resume)**：6 项修复——`--resume <name>` 打开后不可编辑、Ctrl+A 清空搜索、空列表吞掉导航、任务状态替换了对话摘要、跨项目陈旧、>10 KB 文件的文件编辑 diff 消失
- **Fixed (transcript)**：未保存的附件消息导致 `--resume` 缓存未命中；Claude 响应期间输入的消息未持久化
- **Fixed (hooks)**：`Stop`/`SubagentStop` hook 在长会话上失败；hook 评估器 API 错误显示「JSON validation failed」而非实际消息
- **Fixed (subagents)**：worktree 隔离 / `cwd:` 覆盖将工作目录泄漏回父 Bash 工具
- **Fixed (compaction)**：prompt-too-long 重试时出现重复的数 MB subagent 转录文件
- **Fixed (plugins)**：对于有更新远程提交的基于 git 的 marketplace 插件，`claude plugin update` 报告「already at latest」；当插件 frontmatter `name` 为 YAML 布尔关键字时 slash command 选择器损坏
- **Fixed (NO_FLICKER, 15 项修复)**：换行 URL 中的空格、zellij 滚动伪影、MCP 结果悬停崩溃、API 重试内存泄漏、Windows Terminal 鼠标滚轮缓慢、<24 行终端上自定义状态栏隐藏、Warp 中的 Shift+Enter/Alt+arrow、Windows 复制时 CJK 文本乱码、底栏指示器换行、跨换行的引用块左侧栏、瞬时的 context-low 通知
- **Fixed (Bedrock)**：当 `AWS_BEARER_TOKEN_BEDROCK` / `ANTHROPIC_BEDROCK_BASE_URL` 设为空字符串时（如 GitHub Actions 对未设置的输入所做的那样）SigV4 认证失败
- **Improved**：Accept Edits 模式自动批准带安全环境变量或进程包装器前缀的文件系统命令（例如 `LANG=C rm foo`、`timeout 5 mkdir out`）
- **Improved**：Auto 模式和 bypass-permissions 模式自动批准沙箱网络访问提示；`sandbox.network.allowMachLookup` 现在在 macOS 上生效
- **Improved**：粘贴和附加的图像压缩到与 Read 工具图像相同的 token 预算
- **Improved**：Slash command 和 `@` 提及补全现在在 CJK 句末标点后触发——日语/中文输入不再要求在 `/` 或 `@` 前加空格
- **Improved**：桥接会话在 claude.ai 会话卡片上显示本地 git 仓库、分支和工作目录
- **Improved**：通过跳过空 hook 条目并限制存储的编辑前文件副本来减小会话转录大小；逐块条目现在携带最终 token 用量
- **Updated**：`/claude-api` skill 在 Claude API 之外也涵盖 Managed Agents

---

### v2.1.96 (2026-04-08)

> 热修复版本，解决 v2.1.94 中引入的 Bedrock 认证回归。

- **Fixed**：使用 `AWS_BEARER_TOKEN_BEDROCK` 或 `CLAUDE_CODE_SKIP_BEDROCK_AUTH` 时 Bedrock 请求以 `403 "Authorization header is missing"` 失败（v2.1.94 的回归）

---

### v2.1.94 (2026-04-07)

> 功能版本，新增 Amazon Bedrock Mantle 支持，为专业用户提高默认 effort 级别，并改进插件 skill 命名。

- **New**：由 Mantle 驱动的 Amazon Bedrock 支持——设置 `CLAUDE_CODE_USE_MANTLE=1`
- **New**：默认 effort 级别从 medium 改为 **high**，适用于 API-key、Bedrock/Vertex/Foundry、Team 和 Enterprise 用户（用 `/effort` 控制）
- **New**：通过 `"skills": ["./"]` 声明的插件 skill 现在使用 frontmatter `name` 而非目录基名——跨安装方法保持命名稳定
- **New**：为 Slack MCP send-message 工具调用提供紧凑的 `Slacked #channel` 头部及可点击链接
- **New**：支持插件输出样式的 `keep-coding-instructions` frontmatter 字段
- **New**：`UserPromptSubmit` hook 上的 `hookSpecificOutput.sessionTitle`，用于以编程方式设置会话标题
- **Fixed**：带长 Retry-After 的 429 速率限制后 agent 卡住——错误立即浮现而非静默等待
- **Fixed**：当登录钥匙串被锁定时，macOS 上控制台登录静默失败并显示「Not logged in」——错误现在会浮现并附带 `claude doctor` 修复指引
- **Fixed**：在 YAML frontmatter 中定义的插件 skill hook 被静默忽略
- **Fixed**：长时间运行的会话中回滚显示重复的 diff 和空白页

---

### v2.1.92 (2026-04-04)

> 功能版本，新增交互式 Bedrock 向导、fail-closed 托管设置强制执行，以及 /cost 按模型细分。

- **New**：登录界面的交互式 Bedrock 设置向导（「3rd-party platform」）——分步进行 AWS 认证、区域配置、凭据验证和模型固定
- **New**：`forceRemoteSettingsRefresh` 策略设置——在托管设置被全新获取之前阻断 CLI 启动，若获取失败则以错误退出（fail-closed 强制执行）
- **New**：为订阅用户在 `/cost` 中提供按模型和缓存命中的成本细分
- **New**：`/release-notes` 现在是交互式版本选择器
- **New**：Remote Control 会话名默认以主机名为前缀（例如 `myhost-graceful-unicorn`），可用 `--remote-control-session-name-prefix` 覆盖
- **New**：Pro 用户在 prompt cache 过期后返回时会看到底栏提示，估算下一回合的未缓存 token
- **Fixed**：在 tmux 窗口被关闭或重新编号后，subagent 生成永久失败并显示「Could not determine pane count」
- **Fixed**：当 extended thinking 在真实内容旁产生仅含空白的文本块时出现 API 400 错误
- **Fixed**：Linux 沙箱 `apply-seccomp` helper 现在同时随 npm 和原生构建一起发布——恢复了对沙箱化命令的 unix-socket 阻断
- **Improved**：带制表符/`&`/`$` 的大文件上 Write 工具 diff 计算快 60%
- **Removed**：`/tag` 命令
- **Removed**：`/vim` 命令——通过 `/config` → Editor 模式切换 vim 模式

---

### v2.1.91 (2026-04-03)

> 维护版本，带 MCP 结果大小覆盖、插件可执行文件支持，以及 Edit 工具 token 缩减。

- **New**：通过 `_meta["anthropic/maxResultSizeChars"]` 注解覆盖 MCP 工具结果大小（最高 500K）——大型数据库 schema 和 API 载荷无需截断即可通过
- **New**：`disableSkillShellExecution` 设置——禁用 skill、slash commands 和插件命令中的行内 shell 执行
- **New**：插件可在 `bin/` 下提供可执行文件，供 Bash 工具直接调用而无需完整路径
- **New**：`claude-cli://open?q=` deep links 现在支持多行 prompt（接受 `%0A` 编码的换行）
- **Fixed**：异步转录写入静默失败时 `--resume` 丢失对话历史
- **Fixed**：iTerm2、Kitty、WezTerm、Ghostty、Windows Terminal 中 `cmd+delete` 无法删除到行首
- **Fixed**：远程会话中 Plan 模式在容器重启后丢失对计划文件的追踪
- **Fixed**：settings.json 中 `permissions.defaultMode: "auto"` 的 JSON schema 验证
- **Improved**：Edit 工具使用更短的 `old_string` 锚点——减少输出 token
- **Improved**：`/claude-api` skill 指引扩展了 agent 设计模式（工具表面决策、上下文管理、缓存策略）
- **Improved**：`stripAnsi` 在 Bun 上通过 `Bun.stripANSI` 快约 2 倍

---

### v2.1.90 (2026-04-02)

> 功能版本，新增 `/powerup` 交互式课程、PowerShell 工具加固，以及关键的性能/可靠性修复。

- **New**：`/powerup` 命令——通过实时终端演示教授 Claude Code 功能的交互式动画课程
- **Fixed**：触发用量限制后速率限制选项对话框反复自动打开导致会话崩溃的无限循环
- **Fixed**：对于使用延迟工具、MCP 服务器或自定义 agent 的用户，`--resume` 在首次请求时导致完全的 prompt-cache 未命中（自 v2.1.69 起的回归）
- **Fixed**：向 stdout 发出 JSON 并以代码 2 退出的 `PreToolUse` hook 未正确阻断工具调用
- **Fixed**：CLAUDE.md 自动加载期间全屏回滚中折叠的搜索/读取摘要徽章多次出现
- **Fixed**：Auto 模式不尊重明确的用户边界（「don't push」「wait for X before Y」）
- **Fixed**：滚动 `/model`、`/config` 及其他选择界面时头部消失
- **Hardened**：PowerShell 工具权限——尾部 `&` 后台作业绕过、`-ErrorAction Break` 调试器挂起、归档解压 TOCTOU、解析失败回退导致拒绝规则降级
- **Improved**：SSE 传输以线性时间处理大型流式帧（此前为二次方）
- **Improved**：消除了缓存键查找时对 MCP 工具 schema 的逐回合 JSON.stringify
- **Improved**：`/resume` 全项目视图并行加载项目会话
- **Changed**：`--resume` 选择器不再显示由 `claude -p` 或 SDK 调用创建的会话

---

### v2.1.89 (2026-04-01)

> 大型 bug 修复 + 功能版本，带新的 hook 类型、headless 工作流改进，以及值得注意的行为变更。

- **New**：`PreToolUse` hook 的 `"defer"` 权限决策——headless 会话可在某个工具调用处暂停，并以 `-p --resume` 恢复以重新评估
- **New**：`PermissionDenied` hook——在 auto 模式分类器拒绝后触发；返回 `{retry: true}` 让模型以替代方法重试
- **New**：命名的 subagent 现在出现在 `@` 提及的预输入建议中，便于调用
- **New**：`CLAUDE_CODE_NO_FLICKER=1` 环境变量，用于选用带虚拟化回滚的无闪烁备用屏幕渲染
- **New**：`-p` 模式的 `MCP_CONNECTION_NONBLOCKING=true`——跳过 MCP 连接等待；`--mcp-config` 服务器以 5s 为界
- **New**：Auto 模式被拒绝的命令现在会显示通知并出现在 `/permissions` → Recent 选项卡中
- **Changed**：交互式会话中默认不再生成 thinking 摘要——在 `settings.json` 中添加 `showThinkingSummaries: true` 以恢复
- **Improved**：`/env` 现在适用于 PowerShell 工具命令（此前仅影响 Bash）
- **Improved**：带版本对应语法指引（5.1 vs 7+）的 PowerShell 工具 prompt
- **Fixed**：`StructuredOutput` schema 缓存 bug，导致含多个 schema 的工作流约 50% 失败率
- **Fixed**：Edit/Write 工具在 Windows 上重复 CRLF 并剥离 Markdown 硬换行（两个尾随空格）
- **Fixed**：Hooks `if` 条件过滤未匹配复合命令（`ls && git push`）或带环境变量前缀的命令（`FOO=bar git push`）
- **Fixed**：会话中途工具 schema 字节变化导致的长会话 prompt cache 未命中
- **Fixed**：在读取大量文件的长会话中嵌套 CLAUDE.md 文件被重新注入数十次
- **Fixed**：内存泄漏：大型 JSON LRU 缓存键保留、LSP 诊断数据、StructuredOutput 缓存
- **Fixed**：崩溃：大型文件编辑（>1 GiB）、大型会话文件移除（>50 MB）、带旧工具结果的 `--resume`
- **Fixed**：语音模式：macOS Apple Silicon 麦克风权限、Windows WebSocket 101 错误、修饰键组合按住说话
- **Fixed**：`/stats` 丢失超过 30 天的历史数据；`/stats` 少计 subagent/fork 用量的 token
- **Fixed**：长会话中向上滚动时回滚消失；主屏终端上的渲染伪影
- **Fixed**：SDK 错误结果消息（`error_during_execution`、`error_max_turns`）现在正确设置 `is_error: true`
- **Fixed**：PreToolUse/PostToolUse hook 未为 Write/Edit/Read 工具提供绝对路径的 `file_path`

> **Breaking**：thinking 摘要现在默认关闭。在 settings.json 中设置 `showThinkingSummaries: true` 以恢复。

---

### v2.1.87 (2026-03-30)

- **Fixed**：Cowork Dispatch 中的消息未送达

---

### v2.1.86 (2026-03-28)

- **New**：向 API 请求添加 `X-Claude-Code-Session-Id` 头部——代理可按会话聚合请求而无需解析主体
- **New**：将 `.jj` 和 `.sl` 加入 VCS 目录排除列表，使 Grep 和文件自动补全不会进入 Jujutsu 或 Sapling 的元数据
- **Improved**：减少了用 `@` 提及文件时的 token 开销——原始字符串内容不再经 JSON 转义
- **Improved**：通过从工具描述中移除动态内容，提高 Bedrock、Vertex 和 Foundry 用户的 prompt cache 命中率
- **Improved**：Read 工具现在使用紧凑的行号格式并对未改动的重读去重，减少 token 用量
- **Improved**：`/skills` 列表中的 skill 描述上限为 250 字符以减少上下文占用；`/skills` 菜单现在按字母排序
- **Improved**：配置许多 claude.ai MCP 连接器时减少了启动事件循环停顿（macOS 钥匙串缓存从 5s 延长到 30s）
- **Fixed**：官方 marketplace 插件脚本自 v2.1.83 起在 macOS/Linux 上以「Permission denied」失败
- **Fixed**：`--resume` 在 v2.1.85 之前创建的会话上以「tool_use ids were found without tool_result blocks」失败
- **Fixed**：配置了条件 skill 或规则时，Write/Edit/Read 在项目根目录之外的文件（例如 `~/.claude/CLAUDE.md`）上失败
- **Fixed**：每次 skill 调用时不必要的配置磁盘写入——可能导致性能问题以及 Windows 上的配置损坏
- **Fixed**：在带大型转录文件的超长会话上使用 `/feedback` 时可能出现的内存溢出崩溃
- **Fixed**：`--bare` 模式在交互式会话中丢弃 MCP 工具，并静默丢弃回合中途入队的消息
- **Fixed**：`c` 快捷键仅复制 OAuth 登录 URL 的约 20 个字符而非完整 URL
- **Fixed**：掩码输入（例如 OAuth 代码粘贴）在窄终端上跨多行换行时泄漏令牌开头
- **Fixed**：运行多个 Claude Code 实例并使用 `/model` 时状态栏显示另一会话的模型
- **Fixed**：在长对话底部进行滚轮滚动或点击选择后滚动不跟随新消息
- **Fixed**：`/plugin` 卸载对话框：按 `n` 现在会正确卸载并保留插件的数据目录
- **Fixed**：点击后按 Enter 可能使转录保持空白直到响应到达的回归
- **Fixed**：删除关键词后 `ultrathink` 提示仍残留
- **Fixed**：markdown/highlight 渲染缓存保留完整内容字符串导致长会话内存增长
- **Fixed (VSCode)**：扩展在长时间运行操作期间错误显示「Not responding」
- **Fixed (VSCode)**：OAuth 令牌刷新后（登录 8 小时后）扩展将 Max 套餐用户默认为 Sonnet

### v2.1.85 (2026-03-27)

- **New**: hooks 新增条件 `if` 字段——使用权限规则语法（如 `Bash(git *)`）过滤 hooks 的运行时机，减少不必要的进程创建开销
- **New**: 为 MCP `headersHelper` 脚本新增 `CLAUDE_CODE_MCP_SERVER_NAME` 和 `CLAUDE_CODE_MCP_SERVER_URL` 环境变量，使一个 helper 脚本可服务多个 MCP server
- **New**: PreToolUse hooks 现在可通过在 `permissionDecision: "allow"` 的同时返回 `updatedInput` 来满足 `AskUserQuestion`——使无头集成能通过自身 UI 收集答案
- **New**: 当定时任务（`/loop`、`CronCreate`）触发时，在 transcript 中加入时间戳标记
- **New**: 深度链接查询（`claude-cli://open?q=…`）现在支持最多 5,000 个字符，对超长预填提示词会显示"滚动查看"警告
- **New**: MCP OAuth 现在遵循 RFC 9728 Protected Resource Metadata 发现机制来查找授权服务器
- **New**: 被组织策略（`managed-settings.json`）阻止的 plugins 现在会从 marketplace 视图中隐藏，且无法安装/启用
- **New**: OpenTelemetry `tool_result` 事件中的 `tool_parameters` 现在受 `OTEL_LOG_TOOL_DETAILS=1` 控制
- **Improved**: 大型 transcript 的滚动性能——将 WASM yoga-layout 替换为纯 TypeScript 实现
- **Improved**: 大型仓库上 `@`-mention 文件自动补全的性能
- **Improved**: PowerShell 危险命令检测
- **Fixed**: 当对话本身过大、compact 请求无法容纳时，`/compact` 报"context exceeded"失败的问题
- **Fixed**: `deniedMcpServers` 设置未能阻止 claude.ai MCP server 的问题
- **Fixed**: 在 Ghostty、Kitty、WezTerm 中退出后终端仍处于增强键盘模式——退出后 Ctrl+C 和 Ctrl+D 现可正常工作
- **Fixed**: `--worktree` 在非 git 仓库中于 `WorktreeCreate` hook 运行前就报错退出的问题
- **Fixed**: 当存在 refresh token 时 MCP step-up 授权失败的问题（server 通过 `403 insufficient_scope` 请求更高权限范围）
- **Fixed**: 运行某些 slash commands 后提示词卡在队列中（上方向键无法取回）的问题
- **Fixed**: 通过 SSH 或在 VS Code 集成终端中运行时，原始按键序列出现在提示词中的问题
- **Fixed**: `shift+enter` 和 `meta+enter` 被预输入建议拦截而非插入换行的问题
- **Fixed**: 权限解决后 Remote Control 会话状态卡在"Requires Action"的问题
- **Fixed**: 流式响应被中断时远程会话中的内存泄漏
- **Fixed**: Python Agent SDK：通过 `--mcp-config` 传入的 `type:'sdk'` MCP server 不再在启动时被丢弃
- **Fixed**: 当 `OTEL_LOGS_EXPORTER`、`OTEL_METRICS_EXPORTER` 或 `OTEL_TRACES_EXPORTER` 设为 `none` 时崩溃的问题
- **Fixed**: 非原生构建中 diff 语法高亮不工作的问题
- **Fixed**: 流式输出时向上滚动会渗出陈旧内容的问题

### v2.1.84 (2026-03-26)

- **New**: 面向 Windows 的 PowerShell 工具（可选预览）——在 Bash 工具之外提供直接的 PowerShell 访问。详见 https://code.claude.com/docs/en/tools-reference#powershell-tool
- **New**: 通过 `TaskCreate` 创建任务时触发 `TaskCreated` hook
- **New**: `WorktreeCreate` hook 现在支持 `type: "http"`——在响应 JSON 中通过 `hookSpecificOutput.worktreePath` 返回创建的 worktree 路径
- **New**: 为团队/企业管理员新增 `allowedChannelPlugins` 托管设置，用于定义 channel plugin 允许列表
- **New**: `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL_SUPPORTS` 环境变量，用于覆盖 Bedrock、Vertex、Foundry 上固定模型的 effort/thinking 能力检测；`_MODEL_NAME`/`_DESCRIPTION` 用于自定义 `/model` 选择器标签
- **New**: `CLAUDE_STREAM_IDLE_TIMEOUT_MS` 环境变量，用于配置流式空闲看门狗阈值（默认 90s）
- **New**: 空闲返回提示，在用户离开 75 分钟以上后引导其 `/clear`，减少陈旧会话上不必要的 token 重新缓存
- **New**: 深度链接（`claude-cli://`）现在会在你偏好的终端中打开，而非最先检测到的那个终端
- **New**: API 请求中新增 `x-client-request-id` 头，用于调试超时
- **New**: rules 和 skills 的 `paths:` frontmatter 现在接受 YAML 形式的 glob 列表
- **New**: MCP 工具描述和 server 说明上限设为 2KB，防止 OpenAPI 生成的 server 撑爆上下文
- **New**: `ANTHROPIC_CUSTOM_MODEL_OPTION` 环境变量，用于向 `/model` 选择器添加自定义条目
- **New**: 托管设置现在可通过 macOS plist 或 Windows Registry 设置
- **Improved**: 启用 `ToolSearch` 时全局系统提示词缓存现在可正常工作，包括拥有大量 MCP 工具的用户
- **Improved**: 更好的 Windows 驱动器根目录（`C:\`、`C:\Windows` 等）危险删除检测
- **Improved**: 交互式启动加快约 30ms（`setup()` 与 slash command/agent 加载并行）
- **Improved**: 统计截图（`/stats` 中按 Ctrl+S）现在在所有构建中均可用，且快 16 倍
- **Improved**: p90 提示词缓存命中率提升
- **Fixed**: 使用 Haiku 模型时 `ANTHROPIC_BETAS` 环境变量被静默忽略的问题
- **Fixed**: 部分克隆仓库（Scalar/GVFS）上触发大量 blob 下载的启动性能问题
- **Fixed**: macOS 上由瞬时 keychain 读取失败导致的虚假"Not logged in"错误
- **Fixed**: 核心工具可能在未激活其旁路的情况下被延迟的冷启动竞态（Edit/Write 报 InputValidationError 失败）
- **Fixed**: 原生终端光标未跟踪输入插入符（CJK 的 IME 输入法组合现在内联渲染）
- **Fixed**: 当外层会话使用 `--json-schema` 且子 agent 也指定 schema 时，workflow 子 agent 报 API 400 失败的问题
- **Fixed**: 为大型已编辑文件生成附件片段时卡死；重连时 MCP 工具/资源缓存泄漏
- **Fixed**: 语音按键说话（push-to-talk）泄漏字符到文本输入；转写现在插入到正确位置
- **Fixed**: 多行输入中 `Ctrl+U`（删除至行首）在行边界处无效的问题
- **Fixed**: 空解绑（Null-unbind）默认 chord 绑定后仍进入 chord 等待模式而非释放前缀键的问题
- **Changed**: 仅当写成 `owner/repo#123` 时 Issue/PR 引用才变为可点击链接——裸 `#123` 不再自动链接
- **Changed**: 当前鉴权设置下不可用的 slash commands（`/voice`、`/mobile`、`/chrome`、`/upgrade` 等）现在被隐藏而非显示
- **VSCode**: 新增带使用百分比和重置时间的限流警告横幅
- **VSCode**: 修复 Bash 工具的 Windows PATH 继承回归问题（源自 v2.1.78 的修复）

### v2.1.83 (2026-03-25)

- **New**: 与 `managed-settings.json` 并存的 `managed-settings.d/` 投放目录——不同团队可部署独立的策略片段，按字母顺序合并
- **New**: `CwdChanged` 和 `FileChanged` hook 事件，用于响应式环境管理（如 direnv、自动工具链切换）
- **New**: `sandbox.failIfUnavailable` 设置——启用 sandbox 但无法启动时报错退出，而非以非 sandbox 方式运行
- **New**: `disableDeepLinkRegistration` 设置，用于阻止 `claude-cli://` 协议处理程序注册
- **New**: `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` 会从 Bash 工具、hooks 和 MCP stdio server 子进程环境中清除 Anthropic 及云服务商凭据
- **New**: Transcript 搜索——在 transcript 模式（Ctrl+O）中按 `/` 搜索，`n`/`N` 在匹配项间逐个跳转
- **New**: `Ctrl+X Ctrl+E` 作为打开外部编辑器的别名（readline 原生绑定；`Ctrl+G` 仍可用）
- **New**: 粘贴的图片现在在光标处插入 `[Image #N]` 标记，便于在提示词中按位置引用
- **New**: agents 可在 frontmatter 中声明 `initialPrompt`，自动提交第一轮对话
- **New**: `chat:killAgents` 和 `chat:fastMode` 现在可通过 `~/.claude/keybindings.json` 重新绑定
- **Security**: 修复 `--mcp-config` CLI flag 绕过 `allowedMcpServers`/`deniedMcpServers` 托管策略强制执行的问题
- **Fixed**: macOS 上 Claude Code 退出时卡死的问题
- **Fixed**: 空闲数秒后屏幕闪烁为空白的问题
- **Fixed**: 退出后鼠标跟踪转义序列泄漏到 shell 提示符的问题
- **Fixed**: 上下文压缩后后台子 agent 变为不可见（可能导致重复 agent）的问题
- **Fixed**: `--mcp-config` CLI flag 绕过 `allowedMcpServers`/`deniedMcpServers` 托管策略的问题
- **Fixed**: 原生模块在 Amazon Linux 2 和 glibc 2.26 系统上无法加载；Linux sandbox 报"ripgrep not found"失败
- **Fixed**: 带 `saved_hook_context` 的会话导致启动性能问题
- **Fixed**: 条件式 `.claude/rules/*.md` 和嵌套 CLAUDE.md 文件在 print 模式下未加载的问题
- **Fixed**: `.claude/agents/` 中的 agents 在 git worktree 中未被发现（现从主仓库加载）
- **Improved**: `WebFetch` 在请求中标识为 `Claude-User`；二进制内容（PDF、音频）以正确扩展名保存到磁盘
- **Improved**: 将回滚缓冲（scrollback）重置从每轮一次减少到每约 50 条消息一次
- **Improved**: 提高非流式回退的 token 上限（21k → 64k）和超时（120s → 300s）
- **Changed**: "Stop all background agents" 键位绑定从 `Ctrl+F` 移至 `Ctrl+X Ctrl+K`

### v2.1.81 (2026-03-22)

- **New**: 面向脚本化 `-p` 调用的 `--bare` flag——跳过 hooks、LSP、plugin 同步和 skill 目录遍历；需通过 `--settings` 提供 `ANTHROPIC_API_KEY` 或 `apiKeyHelper`（OAuth 和 keychain 鉴权禁用）；自动记忆完全禁用
- **New**: `--channels` 权限中继——声明权限能力的 channel server 现在可将工具批准提示转发到你的手机
- **Changed**: Plan mode 默认隐藏"clear context"选项（在设置中用 `"showClearContextOnPlanAccept": true` 恢复）
- **Improved**: MCP 读取/搜索工具调用折叠为单行"Queried {server}"（用 Ctrl+O 展开）
- **Improved**: `!` bash 模式的可发现性——需要运行交互式命令时 Claude 现在会建议它
- **Improved**: Plugin 时效性——ref 跟踪的 plugins 每次加载时重新 clone 以获取上游更改
- **Improved**: Remote Control 会话标题在你发送第三条消息后刷新；`/rename` 现在为 RC 会话同步标题
- **Improved**: MCP OAuth 更新为支持 Client ID Metadata Document（CIMD / SEP-991），用于不支持 Dynamic Client Registration 的 server
- **Fixed**: 恢复 worktree 会话现在会自动切回该 worktree
- **Fixed**: 当一个会话刷新其 OAuth token 时多个并发会话需要反复重新鉴权的问题
- **Fixed**: 语音模式静默吞掉重试失败并显示误导性的"check your network"消息；当 server 静默断开 WebSocket 时语音音频无法恢复
- **Fixed**: `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` 未抑制结构化输出 beta 头（在 Vertex/Bedrock 代理上导致 400 错误）
- **Fixed**: 当任务在轮询间隔之间完成时，后台 agent 任务输出可能无限期卡死的竞态条件
- **Fixed**: 在响应进行中使用 `/btw` 时不包含粘贴文本的问题
- **Fixed**: 会话中途删除 plugin 目录时 plugin hooks 阻塞提示词提交的问题
- **Fixed**: Remote Control `/exit` 未可靠归档会话的问题
- **Fixed**: Node.js 18 崩溃
- **Fixed**: 字符串中包含连字符的 Bash 命令产生不必要权限提示的问题
- **Disabled**: 由于渲染问题，在 Windows（包括 Windows Terminal 中的 WSL）上禁用逐行响应流式输出
- **VSCode**: 修复使用 Git Bash 时 Bash 工具的 Windows PATH 继承问题（v2.1.78 中的回归）

### v2.1.80 (2026-03-20)

- **New**: statusline 脚本中新增 `rate_limits` 字段，用于显示 Claude.ai 限流使用情况（5 小时和 7 天窗口，含 `used_percentage` 和 `resets_at`）
- **New**: `source: 'settings'` plugin marketplace 源——在 `settings.json` 中内联声明 plugin 条目
- **New**: 除文件模式匹配外，新增基于 CLI 工具使用的 plugin 提示检测
- **New**: skills 和 slash commands 支持 `effort` frontmatter，在调用时覆盖模型 effort 级别
- **New**: `--channels`（research preview）——允许 MCP server 向你的会话推送消息
- **Fixed**: `--resume` 丢弃并行工具结果——含并行工具调用的会话现在会恢复所有 tool_use/tool_result 对，而非显示 `[Tool result missing]` 占位符
- **Fixed**: 由 Cloudflare 对非浏览器 TLS 指纹的机器人检测引起的语音模式 WebSocket 失败
- **Fixed**: 通过 API 代理、Bedrock 或 Vertex 使用细粒度工具流式输出时的 400 错误
- **Fixed**: `/remote-control` 出现在无法运行它的 gateway 和第三方 provider 部署中的问题
- **Fixed**: 当 `remote-settings.json` 从上一会话缓存时，托管设置未在启动时应用的问题
- **Performance**: 大型仓库启动时内存减少约 80MB（在 25 万文件仓库上测试）
- **Improved**: 大型 git 仓库中 `@` 文件自动补全的响应速度；`/effort` 现在显示 auto 当前解析为什么
- **Improved**: `/permissions`——Tab 和方向键现在可在列表内切换标签页；后台任务面板左方向键关闭列表视图

### v2.1.79 (2026-03-19)

- **New**: 为 `claude auth login` 新增 `--console` flag，用于 Anthropic Console（API 计费）鉴权
- **New**: `/config` 菜单中新增"Show turn duration"开关
- **Fixed**: 当作为子进程生成且无显式 stdin 时（如 Python `subprocess.run`）`claude -p` 卡死的问题
- **Fixed**: `-p`（print）模式下 Ctrl+C 不工作的问题
- **Fixed**: 流式输出期间触发 `/btw` 时返回主 agent 输出而非回答副问题的问题
- **Fixed**: 设置 `voiceEnabled: true` 时语音模式启动时未正确激活的问题
- **Fixed**: 企业用户在限流（429）错误时无法重试的问题
- **Fixed**: 使用交互式 `/resume` 切换会话时 `SessionEnd` hooks 未触发的问题
- **Fixed**: 工作区信任阻止时自定义状态栏显示为空的问题
- **Fixed**: `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` 未阻止启动时设置终端标题的问题
- **Performance**: 在所有场景下将启动内存使用改善约 18MB
- **Performance**: 非流式 API 回退现在有 2 分钟的单次尝试超时（防止无限期卡死）
- **VSCode**: 新增 `/remote-control` 以将会话桥接到 claude.ai/code，供浏览器/手机继续使用
- **VSCode**: 会话标签页现在基于首条消息获得 AI 生成的标题
- **VSCode**: 修复响应完成后 thinking 标记显示"Thinking"而非"Thought for Ns"的问题

### v2.1.78 (2026-03-18)

- **New**: `StopFailure` hook 事件，在轮次因 API 错误（限流、鉴权失败等）结束时触发
- **New**: `${CLAUDE_PLUGIN_DATA}` 变量用于在 plugin 更新后仍保留的 plugin 持久状态；`/plugin uninstall` 现在会在删除 plugin 数据前提示
- **New**: plugin 自带的 agents 支持 `effort`、`maxTurns` 和 `disallowedTools` frontmatter
- **New**: `ANTHROPIC_CUSTOM_MODEL_OPTION` 环境变量，用于向 `/model` 选择器添加自定义条目（带可选的 `_NAME` 和 `_DESCRIPTION` 后缀变量）
- **New**: 在 tmux 中运行且设置 `set -g allow-passthrough on` 时，终端通知（iTerm2/Kitty/Ghostty 弹窗、进度条）现在可到达外层终端
- **New**: 响应文本现在在生成时逐行流式输出
- **Fixed**: ⚠️ **Security** — 设置 `sandbox.enabled: true` 但缺少依赖时静默禁用 sandbox——现在会显示可见的启动警告
- **Fixed**: ⚠️ **Security** — `deny: ["mcp__servername"]` 权限规则未在发送给模型前移除 MCP server 工具，使其能看到并尝试被阻止的工具
- **Fixed**: ⚠️ **Security** — 在 `bypassPermissions` 模式下 `.git`、`.claude` 及其他受保护目录可无提示写入
- **Fixed**: 当 API 错误触发 stop hooks 又将阻塞错误重新喂回模型时的无限循环
- **Fixed**: `cc log` 和 `--resume` 在使用了子 agent 的大型会话（>5 MB）上静默截断对话历史的问题
- **Fixed**: `sandbox.filesystem.allowWrite` 不支持绝对路径（此前需要 `//` 前缀）的问题
- **Fixed**: `--worktree` flag 未从 worktree 目录加载 skills 和 hooks 的问题
- **Fixed**: `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` 和 `includeGitInstructions` 设置未抑制系统提示词中 git 状态部分的问题
- **Fixed**: 从 Dock/Spotlight 启动 VS Code 时 Bash 工具找不到 Homebrew 及其他依赖 PATH 的二进制文件的问题
- **Fixed**: 语音模式修饰键组合按键说话键位绑定需要长按而非立即激活的问题
- **Fixed**: 语音模式在带 WSLg 的 WSL2（Windows 11）上不工作的问题
- **Fixed**: 使用 Haiku 模型时 `ANTHROPIC_BETAS` 环境变量被静默忽略的问题
- **VSCode**: 修复选择 Opus 时出现的"API Error: Rate limit reached"——模型下拉菜单不再向计划层级未知的订阅者提供 1M 上下文变体
- **Performance**: 改善恢复大型会话时的内存使用和启动时间

### v2.1.77 (2026-03-17)

- **New**: ⭐ Opus 4.6 默认最大输出 token 提升至 64k；Opus 4.6 和 Sonnet 4.6 的上限提升至 128k token
- **New**: `allowRead` sandbox 文件系统设置，用于在 `denyRead` 区域内重新允许读取访问
- **New**: `/copy N` 直接复制倒数第 N 条助手响应
- **New**: `/branch` 命令（取代 `/fork`；`/fork` 仍作为别名可用）
- **New**: `SendMessage` 现在会在后台自动恢复已停止的 agent，而非返回错误
- **Fixed**: ⚠️ **Security** — 返回 `"allow"` 的 `PreToolUse` hooks 可能绕过 `deny` 权限规则，包括企业托管设置
- **Fixed**: 当 slash-command 浮层反复打开/关闭触发重叠的二进制下载时，自动更新器累积数十 GB 内存的问题
- **Fixed**: 由于记忆提取写入与主 transcript 之间的竞态，`--resume` 静默截断最近对话历史的问题
- **Fixed**: 复合 bash 命令（如 `cd src && npm test`）上的"Always Allow"为整个字符串保存单条规则而非按子命令保存，导致出现失效规则和重复权限提示的问题
- **Fixed**: 覆盖 CRLF 文件或在 CRLF 目录中创建文件时 Write 工具静默转换行尾的问题
- **Fixed**: 当 API 回退到非流式模式时未跟踪成本和 token 用量的问题
- **Fixed**: `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` 未剥离 beta 工具 schema 字段，导致代理网关拒绝请求的问题
- **Fixed**: 当系统临时目录路径含空格时 Bash 工具对成功命令报错的问题
- **Fixed**: 粘贴后立即输入导致粘贴内容丢失；`/feedback` 中 Ctrl+D 向前删除而非退出的问题
- **Fixed**: 多项渲染修复：有序列表编号、CJK 渗出、tmux 中的背景色、VS Code 中超链接打开两次
- **Fixed**: leader 退出时 teammate 窗格未关闭；通过 SSH 在 tmux 内选择文本时 iTerm2 会话崩溃
- **Breaking**: `Agent` 工具不再接受 `resume` 参数——使用 `SendMessage({to: agentId})` 来继续之前生成的 agent
- **VSCode**: 修复含逗号的 gitignore 模式静默将文件类型从 `@`-mention 文件选择器中排除的问题；改善滚轮响应；改善 plan 预览标签标题
- **Performance**: macOS 上启动更快（约 60ms），通过与模块加载并行读取 keychain 凭据实现；fork 密集型会话上 `--resume` 更快（最高快 45%，峰值内存减少 100-150MB）

### v2.1.76 (2026-03-14)

- **New**: ⭐ MCP elicitation 支持——MCP server 现在可在任务中途通过交互式对话框（表单字段或浏览器 URL）请求结构化输入
- **New**: `Elicitation` 和 `ElicitationResult` hooks，用于在 MCP 输入响应发回 server 前拦截和覆盖
- **New**: `PostCompact` hook，在压缩完成后触发
- **New**: `-n` / `--name <name>` CLI flag，在启动时为会话设置显示名称
- **New**: 面向大型 monorepo 中 `claude --worktree` 的 `worktree.sparsePaths` 设置——通过 git sparse-checkout 仅检出所需目录
- **New**: `/effort` slash command，用于设置模型 effort 级别
- **Fixed**: 延迟工具（通过 `ToolSearch` 加载）在对话压缩后丢失其输入 schema——数组和数字参数被类型错误拒绝的问题
- **Fixed**: 连续失败后自动压缩无限期重试——断路器现在在 3 次尝试后停止
- **Fixed**: 当带引号的参数含 `#` 时 `Bash(cmd:*)` 权限规则不匹配的问题
- **Fixed**: slash commands 显示"Unknown skill"的问题
- **Fixed**: Plan mode 在 plan 已被接受后仍要求重新批准的问题
- **Fixed**: 当权限对话框或 plan 编辑器打开时语音模式吞掉按键的问题
- **Fixed**: 通过 npm 安装时 `/voice` 在 Windows 上不工作的问题
- **Fixed**: 桥接会话在长时间 WebSocket 断开后无法恢复的问题
- **Improved**: `--worktree` 启动性能，通过直接读取 git refs、跳过冗余的 `git fetch` 实现
- **Improved**: 终止后台 agent 现在会在对话上下文中保留其部分结果
- **Improved**: 模型回退通知——现在始终可见，并使用易读的模型名称
- **Improved**: 陈旧 worktree 清理——并行运行中断后遗留的 worktree 会被自动清理
- **Improved**: 深色终端主题上的块引用可读性——改为带左侧竖条的斜体而非暗淡显示
- **Updated**: `--plugin-dir` 现在仅接受一个路径；多个目录请重复使用该 flag
- **VSCode**: 修复含逗号的 gitignore 模式静默将整个文件类型从 `@`-mention 文件选择器中排除的问题

### v2.1.75 (2026-03-13)

- **New**: ⭐ Opus 4.6 的 1M 上下文窗口现在对 Max、Team 和 Enterprise 计划默认启用（此前需额外用量）
- **New**: 使用 `/rename` 时在提示栏上显示会话名称
- **New**: 记忆文件上的最后修改时间戳——帮助 Claude 推断记忆的新鲜度
- **New**: 当 hook 需要确认时，在权限提示中显示 hook 来源（settings/plugin/skill）
- **New**: `/color` 命令向所有用户开放，用于设置提示栏颜色
- **Fixed**: thinking 和 `tool_use` 块的 token 估算偏高（导致过早的上下文压缩）的问题
- **Fixed**: Bash 工具在管道命令中破坏 `!` 的问题（如 `jq 'select(.x != .y)'` 现在可正常工作）
- **Fixed**: 全新安装时无需切换两次 `/voice` 语音模式即未正确激活的问题
- **Fixed**: 使用 `/model` 或 Option+P 切换后 Claude Code 头部未更新模型名称的问题
- **Fixed**: 当附件消息计算返回 undefined 值时会话崩溃的问题
- **Fixed**: 被托管禁用的 plugins 出现在 `/plugin` Installed 标签页的问题
- **Fixed**: 损坏的 marketplace 配置路径处理
- **Fixed**: `/resume` 在恢复 fork 或继续的会话后丢失会话名称的问题
- **Improved**: macOS 非 MDM 机器上的启动性能（跳过不必要的子进程生成）
- **Improved**: 默认抑制异步 hook 完成消息（用 `--verbose` 或 transcript 模式可见）

### v2.1.74 (2026-03-12)

- **New**: `/context` 命令显示可操作建议——识别上下文密集型工具、记忆膨胀、容量警告，并给出优化提示
- **New**: `autoMemoryDirectory` 设置，用于配置自动记忆存储的自定义目录
- **Fixed**: 流式 API 响应缓冲区的内存泄漏——已解决 Node.js/npm 路径上无限制的 RSS 增长
- **Fixed**: 托管策略的 `ask` 规则被用户 `allow` 规则或 skill `allowed-tools` 绕过的问题
- **Fixed**: 当回调端口已被占用时 MCP OAuth 鉴权卡死的问题
- **Fixed**: MCP OAuth 刷新（Slack）在 refresh token 过期后从不提示重新鉴权的问题
- **Fixed**: macOS 原生二进制上的语音模式——二进制现在包含 `audio-input` 权限以触发麦克风权限提示
- **Fixed**: 无论 `hook.timeout` 为何，`SessionEnd` hooks 都在 1.5s 后被终止（现在可通过 `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` 配置）
- **Changed**: `--plugin-dir` 本地开发副本现在覆盖同名的已安装 marketplace plugins
- **VSCode**: 修复删除按钮对 Untitled 会话不工作的问题

### v2.1.73 (2026-03-11)

- **New**: `modelOverrides` 设置——将模型选择器条目映射到自定义 provider 模型 ID（Bedrock inference profile ARN 等）
- **New**: 当 OAuth 登录或连接检查因 SSL 证书错误（企业代理、`NODE_EXTRA_CA_CERTS`）失败时给出可操作指引
- **Fixed**: 复杂 bash 命令的权限提示触发的卡死和 100% CPU 循环
- **Fixed**: 大量 skill 文件同时变更时的死锁（如在含大型 `.claude/skills/` 目录的仓库中执行 `git pull`）
- **Fixed**: 在同一项目目录中运行多个 Claude Code 会话时 Bash 工具输出丢失的问题
- **Fixed**: 带 `model: opus`/`sonnet`/`haiku` 的子 agent 在 Bedrock、Vertex、Foundry 上被静默降级的问题
- **Fixed**: agent 退出时子 agent 的后台 bash 进程未被清理的问题
- **Fixed**: 通过 `--resume` 或 `--continue` 恢复时 `SessionStart` hooks 触发两次的问题
- **Fixed**: JSON 输出 hooks 在每轮向模型上下文注入无操作 system-reminder 消息的问题
- **Fixed**: Linux sandbox 在原生构建上报"ripgrep not found"失败的问题
- **Fixed**: Amazon Linux 2（glibc 2.26 系统）上的 Linux 原生模块问题
- **Changed**: Bedrock、Vertex、Foundry 上默认 Opus 模型 → Opus 4.6（原为 4.1）
- **Changed**: 弃用 `/output-style`——改用 `/config`；输出样式在会话开始时固定以获得更好的提示词缓存
- **VSCode**: 修复代理后或在 Bedrock/Vertex 上使用 Claude 4.5 模型的用户的 HTTP 400 错误

### v2.1.72 (2026-03-09)

- **New**: 恢复了 Agent 工具上的 `model` 参数——按调用覆盖模型回来了
- **New**: `/plan` 接受可选描述（如 `/plan fix the auth bug`），进入 plan mode 并立即开始
- **New**: `ExitWorktree` 工具，用于离开 `EnterWorktree` 会话
- **New**: `CLAUDE_CODE_DISABLE_CRON` 环境变量，用于在会话中途停止定时 cron 任务
- **New**: `lsof`、`pgrep`、`tput`、`ss`、`fd`、`fdfind` 加入 bash 自动批准允许列表
- **New**: `/copy` 的 `w` 键将选区直接写入文件，绕过剪贴板（在 SSH 上很有用）
- **Changed**: 简化 effort 级别为 low/medium/high（移除 max），新符号 ○ ◐ ●；用 `/effort auto` 重置
- **Changed**: CLAUDE.md HTML 注释（`<!-- ... -->`）在自动注入时现在对 Claude 隐藏（通过 Read 工具可见）
- **Changed**: `/config`——Escape 取消更改，Enter 保存并关闭，Space 切换设置
- **Fixed**: SDK `query()` 提示词缓存失效——输入 token 成本最高降低 12 倍
- **Fixed**: 设置 `ENABLE_TOOL_SEARCH` 时工具搜索现在会随 `ANTHROPIC_BASE_URL` 一起激活
- **Fixed**: 当启用 hooks 的 skill 被模型调用时 skill hooks 每个事件触发两次的问题
- **Fixed**: `/clear` 终止后台 agent/bash 任务——现在仅清除前台任务
- **Fixed**: Worktree 隔离：Task 工具恢复时未恢复 cwd，后台任务通知缺少 `worktreePath`/`worktreeBranch`
- **Fixed**: `--compact` 后 `--continue` 未从最近点恢复的问题
- **Fixed**: 团队 agents 现在继承 leader 的模型
- **Fixed**: 并行工具调用——现在仅 Bash 错误级联到同级（Read/WebFetch/Glob 失败不再取消同级）
- **Fixed**: 多个 hooks 问题：恢复/fork 会话的 `transcript_path` 错误、异步 hooks 未收到 stdin、PostToolUse 阻止原因显示两次
- **Fixed**: 若干 sandbox 权限、plugin 安装（Windows/OneDrive）和语音模式问题
- **Perf**: 包体积减少约 510 KB；改善长会话中的 CPU 利用率；通过原生模块加快 bash 初始化

### v2.1.69 (2026-03-04)

- **Security**: 修复嵌套 skill 发现从 `node_modules` 等 gitignored 目录加载 skills 的问题——关键安全修复
- **Security**: 修复 `acceptEdits` 模式下允许在工作目录外写入的符号链接绕过问题
- **Security**: 修复信任对话框在首次运行时静默启用所有 `.mcp.json` server 的问题（现在需要按 server 批准）
- **Security**: 修复启用 `allowManagedDomainsOnly` 时 sandbox 未阻止非允许域名的问题
- **New**: `InstructionsLoaded` hook 事件，在 CLAUDE.md 或 `.claude/rules/*.md` 文件加载进上下文时触发
- **New**: 所有 hook 事件新增 `agent_id`、`agent_type`、`worktree` 字段（子 agent 跟踪、worktree 元数据）
- **New**: `${CLAUDE_SKILL_DIR}` 变量，供 skills 在 SKILL.md 内容中引用自身安装目录
- **New**: `/reload-plugins` 命令，无需重启 Claude Code 即可激活待处理的 plugin 更改
- **New**: 语音 STT 扩展至 20 种语言（+10：俄语、波兰语、土耳其语、荷兰语、乌克兰语、希腊语、捷克语、丹麦语、瑞典语、挪威语）
- **New**: `sandbox.enableWeakerNetworkIsolation` 设置（macOS），用于 MITM 代理后的 Go 工具（gh、gcloud、terraform）
- **New**: `includeGitInstructions` 设置（及 `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` 环境变量），用于从系统提示词中移除内置的 commit/PR 说明
- **New**: 面向具有自定义 OAuth 发现的 MCP server 的 `oauth.authServerMetadataUrl` 配置选项
- **New**: 托管设置中的 `pluginTrustMessage`，用于组织特定的 plugin 信任上下文
- **New**: `/remote-control` 的可选 `--name` 参数，用于设置在 claude.ai/code 中可见的自定义会话标题
- **Changed**: Pro/Max/Team 上的 Sonnet 4.5 用户自动迁移至 Sonnet 4.6
- **Changed**: `/resume` 选择器现在显示最近的提示词而非第一个
- **Fixed**: 15+ 处内存泄漏——React Compiler memoCache、REPL 渲染作用域（1000 轮约 35MB）、teammate 历史固定、hook 事件累积
- **Fixed**: 约 16MB 基线内存减少（延迟 Yoga WASM 预加载）
- **Fixed**: MCP 二进制内容（PDF、Office 文档、音频）现在以正确扩展名保存到磁盘，而非在上下文中以原始 base64 形式存在
- **Fixed**: 启动性能——skills/plugins 加载、worktree git 子进程、macOS keychain、托管设置
- **Fixed**: 当输入框有草稿文本时 Escape 未中断运行中轮次的问题
- **Fixed**: 从嵌套 worktree 运行时 CLAUDE.md、slash commands、agents 和 rules 重复的问题
- **Fixed**: 多个 OAuth MCP server 导致的 macOS keychain 损坏（stdin 缓冲区溢出）

### v2.1.68 (2026-03-04)

- **Changed**: Opus 4.6 现在对 Max 和 Team 订阅者默认采用 medium effort（速度与彻底性之间的最佳平衡点）
- **New**: 重新引入 `ultrathink` 关键词，专门为下一轮启用 high effort
- **Breaking**: Opus 4 和 Opus 4.1 从 Claude Code 的第一方 API 中移除——用户自动迁移至 Opus 4.6

### v2.1.66 (2026-03-04)

- **Fixed**: 减少虚假错误日志

### v2.1.63 (2026-02-27)

- **New**: HTTP hooks——hooks 现在可向 URL `POST` JSON 并接收返回的 JSON，而非运行 shell 命令。适用于 CI/CD 集成和无状态后端端点（v2.1.63+）
- **New**: 项目配置和自动记忆现在在同一仓库的所有 git worktree 间共享
- **New**: `/simplify` 和 `/batch` 内置 slash commands
- **New**: `ENABLE_CLAUDEAI_MCP_SERVERS=false` 环境变量，用于选择退出 claude.ai MCP server 暴露
- **Improved**: `/model` 命令在选择器中显示当前活动模型
- **Fixed**: 大批内存泄漏——WebSocket 监听器、MCP 缓存、git 根目录检测缓存、JSON 解析缓存、bash 前缀缓存、压缩后子 agent AppState、重连时 MCP server fetch 缓存
- **Fixed**: VSCode 远程会话未出现在对话历史中的问题
- **Fixed**: `/clear` 未重置已缓存 skills（陈旧 skill 内容残留到新对话）的问题
- **Fixed**: 本地 slash command 输出（如 `/cost`）在 UI 中显示为用户消息的问题

### v2.1.62 (2026-02-27)

- **Fixed**: 降低缓存命中率的提示词建议缓存回归

### v2.1.61 (2026-02-27)

- **Fixed**: Windows 上并发写入损坏配置文件的问题

### v2.1.59 (2026-02-26)

- **New**: 自动记忆——Claude 自动将有用的上下文保存到记忆；用 `/memory` 管理
- **New**: `/copy` 命令——存在代码块时弹出交互式选择器，可选择单个代码块或完整响应
- **Improved**: 复合 bash 命令更智能的"always allow"前缀建议（按子命令前缀而非将整条命令视为一体）
- **Improved**: 多 agent 会话中的内存使用（释放已完成的子 agent 任务状态）
- **Improved**: 短任务列表的排序
- **Fixed**: 同时运行多个 Claude Code 实例时 MCP OAuth token 刷新的竞态条件
- **Fixed**: 工作目录已被删除时 shell 命令未显示清晰错误消息的问题
- **Fixed**: 多个 Claude Code 实例同时运行时可能清除鉴权的配置文件损坏问题

### v2.1.58 (2026-02-26)

- **Expanded**: Remote Control 向更多用户开放

### v2.1.56 (2026-02-25)

- **Fixed**: VSCode：另一处导致"command 'claude-vscode.editor.openLast' not found"崩溃的原因

### v2.1.55 (2026-02-25)

- **Fixed**: BashTool 在 Windows 上以 EINVAL 错误失败的问题

### v2.1.53 (2026-02-25)

- **Fixed**: 用户输入在提交后渲染前短暂消失的 UI 闪烁
- **Fixed**: 批量终止 agent（ctrl+f）现在发送单条聚合通知而非每个 agent 一条，并正确清除命令队列
- **Fixed**: 使用 Remote Control 时优雅关闭有时遗留陈旧会话（已并行化拆除）
- **Fixed**: `--worktree` flag 有时在首次启动时被忽略的问题
- **Fixed**: Windows 上的 panic（"switch on corrupted value"）
- **Fixed**: Windows 上生成大量进程时崩溃
- **Fixed**: Linux x64 和 Windows x64 上 WebAssembly 解释器崩溃
- **Fixed**: Windows ARM64 上有时在 2 分钟后发生的崩溃

### v2.1.52 (2026-02-24)

- **Fixed**: Windows 上 VSCode 扩展崩溃（"command 'claude-vscode.editor.openLast' not found"）

### v2.1.51 (2026-02-24)

- **New**: 面向外部构建的 `claude remote-control` 子命令——为所有用户启用本地环境服务
- **New**: 从 npm 源安装 plugins 时支持自定义 npm 注册表和特定版本固定
- **New**: SDK：`CLAUDE_CODE_ACCOUNT_UUID`、`CLAUDE_CODE_USER_EMAIL`、`CLAUDE_CODE_ORGANIZATION_UUID` 环境变量，用于同步提供账户信息（消除早期遥测中的竞态条件）
- **Changed**: 当 shell 快照可用时，BashTool 现在默认跳过登录 shell（`-l` flag）——性能改进（此前需要 `CLAUDE_BASH_NO_LOGIN=true`）
- **Changed**: 大于 50K 字符的工具结果现在持久化到磁盘（此前阈值为 100K）
- **Improved**: `/model` 选择器现在为固定版本显示易读标签（如 "Sonnet 4.5"）而非原始模型 ID，并在有更新版本时给出升级提示
- **Fixed**: 在交互模式下 `statusLine` 和 `fileSuggestion` hook 命令可在未接受工作区信任的情况下执行的安全问题
- **Fixed**: WebSocket 重连产生的重复 `control_response` 消息导致 API 400 错误的问题
- **Fixed**: 当 plugin 的 SKILL.md 描述是 YAML 数组或其他非字符串类型时 slash command 自动补全崩溃的问题

### v2.1.50 (2026-02-21)

- **New**: `WorktreeCreate` 和 `WorktreeRemove` hook 事件——当 agent worktree 隔离创建或移除 worktree 时进行自定义 VCS 设置/拆除
- **New**: agent 定义中的 `isolation: worktree`，用于声明式 worktree 隔离（不再需要在每次调用中设置）
- **New**: `claude agents` CLI 命令，用于列出所有已配置的 agents
- **New**: LSP server 的 `startupTimeout` 配置
- **New**: `CLAUDE_CODE_DISABLE_1M_CONTEXT` 环境变量，用于禁用 1M 上下文窗口支持
- **New**: 为不支持 Dynamic Client Registration 的 MCP server（Slack）预配置 OAuth 客户端凭据；在 `claude mcp add` 时使用 `--client-id` 和 `--client-secret`
- **New**: VSCode `/extra-usage` 命令支持
- **Changed**: Opus 4.6（fast mode）现在包含完整的 1M 上下文窗口
- **Changed**: `CLAUDE_CODE_SIMPLE` 模式现在还会禁用 MCP 工具、附件、hooks 和 CLAUDE.md 加载，以获得完全最小化的体验
- **Fixed**: 当工作目录涉及符号链接时恢复的会话可能不可见的 bug
- **Fixed**: `disableAllHooks` 设置以遵循托管设置层级（非托管设置不再能禁用托管 hooks）
- **Fixed**: Linux：glibc 早于 2.30（RHEL 8）的系统上原生模块无法加载的问题
- **Fixed**: agent 团队中已完成的 teammate 任务从不被垃圾回收的内存泄漏
- **Fixed**: 已完成的任务状态对象从不从 AppState 中移除的内存泄漏
- **Fixed**: LSP 诊断数据在交付后从不清理的内存泄漏
- **Fixed**: 长会话中无限制的内存增长（文件历史快照已封顶；循环缓冲区修复；流缓冲区使用后释放）
- **Fixed**: 当启用工具搜索且提示词作为启动参数传入时未发现 MCP 工具的问题
- **Fixed**: 降低缓存命中率的提示词建议缓存回归
- **Improved**: 通过延迟 Yoga WASM 和 UI 组件导入，改善无头模式（`-p`）的启动性能
- **Improved**: 通过压缩后清除内部缓存和处理后清除大型工具结果，改善长会话期间的内存使用

### v2.1.49 (2026-02-20)

- **New**: `--worktree` / `-w` CLI flag，用于在隔离的 git worktree 中启动 Claude
- **New**: 子 agent 支持 `isolation: "worktree"`，用于在临时 git worktree 中工作
- **New**: agent 定义中的 `background: true` 字段，始终作为后台任务运行
- **New**: `ConfigChange` hook 事件——会话期间配置文件变更时触发（企业安全审计 + 阻止）
- **New**: plugins 可自带 `settings.json` 作为默认配置
- **New**: `--from-pr` flag，用于恢复关联到特定 GitHub PR 的会话（+ 通过 `gh pr create` 创建时会话自动关联）
- **New**: `PreToolUse` hooks 可向模型返回 `additionalContext`
- **New**: `plansDirectory` 设置，用于自定义 plan 文件的存储位置
- **New**: `auto:N` 语法，用于配置 MCP 工具搜索自动启用阈值
- **New**: 通过 `--init`、`--init-only` 或 `--maintenance` CLI flag 触发的 `Setup` hook 事件
- **Changed**: Sonnet 4.5 1M 上下文从 Max 计划中移除——Sonnet 4.6 现在拥有 1M 上下文（在 `/model` 中切换）
- **Changed**: Simple mode 现在包含文件编辑工具（不仅是 Bash）
- **Fixed**: 当模型遗漏仓库文件夹时，文件未找到错误现在会建议修正后的路径
- **Fixed**: 当后台 agent 运行且主线程空闲时 Ctrl+C 和 ESC 被静默忽略（现在 3s 内双击可终止所有 agent）
- **Fixed**: Plugin `enable`/`disable` 自动检测正确作用域（不再默认为用户作用域）
- **Fixed**: 上下文窗口阻塞限制计算过于激进（约 65% 而非约 98%）的问题
- **Fixed**: 并行子 agent 导致崩溃的内存问题
- **Fixed**: 长会话中流资源未清理的内存泄漏
- **Fixed**: bash 模式下 `@` 符号错误触发文件自动补全的问题
- **Fixed**: 后台 agent 结果返回原始 transcript 数据而非最终答案的问题
- **Fixed**: slash command 自动补全选错命令（如 `/context` vs `/compact`）的问题
- **Improved**: `@` mention 文件建议速度（git 仓库中约快 3 倍）
- **Improved**: MCP 连接：支持 `list_changed` 通知以实现无需重连的动态工具更新
- **Improved**: Skills 调用进度显示；skill 建议优先考虑最近/频繁使用的
- **Improved**: 异步 agent 的增量输出；token 计数包含后台 agent token

### v2.1.47 (2026-02-19)

- **Improved**: VS Code plan 预览随 Claude 迭代自动更新；仅当 plan 准备好审查时才启用评论；预览在被拒绝以待修订时保持打开
- **New**: `ctrl+f` 同时终止所有后台 agent（取代双击 ESC）；ESC 现在仅取消主线程，后台 agent 继续运行
- **New**: Stop 和 SubagentStop hook 输入新增 `last_assistant_message` 字段（无需解析 transcript 文件即可访问最终响应）
- **New**: `chat:newline` 键位绑定操作；statusline JSON workspace 部分中的 `added_dirs`
- **Fixed**: 当对话包含许多 PDF 文档时压缩失败（连同图片一起剥离文档块）的问题
- **Fixed**: Edit 工具通过替换为直引号而损坏 Unicode 弯引号（`"` `"` `'` `'`）的问题
- **Fixed**: 并行文件写入/编辑——单个文件失败不再中止同级操作
- **Fixed**: 当链接文本跨多个终端行换行时 OSC 8 超链接仅在首行可点击的问题
- **Fixed**: Bash 权限分类器现在根据实际输入规则验证匹配描述（防止幻觉权限）
- **Fixed**: 配置备份带时间戳并轮转（保留最近 5 份）而非覆盖
- **Fixed**: 上下文压缩后会话名称丢失；压缩后 plan mode 丢失
- **Fixed**: Hooks（PreToolUse、PostToolUse）在 Windows 上静默失败（现在使用 Git Bash）
- **Fixed**: 自定义 agents/skills 在 git worktree 中未被发现（现在包含主仓库 `.claude/`）
- **Fixed**: 70+ 处额外的渲染、会话、权限和平台修复

### v2.1.46 (2026-02-19)

- **修复**：macOS 上终端断开连接后残留的 Claude Code 孤儿进程
- **新增**：支持在 Claude Code 中使用 claude.ai MCP 连接器

### v2.1.45 (2026-02-17)

- **新增**：Claude Sonnet 4.6 模型支持
- **新增**：`spinnerTipsOverride` 设置——通过 `tips` 数组自定义 spinner 提示，使用 `excludeDefault: true` 可退出内置提示
- **新增**：SDK 的 `SDKRateLimitInfo` 和 `SDKRateLimitEvent` 类型，用于追踪速率限制状态（使用率、重置时间、超额）
- **修复**：Agent Teams 队友在 Bedrock、Vertex 和 Foundry 上失败的问题（环境变量现在会传播到 tmux 派生的进程）
- **修复**：macOS 上向临时文件写入时出现 Sandbox "operation not permitted" 错误
- **修复**：Task tool（后台 agents）在完成时因 `ReferenceError` 崩溃
- **改进**：大型 shell 命令输出的内存使用（RSS 不再无限增长）
- **改进**：启动性能（移除了急切的会话历史加载）
- **改进**：插件提供的命令、agents 和 hooks 在安装后立即可用（无需重启）

### v2.1.44 (2026-02-17)

- 修复：认证刷新错误

### v2.1.43 (2026-02-17)

- 修复：AWS 认证刷新无限期挂起的问题（新增 3 分钟超时）
- 修复：在 Vertex/Bedrock 上无条件发送 structured-outputs beta header 的问题
- 修复：`.claude/agents/` 目录中非 agent markdown 文件出现的虚假警告

### v2.1.42 (2026-02-14)

- **改进**：通过延迟 Zod schema 构造优化启动性能（在大型项目上更快）
- **改进**：将日期移出系统提示以提高 prompt cache 命中率（避免每日缓存失效）
- **新增**：为符合条件的用户提供 Opus 4.6 effort 提示说明（一次性引导）
- 修复：`/resume` 将中断消息显示为会话标题的问题
- 修复：图像尺寸超限错误现在会建议使用 `/compact`，而非晦涩的失败提示

### v2.1.41 (2026-02-13)

- **新增**：防止在另一个 Claude Code 会话内启动 Claude Code 的保护机制
- **新增**：`claude auth login`、`claude auth status`、`claude auth logout` CLI 子命令
- **新增**：Windows ARM64 (win32-arm64) 原生二进制支持
- 为 OTel 事件和 trace span 添加 `speed` 属性，以提升 fast mode 的可见性
- **改进**：`/rename` 在不带参数调用时会根据对话上下文自动生成会话名称
- 改进窄终端下的提示页脚布局
- 修复：Agent Teams 为 Bedrock、Vertex 和 Foundry 客户使用错误模型标识符的问题
- 修复：MCP 工具在流式传输期间返回图像内容时崩溃的问题
- 修复：`/resume` 会话预览显示原始 XML 标签而非可读命令名的问题
- 修复：向 Bedrock/Vertex/Foundry 用户显示 Opus 4.6 发布公告的问题
- 修复：Hook 阻止错误（退出码 2）未向用户显示 stderr 的问题
- 修复：在 Vertex/Bedrock 上无条件发送 structured-outputs beta header 的问题
- 修复：带锚点片段的 @-mentions 文件解析问题（例如 `@README.md#installation`）
- 修复：FileReadTool 在 FIFO、`/dev/stdin` 和大文件上阻塞的问题
- 修复：流式 Agent SDK 模式下后台任务通知未送达的问题
- 修复：向用户显示自动 compact 失败错误通知的问题
- 修复：磁盘上设置变更时陈旧权限规则未清除的问题
- 修复：权限等待时间被计入 subagent 耗时显示的问题
- 修复：plan mode 中主动 tick 触发的问题
- 改进：为 Bedrock/Vertex/Foundry 提供带回退建议的模型错误消息

### v2.1.39 (2026-02-10)

- 改进：终端渲染性能
- 修复：致命错误被吞掉而非显示的问题
- 修复：会话关闭后进程挂起的问题
- 修复：终端屏幕边界处的字符丢失问题
- 修复：详细 transcript 视图中的空行问题

### v2.1.38 (2026-02-10)

- 修复：2.1.37 引入的 VS Code 终端滚动到顶部回归问题
- 修复：Tab 键将 slash commands 加入队列而非自动补全的问题
- 修复：使用环境变量包装器的命令的 Bash 权限匹配问题
- 修复：不使用流式传输时工具调用之间的文本消失的问题
- **安全**：改进 heredoc 分隔符解析以防止命令走私
- **安全**：在 sandbox 模式下阻止向 `.claude/skills` 目录写入

### v2.1.37 (2026-02-08)

- 修复启用 `/extra-usage` 后 `/fast` 不能立即可用的问题

### v2.1.36 (2026-02-08) ⭐

- ⭐ **Fast mode 现已支持 Opus 4.6**——同样的模型，更快的输出。使用 `/fast` 切换。[了解更多](https://code.claude.com/docs/en/fast-mode)

### v2.1.34 (2026-02-07)

- 修复 agent teams 设置在渲染之间变更时的崩溃问题
- **安全修复**：当启用 `autoAllowBashIfSandboxed` 时，被排除在 sandbox 之外的命令（通过 `sandbox.excludedCommands` 或 `dangerouslyDisableSandbox`）可能绕过 Bash 询问权限规则

### v2.1.33 (2026-02-06)

**亮点**：
- **Agent teams 修复**——改进 tmux 会话处理和可用性警告
- **新增 hook 事件**——`TeammateIdle` 和 `TaskCompleted`，用于多 agent 工作流
- **Agent frontmatter 增强**：
  - `memory` 字段，用于选择 user/project/local 范围的内存
  - `Task(agent_type)` 语法，用于在 agent 定义中限制 sub-agent 派生
- **插件标识**——插件名称现在显示在 skill 描述和 `/skills` 菜单中
- **VSCode 改进**——支持远程会话，会话选择器中显示分支/消息数量
- 修复：思考中断、流式中止、代理设置、`/resume` XML 标记
- 改进：API 连接错误显示具体原因而非通用消息
- 改进：无效的托管设置错误现在能正确呈现
- 跨 agent 工作流和工具交互的多项稳定性修复

### v2.1.32 (2026-02-05) ⭐ 重大

**亮点**：
- ⭐ **Claude Opus 4.6 现已可用！**
- ⭐ **Agent teams 研究预览**——用于复杂任务的多 agent 协作（token 密集，需要 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`）
- ⭐ **自动记忆记录与回忆**——Claude 现在会在工作时自动记录并回忆记忆
- **"从此处总结"**——消息选择器现在允许对部分对话进行总结
- `--add-dir` 目录中 `.claude/skills/` 的 skills 自动加载
- 修复：`@` 文件补全在子目录中显示错误相对路径的问题
- 修复：Bash tool 不再因 JavaScript 模板字面量（例如 `${index + 1}`）抛出 "Bad substitution" 错误
- 改进：Skill 字符预算现在随上下文窗口缩放（上下文的 2%）
- 改进：`--resume` 默认复用上一次对话的 `--agent` 值
- 修复：泰语/老挝语间距元音的渲染问题
- [VSCode] 修复在有前置文本时按 Enter 错误执行 slash commands 的问题
- [VSCode] 加载历史对话列表时添加 spinner

### v2.1.31 (2026-02-03)

- **会话恢复提示**——退出消息现在会显示稍后如何继续你的对话
- **全角（zenkaku）空格支持**——添加日语 IME 复选框选择支持
- 修复：PDF 过大错误永久锁定会话的问题（现在无需开启新对话即可恢复）
- 修复：启用 sandbox 时 Bash 命令错误报告 "Read-only file system" 的问题
- 修复：项目配置缺少默认字段时 plan mode 崩溃的问题
- 修复：流式 API 路径中 `temperatureOverride` 被静默忽略的问题
- 修复：与严格语言服务器的 LSP 关闭/退出兼容性问题
- 改进：系统提示现在引导模型使用 Read/Edit/Glob/Grep 工具而非 bash 等效命令
- 改进：PDF 和请求大小错误消息显示实际限制（100 页，20MB）
- 减少：流式传输期间 spinner 出现/消失时的布局抖动

### v2.1.30 (2026-02-02)

- **⭐ PDF 页面范围支持**——Read tool 中针对 PDF 的 `pages` 参数（例如 `pages: "1-5"`），并对大型 PDF（>10 页）使用轻量引用
- **⭐ MCP 服务器的预配置 OAuth**——为没有动态客户端注册的服务器内置客户端凭据（通过 `--client-id` 和 `--client-secret` 支持 Slack）
- **⭐ 新增 `/debug` 命令**——Claude 可帮助排查当前会话问题
- **额外的 git 标志**——支持 `git log` 和 `git show` 只读标志（`--topo-order`、`--cherry-pick`、`--format`、`--raw`）
- **Task tool 指标**——结果现在包含 token 数量、工具使用次数和持续时间
- **减少动效模式**——用于无障碍的新配置选项
- 修复：API 历史中的幽灵 "(no content)" 文本块（减少 token 浪费）
- 修复：工具 schema 变更时 prompt cache 未失效的问题
- 修复：`/login` 后带思考块时出现 400 错误的问题
- 修复：`parentUuid` 循环损坏导致会话恢复挂起的问题
- 修复：为 Max 20x 用户显示错误的 "/upgrade" 速率限制提示
- 修复：权限对话框在打字时抢占焦点的问题
- 修复：subagents 无法访问 SDK MCP 工具的问题
- 修复：拥有 `.bashrc` 的 Windows 用户无法运行 bash 的问题
- 改进：`--resume` 的内存使用（多会话场景下减少 68%）
- 改进：TaskStop 显示已停止命令的描述而非通用消息
- 变更：`/model` 立即执行而非排队
- [VSCode] 在 "Other" 文本字段中添加多行输入（Shift+Enter 换行）
- [VSCode] 修复会话列表中的重复会话

### v2.1.29 (2026-01-31)

- **性能**：修复恢复带有已保存 hook 上下文的会话时的启动性能问题
- 显著提升长时间会话的恢复速度

### v2.1.27 (2026-01-29)

- **新增**：`--from-pr` 标志，用于恢复与特定 GitHub PR 编号或 URL 关联的会话
- **新增**：通过 `gh pr create` 创建的会话自动关联到 PR
- 将工具调用失败和拒绝添加到调试日志
- 修复 Bedrock/Vertex 网关用户的上下文管理验证错误
- 修复 `/context` 命令不显示彩色输出的问题
- 修复显示 PR 状态时状态栏重复后台任务指示器的问题
- [Windows] 修复拥有 `.bashrc` 文件的用户 bash 命令执行失败的问题
- [Windows] 修复派生子进程时控制台窗口闪烁的问题
- [VSCode] 修复 OAuth token 过期导致长时间会话后出现 401 错误的问题

### v2.1.25 (2026-01-30)

- 修复 Bedrock 和 Vertex 网关用户的 beta header 验证问题——确保 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` 环境变量正常工作

### v2.1.23 (2026-01-29)

- **可自定义 spinner 动词**——新增 `spinnerVerbs` 设置，允许个性化 spinner 动作词
- mTLS 和企业代理连接修复——改进对使用客户端证书、处于企业代理之后用户的支持
- 按用户隔离临时目录——防止共享系统上的权限冲突
- 改进终端渲染性能——优化屏幕数据布局以加快更新
- 修复：prompt caching 竞态条件导致的 400 错误
- 修复：headless 流式传输结束时异步 hooks 未取消的问题
- 修复：Tab 补全未更新输入字段的问题
- 修复：Ripgrep 搜索超时返回空结果而非错误的问题
- 变更：Bash 命令在显示耗时的同时显示超时时长
- 变更：已合并的 PR 在提示页脚显示紫色状态指示器
- [IDE] 修复：headless 模式下为 Bedrock 用户显示错误区域字符串的模型选项

### v2.1.22 (2026-01-28)

- 通过虚拟化改进任务 UI 性能——任务列表现在使用虚拟滚动，在任务较多时响应更佳
- Vim 选择和删除修复——修复可视模式选择和 `dw` 命令行为
- LSP 改进：Kotlin 支持、UTF-16 范围处理、更好的错误恢复
- 任务现在统一使用 `task-N` ID，而非内部 UUID
- 修复：`#` 键盘快捷键在任务创建字段中不起作用的问题
- 修复：聊天历史中紧凑工具使用的渲染问题
- 修复：git commit 消息中的会话 URL 转义问题
- 修复：命令输出处理的改进

### v2.1.21 (2026-01-28)

- **Skills/commands 可指定所需/推荐的 Claude Code 版本**——在 frontmatter 中使用 `minClaudeCodeVersion` 和 `recommendedClaudeCodeVersion`
- **新增 TaskCreate 字段**：`category`（testing、implementation、documentation 等）、`checklist`（以 markdown 列表形式的子任务）、`parentId`（任务层级）
- 会话启动时**自动检查 Claude Code 更新**（遵循自动更新设置）
- 任务出现在 `/context` 输出中，并带有 'Disable tasks' 快捷方式以便快速切换
- 改进任务 UI：添加删除按钮，更好的空状态提示
- 修复：任务删除现在能正确移除所有相关任务数据
- 修复：hook 命令中 shell 环境变量正确展开
- 修复：粘贴的带括号 URL 在 markdown 中正确格式化
- 修复：大输出命令的 Bash 输出捕获

### v2.1.20 (2026-01-27)

- **新增**：TaskUpdate tool 可通过 `status="deleted"` 删除任务
- **新增**：提示页脚中的 PR 审查状态指示器——以彩色圆点显示 PR 状态（已批准、要求更改、待处理、草稿），并附可点击链接
- 当光标无法继续移动时，vim normal mode 下使用方向键浏览历史
- 帮助菜单中添加外部编辑器快捷键 (Ctrl+G)
- 支持从 `--add-dir` 目录加载 CLAUDE.md（需要 `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`）
- 修复：会话 compaction 问题导致加载完整历史而非紧凑摘要
- 修复：agents 在活跃工作时忽略用户消息的问题
- 修复：宽字符（emoji、CJK）渲染瑕疵
- 改进：任务列表动态适应终端高度
- 变更：后台 agents 在启动前会提示工具权限
- 变更：配置备份带时间戳并轮换（保留最近 5 个）

### v2.1.19 (2026-01-25)

- **新增**：`CLAUDE_CODE_ENABLE_TASKS` 环境变量——设为 `false` 可临时回退到旧任务系统
- **新增**：自定义命令中的参数简写——使用 `$0`、`$1` 等代替冗长语法
- [VSCode] 为所有用户启用会话 forking 和回退功能
- 修复：不支持 AVX 指令的处理器上的崩溃
- 修复：终端关闭时残留的 Claude Code 进程（SIGKILL 回退）
- 修复：从不同目录恢复时（git worktrees）`/rename` 和 `/tag` 未更新正确会话的问题
- 修复：从不同目录按自定义标题恢复会话的问题
- 修复：使用 prompt stash (Ctrl+S) 并恢复时粘贴文本丢失的问题
- 修复：对于没有显式模型的 agents，agent 列表显示 "Sonnet (default)" 而非 "Inherit (default)" 的问题
- 修复：后台 hook 命令阻塞会话而非提前返回的问题
- 修复：文件写入预览省略空行的问题
- 变更：没有额外权限/hooks 的 skills 无需批准即可使用
- [SDK] 启用 `replayUserMessages` 时添加 queued_command 附件消息的重放

**⚠️ 破坏性变更**：
- 索引参数语法变更：`$ARGUMENTS.0` → `$ARGUMENTS[0]`（方括号语法）

### v2.1.18 (2026-01-24) ⭐

- ⭐ **可自定义键盘快捷键**——按上下文配置键位绑定、创建 chord 序列、个性化工作流
- 运行 `/keybindings` 即可开始
- 了解更多：[code.claude.com/docs/en/keybindings](https://code.claude.com/docs/en/keybindings)

### v2.1.17 (2026-01-23)

- 修复：不支持 AVX 指令的处理器上的崩溃

### v2.1.16 (2026-01-22) ⭐

- ⭐ **新的任务管理系统**，带依赖追踪
- [VSCode] 原生插件管理支持
- [VSCode] OAuth 用户可从 Sessions 对话框浏览并恢复远程会话
- 修复：恢复大量使用 subagent 的会话时出现内存不足崩溃的问题
- 修复：`/compact` 后 "Context remaining" 警告未隐藏的问题
- [IDE] 修复 Windows 上侧边栏视图容器不出现的竞态条件

### v2.1.15 (2026-01-22)

- **⚠️ npm 安装弃用通知**——运行 `claude install` 或查看[文档](https://docs.anthropic.com/en/docs/claude-code/getting-started)
- 通过 React Compiler 改进 UI 渲染性能
- 修复：MCP stdio 服务器超时未终止子进程，可能导致 UI 冻结的问题

### v2.1.14 (2026-01-21)

- **bash 模式下基于历史的自动补全**——输入 `!` 后跟部分命令并按 Tab，从 bash 历史中补全
- 已安装插件列表的搜索功能
- 支持将插件固定到特定 git commit SHA 以实现精确版本控制
- 修复：上下文窗口阻塞限制计算过于激进（约 65% 而非约 98%）
- 修复：使用并行 subagents 的长时间运行会话中的内存问题和泄漏
- 修复：`@` 符号在 bash 模式下错误触发文件自动补全的问题
- 修复：slash command 自动补全为相似名称选择错误命令的问题
- 改进：退格键将粘贴文本作为单个 token 删除

### v2.1.12 (2026-01-18)

- 错误修复：消息渲染

### v2.1.11 (2026-01-17)

- 修复：HTTP/SSE 传输的 MCP 连接请求过多

### v2.1.10 (2026-01-17)

- 新增 `Setup` hook 事件（--init、--init-only、--maintenance 标志）
- 键盘快捷键 'c' 用于复制 OAuth URL
- 文件建议显示为可移除的附件
- [VSCode] 插件安装计数 + 信任警告

### v2.1.9 (2026-01-16)

- **MCP 工具搜索阈值的 `auto:N` 语法**——配置 Tool Search 何时激活：`ENABLE_TOOL_SEARCH=auto:5`（5% 上下文）、`auto:10`（默认）、`auto:20`（保守）。详见 [architecture.md](./architecture.md#mcp-tool-search-lazy-loading)。
- `plansDirectory` 设置，用于自定义 plan 文件位置
- 将会话 URL 归因到来自 web 会话的 commits/PRs
- PreToolUse hooks 可返回 `additionalContext`
- skills 的 `${CLAUDE_SESSION_ID}` 字符串替换

### v2.1.7 (2026-01-15)

- `showTurnDuration` 设置，用于隐藏轮次时长消息
- **MCP Tool Search 自动模式默认启用**——当定义超过上下文的 10% 时对 MCP 工具进行延迟加载。基于 Anthropic 的 [Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use) API 功能。结果：工具定义的 **token 减少 85%**，工具选择准确性提升（Opus 4：49%→74%，Opus 4.5：79.5%→88.1%）
- 在任务通知中内联显示 agent 最终响应

**⚠️ 破坏性变更**：
- OAuth/API Console URL 变更：`console.anthropic.com` → `platform.claude.com`
- 安全修复：通配符权限规则可能匹配复合命令

### v2.1.6 (2026-01-14)

- `/config` 命令中的搜索功能
- `/stats` 中的日期范围过滤（按 `r` 循环）
- 从嵌套 `.claude/skills` 目录自动发现 skills
- `/doctor` 中显示自动更新通道的 Updates 部分

**⚠️ 安全修复**：通过 shell 行续延符绕过权限

### v2.1.5 (2026-01-13)

- `CLAUDE_CODE_TMPDIR` 环境变量，用于自定义临时目录

### v2.1.4 (2026-01-12)

- `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` 环境变量

### v2.1.3 (2026-01-11)

- 合并 slash commands 和 skills（简化心智模型）
- `/config` 中的发布通道切换（stable/latest）
- `/doctor` 对无法触及的权限规则发出警告

### v2.1.2 (2026-01-10)

- Windows Package Manager (winget) 支持
- 文件路径的可点击超链接（OSC 8 终端）
- plan mode 中用于自动接受编辑的 Shift+Tab 快捷键
- 大型 bash 输出保存到磁盘而非截断

**⚠️ 破坏性变更**：
- 安全修复：bash 命令处理中的命令注入
- 已弃用：`C:\ProgramData\ClaudeCode` 托管设置路径

### v2.1.0 (2026-01-08) ⭐ 重大

**亮点**：
- ⭐ **自动 skill 热重载**——在 `~/.claude/skills` 或 `.claude/skills` 中修改的 skills 立即可用
- ⭐ **Shift+Enter 开箱即用**，支持 iTerm2、WezTerm、Ghostty、Kitty
- ⭐ **新 Vim motions**：`;` `,` `y` `yy` `Y` `p` `P` 文本对象（`iw` `aw` `i"` 等）`>>` `<<` `J`
- **统一的 Ctrl+B**，用于将所有运行中的任务转入后台
- `/plan` 命令快捷方式，用于启用 plan mode
- 输入框任意位置的 slash command 自动补全
- `language` 设置，用于响应语言（例如 `language: "japanese"`）
- skills 的 `context: fork` 支持，用于 forked sub-agent 上下文
- agent/skill/command frontmatter 中的 hooks 支持
- MCP `list_changed` 通知支持
- 用于 web 会话的 `/teleport` 和 `/remote-env` 命令
- 使用 `Task(AgentName)` 语法禁用特定 agents
- 交互模式中的 `--tools` 标志
- frontmatter `allowed-tools` 中的 YAML 风格列表

**⚠️ 破坏性变更**：
- OAuth URL：`console.anthropic.com` → `platform.claude.com`
- 移除了进入 plan mode 的权限提示
- [SDK] 最低 zod peer dependency：`^4.0.0`

---

## 2.0.x 系列（2025 年 11 月 - 2026 年 1 月）

### v2.0.76 (2026-01-05)

- 修复：在 Chrome 中使用 Claude 时出现的 macOS 代码签名警告

### v2.0.74 (2026-01-04) ⭐

- ⭐ **LSP（Language Server Protocol）工具**，提供代码智能（跳转到定义、查找引用、悬停提示）
- `/terminal-setup` 支持 Kitty、Alacritty、Zed、Warp
- 在 `/theme` 中按 Ctrl+T 切换语法高亮
- 在 `/context` 中按来源对 skills/agents 进行分组

### v2.0.72 (2026-01-02) ⭐

- ⭐ **Claude in Chrome（Beta）** — 直接从 Claude Code 控制浏览器
- 减少终端闪烁
- 用于下载移动端 App 的二维码
- thinking 切换方式变更：Tab → Alt+T

### v2.0.70 (2025-12-30)

- Enter 键可立即接受/提交提示建议
- MCP 工具权限支持通配符语法 `mcp__server__*`
- 插件市场的自动更新开关
- 大型对话的内存占用改善 3 倍

**⚠️ 破坏性变更**：移除了用于快速录入记忆的 `#` 快捷键

### v2.0.67 (2025-12-26) ⭐

- ⭐ **Opus 4.5 默认启用 thinking 模式**
- thinking 配置移至 `/config`
- 在 `/permissions` 中可用 `/` 快捷键进行搜索

### v2.0.64 (2025-12-22) ⭐

- ⭐ **即时自动压缩（auto-compacting）**
- ⭐ **异步 agents 和 bash 命令**，附带唤醒消息
- `/stats` 提供使用图表、连续记录、常用模型
- 命名会话：`/rename`、`/resume <name>`
- 支持 `.claude/rules/` 目录
- 用于坐标映射的图像尺寸元数据

### v2.0.60 (2025-12-18) ⭐

- ⭐ **后台 agents** — agents 在你工作的同时运行
- `--disable-slash-commands` CLI 标志
- Co-Authored-By 提交中包含模型名称
- `/mcp enable|disable [server-name]`

### v2.0.51 (2025-12-10) ⭐ 重大更新

- ⭐ **Opus 4.5 发布**
- ⭐ **Claude Code for Desktop**
- 更新了 Opus 4.5 的使用限额
- Plan Mode 能够构建更精确的计划

### v2.0.45 (2025-12-05) ⭐

- ⭐ **支持 Microsoft Foundry**
- 用于自动批准/拒绝的 `PermissionRequest` hook
- 向 web 发送后台任务的 `&` 前缀

### v2.0.28 (2025-11-18) ⭐

- ⭐ **Plan mode：引入 Plan subagent**
- Subagents：恢复（resume）能力
- Subagents：动态模型选择
- `--max-budget-usd` 标志（SDK）
- 基于 Git 的插件支持分支/标签（`#branch`）

### v2.0.24 (2025-11-10)

- Claude Code Web：Web → CLI 传送（teleport）
- BashTool 的 Sandbox 模式（Linux & Mac）
- Bedrock：`awsAuthRefresh` 输出显示

---

## 破坏性变更汇总

### URLs

| 版本 | 变更 |
|---------|--------|
| v2.1.0, v2.1.7 | OAuth/API Console：`console.anthropic.com` → `platform.claude.com` |

### Windows

| 版本 | 变更 |
|---------|--------|
| v2.0.58 | 托管设置优先使用 `C:\Program Files\ClaudeCode` |
| v2.1.2 | 弃用 `C:\ProgramData\ClaudeCode` 路径 |

### SDK / Agent Tool

| 版本 | 变更 |
|---------|--------|
| v2.0.25 | 移除旧版 SDK 入口 → `@anthropic-ai/claude-agent-sdk` |
| v2.1.0 | zod 最低对等依赖：`^4.0.0` |
| v2.1.77 | `Agent` 工具不再接受 `resume` 参数 — 改用 `SendMessage({to: agentId})` |

### API 生态

| 日期 | 功能 |
|------|---------|
| 2026-01-29 | **Structured Outputs 正式发布（GA）**：`output_config.format` 取代 `output_format`。[文档](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) |
| 2026-04-30 | **1M context beta 退役**：Sonnet 4.5/4 不再接受 `context-1m-2025-08-07` 标头 — 超过 200k token 的请求会报错。请迁移到 Sonnet 4.6 或 Opus 4.6。 |

### 快捷键

| 版本 | 变更 |
|---------|--------|
| v2.0.70 | 移除了用于快速录入记忆的 `#` 快捷键 |
| v2.1.153 | `keybindings.json` 中的 `modelPicker:setAsDefault` 按键绑定重命名为 `modelPicker:thisSessionOnly` |

### 安全修复

| 版本 | 问题 |
|---------|-------|
| v2.1.2 | bash 命令处理中的命令注入 |
| v2.1.6 | shell 行延续导致的权限绕过 |
| v2.1.7 | 通配符权限规则下的复合命令 |
| v2.1.38 | 防止 heredoc 分隔符命令走私 |

### 语法

| 版本 | 变更 |
|---------|--------|
| v2.1.19 | 索引参数语法变更：`$ARGUMENTS.0` → `$ARGUMENTS[0]`（方括号语法） |

---

## 里程碑功能

| 版本 | 关键功能 |
|---------|--------------|
| **v2.1.69** | InstructionsLoaded hook、4 项安全修复、15+ 项内存修复、语音 STT 支持 20 种语言 |
| **v2.1.68** | 重新引入 ultrathink、Opus 4.6 默认 medium effort、移除 Opus 4/4.1 |
| **v2.1.63** | HTTP hooks、worktree 配置共享、捆绑命令 /simplify + /batch |
| **v2.1.32** | Opus 4.6、Agent teams 预览、自动记忆 |
| **v2.1.18** | 通过 /keybindings 自定义键盘快捷键 |
| **v2.1.16** | 带依赖跟踪的全新任务管理系统 |
| **v2.1.0** | Skill 热重载、开箱即用的 Shift+Enter、Vim 操作、/plan 命令 |
| **v2.0.74** | 提供代码智能的 LSP 工具 |
| **v2.0.72** | Claude in Chrome（浏览器控制） |
| **v2.0.67** | Opus 4.5 默认启用 thinking 模式 |
| **v2.0.64** | 即时自动压缩、异步 agents、命名会话 |
| **v2.0.60** | 后台 agents |
| **v2.0.51** | Opus 4.5、Claude Code for Desktop |
| **v2.0.45** | Microsoft Foundry、PermissionRequest hook |
| **v2.0.28** | Plan subagent、subagent 恢复/模型选择 |
| **v2.0.24** | Web 传送、Sandbox 模式 |

---

## 更新本文档

1. **关注**：[github.com/anthropics/claude-code/releases](https://github.com/anthropics/claude-code/releases)
2. **更新**：`machine-readable/claude-code-releases.yaml`（事实来源）
3. **重新生成**：相应地更新本 markdown 文件
4. **同步落地页**：运行 `./scripts/check-landing-sync.sh`

---

*最后更新：2026-03-05 | [返回主指南](../ultimate-guide.md)*
