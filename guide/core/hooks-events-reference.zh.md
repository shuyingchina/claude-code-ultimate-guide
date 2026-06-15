# Hooks 事件参考

涵盖全部 30 个 Claude Code hook 事件的完整参考：matcher 字段、输入 schema、决策控制以及超时默认值。来源：Anthropic 官方文档。

关于审计 skill，参见 `examples/skills/eval-hooks/SKILL.md`。

---

## 快速参考

| 事件 | 触发时机 | Matcher 字段 | 能否阻止？ | 默认超时 |
|-------|-----------|---------------|------------|----------------|
| `SessionStart` | 会话开始或恢复 | `source` | 否 | 600s |
| `Setup` | `--init-only` 或 `-p --init/--maintenance` | `trigger` | 否 | 600s |
| `UserPromptSubmit` | 用户提交一条 prompt | 无 | 是 | **30s** |
| `UserPromptExpansion` | slash command 展开为 prompt | `command_name` | 是 | 600s |
| `PreToolUse` | 工具调用执行之前 | `tool_name` | 是 | 600s |
| `PermissionRequest` | 权限对话框即将出现 | `tool_name` | 是（通过 JSON） | 600s |
| `PermissionDenied` | 自动模式分类器拒绝某次调用 | `tool_name` | 否（仅可重试） | 600s |
| `PostToolUse` | 工具调用成功之后 | `tool_name` | 否（stderr 发给 Claude） | 600s |
| `PostToolUseFailure` | 工具调用失败之后 | `tool_name` | 否 | 600s |
| `PostToolBatch` | 整个并行批次解析完成之后 | 无 | 是（终止循环） | 600s |
| `Notification` | Claude 发送通知 | `notification_type` | 否 | 600s |
| `MessageDisplay` | 助手消息文本流式输出 | 无 | 否 | **10s** |
| `SubagentStart` | 通过 Agent 工具派生 subagent | `agent_type` | 否 | 600s |
| `SubagentStop` | subagent 结束 | `agent_type` | 是 | 600s |
| `TaskCreated` | 正在通过 TaskCreate 创建任务 | 无 | 是 | 600s |
| `TaskCompleted` | 任务正在被标记为完成 | 无 | 是 | 600s |
| `Stop` | Claude 完成响应 | 无 | 是（继续本轮） | 600s |
| `StopFailure` | 因 API 错误结束本轮 | `error` | 否（被忽略） | 600s |
| `TeammateIdle` | agent team 中的队友进入空闲 | 无 | 是 | 600s |
| `InstructionsLoaded` | 加载 CLAUDE.md 或 rules 文件 | `load_reason` | 否 | 600s |
| `ConfigChange` | 会话期间配置文件发生变化 | `source` | 是（`policy_settings` 除外） | 600s |
| `CwdChanged` | 工作目录发生变化 | 无 | 否 | 600s |
| `FileChanged` | 磁盘上被监视的文件发生变化 | filename（字面量） | 否 | 600s |
| `WorktreeCreate` | 正在创建 worktree | 无 | 是（任何非零值） | 600s |
| `WorktreeRemove` | 正在移除 worktree | 无 | 否 | 600s |
| `PreCompact` | 上下文 compact 之前 | `trigger` | 是 | 600s |
| `PostCompact` | compact 完成之后 | `trigger` | 否 | 600s |
| `Elicitation` | MCP server 请求用户输入 | `mcp_server_name` | 是 | 600s |
| `ElicitationResult` | 用户对 MCP elicitation 作出响应 | `mcp_server_name` | 是 | 600s |
| `SessionEnd` | 会话终止 | `reason` | 否 | **1.5s 预算** |

**超时例外**：`prompt` hooks 默认 30s。`agent` hooks 默认 60s。`SessionEnd` 总预算为 1.5s；在单个 hook 上设置显式 `timeout` 可提高它（最大 60s）。Plugin hooks 不会提高该预算。

---

## 各事件的 Matcher 取值

`matcher` 字段根据事件类型筛选的字段各不相同。

### 工具事件：matcher 按 `tool_name` 筛选

事件：`PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest`、`PermissionDenied`

取值：`Bash`、`Edit`、`Write`、`Read`、`Glob`、`Grep`、`Agent`、`WebFetch`、`WebSearch`、`AskUserQuestion`、`ExitPlanMode`，以及形如 `mcp__<server>__<tool>` 的 MCP 工具。

匹配规则：
- 仅含字母/数字/下划线/竖线：精确字符串或竖线分隔的列表（`Edit|Write`）
- 包含任何其他字符：按 JS 正则处理（`mcp__memory__.*`）
- `"*"`、`""` 或缺失：匹配全部

要匹配某个 MCP server 的每个工具：`mcp__memory__.*`（`.*` 是必需的；不带它的 `mcp__memory` 是精确字符串，不匹配任何工具）。

### SessionStart：matcher 按 `source` 筛选

| 取值 | 何时 |
|-------|------|
| `startup` | 新会话 |
| `resume` | `--resume`、`--continue` 或 `/resume` |
| `clear` | `/clear` |
| `compact` | 自动或手动 compact |

### Setup：matcher 按 `trigger` 筛选

| 取值 | 何时 |
|-------|------|
| `init` | `claude --init-only` 或 `claude -p --init` |
| `maintenance` | `claude -p --maintenance` |

### SessionEnd：matcher 按 `reason` 筛选

| 取值 | 何时 |
|-------|------|
| `clear` | `/clear` 命令 |
| `resume` | 交互式 `/resume` 切换 |
| `logout` | 用户登出 |
| `prompt_input_exit` | 在 prompt 输入框可见时退出 |
| `bypass_permissions_disabled` | bypass 模式被禁用 |
| `other` | 其他退出原因 |

### Notification：matcher 按 `notification_type` 筛选

取值：`permission_prompt`、`idle_prompt`、`auth_success`、`elicitation_dialog`、`elicitation_complete`、`elicitation_response`

### SubagentStart / SubagentStop：matcher 按 `agent_type` 筛选

取值：`general-purpose`、`Explore`、`Plan`，或自定义 agent 名称（agent frontmatter 中的 `name` 字段，而非文件名）。

### PreCompact / PostCompact：matcher 按 `trigger` 筛选

取值：`manual`（来自 `/compact`）、`auto`（自动）

### InstructionsLoaded：matcher 按 `load_reason` 筛选

取值：`session_start`、`nested_traversal`、`path_glob_match`、`include`、`compact`

### ConfigChange：matcher 按 `source` 筛选

取值：`user_settings`、`project_settings`、`local_settings`、`policy_settings`、`skills`

### StopFailure：matcher 按 `error` 筛选

取值：`rate_limit`、`overloaded`、`authentication_failed`、`oauth_org_not_allowed`、`billing_error`、`invalid_request`、`model_not_found`、`server_error`、`max_output_tokens`、`unknown`

### UserPromptExpansion：matcher 按 `command_name` 筛选

用户输入的 skill 或 command 名称（不含开头的 `/`）。

### Elicitation / ElicitationResult：matcher 按 `mcp_server_name` 筛选

你配置的 MCP server 名称。

### FileChanged：matcher = 字面量文件名

按 `|` 拆分，每一段都被注册为在当前目录中监视的字面量文件名。例如：`".envrc|.env"`。与其他事件不同，这里不应用正则模式。同一个值既用于构建监视列表，也用于筛选哪些 hooks 运行。

### 不支持 matcher 的事件

`UserPromptSubmit`、`PostToolBatch`、`Stop`、`TeammateIdle`、`TaskCreated`、`TaskCompleted`、`WorktreeCreate`、`WorktreeRemove`、`CwdChanged`、`MessageDisplay`

向这些事件添加 `matcher` 字段会被静默忽略。

---

## 各事件在退出码 2 时的行为

只有退出码 2 会阻止。退出码 1 不阻止：动作继续执行，且 stderr 的第一行会出现在 transcript 中。`WorktreeCreate` 是例外：任何非零退出码都会使创建失败。

| 事件 | 退出码 2 时发生什么 |
|-------|------------------------|
| `PreToolUse` | 阻止工具调用；stderr 发给 Claude |
| `PermissionRequest` | 拒绝该权限 |
| `UserPromptSubmit` | 阻止 prompt 并将其从上下文中抹除 |
| `UserPromptExpansion` | 阻止展开 |
| `Stop` | 阻止停止；继续本轮 |
| `SubagentStop` | 阻止 subagent 停止 |
| `TeammateIdle` | 队友继续工作；stderr 回传 |
| `TaskCreated` | 回滚任务创建；stderr 回传 |
| `TaskCompleted` | 阻止完成；stderr 回传 |
| `ConfigChange` | 阻止配置变更（`policy_settings` 除外） |
| `PostToolBatch` | 在下一次模型调用前停止 agentic 循环 |
| `PreCompact` | 阻止 compact |
| `Elicitation` | 拒绝该 elicitation |
| `ElicitationResult` | 阻止响应（实际动作变为拒绝） |
| `WorktreeCreate` | **任何**非零退出码都会使创建失败 |
| `PostToolUse` | 向 Claude 显示 stderr（工具已运行） |
| `PostToolUseFailure` | 向 Claude 显示 stderr |
| `StopFailure` | 完全忽略（输出和退出码均被忽略） |
| `SessionEnd` | 仅向用户显示 stderr |
| `SessionStart`、`Setup`、`SubagentStart` | 仅向用户显示 stderr |
| `Notification` | 仅向用户显示 stderr |
| `InstructionsLoaded` | 退出码被忽略 |
| `PermissionDenied` | 退出码和 stderr 均被忽略 |
| `CwdChanged`、`FileChanged`、`WorktreeRemove` | 仅在 debug 模式下记录 |
| `PostCompact` | 仅向用户显示 stderr |
| `MessageDisplay` | 原始文本原样显示 |

---

## 各事件的决策控制格式

### 顶层 `decision` 字段

使用者：`UserPromptSubmit`、`UserPromptExpansion`、`PostToolUse`、`PostToolUseFailure`、`PostToolBatch`、`Stop`、`SubagentStop`、`ConfigChange`、`PreCompact`

```json
{ "decision": "block", "reason": "Explanation" }
```

只有 `"block"` 是有效值。省略 `decision` 表示允许。对于 `Stop` 和 `SubagentStop`，`reason` 会成为 Claude 的下一条指令。

### PreToolUse

使用 `hookSpecificOutput` 实现更丰富的控制。当 hooks 冲突时的优先级：`deny > defer > ask > allow`。

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow | deny | ask | defer",
    "permissionDecisionReason": "Shown to user (allow/ask) or to Claude (deny)",
    "updatedInput": { "field": "new value" },
    "additionalContext": "Context injected next to tool result"
  }
}
```

`defer` 只在 `-p`（非交互）模式下生效。进程以 `stop_reason: "tool_deferred"` 退出，调用方进程可在稍后恢复。当 Claude 一次发起多个工具调用时，`defer` 不生效。

### PermissionRequest

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow | deny",
      "updatedInput": {},
      "updatedPermissions": [],
      "message": "Reason for deny",
      "interrupt": false
    }
  }
}
```

### PermissionDenied

退出码和 stderr 均被忽略。要发出重试信号：

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

### PostToolUse

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Context injected next to tool result",
    "updatedToolOutput": { "stdout": "...", "stderr": "", "interrupted": false, "isImage": false }
  }
}
```

`updatedToolOutput` 改变的是 Claude 所看到的内容，而非已经执行的内容。必须与工具的输出结构完全一致。结构不正确的内置工具会回退到原始输出。

### WorktreeCreate

Command hooks 在 stdout 上打印绝对路径。HTTP hooks 返回：

```json
{ "hookSpecificOutput": { "hookEventName": "WorktreeCreate", "worktreePath": "/abs/path" } }
```

任何失败或路径缺失都会使 worktree 创建失败。

### MessageDisplay

```json
{
  "hookSpecificOutput": {
    "hookEventName": "MessageDisplay",
    "displayContent": "Replacement text shown on screen"
  }
}
```

只改变屏幕上显示的内容。Claude 和 transcript 保留原始内容。

### SessionStart（附加字段）

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Context before first prompt",
    "sessionTitle": "branch-or-feature-name",
    "watchPaths": ["/absolute/path/to/watch"],
    "reloadSkills": true,
    "initialUserMessage": "First turn in -p mode"
  }
}
```

`reloadSkills: true` 会在 hooks 完成后重新扫描 skill 目录，因此 hook 安装的 skills 在同一会话中立即可用。

### Elicitation

```json
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept | decline | cancel",
    "content": { "field_name": "value" }
  }
}
```

### ElicitationResult

格式与 Elicitation 输出相同。会覆盖用户所提交的内容。

### 通用字段（所有事件）

```json
{
  "continue": false,
  "stopReason": "Message shown to user (not Claude)",
  "suppressOutput": true,
  "systemMessage": "Warning shown to user",
  "terminalSequence": "\033]777;notify;Title;Body\007"
}
```

`continue: false` 会完全停止 Claude，优先级高于所有决策字段。

`terminalSequence`：通过 OSC 序列实现桌面通知和窗口标题。仅限 OSC `0/1/2/9/99/777` 和 BEL。自 v2.1.139 起，直接写入 `/dev/tty` 会失败，因为 hooks 在没有控制终端的情况下运行。

---

## 每个事件的关键输入字段

所有事件都会收到：`session_id`、`transcript_path`、`cwd`、`hook_event_name`，通常还有 `permission_mode`。Subagent 类的 hooks 还会收到 `agent_id` 和 `agent_type`。

| 事件 | 该事件特有的额外输入字段 |
|-------|----------------------------------|
| `SessionStart` | `source`、`model`，可选 `agent_type`、`session_title` |
| `Setup` | `trigger`（`"init"` 或 `"maintenance"`） |
| `UserPromptSubmit` | `prompt` |
| `UserPromptExpansion` | `expansion_type`、`command_name`、`command_args`、`command_source`、`prompt` |
| `PreToolUse` | `tool_name`、`tool_input`、`tool_use_id` |
| `PermissionRequest` | `tool_name`、`tool_input`、`permission_suggestions` |
| `PermissionDenied` | `tool_name`、`tool_input`、`tool_use_id`、`reason` |
| `PostToolUse` | `tool_name`、`tool_input`、`tool_response`、`tool_use_id`、`duration_ms` |
| `PostToolUseFailure` | `tool_name`、`tool_input`、`tool_use_id`、`error`、`is_interrupt`、`duration_ms` |
| `PostToolBatch` | `tool_calls`（包含 `tool_name`、`tool_input`、`tool_use_id`、`tool_response` 的数组） |
| `Notification` | `message`、`title`、`notification_type` |
| `MessageDisplay` | `turn_id`、`message_id`、`index`、`final`、`delta` |
| `SubagentStart` | `agent_id`、`agent_type` |
| `SubagentStop` | `stop_hook_active`、`agent_id`、`agent_type`、`agent_transcript_path`、`last_assistant_message` |
| `TaskCreated` | `task_id`、`task_subject`、`task_description`、`teammate_name`、`team_name` |
| `TaskCompleted` | `task_id`、`task_subject`、`task_description`、`teammate_name`、`team_name` |
| `Stop` | `stop_hook_active`、`last_assistant_message`、`background_tasks`、`session_crons` |
| `StopFailure` | `error`、`error_details`、`last_assistant_message` |
| `TeammateIdle` | `teammate_name`、`team_name` |
| `InstructionsLoaded` | `file_path`、`memory_type`、`load_reason`、`globs`、`trigger_file_path`、`parent_file_path` |
| `ConfigChange` | `source`、`file_path` |
| `CwdChanged` | `old_cwd`、`new_cwd` |
| `FileChanged` | `file_path`、`event`（`"change"`、`"add"`、`"unlink"`） |
| `WorktreeCreate` | `name`（新 worktree 的 slug） |
| `WorktreeRemove` | `worktree_path` |
| `PreCompact` | `trigger`、`custom_instructions` |
| `PostCompact` | `trigger`、`compact_summary` |
| `Elicitation` | `mcp_server_name`、`message`、`mode`、`url`、`elicitation_id`、`requested_schema` |
| `ElicitationResult` | `mcp_server_name`、`action`、`mode`、`elicitation_id`、`content` |
| `SessionEnd` | `reason` |

---

## Hook 处理器字段

### 通用字段（所有类型）

| 字段 | 说明 |
|-------|-------------|
| `type` | `command`、`http`、`mcp_tool`、`prompt` 或 `agent` |
| `if` | 用于缩小处理器范围的权限规则语法。仅限工具类事件（`PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest`、`PermissionDenied`）。在任何其他事件上，设置了 `if` 的 hook 永远不会运行 |
| `timeout` | 取消前的秒数 |
| `statusMessage` | hook 运行时自定义的加载指示器消息 |
| `once` | 每个会话运行一次后即移除。仅在 skill frontmatter 中生效，在 settings 文件中被忽略 |

### Command hook 字段

| 字段 | 说明 |
|-------|-------------|
| `command` | Shell 命令或可执行文件路径 |
| `args` | 参数向量：触发 exec 形式（不涉及 shell） |
| `async` | `true` 表示在后台运行且不阻塞 |
| `asyncRewake` | 类似 `async: true`，但在退出码为 2 时唤醒 Claude，并将 stderr（若 stderr 为空则为 stdout）作为系统提醒显示 |
| `shell` | `"bash"`（默认）或 `"powershell"`（Windows） |

**Shell 形式**（无 `args`）：`command` 传递给 `sh -c`。支持管道、`&&`、通配符。
**Exec 形式**（有 `args`）：`command` 为可执行文件，每个 `args` 元素是一个原样参数。用于含空格的路径，或引用 `${CLAUDE_PROJECT_DIR}` 时。

### HTTP hook 字段

| 字段 | 说明 |
|-------|-------------|
| `url` | POST 端点 URL |
| `headers` | 额外的 header（支持 `$VAR` 插值） |
| `allowedEnvVars` | 允许在 header 值中插值的环境变量 |

非 2xx 响应不会阻塞。若要阻塞，请返回 2xx 并在 JSON body 中包含 `decision: "block"`。

### MCP tool hook 字段

| 字段 | 说明 |
|-------|-------------|
| `server` | 已连接的 MCP 服务器名称 |
| `tool` | 该服务器上的工具名称 |
| `input` | 工具参数。字符串值支持来自 hook 输入的 `${path}` 替换 |

服务器必须已经连接。`SessionStart` 和 `Setup` 通常在服务器完成连接之前触发。

### Prompt hook 字段

| 字段 | 说明 |
|-------|-------------|
| `prompt` | Prompt 文本。使用 `$ARGUMENTS` 表示 hook 的 JSON 输入 |
| `model` | 模型覆盖（默认：快速模型，通常是 Haiku） |
| `continueOnBlock` | 当 `ok: false` 时，将原因反馈给 Claude 并继续，而不是停止 |

返回 `{ "ok": true/false, "reason": "..." }`。支持与 `command` hooks 相同的事件，但 `SessionStart` 和 `Setup` 除外。

### Agent hook 字段

| 字段 | 说明 |
|-------|-------------|
| `prompt` | 任务描述。使用 `$ARGUMENTS` 表示 hook 的 JSON 输入 |
| `model` | 模型覆盖 |

派生一个可使用 Read、Grep、Glob 的 subagent（最多 50 轮），然后返回相同的 `{ "ok": true/false }` schema。实验性功能。

---

## 路径占位符

| 占位符 | 解析为 |
|-------------|-------------|
| `${CLAUDE_PROJECT_DIR}` | 项目根目录 |
| `${CLAUDE_PLUGIN_ROOT}` | 插件安装目录（更新时会变化） |
| `${CLAUDE_PLUGIN_DATA}` | 插件持久化数据目录（更新后仍保留） |

对于引用这些占位符的 hooks，优先使用 exec 形式：每个 `args` 元素原样传递，含空格或特殊字符时无需引号。

---

## CLAUDE_ENV_FILE

可在 `SessionStart`、`Setup`、`CwdChanged` 和 `FileChanged` hooks 中使用。将 `export VAR=value` 行写入该路径，可将变量持久化到本会话后续的 Bash 命令中。

```bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
fi
```

使用追加（`>>`）以保留其他 hooks 设置的变量。

---

## 常见陷阱

**Stop hook 8 次阻塞上限**：Claude Code 在连续 8 次阻塞后会覆盖 Stop hooks。从 stdin 读取 `stop_hook_active`，当其为 `true` 时退出 0，让 Claude 干净地停止。

**退出码 1 不会阻塞**：只有退出码 2 才会阻塞 PreToolUse 调用或 UserPromptSubmit。退出码 1 不阻塞：动作会继续执行。这让大多数遵循 Unix 惯例的开发者感到意外。

**asyncRewake 与 async 的区别**：`asyncRewake: true` 在后台运行 hook，并在进程以退出码 2 结束时唤醒会话，即使 Claude 处于空闲状态。当一个长时间运行的后台检查需要在会话中途报告失败时使用。

**SessionEnd 预算**：总预算为 1.5 秒。在某个 hook 上设置 `timeout: 30` 会将整组的预算提升到 30 秒。插件 hooks 不计入预算计算。可用 `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000` 覆盖。

**MessageDisplay 批处理**：在交互模式下，每条消息会多次触发（每批行触发一次）；在 `-p`/Agent SDK 模式下，整条消息完成后触发一次。`final: true` 标记最后一批；不要依赖非空的 `delta` 作为结束信号。

**WorktreeCreate 完全替代 git**：该 hook 必须处理完整的 worktree 设置。`.worktreeinclude` 不会被处理。请在 hook 内部复制 `.env` 和其他本地文件。

**非工具事件上的 if 字段**：将 `if` 添加到 `SessionStart`、`Stop` 或任何非工具事件，会悄无声息地导致该 hook 完全不运行。

**多个带 updatedInput 的 PreToolUse hooks**：hooks 并行运行；最后完成的获胜。顺序是非确定性的。避免在同一 matcher 上有两个都返回 `updatedInput` 的 hooks。

**PermissionRequest 无法通过退出码 2 阻止**：请在 JSON 输出中使用 `hookSpecificOutput.decision.behavior: "deny"`。这里退出码 2 不是相应机制。

**PermissionDenied 上的 Prompt hooks**：输出会被丢弃。该事件唯一读取的字段是 `hookSpecificOutput.retry`，而 prompt 和 agent hooks 无法设置它。请使用 command hook 来发送重试信号。

**没有控制终端的 Hooks**：自 v2.1.139 起，hooks 在没有 `/dev/tty` 的情况下运行。请在 JSON 输出中使用 `terminalSequence` 来发出桌面通知或窗口标题，而不要直接写入转义序列。

**UserPromptSubmit 默认超时**：30 秒，而非 600 秒。此处卡住的 hook 会阻塞所有用户输入。若需要更多时间，请设置显式的 `timeout`。
