---
title: "Claude Code Cheatsheet"
description: "One-page printable daily essentials for maximum Claude Code productivity"
tags: [cheatsheet, reference]
---

# Claude Code 速查表

**单页可打印** —— 实现最高生产力的每日必备要点

**作者**：Florian BRUNIAUX | Founding Engineer [@Méthode Aristote](https://methode-aristote.fr)

**撰写工具**：Claude (Anthropic)

**版本**：3.41.1 | **最后更新**：2026 年 5 月

---

## 必备命令

| 命令 | 作用 |
|---------|--------|
| `/help` | 上下文相关帮助 |
| `/powerup` | 教授 Claude Code 功能的交互式动画课程 |
| `/clear` | 重置对话 |
| `/compact` | 释放上下文 |
| `/status` | 会话状态 + 上下文使用情况 |
| `/context` | 详细的 token 明细 |
| `/plan` | 进入 Plan Mode（不做更改） |
| `/ultraplan` | 云端 Plan Mode —— 在云端起草，在浏览器中审阅（v2.1.91+） |
| `/execute` | 退出 Plan Mode（应用更改） |
| `/model` | 切换模型（sonnet/opus/opusplan） |
| `/insights` | 使用情况分析 + 优化报告 |
| `/simplify` | 检测已更改代码中的过度设计并自动修复 |
| `/batch` | 通过 5–30 个并行 worktree agents 进行大规模重构 |
| `/teleport` | 从 web 传送会话 |
| `/tasks` | 监控后台任务 |
| `/remote-env` | 配置云端环境 |
| `/remote-control` | 启动远程控制会话（Research Preview，Pro/Max） |
| `/rc` | /remote-control 的别名 |
| `/mobile` | 获取 Claude 移动应用下载链接 |
| `/fast` | 切换快速模式（2.5 倍速度，6 倍成本） |
| `/voice` | 切换语音输入（按住 Space 说话，松开发送） |
| `/recap` | 休息后返回时的会话上下文摘要（v2.1.108） |
| `/effort [level]` | 思考深度：low/medium/high/xhigh/max；无参数 = 交互式滑块（v2.1.111） |
| `/tui [fullscreen]` | 全屏无闪烁 TUI 渲染（v2.1.110） |
| `/focus` | 切换极简专注视图，独立于 Ctrl+O（v2.1.110） |
| `/less-permission-prompts` | 扫描会话记录并提议一个只读工具白名单（v2.1.111） |
| `/btw [question]` | 旁支问题浮层 —— 只读临时 agent，不污染历史，不调用工具 |
| `/loop [interval] [prompt]` | 重复运行一个 prompt（例如：`/loop 5m check the deploy`，默认 10m） |
| `/stats` | 使用情况图表、常用模型、连续记录 *（自 v2.1.118 起为 `/usage` 的别名）* |
| `/usage` | 按模型统计的 token + 成本使用情况（v2.1.118） |
| `/ultrareview` | 多 agent 云端代码审查（v2.1.114） |
| `/goal [condition]` | 自主多轮模式：Claude 持续工作直到满足条件，实时浮层显示已用时间/轮数/token（v2.1.139） |
| `/scroll-speed` | 通过交互式实时预览滑块调节鼠标滚轮滚动速度（v2.1.139） |
| `/rename [name]` | 命名或重命名当前会话 |
| `/copy` | 交互式选择器，用于复制某个代码块或完整回复 |
| `/debug` | 系统化排查 |
| `/exit` | 退出（或 Ctrl+D） |

---

## 键盘快捷键

| 快捷键 | 作用 |
|----------|--------|
| `Shift+Tab` | 切换权限模式 |
| `Esc` × 2 | 回退（撤销） |
| `Ctrl+C` | 中断 |
| `Ctrl+R` | 搜索命令历史 |
| `Ctrl+L` | 清屏（保留上下文） |
| `Tab` | 自动补全 |
| `Shift+Enter` | 换行 |
| `Ctrl+B` | 后台任务 |
| `Ctrl+F` | 终止所有后台 agents（双击） |
| `Alt+T` | 切换 thinking |
| `Space`（按住） | 语音输入（需启用 `/voice`） |
| `Ctrl+D` | 退出 |

---

## 文件引用

```
@path/to/file.ts    → Reference a file
@agent-name         → Call an agent
!shell-command      → Run shell command
```

| IDE | 快捷键 |
|-----|----------|
| VS Code | `Alt+K` |
| JetBrains | `Cmd+Option+K` |

---

## 鲜为人知的功能（但都是官方的！）

| 功能 | 起始版本 | 作用 |
|---------|-------|--------------|
| **Tasks API** | v2.1.16 | 带依赖关系的持久化任务列表 |
| **Background Agents** | v2.0.60 | 子 agent 在你编码时同步工作 |
| **Agent Teams** | v2.1.32 | 多 agent 协调（TeamCreate/SendMessage） |
| **Auto-Memories** | v2.1.32 | 自动跨会话捕获上下文 |
| **Session Forking** | v2.1.19 | 回退 + 创建并行时间线 |
| **LSP Tool** | v2.0.74 | 类 IDE 导航：符号、类型、引用。约 50ms，相比 grep 的 45s。支持 11 种语言 |
| **Voice Mode** | v2.1.x | 原生语音输入，免费转录，不影响速率限制 |
| **Remote Control** | v2.1.51 | 从手机/浏览器控制本地会话（Research Preview，Pro/Max） |
| **`/loop`** | v2.1.71 | 会话范围内的重复调度器：`/loop 5m check the deploy`（会话结束时停止）。最短 1 分钟，每会话最多 50 个任务 |
| **`/goal`** | v2.1.139 | 自主完成循环：设定一个条件，Claude 跨轮次工作，直到一个独立的评估器（Haiku）验证其已满足。实时浮层显示已用时间、轮数和 token。三要素公式：可衡量的终态 + 验证机制 + 约束条件。 |
| **Cloud Scheduled Tasks** | 2026 | 通过 `/schedule` 或 `claude.ai/code/scheduled` 实现关机调度。运行于 Anthropic 基础设施，每次运行重新克隆仓库，最短间隔 1 小时。Pro/Max/Team/Enterprise |
| **Desktop Scheduled Tasks** | 2026 | 通过桌面应用进行本地机器调度。最短 1 分钟，完整本地文件访问，无需会话 |
| **Skill Evals** | 2026 年 3 月 | 两种 skill 类型：Capability Uplift（填补模型能力差距，会逐渐淡出）/ Encoded Preference（编码工作流，会持续保留）。Benchmark Mode、A/B 测试、Trigger Tuning。 |
| **Output Styles** | v2.1.108 | `/config` → "Preferred output style"：**Default**（简洁）、**Explanatory**（添加设计理由）、**Learning**（结对编程，`TODO(human)` 标记）。通过 `.claude/styles/` 自定义样式。 |

**启用 LSP**：在 `~/.claude/settings.json` 中添加 → `{ "env": { "ENABLE_LSP_TOOL": "1" } }`（需为你的语言安装 LSP 服务器：`tsserver`、`pylsp`、`gopls`、`rust-analyzer`、`sourcekit-lsp`……）

**小贴士**：这些并非"秘密"——它们都在 [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) 中。去读一读！

---

## 权限模式

| 模式 | 编辑 | 执行 |
|------|---------|-----------|
| Default | 询问 | 询问 |
| acceptEdits | 自动 | 询问 |
| Plan Mode | ❌ | ❌ |
| auto | 由分类器决定 | 由分类器决定 |
| dontAsk | 仅当在允许规则中 | 仅当在允许规则中 |
| bypassPermissions | 自动 | 自动（仅限 CI/CD） |

**Shift+Tab** 切换模式

---

## 记忆与设置（2 个层级）

| 层级 | macOS/Linux | Windows | 范围 | Git |
|-------|-------------|---------|-------|-----|
| **项目级** | `.claude/` | `.claude\` | 团队 | ✅ |
| **个人级** | `~/.claude/` | `%USERPROFILE%\.claude\` | 你（所有项目） | ❌ |

**优先级**：项目级覆盖个人级

| 文件 | 位置 | 用途 |
|------|-------|-------|
| `CLAUDE.md` | 项目根目录 | 团队记忆（指令） |
| `settings.json` | `.claude/` | 团队设置（hooks） |
| `settings.local.json` | `.claude/` | 你的设置覆盖 |
| `CLAUDE.md` | `~/.claude/`（Win：`%USERPROFILE%\.claude\`） | 个人记忆 |

---

## .claude/ 文件夹结构

```
.claude/
├── CLAUDE.md           # Local memory (gitignored)
├── settings.json       # Hooks (committed)
├── settings.local.json # Permissions (not committed)
├── agents/             # Custom agents
├── hooks/              # Event scripts
├── rules/              # Auto-loaded rules
└── skills/             # Slash commands + knowledge modules (unified)
```

---

## 典型工作流

```
1. Start session      → claude
2. Check context      → /status
3. Plan Mode          → Shift+Tab × 2 (for complex tasks)
4. Describe task      → Clear, specific prompt
5. Review changes     → Always read the diff!
6. Accept/Reject      → y/n
7. Verify             → Run tests
8. Commit             → When task complete
9. /compact           → When context >70%
```

---

## 上下文管理（关键）

### 状态栏

```
Model: Sonnet | Ctx: 89.5k | Cost: $2.11 | Ctx(u): 56.0%
```
**关注 `Ctx(u):`** → >70% = `/compact`，>85% = `/clear`

**增强状态栏（[ccstatusline](https://github.com/sirmalloc/ccstatusline)）：** 在 `~/.claude/settings.json` 中添加：
```json
{ "statusLine": { "type": "command", "command": "npx -y ccstatusline@latest", "padding": 0 } }
```

### 上下文阈值

| 上下文占用 % | 状态 | 行动 |
|-----------|--------|--------|
| 0-50% | 绿色 | 自由工作 |
| 50-70% | 黄色 | 有所取舍 |
| 70-90% | 橙色 | 立即 `/compact` |
| 90%+ | 红色 | 必须 `/clear` |

### 按症状采取的行动

| 迹象 | 行动 |
|------|--------|
| 回复变短 | `/compact` |
| 频繁遗忘 | `/clear` |
| 上下文 >70% | `/compact` |
| 任务完成 | `/clear` |

### 上下文恢复命令

| 命令 | 用途 |
|---------|-------|
| `/compact` | 总结并释放上下文 |
| `/clear` | 全新开始 |
| `/rewind` | 撤销近期更改 |
| `claude -c` | 恢复上次会话（CLI flag） |
| `claude -r <id>` | 恢复指定会话（CLI flag） |

---

## 底层原理（速览）

| 概念 | 要点 |
|---------|-----------|
| **主循环** | 简单的 `while(tool_call)` —— 没有 DAG，没有分类器 |
| **工具** | 8 个核心工具：Bash、Read、Edit、Write、Grep、Glob、Agent、TodoWrite（[完整 40 工具参考](./core/tools-reference.md)） |
| **上下文** | 约 200K tokens，在 75-92% 时自动 compact |
| **Sub-agents** | 隔离的上下文，最大深度 depth=1 |
| **理念** | "Less scaffolding, more model" —— 信任 Claude 的推理能力 |

**深入了解**：[架构与内部机制](./core/architecture.md)

---

## Plan Mode 与思考

| 特性 | 激活方式 | 用途 |
|---------|------------|-------|
| **Plan Mode** | `Shift+Tab × 2` 或 `/plan` | 在不修改的情况下探索 |
| **OpusPlan** | `/model opusplan` | 用 Opus 做规划，用 Sonnet 执行 |
| **Ultraplan** | `/ultraplan <prompt>` | 云端规划，浏览器审阅，终端保持空闲（v2.1.91+，需要 GitHub） |

> **Opus 4.7**（v2.1.114+）：Claude Code 中的默认 effort = **xhigh**（所有计划）。新增的 `xhigh` 级别位于 `high` 和 `max` 之间 —— 提供更精细的推理/延迟控制。使用 `ultrathink` 可强制下一轮采用 max effort。

| 控制项 | 操作 | 持久性 |
|---------|--------|-------------|
| **Alt+T** | 开关思考功能 | 会话级 |
| **/config** | 全局启用/禁用 | 永久 |
| **`/model` 滑块** | 左右方向键：`low\|medium\|high\|xhigh` | 会话级 |
| **`CLAUDE_CODE_EFFORT_LEVEL`** | 环境变量：`low\|medium\|high\|xhigh\|max` | Shell 会话级 |
| **`effortLevel` 设置** | 在 settings.json 中：`low\|medium\|high\|xhigh\|max` | 永久 |
| **skill frontmatter 中的 `effort`**（v2.1.80+） | 按 skill 覆盖：`low\|medium\|high\|xhigh` | 每次调用 |

**成本提示**：对于简单任务，按 Alt+T 禁用思考 → 更快更省。

**按 skill 设置 effort** —— 给机械性 skill（commit、sync、scaffold）添加 `effort: low`，给分析性 skill（security-audit、architecture-review）添加 `effort: high`。会自动覆盖会话级设置。

**OpusPlan 工作流**：`/model opusplan` → `Shift+Tab × 2`（用 Opus 规划）→ `Shift+Tab`（用 Sonnet 执行）

**Ultraplan 工作流**：`/ultraplan <task>` → 云端起草期间终端空闲 → 在浏览器中内联审阅 → 批准 → 在网页端执行（PR）或传送回终端

**适用于**：涉及 3 个以上文件的功能、架构设计、复杂调试

### 快速选择模型

| 任务 | 模型 | Effort |
|------|-------|--------|
| 重命名、样板代码、测试生成 | Haiku | low |
| 功能开发、调试、重构 | Sonnet | medium–high |
| 架构设计、安全审计 | Opus | high–max |

> 含成本估算的完整决策表：[第 2.5 节 模型选择与思考指南](ultimate-guide.md#25-model-selection--thinking-guide)

### 动态切换模型（会话中途）

**模式**：从 Sonnet 开始（速度）→ 切换到 Opus（复杂度）→ 切回 Sonnet

**工作流**：
```bash
# Session start (default Sonnet)
claude

# Complex feature encountered
> "Implement OAuth2 flow with PKCE"
/model opus                    # Switch to deep reasoning

# Feature complete, back to routine
/model sonnet                  # Speed + cost optimization
```

**最佳实践**：
- ✅ 在**任务边界**切换，而非任务中途
- ✅ 在以下场景使用 Opus：架构决策、复杂调试、安全关键代码
- ✅ 在以下场景使用 Sonnet：常规编辑、重构、编写测试
- ✅ 在以下场景使用 Haiku：简单修复、错别字、校验检查
- ❌ 不要在实现过程中途切换（会丢失上下文）

**成本影响**：
| 模型 | 输入 | 输出 | 适用场景 |
|-------|--------|--------|----------|
| Opus 4.7 | $5/MTok | $25/MTok | 复杂推理（占任务的 10-20%） |
| Sonnet 4.6 | $3/MTok | $15/MTok | 大多数开发工作（占任务的 70-80%） |
| Haiku 4.5 | $0.80/MTok | $4/MTok | 简单校验（占任务的 5-10%） |

**动态切换**在保证复杂任务质量的同时优化成本。

**来源**：[Gur Sannikov 嵌入式工程工作流](https://www.linkedin.com/posts/gursannikov_claudecode-embeddedengineering-aiagents-activity-7423851983331328001-DrFb)

---

## MCP Servers

| 服务器 | 用途 |
|--------|---------|
| **Serena** | 索引 + 会话记忆 + 符号搜索 |
| **grepai** | 语义搜索 + 调用图分析 |
| **Context7** | 库文档 |
| **Sequential** | 结构化推理 |
| **Playwright** | 浏览器自动化 |
| **Postgres** | 数据库查询 |
| **doobidoo** | 语义记忆 + 多客户端 + Knowledge Graph |

**Serena 记忆**：`write_memory()` / `read_memory()` / `list_memories()`

**Serena 索引**：
```bash
# Initial index
uvx --from git+https://github.com/oraios/serena serena project index

# Force rebuild
serena project index --force-full

# Incremental update (faster)
serena project index --incremental --parallel 4
```

检查状态：`/mcp`

---

## 创建自定义组件

### Agent（`.claude/agents/my-agent.md`）
```yaml
---
name: my-agent
description: Use when [trigger]
model: sonnet
tools: Read, Write, Edit, Bash
---
# Instructions here
```

### Skill —— 用户可调用（`.claude/skills/my-command/SKILL.md`）
```markdown
---
description: Brief description
argument-hint: "<required_arg> [--flag]"
disable-model-invocation: true
---
# Command Name
Instructions for what to do...
$ARGUMENTS[0] $ARGUMENTS[1] (or $0 $1) - user args
```

### Hook（macOS/Linux：`.sh` | Windows：`.ps1`）

**Bash**（macOS/Linux）：
```bash
#!/bin/bash
INPUT=$(cat)
# Process JSON input
exit 0  # 0=continue, 2=block
```

**PowerShell**（Windows）：
```powershell
$input = [Console]::In.ReadToEnd() | ConvertFrom-Json
# Process JSON input
exit 0  # 0=continue, 2=block
```

---

## 反模式

| ❌ 不要 | ✅ 应该 |
|----------|-------|
| 模糊的 prompt | 用 @references 指定文件 + 行号 |
| 不阅读就接受 | 阅读每一处 diff |
| 忽略警告 | 在 70% 时使用 `/compact` |
| 跳过权限 | 生产环境中绝不跳过 |
| 只给否定约束 | 提供替代方案 |

---

## 快速 Prompt 公式

```
WHAT: [Concrete deliverable]
WHERE: [File paths]
HOW: [Constraints, approach]
VERIFY: [Success criteria]
```

**示例：**
```
Add input validation to the login form.
WHERE: src/components/LoginForm.tsx
HOW: Use Zod schema, show inline errors
VERIFY: Empty email shows error, invalid format shows error
```

---

## CLI Flags 快速参考

| Flag | 用途 |
|------|-------|
| `-p "query"` | 非交互模式（CI/CD） |
| `-c` / `--continue` | 继续上一个会话 |
| `-r` / `--resume <id>` | 恢复指定会话 |
| `--teleport` | 从网页端传送会话 |
| `remote-control` | 子命令：启动远程控制会话 |
| `--model sonnet` | 切换模型 |
| `--add-dir ../lib` | 允许访问 CWD 之外的目录 |
| `--permission-mode plan` | Plan 模式 |
| `--tools "Tool1,Tool2"` | 为本次会话启用特定工具 |
| `--max-budget-usd 5.00` | 最大 API 花费上限（print 模式） |
| `--system-prompt "..."` | 追加自定义系统 prompt |
| `--worktree` / `-w` | 在隔离的 git worktree 中运行 |
| `--dangerously-skip-permissions` | 自动接受（谨慎使用） |
| `--debug` | 调试输出 |
| `--allowedTools "Edit,Read"` | 工具白名单 |

> 完整 CLI 参考（约 45 个 flag）：参见 [code.claude.com 上的 cli-reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference)

## 关键 CLI 子命令

| Command | 说明 |
|---------|-------------|
| `claude project purge [path]` | 删除某个项目的所有 Claude Code 状态（transcript、任务、配置）。使用 `--dry-run` 预览。(v2.1.126) |
| `claude ultrareview [target]` | 面向 CI 的非交互式云端代码审查。`--json` 输出。退出码 0/1。(v2.1.120) |
| `claude plugin prune` | 移除孤立的自动安装 plugin 依赖。(v2.1.121) |
| `claude plugin details <name>` | 显示 plugin 清单及 token 成本估算。(v2.1.139) |
| `claude --plugin-url <url>` | 在本次会话中从 URL 加载 plugin `.zip`。(v2.1.129) |

---

## 调试命令

```bash
claude --version     # Version
claude update        # Check/install updates
claude doctor        # Diagnostic
claude --debug       # Verbose mode
claude --mcp-debug   # Debug MCPs
/mcp                 # MCP status (inside Claude)
```

---

## CI/CD 模式（无头）

```bash
# Non-interactive execution
claude -p "analyze this file" src/api.ts

# JSON output
claude -p "review" --output-format json

# Economic model
claude -p "lint" --model haiku

# With auto-accept
claude -p "fix typos" --dangerously-skip-permissions
```

---

## 远程控制 — 移动端访问 (v2.1.51+, Research Preview)

> **仅限 Pro/Max** — 不适用于 Team、Enterprise 或 API key

```bash
# Start from terminal (new session)
claude remote-control

# Or from inside an active session:
/rc        # (or /remote-control)
```

**从手机/平板/浏览器连接：**
1. 扫描 **二维码**（启动后按空格键）
2. 或在浏览器 / Claude 移动应用中打开 **会话 URL**
3. 或者：`/mobile` → 显示 App Store + Play Store 链接

| ⚠️ 已知限制 | 详情 |
|--------------------|--------|
| 一次仅一个会话 | 只能有一个远程会话处于活动状态 |
| Slash commands 失效 | `/new`、`/compact` 在远程端会变成纯文本 → 请在本地终端使用 |
| 终端必须保持打开 | 关闭本地终端会结束会话 |
| 网络超时 | 断连约 10 分钟 → 会话过期 |

**进阶：tmux 多会话**（绕过单会话限制）
```bash
tmux new-session -s dev
# Each pane = its own claude session
# Run /rc in the pane you want to control remotely
```

**自动启用：** `/config` → 切换 "Remote Control: auto-enable"

**完整文档**：[§9.22 远程控制](ultimate-guide.md#922-remote-control-mobile-access) | [安全说明](security/security-hardening.md#remote-control-security)

---

## 任务管理 (v2.1.16+)

**有两套系统可用：**

| 系统 | 适用场景 | 持久化 |
|--------|-------------|-------------|
| **Tasks API** (v2.1.16+) | 多会话项目、依赖关系 | ✅ 磁盘 (`~/.claude/tasks/`) |
| **TodoWrite**（旧版） | 简单的单会话 | ❌ 仅会话内 |

### Tasks API 命令

```bash
# Enable persistence across sessions
export CLAUDE_CODE_TASK_LIST_ID="project-name"
claude

# Inside Claude: Create task hierarchy
> "Create tasks for auth system with dependencies"

# Resume later (new session)
export CLAUDE_CODE_TASK_LIST_ID="project-name"
claude
> "TaskList to see current state"
```

**核心能力：**
- 📁 **持久化**：在会话结束、上下文 compaction 后依然保留
- 🔗 **依赖关系**：任务 A 阻塞任务 B
- 🔄 **多会话**：将状态广播到多个终端
- 📊 **状态**：pending → in_progress → completed/failed

**⚠️ 限制**：TaskList 仅显示 `id`、`subject`、`status`、`blockedBy`。
若需 `description`/`metadata` → 对每个任务使用 `TaskGet(taskId)`。

**提示**：将关键信息存入 `subject` 以便快速浏览。

**迁移标志** (v2.1.19+)：
```bash
# Revert to old TodoWrite system
CLAUDE_CODE_ENABLE_TASKS=false claude
```

**→ 完整工作流**：[guide/workflows/task-management.md](workflows/task-management.md)

---

## 黄金法则

1. **始终审查 diff** 后再接受
2. 在上下文进入临界（>70%）之前 **使用 `/compact`**
3. 请求时 **要具体**（做什么、在哪里、怎么做、如何验证）
4. 复杂/高风险任务 **先用 Plan Mode**
5. 为每个项目 **创建 CLAUDE.md**
6. 每完成一个任务就 **频繁提交**
7. **清楚发送了什么** —— prompt、文件、MCP 结果 → Anthropic（[退出训练](https://claude.ai/settings/data-privacy-controls)）

---

## 快速决策树

```
Simple task       → Just ask Claude
Complex task      → Tasks API to plan first
Risky change      → Plan Mode first
Repeating task    → Create agent or command
Context full      → /compact or /clear
Need docs         → Use Context7 MCP
Deep analysis     → Use Opus (thinking on by default)
```

---

## 常见问题快速修复

| 问题 | 解决方案 |
|---------|----------|
| "Command not found" | 检查 PATH，重新安装：`curl -fsSL https://claude.ai/install.sh \| sh` |
| 上下文过高（>70%） | 立即执行 `/compact` |
| 响应缓慢 | `/compact` 或 `/clear` |
| MCP 不工作 | `claude mcp list`，检查配置 |
| Permission denied | 检查 `settings.local.json` |
| Hook 阻塞 | 检查 hook 退出码，审查逻辑 |

**健康检查脚本**（保存并运行）：
```bash
# macOS/Linux
which claude && claude doctor && claude mcp list

# Windows PowerShell
where.exe claude; claude doctor; claude mcp list
```

---

## 成本优化

| 模型 | 适用于 | 成本 |
|-------|---------|------|
| Haiku | 简单修复、审查 | $ |
| Sonnet | 大多数开发工作 | $$ |
| Opus | 架构、复杂 bug | $$$ |
| OpusPlan | 规划 (Opus) + 执行 (Sonnet) | $$ |

**提示**：使用 `--add-dir` 允许工具访问当前工作目录之外的目录

---

## 社区工具

| 工具 | 用途 | 安装 |
|------|---------|---------|
| **ccusage** | 成本跟踪与报告 | `bunx ccusage daily` |
| **RTK** | Token 缩减（60-90%） | `brew install rtk-ai/tap/rtk` 或 `cargo install rtk` · [站点](https://www.rtk-ai.app/) |
| **claude-code-viewer** | 会话历史 UI | `npx @kimuson/claude-code-viewer` |
| **Entire CLI** | 会话检查点 + 治理 | [entire.io](https://entire.io)（2026 年 2 月） |

> **Entire CLI**：由前 GitHub CEO 打造的 agent 原生平台，具备可回退检查点、审批门控、审计跟踪。适用于合规场景（SOC2、HIPAA）或多 agent 工作流。

---

## 搜索工具快速参考

快速决策（5 秒）：精确文本 → `rg` | 精确名称 → `rg`/Serena | 概念 → grepai | 结构 → ast-grep

| 任务 | 工具 | 命令 |
|------|------|---------|
| "查找 TODO 注释" | `rg` | `rg "TODO"` |
| "查找认证代码" | `grepai` | `grepai search "authentication"` |
| "谁调用了 login？" | `grepai` | `grepai trace callers "login"` |
| "获取文件结构" | `Serena` | `serena get_symbols_overview` |
| "没有 try/catch 的 async" | `ast-grep` | `ast-grep "async function $F"` |

速度：`rg`（约 20ms）→ Serena（约 100ms）→ ast-grep（约 200ms）→ grepai（约 500ms）

> 完整工作流：[workflows/search-tools-mastery.md](./workflows/search-tools-mastery.md)

---

## 资源

- **官方文档**：[docs.anthropic.com/claude-code](https://docs.anthropic.com/en/docs/claude-code)
- **进阶指南**：[Claudelog.com](https://claudelog.com/) - 技巧与模式
- **完整指南**：`ultimate-guide.md`（本仓库）
- **白皮书（FR + EN）**：[cc.bruniaux.com/whitepapers](https://cc.bruniaux.com/whitepapers/) — 10 份主题 PDF
- **项目记忆**：在项目根目录创建 `CLAUDE.md`
- **DeepSeek（高性价比）**：通过 `ANTHROPIC_BASE_URL` 配置

---

**作者**：Florian BRUNIAUX | [@Méthode Aristote](https://methode-aristote.fr) | 使用 Claude 撰写

*最后更新：2026 年 5 月 | 版本 3.41.1*
