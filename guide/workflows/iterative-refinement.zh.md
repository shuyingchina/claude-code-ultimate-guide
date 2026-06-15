---
title: "Iterative Refinement"
description: "Prompt, observe, and reprompt until satisfied — the core loop of AI-assisted development"
tags: [workflow, guide, design-patterns]
---

# 迭代式精炼

> **可信度**：Tier 2 — 在众多 Claude Code 用户中观察到的已验证模式。

提示、观察、再提示，直到满意为止。这是高效 AI 辅助开发的核心循环。

---

## 目录

1. [TL;DR](#tldr)
2. [循环](#the-loop)
3. [反馈模式](#feedback-patterns)
4. [自主循环](#autonomous-loops)
5. [与 Claude Code 集成](#integration-with-claude-code)
6. [脚本生成工作流](#script-generation-workflow)
7. [迭代策略](#iteration-strategies)
8. [反模式](#anti-patterns)
9. [社区模式与已知限制](#community-patterns--known-limitations)
10. [另请参阅](#see-also)

---

## TL;DR

```
1. Initial prompt with clear goal
2. Claude produces output
3. Evaluate against criteria
4. Specific feedback: "Change X because Y"
5. Repeat until done
```

关键要点：**具体的反馈 > 模糊的反馈**

---

## 循环

### 第 1 步：初始提示

从清晰的意图和约束开始：

```
Create a React component for a user profile card.
- Show avatar, name, bio
- Include edit button
- Use Tailwind CSS
- Mobile-responsive
```

### 第 2 步：评估输出

Claude 生成代码。评估：
- 它是否满足需求？
- 缺少了什么？
- 哪里出错了？
- 哪里可以做得更好？

### 第 3 步：具体反馈

提供有针对性的修正：

```
Good start. Changes needed:
1. Avatar should be circular, not square
2. Edit button should only show for own profile (add isOwner prop)
3. Bio should truncate after 3 lines with "Show more"
```

### 第 4 步：重复

持续迭代直到满意：

```
Better. One more thing:
- Add loading skeleton state for when data is fetching
```

---

## 反馈模式

### 有效的反馈

| 模式 | 示例 |
|---------|---------|
| **具体定位** | "Line 23: change `===` to `==`" |
| **明确的动作** | "Add error boundary around the form" |
| **给出原因** | "Remove the console.log because it leaks user data" |
| **标注优先级** | "Critical: fix the SQL injection. Nice-to-have: add pagination." |

### 无效的反馈

| 反模式 | 为何失败 | 更好的替代方案 |
|--------------|--------------|-------------------|
| "Make it better" | 没有方向 | "Improve readability by extracting the validation logic" |
| "This is wrong" | 没有细节 | "The date format should be ISO 8601, not Unix timestamp" |
| "I don't like it" | 主观 | "Use functional components instead of class components" |
| "Fix the bugs" | 太模糊 | "Fix: 1) null check on line 12, 2) off-by-one in loop" |

---

## 自主循环

Claude 可以在明确的完成标准下进行自我迭代。

### Ralph Wiggum 模式

得名于这种自我改进的循环模式：

```
Keep improving the code quality until:
1. All tests pass
2. No TypeScript errors
3. ESLint shows zero warnings

After each iteration, run the checks and fix any issues.
Stop when all criteria are met.
```

### 完成标准示例

```
Iterate until:
- Response time < 100ms for 95th percentile
- Test coverage > 80%
- All accessibility checks pass
- Bundle size < 200KB
```

### 迭代上限

始终设置上限以防止无限循环：

```
Improve the algorithm performance.
Maximum 5 iterations.
Stop early if improvement < 5% between iterations.
```

---

## 与 Claude Code 集成

### 配合 Task 工具

使用 `TaskCreate` 和 `TaskUpdate` 跟踪精炼迭代：

```
TaskCreate: "Implement initial version"
TaskCreate: "Fix: handle empty arrays"
TaskCreate: "Fix: add input validation"
TaskCreate: "Optimization: memoize expensive calculations"
# Mark completed as you progress with TaskUpdate
```

### 配合 Hooks

使用 Claude Code hooks（通过 `/hooks` 命令或 `settings.json` 配置）在每次更改后自动校验。例如，针对 `Edit` 工具的 `PostToolUse` hook 可以自动运行 linting 和测试。Claude 看到失败信息后可以自我纠正。

### 配合 /compact

当迭代过程中上下文不断增长时：

```
/compact

Continue refining the search algorithm.
We've made good progress, focus on the remaining issues.
```

### 检查点（Checkpointing）

在取得显著进展后：

```
Good progress. Let's checkpoint:
- Commit what we have
- List remaining issues
- Continue with the next priority
```

---

## 脚本生成工作流

脚本和自动化生成为迭代式精炼带来了最高的投资回报率——在实践者的报告中可节省 70-90% 的时间。脚本是自包含的，可以独立测试，并能立即产生价值。

### 3-7 次迭代模式

大多数生产就绪的脚本会在 3-7 次迭代后成型：

| 迭代 | 重点 | 提示模式 |
|-----------|-------|----------------|
| 1 | 基础功能 | "Create a script that [goal]" |
| 2-3 | 约束 + 边缘情况 | "Add [constraint]. Handle [edge case]." |
| 4-5 | 加固 | "Add error handling, logging, input validation" |
| 6-7 | 打磨 | "Optimize for [metric]. Add usage docs." |

### 示例：Kubernetes Pod 管理器（PowerShell）

**迭代 1 — 基础**
```
Create a PowerShell function to list pods in a Kubernetes namespace.
```

**迭代 2 — 添加过滤**
```
Add: filter by label selector and pod status.
Show: pod name, status, age, restarts.
```

**迭代 3 — 添加操作**
```
Add: ability to delete pods matching filter.
Require: confirmation before deletion.
```

**迭代 4 — 错误处理**
```
Handle: kubectl not found, invalid namespace, permission denied.
Add: verbose logging with -Verbose flag.
```

**迭代 5 — 生产就绪**
```
Add: dry-run mode, output to JSON for piping, help documentation.
Ensure: works on Windows, Linux, macOS.
```

### 常见陷阱

| 陷阱 | 示例 | 缓解措施 |
|---------|---------|------------|
| 幻觉命令 | 在 macOS 上使用 `apt-get` | 指定操作系统："Ubuntu 22.04 only" |
| 安全漏洞 | 没有输入校验 | 始终要求："validate all user inputs" |
| 过度工程 | 添加不必要的库 | 要求："minimal dependencies, stdlib preferred" |
| 上下文漂移 | 在第 5 次迭代后忘记需求 | 检查点提示："Recap current requirements before next change" |
| 平台假设 | 在 sh 中假设有 bash 特性 | 指定："POSIX-compliant" 或 "bash 4+" |

### 脚本迭代模板

```
Current script: [paste or reference]

Iteration goal: [specific improvement]

Constraints:
- Must preserve: [existing behavior to keep]
- Must not: [things to avoid]
- Target environment: [OS, shell, runtime]

Success criteria: [how to verify this iteration works]
```

---

## 迭代策略

### 广度优先

在深入之前，先修复同一层级的所有问题：

```
First pass: Fix all type errors
Second pass: Fix all lint warnings
Third pass: Improve test coverage
Fourth pass: Optimize performance
```

### 深度优先

在转向下一个领域之前，先彻底完成一个领域：

```
1. Perfect the authentication flow (all aspects)
2. Then move to user management
3. Then move to settings
```

### 基于优先级

按重要性逐一处理：

```
Iterate in this order:
1. Security issues (critical)
2. Data integrity bugs (high)
3. UX problems (medium)
4. Code style (low)
```

---

## 反模式

### 移动靶标

```
# Wrong
"Actually, let's change the approach entirely..."
(Repeated 5 times)

# Right
Commit to an approach, iterate within it.
If approach is wrong, explicitly restart.
```

### 完美主义循环

```
# Wrong
Keep improving forever

# Right
Set clear "good enough" criteria:
- Tests pass
- Handles main use cases
- No critical issues
→ Ship it, improve later
```

### 上下文丢失

```
# Wrong
After 50 iterations, forget what the goal was

# Right
Periodically restate the goal:
"Reminder: we're building a rate limiter.
Current state: basic implementation works.
Next: add Redis backend."
```

---

## 评审自我修正循环

这是一种专门用于代码评审的迭代模式，Claude 评审 → 修复 → 再评审，直到收敛。

### 模式

```
┌─────────────────────────────────────────┐
│   Review Auto-Correction Loop           │
│                                          │
│   Review (identify issues)               │
│        ↓                                 │
│   Fix (apply corrections)                │
│        ↓                                 │
│   Re-Review (verify fixes)               │
│        ↓                                 │
│   Converge (minimal changes) → Done      │
│        ↑                                 │
│        └──── Repeat (max iterations)     │
└─────────────────────────────────────────┘
```

### 提示词模板

```
Review this PR with auto-correction:
1. Multi-agent review (3 scope-focused agents)
2. Fix all 🔴 Must Fix issues
3. Re-review to verify fixes didn't introduce new issues
4. Fix all 🟡 Should Fix issues
5. Re-review one final time
6. Stop when only 🟢 Can Skip remain

Max iterations: 3
Stop early if iteration produces <5 lines changed
```

### 安全防护

| 安全防护 | 目的 | 实现方式 |
|-----------|---------|----------------|
| **最大迭代次数** | 防止无限循环 | 硬性限制：3 次迭代 |
| **质量门禁** | 确保修复有效 | 每次迭代前运行 `tsc && lint` |
| **受保护文件** | 防止有风险的改动 | 跳过对以下文件的自动修复：package.json、migrations、.env |
| **变更阈值** | 在收敛时停止 | 若某次迭代改动 <5 行则退出 |
| **回滚能力** | 从糟糕的修复中恢复 | 每次迭代前进行 Git 提交 |

### 示例会话

**迭代 1：初次评审**
```
Claude: Found 8 issues:
- 🔴 3 Must Fix (SQL injection, empty catch, missing auth)
- 🟡 4 Should Fix (DRY violations, N+1 query)
- 🟢 1 Can Skip (naming style)
```

**迭代 2：修复 Must Fix + 再评审**
```
Claude: Fixed 3 Must Fix issues.
Re-review: All 🔴 resolved. No new issues introduced.
Remaining: 4 🟡 Should Fix, 1 🟢 Can Skip
```

**迭代 3：修复 Should Fix + 再评审**
```
Claude: Fixed 4 Should Fix issues.
Re-review: All 🟡 resolved. No new issues.
Remaining: 1 🟢 Can Skip (optional improvement)
```

**收敛**
```
Claude: Converged. Only optional improvements remain.
Changes this iteration: 2 lines (below threshold).
Review complete. ✅
```

### 对比：单遍评审 vs 收敛循环

| 方面 | 单遍评审 | 收敛循环 |
|--------|-----------------|------------------|
| **问题检测** | 一次性找出所有问题 | 找出问题 → 修复 → 验证 → 重复 |
| **后续感知** | 检查 git log 中的 "Co-Authored-By: Claude" | 每次迭代都感知上一次的结果 |
| **误报** | 可能为已修复的代码再次建议修复 | 再评审能捕捉到这一点 |
| **置信度** | 单次验证 | 多遍验证 |
| **时间成本** | 最快（1 次评审） | 较慢（3+ 次评审） |
| **质量** | 适合经验丰富的开发者 | 更适合关键代码 |

**何时使用**：
- **单遍评审**：简单的 PR、经验丰富的团队、时间紧迫
- **收敛循环**：安全关键代码、初级团队、高风险生产环境

### 与多 agent 评审集成

将收敛循环与多 agent 评审结合，以获得最高质量：

```
Each iteration:
├─ Agent 1: Consistency Auditor
├─ Agent 2: SOLID Principles Analyst
└─ Agent 3: Defensive Code Auditor
     ↓
  Fix issues
     ↓
  Re-run 3 agents
     ↓
  Verify fixes + check for new issues
     ↓
  Repeat until convergence
```

### 收敛标准

当以下任一条件为真时停止迭代：

1. **没有剩余问题**（理想结果）
2. **达到最大迭代次数**（默认 3 次迭代）
3. **变更阈值**（某次迭代改动 <5 行）
4. **质量门禁失败**（修复后 tsc/lint 失败）
5. **手动停止**（用户请求中止）

### 评审循环中的反模式

| 反模式 | 问题 | 解决方案 |
|--------------|---------|----------|
| **无限循环** | 没有收敛标准 | 设定最大迭代次数 + 变更阈值 |
| **范围蔓延** | 每次迭代都新增需求 | 在开始循环前锁定范围 |
| **破坏性修复** | 修复引入新 bug | 每次修复后再评审 + 质量门禁 |
| **受保护文件改动** | 修改 package.json、migrations | 为受保护文件设置明确的跳过列表 |
| **上下文丢失** | 在第 3 次迭代后忘记最初的问题 | 跨迭代维护一个问题追踪器 |

---

## 示例会话

### 初始请求
```
Create a debounce function in TypeScript.
```

### 迭代 1
```
Looks good. Add:
- Generic type support for any function signature
- Option to execute on leading edge
```

### 迭代 2
```
Better. Issues:
- The return type should preserve the original function's return type
- Add cancellation support
```

### 迭代 3
```
Almost there. Final polish:
- Add JSDoc comments
- Export the types separately
- Add unit tests
```

### 完成
```
Perfect. Commit this as "feat: add debounce utility with full TypeScript support"
```

---

## 社区模式与已知限制

社区在 Claude Code 的迭代循环之上构建了若干模式。有些解决了真实的痛点，另一些则暴露了当前值得了解的限制。

### Ralph Loop（测试驱动的自主迭代）

来源：nathanonn.com，2026 年 2 月。

Ralph Loop 将自主迭代约束为每个周期只处理一个测试用例，而不是每次都运行整个测试套件。这让每个周期保持专注，避免 agent 同时追逐多个失败。

工作原理：

1. 选取一个失败的测试用例
2. 修复它，验证它通过
3. 将进度保存到一个 JSON 状态文件
4. 移动到下一个失败的测试用例
5. 对同一个用例尝试 3 次失败后，将其标记为 `known_issue` 并跳过

```json
{
  "current_case": "test_auth_token_refresh",
  "attempts": 2,
  "known_issues": ["test_legacy_migration_edge_case"],
  "completed": ["test_login", "test_logout", "test_session_timeout"]
}
```

状态文件是这里的关键创新。它能在上下文重置、`/compact` 操作，乃至完整的会话重启后依然存续。agent 在每个周期开始时读取该文件，从而准确知道上次停在哪里、哪些用例已完成、哪些需要跳过。

3 次尝试上限避免了困扰朴素自主循环的无限循环陷阱。与其在一个顽固的测试用例上耗费 token，agent 会继续前进，并标记该问题留待人工后续审查。

### Auto-Continue Skill

来源：mcpmarket.com。

一个基于置信度的续行系统，用于决定 agent 应当继续还是停下来等待人工输入。它不采用固定的迭代次数，而是在每个周期后评估当前情况：

**在以下情况自动续行**：
- 测试通过
- 构建成功
- 未检测到新的错误类型
- 置信度分数保持在阈值之上

**在以下情况停下等待人工输入**：
- 置信度降至阈值以下
- 出现一类新的错误（而不仅仅是已知错误的新实例）
- 构建或类型检查以 agent 此前未见过的方式失败

这与 Claude Code 的 Stop hooks 配合得很好。该 skill 可以触发任务后验证，并根据结果决定是否恢复。

### 用于自动验证的 Stop Hooks

一种将 Claude Code 的 hook 系统变为迭代之间自动质量门禁的模式：

1. Claude 完成一项任务（或一次迭代）
2. 一个作用于 `TodoWrite` 的 `PostToolUse` hook 触发验证脚本
3. 脚本运行类型检查、lint 和测试
4. 错误被自动回传给 Claude
5. Claude 在无人工干预的情况下修复问题

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "TodoWrite",
        "command": "bash -c 'npm run typecheck 2>&1; npm run lint 2>&1; npm test 2>&1'"
      }
    ]
  }
}
```

每当 Claude 把一项任务标记为完成时，这个 hook 就会触发。如果验证发现了问题，Claude 会看到输出，并能在进入下一个任务前自我纠正。

### 升级策略

当同一个问题上 3 次迭代都失败时该怎么办。与其永远循环或直接放弃，不如遵循一条结构化的升级路径：

1. **拆解**：将失败的任务拆成 2-3 个可以独立处理的更小子任务
2. **收集上下文**：把所有错误消息、堆栈跟踪和尝试过的修复方案转储到一个结构化文件中
3. **模型升级**：如果在用 Sonnet，就用 Opus 重试这个具体的失败用例，以获得更深入的推理
4. **人工升级**：如果升级模型也无济于事，则创建一个 GitHub issue，附上完整的错误上下文，并把任务标记为 `known_issue`

```bash
# Escalation in practice
if [ "$ATTEMPT_COUNT" -ge 3 ]; then
    # Collect context
    cat errors.log attempts.log > escalation-context.md

    # Try with Opus
    claude --model claude-opus-4-6 \
        "Fix this failing test. Context: $(cat escalation-context.md)"

    # If still failing, create issue
    if [ $? -ne 0 ]; then
        gh issue create \
            --title "Auto-escalation: $TEST_NAME fails after 3 attempts" \
            --body "$(cat escalation-context.md)" \
            --label "known_issue,needs-human"
    fi
fi
```

目标永远是不要悄无声息地丢弃工作。每一次失败要么被解决，要么被升级，要么被明确追踪。

### 已知限制

诚实面对目前还行不通的地方，这样你就不会浪费时间去重新发明那些尚不存在的解决方案。

**没有内置的 retry/verify/resume**（GitHub issue #28489）：Claude Code 中的无头自动化缺乏对重试逻辑、验证门禁和会话恢复的原生支持。每个实现自主循环的团队都得自己造一套这样的东西。状态文件、基于 hook 的验证和升级脚本，全都是社区针对平台这一空白的变通方案。

**Agent 迭代可能丢失**（GitHub issue #28843）：在跨越多天的工作流中，agent 的迭代及其累积的上下文可能被销毁。如果你正在运行一个横跨多个会话或多天的工作流，请每隔 N 次迭代保存一次明确的状态文件。不要把 Claude 的对话记忆当作你唯一的真相来源。

**多天工作流的脆弱性**：长时间运行的自动化需要检查点纪律。定期将状态保存到磁盘（JSON 文件、git 提交、issue 评论）。这个模式很简单却容易被遗忘：如果你无法仅凭磁盘上的文件重建 agent 的进度，你的工作流就会在会话边界处崩溃。

---

## 另见

- [exploration-workflow.md](./exploration-workflow.md) — 在迭代之前先探索备选方案
- [tdd-with-claude.md](./tdd-with-claude.md) — TDD 就是带测试的迭代式精炼
- [plan-driven.md](./plan-driven.md) — 迭代之前先做计划
- [../core/methodologies.md](../core/methodologies.md) — 迭代循环方法论
