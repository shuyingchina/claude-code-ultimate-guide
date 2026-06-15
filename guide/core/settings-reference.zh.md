# Claude Code 设置参考

> `settings.json` 配置与环境变量的完整参考。涵盖截至 Claude Code v2.1.162 已确认的所有设置。

**来源：** [官方设置文档](https://code.claude.com/docs/en/settings) · [官方环境变量文档](https://code.claude.com/docs/en/env-vars) · [JSON Schema](https://json.schemastore.org/claude-code-settings.json)

**图例：**
- 无标记 = 已在官方文档中确认
- `📋 Schema only` = 存在于 JSON schema 中但不在官方设置页面上 —— 仍然有效
- `⚠️ Unverified` = 未在官方来源中确认

---

## 作用域与优先级

Claude Code 使用四种设置作用域，按从高到低的优先级应用：

| 优先级 | 作用域 | 位置 | 是否共享？ | 用途 |
|----------|-------|----------|---------|---------|
| 1 | **托管（Managed）** | 服务器、MDM 配置文件、注册表或系统级 `managed-settings.json` | 是（由 IT 部署） | 组织级策略，无法被覆盖 |
| 2 | **命令行** | 启动时的 `--` 标志 | 否 | 临时会话覆盖 |
| 3 | **本地（Local）** | `.claude/settings.local.json` | 否（gitignored） | 个人的项目专属设置 |
| 4 | **项目（Project）** | `.claude/settings.json` | 是（已提交） | 团队共享设置 |
| 5 | **用户（User）** | `~/.claude/settings.json` | 否 | 全局个人默认值 |

**数组合并：** 像 `permissions.allow`、`sandbox.filesystem.allowWrite` 和 `allowedHttpHookUrls` 这样的设置会跨作用域拼接并去重 —— 而非替换。

**拒绝优先：** `permissions.deny` 规则始终生效，无论任何作用域下的 allow/ask 规则如何。

**托管设置的交付方式：**
- 服务器托管（Claude.ai 管理控制台）
- macOS MDM：`com.anthropic.claudecode` plist
- Windows 注册表：`HKLM\SOFTWARE\Policies\ClaudeCode`
- 文件：位于 `/Library/Application Support/ClaudeCode/`（macOS）、`/etc/claude-code/`（Linux/WSL）、`C:\Program Files\ClaudeCode\`（Windows）的 `managed-settings.json`
- 插入式目录：与 `managed-settings.json` 并列的 `managed-settings.d/*.json`，按字母顺序合并

**其他配置：** `~/.claude.json` 存储 OAuth 会话、MCP 服务器配置、按项目的信任状态，以及诸如 `editorMode` 之类的偏好。不要将 `~/.claude.json` 的键放入 `settings.json` —— 这会触发 schema 校验错误。

---

## 设置键

### 核心配置

#### `$schema`
**类型：** string
**作用域：** all
**默认值：** none

用于 IDE 校验和自动补全的 JSON Schema URL。添加 `"https://json.schemastore.org/claude-code-settings.json"` 即可在 VS Code、Cursor 及其他编辑器中启用内联校验。

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json"
}
```

#### `model`
**类型：** string
**作用域：** all
**默认值：** `"default"`

覆盖所有会话的默认模型。接受别名（`"sonnet"`、`"opus"`、`"haiku"`、`"opusplan"`）或完整的模型 ID，如 `"claude-sonnet-4-6"`。`ANTHROPIC_MODEL` 环境变量优先级更高。

```json
{ "model": "opus" }
```

#### `agent`
**类型：** string
**作用域：** all
**默认值：** none

将主线程作为某个命名的 subagent 运行。应用该 agent 的系统提示、工具限制和模型。该值必须匹配 `.claude/agents/` 中定义的某个 agent。也可通过 `--agent` CLI 标志使用。

```json
{ "agent": "code-reviewer" }
```

#### `language`
**类型：** string
**作用域：** all
**默认值：** `"english"`

Claude 的首选响应语言。同时也设置语音听写的语言。示例：`"japanese"`、`"spanish"`、`"french"`。

#### `cleanupPeriodDays`
**类型：** number
**作用域：** all
**默认值：** `30`

闲置时间超过此天数的会话会在启动时被删除。设为 `0` 会在启动时删除所有现有的会话记录，并完全禁用会话持久化 —— 不会写入任何 `.jsonl` 文件，`/resume` 不显示任何对话，hooks 收到的 `transcript_path` 为空。

#### `autoUpdatesChannel`
**类型：** string
**作用域：** all
**默认值：** `"latest"`
**取值：** `"latest"` | `"stable"`

要跟随的发布渠道。`"stable"` 通常比 `"latest"` 落后约一周，并会跳过存在重大回退的版本。

#### `alwaysThinkingEnabled`
**类型：** boolean
**作用域：** all
**默认值：** `false`

为所有会话默认启用 extended thinking。通常通过 `/config` 配置，而非直接编辑。

#### `includeGitInstructions`
**类型：** boolean
**作用域：** all
**默认值：** `true`

在系统提示中包含内置的 commit 和 PR 工作流说明以及一份 git 状态快照。当使用自定义的 git 工作流 skill 时设为 `false`。`CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` 环境变量优先级更高。

#### `voiceEnabled`
**类型：** boolean
**作用域：** user
**默认值：** none

启用按住说话的语音听写。运行 `/voice` 时会自动写入。需要 Claude.ai 账户。

#### `companyAnnouncements`
**类型：** array of strings
**作用域：** all
**默认值：** none

在启动时向用户显示的公告。多条公告会随机轮换展示。

```json
{
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review code guidelines at docs.acme.com",
    "All PRs require code review before merge"
  ]
}
```

#### `availableModels`
**类型：** array of strings
**作用域：** all
**默认值：** none

限制用户可通过 `/model`、`--model`、Config 工具或 `ANTHROPIC_MODEL` 选择的模型。不影响 Default 选项。

```json
{ "availableModels": ["sonnet", "haiku"] }
```

#### `fastModePerSessionOptIn`
**类型：** boolean
**作用域：** all
**默认值：** `false`

为 `true` 时，fast mode 不会跨会话保留。每个会话启动时 fast mode 都为关闭状态，需要用户用 `/fast` 启用。用户的偏好仍会被保存。

#### `teammateMode`
**类型：** string
**作用域：** all
**默认值：** `"auto"`
**取值：** `"auto"` | `"in-process"` | `"tmux"`

agent team 队友的显示方式。`"auto"` 在 tmux 或 iTerm2 中使用分屏，其他情况下使用 in-process。

#### `showClearContextOnPlanAccept`
**类型：** boolean
**作用域：** all
**默认值：** `false`

在 plan 接受界面上显示“清除上下文”选项。设为 `true` 可恢复该选项，该选项自 v2.1.81 起默认被隐藏。

#### `feedbackSurveyRate`
**类型：** number
**作用域：** all
**默认值：** none

在符合条件时出现会话质量调查的概率（0–1）。设为 `0` 可完全抑制。在使用 Bedrock、Vertex 或 Foundry 时很有用。

#### `disableAutoMode`
**类型：** string
**作用域：** all
**默认值：** none
**取值：** `"disable"`

设为 `"disable"` 可阻止 auto mode 被激活。会从 `Shift+Tab` 循环中移除 `auto`，并在启动时拒绝 `--permission-mode auto`。

#### `useAutoModeDuringPlan`
**类型：** boolean
**作用域：** user / local
**默认值：** `true`

在 auto mode 可用时，plan mode 是否使用 auto mode 语义。不从共享的项目设置中读取。

#### `autoMode`
**类型：** object
**作用域：** user / local
**默认值：** none

自定义 auto mode 分类器。包含 `environment`、`allow` 和 `soft_deny` 等散文式规则数组。不从共享的项目设置中读取。

#### `defaultShell`
**类型：** string
**作用域：** all
**默认值：** `"bash"`
**取值：** `"bash"` | `"powershell"`

输入框 `!` 命令的默认 shell。`"powershell"` 需要 `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`。

#### `skipWebFetchPreflight` `📋 Schema only`
**类型：** boolean
**作用域：** all
**默认值：** `false`

在抓取 URL 之前跳过 WebFetch 黑名单检查。

#### `env`
**类型：** object
**作用域：** all
**默认值：** none

应用于每个会话的环境变量。使用它来设置变量，而非借助包装脚本。所有受支持的键见 [环境变量](#environment-variables) 一节。

```json
{
  "env": {
    "NODE_ENV": "development",
    "CLAUDE_CODE_EFFORT_LEVEL": "medium"
  }
}
```

---

### 计划与记忆

#### `plansDirectory`
**类型：** string
**作用域：** all
**默认值：** `"~/.claude/plans"`

`/plan` 输出的存储目录。路径相对于项目根目录。

#### `autoMemoryEnabled`
**类型：** boolean
**作用域：** all
**默认值：** `true`

启用或禁用自动记忆功能，该功能可跨会话自动保存上下文。

#### `autoMemoryDirectory`
**类型：** string
**作用域：** user / local / managed
**默认值：** none

自动记忆存储的自定义目录。接受以 `~/` 展开的路径。不接受在项目设置（`.claude/settings.json`）中设置，以防止共享仓库将记忆写入重定向到敏感位置。

---

### 权限

控制 Claude 可以执行哪些工具和操作。

#### `permissions.allow`
**类型：** array of strings
**作用域：** all
**默认值：** `[]`

允许工具在不提示的情况下使用的权限规则。数组会跨作用域拼接。见下文 [权限规则语法](#permission-rule-syntax)。

#### `permissions.ask`
**类型：** array of strings
**作用域：** all
**默认值：** `[]`

在使用工具前需要用户确认的权限规则。

#### `permissions.deny`
**类型：** array of strings
**作用域：** all
**默认值：** `[]`

阻止工具使用的权限规则。安全优先级最高 —— 无法被任何作用域下的 allow/ask 规则覆盖。

#### `permissions.additionalDirectories`
**类型：** array of strings
**作用域：** all
**默认值：** `[]`

Claude 除当前项目根目录之外还可访问的额外工作目录。

```json
{ "permissions": { "additionalDirectories": ["../shared-libs/"] } }
```

#### `permissions.defaultMode`
**类型：** string
**作用域：** all
**默认值：** `"default"`
**取值：** `"default"` | `"acceptEdits"` | `"plan"` | `"bypassPermissions"`

打开 Claude Code 时的默认权限模式。在 Remote 环境中，仅 `"acceptEdits"` 和 `"plan"` 受支持。

#### `permissions.disableBypassPermissionsMode`
**类型：** string
**作用域：** all
**默认值：** none
**取值：** `"disable"`

设为 `"disable"` 可阻止 `bypassPermissions` 模式被激活。会禁用 `--dangerously-skip-permissions` 标志。在托管设置中最为有用。

#### `allowManagedPermissionRulesOnly`
**类型：** boolean
**作用域：** managed only
**默认值：** `false`

为 `true` 时，用户和项目的 `allow`、`ask` 和 `deny` 规则会被忽略。仅托管权限规则生效。

### 权限规则语法

规则遵循 `Tool` 或 `Tool(specifier)` 的格式。求值顺序：先 deny，再 ask，最后 allow。第一条匹配的规则生效。

| 工具 | 模式 | 示例 |
|------|---------|---------|
| `Bash` | 带通配符的命令模式 | `Bash(npm run *)`、`Bash(git *)` |
| `Read` | 文件路径模式 | `Read(.env)`、`Read(./secrets/**)` |
| `Edit` | 文件路径模式 | `Edit(src/**)`、`Edit(*.ts)` |
| `Write` | 文件路径模式 | `Write(*.md)` |
| `WebFetch` | `domain:hostname` | `WebFetch(domain:example.com)` |
| `WebSearch` | 无 specifier | `WebSearch` |
| `Task` | agent 名称 | `Task(Explore)` |
| `Agent` | agent 名称 | `Agent(researcher)` |
| `MCP` | `mcp__server__tool` 或 `MCP(server:tool)` | `mcp__memory__*` |

**Read/Edit 规则的路径前缀：**

| 前缀 | 含义 |
|--------|---------|
| `//` | 从文件系统根开始的绝对路径 |
| `~/` | 相对于主目录 |
| `/` | 相对于项目根目录 |
| `./` 或无前缀 | 相对路径（当前目录） |

**Bash 通配符说明：** `*` 可在任意位置匹配。`Bash(ls *)`（`*` 前有空格）匹配 `ls -la` 但不匹配 `lsof`。`Bash(*)` 等同于 `Bash`（匹配所有命令）。旧式的 `:*` 后缀（如 `Bash(npm:*)`）已废弃。

```json
{
  "permissions": {
    "allow": ["Edit(*)", "Bash(npm run *)", "Bash(git *)"],
    "ask": ["Bash(git push *)"],
    "deny": ["Read(.env)", "Read(./secrets/**)"],
    "defaultMode": "acceptEdits"
  }
}
```

---

### Hooks

#### `hooks`
**类型：** object
**作用域：** all
**默认值：** none

配置在生命周期事件触发时运行的自定义命令。完整的 30 个 hook 事件、退出码和环境变量见 [hooks 文档](https://code.claude.com/docs/en/hooks) 以及 [指南 §7.1](../ultimate-guide.md#71-the-event-system)。

#### `disableAllHooks`
**类型：** boolean
**作用域：** all
**默认值：** `false`

禁用所有 hooks 以及任何自定义状态行。

#### `allowManagedHooksOnly`
**类型：** boolean
**作用域：** managed only
**默认值：** `false`

为 `true` 时，仅加载托管 hooks 和 SDK hooks。用户、项目和插件 hooks 会被阻止。

#### `allowedHttpHookUrls`
**类型：** array of strings
**作用域：** all
**默认值：** none（无限制）

HTTP hooks 可以指向的 URL 模式的允许列表。支持 `*` 作为通配符。一旦定义，URL 不匹配的 hooks 会被静默阻止。空数组会阻止所有 HTTP hooks。数组会跨设置来源合并。

```json
{ "allowedHttpHookUrls": ["https://hooks.example.com/*"] }
```

#### `httpHookAllowedEnvVars`
**类型：** array of strings
**作用域：** all
**默认值：** none（无限制）

HTTP hooks 可以插值到 header 值中的环境变量名称的允许列表。每个 hook 实际生效的 `allowedEnvVars` 是与此列表的交集。数组会跨设置来源合并。

---

### MCP 服务器

#### `enableAllProjectMcpServers`
**类型：** boolean
**作用域：** all
**默认值：** `false`

自动批准在项目 `.mcp.json` 文件中定义的所有 MCP 服务器。避免逐个服务器的确认提示。

#### `enabledMcpjsonServers`
**类型：** array of strings
**作用域：** all
**默认值：** none

要批准的来自 `.mcp.json` 文件的特定服务器名称的允许列表。

#### `disabledMcpjsonServers`
**类型：** array of strings
**作用域：** all
**默认值：** none

要拒绝的来自 `.mcp.json` 文件的特定服务器名称的阻止列表。

#### `allowedMcpServers`
**类型：** array
**作用域：** managed only
**默认值：** none（无限制）

用户可配置的 MCP 服务器的允许列表。每个条目按 `serverName`、`serverCommand` 或 `serverUrl` 匹配。未定义 = 无限制，空数组 = 完全锁定。

```json
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverCommand": "npx @modelcontextprotocol/*" },
    { "serverUrl": "https://mcp.company.com/*" }
  ]
}
```

#### `deniedMcpServers`
**类型：** array
**作用域：** managed only
**默认值：** none

被明确阻止的 MCP 服务器的阻止列表。适用于包括托管服务器在内的所有作用域。优先级高于 `allowedMcpServers`。

#### `allowManagedMcpServersOnly`
**类型：** boolean
**作用域：** managed only
**默认值：** `false`

为 `true` 时，仅尊重来自托管设置的 `allowedMcpServers`。用户仍可添加 MCP 服务器，但只有管理员定义的服务器可用。`deniedMcpServers` 仍会从所有来源合并。

#### `channelsEnabled`
**类型：** boolean
**作用域：** managed only
**默认值：** `false`

为 Team 和 Enterprise 用户允许 channels。当未设置或为 `false` 时，无论用户向 `--channels` 传入什么，channel 消息投递都会被阻止。

#### `allowedChannelPlugins`
**类型：** array
**作用域：** managed only
**默认值：** none（使用默认的 Anthropic 允许列表）

可推送消息的 channel 插件的允许列表。设置后会替换默认的 Anthropic 允许列表。需要 `channelsEnabled: true`。空数组会阻止所有 channel 插件。

---

### Sandbox

配置 bash 命令沙箱以增强安全性。适用于 macOS、Linux 和 WSL2。

#### `sandbox.enabled`
**Type:** boolean
**Scope:** all
**Default:** `false`

启用 bash 沙箱。将 bash 命令与你的文件系统和网络隔离开来。

#### `sandbox.failIfUnavailable`
**Type:** boolean
**Scope:** all
**Default:** `false`

当 `sandbox.enabled` 为 `true` 但沙箱无法启动（缺少依赖、平台不受支持）时，在启动阶段以错误退出。当为 `false` 时，会显示警告并以非沙箱方式运行命令。在将沙箱作为硬性门槛要求的受管部署中非常有用。

#### `sandbox.autoAllowBashIfSandboxed`
**Type:** boolean
**Scope:** all
**Default:** `true`

在沙箱内自动批准 bash 命令。当沙箱处于激活状态时，原本需要确认的 bash 命令会被自动批准。

#### `sandbox.excludedCommands`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

绕过沙箱、直接在你的环境中运行的命令。

#### `sandbox.allowUnsandboxedCommands`
**Type:** boolean
**Scope:** all
**Default:** `true`

允许命令通过 `dangerouslyDisableSandbox` 参数选择退出沙箱。设为 `false` 可实现严格沙箱模式，此时所有命令都必须在沙箱内运行或位于 `excludedCommands` 中。

#### `sandbox.enableWeakerNestedSandbox`
**Type:** boolean
**Scope:** all
**Default:** `false`

为非特权 Docker 环境启用较弱的沙箱（仅限 Linux 和 WSL2）。会降低安全性。

#### `sandbox.enableWeakerNetworkIsolation`
**Type:** boolean
**Scope:** all
**Default:** `false`

（仅限 macOS）允许访问系统 TLS 信任服务（`com.apple.trustd.agent`）。当通过 `httpProxyPort` 配合 MITM 代理和自定义 CA 使用时，基于 Go 的工具（如 `gh`、`gcloud` 和 `terraform`）需要此项。会降低安全性。

#### `sandbox.network.allowUnixSockets`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

沙箱中可访问的特定 Unix socket 路径（用于 SSH agent、Docker 等）。

#### `sandbox.network.allowAllUnixSockets`
**Type:** boolean
**Scope:** all
**Default:** `false`

允许沙箱中的所有 Unix socket 连接。会覆盖 `allowUnixSockets`。

#### `sandbox.network.allowLocalBinding`
**Type:** boolean
**Scope:** all
**Default:** `false`

允许绑定到 localhost 端口（仅限 macOS）。

#### `sandbox.network.allowedDomains`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

允许出站网络流量的域名。支持通配符，如 `*.example.com`。

#### `sandbox.network.allowManagedDomainsOnly`
**Type:** boolean
**Scope:** managed only
**Default:** `false`

当为 `true` 时，只有来自受管设置的 `allowedDomains` 和 `WebFetch(domain:...)` 允许规则会被遵守。未被允许的域名会被直接阻止，不会弹出提示。来自所有来源的被拒绝域名仍然会被遵守。

#### `sandbox.network.httpProxyPort`
**Type:** number
**Scope:** all
**Default:** none

自定义代理的 HTTP 代理端口（1–65535）。如果未指定，Claude 会运行自己的代理。

#### `sandbox.network.socksProxyPort`
**Type:** number
**Scope:** all
**Default:** none

自定义代理的 SOCKS5 代理端口（1–65535）。

#### `sandbox.network.deniedDomains` `⚠️ Unverified`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

沙箱的网络域名拒绝列表。未在官方文档中确认。

#### `sandbox.filesystem.allowWrite`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

沙箱命令可写入的额外路径。会在所有设置作用域之间合并。也会与 `Edit(...)` 允许权限规则中的路径合并。

**路径前缀约定：** `/` = 绝对路径，`~/` = 相对于 home 目录，`./` 或无前缀 = 在项目设置中相对于项目 / 在用户设置中相对于 `~/.claude`。

#### `sandbox.filesystem.denyWrite`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

沙箱命令不能写入的路径。会与 `Edit(...)` 拒绝规则合并。

#### `sandbox.filesystem.denyRead`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

沙箱命令不能读取的路径。会与 `Read(...)` 拒绝规则合并。

#### `sandbox.filesystem.allowRead`
**Type:** array of strings
**Scope:** all
**Default:** `[]`

在 `denyRead` 区域内重新允许读取访问的路径。优先级高于 `denyRead`。数组会在所有设置作用域之间合并。

#### `sandbox.filesystem.allowManagedReadPathsOnly`
**Type:** boolean
**Scope:** managed only
**Default:** `false`

当为 `true` 时，只有来自受管设置的 `allowRead` 路径会被遵守。来自用户、项目和本地设置的 `allowRead` 条目会被忽略。

**沙箱示例：**
```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["git", "docker"],
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"],
      "allowUnixSockets": ["/var/run/docker.sock"],
      "allowLocalBinding": true
    }
  }
}
```

---

### 插件与市场

#### `enabledPlugins`
**Type:** object
**Scope:** all
**Default:** none

按 key（格式：`plugin-name@marketplace-name`）启用或禁用特定插件。

```json
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "experimental@acme-tools": false
  }
}
```

#### `extraKnownMarketplaces`
**Type:** object
**Scope:** project
**Default:** none

添加自定义插件市场。使用 `source: "settings"` 可内联声明插件，而无需托管代码仓库。

#### `strictKnownMarketplaces`
**Type:** array
**Scope:** managed only
**Default:** none（无限制）

允许的插件市场的白名单。设置后，用户只能从列出的市场添加插件。空数组会阻止所有添加操作。

#### `blockedMarketplaces`
**Type:** array
**Scope:** managed only
**Default:** none

阻止特定的插件市场来源。被阻止的来源会在下载之前进行检查，因此它们绝不会触及文件系统。

#### `pluginTrustMessage`
**Type:** string
**Scope:** managed only
**Default:** none

在安装前显示的插件信任警告之后追加的自定义消息。可用于组织专属的上下文，例如确认来自内部市场的插件已经过审核。

#### `skippedMarketplaces` `📋 Schema only`
**Type:** array
**Scope:** all
**Default:** none

用户拒绝安装的市场（自动存储）。

#### `skippedPlugins` `📋 Schema only`
**Type:** array
**Scope:** all
**Default:** none

用户拒绝安装的插件（自动存储）。

#### `pluginConfigs` `📋 Schema only`
**Type:** object
**Scope:** all
**Default:** none

按插件划分的 MCP 服务器配置，以 `plugin@marketplace` 为 key。

---

### 模型配置

#### `effortLevel`
**Type:** string
**Scope:** all
**Default:** `"medium"`
**Values:** `"low"` | `"medium"` | `"high"`

在多个会话之间持久化推理强度等级。控制推理深度。运行 `/effort low|medium|high` 时会自动写入。Opus 4.6+ 和 Sonnet 4.6 支持此项。`CLAUDE_CODE_EFFORT_LEVEL` 环境变量优先级更高。

#### `modelOverrides`
**Type:** object
**Scope:** all
**Default:** none

将 Anthropic 模型 ID 映射到特定服务商的模型 ID（例如 Bedrock 推理配置文件 ARN）。每个 key 是模型选择器中的条目名称；每个 value 是服务商的模型 ID。

```json
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-1:123456789:inference-profile/anthropic.claude-opus-4-6-v1:0"
  }
}
```

**模型别名参考：**

| 别名 | 说明 |
|-------|-------------|
| `"default"` | 适合你账户类型的推荐模型 |
| `"sonnet"` | 最新 Sonnet（Claude Sonnet 4.6） |
| `"opus"` | 最新 Opus（Claude Opus 4.8） |
| `"haiku"` | 快速的 Haiku 模型 |
| `"sonnet[1m]"` | 具备 1M token 上下文的 Sonnet |
| `"opusplan"` | 用 Opus 做规划，用 Sonnet 做执行 |

---

### 显示与用户体验

#### `statusLine`
**Type:** object
**Scope:** all
**Default:** none

配置自定义状态行。该命令会在 stdin 上接收一个 JSON 对象，其中包含 `context_window.used_percentage`、`rate_limits.five_hour.used_percentage` 等字段。

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0
  }
}
```

#### `fileSuggestion`
**Type:** object
**Scope:** all
**Default:** none

为 `@` 文件路径自动补全配置自定义脚本。该命令会在 stdin 上接收带有 `query` 字段的 JSON，并输出以换行符分隔的文件路径（最多 15 个）。

```json
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

#### `outputStyle`
**Type:** string
**Scope:** all
**Default:** `"Default"`

控制 Claude 在整个会话中的沟通方式。等同于通过 `/config` → "Preferred output style" 选择某种风格。

**内置取值：**
- `"Default"` — 简洁、聚焦任务的回复，针对速度进行了优化
- `"Explanatory"` — 添加推理块，解释设计选择、权衡取舍和代码库模式
- `"Learning"` — 在关键步骤暂停，插入 `TODO(human)` 标记，请你来编写有意义的部分（结对编程模式）

**自定义风格：** 引用 `.claude/styles/` 中的任意文件名（不带 `.md`）。

```json
{ "outputStyle": "Explanatory" }
```

```json
{ "outputStyle": "strict-reviewer" }
```

该设置在多个会话之间持久化。Explanatory 和 Learning 会增加输出 token 量；prompt caching 会在首次请求之后抵消这部分成本。完整文档及自定义风格示例参见 [Section 9.7](../ultimate-guide.md#97-output-styles)。

#### `spinnerTipsEnabled`
**Type:** boolean
**Scope:** all
**Default:** `true`

在 Claude 工作时于 spinner 中显示提示。

#### `spinnerVerbs`
**Type:** object
**Scope:** all
**Default:** none

自定义 spinner 和回合时长消息中显示的动作动词。将 `mode` 设为 `"replace"` 以仅使用你的动词，或设为 `"append"` 以追加到默认动词。

```json
{
  "spinnerVerbs": {
    "mode": "replace",
    "verbs": ["Cooking", "Brewing", "Crafting", "Conjuring"]
  }
}
```

#### `spinnerTipsOverride`
**Type:** object
**Scope:** all
**Default:** none

用自定义字符串覆盖 spinner 提示。`tips`：字符串数组。`excludeDefault`：当为 `true` 时，仅显示自定义提示。

```json
{
  "spinnerTipsOverride": {
    "tips": ["Use /compact at 50% context", "Plan mode helps for complex tasks"],
    "excludeDefault": true
  }
}
```

#### `respectGitignore`
**Type:** boolean
**Scope:** all
**Default:** `true`

控制 `@` 文件选择器是否遵守 `.gitignore` 模式。

#### `prefersReducedMotion`
**Type:** boolean
**Scope:** all
**Default:** `false`

为了可访问性，减少或禁用 UI 动画（spinner、微光、闪烁效果）。

---

### 认证

#### `apiKeyHelper`
**Type:** string
**Scope:** all
**Default:** none

Shell 脚本路径（在 `/bin/sh` 中执行），输出一个认证 token，作为模型请求的 `X-Api-Key` 和 `Authorization: Bearer` 头发送。适用于短期凭证。

```json
{ "apiKeyHelper": "/bin/generate_temp_api_key.sh" }
```

#### `forceLoginMethod`
**Type:** string
**Scope:** all
**Default:** none
**Values:** `"claudeai"` | `"console"`

将登录限制为 Claude.ai 账户（`"claudeai"`）或 Claude Console API 计费账户（`"console"`）。

#### `forceLoginOrgUUID`
**Type:** string
**Scope:** all
**Default:** none

在登录期间自动选择的组织 UUID，跳过组织选择步骤。需要先设置 `forceLoginMethod`。

---

### 归属信息

#### `attribution.commit`
**Type:** string
**Scope:** all
**Default:** 带有 co-authored-by 行的 Git trailer

添加到 git 提交中的归属文本。支持 git trailer。设为空字符串可完全禁用提交归属。

#### `attribution.pr`
**Type:** string
**Scope:** all
**Default:** 带有 Claude Code 链接的生成消息

添加到 pull request 描述中的归属文本。设为空字符串可禁用。

#### `includeCoAuthoredBy`
**Type:** boolean
**Scope:** all
**Default:** `true`
**Status:** DEPRECATED — 改用 `attribution`

是否包含 `Co-Authored-By` 署名行。已被 `attribution` 对象取代。

```json
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

---

### Worktrees

#### `worktree.symlinkDirectories`
**类型：** 字符串数组
**作用域：** all
**默认值：** `[]`

从主仓库符号链接到每个 worktree 的目录，避免在磁盘上重复存放大型目录（例如 `node_modules`）。

#### `worktree.sparsePaths`
**类型：** 字符串数组
**作用域：** all
**默认值：** `[]`

通过 git sparse-checkout（cone 模式）在每个 worktree 中检出的目录。只有列出的路径才会写入磁盘——这对大型 monorepo 很有用。

```json
{
  "worktree": {
    "symlinkDirectories": ["node_modules", ".cache"],
    "sparsePaths": ["packages/my-app", "shared/utils"]
  }
}
```

---

### AWS 与云

#### `awsAuthRefresh`
**类型：** 字符串
**作用域：** all
**默认值：** 无

修改 `.aws` 目录的自定义脚本。在 API 调用之前运行以刷新 AWS 凭证。

```json
{ "awsAuthRefresh": "aws sso login --profile myprofile" }
```

#### `awsCredentialExport`
**类型：** 字符串
**作用域：** all
**默认值：** 无

输出包含 AWS 凭证的 JSON 的自定义脚本。用于非标准的凭证来源。

#### `otelHeadersHelper`
**类型：** 字符串
**作用域：** all
**默认值：** 无

生成动态 OpenTelemetry 请求头的脚本。在启动时及周期性运行。预期的输出格式请参阅监控文档。

---

### 全局配置（`~/.claude.json`）

这些设置存储在 `~/.claude.json` 中，而非 `settings.json`。将它们添加到 `settings.json` 会触发 schema 校验错误。

| 键 | 类型 | 默认值 | 说明 |
|-----|------|---------|-------------|
| `autoConnectIde` | boolean | `false` | 当 Claude Code 从外部终端启动时，自动连接到正在运行的 IDE |
| `autoInstallIdeExtension` | boolean | `true` | 从 VS Code 终端运行时，自动安装 Claude Code IDE 扩展 |
| `editorMode` | string | `"normal"` | 按键绑定模式：`"normal"` 或 `"vim"`。由 `/vim` 自动写入 |
| `showTurnDuration` | boolean | `true` | 在响应后显示本轮耗时消息（例如 "Cooked for 1m 6s"） |
| `terminalProgressBarEnabled` | boolean | `true` | 在 ConEmu、Ghostty 1.2.0+ 和 iTerm2 3.6.6+ 中显示终端进度条 |

---

### 其他仅 Schema 的键

在 JSON schema 中确认但未在上述各节中涵盖的键：

| 键 | 类型 | 说明 |
|-----|------|-------------|
| `claudeMdExcludes` `📋 Schema only` | array | 要排除加载的 CLAUDE.md 文件的 glob 模式 |
| `allowManagedMcpServersOnly` | boolean | （受管）仅允许使用受管的 MCP 服务器 |
| `allowManagedHooksOnly` | boolean | （受管）仅加载受管的和 SDK 的 hooks |
| `autoMemoryEnabled` | boolean | 启用/禁用自动记忆功能 |
| `feedbackSurveyRate` | number | 问卷出现的概率（0–1） |

---

## 环境变量

在启动 `claude` 之前在 shell 中设置，或在 `settings.json` 的 `env` 键下配置，以应用于每个会话。当某个环境变量与一个等效的设置字段同时生效时，环境变量优先（例如 `ANTHROPIC_MODEL` 会覆盖 `model` 设置）。更改将在下次启动 `claude` 时生效。

### 认证

| 变量 | 说明 |
|----------|-------------|
| `ANTHROPIC_API_KEY` | 用于访问 Anthropic API 的 API 密钥。设置后，即使已登录也会用它代替你的 Claude 订阅 |
| `ANTHROPIC_AUTH_TOKEN` | 自定义 `Authorization` 请求头的值（前缀为 `Bearer `） |
| `ANTHROPIC_BASE_URL` | 用于代理或 LLM 网关的自定义 API 端点 |
| `ANTHROPIC_CUSTOM_HEADERS` | 添加到 API 请求的自定义请求头。格式：`Name: Value`，多个时以换行分隔 |
| `ANTHROPIC_BETAS` | 逗号分隔的额外 `anthropic-beta` 请求头值。适用于所有认证方式，包括 Claude.ai 订阅 |
| `ANTHROPIC_WORKSPACE_ID` | 当某条联邦规则涵盖多个工作区时，用于工作负载身份联邦的工作区 ID |
| `CLAUDE_CODE_OAUTH_TOKEN` | 用于 Claude.ai 认证的 OAuth 访问令牌。在 SDK 和自动化环境中可替代 `/login` |
| `CLAUDE_CODE_OAUTH_REFRESH_TOKEN` | 用于无头认证的 OAuth 刷新令牌。`claude auth login` 会直接用它兑换，而不打开浏览器。需要 `CLAUDE_CODE_OAUTH_SCOPES` |
| `CLAUDE_CODE_OAUTH_SCOPES` | 刷新令牌签发时所用的、以空格分隔的 OAuth 作用域。设置 `CLAUDE_CODE_OAUTH_REFRESH_TOKEN` 时必需 |
| `CLAUDE_CONFIG_DIR` | 覆盖配置目录（默认：`~/.claude`） |

### 模型选择

| 变量 | 说明 |
|----------|-------------|
| `ANTHROPIC_MODEL` | 要使用的模型。接受别名（`sonnet`、`opus`、`haiku`）或完整的模型 ID。会覆盖 `model` 设置 |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | 用自定义模型 ID 覆盖 Haiku 模型别名 |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL_NAME` | Haiku 模型覆盖项的显示名称 |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL_DESCRIPTION` | Haiku 模型覆盖项的说明 |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL_SUPPORTED_CAPABILITIES` | Haiku 模型覆盖项的能力 |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | 覆盖 Sonnet 模型别名 |
| `ANTHROPIC_DEFAULT_SONNET_MODEL_NAME` | Sonnet 模型覆盖项的显示名称 |
| `ANTHROPIC_DEFAULT_SONNET_MODEL_DESCRIPTION` | Sonnet 模型覆盖项的说明 |
| `ANTHROPIC_DEFAULT_SONNET_MODEL_SUPPORTED_CAPABILITIES` | Sonnet 模型覆盖项的能力 |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | 覆盖 Opus 模型别名（例如 `claude-opus-4-6[1m]`） |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_NAME` | Opus 模型覆盖项的显示名称 |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION` | Opus 模型覆盖项的说明 |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES` | Opus 模型覆盖项的能力 |
| `ANTHROPIC_CUSTOM_MODEL_OPTION` | 要作为自定义条目添加到 `/model` 选择器中的模型 ID |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` | 自定义模型条目的显示名称 |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` | 自定义模型条目的显示说明 |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_SUPPORTED_CAPABILITIES` | 自定义模型条目的能力 |
| `ANTHROPIC_SMALL_FAST_MODEL` | **已弃用。** 请改用 `ANTHROPIC_DEFAULT_HAIKU_MODEL` |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | 当同时设置了 `ANTHROPIC_DEFAULT_HAIKU_MODEL` 时，Bedrock 上 Haiku 级模型的 AWS 区域 |
| `CLAUDE_CODE_SUBAGENT_MODEL` | 为子代理覆盖模型（例如 `haiku`） |
| `CLAUDE_CODE_EFFORT_LEVEL` | 努力级别：`low`、`medium`、`high`、`xhigh`、`max` 或 `auto`。优先于 `/effort` 和 `effortLevel` 设置 |
| `FALLBACK_FOR_ALL_PRIMARY_MODELS` | 任何非空值都会在任意主模型（而不仅是 Opus）反复出现过载错误后触发回退到 `--fallback-model` |
| `CLAUDE_CODE_DISABLE_LEGACY_MODEL_REMAP` | 设为 `1` 可阻止在 Anthropic API 上将 Opus 4.0 和 4.1 自动重映射到当前 Opus 版本 |

### 云服务提供商

#### Amazon Bedrock

| 变量 | 说明 |
|----------|-------------|
| `CLAUDE_CODE_USE_BEDROCK` | 使用 Amazon Bedrock（`1` 启用） |
| `AWS_BEARER_TOKEN_BEDROCK` | 用于认证的 Bedrock API 密钥 |
| `ANTHROPIC_BEDROCK_BASE_URL` | 覆盖 Bedrock 端点 URL。用于自定义区域或通过 LLM 网关路由时 |
| `ANTHROPIC_BEDROCK_SERVICE_TIER` | Bedrock 服务层级：`default`、`flex` 或 `priority`。作为 `X-Amzn-Bedrock-Service-Tier` 发送 |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH` | 跳过 Bedrock 的 AWS 认证（例如使用 LLM 网关时） |
| `CLAUDE_ENABLE_BYTE_WATCHDOG_BEDROCK` | 设为 `1` 可在 Bedrock 上启用字节级流式空闲看门狗 |

#### Bedrock Mantle

| 变量 | 说明 |
|----------|-------------|
| `CLAUDE_CODE_USE_MANTLE` | 使用 Bedrock Mantle 端点 |
| `ANTHROPIC_BEDROCK_MANTLE_BASE_URL` | 覆盖 Bedrock Mantle 端点 URL |
| `CLAUDE_CODE_SKIP_MANTLE_AUTH` | 跳过 Bedrock Mantle 的 AWS 认证 |

#### Google Vertex AI

| 变量 | 说明 |
|----------|-------------|
| `CLAUDE_CODE_USE_VERTEX` | 使用 Google Vertex AI（`1` 启用） |
| `ANTHROPIC_VERTEX_BASE_URL` | 覆盖 Vertex AI 端点 URL |
| `ANTHROPIC_VERTEX_PROJECT_ID` | 用于 Vertex AI 请求的 GCP 项目 ID（会被 `GCLOUD_PROJECT` 或 `GOOGLE_CLOUD_PROJECT` 覆盖） |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH` | 跳过 Vertex 的 Google 认证 |
| `VERTEX_REGION_CLAUDE_3_5_HAIKU` | Vertex AI 上 Claude 3.5 Haiku 的区域覆盖 |
| `VERTEX_REGION_CLAUDE_3_5_SONNET` | Vertex AI 上 Claude 3.5 Sonnet 的区域覆盖 |
| `VERTEX_REGION_CLAUDE_3_7_SONNET` | Vertex AI 上 Claude 3.7 Sonnet 的区域覆盖 |
| `VERTEX_REGION_CLAUDE_4_0_OPUS` | Vertex AI 上 Claude 4.0 Opus 的区域覆盖 |
| `VERTEX_REGION_CLAUDE_4_0_SONNET` | Vertex AI 上 Claude 4.0 Sonnet 的区域覆盖 |
| `VERTEX_REGION_CLAUDE_4_1_OPUS` | Vertex AI 上 Claude 4.1 Opus 的区域覆盖 |
| `VERTEX_REGION_CLAUDE_4_5_OPUS` | Vertex AI 上 Claude Opus 4.5 的区域覆盖 |
| `VERTEX_REGION_CLAUDE_4_5_SONNET` | Vertex AI 上 Claude Sonnet 4.5 的区域覆盖 |
| `VERTEX_REGION_CLAUDE_4_6_OPUS` | Vertex AI 上 Claude Opus 4.6 的区域覆盖 |
| `VERTEX_REGION_CLAUDE_4_6_SONNET` | Vertex AI 上 Claude Sonnet 4.6 的区域覆盖 |
| `VERTEX_REGION_CLAUDE_4_7_OPUS` | Vertex AI 上 Claude Opus 4.7 的区域覆盖。于 v2.1.111 加入 |
| `VERTEX_REGION_CLAUDE_HAIKU_4_5` | Vertex AI 上 Claude Haiku 4.5 的区域覆盖 |

#### Microsoft Foundry

| 变量 | 说明 |
|----------|-------------|
| `CLAUDE_CODE_USE_FOUNDRY` | 使用 Microsoft Foundry（`1` 启用） |
| `ANTHROPIC_FOUNDRY_API_KEY` | 用于 Microsoft Foundry 认证的 API 密钥 |
| `ANTHROPIC_FOUNDRY_BASE_URL` | Foundry 资源的完整 base URL（作为 `ANTHROPIC_FOUNDRY_RESOURCE` 的替代项） |
| `ANTHROPIC_FOUNDRY_RESOURCE` | Foundry 资源名称。若未设置 `ANTHROPIC_FOUNDRY_BASE_URL` 则必需 |
| `CLAUDE_CODE_SKIP_FOUNDRY_AUTH` | 跳过 Foundry 的 Azure 认证 |

#### Claude Platform on AWS

| 变量 | 说明 |
|----------|-------------|
| `CLAUDE_CODE_USE_ANTHROPIC_AWS` | 使用 Claude Platform on AWS |
| `ANTHROPIC_AWS_API_KEY` | 在 AWS Console 中生成的、用于 Claude Platform on AWS 的工作区 API 密钥 |
| `ANTHROPIC_AWS_BASE_URL` | 覆盖 Claude Platform on AWS 端点 URL |
| `ANTHROPIC_AWS_WORKSPACE_ID` | 必需的工作区 ID。作为 `anthropic-workspace-id` 请求头在每个请求中发送 |
| `CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH` | 跳过 Claude Platform on AWS 的客户端认证 |

#### 多云

| 变量 | 说明 |
|----------|-------------|
| `CLAUDE_CODE_ENABLE_AUTO_MODE` | 设为 `1` 可在 Bedrock、Vertex AI 和 Foundry 上启用自动模式。于 v2.1.158 加入。对 Anthropic API 无影响 |
| `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST` | 由管理模型提供商路由的宿主平台设置。设置后，设置文件中的提供商选择和认证变量将被忽略 |

### 超时与限制

| 变量 | 说明 |
|----------|-------------|
| `API_TIMEOUT_MS` | API 请求超时（毫秒）（默认：600000）。最大值：2147483647 |
| `BASH_DEFAULT_TIMEOUT_MS` | 默认 bash 命令超时（毫秒）（默认：120000） |
| `BASH_MAX_TIMEOUT_MS` | 最大 bash 命令超时（毫秒）（默认：600000） |
| `BASH_MAX_OUTPUT_LENGTH` | bash 输出在保存到文件并发送路径之前的最大字符数 |
| `MAX_THINKING_TOKENS` | 扩展思考的 token 预算。设为 `0` 可禁用。在采用自适应推理的模型上会被忽略，除非设置了 `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | 每次响应的最大输出 token（默认：32,000；在 Opus 4.8 和 Sonnet 4.6 上最高 128,000） |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS` | 覆盖默认的文件读取 token 限制 |
| `CLAUDE_CODE_MAX_CONTEXT_TOKENS` | 覆盖 Claude Code 为当前模型所假定的上下文窗口大小。仅在同时设置了 `DISABLE_COMPACT` 时才生效 |
| `CLAUDE_CODE_MAX_TURNS` | 限制每个会话的 agentic 轮数。等同于 `--max-turns`（两者同时设置时以该标志为准） |
| `CLAUDE_CODE_MAX_RETRIES` | 覆盖失败 API 请求的重试次数（默认：10） |
| `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY` | 并行执行的只读工具和子代理的最大数量（默认：10） |
| `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS` | 后台子代理的停滞超时（毫秒）（默认：600000） |
| `TASK_MAX_OUTPUT_LENGTH` | 子代理输出在被截断前的最大字符数（默认：32000，最大：160000） |
| `MAX_STRUCTURED_OUTPUT_RETRIES` | 在非交互模式下模型响应未通过 `--json-schema` 校验时的重试次数（默认：5） |
| `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` | 在 Claude Code 覆盖之前，Stop hook 连续阻止本轮结束的最大次数（默认：8） |
| `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` | SessionEnd hook 的时间预算（毫秒）。默认：1.5 秒，提升至配置的最高单 hook 超时，上限 60 秒 |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` | `apiKeyHelper` 的凭证刷新间隔（毫秒） |
| `MCP_TIMEOUT` | MCP 服务器启动超时（毫秒）（默认：30000） |
| `MCP_TOOL_TIMEOUT` | MCP 工具执行超时（毫秒）（默认：100000000） |

### 行为控制

| 变量 | 说明 |
|----------|-------------|
| `CLAUDECODE` | 在 Claude Code 派生的子进程（Bash/PowerShell 工具、tmux 会话、hook 命令、状态栏命令、stdio MCP 子进程）中设为 `1`。用于检测脚本是否运行在 Claude Code 内部 |
| `DEBUG` | 设为 `1`（或 `true`/`yes`/`on`）以启用调试模式。日志写入 `~/.claude/debug/<session-id>.txt`。诸如 `DEBUG=express:*` 的命名空间模式不会触发它 |
| `CLAUDE_CODE_DEBUG_LOGS_DIR` | 覆盖调试日志文件路径（文件路径，而非目录）。需要单独启用调试模式 |
| `CLAUDE_CODE_DEBUG_LOG_LEVEL` | 调试文件的最低日志级别：`verbose`、`debug`（默认）、`info`、`warn`、`error` |
| `CLAUDE_CODE_SHELL` | 覆盖自动 shell 检测 |
| `CLAUDE_CODE_SHELL_PREFIX` | 添加到 Claude Code 派生的所有 shell 命令前的命令前缀 |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | 在主会话中每个 Bash 命令之后返回到原始工作目录（`1` 启用） |
| `CLAUDE_CODE_NEW_INIT` | 设为 `1` 使 `/init` 运行一个交互式设置流程，询问要生成哪些文件 |
| `CLAUDE_CODE_SIMPLE` | 以最小系统提示词运行，仅提供 Bash、文件读取和文件编辑工具。等同于 `--bare` |
| `CLAUDE_CODE_SIMPLE_SYSTEM_PROMPT` | 设为 `1` 以使用更短的系统提示词和精简的工具描述。设为 `0`/`false`/`no`/`off` 以退出 |
| `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` | 设为 `1` 以从子进程环境（Bash、hooks、MCP stdio 服务器）中剥离 Anthropic 和云提供商凭证 |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | 设为 `1` 以从用 `--add-dir` 指定的目录加载 CLAUDE.md 文件 |
| `CLAUDE_CODE_TMPDIR` | 覆盖用于内部临时文件的临时目录 |
| `CLAUDE_CODE_GIT_BASH_PATH` | 仅 Windows：当 Git Bash 不在 PATH 中时其可执行文件的路径 |
| `CLAUDE_CODE_GLOB_HIDDEN` | 设为 `false` 以从 Glob 工具结果中排除点文件（默认包含点文件） |
| `CLAUDE_CODE_GLOB_NO_IGNORE` | 设为 `false` 使 Glob 工具遵循 `.gitignore` 模式 |
| `CLAUDE_CODE_GLOB_TIMEOUT_SECONDS` | Glob 工具文件发现超时（秒）（默认：20，在 WSL 上为 60） |
| `CLAUDE_CODE_USE_NATIVE_FILE_SEARCH` | 设为 `1` 以使用 Node.js 文件 API 而非 ripgrep 来发现命令/子代理 |
| `CLAUDE_CODE_PERFORCE_MODE` | 设为 `1` 以启用 Perforce 感知的写保护（对缺少 owner-write 位的文件进行编辑会失败） |
| `CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY` | 设为 `1` 以阻止 Claude Code 在派生 PowerShell 时传递 `-ExecutionPolicy Bypass` |
| `CLAUDE_CODE_FORK_SUBAGENT` | 设为 `1` 使 forked 子代理成为默认：派生的代理会继承完整的对话上下文，而不是从头开始 |
| `CLAUDE_CODE_AUTO_BACKGROUND_TASKS` | 设为 `1` 以强制启用长时间运行的代理任务的自动后台化 |
| `CLAUDE_CODE_REMOTE` | 作为云会话运行时自动设为 `true` |
| `CLAUDE_CODE_REMOTE_SESSION_ID` | 在云会话中自动设为当前会话 ID |
| `CLAUDE_CODE_SESSION_ID` | 在 Bash/PowerShell 子进程、hook 命令和 MCP stdio 子进程中自动设为当前会话 ID |
| `CLAUDE_EFFORT` | 在 Bash/hook 子进程中自动设为当前的努力级别：`low`、`medium`、`high`、`xhigh` 或 `max` |
| `CLAUDE_ENV_FILE` | 在每个 Bash 命令之前运行的 shell 脚本路径。也会由 SessionStart、Setup、CwdChanged 和 FileChanged hooks 动态填充 |
| `USE_BUILTIN_RIPGREP` | 设为 `0` 以使用系统安装的 `rg` 而非 Claude Code 自带的那个 |

### 上下文窗口与压缩

| 变量 | 说明 |
|----------|-------------|
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | 自动压缩的触发阈值，以百分比表示（1-100）。默认约 95%。较低的值会更早触发压缩 |
| `CLAUDE_CODE_AUTO_COMPACT_WINDOW` | 用于压缩计算的上下文容量（以 token 计）。默认为模型的上下文窗口（标准 200K，扩展 1M）。在 1M 模型上设较低值会在压缩时将其视为更小 |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT` | 设为 `1` 以禁用 1M token 上下文窗口支持 |
| `DISABLE_AUTO_COMPACT` | 设为 `1` 以在接近上下文限制时禁用自动压缩。手动 `/compact` 仍可用 |
| `DISABLE_COMPACT` | 设为 `1` 以禁用所有压缩，包括手动 `/compact` |
| `CLAUDE_CODE_DISABLE_THINKING` | 设为 `1` 以强制禁用扩展思考，无论模型是否支持 |
| `DISABLE_INTERLEAVED_THINKING` | 设为 `1` 以阻止发送 interleaved-thinking beta 请求头。当你的网关不支持时使用 |

### 遥测与可观测性

| 变量 | 说明 |
|----------|-------------|
| `CLAUDE_CODE_ENABLE_TELEMETRY` | 启用 OpenTelemetry 数据采集（`1` 启用）。在配置 OTel 导出器之前必需 |
| `DISABLE_TELEMETRY` | 禁用遥测（`1` 禁用） |
| `DO_NOT_TRACK` | 设为 `1` 以退出遥测。等同于 `DISABLE_TELEMETRY` |
| `DISABLE_ERROR_REPORTING` | 禁用 Sentry 错误报告（`1` 禁用） |
| `DISABLE_GROWTHBOOK` | 设为 `1` 以禁用 GrowthBook 特性标志拉取，并对每个标志使用代码默认值 |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | 等同于同时设置 `DISABLE_AUTOUPDATER`、`DISABLE_FEEDBACK_COMMAND`、`DISABLE_ERROR_REPORTING` 和 `DISABLE_TELEMETRY` |

### OpenTelemetry

支持标准的 OTEL 导出器变量（`OTEL_METRICS_EXPORTER`、`OTEL_LOGS_EXPORTER`、`OTEL_EXPORTER_OTLP_ENDPOINT`、`OTEL_EXPORTER_OTLP_PROTOCOL`、`OTEL_EXPORTER_OTLP_HEADERS`、`OTEL_METRIC_EXPORT_INTERVAL`、`OTEL_RESOURCE_ATTRIBUTES` 以及各信号专属的变体）。激活 OTel 采集需要 `CLAUDE_CODE_ENABLE_TELEMETRY=1`。

| 变量 | 说明 |
|----------|-------------|
| `OTEL_LOG_RAW_API_BODIES` | 将 API 请求/响应 JSON 作为日志事件发出。设为 `1` 内联请求体（在 60 KB 处截断），或设为 `file:<dir>` 将完整请求体写入磁盘 |
| `OTEL_LOG_TOOL_CONTENT` | 设为 `1` 以在 OTel span 事件中包含工具的输入/输出内容。默认禁用 |
| `OTEL_LOG_TOOL_DETAILS` | 设为 `1` 以在 OTel 追踪中包含工具输入参数、MCP 服务器名称和原始错误字符串。默认禁用 |
| `OTEL_LOG_USER_PROMPTS` | 设为 `1` 以在 OTel 追踪中包含用户提示词文本。默认禁用 |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | 设为 `false` 以从指标属性中排除账户 UUID（默认：包含） |
| `OTEL_METRICS_INCLUDE_ENTRYPOINT` | 设为 `true` 以在指标属性中包含会话入口点（默认：排除）。于 v2.1.152 加入 |
| `OTEL_METRICS_INCLUDE_RESOURCE_ATTRIBUTES` | 设为 `false` 以从指标数据点标签中排除 `OTEL_RESOURCE_ATTRIBUTES` 键（默认：包含）。于 v2.1.161 加入 |
| `OTEL_METRICS_INCLUDE_SESSION_ID` | 设为 `false` 以从指标属性中排除会话 ID（默认：包含） |
| `OTEL_METRICS_INCLUDE_VERSION` | 设为 `true` 以在指标属性中包含 Claude Code 版本（默认：排除） |
| `CLAUDE_CODE_OTEL_FLUSH_TIMEOUT_MS` | 关闭时刷新待处理 OTel span 的超时（毫秒）（默认：5000） |
| `CLAUDE_CODE_OTEL_SHUTDOWN_TIMEOUT_MS` | 退出时 OTel 导出器完成的超时（毫秒）（默认：2000） |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` | 动态 OTel 请求头的刷新间隔（毫秒）（默认：1740000，29 分钟） |
| `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL` | 设为 `1` 以将会话质量问卷评分路由到你的 OTel collector 而非 Anthropic |
| `CLAUDE_CODE_PROPAGATE_TRACEPARENT` | 设为 `1`，当 `ANTHROPIC_BASE_URL` 指向自定义代理时传播 W3C trace context。于 v2.1.152 加入 |

### 功能开关

| 变量 | 说明 |
|----------|-------------|
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` | 在支持的模型上禁用自适应推理（`1` 禁用）。对 Opus 4.7 及更新版本无影响 |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` | 剥离 `anthropic-beta` 请求头和 beta 工具 schema 字段。当代理拒绝未知 beta 请求头时使用 |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | 禁用所有后台任务功能，包括 `run_in_background`、自动后台化和 Ctrl+B |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | 设为 `1` 以禁用自动记忆。设为 `0` 以在 `--bare` 模式本会禁用它时强制开启 |
| `CLAUDE_CODE_DISABLE_FAST_MODE` | 完全禁用快速模式（`1` 禁用） |
| `CLAUDE_CODE_DISABLE_CRON` | 禁用计划/cron 任务（`1` 禁用） |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` | 从系统提示词中移除内置的 commit/PR 指令。优先于 `includeGitInstructions` |
| `CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK` | 禁用对失败的流式请求的非流式回退 |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY` | 禁用会话质量问卷提示（`1` 禁用） |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` | 禁用终端标题自动更新和后台标题生成请求 |
| `CLAUDE_CODE_DISABLE_AGENT_VIEW` | 设为 `1` 以禁用后台代理和代理视图（`claude agents`、`--bg`、`/background`） |
| `CLAUDE_CODE_DISABLE_WORKFLOWS` | 设为 `1` 以禁用工作流 |
| `CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING` | 设为 `1` 以禁用文件检查点。`/rewind` 将不会恢复代码更改 |
| `CLAUDE_CODE_DISABLE_CLAUDE_MDS` | 设为 `1` 以阻止加载任何 CLAUDE.md 记忆文件，包括自动记忆 |
| `CLAUDE_CODE_DISABLE_ATTACHMENTS` | 设为 `1` 以禁用附件处理。`@` 文件提及将作为纯文本发送 |
| `CLAUDE_CODE_DISABLE_POLICY_SKILLS` | 设为 `1` 以跳过从系统级受管 skills 目录加载 skills |
| `CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL` | 设为 `1` 以在首次运行时跳过自动添加官方插件市场 |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION` | 设为 `false` 以禁用输入区域中的提示词建议 |
| `CLAUDE_CODE_ENABLE_TASKS` | 自 v2.1.142 起，Task 工具为默认。设为 `0` 以回退到 `TodoWrite` |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | 启用实验性的 agent teams 功能（`1` 启用） |
| `ENABLE_CLAUDEAI_MCP_SERVERS` | 设为 `false` 以禁用 Claude.ai MCP 服务器（对已登录用户默认启用） |
| `CLAUDE_CODE_USE_POWERSHELL_TOOL` | 控制 PowerShell 工具。在没有 Git Bash 的 Windows 上自动启用。设 `0` 禁用，`1` 选择启用 |
| `CLAUDE_CODE_ENABLE_AWAY_SUMMARY` | 覆盖会话回顾的可用性：`0` 强制关闭，`1` 强制开启 |
| `CLAUDE_CODE_ENABLE_FINE_GRAINED_TOOL_STREAMING` | 控制工具调用输入的流式传输。设 `0` 退出，`1` 通过代理强制开启 |
| `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY` | 设为 `1` 以从你的网关的 `/v1/models` 端点填充 `/model` 选择器 |
| `DISABLE_DOCTOR_COMMAND` | 设为 `1` 以隐藏 `/doctor` 命令 |
| `DISABLE_LOGIN_COMMAND` | 设为 `1` 以隐藏 `/login` 命令 |
| `DISABLE_LOGOUT_COMMAND` | 设为 `1` 以隐藏 `/logout` 命令 |
| `DISABLE_UPGRADE_COMMAND` | 设为 `1` 以隐藏 `/upgrade` 命令 |
| `DISABLE_EXTRA_USAGE_COMMAND` | 设为 `1` 以隐藏 `/usage-credits` 命令 |
| `DISABLE_INSTALL_GITHUB_APP_COMMAND` | 设为 `1` 以隐藏 `/install-github-app` 命令 |
| `DISABLE_UPDATES` | 设为 `1` 以阻止所有更新，包括手动的 `claude update` 和 `claude install` |
| `IS_DEMO` | 启用演示模式：隐藏邮箱/组织信息，跳过引导。在屏幕共享时很有用 |

### 提示词缓存

| 变量 | 说明 |
|----------|-------------|
| `DISABLE_PROMPT_CACHING` | 禁用所有提示词缓存（`1` 禁用，优先于各模型的设置） |
| `DISABLE_PROMPT_CACHING_HAIKU` | 为 Haiku 模型请求禁用提示词缓存 |
| `DISABLE_PROMPT_CACHING_SONNET` | 为 Sonnet 模型请求禁用提示词缓存 |
| `DISABLE_PROMPT_CACHING_OPUS` | 为 Opus 模型请求禁用提示词缓存 |
| `ENABLE_PROMPT_CACHING_1H` | 设为 `1` 以请求 1 小时的提示词缓存 TTL，而非默认的 5 分钟 |
| `ENABLE_PROMPT_CACHING_1H_BEDROCK` | **已弃用。** 请改用 `ENABLE_PROMPT_CACHING_1H` |
| `FORCE_PROMPT_CACHING_5M` | 设为 `1` 以强制使用 5 分钟缓存 TTL，即使本来会应用 1 小时 TTL |
| `CLAUDE_CODE_ATTRIBUTION_HEADER` | 设为 `0` 以从系统提示词中省略署名块。通过 LLM 网关时可提升提示词缓存命中率 |

### MCP 配置

| 变量 | 说明 |
|----------|-------------|
| `MAX_MCP_OUTPUT_TOKENS` | 每次调用的最大 MCP 输出 token（默认：25000）。输出超过 10,000 token 时显示警告 |
| `ENABLE_TOOL_SEARCH` | MCP 工具搜索模式：`auto:N` 在工具数量超过上下文的 N% 时激活，`true` 始终延迟，`false` 全部预先加载 |
| `MCP_CLIENT_SECRET` | MCP OAuth 客户端密钥。使用 `--client-secret` 添加服务器时可避免交互式提示 |
| `MCP_OAUTH_CALLBACK_PORT` | MCP OAuth 重定向回调的固定端口 |
| `MCP_CONNECTION_NONBLOCKING` | 自 v2.1.142 起，MCP 启动默认为非阻塞。设为 `0` 以恢复阻塞式的 5 秒等待 |
| `MCP_CONNECT_TIMEOUT_MS` | 阻塞式 MCP 启动在对工具列表做快照之前等待的时长（默认：5000） |
| `MCP_SERVER_CONNECTION_BATCH_SIZE` | 启动期间并行连接的 stdio MCP 服务器的最大数量（默认：3） |
| `MCP_REMOTE_SERVER_CONNECTION_BATCH_SIZE` | 启动期间并行连接的远程（HTTP/SSE）MCP 服务器的最大数量（默认：20） |
| `CLAUDE_CODE_MCP_ALLOWLIST_ENV` | 设为 `1` 以仅用安全的基线环境加上服务器配置的 `env` 来派生 stdio MCP 服务器 |
| `CLAUDE_AGENT_SDK_MCP_NO_PREFIX` | 设为 `1` 以跳过 SDK 创建的 MCP 服务器工具名上的 `mcp__<server>__` 前缀 |

### 代理与网络

| 变量 | 说明 |
|----------|-------------|
| `HTTP_PROXY` | 用于网络请求的 HTTP 代理 URL |
| `HTTPS_PROXY` | 用于网络请求的 HTTPS 代理 URL |
| `NO_PROXY` | 逗号分隔的、绕过代理的主机 |
| `CLAUDE_CODE_PROXY_RESOLVES_HOSTS` | 允许代理执行 DNS 解析（`1` 启用） |
| `CLAUDE_CODE_CERT_STORE` | 逗号分隔的 CA 证书来源：`bundled`（Mozilla CA 集合）和/或 `system`（操作系统信任库）。默认：`bundled,system` |
| `CLAUDE_CODE_CLIENT_CERT` | 用于 mTLS 的客户端证书路径 |
| `CLAUDE_CODE_CLIENT_KEY` | 用于 mTLS 的客户端私钥路径 |
| `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE` | 加密 mTLS 密钥的口令 |
| `CLAUDE_CODE_EXTRA_BODY` | 合并到每个 API 请求体顶层的 JSON 对象。对提供商专属参数很有用 |
| `CLAUDE_ENABLE_STREAM_WATCHDOG` | 设为 `1` 以启用事件级流式空闲看门狗。默认关闭 |
| `CLAUDE_ENABLE_BYTE_WATCHDOG` | 强制启用字节级流式空闲看门狗。对 Anthropic API 连接默认开启。设 `0` 禁用 |
| `CLAUDE_STREAM_IDLE_TIMEOUT_MS` | 流式看门狗关闭停滞连接前的超时（毫秒）（默认最小值：300000） |

### UI 与显示

| 变量 | 说明 |
|----------|-------------|
| `CLAUDE_CODE_NO_FLICKER` | 设为 `1` 以启用全屏渲染（减少闪烁，在长对话中保持内存平稳）。等同于 `tui` 设置 |
| `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN` | 设为 `1` 以禁用全屏渲染并使用经典的主屏渲染器 |
| `CLAUDE_CODE_ALT_SCREEN_FULL_REPAINT` | 设为 `1` 以在每一帧重绘整个屏幕，而非增量更新。若全屏模式显示陈旧文本时使用 |
| `CLAUDE_CODE_DISABLE_VIRTUAL_SCROLL` | 设为 `1` 以在全屏模式下禁用虚拟滚动。若滚动出现空白区域时使用 |
| `CLAUDE_CODE_DISABLE_MOUSE` | 设为 `1` 以在全屏模式下禁用鼠标追踪。保留终端原生的选中即复制行为 |
| `CLAUDE_CODE_SCROLL_SPEED` | 全屏模式下的鼠标滚轮滚动倍率（1-20） |
| `CLAUDE_CODE_NATIVE_CURSOR` | 设为 `1` 以在输入光标处显示终端自身的光标，而非绘制的方块 |
| `CLAUDE_CODE_ACCESSIBILITY` | 设为 `1` 以保持原生终端光标可见并禁用反色文本光标指示器 |
| `CLAUDE_CODE_HIDE_CWD` | 设为 `1` 以在启动 logo 中隐藏工作目录 |
| `CLAUDE_CODE_TMUX_TRUECOLOR` | 设为 `1` 以允许在 tmux 内输出 24 位 truecolor |
| `CLAUDE_CODE_FORCE_SYNC_OUTPUT` | 设为 `1` 以在你的终端支持但未被自动检测时强制启用同步输出（DEC private mode 2026） |
| `CLAUDE_CODE_SYNTAX_HIGHLIGHT` | 设为 `false` 以在 diff 输出中禁用语法高亮 |
| `CLAUDE_CODE_AUTO_CONNECT_IDE` | 覆盖自动 IDE 连接。设为 `false` 以阻止它，`true` 以强制尝试连接 |
| `CLAUDE_CODE_IDE_HOST_OVERRIDE` | 覆盖用于连接 IDE 扩展的主机地址 |
| `CLAUDE_CODE_IDE_SKIP_VALID_CHECK` | 设为 `1` 以在连接期间跳过对 IDE lockfile 条目的校验 |
| `DISABLE_COST_WARNINGS` | 禁用成本警告消息 |
| `DISABLE_INSTALLATION_CHECKS` | 禁用安装警告 |
| `DISABLE_AUTOUPDATER` | 禁用自动更新器。手动 `claude update` 仍然有效 |
| `DISABLE_FEEDBACK_COMMAND` | 禁用 `/feedback` 命令。也接受 `DISABLE_BUG_COMMAND` |
| `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL` | 跳过 IDE 扩展自动安装（`1` 跳过） |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET` | 向 Skill 工具显示的 skill 元数据的字符预算。按上下文窗口的 1% 动态缩放 |

### 插件

| 变量 | 说明 |
|----------|-------------|
| `CLAUDE_CODE_PLUGIN_CACHE_DIR` | 覆盖插件根目录（默认：`~/.claude/plugins`） |
| `CLAUDE_CODE_PLUGIN_SEED_DIR` | 只读插件 seed 目录的路径，在 Unix 上以 `:`、在 Windows 上以 `;` 分隔。用于将插件打包进容器镜像 |
| `CLAUDE_CODE_PLUGIN_PREFER_HTTPS` | 设为 `1` 以通过 HTTPS 而非 SSH 克隆 GitHub `owner/repo` 来源 |
| `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE` | 设为 `1`，当 `git pull` 失败时保留现有的市场缓存。在离线环境中很有用 |
| `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` | 插件安装/更新期间 git 操作的超时（毫秒）（默认：120000） |
| `CLAUDE_CODE_SYNC_PLUGIN_INSTALL` | 在非交互模式（`-p` 标志）下设为 `1` 以在首次查询之前等待插件安装完成 |
| `CLAUDE_CODE_SYNC_PLUGIN_INSTALL_TIMEOUT_MS` | 同步插件安装的超时（毫秒）。无默认值（不设此变量时会一直等到完成） |
| `CLAUDE_CODE_ENABLE_BACKGROUND_PLUGIN_REFRESH` | 设为 `1` 以在非交互模式下后台安装后于轮次边界刷新插件状态 |
| `FORCE_AUTOUPDATE_PLUGINS` | 设为 `1` 以在主自动更新器被禁用时仍强制插件自动更新 |

### SDK 与无头模式

| 变量 | 说明 |
|----------|-------------|
| `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS` | 设为 `1` 以仅在非交互模式下禁用所有内置子代理类型（Explore、Plan） |
| `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY` | 查询循环变为空闲后自动退出前等待的时间（毫秒）。对 SDK/脚本化会话很有用 |
| `CLAUDE_CODE_RESUME_INTERRUPTED_TURN` | 设为 `1` 以在上一会话中途结束时自动恢复。供 SDK 使用 |
| `CLAUDE_CODE_RESUME_PROMPT` | 覆盖恢复中途会话时注入的续接消息（默认：`Continue from where you left off.`） |
| `CLAUDE_CODE_SKIP_PROMPT_HISTORY` | 设为 `1` 以跳过将提示词历史和会话记录写入磁盘 |
| `CLAUDE_CODE_SYNC_SKILLS` | 设为 `1` 以在首次查询之前下载已启用的 Claude.ai skills，并每 10 分钟重新同步。仅限非交互模式 |
| `CLAUDE_CODE_SYNC_SKILLS_WAIT_TIMEOUT_MS` | 设置 `CLAUDE_CODE_SYNC_SKILLS` 时初次 skills 同步的超时（毫秒）（默认：5000） |
| `CLAUDE_CODE_SCRIPT_CAPS` | 当设置了 `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` 时，限制每个会话中特定脚本调用次数的 JSON 对象 |
| `CCR_FORCE_BUNDLE` | 设为 `1` 以强制 `claude --remote` 即使在有 GitHub 访问权限时也打包并上传本地仓库 |
| `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX` | 自动生成的 Remote Control 会话名称的前缀。默认为机器主机名 |

### Agent Teams 与任务

| 变量 | 说明 |
|----------|-------------|
| `CLAUDE_CODE_TEAM_NAME` | agent teams 的团队名称。在 agent team 成员上自动设置 |
| `CLAUDE_CODE_TASK_LIST_ID` | 跨会话共享任务列表。在多个 Claude Code 实例中设置相同的 ID 即可在共享任务列表上协作 |

### 未验证的变量

这些出现在社区来源或较旧的文档中，但未在当前的官方文档中得到确认。

| 变量 | 说明 |
|----------|-------------|
| `CLAUDE_CODE_USER_EMAIL` `⚠️ Unverified` | 同步提供用户邮箱以用于认证 |
| `CLAUDE_CODE_ORGANIZATION_UUID` `⚠️ Unverified` | 同步提供组织 UUID 以用于认证 |
| `CLAUDE_CODE_ACCOUNT_UUID` `⚠️ Unverified` | 覆盖用于认证的账户 UUID |
| `CLAUDE_CODE_PLAN_MODE_REQUIRED` `⚠️ Unverified` | 要求会话使用 plan mode |
| `CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS` `⚠️ Unverified` | 当组织状态检查因网络错误失败时允许使用快速模式 |
| `CLAUDE_CODE_SKIP_SETTINGS_SETUP` `⚠️ Unverified` | 跳过首次运行的设置设置流程 |
| `CLAUDE_CODE_DISABLE_TOOLS` `⚠️ Unverified` | 逗号分隔的、要禁用的工具列表 |
| `CLAUDE_CODE_DISABLE_MCP` `⚠️ Unverified` | 禁用所有 MCP 服务器（`1` 禁用） |
| `CLAUDE_CODE_HIDE_ACCOUNT_INFO` `⚠️ Unverified` | 从 UI 中隐藏邮箱/组织信息 |
| `CLAUDE_CODE_PROMPT_CACHING_ENABLED` `⚠️ Unverified` | 覆盖提示词缓存行为 |
| `DISABLE_NON_ESSENTIAL_MODEL_CALLS` `⚠️ Unverified` | 禁用风味文本和非必要的模型调用 |

---

## 完整示例

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "sonnet",
  "language": "english",
  "cleanupPeriodDays": 30,
  "autoUpdatesChannel": "stable",
  "alwaysThinkingEnabled": false,
  "includeGitInstructions": true,
  "effortLevel": "medium",
  "plansDirectory": "./plans",

  "worktree": {
    "symlinkDirectories": ["node_modules"],
    "sparsePaths": ["packages/my-app", "shared/utils"]
  },

  "permissions": {
    "allow": [
      "Edit(*)",
      "Write(*)",
      "Bash(npm run *)",
      "Bash(git *)",
      "WebFetch(domain:*)",
      "mcp__*"
    ],
    "ask": ["Bash(git push *)"],
    "deny": [
      "Read(.env)",
      "Read(./secrets/**)"
    ],
    "additionalDirectories": ["../shared/"],
    "defaultMode": "acceptEdits"
  },

  "enableAllProjectMcpServers": true,

  "sandbox": {
    "enabled": true,
    "excludedCommands": ["git", "docker"],
    "filesystem": {
      "allowWrite": ["/tmp/build"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"],
      "allowUnixSockets": ["/var/run/docker.sock"]
    }
  },

  "attribution": {
    "commit": "Generated with Claude Code",
    "pr": ""
  },

  "statusLine": {
    "type": "command",
    "command": "git branch --show-current"
  },

  "spinnerTipsEnabled": true,
  "prefersReducedMotion": false,

  "env": {
    "NODE_ENV": "development",
    "CLAUDE_CODE_EFFORT_LEVEL": "medium"
  }
}
```

---

## 快速参考

| 任务 | 设置 / 变量 |
|------|--------------------|
| 设置默认模型 | settings 中的 `model` 或 `ANTHROPIC_MODEL` 环境变量 |
| 锁定模型选项 | `availableModels` 数组 |
| 关闭遥测 | `DISABLE_TELEMETRY=1` 或 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` |
| 自动批准 bash | `permissions.defaultMode: "acceptEdits"` |
| 阻止敏感文件 | `permissions.deny: ["Read(.env)"]` |
| 降低上下文压缩频率 | `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70` |
| 设置回复语言 | `language: "japanese"` |
| 自定义 spinner 文本 | `spinnerVerbs` + `spinnerTipsOverride` |
| 移除署名 | `attribution.commit: ""`、`attribution.pr: ""` |
| 固定到稳定版发布 | `autoUpdatesChannel: "stable"` |
| 动态认证令牌 | `apiKeyHelper: "/path/to/script.sh"` |
| 大型 monorepo | `worktree.symlinkDirectories` + `worktree.sparsePaths` |
| 启用沙箱 | `sandbox.enabled: true` |
| 信任所有项目 MCP 服务器 | `enableAllProjectMcpServers: true` |
