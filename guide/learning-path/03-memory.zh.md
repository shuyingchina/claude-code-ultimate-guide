# 模块 03：记忆与配置

**时长**：1 小时 | **难度**：⭐⭐ 中级

## 目标

配置 Claude Code 以记住你的偏好和项目专属规则。构建你的第一个 CLAUDE.md 文件。

---

## 你将学到什么

- Claude Code 的记忆层级如何运作
- 创建和组织 CLAUDE.md 文件
- 设置项及其优先级
- 自定义指令和 agent 定义
- 项目级配置与全局配置

---

## 记忆层级

Claude Code 在三个层级上记住偏好：

```
┌──────────────────────────────────────────┐
│ 1. GLOBAL (~/.claude/CLAUDE.md)          │
│    Applies to ALL your projects          │
│    Example: Your coding style, timezone  │
└──────────────────────────────────────────┘
                    ▲
                    │ (overridden by)
                    │
┌──────────────────────────────────────────┐
│ 2. PROJECT (/your-project/CLAUDE.md)    │
│    Applies to THIS project only          │
│    Example: Team standards, tech stack   │
└──────────────────────────────────────────┘
                    ▲
                    │ (overridden by)
                    │
┌──────────────────────────────────────────┐
│ 3. PERSONAL (/your-project/.claude/)    │
│    Local settings, not committed to git  │
│    Example: API keys, personal prefs     │
└──────────────────────────────────────────┘
```

### 规则
第 3 级的设置覆盖第 2 级，第 2 级覆盖第 1 级。

---

## 创建你的第一个 CLAUDE.md

CLAUDE.md 是一个简单的 markdown 文件，用于告诉 Claude Code 你的规则。

### 基本结构

```markdown
# My Project

## Purpose
Brief description of what this project does.

## Tech Stack
- TypeScript
- React 18
- Next.js
- PostgreSQL

## Coding Standards
- Use functional components only
- All exports must be typed
- Max 300 lines per file
- Use meaningful variable names (no `x`, `temp`)

## Behavioral Rules
Always review diffs before accepting.
Use /plan for any breaking changes.

## Git Workflow
- All work on feature branches
- PRs require 1 approval
- Commits must be squashed

## Current Status
What you're currently working on.
```

### 最小示例（从这里开始）

创建 `/your-project/CLAUDE.md`：

```markdown
# My Project

## Quick Context
- Frontend: React with TypeScript
- Backend: Node.js with Express
- Database: PostgreSQL
- Package manager: pnpm

## Coding Rules
- Functional programming preferred
- All functions must have type signatures
- Tests are required for features
- No console.log in production code

## My Preferences
- Use /plan for architectural changes
- Be verbose in comments, not code
- Ask before making cross-file refactors
```

Claude 会在会话开始时自动读取这个文件并遵循你的规则。

---

## CLAUDE.md 里可以放什么？

你几乎可以配置任何东西。常见的章节：

### 1. 项目概览
```markdown
## Purpose
This is our payment processing backend.
It handles credit card validation and transaction logging.

## Important
- Handles PCI-DSS compliance critical code
- Must never log card numbers
- All changes need security review
```

### 2. 技术栈
```markdown
## Stack
- Language: Python 3.10+
- Framework: Django 4.0
- Database: PostgreSQL 13
- Cache: Redis
- Task queue: Celery
```

### 3. 编码规范
```markdown
## Code Style
- Follow PEP 8
- Type hints on all functions
- Docstrings in Google format
- No wildcard imports
- Max line length: 100 chars

## Testing
- Minimum 80% coverage
- Unit + integration tests
- Use pytest
```

### 4. 规则
```markdown
## Rules
- All PRs require review
- No direct pushes to main
- Database migrations need approval
- Security changes flagged automatically
- /plan mode for refactors >100 lines
```

### 5. 当前工作
```markdown
## Current Task
Building the checkout flow.
Working on: src/checkout/payment-form.tsx
Dependencies: stripe-js library, payment API
```

---

## 全局 CLAUDE.md

对于适用于**所有项目**的设置，创建 `~/.claude/CLAUDE.md`：

```markdown
# My Global Preferences

## Communication Style
- Be direct and factual
- Show working in steps
- Suggest alternatives when unclear

## Tools I Use
- TypeScript for all JS projects
- Python for data/scripts
- Docker for deployment
- Git for all version control

## My Timezone
America/New_York

## 工作时间
Mon-Fri 9am-5pm (UTC-5)
```

Claude 会在启动时加载这个文件，并将其与你的项目 CLAUDE.md 结合使用。

---

## 项目专属 vs 全局

### 在以下情况使用全局：
- 你的通用编码风格（命名约定、处理方式）
- 你始终使用的工具
- 沟通偏好
- 通用原则

### 在以下情况使用项目级：
- 团队标准（如果与你的全局设置不同）
- 项目专属的技术栈
- 业务规则（PCI 合规等）
- 当前的工作上下文

### 示例

**全局**（~/.claude/CLAUDE.md）：
```markdown
## My Style
Functional programming, clear variable names, typed functions
```

**项目**（my-payment-app/CLAUDE.md）：
```markdown
## Special Rules
Security critical—use /plan for all changes.
Must handle PCI compliance.
```

Claude 会将两者结合：你的风格 + 项目规则。

---

## 练习：创建你的 CLAUDE.md

### 第 1 步：选择一个项目

使用现有项目，或创建一个测试目录：

```bash
mkdir test-claude-config
cd test-claude-config
git init
```

### 第 2 步：创建 CLAUDE.md

```bash
cat > CLAUDE.md << 'EOF'
# My Test Project

## Tech Stack
- Language: [your main language]
- Framework: [what you use]
- Database: [if applicable]

## Coding Standards
- [Rule 1]
- [Rule 2]

## My Preferences
- [Preference 1]
- [Preference 2]
EOF
```

### 第 3 步：启动 Claude

```bash
claude
```

Claude 会显示它在启动时加载了 CLAUDE.md。

### 第 4 步：测试它

让 Claude 做点什么。它应该遵循你的规则。

```
Add a function called greet that returns "Hello, World!"
```

Claude 应该：
1. 提到你的技术栈
2. 遵循你的编码标准
3. 尊重你的偏好

---

## .claude/ 目录

对于本地设置（不提交到版本库），使用 `.claude/`：

```
my-project/
├── CLAUDE.md           (committed - team rules)
├── .claude/
│   ├── settings.json   (not committed - personal settings)
│   ├── agents/         (custom agents)
│   ├── skills/         (custom skills)
│   └── hooks/          (automation scripts)
```

添加到 `.gitignore`：
```
.claude/
.claude/settings.json
```

例外：如果 `.claude/agents/` 是面向整个团队的，你可以提交它们。

---

## Settings.json（可选）

如需精细化控制，创建 `.claude/settings.json`：

```json
{
  "model": "claude-opus-4-7",
  "temperature": 0.7,
  "context_threshold": 0.75,
  "auto_compact": true,
  "require_diff_review": true,
  "max_file_size": 10000
}
```

常用设置：
- **model**：使用哪个 Claude 模型
- **context_threshold**：何时对上下文发出警告（0.7 = 70%）
- **auto_compact**：达到阈值时自动 compact
- **require_diff_review**：强制审查所有更改（安全的默认值）

---

## Agents 与 Skills（预览）

在 CLAUDE.md 中，你可以引用自定义 agents：

```markdown
## Available Agents
- /code-reviewer: Reviews code for quality
- /security-auditor: Scans for vulnerabilities
- /test-writer: Generates test cases

Use with: /agent code-reviewer
```

它们定义在 `.claude/agents/` 中（将在 Module 04 中介绍）。

---

## 最佳实践

### 应该做

✅ 随着项目演进，保持 CLAUDE.md 更新

✅ 将你的项目 CLAUDE.md 纳入版本控制（有助于团队成员）

✅ 对需求保持具体（不要含糊）

✅ 包含 "Current Status" 部分，让 Claude 拥有上下文

✅ 记录重要的业务规则

### 不应该做

❌ 在 CLAUDE.md 中存储密码或密钥（使用 .env 或密钥管理器）

❌ 让它太长（>500 行会令人不堪重负）

❌ 在全局规则与项目规则之间使用相互冲突的规则

❌ 假设 Claude 会记住之前会话的偏好

---

## 验证：满足以下条件即表示你准备就绪……

✓ 你已在某个项目中创建了 CLAUDE.md 文件

✓ 你能够解释三层层级（全局、项目、个人）

✓ 你理解哪些内容应放入已提交的 CLAUDE.md，哪些应放入 .claude/

✓ 你已启动 Claude 并看到它加载了你的 CLAUDE.md

✓ Claude 至少遵循了你 CLAUDE.md 中的一条规则

---

## 接下来是什么？

**模块 04：Agents 与专业化** 涵盖：
- 为特定任务创建专门的 agents
- 限制 agent 的能力
- 编排多个 agents
- 使用 agents 的团队工作流

这将教你如何创建专注的 AI 角色，而不是使用单个通用的 Claude。

---

**完成模块 03 了吗？** → 准备进入模块 04：Agents 与专业化

---

## 更进一步：跨会话与团队记忆

上述章节涵盖了基础的 CLAUDE.md 模式。当你准备深入了解时，生态系统还有更多内容：

**Auto Memory 与 Auto Dream（原生，v2.1.59+）**

Claude Code 可以在会话之间编写自己的 MEMORY.md（Auto Memory），并在后台对其进行整合（Auto Dream）。两者开箱即用，可通过 `/memory` 管理已存储的条目。参见 [记忆系统：Auto Memory](../core/memory-systems.md#22-auto-memory-v21594) 和 [Auto Dream](../core/memory-systems.md#23-auto-dream-background-consolidation)。

**面向个人开发者的跨会话工具**

- **claude-mem**（26.5K stars）—— 通过 hooks 自动压缩会话，无需手动调用。安装：`/plugin marketplace add thedotmack/claude-mem`
- **agentmemory**（16K stars）—— BM25 + 向量 + 图的混合检索，12 个自动接线的 hooks，在 LongMemEval-S 上 R@5 达到 95.2%
- **ICM**（Rust 二进制文件）—— 情景衰减 + 永久知识图谱，`brew install icm`，支持 14 个 IDE 客户端

**团队共享**

- Trinity 模式：CLAUDE.md + `.mcp.json` + `/skills` 全部提交到仓库 —— 零基础设施，零成本
- **Mem0 Cloud MCP** —— 通过 `npx mcp-add --url https://mcp.mem0.ai/mcp` 实现共享记忆池，提供免费层级
- **doobidoo** —— 跨 13+ 个 IDE 的语义搜索，本地 SQLite 或 Cloudflare D1 后端

所有工具、架构模式、风险以及决策流程图的完整说明：[记忆系统指南](../core/memory-systems.md)。
