---
title: "Task Management Workflow"
description: "Multi-session task coordination using Tasks API and TodoWrite for complex projects"
tags: [workflow, guide, agents]
---

# 任务管理工作流

**版本**：Claude Code v2.1.16+
**前置条件**：理解多会话工作流，具备基本的 CLI 操作能力
**耗时**：学习需 15-30 分钟，适用于所有复杂项目

## 概述

Claude Code 的任务管理在 v2.1.16 中迎来重大演进，引入了 **Tasks API**，与最初的 **TodoWrite** 工具形成互补。本工作流将教你何时使用各个系统，以及如何在复杂项目中利用多会话任务协调能力。

**何时使用此工作流：**
- 跨越多个编码会话的项目
- 多 agent 协调场景
- 带依赖关系的复杂任务层级
- 需要在上下文 compact 或会话中断后恢复工作

**何时不要使用：**
- 单会话、直截了当的实现
- 快速修复或探索性编码
- 10 分钟以内即可完成的任务

---

## 系统对比速查

| 特性 | TodoWrite（旧版） | Tasks API（v2.1.16+） |
|---------|-------------------|---------------------|
| **持久化** | 仅会话内存 | 磁盘存储（`~/.claude/tasks/`） |
| **多会话** | ❌ 会话结束即丢失 | ✅ 跨会话保留 |
| **依赖关系** | ❌ 手动排序 | ✅ 任务阻塞（A 阻塞 B） |
| **协调** | 单 agent | ✅ 多 agent 并支持广播 |
| **状态跟踪** | pending/in_progress/completed | pending/in_progress/completed |
| **何时使用** | 简单的单会话待办事项 | 复杂的多会话项目 |

**迁移标志**（v2.1.19+）：
```bash
# Use old system (TodoWrite)
CLAUDE_CODE_ENABLE_TASKS=false claude

# Use new system (Tasks API) - default since v2.1.19
claude
```

---

## 工作流阶段 1：任务规划

**目标**：将复杂工作分解为可跟踪、可执行的单元

### 步骤 1：分析范围

在创建任务之前，先理解你要构建的内容：

```bash
# Discovery pattern
claude
> "Analyze this codebase for implementing JWT authentication:
  - Glob for existing auth patterns
  - Grep for security-related code
  - Identify integration points"
```

### 步骤 2：设计任务层级

将工作拆分为带依赖关系的逻辑阶段：

**示例：认证系统**
```
Authentication System (parent)
├── 1. Login endpoint (no dependencies)
├── 2. Token refresh (depends on #1)
├── 3. Logout endpoint (depends on #1)
└── 4. Integration tests (depends on #1, #2, #3)
```

### 步骤 3：创建任务结构

使用 `TaskCreate` 将你的计划具体化：

```bash
# Session 1: Planning phase
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude

# Inside Claude session:
> "Create a task hierarchy for JWT authentication:

  Parent task: 'Implement JWT authentication system'
  - Description: Add JWT-based auth with refresh tokens and secure storage

  Child tasks:
  1. 'Create login endpoint' (no dependencies)
  2. 'Implement token refresh logic' (depends on task 1)
  3. 'Create logout endpoint' (depends on task 1)
  4. 'Write integration tests' (depends on tasks 1, 2, 3)

  Use TaskCreate with proper metadata."
```

**Claude 的预期输出：**
```json
{
  "tasks": [
    {
      "id": "task-auth-parent",
      "title": "Implement JWT authentication system",
      "status": "pending",
      "children": ["task-login", "task-refresh", "task-logout", "task-tests"]
    },
    {
      "id": "task-login",
      "title": "Create login endpoint",
      "status": "pending",
      "dependencies": [],
      "metadata": {"priority": "high", "estimated_duration": "2h"}
    },
    {
      "id": "task-refresh",
      "title": "Implement token refresh logic",
      "status": "pending",
      "dependencies": ["task-login"],
      "metadata": {"priority": "high", "estimated_duration": "1h"}
    }
    // ... other tasks
  ]
}
```

---

## 工作流阶段 2：任务执行

**目标**：系统化地执行任务并跟踪进度

### 执行模式

```
TaskList → TaskGet (next pending) → Execute → TaskUpdate → Validate → Repeat
```

### 步骤 1：发现下一个任务

```bash
# Session 2: Start implementation
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude

> "TaskList to show all pending tasks"
```

**输出：**
```
Tasks for 'auth-system-v2':
✅ task-login: Create login endpoint [completed]
⏳ task-refresh: Implement token refresh logic [pending, blocked by: none]
⏳ task-logout: Create logout endpoint [pending, blocked by: none]
⏳ task-tests: Write integration tests [pending, blocked by: task-refresh, task-logout]
```

### 步骤 2：获取任务详情

```bash
> "TaskGet task-refresh to see full requirements"
```

**输出：**
```json
{
  "id": "task-refresh",
  "title": "Implement token refresh logic",
  "description": "Create endpoint POST /auth/refresh that validates refresh token and issues new access token",
  "status": "pending",
  "dependencies": ["task-login"],
  "metadata": {
    "priority": "high",
    "estimated_duration": "1h",
    "files": ["src/auth/refresh.ts", "src/middleware/auth.ts"]
  }
}
```

### 步骤 3：执行并更新

```bash
> "Mark task-refresh as in_progress, then implement the token refresh endpoint according to requirements"

# Claude executes: TaskUpdate task-refresh status=in_progress
# Claude implements the feature...
# Upon completion:

> "Mark task-refresh as completed"
# Claude executes: TaskUpdate task-refresh status=completed
```

### 步骤 4：验证

```bash
> "Run tests for token refresh functionality"

# If tests pass:
# ✅ Task remains completed

# If tests fail:
> "TaskUpdate task-refresh status=in_progress, add error details to metadata and fix issues"
```

---

## 工作流阶段 3：会话管理

**目标**：在不同会话和上下文边界之间无缝恢复工作

### 持久化机制

**存储位置**：`~/.claude/tasks/<task-list-id>/`

任务可以在以下情况下保留：
- 会话终止
- 上下文压缩（`/compact`）
- 系统重启
- 多日的中断

#### ⚠️ 字段可见性限制

**TaskList 仅返回**：`id`、`subject`、`status`、`owner`、`blockedBy`

**TaskList 输出中缺失的字段**：
- `description`（需要对每个任务调用 TaskGet）
- `metadata`（自定义字段，如优先级、估算）
- `activeForm`（进度指示器文本）

**工作流调整**：

```bash
# DON'T: Assume you can scan all descriptions
TaskList  # Shows subjects only

# DO: Fetch selectively
TaskList                    # Get overview (which tasks exist, statuses)
TaskGet(task-auth-login)    # Get full details for specific task
TaskGet(task-auth-tests)    # Get details for next task
```

**何时需要关注这一点**：
- 任务描述详尽的复杂项目（每个任务 >50 个词）
- 需要共享上下文可见性的多智能体协调
- 需要快速浏览所有任务备注以决定恢复点

**成本意识**：
- TaskList = 1 次 API 调用
- 为 N 个任务获取描述 = 1 + N 次调用
- 对于 20 个任务，如果你需要全部描述，开销将是 20 倍

**缓解措施**：
- 将关键信息放入 `subject` 字段（在 TaskList 中可见）
- 保持 `description` 简洁（最多 50-100 个词）
- 将详细计划存储在 markdown 文件中（`docs/plan-*.md`）

### 恢复模式

```bash
# Days later, different terminal session
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude

> "TaskList to show current state"

# Output shows exactly where you left off:
# ✅ task-login [completed]
# ✅ task-refresh [completed]
# ⏳ task-logout [pending]
# ⏳ task-tests [pending, blocked by: task-logout]

> "Continue with next pending task that isn't blocked"
```

### 多终端协调

**使用场景**：运行多个 Claude 实例在同一项目上工作

```bash
# Terminal 1: Frontend work
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude
> "Work on task-logout endpoint"

# Terminal 2: Test writing (simultaneous)
export CLAUDE_CODE_TASK_LIST_ID="auth-system-v2"
claude
> "TaskList - check what's completed so I can write tests"

# Both terminals see real-time state updates
```

**⚠️ 警告**：使用特定于仓库的任务列表 ID，以避免跨项目污染：
```bash
# ❌ BAD: Generic ID used across multiple repos
export CLAUDE_CODE_TASK_LIST_ID="my-project"

# ✅ GOOD: Repo-specific with context
export CLAUDE_CODE_TASK_LIST_ID="mycompany-api-auth-refactor"
```

---

## 集成：TDD + 任务管理

将测试驱动开发与任务跟踪相结合，以实现系统化的测试覆盖。

### 模式：测试优先的任务执行

```bash
export CLAUDE_CODE_TASK_LIST_ID="tdd-feature-x"
claude

# Create tasks with test-first approach
> "Create task hierarchy for feature X:

  For each feature component:
  1. Task: 'Write failing tests for [component]'
  2. Task: 'Implement [component] to pass tests' (depends on #1)
  3. Task: 'Refactor [component]' (depends on #2)

  Use TDD red-green-refactor cycle per task."
```

### 示例：使用 TDD 的登录功能

```bash
# Phase 1: Red (failing tests)
TaskCreate: {
  title: "Write failing tests for login endpoint",
  description: "Test cases: valid credentials, invalid password, user not found, rate limiting",
  status: "pending"
}

# Execute test writing
> "Implement task-login-tests, ensure all tests fail initially"

# Phase 2: Green (minimal implementation)
TaskCreate: {
  title: "Implement login endpoint (minimal)",
  description: "Make tests pass with simplest possible implementation",
  dependencies: ["task-login-tests"],
  status: "pending"
}

# Phase 3: Refactor
TaskCreate: {
  title: "Refactor login endpoint",
  description: "Optimize, remove duplication, improve readability",
  dependencies: ["task-login-impl"],
  status: "pending"
}
```

**完整工作流参考**：参见 [TDD with Claude](tdd-with-claude.md#task-management-integration)

---

## 集成：计划驱动 + 任务管理

将战略计划转换为可执行的任务层级结构。

### 模式：计划到任务的转换

```bash
# Step 1: Enter plan mode
claude
> [Press Shift+Tab to enter Plan Mode]

# Step 2: Create architectural plan
> "Design architecture for microservices migration:
  - Identify service boundaries
  - Plan data migration strategy
  - Design API contracts"

# Step 3: Exit plan mode with task creation
> "Convert this plan into a task hierarchy using TaskCreate"
```

### 示例：微服务迁移

**计划输出：**
```
Phase 1: Analysis (Week 1)
- Map monolith dependencies
- Identify bounded contexts
- Design service boundaries

Phase 2: Infrastructure (Week 2)
- Set up service templates
- Configure API gateway
- Establish monitoring

Phase 3: Migration (Week 3-6)
- Extract user service
- Extract order service
- Migrate database schemas
```

**任务转换：**
```bash
TaskCreate: {
  title: "Microservices migration",
  children: [
    {
      title: "Phase 1: Analysis",
      children: [
        {title: "Map monolith dependencies", priority: "critical"},
        {title: "Identify bounded contexts", dependencies: ["map-deps"]},
        {title: "Design service boundaries", dependencies: ["bounded-contexts"]}
      ]
    },
    {
      title: "Phase 2: Infrastructure",
      dependencies: ["phase-1"],
      children: [
        {title: "Set up service templates"},
        {title: "Configure API gateway", dependencies: ["templates"]},
        {title: "Establish monitoring"}
      ]
    }
    // ... Phase 3
  ]
}
```

**完整工作流参考**：参见 [Plan-Driven Development](plan-driven.md#task-hierarchy-design)

---

## TodoWrite 迁移指南

### 何时迁移

**继续使用 TodoWrite，如果：**
- ✅ 所有工作都在单次会话中完成
- ✅ 不需要多 agent 协作
- ✅ 简单的线性任务列表（无依赖关系）
- ✅ 使用的 Claude Code 版本 < v2.1.16

**迁移到 Tasks API，如果：**
- ✅ 工作跨越多次会话
- ✅ 需要任务在数天/数周内持久化
- ✅ 复杂的依赖关系图
- ✅ 多终端协作
- ✅ 希望在上下文 compact 后恢复工作

### 迁移步骤

#### 步骤 1：识别 TodoWrite 的使用

```bash
# Find existing TodoWrite usage in your CLAUDE.md or workflows
grep -r "TodoWrite" .claude/
```

#### 步骤 2：将 TodoWrite 列表转换为 Tasks

**之前（TodoWrite）：**
```markdown
- [ ] Implement user authentication
- [ ] Add password hashing
- [ ] Create session management
- [ ] Write tests
```

**之后（Tasks API）：**
```bash
export CLAUDE_CODE_TASK_LIST_ID="user-auth-2026"
claude

> "Create tasks:
  1. 'Implement user authentication' (parent)
     - Child: 'Add password hashing'
     - Child: 'Create session management' (depends on hashing)
     - Child: 'Write tests' (depends on auth, hashing, sessions)"
```

#### 步骤 3：更新 CLAUDE.md 指令

**之前：**
```markdown
For complex tasks:
- Use TodoWrite to create task list
- Execute tasks sequentially
```

**之后：**
```markdown
For complex tasks:
- Set CLAUDE_CODE_TASK_LIST_ID=<project-name>
- Use TaskCreate for hierarchical planning
- Execute with TaskUpdate status tracking
- Resume with TaskList in new sessions
```

#### 步骤 4：测试迁移

```bash
# Create test task list
export CLAUDE_CODE_TASK_LIST_ID="migration-test"
claude

> "Create 3 test tasks with dependencies, mark one completed, then exit"

# Relaunch in new session
export CLAUDE_CODE_TASK_LIST_ID="migration-test"
claude

> "TaskList - verify tasks persisted correctly"

# Expected: See all 3 tasks with correct states
```

---

## 模式与反模式

### ✅ 良好模式

#### 1. 分层任务分解

```bash
Project (parent)
└── Feature A (child of project)
    ├── Component A1 (child of Feature A)
    │   ├── Implementation (leaf task)
    │   └── Tests (leaf task, depends on Implementation)
    └── Component A2
        └── ...
```

**为何有效**：贴合自然的项目结构，使依赖关系显式化

#### 2. 依赖优先排序

```bash
# Always define dependencies when creating tasks
TaskCreate: {
  title: "Deploy to production",
  dependencies: ["run-tests", "code-review", "backup-database"],
  metadata: {blocking_reason: "Safety checks required"}
}
```

**为何有效**：防止过早执行，强制实施质量关卡

#### 3. 细粒度状态更新

```bash
# Bad: Large task marked completed without intermediate updates
TaskCreate: {title: "Build entire auth system"}
# ... hours later ...
TaskUpdate: {id: "auth-system", status: "completed"}

# Good: Frequent status updates as work progresses
TaskUpdate: {id: "auth-system", status: "in_progress", progress: "25%"}
TaskUpdate: {id: "auth-system", status: "in_progress", progress: "50%"}
TaskUpdate: {id: "auth-system", status: "in_progress", progress: "75%"}
TaskUpdate: {id: "auth-system", status: "completed"}
```

**为何有效**：提供可见性，支持上下文感知的恢复

#### 4. 元数据丰富的任务

```bash
TaskCreate: {
  title: "Optimize database queries",
  description: "Reduce query time for user dashboard from 2s to <200ms",
  metadata: {
    priority: "high",
    estimated_duration: "3h",
    related_files: ["src/db/queries.ts", "src/db/indexes.sql"],
    performance_baseline: "2000ms",
    performance_target: "200ms",
    related_issue: "https://github.com/org/repo/issues/123"
  }
}
```

**为何有效**：上下文丰富的恢复、更易于委派、更好的文档记录

### ❌ 反模式

#### 1. 单体式任务（>10 个步骤）

```bash
# ❌ BAD: Task too large, hard to track progress
TaskCreate: {
  title: "Implement entire payment system",
  description: "Stripe integration, webhooks, refunds, disputes, reporting, admin UI, ..."
}

# ✅ GOOD: Break into phases
TaskCreate: {
  title: "Payment system - Phase 1: Core integration",
  children: [
    {title: "Stripe SDK setup"},
    {title: "Payment intent creation"},
    {title: "Webhook handling"}
  ]
}
```

#### 2. 缺失依赖关系

```bash
# ❌ BAD: Tasks can execute in wrong order
TaskCreate: {title: "Deploy to production"} # No dependencies
TaskCreate: {title: "Write tests"} # No dependencies

# ✅ GOOD: Explicit ordering
TaskCreate: {
  title: "Deploy to production",
  dependencies: ["write-tests", "run-tests", "code-review"]
}
```

#### 3. 缺乏上下文的孤立任务

```bash
# ❌ BAD: Future you won't remember what this means
TaskCreate: {
  title: "Fix the bug",
  description: "That one from yesterday"
}

# ✅ GOOD: Self-contained context
TaskCreate: {
  title: "Fix login timeout on Safari",
  description: "Users on Safari 17.2+ experience session timeout after 5min. Expected: 30min timeout. Root cause: cookie SameSite=Strict not supported.",
  metadata: {
    browser: "Safari 17.2+",
    error_message: "Session expired",
    related_commit: "a1b2c3d",
    slack_thread: "https://slack.com/archives/C123/p456"
  }
}
```

#### 4. 状态不一致

```bash
# ❌ BAD: Task marked completed but tests fail
TaskUpdate: {id: "login-feature", status: "completed"}
# Tests run later: 3 failures

# ✅ GOOD: Validation before completion
> "Run tests for login feature"
# If tests pass:
TaskUpdate: {id: "login-feature", status: "completed", metadata: {test_results: "pass"}}
# If tests fail:
TaskUpdate: {id: "login-feature", status: "in_progress", metadata: {test_results: "3 failures", error_log: "..."}}
```

---

## 故障排查

### Q：任务无法跨会话持久化

**症状**：重启 Claude 后 `TaskList` 显示为空

**解决方案**：
```bash
# Ensure CLAUDE_CODE_TASK_LIST_ID is set before launching
export CLAUDE_CODE_TASK_LIST_ID="your-project-name"
claude

# Verify storage directory exists
ls ~/.claude/tasks/your-project-name/
```

### Q：多个项目共享任务列表

**症状**：在项目 B 中工作时看到来自项目 A 的任务

**原因**：在不同的仓库之间使用了相同的任务列表 ID

**解决方案**：
```bash
# Use repo-specific IDs with context
cd ~/projects/api
export CLAUDE_CODE_TASK_LIST_ID="api-v2-migration"
claude

cd ~/projects/frontend
export CLAUDE_CODE_TASK_LIST_ID="frontend-redesign"
claude
```

### Q：仍在使用 TodoWrite 而非 Tasks API

**症状**：即使设置了任务列表 ID，任务仍无法持久化

**原因**：环境中设置了 `CLAUDE_CODE_ENABLE_TASKS=false`

**解决方案**：
```bash
# Check environment
env | grep CLAUDE_CODE_ENABLE_TASKS

# Unset if present
unset CLAUDE_CODE_ENABLE_TASKS

# Or explicitly enable (v2.1.19+ defaults to enabled)
export CLAUDE_CODE_ENABLE_TASKS=true
```

### Q：任务依赖未被强制执行

**症状**：Claude 在依赖完成之前就执行了被阻塞的任务

**原因**：在 TaskCreate 中未正确定义依赖

**解决方案**：
```bash
# Ensure dependencies use correct task IDs
TaskCreate: {
  title: "Task B",
  dependencies: ["task-a-id"], # ✅ Use actual task ID
  # NOT dependencies: ["Task A"] # ❌ Task title won't work
}

# Verify dependencies:
TaskGet task-b-id
# Should show: "blockedBy": ["task-a-id"]
```

---

## 进阶：自定义任务元数据

使用领域特定的元数据扩展任务，以增强工作流。

### 元数据约定

**性能优化任务：**
```json
{
  "metadata": {
    "type": "performance",
    "baseline_metric": "2000ms",
    "target_metric": "200ms",
    "profiling_tool": "Chrome DevTools",
    "measurement_location": "dashboard load time"
  }
}
```

**安全任务：**
```json
{
  "metadata": {
    "type": "security",
    "severity": "critical",
    "cve_id": "CVE-2024-1234",
    "affected_versions": "< 2.1.0",
    "mitigation": "Update package X to v3.0+"
  }
}
```

**缺陷修复任务：**
```json
{
  "metadata": {
    "type": "bugfix",
    "issue_url": "https://github.com/org/repo/issues/456",
    "reported_by": "user@example.com",
    "reproduction_steps": "1. Login 2. Navigate to dashboard 3. Click export",
    "error_message": "TypeError: Cannot read property 'map' of undefined"
  }
}
```

### 按元数据查询

```bash
# Filter tasks by type (requires scripting, not built-in)
TaskList | jq '.tasks[] | select(.metadata.type == "security")'

# Find high-priority pending tasks
TaskList | jq '.tasks[] | select(.metadata.priority == "high" and .status == "pending")'
```

---

## 会话生命周期协议

每个 agent 会话都遵循相同的十步序列，从启动到提交。明确定义这些步骤、而不是让它们隐式存在，正是让会话在中断后能够可靠恢复的关键。Anthropic 自己的工程团队直接观察到了这一点：在一次游戏编辑器实验中，一次裸跑的 Claude 在中途失败，而将同样的工作负载包裹在结构化会话 harness 中则成功完成（来源：[Anthropic Engineering Blog](https://www.anthropic.com/engineering/harness-design-long-running-apps)）。

| 步骤 | 操作 | 产物 |
|------|--------|----------|
| START | 阅读项目指令 | `AGENTS.md` 或 `CLAUDE.md` |
| INIT | 运行环境引导 | `init.sh` / `npm install && npm run check` |
| READ | 加载上一次会话状态 | `progress.md` |
| SELECT | 选定一个功能，将状态设为 active | `feature_list.json` |
| EXECUTE | 仅实现该功能 | 源文件 |
| VERIFY | 运行三层验证（lint、tests、e2e） | 退出码 |
| WRAP UP | 记录完成情况与证据 | `progress.md`、`feature_list.json` |
| CLEANUP | 删除临时文件，验证仓库能干净地重新启动 | 仓库状态 |
| COMMIT | 在 git 中标记会话边界 | Git 历史 |
| HANDOFF | 编写或更新交接说明 | `claudedocs/handoffs/` |

### 连续性产物：`progress.md`

`progress.md` 是让 READ 步骤在数秒而非数分钟内完成的文件。它位于项目根目录，保持在 50 行以内，并且是为下一次 agent 会话而写的，而非为人类审阅者而写。这个区别很重要。交接文档（WRAP UP 和 HANDOFF 步骤）在设计上就是详尽的：它告诉人类发生了什么、为什么做出这些决策、以及需要注意什么。`progress.md` 做的事情则更狭窄。它记录当前活跃的功能 ID、最后一次提交的哈希、任何当前的阻塞项，以及 agent 应采取的唯一下一步操作。没有散文，没有叙述。

```markdown
# Session Progress

last_updated: 2026-05-04
active_feature: feat-002
last_commit: a3f92c1
session_count: 3

## Status
- feat-001: passing (verified 2026-05-01)
- feat-002: active (in progress)
- feat-003: not_started

## Next action
Finish chunking implementation, then run: npm test -- --grep 'chunking'

## Blockers
None
```

下一次会话在 READ 步骤读取此文件，接手 `active_feature: feat-002`，检查最后一次提交的哈希以在 git 历史中定位自己，然后直接转入下一步操作。无需冷启动的背景介绍。

### 它如何与交接三件套协同

本工作流前文记录的交接三件套模式（创建、恢复、更新）与 `progress.md` 服务于阅读同一会话边界的不同受众。`progress.md` 为 agent 提供机器可读的起点。交接文档为人类审阅者提供关于改动内容及原因的叙述性记录。两者互不替代，并且在同一步骤（WRAP UP）中更新，从而无需额外开销即可保持同步。

### 作为会话边界的 COMMIT 步骤

COMMIT 步骤的一次提交不仅仅是一次 VCS 操作。它是对仓库处于可重启状态的一种断言。规则与交接三件套相同：只有在功能完成并通过验证时才提交。一个处于破损状态、仅实现了一半的功能，意味着下一次会话将以一个破损的环境开始，并且 INIT 步骤的 `npm run check` 会立即失败，在任何新工作开始之前就暴露出问题。这种失败是有信息量的，但更好的做法是通过将提交保留到 VERIFY 步骤干净通过为止来预防它。

关于跳过 VERIFY 步骤时出现的失败模式，参见 [tdd-with-claude.md](tdd-with-claude.md#the-verification-gap) 中的「验证缺口」（The Verification Gap）。

---

## 相关工作流

- **[与 Claude 进行 TDD](tdd-with-claude.md)** —— 结合任务追踪的测试先行开发
- **[计划驱动开发](plan-driven.md)** —— 从战略规划到任务层级
- **[迭代式精炼](iterative-refinement.md)** —— 结合任务的增量改进
- **[探索工作流](exploration-workflow.md)** —— 创建任务之前的发现阶段

---

## 参考

**工具文档**：参见 [终极指南第 5.X 节](#task-management-system)

**来源：**
- 官方：[Claude Code CHANGELOG v2.1.16](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- 官方：[System Prompts - TaskCreate](https://github.com/Piebald-AI/claude-code-system-prompts)
- 社区：[paddo.dev - From Beads to Tasks](https://paddo.dev/blog/from-beads-to-tasks/)
- 社区：[llbbl.blog - Two Changes in Claude Code](https://llbbl.blog/2026/01/25/two-changes-in-claude-code.html)

**版本追踪**：本工作流记录的是 Claude Code v2.1.16+（发布于 2026-01-22）。请在 [claude-code-releases.yaml](../../machine-readable/claude-code-releases.yaml) 中核对最新变更。
