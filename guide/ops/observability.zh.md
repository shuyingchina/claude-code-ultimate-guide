---
title: "Session Observability & Monitoring"
description: "Track Claude Code usage, estimate costs, and identify patterns across development sessions"
tags: [observability, guide, performance]
---

# 会话可观测性与监控

> 追踪 Claude Code 使用情况、估算成本，并识别开发会话中的各种模式。

## 目录

1. [为何要监控会话](#why-monitor-sessions)
2. [会话搜索与恢复](#session-search--resume)
3. [设置会话日志](#setting-up-session-logging)
4. [分析会话数据](#analyzing-session-data)
5. [成本追踪](#cost-tracking)
6. [活动监控](#activity-monitoring)
7. [外部监控工具](#external-monitoring-tools)
8. [代理 Claude Code 流量](#proxying-claude-code)
9. [模式与最佳实践](#patterns--best-practices)
10. [局限性](#limitations)

---

## 为何要监控会话

Claude Code 的使用量会快速累积，尤其在活跃开发期间。监控可以帮助你：

- **了解成本**：在账单到来之前估算 API 开销
- **识别模式**：查看你最常使用哪些工具、哪些文件被反复编辑
- **优化工作流**：发现低效之处（例如反复读取同一个大文件）
- **追踪项目**：在不同代码库之间对比使用情况
- **团队可见性**：汇总使用数据以进行团队预算（在合并日志时）

---

## 会话搜索与恢复

使用 Claude Code 数周后，找回过往的对话会变得困难。本节介绍原生选项和社区工具。

### 原生命令

| 命令 | 使用场景 |
|---------|----------|
| `claude -c` / `claude --continue` | 恢复最近一次会话 |
| `claude -r <id>` / `claude --resume <id>` | 按 ID 恢复指定会话 |
| `claude --resume` | 交互式会话选择器 |

会话以 JSONL 文件的形式本地存储于 `~/.claude/projects/<project>/`。

### 社区工具对比

| 工具 | 安装 | 列表速度 | 搜索速度 | 依赖 | 恢复命令 |
|------|---------|------------|--------------|--------------|----------------|
| **session-search.sh**（本仓库） | 复制脚本 | **10ms** | **400ms** | 无（bash） | ✅ 显示 |
| claude-conversation-extractor | `pip install` | 230ms | 1.7s | Python | ❌ |
| claude-code-transcripts | `uvx` | N/A | N/A | Python | ❌ |
| ran CLI | `npm -g` | N/A | 快 | Node.js | ❌（仅命令） |

### 推荐：session-search.sh

零依赖的 bash 脚本，针对速度进行了优化，并提供可直接使用的恢复命令。

**安装：**
```bash
cp examples/scripts/session-search.sh ~/.claude/scripts/cs
chmod +x ~/.claude/scripts/cs
echo "alias cs='~/.claude/scripts/cs'" >> ~/.zshrc
source ~/.zshrc
```

**用法：**
```bash
cs                          # List 10 most recent sessions (~15ms)
cs "authentication"         # Single keyword search (~400ms)
cs "Prisma migration"       # Multi-word AND search (both must match)
cs -n 20                    # Show 20 results
cs -p myproject "bug"       # Filter by project name
cs --since 7d               # Sessions from last 7 days
cs --since today            # Today's sessions only
cs --json "api" | jq .      # JSON output for scripting
cs --rebuild                # Force index rebuild
```

**输出：**
```
2026-01-15 08:32 │ my-project             │ Implement OAuth flow for...
  claude --resume 84287c0d-8778-4a8d-abf1-eb2807e327a8

2026-01-14 21:13 │ other-project          │ Fix database migration...
  claude --resume 1340c42e-eac5-4181-8407-cc76e1a76219
```

复制并粘贴 `claude --resume` 命令即可继续任意会话。

### 工作原理

1. **索引模式**（无过滤器）：使用缓存的 TSV 索引。会话变更时自动刷新。查找耗时约 15ms。
2. **搜索模式**（带关键词/过滤器）：全文搜索，超时时间为 3s。多词查询使用 AND 逻辑。
3. **过滤器**：`--project`（子串匹配）、`--since`（支持 `today`、`yesterday`、`7d`、`YYYY-MM-DD`）
4. **输出**：默认为人类可读格式，`--json` 用于脚本化。排除 agent/subagent 会话。

### 备选方案：Python 工具

如果你偏好更丰富的功能（HTML 导出、多种格式）：

```bash
# Install
pip install claude-conversation-extractor

# Interactive UI
claude-start

# Direct search
claude-search "keyword"

# Export to markdown
claude-extract --format markdown
```

完整脚本参见 [session-search.sh](../../examples/scripts/session-search.sh)。

---

### 会话恢复的局限性与跨目录迁移

**一句话总结**：原生 `--resume` 在设计上仅限于当前工作目录。对于跨目录迁移，请使用手动文件系统操作（推荐）或社区自动化工具（未经测试）。

#### 为何恢复受目录范围限制

Claude Code 将会话存储于 `~/.claude/projects/<encoded-path>/`，其中 `<encoded-path>` 派生自项目的绝对路径。例如：
- 位于 `/home/user/myapp` 的项目 → 会话存于 `~/.claude/projects/-home-user-myapp-/`
- 项目移动到 `/home/user/projects/myapp` → Claude 会查找 `~/.claude/projects/-home-user-projects-myapp-/`（不同的目录）

**设计理由**：会话存储绝对文件路径、项目专属上下文（MCP server 配置、`.claudeignore` 规则、环境变量）。跨目录恢复需要路径重写和上下文校验，目前尚未实现。

**相关**：GitHub issue [#1516](https://github.com/anthropics/claude-code/issues/1516) 跟踪了社区对原生跨目录支持的需求。

#### 手动迁移（推荐）

**移动项目文件夹时：**

```bash
# Before moving project
cd ~/.claude/projects/
ls -la  # Note the current encoded path

# Move your project
mv /old/location/myapp /new/location/myapp

# Rename session directory to match new path
cd ~/.claude/projects/
mv -- -old-location-myapp- -new-location-myapp-

# Verify
cd /new/location/myapp
claude --continue  # Should resume successfully
```

**将会话 fork 到新项目时：**

```bash
# Copy session files (preserves original)
cd ~/.claude/projects/
cp -n ./-source-project-/*.jsonl ./-target-project-/

# Copy subagents directory if exists
if [ -d ./-source-project-/subagents ]; then
  cp -r ./-source-project-/subagents ./-target-project-/
fi

# Resume in target project
cd /path/to/target/project
claude --continue
```

#### ⚠️ 迁移风险与注意事项

**迁移会话前，请验证兼容性：**

| 风险 | 影响 | 缓解措施 |
|------|--------|------------|
| **硬编码密钥** | 凭据在新上下文中暴露 | 迁移前审计 `.jsonl` 文件，必要时脱敏 |
| **绝对路径** | 路径不同则文件引用失效 | 验证目标中路径存在，或接受失效引用 |
| **MCP server 配置** | 目标中缺少源端 MCP server | 恢复前安装匹配的 MCP server |
| **`.claudeignore` 规则** | 忽略模式不同 | 检查差异，必要时合并 |
| **环境变量** | `process.env` 上下文不匹配 | 检查 `.env` 文件兼容性 |

**不应迁移会话的情形：**

- 依赖冲突（例如 Node.js 版本不同、包管理器不同）
- 数据库状态差异（迁移已在源端应用而目标端未应用）
- 认证上下文（API token、源项目专属的 OAuth 会话）
- 安全边界（从私有仓库迁移到公开仓库）

#### 社区自动化工具

**claude-migrate-session**（作者 Jim Weller，灵感来自 Alexis Laporte）自动化了上述手动流程：

- **仓库**：[jimweller/dotfiles](https://github.com/jimweller/dotfiles/tree/main/dotfiles/claude-code/skills/claude-migrate-session)
- **功能**：带过滤的全局搜索，保留 `.jsonl` + subagents，使用 ripgrep 提升性能
- **状态**：个人 dotfiles（截至 2026 年 2 月 0 stars/forks），采用率有限
- **命令**：`/claude-migrate-session <source> <target>`

**⚠️ 注意**：该工具几乎未经社区测试。手动方式更安全，并能让你对迁移内容有明确的控制权。在生产工作流中使用前请充分测试。

**迁移的使用场景：**
- 将原型工作 fork 进生产代码库
- 将调试会话移至隔离的测试仓库
- 在新项目中继续架构讨论

#### 备选方案：整个 CLI 会话的可移植性

**原生局限**：Claude Code 的 `--resume` 绑定到绝对文件路径，文件夹移动后即失效。

**Entire CLI 方案**：检查点是**路径无关的**，从而实现跨项目位置的真正会话可移植性。

**工作原理：**

```bash
# In source project
cd /old/location/myapp
entire capture --agent="claude-code"
[... work in Claude Code ...]
entire checkpoint --name="migration-complete"

# Move project to new location
mv /old/location/myapp /new/location/myapp

# Resume in target (works because Entire stores relative paths)
cd /new/location/myapp
entire resume --checkpoint="migration-complete"
claude --continue  # Resumes with full context
```

**为何 Entire 检查点可移植：**

| 方面 | 原生 `--resume` | Entire CLI |
|--------|-------------------|-----------|
| **路径存储** | JSONL 中的绝对路径 | 检查点中的相对路径 |
| **跨目录** | 失效（项目编码不同） | 可用（路径无关） |
| **上下文保留** | 仅提示历史 | 提示 + 推理 + 文件状态 |
| **agent 交接** | 否 | 是（在 Claude/Gemini 之间） |

**何时使用 Entire 而非手动迁移：**

- ✅ 频繁的项目移动/fork
- ✅ 多 agent 工作流（Claude → Gemini 交接）
- ✅ 用于调试的会话回放（回退到精确状态）
- ✅ 治理（恢复时的审批关卡）

**权衡**：增加工具依赖 + 存储开销（约项目体积的 5-10%）。

> **完整文档**：[AI 可追溯性指南](./ai-traceability.md#51-entire-cli)

---

### 多 Agent 编排监控

要通过外部编排器（Gas Town、multiclaude）监控多个并发的 Claude Code 实例，参见：

- **agent-chat**（https://github.com/justinabrahms/agent-chat）：类似 Slack 的 agent 通信实时 UI
- **架构指南**：`guide/ai-ecosystem.md` 第 8.1 节 - 多 Agent 编排系统

**架构模式**（用于自定义实现）：
1. Hook 记录 Task agent 的派生：`.claude/hooks/multi-agent-logger.sh`
2. 存入 SQLite：`~/.claude/logs/agents.db`（parent_id、child_id、timestamp、task）
3. 通过 SSE 流式传输：简单的 Go/Node HTTP 服务器
4. 仪表盘：消费 SSE 流的 React/HTML

**原生 Claude Code 监控**（本指南）：
- 会话搜索：`session-search.sh`（参见[会话搜索与恢复](#session-search--resume)）
- 活动日志：`session-logger.sh` hook（参见[设置会话日志](#setting-up-session-logging)）
- 统计分析：`session-stats.sh`（参见[分析会话数据](#analyzing-session-data)）

**何时使用外部编排器监控**：
- 运行 Gas Town 或 multiclaude，并有 5 个以上并发 agent
- 需要对 agent 协调进行实时可见性观测
- 调试编排故障（agent 冲突、合并问题）

**何时原生监控已足够**：
- 单个 Claude Code 会话，或 subagent 少于 3 个的 `--delegate`
- 事后分析（日志、统计）即可满足需求
- 预算/复杂度受限

---

## 设置会话日志记录

### 1. 安装 Logger Hook

将会话 logger 复制到你的 hooks 目录:

```bash
# Create hooks directory if needed
mkdir -p ~/.claude/hooks

# Copy the logger (from this repo's examples)
cp examples/hooks/bash/session-logger.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/session-logger.sh
```

### 2. 在 Settings 中注册

添加到 `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "type": "command",
        "command": "~/.claude/hooks/session-logger.sh"
      }
    ]
  }
}
```

### 3. 验证安装

运行几条 Claude Code 命令,然后检查日志:

```bash
ls ~/.claude/logs/
# Should see: activity-2026-01-14.jsonl

# View recent entries
tail -5 ~/.claude/logs/activity-$(date +%Y-%m-%d).jsonl | jq .
```

### 配置选项

| 环境变量 | 默认值 | 描述 |
|---------------------|---------|-------------|
| `CLAUDE_LOG_DIR` | `~/.claude/logs` | 日志存储位置 |
| `CLAUDE_LOG_TOKENS` | `true` | 启用 token 估算 |
| `CLAUDE_SESSION_ID` | 自动生成 | 自定义会话标识符 |

---

## 分析会话数据

### 使用 session-stats.sh

```bash
# Copy the script
cp examples/scripts/session-stats.sh ~/.local/bin/
chmod +x ~/.local/bin/session-stats.sh

# Today's summary
session-stats.sh

# Last 7 days
session-stats.sh --range week

# Specific date
session-stats.sh --date 2026-01-14

# Filter by project
session-stats.sh --project my-app

# Machine-readable output
session-stats.sh --json
```

### 示例输出

```
═══════════════════════════════════════════════════════════
        Claude Code Session Statistics - today
═══════════════════════════════════════════════════════════

Summary
  Total operations:  127
  Sessions:          3

Token Usage
  Input tokens:      45,230
  Output tokens:     12,450
  Total tokens:      57,680

Estimated Cost (Sonnet rates)
  Input:   $0.1357
  Output:  $0.1868
  Total:   $0.3225

Tools Used
  Edit: 45
  Read: 38
  Bash: 24
  Grep: 12
  Write: 8

Projects
  my-app: 89
  other-project: 38
```

### 读懂质量,而不只是数量

token 计数告诉你使用了多少 Claude Code。JSONL 日志还能告诉你**你的配置工作得如何**——前提是你知道该关注什么。

除了成本指标之外,有三种模式可以可靠地表明某个 skill、规则或 CLAUDE.md 章节需要更新:

**反复读取同一个文件**

如果 Claude 在一次会话中读取同一个文件 3 次以上,那么它所需要的内容很可能并不在它预期找到的位置。考虑把相关上下文移入某个 skill 或 CLAUDE.md 章节。

```bash
# Files read more than 3x in recent sessions
jq -r 'select(.tool == "Read") | .file' ~/.claude/logs/activity-*.jsonl \
  | sort | uniq -c | sort -rn | awk '$1 > 3'
```

**同一条命令上的工具失败**

一条 Bash 命令在多次会话中反复失败,通常意味着某个 skill 中存在过时的路径、被重命名的二进制文件,或者已经无法在你当前技术栈下工作的命令。

```bash
# Failing commands
jq -r 'select(.tool == "Bash" and (.exit_code // 0) != 0) | .command' \
  ~/.claude/logs/activity-*.jsonl | sort | uniq -c | sort -rn | head -10
```

**同一个文件上的高频编辑**

跨会话被大量编辑的文件,往往表明上下文缺失——该文件的用途对 agent 来说不够清晰,或者围绕它的约定没有被记录下来。

```bash
# Most-edited files (proxy for context gaps)
jq -r 'select(.tool == "Edit") | .file' ~/.claude/logs/activity-*.jsonl \
  | sort | uniq -c | sort -rn | head -10
```

对于你发现的每一种模式,都要问:是否存在某个 skill、规则或 CLAUDE.md 章节应当涵盖这一点?完整工作流程见 [§9.23 配置生命周期与更新循环](#923-configuration-lifecycle-the-update-loop)。

---

### 日志格式

每条日志条目都是一个 JSON 对象:

```json
{
  "timestamp": "2026-01-14T15:30:00Z",
  "session_id": "1705234567-12345",
  "tool": "Edit",
  "file": "src/components/Button.tsx",
  "project": "my-app",
  "tokens": {
    "input": 350,
    "output": 120,
    "total": 470
  }
}
```

---

## 成本追踪

### token 估算方法

logger 使用一个简单的启发式方法估算 token:**每个 token 约 4 个字符**。这是近似值,且往往会略微高估。

### 成本费率

默认费率针对 Claude Sonnet。可通过环境变量调整:

```bash
# Sonnet rates (default)
export CLAUDE_RATE_INPUT=0.003   # $3/1M tokens
export CLAUDE_RATE_OUTPUT=0.015  # $15/1M tokens

# Opus rates (if using Opus)
export CLAUDE_RATE_INPUT=0.015   # $15/1M tokens
export CLAUDE_RATE_OUTPUT=0.075  # $75/1M tokens

# Haiku rates
export CLAUDE_RATE_INPUT=0.00025 # $0.25/1M tokens
export CLAUDE_RATE_OUTPUT=0.00125 # $1.25/1M tokens
```

### 预算告警(手动模式)

将以下内容添加到你的 shell 配置文件中,以获得每日预算警告:

```bash
# ~/.zshrc or ~/.bashrc
claude_budget_check() {
  local cost=$(session-stats.sh --json 2>/dev/null | jq -r '.summary.estimated_cost.total // 0')
  local threshold=5.00  # $5 daily budget

  if (( $(echo "$cost > $threshold" | bc -l) )); then
    echo "⚠️  Claude Code daily spend: \$$cost (threshold: \$$threshold)"
  fi
}

# Run on shell start
claude_budget_check
```

---

## 活动监控

成本追踪告诉你*花了多少钱*。活动监控告诉你 *Claude Code 实际做了什么*：它读取了哪些文件、运行了哪些命令、抓取了哪些 URL。这是审计层。

### 会话 JSONL：真相之源

Claude Code 发起的每一次工具调用都记录在 `~/.claude/projects/<project>/` 下的会话 JSONL 文件中。每个 `type: "assistant"` 的条目都包含一个 `content` 数组，其中 `type: "tool_use"` 的块记录了每一次操作。

```bash
# Find your session files
ls ~/.claude/projects/-$(pwd | tr '/' '-')-/

# Inspect tool calls in a session
cat ~/.claude/projects/-your-project-/SESSION_ID.jsonl | \
  jq 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use") | {tool: .name, input: .input}'
```

### 工具调用揭示了什么

| 工具 | 它暴露了什么 |
|------|----------------|
| `Read` | 访问的文件（路径、行范围） |
| `Write` / `Edit` | 修改的文件（路径、内容差异） |
| `Bash` | 执行的命令（完整命令字符串） |
| `WebFetch` | 抓取的 URL（可能包含 POST 中发送的数据） |
| `Task` | Subagent 的派生（传递给子模型的 prompt） |
| `Glob` / `Grep` | 搜索模式和范围 |

### 实用审计查询

```bash
# All files read in a session
SESSION=~/.claude/projects/-your-project-/SESSION_ID.jsonl
jq 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use" and .name == "Read") | .input.file_path' "$SESSION"

# All bash commands executed
jq 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use" and .name == "Bash") | .input.command' "$SESSION"

# All URLs fetched
jq 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use" and .name == "WebFetch") | .input.url' "$SESSION"

# Count tool usage by type
jq -r 'select(.type == "assistant") | .message.content[]? | select(.type == "tool_use") | .name' "$SESSION" | sort | uniq -c | sort -rn
```

### 需要关注的敏感模式

以下工具调用模式值得在自动化审计中标记出来：

| 模式 | 风险 | 检测方式 |
|---------|------|-----------|
| 对 `.env`、`*.pem`、`id_rsa` 执行 `Read` | 凭据访问 | `jq '... | select(.input.file_path | test("\\.(env|pem|key)$"))'` |
| 包含 `rm -rf`、`git push --force` 的 `Bash` | 破坏性操作 | `jq '... | select(.input.command | test("rm -rf\|force-push"))'` |
| 对外部 URL 执行 `WebFetch` | 数据外泄风险 | `jq '... | select(.name == "WebFetch") | .input.url'` |
| 对项目根目录之外的文件执行 `Write` | 范围蔓延 | 将路径与工作目录进行核对 |

> **安全背景**：Claude Code 以你的用户权限对文件系统进行读写操作。JSONL 审计跟踪是你对所发生事情的记录。对于团队而言，可考虑将这些日志同步到不可变存储中。

---

## 外部监控工具

除了上文基于 hooks 的方法之外，社区还构建了一些专用工具。以下是截至 2026 年初的事实性快照。

| 工具 | 类型 | 它做什么 | 安装 |
|------|------|-------------|---------|
| **ccusage** | CLI / TUI | 基于 JSONL 的成本追踪 —— 价格数据的事实标准参考。约 10K GitHub stars。 | `npm i -g ccusage` |
| **claude-code-otel** | OpenTelemetry 导出器 | 向任意 OTEL collector 发送 span。与 Prometheus + Grafana 仪表盘集成。面向企业。 | `npm i -g claude-code-otel` |
| **Akto** | SaaS / 自托管 | API 安全护栏 + 审计跟踪。在 API 层拦截，标记策略违规。 | [akto.io](https://akto.io) |
| **MLflow Tracing** | CLI + SDK | 精确的 token 计数、工具 span、LLM-as-judge 评估。CLI 模式：无需任何 Python。最适合 ML/MLOps 团队。 | `pip install mlflow` → [见下方章节](#mlflow-tracing) |
| **ccboard** | TUI + Web | 用于会话、成本、统计数据的统一仪表盘。活动/审计标签页开发中。 | `cargo install ccboard` |
| **claude-crusts** | CLI | 一条命令的上下文污染扫描器：标记过时文件、超大记忆和冗余规则加载。在运行会话之前发现是什么在膨胀你的上下文。 | [github.com/Abinesh-L/claude-crusts](https://github.com/Abinesh-L/claude-crusts) |

### 决策指南

```
Want cost numbers fast?          → ccusage (CLI, 0 config)
Need enterprise audit trail?     → claude-code-otel + Grafana or Akto
Already using MLflow for ML?     → MLflow tracing integration (see below)
Need agent regression detection? → MLflow tracing + LLM-as-judge
Want a persistent TUI/Web UI?    → ccboard
Context pollution audit?         → claude-crusts (1-command scan)
```

### ccusage

```bash
npm i -g ccusage
ccusage          # Today's usage
ccusage --days 7 # Last 7 days
```

直接读取 `~/.claude/projects/**/*.jsonl`。无需 API 密钥，不向外部发送任何数据。来源：[github.com/ryoppippi/ccusage](https://github.com/ryoppippi/ccusage)。

### claude-code-otel

将 Claude Code 活动导出为 OpenTelemetry span：

```bash
npm i -g claude-code-otel
claude-code-otel --collector http://localhost:4318
```

Span 包含工具名称、持续时间、token 计数。可接入任何兼容 OTEL 的后端（Jaeger、Tempo、Datadog）。来源：[github.com/badger-99/claude-code-otel](https://github.com/badger-99/claude-code-otel)。

### ccboard

```bash
cargo install ccboard
ccboard              # Launch TUI
ccboard --web        # Launch Web UI (localhost:3000)
```

来源：[github.com/FlorianBruniaux/ccboard](https://github.com/FlorianBruniaux/ccboard)。一个涵盖文件访问、bash 命令和网络调用的活动标签页正在规划中（见 `docs/resource-evaluations/ccboard-activity-module-plan.md`）。

### MLflow Tracing

**何时使用**：已经身处 MLflow/MLOps 生态的团队，或任何需要精确 token 计数 + 基于 LLM 的质量评估的人。对于想快速得到成本数字的独立开发者并不合适（请改用 ccusage）。

**它与其他工具的不同之处**：MLflow 在 API 层拦截，而不是事后从 JSONL 中读取。它捕获**精确的** token 计数（相比之下，基于 hook 的估算有约 15-25% 的偏差），并支持 **LLM-as-judge** 回归检测 —— 不只是"发生了什么"，而是"它好不好？"。

#### 设置：CLI 模式（无需 Python）

可与交互式 `claude` 会话配合使用。挂接到 `.claude/settings.json`：

```bash
pip install "mlflow[genai]>=3.4"

# Enable tracing in current project directory
mlflow autolog claude

# With custom backend (recommended for persistence)
mlflow autolog claude -u sqlite:///mlflow.db

# With named experiment
mlflow autolog claude -n "my-project"

# Check status / disable
mlflow autolog claude --status
mlflow autolog claude --disable
```

启动 UI 以检查 trace：

```bash
mlflow server  # → http://localhost:5000
```

**自动捕获的内容**：用户 prompt、助手响应、工具调用（名称 + 输入 + 输出）、token 计数（精确）、每次调用的延迟、会话元数据。

#### 设置：SDK 模式（Python agents）

```python
import mlflow
mlflow.anthropic.autolog()         # one line, before anything else
mlflow.set_experiment("my-agent")

# Use ClaudeSDKClient normally — all interactions are traced
# ⚠️ Only ClaudeSDKClient is supported. Direct API calls are not traced.
from anthropic import claude_agent_sdk
async with ClaudeSDKClient(options=AGENT_OPTIONS) as client:
    await client.query(query)
```

依赖：`mlflow>=3.5` + `claude-agent-sdk>=0.1.0`。

#### MCP server：双向集成

Claude Code 可以直接查询它自己的 trace。添加到 `.claude/settings.json`：

```json
{
  "mcpServers": {
    "mlflow-mcp": {
      "command": "uv",
      "args": ["run", "--with", "mlflow[mcp]>=3.5.1", "mlflow", "mcp", "run"],
      "env": { "MLFLOW_TRACKING_URI": "<your-tracking-uri>" }
    }
  }
}
```

配置完成后，你可以问 Claude Code：*"找出所有 backend-architect agent 使用了超过 20 次工具调用的会话"* —— 它会直接查询 MLflow，无需复制粘贴 ID。

#### LLM-as-judge：agent 回归检测

这是本节所有其他工具都缺失的关键能力。在修改某个 agent 的指令之后，衡量质量是提升了还是下降了：

```python
from mlflow.genai.scorers import scorer, ConversationCompleteness, RelevanceToQuery
from mlflow.entities.model_registry import Feedback

@scorer
def tool_efficiency(trace) -> int:
    """Count tool calls — lower is better for well-scoped tasks."""
    return len(trace.search_spans(span_type="TOOL"))

@scorer
def permission_blocks(trace) -> int:
    """Detect how often the agent was blocked by permission gates."""
    return sum(
        1 for span in trace.search_spans(span_type="TOOL")
        if span.outputs and "requires approval" in str(span.outputs).lower()
    )

# Run evaluation against recorded traces
traces = mlflow.search_traces(experiment_ids=["<id>"], max_results=50)
results = mlflow.genai.evaluate(
    data=traces,
    scorers=[
        tool_efficiency,
        permission_blocks,
        ConversationCompleteness(),
        RelevanceToQuery(),
    ]
)
```

**内置 scorer**：`ConversationCompleteness`、`RelevanceToQuery`、`UserFrustration`、`SafetyScorer`。

**自定义 scorer**：可完全访问 trace 对象（所有 span、输入、输出、token 计数）。

#### 局限性

| 局限 | 详情 |
|------------|--------|
| **CLI 模式适用人群** | 最适合交互式会话；编程式 agent 需使用 SDK 模式 |
| **SDK 限制** | 仅支持 `ClaudeSDKClient` —— 直接的 API 调用会绕过 tracing |
| **PII 风险** | trace 会捕获完整的对话内容。若处理敏感数据，存储前请先脱敏 |
| **生产后端** | SQLite 仅限开发使用。生产环境请使用 PostgreSQL/MySQL |
| **OpenTelemetry** | MLflow 3.6+ 可导出到任何兼容 OTEL 的后端（Datadog、Grafana 等） |

---

## 为 Claude Code 设置代理

一个常见的问题:"我能用 Proxyman/Charles 查看 Claude Code 向 Anthropic 发送了什么吗?"

**简短回答**:不能直接做到。下面解释原因,以及哪些替代方案有效。

### 为什么系统代理不起作用

Claude Code 是一个 Node.js 进程。默认情况下,Node.js 会忽略系统级别的代理设置(`HTTP_PROXY`、`HTTPS_PROXY`)——它使用自己的 TLS 栈,不读取 macOS/Windows 的代理配置。

此外,即使流量确实经过你的代理,TLS 证书不匹配也会导致 Claude Code 失败(`CERT_UNTRUSTED`)。

### 方案 1:信任 MITM 证书(Proxyman / Charles)

强制 Node.js 信任你的代理的 CA 证书:

```bash
# Export Proxyman's CA cert (File → Export → Root Certificate)
# Then point Node.js at it:
export NODE_EXTRA_CA_CERTS="/path/to/proxyman-ca.pem"

# Start Claude Code — traffic will now route through Proxyman
claude
```

同样的方法也适用于 Charles:`Help → SSL Proxying → Export Charles Root Certificate`。

**注意事项**:

- 某些版本的 Claude Code 对 `api.anthropic.com` 使用证书固定(certificate pinning)——这种情况下可能仍然会失败
- 该方法需要有一个正在运行的 Proxyman/Charles 实例,监听所配置的端口

### 方案 2:用 ANTHROPIC_API_URL 重定向 API 流量

让 Claude Code 指向本地拦截器,而非 `api.anthropic.com`:

```bash
export ANTHROPIC_API_URL="http://localhost:8080"
claude
```

在 8080 端口运行任意 HTTP 代理/日志记录器,并将请求转发到 `https://api.anthropic.com`。这会让 Claude Code → 代理这一跳完全绕过 TLS。

**使用场景**:记录请求负载、注入请求头、在本地做限流、重放请求。

### 方案 3:mitmproxy(推荐)

[mitmproxy](https://mitmproxy.org) 是最干净的开源解决方案。它提供一个可脚本化的 HTTPS 代理,带有 Web UI 和终端界面。

```bash
# Install
brew install mitmproxy  # macOS
# or: pip install mitmproxy

# Start transparent proxy on port 8080
mitmproxy --listen-port 8080

# In a new terminal, point Claude Code at it
export NODE_EXTRA_CA_CERTS="$(python3 -c 'import mitmproxy.certs; print(mitmproxy.certs.Cert.default_ca_path())')"
export HTTPS_PROXY="http://localhost:8080"
claude
```

mitmproxy 的 Web UI(`mitmweb`)位于 `http://localhost:8081`,可以显示完整的请求/响应主体——包括 Claude Code 发送给 Anthropic 的 JSON 负载。

**你能看到的内容**:系统提示词、用户消息、工具定义、工具结果、模型参数。

### 方案 4:极简 Python 日志代理

如果想要零依赖的方案:

```python
# proxy.py — simple HTTPS logging proxy
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request, json, sys

TARGET = "https://api.anthropic.com"

class LoggingProxy(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length)
        print(json.dumps(json.loads(body), indent=2))  # Log request
        # Forward to Anthropic...

HTTPServer(("localhost", 8080), LoggingProxy).serve_forever()
```

```bash
python3 proxy.py &
export ANTHROPIC_API_URL="http://localhost:8080"
claude
```

> **隐私提示**:被代理的流量包含对话上下文中的一切——Claude 读取过的文件内容、你的代码、它遇到的任何密钥。请相应地妥善处理代理日志。

---

## 模式与最佳实践

### 1. 每周回顾

设置一个日历提醒,每周查看统计数据:

```bash
session-stats.sh --range week
```

留意以下情况:

- token 用量异常偏高的日子
- 对同一文件的重复操作(低效信号)
- 项目分布(时间花在了哪里)

### 2. 按项目追踪

使用 `CLAUDE_SESSION_ID` 按项目给会话打标签:

```bash
export CLAUDE_SESSION_ID="project-myapp-$(date +%s)"
claude
```

### 3. 团队聚合

要做全团队范围的追踪,可将日志同步到共享存储:

```bash
# Example: sync to S3 daily
aws s3 sync ~/.claude/logs/ s3://company-claude-logs/$(whoami)/
```

然后这样聚合:

```bash
# Download all team logs
aws s3 sync s3://company-claude-logs/ /tmp/team-logs/

# Combine and analyze
cat /tmp/team-logs/*/activity-$(date +%Y-%m-%d).jsonl | \
  jq -s 'group_by(.project) | map({project: .[0].project, total_tokens: [.[].tokens.total] | add})'
```

### 4. 日志轮转

日志会随时间累积。将清理操作加入 cron:

```bash
# Clean logs older than 30 days
find ~/.claude/logs -name "*.jsonl" -mtime +30 -delete
```

---

## 局限性

### 这套监控做不到什么

| 局限 | 原因 |
|------------|--------|
| **精确的 token 计数** | Claude Code CLI 不暴露 API token 指标 |
| **TTFT(首 token 时间)** | hook 在工具完成后运行,而非流式传输期间 |
| **实时流式指标** | 响应生成期间没有 hook 事件 |
| **真实的 API 成本** | token 估算是启发式的,并非来自计费 |
| **模型选择** | 日志不记录每个请求使用了哪个模型 |
| **上下文窗口使用情况** | 无法看到当前的上下文百分比 |

### 关于准确度的说明

- **token 估算**:与实际计费有约 15-25% 的偏差
- **成本估算**:作为方向性参考,而非会计依据
- **会话边界**:会话是按 ID 近似划分的,并非精确的 API 会话

### 你可以信赖的内容

- **工具使用次数**:每次工具调用的精确计数
- **文件访问模式**:哪些文件被触及
- **相对比较**:逐日/逐项目的趋势
- **操作时间**:工具的使用时刻(时间戳)

---

---

## 管理者审计清单

对于需要核实团队内 Claude Code 使用是否得当的工程经理和团队负责人,以下是实用的审计查询。

### 每周抽查(5 分钟)

```bash
# Did anything unusual happen this week?

# 1. Files accessed outside project scope
find ~/.claude/projects/ -name "*.jsonl" -newer "$(date -d '7 days ago' +%Y-%m-%d 2>/dev/null || date -v-7d +%Y-%m-%d)" 2>/dev/null | \
  xargs jq -r 'select(.type == "assistant") |
    .message.content[]? |
    select(.type == "tool_use" and .name == "Read") |
    .input.file_path' 2>/dev/null | \
  grep -v "^$(pwd)" | sort -u

# 2. Destructive commands run
find ~/.claude/projects/ -name "*.jsonl" -newer "$(date -d '7 days ago' +%Y-%m-%d 2>/dev/null || date -v-7d +%Y-%m-%d)" 2>/dev/null | \
  xargs jq -r 'select(.type == "assistant") |
    .message.content[]? |
    select(.type == "tool_use" and .name == "Bash") |
    .input.command' 2>/dev/null | \
  grep -iE "(drop|delete|truncate|rm -rf|git push --force)"
```

### 合规报告

对于受监管的环境,可生成一份 AI 活动摘要供审计人员使用:

```bash
#!/bin/bash
# Monthly compliance report for Claude Code activity

START_DATE=${1:-$(date -d '30 days ago' +%Y-%m-%d 2>/dev/null || date -v-30d +%Y-%m-%d)}
END_DATE=${2:-$(date +%Y-%m-%d)}
REPORT_FILE="ai-activity-report-${START_DATE}-${END_DATE}.json"

echo "Generating compliance report: $START_DATE to $END_DATE"

# Count sessions, tool calls, and file accesses
jq -s '{
  report_period: {start: "'"$START_DATE"'", end: "'"$END_DATE"'"},
  tool_usage: (group_by(.tool) | map({tool: .[0].tool, count: length})),
  unique_files_accessed: ([.[].file] | unique | length),
  sessions: ([.[].session_id] | unique | length)
}' ~/.claude/logs/activity-*.jsonl 2>/dev/null > "$REPORT_FILE" || \
  echo "No activity logs found. Set up session-logger.sh hook to enable."

echo "Report saved: $REPORT_FILE"
```

如需配置带自动审计追踪日志的完整治理方案,参见 [Enterprise AI Governance §6.2](../security/enterprise-governance.md#62-audit-trail-setup)。

---

## 相关资源

- [会话搜索脚本](../../examples/scripts/session-search.sh) - 快速搜索与恢复会话
- [会话日志记录 Hook](../../examples/hooks/bash/session-logger.sh)
- [统计分析脚本](../../examples/scripts/session-stats.sh)
- [企业级 AI 治理](../security/enterprise-governance.md) - 组织级治理、审计追踪、合规
- [第三方工具](../ecosystem/third-party-tools.md) - 社区 GUI、TUI 与仪表盘（ccusage、ccburn、claude-code-viewer）
- [数据隐私指南](../security/data-privacy.md) - 哪些数据会离开你的机器
- [成本优化](#cost-optimization-tips) - 降低开销的技巧
