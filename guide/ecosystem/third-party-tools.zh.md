---
title: "Third-Party Tools for Claude Code"
description: "Community tools for token tracking, context compression, session management, configuration, security scanning, project context bootstrapping, hook utilities, alternative UIs, and knowledge graph generation"
tags: [reference, integration, plugin, security]
---

# Claude Code 的第三方工具

> 用于 token 跟踪、上下文压缩、会话管理、配置、hook 实用工具以及替代 UI 的社区工具。
>
> **最后验证时间**：2026 年 5 月

## 目录

1. [关于本页](#about-this-page)
2. [Token 与成本跟踪](#token--cost-tracking)
3. [上下文压缩](#context-compression)
4. [会话管理](#session-management)
5. [配置管理](#configuration-management)
6. [安全扫描](#security-scanning)
7. [配置质量](#configuration-quality)
8. [项目上下文引导](#project-context-bootstrapping)
9. [工程标准分发](#engineering-standards-distribution)
10. [Hook 实用工具](#hook-utilities)
11. [替代 UI](#alternative-uis)
12. [多 Agent 编排](#multi-agent-orchestration)
13. [知识图谱](#knowledge-graph)
14. [插件生态](#plugin-ecosystem)
15. [Skills 可观测性](#skills-observability)
16. [已知缺口](#known-gaps)
17. [按角色的推荐](#recommendations-by-persona)

---

## 关于本页

本页收录了**扩展 Claude Code 的社区构建工具**。每个工具都已对照其公开仓库或软件包注册表进行验证。仅收录具有公开源（GitHub、npm、PyPI）的工具。

**本页 NOT 包含的内容**：
- 不是补充 Claude Code 的 AI 工具清单（参见 [AI Ecosystem](./ai-ecosystem.md)）
- 不是 DIY 监控脚本（参见 [Observability](../ops/observability.md)）
- 不是 MCP 服务器推荐（参见 [MCP Servers Ecosystem](./mcp-servers-ecosystem.md)）

---

## Token 与成本跟踪

### ccusage

Claude Code 最成熟的成本跟踪工具。解析本地会话数据，按天、月、会话或 5 小时计费窗口生成成本报告。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [npm: ccusage](https://www.npmjs.com/package/ccusage) / [ccusage.com](https://ccusage.com) |
| **安装** | `bunx ccusage`（最快）或 `npx ccusage` |
| **语言** | TypeScript (Node.js 18+) |
| **版本** | 18.x（积极维护中） |

**核心功能**：

- `ccusage daily` / `ccusage monthly` / `ccusage session` - 聚合成本报告
- `ccusage blocks --live` - 针对 5 小时计费窗口的实时监控
- `--breakdown` 标志用于按模型拆分成本（Opus/Sonnet/Haiku）
- `--since` / `--until` 日期过滤
- JSON 输出（`--json`）用于程序化访问
- 离线模式，使用缓存的定价数据
- MCP 服务器集成（`@ccusage/mcp`）
- macOS 小组件（`ccusage-widget`）和 [Raycast 扩展](https://www.raycast.com/nyatinte/ccusage)

**局限性**：依赖本地 JSONL 解析；成本估算可能与官方 Anthropic 计费不同。没有手动合并日志就无法进行团队聚合。

> **交叉引用**：主指南在 [ultimate-guide.md 第 2.4 节](../ultimate-guide.md)（成本监控）中介绍了基础的 ccusage 命令。
> 关于使用 hooks 进行 DIY 成本跟踪，参见 [Observability](../ops/observability.md)。

---

### ccburn

一个用于可视化 token 消耗速率跟踪的 Python TUI。显示相对于 Claude 计费窗口的消耗速率图表。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: JuanjoFuchs/ccburn](https://github.com/JuanjoFuchs/ccburn) / [博客文章](https://juanjofuchs.github.io/ai-development/2026/01/13/introducing-ccburn-visual-token-tracking.html) |
| **安装** | `pip install ccburn` |
| **语言** | Python 3.10+ (Rich + Plotext) |

**核心功能**：

- 显示一段时间内 token 消耗的终端图表
- 消耗速率指示器（进度正常 / 减速警告）
- 紧凑显示模式
- 针对限额的可视化预算跟踪

**局限性**：仅限 Python 生态。社区规模小于 ccusage。无 MCP 集成。

**何时选择 ccburn 而非 ccusage**：如果你偏好可视化的消耗速率图表而非表格报告，或者你的工具链基于 Python。

---

### Straude

一个用于跟踪和分享 Claude Code（以及 OpenAI Codex）使用统计的社交仪表盘。将你每日的 token 消耗和成本推送到公开排行榜，以跟踪你的连续打卡天数、每周花费和全球排名。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [npm: straude](https://www.npmjs.com/package/straude) |
| **网站** | [straude.com](https://straude.com) |
| **安装** | `npx straude@latest` |
| **语言** | TypeScript (Node.js 18+) |
| **版本** | 0.1.9（积极开发中，创建于 2026 年 2 月） |
| **维护者** | 社区 (oscar.hong2015@gmail.com) |

**核心功能**：

- `straude` — 智能同步：在一条命令中完成认证 + 推送使用数据
- `straude push --dry-run` — 预览将提交的内容，但不实际发送
- `straude push --days N` — 回填最近 N 天（最多 7 天）
- `straude status` — 连续打卡天数、每周花费、token 总量、全球排名
- 同时跟踪 Claude Code（`ccusage`）和 OpenAI Codex（`@ccusage/codex`）

**发送到 Straude 服务器的内容**：

每天：以美元计的成本、token 计数（输入/输出/缓存创建/缓存读取）、使用的模型名称（例如 `claude-sonnet-4-6`）、按模型拆分的成本。此外还有：原始数据的 SHA256 哈希、一个随机设备 UUID 以及你的机器主机名。

你的源代码、API 密钥和对话内容**不会**被访问或传输。

**安全注意事项**：

- 认证 token 存储在 `~/.straude/config.json` 中，权限为 `0600`（仅所有者可访问）
- 项目非常年轻（创建于 2026-02-18，快速迭代）——没有公开的安全审计
- 机器主机名以 `device_name` 形式发送
- 截至 2026 年 3 月没有发布隐私政策
- 在首次推送之前，使用 `--dry-run` 验证将提交的内容

**何时选择 Straude 而非 ccusage/ccburn**：

Straude 是此列表中唯一**社交**性质的工具——它会将你的统计数据上传到一个共享平台。如果你想要排行榜、连续打卡跟踪，或者想将你的使用情况与其他开发者作对比，Straude 独一无二。如果你只想要本地的成本可见性，ccusage 或 ccburn 更合适，且不涉及任何数据共享。

> **安全提醒**：在使用 `npx` 运行任何社区 CLI 工具之前，请审查其 npm 页面和源代码以发现可疑迹象。对于 Straude，其编译源码可读，且与其声明的用途一致。完整分析参见[资源评估](../../docs/resource-evaluations/straude-evaluation.md)。

---

### RTK (Rust Token Killer)

一个 CLI 代理，**在**命令输出到达 Claude 的上下文**之前**对其进行过滤。446 stars，38 forks，在 r/ClaudeAI 上获得 700+ 赞。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: rtk-ai/rtk](https://github.com/rtk-ai/rtk) |
| **网站** | [rtk-ai.app](https://www.rtk-ai.app/) |
| **安装** | `brew install rtk-ai/tap/rtk` 或 `cargo install rtk` |
| **语言** | Rust（独立二进制文件） |
| **版本** | v0.28.0 |

**核心功能**：

- `rtk git log`（减少 92%）、`rtk git status`（减少 76%）、`rtk git diff`（减少 56%）
- `rtk vitest run`、`rtk prisma`、`rtk pnpm`（减少 70-90%）
- `rtk python pytest`、`rtk mypy`、`rtk go test`（多语言支持）
- `rtk cargo test/build/clippy/nextest`（Rust 工具链）
- `rtk aws`、`rtk psql`、`rtk docker compose`、`rtk gt`（Graphite CLI）
- `rtk wc` - 紧凑的单词/行/字节计数
- `rtk init --global` - hook 优先安装，自动修补 settings.json
- `rtk gain` / `rtk gain -p` - token 节省分析（全局 + 按项目）
- **TOML Filter DSL**：无需编写 Rust 即可为任意命令添加自定义输出过滤器——`.rtk/filters.toml`（项目级）或 `~/.config/rtk/filters.toml`（全局级），内置 33+ 个过滤器
- `rtk rewrite` - hook 命令映射的单一可信来源（v0.25.0+，升级后需运行 `rtk init --global`）
- `exclude_commands` 配置项用于将特定命令排除在自动重写之外

**何时选择 RTK 而非 ccusage/ccburn**：

- RTK **减少** token 消耗（预处理）
- ccusage/ccburn **监控** token 消耗（后处理）
- 两者搭配使用以获得最大效率

**局限性**：不适用于交互式命令或极小的输出（<100 字符）。

> **交叉引用**：完整文档参见 [ultimate-guide.md 第 9 节](#command-output-optimization-with-rtk)

---

### Claude Code Usage Monitor

具有消耗速率预测和会话级警告的实时使用监控工具。截至 2026 年 5 月，它是 Claude Code 专用监控工具中 star 数最高的，约 7,955 stars。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: Maciek-roboblog/Claude-Code-Usage-Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor) |
| **安装** | `npx ccusage@latest`（CLI）或 Web UI（参见 GitHub） |
| **Stars** | ~7,955（2026 年 5 月） |

**核心功能**：

- 在 5 小时会话计费窗口内跟踪 token 消耗、消息数量和成本
- 显示当前消耗速率，并预测何时将达到会话限额
- 在达到限额之前而非之后显示警告
- 不受计费模式影响：解析磁盘上的本地会话文件，而非拦截 API 流量，因此同等覆盖 API 密钥计费和 Claude Max/Pro 订阅

**何时选择它而非 ccusage**：如果你主要想要实时警告和消耗速率预测，而非历史报告和聚合分析。两者读取相同的本地会话文件；区别在于界面和侧重点。

---

### claude-spend

针对 Claude Code 会话的一次性花费检查。是无需搭建完整监控仪表盘即可偶尔查看成本的最简单入口。

| 属性 | 详情 |
|-----------|---------|
| **安装** | `npx claude-spend` |

**核心功能**：

- 单条命令：无需配置
- 读取本地 Claude Code 会话文件（与 ccusage 相同的来源）
- 显示每次对话和每个模型的 token 消耗

**何时使用**：在不投入持久监控设置的情况下进行临时成本检查。对于周期性跟踪，ccusage 提供更多深度。

---

### cc-statistics

跨 agent 统计仪表盘，在单一视图中聚合多个 AI 编码工具的成本和 token 数据。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: androidZzT/cc-statistics](https://github.com/androidZzT/cc-statistics) |
| **Stars** | ~87（2026 年 5 月） |

**核心功能**：

- 在一个仪表盘中涵盖 Claude Code、Gemini CLI、OpenAI Codex 和 Cursor
- 跨 agent 的成本、token 计数和效率指标
- 适用于运行多个 AI 工具并希望获得统一视图的团队

**何时使用**：如果你的工作流涉及不止一个 AI 编码助手，并且你想在它们之间比较成本和使用情况。

---

### claude-context-optimizer

一个 Claude Code 插件，专注于揭示上下文预算实际花在了哪里，而不仅仅是报告总花费。

| 属性 | 详情 |
|-----------|---------|
| **Stars** | ~48（2026 年 5 月） |

**核心功能**：

- 上下文热力图：可视化哪些文件和指令消耗了最多 token
- 浪费上下文检测：标记那些很少影响模型输出的指令
- Git 感知分析：将文件上下文消耗与编辑频率交叉引用，以识别高成本、低编辑的文件
- ROI 报告和预算警报

**何时使用**：当你遇到上下文效率问题（上下文增长过快、遵循度下降）并需要找出具体来源，而非仅仅了解总体大小时。

---

### 关于第 4 层计费盲区的说明

API 级网关（Helicone、Portkey、Langfuse、Bifrost、Compresr）拦截 HTTP 调用并在 API 层测量 token 使用量。这对于直接调用 Anthropic API 的应用程序效果良好。但它不适用于 Claude Code Max 或 Pro 订阅，因为 Claude Code 使用订阅凭据而非 API 密钥直接连接到 Anthropic 服务器。不存在可供网关拦截的 HTTP 层。

上述所有四个工具（Claude Code Usage Monitor、claude-spend、cc-statistics、claude-context-optimizer）都通过解析 Claude Code 写入磁盘的本地会话文件来工作。这种方式与计费模式无关：它在 API 密钥计费和 Max/Pro 订阅上同等有效。如果你使用 Max 订阅且你的网关显示 Claude Code 流量为零，那是预期行为，而非配置错误。

---

## 上下文压缩

通过压缩、惰性加载或智能过滤来减少进入 LLM 上下文的 token 的工具——是对上述追踪工具的补充。

### lean-ctx

一个用 Rust 编写的本地优先（local-first）上下文压缩 CLI 和 MCP 服务器。全局安装一次后即可在每个 Claude Code 项目中激活，无需逐项目配置。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: yvgude/lean-ctx](https://github.com/yvgude/lean-ctx) |
| **安装** | `curl -fsSL https://raw.githubusercontent.com/yvgude/lean-ctx/main/skills/lean-ctx/scripts/install.sh \| bash && lean-ctx setup` |
| **语言** | Rust |
| **Stars** | ~1 366 |
| **版本** | v3.6.3 |

**工作原理**

lean-ctx 注册为全局 MCP 服务器（`~/.claude.json`），并在 `~/.claude/settings.json` 中安装三个会在每次工具调用时触发的 hooks：

- `PreToolUse hook redirect` — 拦截原生 Read 调用，并将其路由到 `ctx_read`（AST 解析 + 文件缓存）
- `PreToolUse hook rewrite` — 将 Bash 调用经由 `ctx_shell` 路由（基于模式的 shell 压缩）
- `PostToolUse / SessionEnd hook observe` — 向 CCP 跨会话记忆提供数据

**4 个压缩维度**

- **带 AST 解析的文件读取**：tree-sitter 解析 TypeScript、Python、Rust 以及其他 15 种语言。`signatures` 模式仅返回类型和函数签名（不含函数体）。`map` 模式返回导出项和依赖关系。一个 2364 行的 `schema.prisma` 可压缩至 ~200 tokens。未变更的文件在重新读取时以 ~13 tokens 从缓存提供。
- **Shell 输出**：60 多个针对 git、cargo、npm、docker 和 kubectl 的压缩模式。`git log -10 --stat` 被压缩为 10 行 commit 信息加一行汇总。
- **跨会话记忆（CCP — Context Continuity Protocol）**：在退出时存储 ~400 tokens 的会话摘要。下一个会话会加载它，而不是冷读取此前 50,000+ tokens 的上下文。
- **代码库图谱**：基于 SQLite 的依赖图谱，由跨 18 种语言的 tree-sitter 导入/导出关系构建。`ctx_overview` 利用它按导入中心度（import centrality）为文件评分，并优先呈现连接最紧密的模块。

**实测基准（TypeScript/T3 monorepo，2455 个文件）**

| 指标 | 数值 |
|--------|-------|
| 整体压缩率 | 57.8% |
| ctx_read 节省率 | 86% |
| ctx_search 节省率 | 72% |
| 单日节省的 tokens | 1.3M |
| signatures 模式下的 schema.prisma 2364 行 | ~200 tokens (99%) |
| 文件重新读取（缓存命中） | 13 tokens |

在以 Markdown 为主的仓库上结果较低——AST 解析器在文档文件中能找到的可压缩结构比 TypeScript 或 Rust 源码中少。

**RTK 对比 lean-ctx：互补的层次**

两个工具都能减少 token 消耗，但作用于流水线中的不同环节，且不会冲突：

| 层次 | 工具 | 压缩对象 |
|-------|------|--------------------|
| CLI 输出（shell hook） | RTK | git、cargo、npm、tsc 的输出文本 |
| 文件读取（MCP redirect） | lean-ctx | 经 AST + 缓存处理的文件内容 |
| 跨会话记忆 | lean-ctx | 经 CCP 处理的会话摘要 |

RTK 对 shell 输出的压缩更激进（节省 60-90%）。lean-ctx 的节省几乎全部来自文件读取（在实测会话中占其总节省量的 86%）。两者应配合使用。

**监控**

```bash
lean-ctx gain           # dashboard: tokens saved, USD, top commands
lean-ctx gain --daily   # day-by-day breakdown
lean-ctx cep            # efficiency score /100 (compression, cache hit rate, consistency)
lean-ctx dashboard      # web UI at localhost:3333
```

一个全局的 `/lean-ctx-audit` slash command（`~/.claude/commands/lean-ctx-audit.md`）可在任意会话内运行完整审计。完整的工具对比和设置指南见 [context-engineering.md §12](../core/context-engineering.md#12-token-compression-tools)。

**何时采用 lean-ctx**

在 TypeScript、Rust 或 Python 项目中价值最高——在这些项目中，大文件会在一个会话内被反复读取、会话在任务完成前就已填满上下文，或跨会话记忆很重要。在大多数文件为 Markdown 的文档仓库中影响较小。

> **注意**：lean-ctx 发布频繁。升级后请运行 `lean-ctx setup` 以刷新 hook 和 MCP 注册。如果只需要 shell 输出过滤，RTK 是更简单的起点。

---

### mcp2cli

一个通用的 CLI 桥接器，可将任意 MCP 服务器、OpenAPI 规范或 GraphQL 端点转换为 shell 命令——无需将工具 schema 注入 LLM 上下文。关键洞见在于：大多数 MCP 客户端会在每一轮都将所有已注册工具的完整 schema 推入上下文，无论 agent 是否需要。mcp2cli 用惰性加载（lazy loading）取而代之。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: knowsuchagency/mcp2cli](https://github.com/knowsuchagency/mcp2cli) |
| **安装** | `uvx mcp2cli --help`（免安装）或 `uv tool install mcp2cli` |
| **语言** | Python |
| **Stars** | ~1 900 |
| **状态** | 活跃（Show HN Best of March 2026） |

**惰性加载的工作方式**：

agent 不再注入完整的工具 schema（一个 43 工具的 GitHub MCP 服务器约 44 000 tokens），而是：

1. 调用 `mcp2cli --mcp <url> --list` → 每个工具收到 ~16 tokens（名称 + 简短描述）
2. 调用 `mcp2cli --mcp <url> <tool-name> --help` → 收到 ~120 tokens（完整 schema，单个工具）
3. 用正确的参数执行该工具

除非明确请求，完整 schema 永远不会进入 LLM 上下文。

**基准测试**（由 Firecrawl、Scalekit、CircleCI 独立复现）：

- GitHub MCP 服务器（43 工具），简单任务：44 026 tokens（MCP 原生）对比 1 365 tokens（gh CLI / mcp2cli 模式）——减少 32 倍
- 同样任务的失败率：MCP 原生 28%，CLI 模式 0%（上下文溢出 = 步骤遗漏）
- 120 工具，25 轮：MCP 原生在任何实际工作开始前就注入了 ~362 000 tokens 的 schema

**关键特性**：

- **多源**：MCP（HTTP/SSE/stdio）、OpenAPI 规范、GraphQL 集于一个二进制文件
- **认证**：交互式使用采用带 PKCE 的 OAuth 2.1，CI/CD 流水线采用 client credentials，token 刷新带缓存
- **守护进程 + 连接池**：MCP 连接冷启动需要 2-5 秒。守护进程将其保持热态以实现毫秒级延迟的复用。
- **`--toon` 格式**：高 token 效率的输出编码，相比纯 JSON 可削减 40-60% 的响应 tokens
- **语义化退出码**：`validation_error`、`auth_failure`、`tool_error`、`connection_error`——shell 脚本无需文本解析即可分支处理

```bash
# No-install test
uvx mcp2cli --mcp https://mcp.example.com/sse --list

# Execute a tool
mcp2cli --mcp https://mcp.example.com/sse search --query "test"

# Local stdio server
mcp2cli --mcp-stdio "npx @modelcontextprotocol/server-filesystem /tmp" --list

# OpenAPI spec
mcp2cli --spec ./openapi.json --base-url https://api.example.com list-pets

# Reusable config (baked alias)
mcp2cli bake create petstore --spec URL && mcp2cli @petstore --list
```

**何时使用 mcp2cli**：

- 你使用工具众多（10+）的 MCP 服务器，并发现上下文在任何实际工作开始前就被 schema 填满
- 你想从终端调试或测试 MCP 服务器，而不必搭建一个完整的客户端
- 你的 CI/CD 流水线以编程方式消费 MCP 工具

**何时不该使用它**：

- 需要逐用户 OAuth 和审计日志的企业级多租户场景——原生 MCP 网关在此处理得更好
- 使用知名原生 CLI（gh、git、kubectl）的 agent：模型从训练数据中已知道它们的接口，无需桥接
- 每个服务器少于 ~10 个工具：收益真实存在，但并不紧迫

> **命名警示**：GitHub 上至少有四个互不相关的项目共用 "mcp2cli" 这个名字（Python、Go、Bun 等）。本用例的参考实现是 [knowsuchagency/mcp2cli](https://github.com/knowsuchagency/mcp2cli)。安装前请核实作者。

---

## 会话管理

### claude-code-viewer

一个基于 Web 的 UI，用于浏览和阅读 Claude Code 对话历史（JSONL 文件）。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: d-kimuson/claude-code-viewer](https://github.com/d-kimuson/claude-code-viewer) / [npm: @kimuson/claude-code-viewer](https://www.npmjs.com/package/@kimuson/claude-code-viewer) |
| **安装** | `npx @kimuson/claude-code-viewer` 或 `npm install -g @kimuson/claude-code-viewer` |
| **语言** | TypeScript（Node.js 18+） |
| **版本** | 0.5.x |

**关键特性**：

- 带会话计数和元数据的项目浏览器
- 带语法高亮的完整对话展示
- 内联显示工具使用结果
- 通过 Server-Sent Events 实时更新（文件变更时自动刷新）
- 响应式设计（桌面 + 移动端）

**局限**：只读（无法编辑或恢复会话）。无成本数据。需要已有的 `~/.claude/projects/` 历史记录。

> **交叉引用**：关于从 CLI 进行会话搜索，参见 [Observability](../ops/observability.md) 中的 [session-search.sh](../../examples/scripts/session-search.sh)。

---

### agenttrace

一个本地 TUI 和报告生成器，用于检查 AI 编码 agent 的会话历史。它读取 Claude Code 的 JSONL 日志，同时也支持 Codex CLI、Gemini CLI、Qwen Code、Cline、Aider、Cursor 导出、OpenCode/OpenClaw、Hermes Agent、Pi、Oh My Pi、Kimi CLI、Copilot 风格的日志，以及通用的 JSON/JSONL traces。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: luoyuctl/agenttrace](https://github.com/luoyuctl/agenttrace) |
| **安装** | `brew install luoyuctl/tap/agenttrace` 或 `go install github.com/luoyuctl/agenttrace/cmd/agenttrace@latest` |
| **语言** | Go |
| **许可证** | MIT |

**关键特性**：

- 用于历史会话的本地 dashboard，可按成本、tokens、耗时和健康度排序
- 针对工具失败、延迟间隙、重试循环、超大参数、异常和 diff 的逐会话诊断
- 用于 CI 产物或团队评审的 JSON、Markdown 和 HTML 概览输出
- 针对平均健康度、关键会话和工具失败率的 CI 门禁
- 演示模式（`agenttrace --demo`），可在连接本地日志前评估其 UI

**何时选择 agenttrace 而非 claude-code-viewer**：

- 你需要成本、延迟、健康度和失败诊断，而不仅仅是对话浏览
- 你使用多个编码 agent，并希望对它们的会话日志有一个统一的本地视图
- 你想要从会话历史生成可导出的报告或 CI 质量门禁

**局限**：它是一个本地检查/报告工具，而非实时协作 UI。成本估算取决于每种 agent 日志格式中可用的模型定价数据和 token 字段。

---

### Entire CLI

一个 agent 原生平台，用于与 Git 集成的会话捕获，具备可回溯检查点（checkpoint）和治理层。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: entireio/cli](https://github.com/entireio/cli) / [entire.io](https://entire.io) |
| **安装** | 参见 GitHub（平台于 2026 年 2 月上线，早期访问） |
| **语言** | TypeScript |
| **创立** | 2026 年 2 月由 Thomas Dohmke（前 GitHub CEO）创立，融资 6000 万美元 |

**关键特性：**

- **会话捕获**：自动记录 AI agent 会话（Claude Code、Gemini CLI）及其完整上下文
- **可回溯检查点**：恢复到任意会话状态，包含 prompts + 推理过程 + 文件变更
- **治理层**：权限系统、人工审批门禁、用于合规的审计追踪
- **Agent 交接**：在切换 agent 时保留上下文（Claude → Gemini）
- **Git 集成**：将检查点存储在独立的 `entire/checkpoints/v1` 分支上（不污染历史）
- **多 agent 支持**：同时支持多个 AI agent 并共享上下文

**使用场景：**

| 场景 | 为何选择 Entire CLI |
|----------|---------------|
| **合规（SOC2、HIPAA）** | 完整审计追踪：prompts → 推理 → 输出 |
| **多 agent 工作流** | 跨 agent 切换时保留上下文 |
| **调试 AI 决策** | 回溯到检查点，检查推理过程 |
| **治理** | 在生产变更前设置审批门禁 |
| **团队交接** | 带完整上下文恢复会话 |

**对比 claude-code-viewer：**

| 特性 | claude-code-viewer | Entire CLI |
|---------|-------------------|-----------|
| **用途** | 只读历史查看 | 主动会话管理 + 回放 |
| **回放** | 否 | 是（回溯到检查点） |
| **上下文** | 仅对话 | prompts + 推理 + 文件状态 |
| **治理** | 否 | 是（审批门禁、权限） |
| **多 agent** | 否 | 是（agent 交接） |
| **开销** | 无 | ~5-10% 存储 |

**何时选择 Entire 而非 claude-code-viewer：**

- ✅ 需要会话回放/回溯功能
- ✅ 企业级合规需求（审计追踪）
- ✅ 多 agent 工作流（Claude + Gemini）
- ✅ 治理门禁（部署前审批）
- ❌ 只想浏览历史 → 使用 claude-code-viewer（更轻量）

**局限：**

- 非常新（2026 年 2 月 10-12 日上线）——生产反馈有限
- 面向企业（对独立开发者可能偏复杂）
- 存储开销（会话数据约占项目大小的 5-10%）
- 仅支持 macOS/Linux（Windows 需经由 WSL）
- 早期阶段（v1.x）——预期会有 API 变更

**相对于常见现有方案的增量价值：**

| 需求 | 典型现有方案 | Entire 新增的 |
|------|----------------------|-----------------|
| 工具调用日志 | 本地 JSONL（7 天轮转） | 推理 + 归属占比 %，Git 永久保存 |
| 人/AI 归属 | 无 | 按文件给出 %，逐行标注，按模型区分 |
| Agent 交接 | 手动复制上下文 | 上下文检查点自动传递给下一个 agent |
| 开发者间交接 | Git commits/PRs | `entire/checkpoints/v1` 上的可读共享检查点 |
| 会话持久化 | 仅本地、临时性 | Git 原生、永久、可共享 |
| 治理 | 自定义 pre-commit hooks | 基于策略的审批门禁 + 可配置的审计导出 |

**评估（团队推广前建议先做 2 小时试点）：**

```bash
entire enable  # Install on throwaway branch

# After 2-3 normal sessions:
du -sh .git/refs/heads/entire/   # Storage per session → flag if > 10 MB
time git push                     # Push overhead → flag if > 5s
ls .git/hooks/                    # Verify no conflict with existing hooks
```

停止标准：检查点 > 10 MB/会话、push 开销 > 5 秒，或 hook 冲突。

> **交叉引用**：带示例的完整 Entire 工作流见 [AI Traceability Guide](../ops/ai-traceability.md#51-entire-cli)。关于合规使用场景，参见 [Security Hardening](../security/security-hardening.md)。

---

## 配置管理

### claude-code-config

一个用于管理 `~/.claude.json` 配置的 TUI，专注于 MCP server 管理。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: joeyism/claude-code-config](https://github.com/joeyism/claude-code-config) |
| **安装** | `pip install claude-code-config` |
| **语言** | Python (Textual TUI) |

**核心特性**：

- 可视化 MCP server 管理（添加、编辑、删除）
- 带校验的配置文件编辑
- 针对 `~/.claude.json` 结构的 TUI 导航

**局限性**：仅限于 `~/.claude.json` 范围。不管理 `.claude/settings.json`、hooks 或 slash commands。

---

### AIBlueprint

一个 CLI，用于搭建预配置的 Claude Code 环境，包含 hooks、commands、statusline 和工作流自动化。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: Melvynx/aiblueprint](https://github.com/Melvynx/aiblueprint) |
| **安装** | `npx aiblueprint-cli` |
| **语言** | TypeScript |

**核心特性**：

- 预构建的安全 hooks
- 自定义 command 模板
- statusline 配置
- 工作流自动化预设

**局限性**：配置选择带有较强的主观倾向。部分功能需要付费层级。不读取现有配置（从零开始搭建）。

> **交叉引用**：关于手动配置 Claude Code，参见 [ultimate-guide.md 第 4 节](../ultimate-guide.md)（CLAUDE.md、settings、hooks、commands）。

---

### Claude Code Organizer

一个 Web 仪表盘和 MCP server，用于在完整的作用域层级（Global > Workspace > Project）中组织 Claude Code 配置。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: mcpware/claude-code-organizer](https://github.com/mcpware/claude-code-organizer) |
| **安装** | `npx @mcpware/claude-code-organizer` |
| **语言** | JavaScript（原生，零依赖） |
| **许可证** | MIT |

**核心特性**：

- 扫描 `~/.claude/` 中的 11 个类别：memories、skills、MCP servers、commands、agents、rules、configs、hooks、plugins、plans、sessions
- 可视化作用域继承树，展示 Claude 在每个目录下加载的内容
- 在作用域之间拖放条目，每个操作均可撤销
- 批量操作（多选，一次性移动或删除）
- 跨所有作用域的实时搜索和过滤
- MCP server 模式（`--mcp`），使 Claude 能够以编程方式管理自身配置

**局限性**：尚不支持对配置内容进行内联编辑。不支持 Windows。仪表盘对 memories/skills/MCP 可读写，但对 hooks/plugins/configs 锁定为只读。

---

## 安全扫描

两个互补的层次：一类工具审计你的 Claude Code 配置，查找配置错误、hook 注入和 MCP 风险；另一类是 agent 驱动的扫描器，在应用代码本身中发现逻辑层面的漏洞。

### AgentShield

一个安全扫描器，按 0–100 分制（A–F）对你的 `.claude/` 目录进行评级，涵盖 5 个类别中的 102 条规则。在 Claude Code Hackathon（Cerebral Valley x Anthropic，2026 年 2 月）上构建。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: affaan-m/agentshield](https://github.com/affaan-m/agentshield) |
| **安装** | `npx ecc-agentshield scan`（免安装）或 `npm install -g ecc-agentshield` |
| **语言** | TypeScript (Node.js) |
| **许可证** | MIT |
| **状态** | 早期阶段（2026 年 2 月发布）—— 规则未经独立审计 |

**核心特性**：

- **5 个扫描类别**：secrets（14 种模式：`sk-ant-`、`ghp_`、AWS、Stripe……）、permissions（通配符 `Bash(*)`、缺失 deny 列表）、hooks（34 条规则：通过 `${var}` 的命令注入、数据外泄、静默错误、反向 shell）、MCP servers（23 条规则：供应链、`npx -y`、远程传输）、agents（25 条规则：自动运行指令、隐藏 Unicode 指令、prompt 反射）
- **自动修复**：`agentshield scan --fix` —— 将硬编码的密钥替换为环境变量引用
- **多种输出格式**：终端（默认）、JSON（`--format json`）、Markdown、自包含 HTML
- **GitHub Action**：在受影响文件上发布内联注释，输出 `score` 和 `grade`，支持 `fail-on-findings` 阈值
- **Opus 对抗式分析**（`--opus --stream`）：三 agent 流水线（Attacker → Defender → Auditor），使用 Opus 4.6 进行深度威胁建模

```bash
# Scan your Claude Code config (no install required)
npx ecc-agentshield scan

# Auto-fix safe issues
agentshield scan --fix

# JSON output for CI
agentshield scan --format json

# Three-agent adversarial analysis (requires ANTHROPIC_API_KEY — incurs API cost)
agentshield scan --opus --stream
```

**GitHub Action**：

```yaml
- name: AgentShield Security Scan
  uses: affaan-m/agentshield@v1
  with:
    path: "."
    min-severity: "medium"
    fail-on-findings: "true"
```

**`runtimeConfidence` 上下文**：发现项按来源加权 —— `active-runtime`（完整权重）vs `template-example`（0.25 倍）vs `docs-example`（0.25 倍）—— 这样一个庞大的 MCP 模板目录就不会像数十个活跃 server 那样虚高得分。

**局限性**：
- 规则未经独立审计 —— 将评级视为有用的信号，而非合规认证
- `--opus` 模式会触发 Opus 4.6 API 调用；在 CI 中启用前请相应预算
- 项目仅有 2 个月历史 —— API 接口可能演进；在生产环境中固定到特定版本

> **另见**：[安全加固指南](../security/security-hardening.md)，了解手动 hook 和权限模式。

### DeepSec

一个由 Vercel Labs 推出的 agent 驱动漏洞扫描器，可在应用代码中发现逻辑层面的安全缺陷 —— 即基于正则的 SAST 工具会遗漏的那类问题。上面的 AgentShield 审计的是你的 Claude Code 配置，而 DeepSec 审计的是应用本身。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: vercel-labs/deepsec](https://github.com/vercel-labs/deepsec) |
| **安装** | `npx deepsec init`（在仓库根目录引导生成一个 `.deepsec/` 目录） |
| **语言** | TypeScript |
| **许可证** | Apache 2.0 |
| **状态** | Vercel Labs —— 实验性，尚未达到生产就绪 |

**工作原理**：DeepSec 运行一个 5 步流水线。首先用一次快速正则扫描识别敏感区域（认证流程、加密调用、用户输入）。然后 AI agent 追踪每个候选文件中的数据流并产出发现项。第二轮 agent 重新校验这些发现项，并查阅 git 历史以过滤掉已修补的问题。最终输出为结构化的 Markdown 或 JSON，可直接粘贴到工单中。

**所用 AI 模型**：Claude Opus 4 配合 extended thinking（默认）以及 GPT-5.5，通过你现有的 Anthropic 或 OpenAI 订阅使用。生产环境扫描推荐使用 Vercel AI Gateway。

**误报率**：经过重新校验步骤后约为 10–20%。

```bash
# Initialize at repo root
npx deepsec init
cd .deepsec && pnpm install

# Run the full pipeline
pnpm deepsec scan       # fast regex pass
pnpm deepsec process    # AI agent investigation (slow, costs tokens)
pnpm deepsec triage     # P0/P1/P2 classification
pnpm deepsec revalidate # reduce false positives
pnpm deepsec export --format md-dir --out ./findings

# PR mode: scan only changed files (much cheaper)
pnpm deepsec process --diff

# Distributed mode for large monorepos (Vercel Sandboxes)
pnpm deepsec sandbox process --sandboxes 10 --concurrency 4
```

**何时使用**：DeepSec 能发现认证条件中的边界情况以及基于模式的工具无法呈现的微妙数据流问题。它非常适合对关键服务进行周期性的深度审计，或作为安全敏感 PR 上的 `--diff` 门禁 —— 而不适合作为逐次提交的扫描器。

**成本警告**：对一个 5 万行代码库进行完整扫描可能消耗 10–50 美元的 Claude Opus token。大型 monorepo 可能高达数千美元。日常使用请运行 `--diff` 模式；将完整扫描保留给有针对性的审计。

**配置**：创建 `.deepsec/INFO.md`（50–100 行），记录项目特定的认证模式和敏感区域。如果没有它，agent 将在缺乏上下文的情况下推理，产生更多误报。插件系统允许使用与你架构相匹配的自定义正则匹配器。

**安全态势**：DeepSec 拥有完整的 shell 访问权限 —— 应将其视为编码 agent 对待。Vercel 建议在 Sandbox microVM（Firecracker）中部署，以防 API 密钥从 worker 进程中被外泄。

> **另见**：[Vercel 博客公告](https://vercel.com/blog/introducing-deepsec-find-and-fix-vulnerabilities-in-your-code-base)，了解架构细节和真实案例。

---

## 配置质量

这类工具随时间推移对现有 AI agent 配置进行评分、审计和维护质量 —— 与从零创建配置相对。

> **背景**：CLAUDE.md 不是一次性产物。随着代码库的演进，它提供给 AI 的上下文可能会漂移：引用的路径不再存在、领域知识变得陈旧、出现了未被记录的新模式。下面的工具针对的正是这一维护层。

### Caliber

一个 CLI，可对你的 AI agent 配置质量评分（0-100），通过代码库指纹生成定制配置，并检测代码与 CLAUDE.md 之间的漂移。适用于 Claude Code、Cursor 和 Codex。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: rely-ai-org/caliber](https://github.com/rely-ai-org/caliber) |
| **安装** | `npx @rely-ai/caliber score`（免安装）或 `npm install -g @rely-ai/caliber` |
| **语言** | TypeScript (Node.js ≥20) |
| **许可证** | MIT |
| **状态** | 早期阶段（2026 年 3 月发布）—— API 可能演进 |

**核心特性**：

- **本地评分**：跨 6 个类别（Existence、Quality、Grounding、Accuracy、Freshness、Bonus）的确定性 100 分评分标准 —— 无 LLM 调用，无需 API 密钥
- **漂移检测**：基于 git —— 检测代码提交超前于配置更新的情况；缓存在树签名或 HEAD 变化时失效
- **配置生成**：代码库指纹（语言、框架、依赖）→ 通过你现有的 AI 订阅（Claude Code 席位、Cursor 席位或 API 密钥）生成 CLAUDE.md + MCP 建议
- **审查工作流**：评分 → 提议 → diff 审查 → 接受/拒绝 → 备份到 `.caliber/backups/` → `caliber undo`
- **GitHub Action**：发布带评分、等级、相对基线分支增量的 PR 评论；可选的 `fail-below` 阈值可阻止合并

```bash
# Score your current config (read-only, zero install)
npx @rely-ai/caliber score

# Generate or improve configs
npx @rely-ai/caliber init

# Detect drift after code changes
caliber refresh

# GitHub Action (fail PR if score < 75)
# uses: rely-ai-org/caliber@v1
# with: { fail-below: 75 }
```

**评分类别**：

| 类别 | 满分 | 衡量内容 |
|----------|-----|-----------------|
| Existence | 25 | CLAUDE.md 存在、skills、MCP 配置、跨平台一致性 |
| Quality | 25 | token 预算、代码块、具体度比率、无重复 |
| Grounding | 20 | 配置中引用的项目目录/文件占比 |
| Accuracy | 15 | 引用路径在磁盘上存在、自上次配置更新以来的提交数 |
| Freshness | 10 | 相对于 git 历史的配置陈旧度、无密钥 |
| Bonus | 7 | 已配置 hooks、AGENTS.md、存在习得内容 |

**相对本节其他配置工具的差异**：

| 需求 | 现有工具 | Caliber 的补充 |
|------|--------------|-------------------|
| 从零创建配置 | AIBlueprint | — |
| 审计现有配置质量 | 无 | 评分标准 + 具体的失败检查项 |
| 检测配置相对代码的漂移 | 无 | 基于 git 的漂移检测 |
| 在组织规模上分发标准 | Packmind | — |

**局限性**：早期阶段工具（2026 年 3 月，撰写时约 65 stars）。多工具支持（Claude Code + Cursor + Codex + Copilot）可能产出泛泛而足够的配置，而非深度专属于 Claude Code 的配置。评分标准未作为独立文档暴露 —— 各类别是确定性的，但不阅读源码就对用户不可见。

**安全说明**：`caliber refresh` 和 `caliber watch` 拥有对 CLAUDE.md 的写权限。与 Packmind 属同一风险等级：接受前请审查生成的输出，尤其是使用外部来源（`caliber config`）时。对待 `.caliber/` 配置文件应与对待密钥管理器一样严格。

> **交叉引用**：关于从零搭建配置，参见 [AIBlueprint](#aiblueprint)。关于在组织规模上分发和强制执行标准，参见 [Packmind](#packmind)。关于手动撰写 CLAUDE.md，参见 [ultimate-guide.md 第 3 节](#31-memory-files-claudemd)。

---

### context-evaluator

一个由 Packmind 推出的开源工具，使用 17 个专门的 AI 评估器来评估 CLAUDE.md 和 AGENTS.md 的质量。提供免安装 Web 应用、预编译二进制文件或 Bun 源码安装三种形式。

| 属性 | 详情 |
|-----------|---------|
| **网站** | [context-evaluator.ai](https://context-evaluator.ai) |
| **来源** | [GitHub: PackmindHub/context-evaluator](https://github.com/PackmindHub/context-evaluator) |
| **安装** | 在 context-evaluator.ai 免安装使用，或从 GitHub Releases 获取二进制文件 |
| **语言** | TypeScript (Bun) + React 前端 |
| **许可证** | MIT |
| **状态** | 活跃（Packmind 实验性项目，2026） |

**核心特性**：

- 17 个评估器分为 13 种错误类型（现存问题）和 4 种建议类型（来自代码库分析的缺口）：内容质量、结构/格式、命令完整性、测试指引、安全意识、矛盾指令、过时路径等等
- AGENTS.md 与 CLAUDE.md 同等对待 —— 兼容 Claude Code、Cursor、GitHub Copilot 和 Codex 格式
- 代码库指纹识别：CLOC + 文件夹分析 + 配置文件检测先行运行，因此每个评估器 prompt 都包含项目实际使用的语言、框架和关键文件夹。问题是项目特定的，而非泛泛而谈。
- **统一模式**：当所有文件合计低于 10 万 token 时，单个 agent 一并评估它们，并能检测跨文件矛盾。超过该阈值时，agent 按文件独立运行。
- **自动化修复**：从 Web UI 中选择问题，选定目标格式（Claude Code、Cursor、GitHub Copilot、Cursor），AI 会生成一个 `.patch` 文件。用 `git apply remediation.patch` 手动应用。未经审查不提交任何更改。
- 多个 AI 提供方：Claude Code（默认）、Cursor、OpenCode、GitHub Copilot、OpenAI Codex

**相对 Caliber 的差异**：

| 特性 | Caliber | context-evaluator |
|---------|---------|-------------------|
| 无需 AI 提供方 | 是（确定性） | 否（需要 AI CLI） |
| 评分标准（0-100） | 是 | 否 |
| Git 漂移检测 | 是 | 否 |
| 基于 LLM 的内容审查 | 否 | 是（17 个评估器） |
| 跨文件矛盾检测 | 否 | 是（统一模式） |
| 自动化修复（patch 文件） | 否 | 是 |
| 免安装 Web 版本 | 否 | 是（context-evaluator.ai） |

**何时选择 context-evaluator**：

- 你想要对 CLAUDE.md 的实际内容获得 LLM 评分反馈，而非结构性评分标准
- 你的配置可能存在矛盾指令、陈旧路径或缺失的框架约定，而这些是确定性评分捕捉不到的
- 你想要带可审查 diff 的自动化修复（而非就地重写）

**何时改选 Caliber**：

- 你需要用于 CI 门禁的零 LLM 评分（`fail-below` 阈值）
- 你想要随代码演进的基于 git 的漂移检测

**局限性**：需要具备 CLI 访问能力的 AI 提供方。处理耗时 1-3 分钟。无用于 CI 的确定性评分。无 git 漂移检测。

> **交叉引用**：关于确定性配置评分，参见 [Caliber](#caliber)。关于从零生成配置，参见 [AIBlueprint](#aiblueprint)。该工具源码中的运行时 Prompt 日志记录与自适应统一/并行模式模式，记录于 [Skill 设计模式](../core/skill-design-patterns.md)。

---

## 项目上下文引导（Bootstrapping）

这类工具会在 Claude Code 会话开始前编译出结构化的代码库知识，让 AI 从第一条消息起就理解路由、schema、依赖关系和高影响力文件，无需花费 token 进行文件探索。

> **背景**：Claude Code 通过调用 Glob、Grep 和 Read 来探索代码库。在大型项目上，这会在任何实际工作开始前就消耗数千个 token。下面这些工具把这种探索预先编译成一个结构化产物（或一组有针对性的 wiki 文章），Claude 在会话开始时读取一次即可。可以把它理解为"在会话打开之前先把项目加载进 RAM"。

### codesight

一个零依赖的 CLI，通过 AST 分析代码库，并为 Claude Code 及其他 AI 工具生成结构化的上下文地图。与手动文件探索相比，基础扫描可节省 7-12 倍的 token；配合有针对性的 wiki 查询，最高可达 83-131 倍（基于 3 个生产项目的自报数据）。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: Houseofmvps/codesight](https://github.com/Houseofmvps/codesight) |
| **安装** | `npx codesight`（零依赖、零配置） |
| **语言** | TypeScript —— 在项目中存在时会借用项目自带的 TS 编译器 |
| **许可证** | MIT |
| **状态** | 早期阶段（2026 年 4 月发布，撰写时约 386 个 star）—— API 可能会演进 |

**核心命令**：

```bash
# Scan current project — generates .codesight/ folder
npx codesight

# Generate wiki knowledge base (.codesight/wiki/) — targeted articles per topic
npx codesight --wiki

# Generate CLAUDE.md, .cursorrules, codex.md, AGENTS.md from project scan
npx codesight --init

# Show blast radius for a file (all files transitively affected by changing it)
npx codesight --blast src/lib/db.ts

# Start as MCP server (11 tools) — Claude calls it on demand
npx codesight --mcp

# Generate optimized config file for a specific AI tool
npx codesight --profile claude-code

# Watch mode — rescans on file changes
npx codesight --watch

# Open interactive HTML report in browser
npx codesight --open
```

**生成的内容**：

| 文件 | 内容 |
|------|---------|
| `.codesight/CODESIGHT.md` | 合并的上下文地图 —— 用一个文件提供完整的项目理解 |
| `.codesight/routes.md` | 每条 API 路由，含方法、路径、参数，以及它所触及的内容（auth、db、cache、payments） |
| `.codesight/schema.md` | 每个数据库模型，含字段、类型、主键、外键、关系 |
| `.codesight/graph.md` | 导入图 —— 哪些文件导入了什么，哪些文件改动后会破坏最多东西 |
| `.codesight/middleware.md` | Auth、限流、CORS、校验、日志、错误处理器 |
| `.codesight/config.md` | 每个环境变量（必填还是有默认值）、配置文件、关键依赖 |
| `.codesight/wiki/` | 持久化知识库：每个主题一篇文章（`auth.md`、`database.md`、`payments.md` 等） |

**检测覆盖范围**：

- 路由：自动检测 25+ 框架（Express、Hono、Fastify、NestJS、tRPC、FastAPI 等）
- Schema：10 种 ORM（Drizzle、Prisma、TypeORM、Mongoose、SQLAlchemy、ActiveRecord、Ecto、Eloquent、Entity Framework、Sequelize）
- 组件：React、Vue、Svelte、Flutter、SwiftUI
- 语言：TypeScript（完整 AST）、JavaScript、Python、Go、Ruby、Elixir、Java、Kotlin、Rust、PHP、Dart、Swift、C#（非 TS 语言使用正则回退）

**MCP 集成** —— 配置完成后，Claude 直接调用，无需运行 `npx`：

```json
{
  "mcpServers": {
    "codesight": {
      "command": "npx",
      "args": ["codesight", "--mcp"]
    }
  }
}
```

可用的 MCP 工具：`codesight_scan`、`codesight_get_wiki_index`、`codesight_get_wiki_article`、`codesight_get_routes`、`codesight_get_schema`、`codesight_get_blast_radius`、`codesight_get_hot_files`、`codesight_get_env`、`codesight_get_summary`、`codesight_lint_wiki`、`codesight_refresh`。

**wiki 如何降低 token 用量**：

| 问题 | 没有 wiki | 有 wiki |
|----------|-------------|-----------|
| "auth 是怎么工作的？" | ~12K token（读取 8+ 个文件） | ~300 token（`auth.md`） |
| "存在哪些模型？" | ~5K token（完整 CODESIGHT.md） | ~400 token（`database.md`） |
| 新会话开始 | ~5K token（完整重新加载） | ~200 token（`index.md`） |

**在什么规模下应从 CODESIGHT.md 切换到 wiki**：在中小型项目上（约 1,500 个文件以下），通过 CLAUDE.md 在会话开始时加载 `CODESIGHT.md` 是可行的。在大型项目上 —— 一个 1,700 文件的 Next.js + tRPC monorepo 会生成一份 35K token 的 CODESIGHT.md —— 加载完整文件就会适得其反。改用 `--wiki` + MCP server：Claude 针对每个问题拉取一篇有针对性的文章（~200-400 token），而不是一开始就加载整张地图。

**局限与注意事项**：

- 基准数据是在 3 个生产项目上自报的 —— 撰写时尚无独立验证
- AST 精度仅适用于 TypeScript；其他语言使用基于正则的回退
- `--init` 会自动生成一份 CLAUDE.md —— 它可能覆盖已有的文件。在已有成熟配置的项目上运行前，请先备份你的 CLAUDE.md
- 早期阶段工具（2026 年 4 月）：API 面可能在各版本间变化
- MongoDB 项目会正确报告 0 个 schema 模型（没有 SQL ORM 声明）
- 使用原始 HTTP 处理器（没有可识别框架）的 Cloudflare Workers 会报告 0 条路由 —— worker 运行时不在所支持的 25+ 框架列表内
- Next.js App Router 项目会报告 0 条路由 —— 基于文件的路由没有可供静态分析解析的显式路由声明；路由是从文件路径推断的，而非从代码模式推断
- Rust 项目产出几乎为空 —— 没有 AST 支持，正则回退只能捕获顶层模块导入（`src/main.rs` → `mod X`）；路由、结构体和业务逻辑都不可见。在 Rust 代码库上没有用处

**CI 集成**（让上下文在每次 push 时保持新鲜）：

```yaml
name: codesight
on: [push]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm install -g codesight && codesight
      - uses: actions/upload-artifact@v4
        with:
          name: codesight
          path: .codesight/
```

> **交叉引用**：关于 CLAUDE.md 的手动编写和路径作用域，参见 [ultimate-guide.md 第 3 节](../ultimate-guide.md)。关于上下文窗口管理策略，参见 [context-engineering-tools.md](./context-engineering-tools.md)。关于 MCP server 配置，参见 [mcp-servers-ecosystem.md](./mcp-servers-ecosystem.md)。

---

## 工程标准分发

这类工具解决的是组织规模的问题：让工程标准在数十个代码仓库和多个 AI 编码代理之间保持同步。

> **背景**：本指南在项目层面讲解了 CLAUDE.md 的编写（Ultimate Guide 第 3 节）。下面这些工具面向更上一层 —— 在整个工程组织范围内分发并维护这些标准。

### Packmind

一个开源的 "ContextOps" 平台（Packmind 用这个词指代把工程上下文当作有生命周期的受管产物来对待）。它把标准捕获一次，然后作为 AI 可读的上下文分发给团队所使用的每一个 AI 编码代理。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: PackmindHub/packmind](https://github.com/PackmindHub/packmind) |
| **安装** | `npx @packmind/cli init` |
| **许可证** | Apache-2.0（CLI）—— SaaS 层位于 packmind.com（定价未说明） |
| **自托管** | Docker / Kubernetes |
| **语言** | TypeScript |

**主要特性**：

- 单一 playbook → 为 Claude Code 生成 `CLAUDE.md` + slash commands + skills，为 Cursor 生成 `.cursor/rules/*.mdc`，为 Copilot 生成 `.github/copilot-instructions.md`，为通用代理生成 `AGENTS.md`
- MCP server：直接在 Claude Code 会话内创建和管理标准
- 持续学习闭环（声称）：修复 bug → 通过 Skill+MCP 捕获根因 → 提出 playbook 更新建议 → 人工验证 → 在各仓库间分发
- 通过 MCP server 从团队工具中摄取知识：GitHub PR 评论、Slack、Jira、GitLab MR、Confluence、Notion（[演示用例](https://github.com/PackmindHub/demo-use-case-skills)）

**心智模型**：把 Packmind 看作 `.claude/rules/` 模块化模式的组织级版本。`.claude/rules/*.md` 让单个项目保持一致，Packmind 则让 40 个仓库保持一致 —— 并且同步到团队使用的每一个 AI 工具，而不仅仅是 Claude Code。

**安全提示**：集中化的 CLAUDE.md 分发意味着一个被攻陷的 Packmind 仓库可以同时向每位开发者的 AI 会话传播恶意指令。请把 Packmind 配置当作敏感产物对待，施加与对待密钥管理器同等的访问控制，并在合并前仔细审查提出的 playbook 更新。

> **交叉引用**：关于项目规模的 CLAUDE.md 编写，参见 [第 3.5 节 —— 规模化的团队配置](#35-team-configuration-at-scale)。关于 Packmind MCP server，参见 [mcp-servers-ecosystem.md —— 编排](./mcp-servers-ecosystem.md#orchestration)。

---

## Hook 实用工具

这类工具用额外的逻辑、条件执行或自动化模式扩展 Claude Code 的 hook 系统。关于自行实现 hook 的示例，参见 [ultimate guide 中的 hooks 章节](../ultimate-guide.md)。

### gitdiff-watcher

一个 Stop hook 实用工具，在 Claude 交还控制权之前强制执行质量门禁。它仅在相关文件发生变更时才运行 shell 命令（构建、测试、linting），从而让 CLAUDE.md 中的质量规则变得确定可靠。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: fcamblor/gitdiff-watcher](https://github.com/fcamblor/gitdiff-watcher) |
| **安装** | `npx @fcamblor/gitdiff-watcher@0.1.0`（无需全局安装） |
| **语言** | Node.js |
| **版本** | 0.1.0 —— 开发中，API 可能变化 |
| **作者** | Florian Camblor |

**它解决的问题**：诸如"交接前测试必须通过"这样的 CLAUDE.md 规则是非确定性的。随着上下文增长，这些规则会与最近的工具输出争夺模型的注意力，从而可能被降低优先级 —— 因此即便规则写得很明确，Claude 有时仍会带着出错的代码交还控制权。Stop hook 在 LLM 上下文之外运行，使其在结构上不可能被跳过。

**工作原理**：

1. 接收一个 glob 模式（`--on`）和一个或多个 shell 命令（`--exec`）
2. 在每次 Stop 事件时，对出现在 `git diff`（已暂存 + 未暂存）中、匹配该 glob 的所有文件做 SHA-256 哈希
3. 与存储在 `.claude/gitdiff-watcher.state.local.json` 中的上一次快照进行比对
4. 若无相关变更：静默退出 0（不运行任何命令）
5. 若检测到变更：运行所有 `--exec` 命令
6. 若任一命令失败（退出码 2）：Claude 收到 stderr 并重试 —— 快照不会更新，因此下一轮会再次执行该检查
7. 完全成功时：更新快照

**示例配置**（`.claude/settings.json`）：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "npx @fcamblor/gitdiff-watcher@0.1.0 --on 'src/**/*.{ts,tsx}' --exec 'npm run build'",
            "timeout": 300,
            "statusMessage": "Checking TypeScript build..."
          },
          {
            "type": "command",
            "command": "npx @fcamblor/gitdiff-watcher@0.1.0 --on 'src/**/*.{ts,tsx}' --exec 'npm test -- --passWithNoTests'",
            "timeout": 300,
            "statusMessage": "Checking tests..."
          }
        ]
      }
    ]
  }
}
```

多个 hook 并行运行（Claude Code 为每个 hook 条目派生一个 subagent）。

**关键行为**：

- **条件触发**：仅在匹配文件变更时才触发 —— 不会在无关编辑上浪费 CI 时间
- **重试安全**：失败的运行会保留快照，因此下一次尝试仍会运行同一检查
- **并行**：单个 hook 条目内的多个 `--exec` 命令按顺序运行；若需并行执行，请使用独立的 hook 条目
- **空操作时静默**：未检测到相关变更时退出 0 且无输出

**局限**：

- v0.1.0 —— 明确标注"开发中"，CLI 选项和状态文件格式可能变化
- 使用 `git diff（已暂存 + 未暂存）` 进行文件检测 —— 未被 git 跟踪的文件对 watcher 不可见
- 重试循环：配置错误、始终失败的检查会导致 Claude 无限重试；请添加 `--exec-timeout` 并确保你的命令具有正确的退出码
- 每次 Stop hook 失败都会启动新的 Claude 轮次，消耗上下文 —— 接近 200K 上限时，反复失败会加速上下文消耗

**何时使用 gitdiff-watcher 而非原生 Stop hook**：

同样的质量门禁可以用约 20 行 bash、不借助 gitdiff-watcher 来实现。当你想要文件变更条件逻辑和状态持久化、又不想自己编写时，或当你需要在多语言代码库上进行并行检查时（例如同时进行 TypeScript 构建 + Kotlin 测试），就使用 gitdiff-watcher。

> **交叉引用**：Stop hook 的机制见 [ultimate-guide.md hooks 章节](../ultimate-guide.md)。关于 PostToolUse 构建检查（在每次文件编辑后触发，而非在交接时），参见约第 8262 行的 hooks 章节示例。

---

## 替代 UI

### Claude Chic

一个基于 Anthropic claude-agent-sdk 构建的、带样式的 Claude Code 终端 UI。它用视觉上更精美的体验替代了默认的 Claude Code TUI。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [Blog: matthewrocklin.com](https://matthewrocklin.com/introducing-claude-chic/) / [PyPI: claudechic](https://pypi.org/project/claudechic/) |
| **安装** | `uvx claudechic` |
| **语言** | Python (Textual + claude-agent-sdk) |
| **状态** | Alpha |

**核心特性**：

- 颜色编码的消息（橙色：用户，蓝色：Claude，灰色：工具）
- 可折叠的工具使用块
- 在 UI 内进行 git worktree 管理
- 在单个窗口中运行多个 agents
- `/diff` 查看器、vim 键位绑定（`/vim`）、shell 命令（`!ls`）
- 带流式输出的规范 Markdown 渲染

**局限性**：Alpha 状态——可能会有破坏性变更。Python 依赖链。需要 claude-agent-sdk。仅支持 macOS/Linux。

---

### Toad

一个面向 AI 编码 agents 的通用终端前端。通过 Agent Client Protocol (ACP)，除 Claude Code 外还支持 Gemini CLI、OpenHands、Codex 以及其他 12 多个 agents。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: batrachianai/toad](https://github.com/batrachianai/toad) / [willmcgugan.github.io/toad-released](https://willmcgugan.github.io/toad-released/) |
| **安装** | `curl -fsSL batrachian.ai/install \| sh` 或 `uv tool install -U batrachian-toad --python 3.14` |
| **作者** | Will McGugan（Rich 与 Textual 的作者） |
| **语言** | Python (Textual) |

**核心特性**：

- 横跨 12 多个 agent CLI 的统一界面
- 带 tab 补全的完整 shell 集成
- 带模糊搜索的 `@` 文件上下文注入
- 带语法高亮的并排 diff
- 受 Jupyter 启发的块导航
- 无闪烁的字符级渲染

**局限性**：仅支持 macOS/Linux（Windows 需通过 WSL）。agent 支持程度因 ACP 兼容性而异。暂无内置会话持久化（已列入路线图）。

---

### Conductor

一款 macOS 桌面应用，使用 git worktrees 并行编排多个 Claude Code（及 Codex）实例，集成了 diff 查看、PR 工作流和 GitHub 自动化。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [conductor.build](https://conductor.build) |
| **文档** | [docs.conductor.build](https://docs.conductor.build) |
| **安装** | 从 [conductor.build](https://conductor.build) 下载 |
| **平台** | 仅支持 macOS（计划支持 Windows/Linux） |
| **作者** | Melty Labs |

**工作区管理**：

- 每个 feature/bugfix 对应一个工作区，可用 `⌘⇧N` 创建，或直接从 GitHub issue 或 Linear issue 创建
- 工作区按状态组织：backlog → in progress → in review → done（v0.35.0）
- 在单一视图中跨多个 repo 分组工作区（v0.35.2）
- **Next Workspace** 按钮（v0.36.4）：跳转到下一个等待你输入的工作区，让你无需手动扫描被阻塞的 agents
- 归档已完成的工作区，同时保留完整的聊天历史

**diff 查看器与代码编辑**：

- 聊天面板中的集成 diff 查看器，针对每条 agent 消息逐轮显示 diff（v0.22.0）
- 用 `⌘D` 打开 diff；无需离开 Conductor 即可逐文件浏览
- **Manual Mode**（v0.37.0）：内置带语法高亮和 `⌘F` 搜索的文件编辑器——无需打开独立 IDE 即可完成快速编辑
- 直接在 diff 上评论并将反馈发送给 Claude（v0.10.0）

**GitHub 与 CI 集成**：

- 在 Checks 标签页查看 GitHub Actions 日志（v0.33.2）
- 失败的 CI 检查会自动转发给 Claude 修复（v0.12.0）
- 直接在 Checks 标签页编辑 PR 标题和描述（v0.34.1）
- 将 PR 评论从 GitHub 同步到 Conductor（v0.25.4）
- 在合并前，待办项会阻塞工作区直到被勾选完成（v0.28.4）
- 用 `⌘⇧P` 创建 PR

**Linear 及其他集成**：

- 将 Linear issue 附加到消息上，或直接从 Linear issue 打开一个 Conductor 工作区（v0.15.0、v0.36.5）
- 在 AI 生成的回复中嵌入指向 Linear、Slack、VS Code 的深链
- 支持 Mermaid 图表，可平移/缩放及全屏

**agent 支持**：

- Claude Code（默认）+ Codex 并排运行（v0.18.0）；可用键盘导航的模型选择器
- slash command 自动补全（例如用 `/restart` 重启 Claude Code 进程）

**社区报告的工作流模式**：

跨多个 repo、同时处理 5 个以上并行 feature 的用户报告了以下流程：每个 feature 创建一个工作区（以 GitHub issue 或 Linear issue 作为上下文），让 agents 运行，使用 **Next Workspace** 按钮只处理等待输入的工作区，在应用内审查 diff，从 Checks 标签页合并。有人报告了与 BMAD 的组合用法：每个 epic 一个工作区，一个 Claude agent 负责实现，另一个负责下一个 story——这被描述为面向规格驱动开发的显著生产力倍增器。

**局限性**：仅支持 macOS（截至 2026 年 3 月）。专有软件（非开源）。与下文列出的多 agent 编排工具有功能重叠。

---

### Piebald

一款面向 agentic AI 开发的跨平台桌面与 Web 应用。它在保持与 Claude Code hooks 系统及 AGENTS.md 约定完全兼容的同时，增加了多提供商支持和完整的 GUI 环境。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [piebald.ai](https://piebald.ai) / [docs.piebald.ai](https://docs.piebald.ai) |
| **GitHub** | [github.com/Piebald-AI](https://github.com/Piebald-AI) |
| **平台** | Windows / macOS / Linux + Web |
| **定价** | 免费（Basic）/ 20 美元/月（计划中） |
| **版本** | v0.3.1（2026 年 5 月） |

**核心特性**：

- **多提供商**：Claude Pro/Max、GitHub Copilot、Amazon Bedrock、Google Antigravity、Qwen，以及任何 OpenAI/Anthropic/Google 兼容的端点——自带订阅
- **Claude Code 兼容性**：明确支持 hooks、AGENTS.md、MCP 服务器、权限模式、subagents 和聊天 compaction
- **开发环境**：Git worktrees（一等公民）、集成终端、文件浏览器、Git 浏览器和代码编辑器（Pro）
- **聊天管理**：分支/fork、消息排队、slash commands、上下文管理、桌面通知
- **配置**：VS Code 主题导入、本地化（i18n）、颜色/字体自定义、Web 模式

**Windows 空白**：本节中所有其他"替代 UI"都仅支持 macOS/Linux。Piebald 是唯一原生支持 Windows 的 GUI 选项（无需 WSL）。

**与 Piebald-AI 组织的关系**：同一团队维护着 [claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts)——这是对 Claude Code 内部系统提示词最全面的公开逆向工程，本指南中多处引用。

**局限性**：专有软件，非开源。文件浏览器和代码编辑器需要 Pro 等级。

**关于 Agent View 的说明**：自 v2.1.139 起，Claude Code 通过 `claude agents` 原生支持多会话管理（见 [§9.17](#917-scaling-patterns-multi-instance-workflows)）。对于多提供商工作流、Windows，以及偏好完整 GUI 而非 CLI 的用户，Piebald 仍是合适的选择。

---

### Claude Code GUI（VS Code 扩展）

一个第三方 VS Code 扩展（并非 Anthropic 官方扩展），它在 Claude Code 之上增加了一层图形界面。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [VS Code Marketplace: MaheshKok.claude-code-gui](https://marketplace.visualstudio.com/items?itemName=MaheshKok.claude-code-gui) |
| **安装** | VS Code Marketplace → 搜索 "Claude Code GUI" |

**说明**：这**不是** Anthropic 官方的 [Claude Code for VS Code](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code) 扩展。官方扩展直接在编辑器中提供内联 diff、@-提及和 plan 审查。

**局限性**：第三方维护，非 Anthropic 维护。功能集可能与官方扩展重叠或落后于官方扩展。

---

## 多 Agent 编排

本节介绍用于**并行运行多个 Claude Code 实例**的工具。如需详细文档，请参阅：

- **[AI Ecosystem](./ai-ecosystem.md)** - Gas Town、multiclaude、agent-chat、claude-squad
- **[Ultimate Guide Section 9](../ultimate-guide.md)** - 多实例工作流、git worktrees、编排框架
- **[Agent Tools: Beyond Claude Code](./agentic-tools.md)** - Hermes Agent、Codex CLI、Devin、CrewAI、LangGraph 以及其他并非 Claude-Code 专用的工具

**快速参考**：

| 工具 | 类型 | 核心特性 |
|------|------|-------------|
| [Gas Town](https://github.com/steveyegge/gastown) | 多 agent 工作区 | Steve Yegge 的 agent-first 工作区管理器 |
| [multiclaude](https://github.com/dlorenc/multiclaude) | 多 agent 启动器 | tmux + git worktrees（383+ stars） |
| [agent-chat](https://github.com/justinabrahms/agent-chat) | 监控 UI | 面向 Gas Town/multiclaude 的实时 SSE 监控 |
| [abtop](https://github.com/graykode/abtop) | 舰队 TUI 监控器 | htop 风格：tokens、上下文 %、速率限制、端口、subagent 树（584+ stars） |
| [Conductor](#conductor) | 桌面应用 | macOS 并行 agents（上文亦有列出） |
| [Piebald](#piebald) | 桌面/Web 应用 | 多提供商 + Windows + hooks 兼容（上文亦有列出） |

---

### abtop

一个 Rust TUI，在一个屏幕中显示所有活跃的 Claude Code 和 Codex CLI 会话——就像 htop，但面向 agent 舰队。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: graykode/abtop](https://github.com/graykode/abtop) |
| **安装** | `curl --proto '=https' --tlsv1.2 -LsSf https://github.com/graykode/abtop/releases/latest/download/abtop-installer.sh \| sh` 或 `cargo install abtop` |
| **语言** | Rust (ratatui) |
| **许可证** | MIT |
| **平台** | macOS、Linux（Windows 需用 WSL） |

**核心特性**：

- 从本地进程/文件状态自动发现 Claude Code 和 Codex CLI 会话——无需 API key，无需认证
- 每会话条形图：token 用量、上下文窗口 %、速率限制配额
- 孤立端口检测，一键终止（`X`）
- subagent 树（仅 Claude Code）
- tmux 集成：按 `Enter` 直接跳转到会话窗格
- `--once` 标志用于快照输出（CI 友好）
- `--setup` 用于安装速率限制采集 hook
- 10 个内置主题，含 4 个色盲友好变体（`high-contrast`、`protanopia`、`deuteranopia`、`tritanopia`）

**用法**：

```bash
abtop                    # Launch TUI (requires 120x40 terminal, degrades gracefully to 80x24)
abtop --once             # Print snapshot and exit
abtop --setup            # Install rate limit collection hook
abtop --theme dracula    # Launch with a specific theme
```

**推荐的 tmux 配置**：

```bash
tmux new -s work
# pane 0: abtop
# pane 1: claude (project A)
# pane 2: claude (project B)
# Press Enter in abtop to jump to the active agent's pane
```

**各 agent 支持的特性**：

| 特性 | Claude Code | Codex CLI |
|---------|:-----------:|:---------:|
| Token 追踪 | ✅ | ✅ |
| 上下文窗口 % | ✅ | ✅ |
| 速率限制 | ✅ | ✅ |
| Subagents | ✅ | ❌ |
| 内存状态 | ✅ | ❌ |

> **何时使用**：跨多个项目运行 3 个以上并发 agent、撞上速率限制却不知道是哪个会话造成的，或者需要找出上一轮 agent 运行遗留的孤立端口时。

---

## 外部编排框架

> **架构上的区别**：上面提到的工具（Gas Town、multiclaude）是并排运行多个 Claude Code 实例。外部编排框架更进一步——它们用自己的运行时替换或增强 Claude Code 的内部编排层，在其之上叠加蜂群协调、持久化记忆和专用 agent 池。请先使用 Claude Code 的原生能力（Task 工具、sub-agents）；只有在用尽这些能力后，才转而使用这些框架。

### Ruflo（前身为 claude-flow）

**GitHub**：[github.com/ruvnet/ruflo](https://github.com/ruvnet/ruflo)（截至 2026 年 3 月超过 18.9k stars）
**npm**：`ruflo`（前身为 `claude-flow`） | **许可证**：MIT

为 Claude Code 设计的、采用率最高的外部编排框架。它将 Claude Code 转变为一个多 agent 平台，具备分层蜂群（queen + workers）、98 个专用 agent（编码者、测试者、审查者、架构师、安全审计师），并通过 SQLite（AgentDB）实现持久化记忆。

**两种安装路径**（覆盖面差异很大）：

| | Plugin 路径 | CLI 路径 |
|---|---|---|
| 你得到什么 | 每个 plugin 提供 slash commands + agent 定义 | 完整循环：98 个 agent、30 个 skill、MCP server、hooks、daemon |
| 工作区中的文件 | 零 | `.claude/`、`.claude-flow/`、`CLAUDE.md`、辅助脚本、settings |
| 是否注册 MCP server | 否 | 是（`memory_store`、`swarm_init`、`agent_spawn` 等） |
| 适合于 | 不做承诺地试用单个 plugin | 生产环境使用 |

```bash
# Plugin path
/plugin marketplace add ruvnet/ruflo
/plugin install ruflo-core@ruflo    # or any of the 33 available plugins

# CLI path (full install — inspect source first)
npx ruflo@latest init wizard
# Do NOT use the curl|bash variant: it pulls from the old repo name (claude-flow) and bypasses package manager security
```

**核心特性**：
- Q-Learning 路由器，根据过往模式将任务定向到合适的 agent
- 30+ 个内置 skill，27 个原生集成 Claude Code 的 hooks
- 带有 314 个工具的 MCP server（仅 CLI 路径）
- 基于 SQLite 的会话持久化，支持跨 agent 的记忆共享（AgentDB）
- **Agent 联邦（federation）**：通过 mTLS 和 ed25519 身份实现零信任的跨机器协作，在数据出站前剥离 PII，并对每个对等节点进行行为信任评分。与 LangGraph 或 CrewAI（默认单实例）不同，Ruflo 的 agent 可以跨机器、跨组织协调，而无需共享原始数据。通过 9 个 MCP 工具和 10 个 CLI 命令进行控制。
- 在 Claude Code 市场上有 33 个原生 plugin（swarm、RAG memory、安全、浏览器测试、IoT 等）
- 可选的 web UI 位于 [flo.ruv.io](https://flo.ruv.io/)，以及位于 [goal.ruv.io](https://goal.ruv.io/) 的 GOAP 目标规划器
- 非交互式 CI/CD 模式

> **关于声称的说明**：该项目发布了性能指标（SWE-Bench 分数、速度倍率、超过 2200 万次生态系统下载），但缺乏完全独立的方法论。存在一个将其与 LangGraph、AutoGen 和 CrewAI 对比的 SOTA 基准 gist，但独立复现尚未得到确认。请将所有数据视为未经验证。

> **关于成熟度的说明**：于 2026 年初从 claude-flow 重新命名。npm 包现在为 `ruflo`（已确认）。在生产环境部署前请检查源代码。

**何时使用**：当 Claude Code 的原生 Task 工具和 sub-agents 不足以应对时，通常用于需要跨众多会话保持持久状态的复杂多步流水线，或用于需要 agent 通过联邦跨机器协调的团队。

---

### Athena Flow

**GitHub**：[github.com/lespaceman/athena-flow](https://github.com/lespaceman/athena-flow) | **许可证**：MIT（声称）
**状态**：观察中——2026 年 3 月发布，尚未经过审计

一种不同的架构方法：Athena Flow 不增强 Claude Code 的 agent 层，而是位于 **hooks 层**。它通过 Unix Domain Socket（NDJSON）拦截 hook 事件，将其路由经过一个持久化的 Node.js 运行时，并提供一个 TUI 用于实时可观测性和工作流控制。

```
Claude Code → hook-forwarder → Unix Domain Socket → Athena Flow runtime → TUI
```

首个交付的工作流：自主 E2E 测试构建器（输出可用于 Playwright CI）。路线图：视觉回归测试、API 测试、Codex 支持。

**暂不推荐**——源代码审计待进行，项目过于新，无法评估稳定性。4-6 周后再行评估。

---

### Pipelex + MTHDS

**GitHub**：[github.com/Pipelex/pipelex](https://github.com/Pipelex/pipelex) —— 623 stars（2026 年 3 月）
**许可证**：MIT | **语言**：Python | **标准**：[mthds.ai](https://mthds.ai)

> **架构上的区别**：Pipelex 并不编排 Claude Code 的 agent——它提供一个 **声明式 DSL**（`.mthds` 文件）来定义可复用的 AI methods。Ruflo 管理的是 agent 蜂群，而 Pipelex 管理的是带类型、可用 git 版本化的多 LLM 流水线。

为开放标准 MTHDS 设计的 Python 运行时。一个 "AI method" 是一个多步骤工作流，它将 LLM、OCR 和图像生成串联起来——每一步都带类型，并在执行前进行校验。这些方法可用 git 版本化，可通过社区中心 [mthds.sh](https://mthds.sh) 分享，并可由 Claude Code 自动生成。

**Claude Code 集成**（推荐 Path A）：
```bash
pip install pipelex
npm install -g mthds
```
```
# Dans Claude Code :
/plugin marketplace add mthds-ai/skills
/plugin install mthds@mthds-ai-skills
/exit  # Relancer Claude Code

# Générer une méthode :
/mthds-build Analyse des CVs → scorecard + questions d'entretien

# Exécuter :
/mthds-run
```

**使用场景**：高频可重复的工作流——文档处理、候选人评分、邮件分类、合同分析。不适合开放式的创意探索，那种场景下 Claude Code 的原生 agent 仍然更为合适。

**状态**：观察中——存在 8 个月，MTHDS 标准尚未在大规模下得到验证。关注其在 2026 年 Q3 之前的发展势头。

---

## 知识图谱

### Graphify

一个 CLI 工具，它将代码库（外加任意组合的文档、PDF、图片和视频）映射为一个可查询的知识图谱。你不必每次会话都让 Claude Code 重新读取文件来理解结构，而是一次性构建图谱然后查询它。回报是：在熟悉项目结构上花费的 token 大幅减少，并能浮现出 grep 和手动浏览会遗漏的关联。

**GitHub**：[github.com/safishamsi/graphify](https://github.com/safishamsi/graphify)
**PyPI**：`graphifyy`（注意双 y——单 y 的那个包是另一个不相关的项目）
**许可证**：MIT | **语言**：Python 3.10+

| 属性 | 详情 |
|-----------|---------|
| **安装** | `uv tool install graphifyy`（推荐）或 `pipx install graphifyy` |
| **平台** | Claude Code、Cursor、Copilot CLI、Aider、Codex、Gemini CLI、OpenCode，以及另外 8+ 个 |
| **已验证** | 2026 年 5 月（v0.8.9） |

**每次运行的输出：**

| 文件 | 内容 |
|------|---------|
| `graphify-out/graph.html` | 带可点击节点和过滤功能的交互式可视化 |
| `graphify-out/GRAPH_REPORT.md` | 关键概念、出人意料的关联、建议的提问 |
| `graphify-out/graph.json` | 结构化图谱数据，每次查询都会复用 |

**底层原理——`graphify-out/` 中的缓存文件：**

除了那 3 个公开文件之外，Graphify 还保留了一个缓存层，用于支撑增量重建。这些隐藏文件会在首次运行后出现：

| 文件 | 作用 |
|------|------|
| `.graphify_ast.json` | 来自 tree-sitter 的原始 AST——全部代码，无任何 API 调用，通常 15-20 MB |
| `.graphify_detect.json` | `collect_files()` 的输出——完整的文件清单 |
| `.graphify_chunk_XX.json` | 发送给 AI API 进行语义提取的成批文件 |
| `.chunk_manifest_XX.json` | 每个 chunk 包含哪些文件——被 `--update` 用于隔离变更 |
| `.graphify_semantic.json` | 实体去重后的语义嵌入 |
| `.graphify_uncached.txt` | 上次运行中尚未缓存的文件 |
| `cache/` | 每个文件的内容哈希，用于变更检测 |

执行 `--update` 时：Graphify 将当前内容哈希与缓存进行比较，识别出哪些文件发生了变更，仅通过 AI API 重新处理它们的 chunk，然后从未变更的 chunk 加上新的 chunk 重建 `graph.json`。未变更的文件耗费零 API token。

**在项目中初始化：**

```bash
# 1. Build the graph from project root
graphify .

# 2. Register with Claude Code — installs the /graphify skill
graphify install --platform claude

# 3. Commit the output so teammates start with a pre-built map
git add graphify-out/ && git commit -m "chore: add graphify knowledge graph"
# Or exclude it entirely: echo "graphify-out/" >> .gitignore

# 4. Subsequent runs: --update uses semantic caching by content hash
#    Only changed files get re-processed — saves API cost on large repos
graphify . --update
```

**查询图谱：**

```bash
graphify query "what connects auth to the database?"
graphify path "UserService" "DatabasePool"
```

一旦在 Claude Code 中注册，安装的 skill 就能让 Claude 直接读取 `graph.json`，而无需爬取文件——因此查询发生在对话内部，无需重新读取源代码。

**关键分析特性：**

- **God nodes（上帝节点）**：高度互连的架构枢纽——其他一切都依赖的组件
- **出人意料的关联**：按"意外程度"评分排序的跨模块链接
- **设计原理提取**：从内联注释和 docstring 中提取 WHY（为什么），而不仅仅是 WHAT（是什么）
- **置信度标记**：每个关系都会被标记为 `EXTRACTED`（显式的 import/调用）、`INFERRED`（从上下文推断）或 `AMBIGUOUS`（标记以待复查）

**文件支持**：31 种编程语言、Markdown、RST、YAML、HTML、PDF。视频和音频：`pip install graphifyy[video]`（本地 faster-whisper，无外部 API 调用）。Office 文档：`pip install graphifyy[office]`。

**MCP server 模式：**

```bash
# Exposes: query, shortest_path, god_nodes, neighbor_traversal tools
graphify mcp
```

对于大型代码库（graph.json 超过约 5 MB），MCP 模式效率明显更高。没有它时，Claude 会先加载 `GRAPH_REPORT.md` 来熟悉情况，然后按需拉取 `graph.json` 的目标片段。运行 MCP 时，Claude 直接调用 `god_nodes`、`query "auth flow"` 或 `shortest_path`，只接收相关的子图——无需将整个图谱加载进上下文。一个完整加载的 22 MB `graph.json` 耗费的 token 远多于返回相同答案的 4-5 次目标 MCP 工具调用。

**Claude 如何使用安装的 skill：**

执行 `graphify install --platform claude` 后，该 skill 会注入一条规则：如果当前项目中存在 `graphify-out/`，就把架构类问题当作图谱查询来处理，而不是读取文件。实践中的解析顺序：

1. Claude 先读取 `GRAPH_REPORT.md`——它很紧凑（通常 150-200 KB），提供关于 god nodes 和出人意料关联的概览
2. 对于具体查询，Claude 查阅 `graph.json` 的目标片段
3. 在运行 MCP server 时：Claude 直接调用 `query`、`shortest_path`、`god_nodes` 或 `neighbor_traversal` 工具——在大规模下成本低得多

没有 Graphify 时：Claude 每次会话都重新读取源文件来理解结构，在熟悉项目结构上烧掉 token。有了 Graphify：这笔成本在构建时一次性付清，然后分摊到所有会话中。

**额外的导出**：维基百科风格的、带跨社区 wikilink 的 wiki；带 Canvas 布局的 Obsidian vault；D3 可折叠树形 HTML；带交互式缩放/平移的 Mermaid 调用流程图；Neo4j 图谱推送。

**隐私**：代码文件通过 tree-sitter 在本地处理，代码分析不进行任何 API 调用。文档和 PDF 会发送到你配置的 AI 模型 API。如需完全本地推理：`pip install graphifyy[ollama]`。

**团队工作流**：将 `graphify-out/` 提交到 git，可让每个队友在 clone 时获得一份共享的图谱。Graphify 附带一个 git merge driver，可防止 `graph.json` 中出现冲突标记，并提供可选的 git hooks 用于在 commit 时自动重建。

**流水线：** `detect() → extract() → build_graph() → cluster() → analyze() → report() → export()`——每个阶段相互隔离，无共享状态。新增一种语言需要在 `extract.py` 中注册一个 extractor，并加上 tree-sitter 依赖。

**局限性：**

- 包名 `graphifyy`（双 y）是主要的摩擦点——`pip install graphify` 会安装一个不相关的工具，且不报任何错误
- 文档/PDF 提取会进行 AI API 调用；成本随文档体量而非代码体量扩展
- v0.8.x 演进很快；某些 CLI flag 在不同的次要版本之间会发生变化，升级前请查看 changelog

**何时使用**：大型或不熟悉的代码库，Claude Code 仅仅为了理解结构就会反复读取文件而烧掉 token。一次性构建图谱，然后查询它。对于遗留代码的上手、monorepo 导航以及 PR 前的架构审查，价值很高。

---

## Skills 可观测性

### Skillsight

唯一一款面向团队级 skills 使用分析的开源工具。它接入 Claude Code 的 OTEL 遥测数据，展示哪些 skills 实际被调用了——由谁调用、调用频率、在哪些会话中调用——而不是你以为正在被使用的那些 skills。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub — PackmindHub/skillsight](https://github.com/PackmindHub/skillsight) |
| **作者** | Cédric Teyton (Packmind) |
| **许可证** | Apache 2.0 |
| **版本** | 0.2.1（活跃，101 commits） |
| **技术栈** | Bun + Hono + PostgreSQL + React 18（自托管 Docker） |
| **数据接入** | 来自 Claude Code 的 OTLP HTTP push，或来自 Grafana Cloud 的 Loki pull |

**它追踪什么：** 按用户和会话维度的 skill 调用情况、插件目录（从 Git marketplaces 同步）、群体细分、审计日志、实时事件流。

**两种数据接入模式：**

*直接 OTLP push* —— Claude Code 将遥测数据直接发送给 Skillsight。延迟更低、配置更简单：

```json
// ~/.claude/settings.json
{
  "env": {
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_LOGS_ENDPOINT": "http://your-skillsight:4200/api/v0/telemetry/v1/logs",
    "OTEL_EXPORTER_OTLP_LOGS_HEADERS": "Authorization=Bearer <your-ingestion-token>",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "http/json",
    "OTEL_LOG_TOOL_DETAILS": "1",
    "OTEL_LOGS_EXPORT_INTERVAL": "5000"
  }
}
```

*Loki pull* —— Skillsight 按可配置的计划周期轮询某个 Grafana Cloud Loki 端点。如果你已经在那里聚合日志，这种方式很有用。

数据接入令牌在 Skillsight UI（`/tokens`）中创建，其 JWT 类型与会话令牌不同——它只能写入遥测数据，无法访问管理界面。

**配置（直接 push）：**

1. `docker compose up -d` —— 在 4200 端口上启动 Skillsight + Postgres
2. 使用初始管理员凭据登录 `http://localhost:4200`
3. 进入 Onboarding 页面——它会生成一段完整的 settings.json 代码片段，其中包含一个预先创建好的数据接入令牌
4. 将该代码片段复制到 `~/.claude/settings.json` 或你的项目级 `.claude/settings.json`
5. 运行一次 Claude Code 会话——事件会在 5 秒内出现在仪表盘中

**部署注意事项（投入生产前请阅读）：**

- **切勿在不覆盖 `JWT_SECRET` 和 `ADMIN_PASSWORD_INITIAL` 的情况下部署**——出厂默认值是字面意义上的公开字符串（`change-me-in-production...` 和 `admin`）。系统不会在启动时发出任何警告。任何使用这些默认值且可从公网访问的实例都极易被攻破。
- **在你的 `.env` 中设置 `PUBLIC_BASE_URL`**——该变量同时控制 CORS 策略以及 Onboarding 代码片段中显示的端点。若不设置，CORS 会处于宽松状态（回显请求来源），且代码片段会显示 `https://your-domain.com`。
- **升级时手动运行 Drizzle 迁移**——容器在启动时不会自动运行 `drizzle-kit migrate`（截至 v0.2.1）。如果从 0.1.x 升级，请在启动新容器前运行迁移，否则应用会因 schema 过时而崩溃。

这些都是正在积极开发中的已知问题。修复方式很直接；可在该仓库追踪解决进展。

**局限性：**

- 仅支持自托管——无 SaaS 服务
- Marketplace 来源管理仅支持 API（暂无 UI，文档中也没有 curl 示例）
- README 中镜像名称不一致（`skills-obs` 与实际的 `skillsight`）——请以 `docker-compose.yml` 为准，而非 README 中的 curl 代码片段
- v0.2.x——项目尚年轻，文档有些粗糙之处；不过其 CLAUDE.md 对贡献者来说确实很有用

**何时使用：** 你想知道团队在实践中实际调用了哪些 skills，而非你部署了哪些。对于评估 skills 库的 ROI、衡量 onboarding 成效以及识别无用的 skills 很有帮助。

> **相关：** [Packmind ContextOps Platform](#engineering-standards-distribution) —— 同一作者用于向 AI agents *分发* 标准的工具。Skillsight 告诉你哪些 skills 被使用了；Packmind 则帮助你编写并同步它们。
> **评估：** [2026-05-18-skillsight-packmind.md](../../docs/resource-evaluations/2026-05-18-skillsight-packmind.md)

---

## 插件生态系统

Claude Code 的插件系统支持社区构建的扩展。详细文档见：

- **[Ultimate Guide Section 8](../ultimate-guide.md)** - 插件系统、命令、安装
- **[claude-plugins.dev](https://claude-plugins.dev)** - 已索引 11,989 个插件、63,065 个 skills
- **[claudemarketplaces.com](https://claudemarketplaces.com)** - 自动扫描 GitHub 寻找 marketplace 插件
- **[agentskills.io](https://agentskills.io)** - agent skills 的开放标准（26+ 平台）

**值得关注的 skill 包**：
- **[Superpowers](https://github.com/obra/superpowers)** —— 完整的软件开发方法论套件（95k+ stars，7.5k forks，MIT）。7 个上下文感知的 skills，覆盖完整的开发流程：通过苏格拉底式头脑风暴进行需求规约引出、详细的实现规划（2-5 分钟粒度的任务，附带精确文件路径）、由 subagent 驱动的开发并配两阶段评审（先检查规约符合性，再检查代码质量）、强制 TDD（在测试被删除之前必须先写代码）、代码评审、git worktree 管理，以及分支生命周期收尾（合并/PR/丢弃决策）。Skills 会根据上下文自动触发——无需手动调用。安装：`/plugin install superpowers@claude-plugins-official`。由 Jesse Vincent (Prime Radiant) 创建，MIT。同时支持 Cursor、Codex、OpenCode 和 Gemini CLI。
- **[gstack](https://github.com/garrytan/gstack)** —— 6 个 skill 的工作流套件，覆盖完整的发布周期：战略产品关卡（`/plan-ceo-review`）、架构评审（`/plan-eng-review`）、偏执式代码评审（`/review`）、自动化发布（`/ship`）、原生浏览器 QA（`/browse`），以及复盘（`/retro`）。由 Garry Tan (Y Combinator CEO) 创建。工作流模式与采用指南见 [Cognitive Mode Switching](../workflows/gstack-workflow.md)。

---

## 已知空白

截至 2026 年 2 月，社区工具生态系统仍存在一些显著空白：

| 空白 | 描述 |
|-----|-------------|
| **Skills 使用分析** | ✅ **已填补**：[Skillsight](https://github.com/PackmindHub/skillsight)（Packmind，2026 年 5 月发布）—— 自托管的 OTEL 仪表盘，展示每个用户/会话中实际调用了哪些 skills。部署时需注意若干事项（见 [Skills 可观测性](#skills-observability)）。 |
| **可视化 skills 编辑器** | 没有用于创建/编辑 `.claude/skills/` 的 GUI——必须手动编辑 YAML/Markdown |
| **可视化 hooks 编辑器** | 没有用于在 `settings.json` 中管理 hooks 的 GUI——需要手动编辑 JSON |
| **统一管理面板** | 没有一个能将配置、会话、成本和 MCP 管理整合在一起的单一仪表盘 |
| **会话回放** | ✅ **已填补**：Entire CLI（2026 年 2 月发布）提供可回退的检查点，并支持完整上下文回放 |
| **自动化 `.claude/` 安全扫描** | ✅ **已填补**：[AgentShield](https://github.com/affaan-m/agentshield)（2026 年 2 月发布）—— 102 条规则的扫描器，提供 A–F 评级、`--fix` 以及 GitHub Action 集成 |
| **agent 原生的 issue 跟踪** | 尚无成熟的工具用于结合 Claude Code 进行基于 markdown、可提交至 git 的 issue 跟踪。[fp.dev](https://fp.dev/) 是一个早期阶段的方案（本地优先，`/fp-plan` + `/fp-implement` skills，diff 查看器），但缺乏采用信号，且桌面应用需要 Apple Silicon。Tasks API 覆盖了状态持久化，但 issues 无法提交至 git。 |
| **单 MCP server 级别的性能分析器** | 无法单独衡量归因到每个 MCP server 的 token 成本 |
| **跨平台配置同步** | 没有工具能跨机器同步 Claude Code 配置（必须手动复制 `~/.claude/`） |
| **可编程的沙箱化编排** | 关注：[Sandcastle](https://github.com/mattpocock/sandcastle)（`@ai-hero/sandcastle`，Matt Pocock）—— 一套 TypeScript API，用于在 Docker/Podman/Vercel 容器中运行 agents，支持分支策略管理和提示词模板化。定位独特但在 v0.5.x 阶段尚未达到可纳入指南的程度（存在活跃 bug、仅支持 TypeScript、需要单独的 `ANTHROPIC_API_KEY`、对 Docker/Podman 强依赖）。待 v1.0 时再评估。 |

---

## 按角色划分的推荐

| 角色 | 推荐工具 | 理由 |
|---------|-------------------|-----------|
| **独立开发者** | ccusage + claude-code-viewer | 成本感知 + 会话历史回顾 |
| **小型团队（2-5 人）** | ccusage + Conductor 或 multiclaude | 成本追踪 + 并行开发 |
| **企业级** | ccusage (MCP) + 自定义仪表盘 | 可编程的成本数据 + 审计轨迹 |
| **以 Python 为中心** | ccburn + Claude Chic | 原生 Python 生态工具 |
| **多 agent 用户** | Toad 或 Conductor | 统一的 agent 管理 |
| **配置繁重的环境** | claude-code-config + AIBlueprint + Caliber | TUI 配置管理 + 脚手架 + 漂移检测 |
| **代码库新人 / monorepo** | Graphify | 构建一次图谱，通过查询结构来代替每次会话重新读取文件 |
| **团队 skills 采用** | Skillsight | 衡量整个团队中实际被调用的 skills，识别无用的 skills |

---

## 相关资源

- [可观测性](../ops/observability.md) - DIY 会话监控、日志 hooks、成本追踪脚本
- [AI 生态系统](./ai-ecosystem.md) - 互补的 AI 工具（Perplexity、Gemini、NotebookLM）
- [MCP Servers 生态系统](./mcp-servers-ecosystem.md) - 经过验证的社区 MCP servers
- [架构](../core/architecture.md) - Claude Code 内部如何运作
- [Ultimate Guide Section 8](../ultimate-guide.md) - 插件系统与 marketplaces
