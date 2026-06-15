---
title: "Spec-First Development with Claude"
description: "Define specifications in CLAUDE.md before implementation for structured development"
tags: [workflow, architecture, config]
---

# 用 Claude 做规格优先开发（Spec-First Development）

> **可信度**：Tier 2 —— 已被多个生产团队验证，并与官方 SDD 指导保持一致。

在让 Claude 动手构建之前，先在 CLAUDE.md 里定义你想要的东西。一次结构良好的迭代抵得上 8 次无结构的迭代。

---

## 目录

1. [TL;DR](#tldr)
2. [模式](#the-pattern)
3. [任务粒度：为 agents 划定合适的工作量](#task-granularity-sizing-work-for-agents)
4. [CLAUDE.md 规格模板](#claudemd-spec-templates)
5. [分步工作流](#step-by-step-workflow)
6. [与工具的集成](#integration-with-tools)
7. [何时使用](#when-to-use)
8. [反模式](#anti-patterns)
9. [另请参阅](#see-also)

---

## TL;DR

```
1. Write spec in CLAUDE.md
2. Claude reads spec automatically
3. Implementation follows spec exactly
4. Verify against spec
```

CLAUDE.md 就是你的规格文件。把它当作一份契约来对待。

---

## 模式

规格优先开发颠倒了典型的 AI 编码流程：

```
Traditional:        Spec-First:
───────────         ──────────
Prompt → Code       Spec → Prompt → Code → Verify
  │                   │               │       │
  └─ Hope it's       └── Contract    └── Follows spec
     what you want        defined          └── Check against spec
```

规格成为唯一可信来源，它能：
- 约束 Claude 构建的内容
- 为团队记录决策
- 让完整性可被验证

---

## 任务粒度：为 agents 划定合适的工作量

在编写规格之前，先确认任务大小是否合适。Agents 在面对**垂直切片（vertical slices）**时表现最好 —— 即贯穿所有层、但只实现一个完整用户行为的薄薄的端到端单元（例如「通过邮件重置密码」，而不是「认证系统」）。

**经验法则**：一次 agent 会话 = 一个垂直切片。如果任务描述需要用「and」连接两个用户行为，就把它拆开。

### PRD 质量检查清单

在把任何任务交给 agent 之前先跑一遍这份清单。需要验证六个维度：

| 维度 | 要问的问题 | 危险信号 |
|-----------|----------------|----------|
| **问题清晰度** | 问题陈述是否无歧义？ | 「提升性能」 |
| **可测试标准** | 完成与否能否自动验证？ | 「运行良好」 |
| **范围边界** | 哪些内容被明确排除在范围之外？ | 没有列出任何排除项 |
| **可观测的完成态** | 在用户看来「完成」是什么样子？ | 仅描述内部行为 |
| **需求清晰度** | 规格中没有混入实现细节？ | 「用 Redis 做缓存」 |
| **术语** | 全程使用同一套术语？ | 「user」和「account」混用 |

一项有 2 个或更多维度不达标的任务，需要在 agent 接手之前先返工。规格评审能在早期捕获歧义，否则这些歧义会在会话进行到一半时以错误实现的形式暴露出来。

```
❌ Too big, ambiguous:
"Add user authentication to the app"

✅ One vertical slice:
"Users can log in with email + password.
- POST /auth/login returns JWT on success, 401 on failure
- Invalid credentials show 'Email or password incorrect' (not which is wrong)
- Session expires after 24h
- Out of scope: OAuth, password reset, remember me"
```

### 特性清单（Feature List）：机器可读的范围控制

特性清单是一个 JSON 文件，用于跨 agent 会话逐个特性地跟踪范围和完成状态。与描述意图的 PRD 不同，特性清单是 agent 的操作性契约：会话开始时读取它，会话结束时更新它，并在多次交接之间持续存在。

每个特性条目都有三个必填字段。`description` 告诉 agent 要构建什么。`verify` 字段是一条成功时退出码为 0 的 shell 命令，这一点很重要，因为它强制让「完成的定义」变成可执行的，而不仅仅是描述性的。`status` 字段通过一个单向状态机跟踪进度：`not_started` → `active` → `blocked` → `passing`。一个条目只能向前推进，永远不能后退。当一个特性达到 `passing` 时，`evidence` 字段会记录是什么证明了它（一个测试名称、命令输出，或某条具体的日志行）。

WIP=1 规则在这里同样适用：任何时刻只能有一个特性处于 `active` 状态。多个 active 特性会导致工作半途而废，并且无法对它们逐一完成验证。

把 `feature_list.json` 与 `AGENTS.md` 一起存放在项目根目录。会话开始时，agent 读取它，以了解已完成的工作以及接下来该挑选什么。会话结束时，agent 在提交之前写入更新后的状态和证据。

特性清单与 `claudedocs/handoffs/` 配合使用。这两件产物共同为下一次会话提供操作性状态（哪些特性已完成并经过验证）和叙事性上下文（发生了什么、尝试了什么、还有什么悬而未决）。二者谁也无法替代谁。

下面这个最小示例展示了处于不同阶段的两个特性：

```json
{
  "features": [
    {
      "id": "feat-001",
      "name": "Document Import",
      "description": "Allow users to import PDF and TXT files from local filesystem",
      "verify": "npm test -- --grep 'document import'",
      "status": "passing",
      "evidence": "npm test: 12 passed, 0 failed (2026-05-01 14:22)"
    },
    {
      "id": "feat-002",
      "name": "Document Chunking",
      "description": "Split imported documents into ~500-character chunks with metadata",
      "verify": "npm test -- --grep 'chunking'",
      "status": "not_started",
      "evidence": "",
      "dependencies": ["feat-001"]
    }
  ]
}
```

`feat-001` 上的 `evidence` 字段精确地展示了运行了什么以及何时运行的。`feat-002` 条目处于 `not_started` 状态，`evidence` 字段为空，等待 `feat-001` 被确认为 passing 之后才会变为 `active`。这一模式在 Anthropic 工程博客关于[长时运行应用的 harness 设计](https://www.anthropic.com/engineering/harness-design-long-running-apps)的文章中有所描述。在 `examples/workflows/feature-list.json` 处提供了一个可直接使用的模板。

---

## CLAUDE.md 规格模板

### 特性规格（最常见）

```markdown
## Feature: [Name]

### Description
[2-3 sentences explaining the feature purpose]

### Capabilities
- MUST: [Required functionality]
- MUST: [Another requirement]
- SHOULD: [Nice to have]
- MUST NOT: [Explicit exclusions]

### Tech Stack
- Required: [lib1, lib2, lib3]
- Forbidden: [lib4, lib5]

### Acceptance Criteria
- [ ] Criterion 1: [Specific, testable condition]
- [ ] Criterion 2: [Another condition]
- [ ] Criterion 3: [Edge case handling]

### API Contract (if applicable)
- Endpoint: POST /api/[resource]
- Request: { field1: string, field2: number }
- Response: { id: string, created: timestamp }
- Errors: 400 (validation), 404 (not found), 500 (server)
```

### 架构规格

```markdown
## Architecture: [Component Name]

### Purpose
[Why this component exists]

### Boundaries
- Owns: [What this component is responsible for]
- Delegates to: [What other components handle]
- Does NOT: [Explicit non-responsibilities]

### Dependencies
- Upstream: [Components that call this]
- Downstream: [Components this calls]

### Data Flow
```
Input → Validation → Processing → Output
         │              │
         └─ Errors ─────┘
```

### Constraints
- Performance: [Response time, throughput]
- Security: [Auth requirements, data handling]
- Scalability: [Expected load, limits]
```

### API 规格

```markdown

## API：[端点名称]

### Endpoint
`POST /api/v1/[resource]`

### Authentication
需要 Bearer token。作用域：`read:resource`、`write:resource`

### Request
```json
{
  "field1": "string (required, max 255 chars)",
  "field2": "number (optional, default: 0)",
  "nested": {
    "subfield": "boolean"
  }
}
```

### Response
```json
{
  "id": "uuid",
  "created_at": "ISO 8601 timestamp",
  "data": { ... }
}
```

### 错误码
| 错误码 | 含义 | 响应体 |
|------|---------|---------------|
| 400 | 校验失败 | `{ "errors": [...] }` |
| 401 | 未认证 | `{ "message": "..." }` |
| 403 | 未授权 | `{ "message": "..." }` |
| 404 | 资源未找到 | `{ "message": "..." }` |
```

---

## 分步工作流

### 步骤 1：编写规格说明

在发出任何实现请求之前，先把规格说明添加到 CLAUDE.md：

```markdown
## Feature: User Authentication

### Capabilities
- MUST: Email/password login
- MUST: JWT token generation
- MUST: Password hashing with bcrypt
- SHOULD: Remember me functionality
- MUST NOT: Store plain text passwords

### Tech Stack
- Required: bcrypt, jsonwebtoken
- Forbidden: passport.js (too heavy for this use case)

### Acceptance Criteria
- [ ] User can login with valid credentials
- [ ] Invalid credentials return 401
- [ ] Token expires after 24h (or 7d with remember me)
- [ ] Passwords hashed with cost factor 12
```

### 步骤 2：在提示词中引用规格说明

```
Implement the User Authentication feature as specified in CLAUDE.md.
Follow the acceptance criteria exactly.
```

Claude 会自动读取 CLAUDE.md 并遵循规格说明。

### 步骤 3：对照规格说明进行验证

实现完成后，进行验证：

```
Review the implementation against the User Authentication spec.
Check off each acceptance criterion that's satisfied.
List any gaps.
```

### 步骤 4：必要时更新规格说明

如果在实现过程中需求发生变化：

```
Update the User Authentication spec to include:
- MUST: Rate limiting (5 attempts per minute)
Then implement the rate limiting.
```

---

## 与工具集成

### 配合 Spec Kit（全新项目）

```bash
# Install Spec Kit
npx @anthropic/spec-kit init

# Use slash commands
/speckit.constitution  # Define project guardrails
/speckit.specify       # Write feature specs
/speckit.plan          # Create implementation plan
/speckit.implement     # Build from spec
```

### 配合 OpenSpec（既有项目）

```bash
# Install OpenSpec
npm install -g @fission-ai/openspec@latest
openspec init

# Use slash commands
/openspec:proposal "Add dark mode"  # Create change proposal
/openspec:apply add-dark-mode       # Implement changes
/openspec:archive add-dark-mode     # Merge to specs
```

### 配合 Plan Mode

```
[Press Shift+Tab to enter Plan Mode]

I need to implement the Payment Processing feature.
Review the spec in CLAUDE.md and create an implementation plan.
```

---

## 何时使用

### 使用规格优先（Spec-First）

| 场景 | 原因 |
|----------|-----|
| 新功能 | 在构建之前先定义 |
| API 设计 | 契约必须明确 |
| 架构决策 | 记录约束条件 |
| 团队协作 | 共享理解 |
| 复杂需求 | 减少歧义 |

### 跳过规格优先

| 场景 | 原因 |
|----------|-----|
| 快速修复 | 不值得为此付出额外开销 |
| 探索 | 还不清楚自己想要什么 |
| 原型开发 | 需求还会变化 |
| 单行改动 | 意图显而易见 |

---

## 反模式

### 含糊的规格说明

```markdown
# Wrong
## Feature: User Management
- Handle users

# Right
## Feature: User Management
### Capabilities
- MUST: Create user with email, password, name
- MUST: Update user profile (name, avatar)
- MUST: Soft delete (mark as inactive, don't remove data)
- MUST NOT: Allow duplicate emails
```

### 先写代码后补规格

```
# Wrong workflow
1. Ask Claude to implement feature
2. Write spec documenting what was built

# Right workflow
1. Write spec defining what should be built
2. Ask Claude to implement from spec
```

### 忽略禁用项

```markdown
# Don't forget exclusions
### Tech Stack
- Required: React, TypeScript
- Forbidden: jQuery, vanilla JS, class components
             ↑ These constraints prevent drift
```

---

## 模块化规格设计

**模式**：将大型规格拆分为多个聚焦的文件，而不是把所有内容塞进单个 CLAUDE.md。

### 问题：单体式 CLAUDE.md

当规格超过约 200 行时，会出现若干问题：

- **上下文污染**：Claude 难以从臃肿的上下文中提取相关信息
- **认知过载**：开发者无法快速扫读找到自己需要的内容
- **维护负担**：更新某一块内容需要在无关的章节之间穿梭
- **性能下降**：大型 CLAUDE.md 文件会拖慢上下文加载与处理

### 何时拆分

| 阈值 | 操作 |
|-----------|--------|
| **<100 行** | 单个 CLAUDE.md 即可 |
| **100-200 行** | 若存在不同领域，考虑拆分 |
| **>200 行** | **立即拆分** —— 你已经越过了认知负荷阈值 |
| **多团队项目** | 无论大小，都按领域/归属拆分 |

### 拆分策略

**1. 按功能拆分**

```
CLAUDE.md              # Core project context
CLAUDE-auth.md         # Authentication spec
CLAUDE-api.md          # API endpoints spec
CLAUDE-billing.md      # Payment processing spec
```

**2. 按角色拆分**

```
CLAUDE.md              # Shared conventions
CLAUDE-frontend.md     # UI/UX specifications
CLAUDE-backend.md      # API/database specs
CLAUDE-infra.md        # DevOps/deployment specs
```

**3. 按工作流拆分**

```
CLAUDE.md              # Daily development rules
CLAUDE-testing.md      # Test specifications
CLAUDE-release.md      # Release process spec
CLAUDE-security.md     # Security requirements
```

### 实现模式

**主 CLAUDE.md**（保持简洁）：
```markdown
# Project: [NAME]

## Tech Stack
[Core technologies]

## Commands
[Daily commands]

## Rules
[Universal rules]

## Detailed Specs
- Authentication: See @CLAUDE-auth.md
- API Design: See @CLAUDE-api.md
- Testing: See @CLAUDE-testing.md
```

**CLAUDE-auth.md**（聚焦的规格）：
```markdown
# Authentication Specification

## Capabilities
- MUST: JWT-based authentication
- MUST: Refresh token rotation
- MUST NOT: Store tokens in localStorage

## API Contract
[Detailed auth endpoints...]

## Security Requirements
[Specific auth security rules...]
```

**收益**：
- Claude 可以用 `@CLAUDE-auth.md` 引用特定文件
- 更快的上下文加载（仅相关规格）
- 更易维护（编辑某一领域而不影响其他领域）
- 更好的团队协作（每个规格文件有明确归属）

**来源**：Addy Osmani，["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/)（2026 年 1 月）

---

## 操作边界

**模式**：为 AI agents 明确界定哪些应自动执行、哪些应先询问、哪些绝不可碰。

### 三级体系

传统规格使用二元约束（MUST/MUST NOT），但操作性工作需要三个层级：

| 层级 | 含义 | Claude Code 对应 |
|------|---------|---------------------|
| **Always** | 无需询问，自动执行 | Auto-accept 模式 |
| **Ask First** | 在继续之前获得用户确认 | 默认模式 |
| **Never** | 阻止或要求进入 Plan Mode | Plan mode / Hook 阻止 |

### 操作边界模板

```markdown
## Boundaries

### Always (Auto-accept)
- Run tests after code changes
- Format code with Prettier
- Update imports when moving files
- Fix linting errors
- Add type annotations for untyped code

### Ask First (Confirm)
- Modify database schemas
- Add new dependencies
- Change API contracts
- Refactor >50 lines of code
- Update configuration files

### Never (Block)
- Push to production branch
- Commit secrets or API keys
- Delete data without backup
- Modify CI/CD workflows without review
- Bypass security checks
```

### 映射到 Claude Code 权限

**Always → 权限允许列表**：
```json
// In .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(npm test*)",
      "Bash(npx prettier*)",
      "Bash(npx tsc*)"
    ]
  }
}
```

**Ask First → 默认模式**：
- 标准行为，对每个操作进行提示
- 用于中等风险/影响的操作

**Never → Plan Mode + Hooks**：
```bash
# Hook configured via settings.json (PreToolUse event)
#!/bin/bash
if [[ "$TOOL_NAME" == "Bash" ]] && [[ "$INPUT" =~ "git push origin main" ]]; then
  echo "BLOCKED: Direct push to main blocked. Use feature branches."
  exit 2  # Send feedback to Claude (non-zero exit blocks the action)
fi
```

### 决策框架

针对每个操作问自己：
1. **它会导致数据丢失吗？** → Ask First 或 Never
2. **它能通过 git 还原吗？** → 也许可以 Always
3. **它会影响其他开发者吗？** → Ask First
4. **它是安全风险吗？** → Never
5. **它属于标准工作流的一部分吗？** → Always

### 示例：API 开发

```markdown
### Always
- Run unit tests (npm test)
- Validate request schemas
- Generate API documentation
- Check response formats

### Ask First
- Add new API endpoints
- Change existing endpoint signatures
- Modify authentication requirements
- Update rate limiting rules

### Never
- Expose internal endpoints publicly
- Log sensitive user data
- Disable authentication checks
- Remove rate limiting
```

### 维护

每季度审查边界：
- **提升**：从未引发问题的操作（Ask First → Always）
- **降级**：曾引发问题的操作（Always → Ask First）
- **阻止**：反复出现的错误（Ask First → Never）

**来源**：Addy Osmani，["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/)（2026 年 1 月）

---

## 命令规范模板

**模式**：用预期输出和错误处理来记录可执行命令。

### 为什么命令规范很重要

大多数规范聚焦于**功能**（"构建身份验证"），但**命令**（"如何测试身份验证"）对 AI 智能体来说同样关键。

### 模板结构

```markdown
## Commands

### [Command Category]

**Purpose**: [What this command accomplishes]

#### Command: `[actual command]`
**When**: [Trigger condition]
**Expected Output**: [What success looks like]
**Error Handling**: [What to do on failure]
**Flags**: [Important options]

---
```

### 示例：测试命令

```markdown
## Commands

### Testing

#### Command: `pnpm test`
**When**: Before every commit, after code changes
**Expected Output**:
- All tests pass (exit code 0)
- Coverage ≥80% (lines, branches, functions)
- No console warnings
**Error Handling**:
- If tests fail → Fix tests, don't skip
- If coverage drops → Add tests for uncovered code
- If warnings appear → Investigate before committing
**Flags**:
- `--coverage`: Generate coverage report
- `--watch`: Run in watch mode for development
- `--silent`: Suppress console output

#### Command: `pnpm test:e2e`
**When**: Before merging to main, in CI pipeline
**Expected Output**:
- All E2E scenarios pass
- Screenshots captured for failures
- Test duration <5 minutes
**Error Handling**:
- If flaky → Investigate race conditions, don't retry blindly
- If timeout → Check network mocks, async handling
- If screenshots differ → Review UI changes deliberately
**Flags**:
- `--headed`: Run with visible browser (debugging)
- `--project chromium`: Test specific browser
```

### 示例：构建与部署

```markdown
## Commands

### Build

#### Command: `pnpm build`
**When**: Before deployment, in CI pipeline
**Expected Output**:
- Build succeeds (exit code 0)
- Output in `dist/` directory
- No TypeScript errors
- Bundle size <500KB (main chunk)
**Error Handling**:
- If TypeScript errors → Fix types, don't use `@ts-ignore`
- If bundle too large → Analyze with `pnpm analyze`, code-split
- If missing assets → Check public/ directory, update paths
**Flags**:
- `--mode production`: Production optimizations
- `--analyze`: Generate bundle size report

### Deployment

#### Command: `pnpm deploy:staging`
**When**: After PR approval, before production
**Expected Output**:
- Deployment succeeds
- Health check returns 200 OK
- Staging URL: https://staging.example.com
**Error Handling**:
- If health check fails → Rollback automatically
- If database migration fails → Don't proceed, investigate
- If environment vars missing → Check .env.staging, update secrets
**Never**: Run `pnpm deploy:production` manually — use CI/CD only
```

### 示例：数据库命令

```markdown
## Commands

### Database

#### Command: `pnpm db:migrate`
**When**: After pulling schema changes, before development
**Expected Output**:
- Migrations applied successfully
- Database schema matches models
- Seed data loaded (development only)
**Error Handling**:
- If migration fails → Check database connection, review SQL
- If conflicts detected → Resolve migrations, don't force
**Never**: Run migrations in production manually — CI/CD only

#### Command: `pnpm db:reset`
**When**: Development only, never in staging/production
**Expected Output**:
- Database dropped and recreated
- All migrations applied
- Seed data loaded
**Error Handling**:
- If production check fails → Abort immediately, verify environment
**Safety**: Requires `NODE_ENV=development` check
```

### 与 CLAUDE.md 集成

在你的主 CLAUDE.md 中引用命令规范：

```markdown
## Commands
- Build: `pnpm build` (see spec for error handling)
- Test: `pnpm test` (must pass before commit)
- Deploy: See CLAUDE-deployment.md for full procedures
```

**来源**：Addy Osmani，["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/)（2026 年 1 月）

---

## 反模式：单体式 CLAUDE.md

### 问题所在

**症状**：你的 CLAUDE.md 已经膨胀到 300 多行，混杂了功能规范、API 契约、测试要求、部署流程和团队约定。

**影响**：
- **上下文低效**：即便面对简单任务，Claude 也会为每个请求加载全部 300 行
- **响应缓慢**：上下文越大，处理越慢
- **准确性下降**：重要细节淹没在噪声中
- **维护负担**：更新某一节时需要在不相关的内容里反复跳转
- **团队摩擦**：多名开发者编辑同一个文件 = 合并冲突

### 真实案例

**之前**（单体式）：
```markdown
# CLAUDE.md (387 lines)

## Tech Stack
[20 lines]

## Authentication
[45 lines of auth spec]

## API Endpoints
[67 lines of API contracts]

## Database Schema
[52 lines of schema rules]

## Testing
[38 lines of test requirements]

## Deployment
[41 lines of deployment procedures]

## Security Rules
[55 lines of security requirements]

## Team Conventions
[33 lines of coding standards]

## Git Workflow
[28 lines of branching rules]

## Troubleshooting
[8 lines of common issues]
```

**问题**：即便用户只是问"为用户资料添加一个新的 API 端点"，Claude 也会加载全部 387 行。

**之后**（模块化）：
```
CLAUDE.md (82 lines)          # Core context: tech stack, commands, rules
CLAUDE-auth.md (45 lines)     # Authentication spec only
CLAUDE-api.md (67 lines)      # API contracts only
CLAUDE-database.md (52 lines) # Database schema only
CLAUDE-testing.md (38 lines)  # Test requirements only
CLAUDE-deploy.md (41 lines)   # Deployment procedures only
CLAUDE-security.md (55 lines) # Security requirements only
```

**收益**：Claude 加载 CLAUDE.md（82 行）+ CLAUDE-api.md（67 行）= 149 行（减少 61%）

### 拆分策略

**第 1 步：识别领域**

在你的规范中寻找自然边界：
- 这些章节是否服务于不同目的？
- 不同章节是否会由不同团队成员负责？
- 某些章节是否比其他章节被引用得更频繁？

**第 2 步：抽取到聚焦文件**

将特定领域的内容移到专属文件：

```bash
# Keep in CLAUDE.md (always loaded)
- Tech stack (unchanging baseline)
- Daily commands (frequent reference)
- Universal rules (apply to all work)

# Extract to domain files (load on demand)
- Feature specs → CLAUDE-[feature].md
- API contracts → CLAUDE-api.md
- Testing → CLAUDE-testing.md
- Deployment → CLAUDE-deploy.md
```

**第 3 步：在主 CLAUDE.md 中创建索引**

```markdown
# Project: [NAME]

## 技术栈
[核心技术]

## 命令
[日常命令]

## 规则
[通用规则]

## 详细规格
针对特定领域的需求，请参考以下文件：
- @CLAUDE-auth.md — 身份认证与授权
- @CLAUDE-api.md — API 端点契约
- @CLAUDE-database.md — Schema 与迁移
- @CLAUDE-testing.md — 测试需求
- @CLAUDE-deploy.md — 部署流程
- @CLAUDE-security.md — 安全需求
```

**第 4 步：按需引用**

Claude 可以引用特定的文件：
```
User: "Add a new API endpoint for user settings"
Claude: Reads CLAUDE.md + @CLAUDE-api.md (relevant context only)
```

### 维护规则

1. **保持 CLAUDE.md 在 100 行以内**（仅核心上下文）
2. **每个领域文件控制在 150 行以内**（如果更大，则进一步拆分）
3. **每季度审查**：合并很少使用的文件，拆分频繁更新的章节
4. **使用 @file 引用**：显式加载你需要的内容

### 迁移检查清单

- [ ] 识别当前 CLAUDE.md 中的领域（超过 200 行？）
- [ ] 创建特定领域的文件（CLAUDE-[domain].md）
- [ ] 将内容迁移到聚焦的文件中
- [ ] 用索引/引用更新主 CLAUDE.md
- [ ] 测试：让 Claude 执行特定领域的任务
- [ ] 验证：用 `/status` 检查上下文使用情况
- [ ] 文档化：向团队说明新的结构

**来源**：Addy Osmani，["How to write a good spec for AI agents"](https://addyosmani.com/blog/good-spec/)（2026 年 1 月）

---

## SDD vs TDD vs BDD

截至 2026 年，规格驱动开发（spec-driven development）已经足够产品化，可以与更早的方法论进行有意义的对比。区别不在于抽象意义上哪种更好——而在于由哪个产物来主导。

| 方法论 | 主导产物 | 何时运行 | 人类角色 | 是否可重新生成？ |
|-------------|-------------------|--------------|------------|-----------------|
| TDD | 测试套件 | 在代码存在之后 | 先写测试，再写代码 | 否——测试记录的是已构建的内容 |
| BDD | Gherkin（.feature 文件） | 在代码存在之后 | 先写场景，再自动化 | 部分——场景可以驱动代码生成 |
| SDD | 规格文件（结构化的自然语言） | 在代码存在之前 | 写规格，批准契约 | 是——代码是规格的可推导产物 |

SDD 这一列的实际意义是：如果规格是主导产物，那么原则上代码可以从规格重新生成。Tessl 将这一点推向了逻辑上的极致，用 `// GENERATED FROM SPEC - DO NOT EDIT` 标记文件。Martin Fowler 指出这是 "spec-first"（代码从规格开始），但还不是 "spec-anchored"（规格和代码随时间自动保持同步）。还没有任何工具能在生产规模上可靠地解决规格漂移（spec drift）问题。

没有规格结构时多文件任务的失败率：对于多文件基础设施任务，pass@1 降至 19.4%，而独立函数则为 87%（Augment Code 内部数据，无公开的同行评审研究）。这个方向性的结论是可信的——缺乏持久任务上下文的 agent 在跨文件、跨组件的任务上失败得更频繁。具体的数字来自供应商。

### Factory.ai Missions 架构

这是生产环境中记录最完善的多 agent SDD 实现。架构如下：

1. **Orchestrator** 在任何实现开始之前，将需求翻译为行为验证契约。
2. **Workers** 并行实现各项功能，每个 worker 从契约中接收一份有界的任务描述。
3. **Validator agents**（对抗式、独立）针对契约验证每一项实现。它们没有来自 worker 的任何上下文——只有契约和输出。

在一个记录在案的 Slack 克隆项目中：validator 在任何代码合并之前捕获了 81 个问题，产生了占总实现工作量 34% 的"修复功能"。任务的中位时长：2 小时。记录在案的最长任务：16 天。Factory.ai 将状态外化到共享产物中（验证契约、功能列表、技能定义），以便在跨越多天的任务中熬过上下文重置。

CLI 参考（使用 Factory.ai 时）：

```bash
droid exec --mission path/to/mission.yaml    # Start a mission
droid status                                  # Check active missions
droid validate --mission-id <id>             # Run validators manually
```

### 规格漂移：尚未解决的难题

在生产环境中最重要的风险：当规格和代码出现分歧时，agent 会重新生成那些已经被修复的 bug。缓解模式：

- 在任何实现提交之前，将规格作为 git 产物进行版本化。
- Cursor `/evolve` 命令：当实现有意偏离规格时更新规格。
- Intent（agent）：在实现过程中将变更写回规格，使两者保持同步。
- GitHub Spec Kit：将规格存储在 `.specify/` 中，作为 CI 可以读取的版本化文件。

还没有任何工具拥有可靠的、被广泛采用的机制来在长时间尺度上实现自动化的规格-代码同步。截至 2026 年 5 月，这是 SDD 中首要的待解难题。

---

## 另见

- [../core/methodologies.md](../core/methodologies.md) — SDD 及其他方法论
- [Spec Kit 文档](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [OpenSpec 文档](https://github.com/Fission-AI/OpenSpec)
- [tdd-with-claude.md](./tdd-with-claude.md) — 与 TDD 结合
- [Spec-to-Code Factory](https://github.com/SylvainChabaud/spec-to-code-factory) — 完整的参考实现，带有工具化强制约束（通过 Node.js 实现 6 个 gate，"No Spec No Code" + "No Task No Commit" 不变式，约 900K tokens/项目）
- [Superpowers](https://github.com/obra/superpowers) — 插件套件（95k+ stars），带有一个 `brainstorming` 技能，将 spec-first 强制为一个必经的 gate：在规格被审查并批准之前，agent 拒绝编写代码。安装：`/plugin install superpowers@claude-plugins-official`。
