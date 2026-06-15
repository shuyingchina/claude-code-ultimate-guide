---
title: "Plan-Driven Development"
description: "Use /plan mode for non-trivial tasks to explore and propose implementation plans"
tags: [workflow, guide, architecture]
---

# 计划驱动开发

> **置信度**：Tier 1 — 基于 Claude Code 原生的 /plan 模式功能。

对任何非琐碎的任务都使用 `/plan` 模式。Claude 会以只读方式探索代码库，然后提出一份实现计划供你批准。

---

## 目录

1. [TL;DR](#tldr)
2. [/plan 工作流](#the-plan-workflow)
3. [何时使用](#when-to-use)
4. [计划文件结构](#plan-file-structure)
5. [与其他工作流集成](#integration-with-other-workflows)
6. [技巧](#tips)
7. [进阶：自定义 Markdown 计划（Boris Tane 模式）](#advanced-custom-markdown-plans-boris-tane-pattern)
8. [另请参阅](#see-also)

---

## TL;DR

```
1. Enter Plan Mode (Shift+Tab twice) or ask complex question
2. Claude explores codebase (read-only)
3. Claude writes plan to .claude/plans/
4. You review and approve
5. Claude executes
```

---

## /plan 工作流

### 第 1 步：进入 Plan Mode

用 `Shift+Tab` 切换 Plan Mode（按两次循环切换 Normal → Auto-Accept → Plan）：
```
# Press Shift+Tab twice to enter Plan Mode
# (Plan Mode indicator appears in the UI)
```

或者提出一个会自动触发计划模式的复杂问题：
```
How should I refactor the authentication system to support OAuth?
```

### 第 2 步：Claude 进行探索

在计划模式下，Claude 会：
- 读取相关文件
- 搜索模式
- 理解现有架构
- 无法做出任何更改

### 第 3 步：Claude 编写计划

Claude 会在 `.claude/plans/[name].md` 创建一个计划文件：

```markdown
# Plan: Refactor Authentication for OAuth

## Summary
Add OAuth support while maintaining existing email/password auth.

## Files to Modify
- src/auth/providers/index.ts (add OAuth provider)
- src/auth/middleware.ts (handle OAuth tokens)
- src/config/auth.ts (OAuth config)

## Files to Create
- src/auth/providers/oauth.ts
- src/auth/providers/google.ts

## Implementation Steps
1. Create OAuth provider interface
2. Implement Google OAuth provider
3. Update middleware to detect token type
4. Add OAuth routes
5. Update config schema

## Risks
- Breaking existing sessions during migration
- Token format differences between providers
```

### 第 4 步：你进行审查

审查计划的以下方面：
- 完整性（覆盖了所有需求）
- 正确性（适合你代码库的正确方法）
- 范围（没有过度设计）

### 第 5 步：批准并执行

```
Looks good. Proceed with the plan.
```

或者请求修改：
```
Modify the plan: also add support for GitHub OAuth, not just Google.
```

---

## 何时使用

### 使用 Plan Mode

| 场景 | 原因 |
|----------|-----|
| 多文件更改 | 预先看到所有受影响的文件 |
| 架构更改 | 在编码前验证方法 |
| 新功能 | 确保实现完整 |
| 不熟悉的代码库 | 让 Claude 先探索 |
| 高风险操作 | 在执行前审查 |

### 跳过 Plan Mode

| 场景 | 原因 |
|----------|-----|
| 单行修复 | 显而易见，风险低 |
| 拼写纠正 | 无需计划 |
| 简单问题 | 探索，而非实现 |
| 添加注释 | 琐碎的更改 |

---

## 计划文件结构

计划存储在 `.claude/plans/` 中，使用自动生成的名称。

### 典型的计划章节

```markdown
# Plan: [Title]

## Summary
[1-2 sentence overview]

## Context
[Why this change is needed]

## Files to Modify
[List of existing files that will change]

## Files to Create
[List of new files]

## Files to Delete
[List of files to remove, if any]

## Implementation Steps
[Ordered list of steps]

## Testing Strategy
[How to verify the changes]

## Risks & Mitigations
[What could go wrong and how to handle it]

## Open Questions
[Things to clarify before proceeding]
```

---

## 与其他工作流集成

### Plan + TDD

```
# Enter Plan Mode (Shift+Tab twice), then:

I need to implement a rate limiter.
Plan the test cases first, then the implementation.
```

Claude 会按照正确的 TDD 顺序同时规划测试和实现。

### Plan + Spec-First

```
# Enter Plan Mode (Shift+Tab twice), then:

Review the Payment Processing spec in CLAUDE.md.
Create an implementation plan that satisfies all acceptance criteria.
```

### Plan + Task Tool

计划批准后，Claude 可以将其拆解为任务：

```
Approved. Create tasks from this plan and start implementing.
```

---

## 技巧

### 明确界定范围

```
# Too vague (after entering Plan Mode via Shift+Tab twice)
Improve the API

# Better
Add pagination to the /users endpoint with cursor-based navigation.
Maintain backwards compatibility with existing clients.
```

### 请求修改计划

```
The plan looks good but:
- Add error handling for network failures
- Skip the caching optimization for now
- Include rollback procedure
```

### 用于架构决策

```
# Enter Plan Mode (Shift+Tab twice), then:

I'm considering two approaches for state management:
A) Redux Toolkit
B) Zustand

Explore the codebase and recommend which fits better.
```

### 保存计划作为文档

`.claude/plans/` 中的计划可作为决策文档：
- 为什么选择某些方案
- 预期会改动哪些文件
- 实施顺序的理由

---

## 进阶：自定义 Markdown 计划（Boris Tane 模式）

> **来源**：Boris Tane，Cloudflare 工程主管 ——《[How I use Claude Code](https://boristane.com/blog/how-i-use-claude-code/)》（2026 年 2 月）。9 个月的生产环境使用经验。
> **可信度**：第 2 级 —— 经实践者验证的模式，非 Anthropic 官方文档。

当 Plan Mode 还不够用时，可在编写任何代码之前进行人与 agent 的迭代式规划。

### 为什么用自定义计划而非 /plan

| 因素 | Plan Mode（原生） | 自定义 .md 计划 |
|--------|----------------|-----------------|
| **持久性** | 上下文 compaction 时丢失 | 在 compaction 后留存，可共享 |
| **评审界面** | 基于对话，线性 | 结构化文件，可做 diff |
| **迭代** | 在对话中来回交流 | 标注文件，重新运行 |
| **共享状态** | 每会话独立 | 人与 agent 之间的"共享可变状态" |
| **最适用于** | 标准功能，<30 分钟的任务 | 复杂功能、架构决策 |

**决策规则**：范围已明确时使用 Plan Mode（Shift+Tab 两次）。当你预料会出现误解，或希望在写下任何一行代码之前对方案做出明确确认时，使用自定义 `.md` 计划。

---

### 三阶段工作流

```
┌─────────────────────────────────────────────────────────────────┐
│  Phase 1: RESEARCH                                              │
│  → Emphatic prompt → research.md (written, not verbal)          │
├─────────────────────────────────────────────────────────────────┤
│  Phase 2: PLANNING (Annotation Cycle)                           │
│  → plan.md draft → human annotates → agent updates → repeat    │
│  → Exit: plan approved, no open questions                       │
├─────────────────────────────────────────────────────────────────┤
│  Phase 3: IMPLEMENTATION                                        │
│  → Mechanical execution, decisions already made                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 阶段 1：强调式研究

Claude 在没有强烈信号时只会浮于表面。使用强调性的措辞来迫使它深入：

```
Research the authentication system in this codebase deeply.
Understand the intricacies of how sessions are managed, in great detail.
Cover edge cases, existing patterns, and any non-obvious dependencies.

Write your findings to research.md — do not implement anything.
```

**为什么有效**："deeply"、"in great detail"、"intricacies" 会让 Claude 从表层扫描转向彻底调查。输出必须写入文件 —— 口头总结会在上下文 compaction 时消失。

**research.md 应包含**：
- 现有的模式与约定
- 文件路径与关键函数
- 不易察觉的依赖关系
- 识别出的约束与风险

---

### 阶段 2：标注循环

这是 Boris Tane 模式的核心。在**任何实现之前**，对 `plan.md` 反复迭代直至就绪。

```
┌──────────────────────────────────────────────────────────────┐
│                    ANNOTATION CYCLE                           │
│                                                              │
│  Human prompt ──→ Agent writes plan.md                       │
│       ↑                    ↓                                 │
│  Annotate plan    Human reviews plan.md                      │
│  (add comments,          ↓                                   │
│   ask questions,   Issues found?                             │
│   flag trade-offs)       ├─ Yes → Annotate → loop           │
│                          └─ No  → Approved → Phase 3        │
│                                                              │
│  Typical: 1-6 iterations before approval                     │
└──────────────────────────────────────────────────────────────┘
```

**护栏 prompt** —— 始终加上这一句以防止过早开始实现：

```
Based on research.md, write a plan for implementing [feature].

Include: approach, affected file paths, code snippets for key decisions,
trade-offs considered, and open questions.

Write to plan.md. Do NOT implement anything yet.
```

**plan.md 应包含的内容**：

```markdown
# Plan: [Feature Name]

## Approach
[Strategy and rationale]

## Files Affected
- path/to/file.ts — what changes and why
- path/to/other.ts — what changes and why

## Key Implementation Details
[Code snippets for non-obvious parts — not the full implementation]

## Trade-offs
- Option A vs B: chose A because X
- Considered but rejected: Y (reason)

## Open Questions
- [ ] Should we handle edge case Z?
- [ ] Does this affect the mobile client?
```

**标注示例**：

```markdown
## Approach
Use JWT tokens stored in httpOnly cookies.
<!-- Human annotation: ✓ Agreed. But also consider refresh token rotation -->

## Open Questions
- [ ] Should we handle token expiry in middleware?
<!-- Human annotation: Yes, centralize this — don't leave it to each route -->
```

**退出条件** —— 当满足以下条件时计划即就绪：
- 没有遗留的待决问题
- 权衡已记录并达成一致
- 文件路径是具体的（不是"某个 auth 文件"）
- 关键代码片段展示了方案，而非仅作描述

> "这个 markdown 文件充当你与 agent 之间的共享可变状态。" —— Boris Tane

---

### 阶段 3：机械式实现

一旦计划获批，实现就变成纯粹的执行 —— 不再有需要创造性判断的决策。

```
Implement everything in plan.md.
Work through each item sequentially.
Mark tasks as completed as you go with [x].
Do not stop between tasks to ask for confirmation — keep going until done.
```

**实现过程中的反馈**：
- 保持简洁：用短语或截图，而非长段落
- 决策已经做出 —— 把范围变更重新引导回 plan.md
- 如果出现意外情况：暂停，更新 plan.md，再继续

**心态转变**：阶段 3 是机械化的。所有思考都已在阶段 2 完成。

---

### 互补技巧

| 技巧 | 是什么 | 何时使用 |
|-----------|------|------|
| **Cherry-picking（择优实现）** | 实现 plan.md 的一个子集 | 计划过大，需要增量交付 |
| **Scope trimming（范围精简）** | 实现前从计划中删除条目 | 降低风险，聚焦核心 |
| **Reference-based guidance（基于参照的指引）** | 指向现有代码："do it like auth.ts" | 强制保持一致性 |
| **Revert & re-scope（回退并重新界定范围）** | `git revert` + 以更窄的计划重新开始 | 计划走偏了，干净地重置 |

---

## 参见

- [exploration-workflow.md](./exploration-workflow.md) — 在规划之前探索多种方案
- [../ultimate-guide.md](../ultimate-guide.md) — 第 2.3 节 Plan Mode
- [tdd-with-claude.md](./tdd-with-claude.md) — 与 TDD 结合使用
- [spec-first.md](./spec-first.md) — 与 Spec-First 结合使用
- [iterative-refinement.md](./iterative-refinement.md) — 规划后的迭代
- [task-management.md](./task-management.md) — 使用 Tasks API 跨会话追踪计划执行
- [dual-instance-planning.md](./dual-instance-planning.md) — 进阶：使用两个 Claude 实例（planner + implementer）实现注重质量的工作流
