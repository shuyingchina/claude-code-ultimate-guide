---
title: "RPI: Research → Plan → Implement"
description: "A 3-phase feature development pattern with explicit validation gates between phases"
tags: [workflow, architecture, design-patterns, validation]
---

# RPI: Research → Plan → Implement

> **置信度**: Tier 2 — 综合自生产团队的实践模式。这种基于关卡（gate）的结构与 Anthropic 在 agent 任务分解和 agentic 循环控制方面的指导一致。

通过三个锁定的阶段构建功能：先研究可行性，再规划实现方案，最后编写代码。每个阶段都产出一个具体的产物。每个关卡都需要明确的 GO（放行）后才能进入下一阶段。

---

## 目录

1. [TL;DR](#tldr)
2. [何时使用 RPI](#when-to-use-rpi)
3. [关卡的运作方式](#how-the-gates-work)
4. [阶段 1：Research（研究）](#phase-1-research)
5. [阶段 2：Plan（规划）](#phase-2-plan)
6. [阶段 3：Implement（实现）](#phase-3-implement)
7. [Slash 命令模板](#slash-command-templates)
8. [实战示例](#worked-example)
9. [与其他工作流的对比](#comparison-to-other-workflows)
10. [技巧与排障](#tips-and-troubleshooting)
11. [另请参阅](#see-also)

---

## TL;DR

```
Phase 1 — Research:
  Claude explores feasibility, surfaces risks, asks decision questions
  Output: RESEARCH.md
  Gate: You decide GO / NO-GO

Phase 2 — Plan:
  Claude writes architecture decisions, user stories, test plan
  Output: PLAN.md
  Gate: You approve the plan before any code is written

Phase 3 — Implement:
  Claude implements step by step, tests pass before each next step
  Output: working code + passing tests
  Gate: each implementation step validated before the next begins
```

**最适合**：可行性不明确的功能、需要超过一天工作量的功能、未知的技术领域，或任何"晚期才发现错误假设代价高昂"的场景。

---

## 何时使用 RPI

### 在以下情况使用 RPI

- **可行性未知**：你有一个想法，但不确定它在技术上是否站得住脚
- **范围较大**：实现工作量超过一天
- **需求模糊**：你知道想要的结果，但不知道达成的路径
- **走错方向的风险高**：安全、支付、数据迁移、与外部系统的集成
- **你以前被坑过**：一个看起来简单的功能，结果牵涉到另外 6 个系统

### 在以下情况跳过 RPI

| 场景 | 更优做法 |
|----------|----------------|
| 修复显而易见（拼写错误、颜色不对） | 直接编辑 |
| 功能已被充分理解，需求清晰 | [Spec-First](./spec-first.md) 或 [dual-instance](./dual-instance-planning.md) |
| 探索模式——你还不知道自己想要什么 | 探索式工作流 |
| 微小改动，单个文件 | 直接动手 |

### 决策启发法

问问自己："如果研究阶段揭示出一个严重问题，我会庆幸自己没有先花 2 天去实现吗？"

如果会，那就运行 RPI。研究阶段通常需要 30-60 分钟，却能省下许多小时。

---

## 关卡的运作方式

RPI 有两个人工关卡，外加每个实现步骤的一个自动关卡。

```
[Idea]
   |
   v
[Phase 1: Research]
   |
   +- NO-GO -> Stop. Document why. Archive RESEARCH.md.
   |
   +- GO -------------------------------------------------------->
                                                                 |
                                                       [Phase 2: Plan]
                                                                 |
                                          +- Needs revision -> iterate with Claude
                                          |
                                          +- Approved -------------------------------->
                                                                                      |
                                                                          [Phase 3: Implement]
                                                                              Step 1 -> Test gate
                                                                              Step 2 -> Test gate
                                                                              Step 3 -> Test gate
                                                                                   |
                                                                                [Done]
```

**关卡 1（Research 之后）**：你阅读 RESEARCH.md 并做出 GO/NO-GO 决定。这是最重要的关卡——它能彻底防止构建错误的东西。

**关卡 2（Plan 之后）**：在编写任何代码之前，你审阅 PLAN.md。小幅修订在此处以零成本完成。

**步骤关卡（Implement 期间）**：每个实现步骤都必须先通过测试，Claude 才能进入下一步。这是自动的，除非某个步骤失败，否则无需人工介入。

---

## 阶段 1：Research（研究）

### 研究涵盖的内容

研究阶段回答五个问题：

1. **已经存在什么？** 相关代码、库、代码库中过往的尝试
2. **需要构建什么？** 范围边界、需创建 vs 需修改的组件
3. **有哪些风险？** 技术、安全、集成、性能
4. **有哪些决策点？** 影响整个计划的架构选择
5. **工作量估算是多少？** 在投入计划之前的粗略估量

Claude 探索代码库、阅读相关文件、检查依赖项，并暴露任何会改变计划的约束。其结果是 RESEARCH.md。

### 启动研究

创建功能文件夹并发起研究：

```bash
mkdir -p .claude/features/[feature-name]
```

然后在 Claude 中：

```
/rpi:research [feature description]
```

或者不使用 slash 命令：

```
Run RPI Phase 1 (Research) for: [feature description]

Save output to .claude/features/[feature-name]/RESEARCH.md
Use Plan Mode to explore without modifying code.
```

### RESEARCH.md 模板

```markdown
# Research: [Feature Name]

**Date**: [YYYY-MM-DD]
**Requested**: [One-sentence description of the feature]
**Status**: PENDING DECISION

---

## What Exists Today

### Relevant Code
- [file path]: [what it does, why it matters]
- [file path]: [what it does, why it matters]

### Relevant Libraries
- [library]: [currently used / available / needs to be added]

### Prior Attempts or Related Work
- [any existing partial implementation, related PR, note in codebase]

---

## What Needs to Be Built

### New Files
- [file path]: [purpose]
- [file path]: [purpose]

### Files to Modify
- [file path]: [what changes, why]

### External Dependencies
- [dependency]: [reason needed, version constraint if any]

---

## Risks

| Risk | Likelihood | Impact | Notes |
|------|-----------|--------|-------|
| [risk description] | Low/Med/High | Low/Med/High | [mitigation or blocker] |

---

## Architecture Decision Points

Questions that need a decision before planning can start:

1. **[Decision]**: Option A (pros: X, cons: Y) vs Option B (pros: X, cons: Y)
2. **[Decision]**: [Options and trade-offs]

---

## 工作量估算

- 调研到计划：[time]
- 实现：[time range]
- 测试：[time]
- **总估算**：[range]

**估算置信度**：低 / 中 / 高
**原因**：[reason for confidence level]

---

## 建议

[GO / NO-GO / NEEDS CLARIFICATION]

[用 1-3 句话解释该建议]

---

**决策**：[ ] GO  [ ] NO-GO  [ ] NEEDS CLARIFICATION
**备注**：[human fills this in]
```

### NO-GO 是什么样的

并非每个调研阶段都以 GO 结束。常见的 NO-GO 原因：

- **技术阻碍**：外部 API 不支持所需的操作
- **发现范围蔓延**："简单功能"结果需要重写认证层
- **存在更好的替代方案**：调研发现了一个现成的库或配置更改，能更简单地解决问题
- **当前风险过高**：功能本身合理，但时机不对

归档 NO-GO 调研文档——它们是关于所做决策及其原因的宝贵记录。

---

## 阶段 2：计划

### 计划涵盖的内容

只有在你将 RESEARCH.md 标记为 GO 之后，阶段 2 才会开始。Claude 阅读调研文档，并生成一份精确的实现计划。

一份好的计划应足够具体，使得另一位工程师（或处于新会话中的 Claude）无需提问即可执行。

```
/rpi:plan .claude/features/[feature-name]/RESEARCH.md
```

或者不使用 slash command：

```
Run RPI Phase 2 (Plan) using:
- Research: .claude/features/[feature-name]/RESEARCH.md

Save output to .claude/features/[feature-name]/PLAN.md
Do not write any code yet. Plan only.
```

### PLAN.md 模板

```markdown
# Plan: [Feature Name]

**Date**: [YYYY-MM-DD]
**Research**: [link to RESEARCH.md]
**Estimated effort**: [from research]
**Risk level**: Low / Medium / High

---

## Summary

[2-4 sentences: what this implements, major design decisions taken, what it does NOT include]

---

## Architecture Decisions

[Record decisions made from the research decision points]

1. **[Decision]**: Chose [Option] because [reason]
2. **[Decision]**: Chose [Option] because [reason]

---

## Implementation Steps

Steps must be sequential and independently testable.

### Step 1: [Name]

**Files**: [list of files to create or modify]
**What to build**: [precise description]
**Test gate**: [specific test or check that must pass before Step 2 starts]

### Step 2: [Name]

**Files**: [list of files to create or modify]
**What to build**: [precise description]
**Test gate**: [specific test or check that must pass before Step 3 starts]

[...continue for all steps]

---

## Success Criteria

- [ ] [Testable criterion — describes observable behavior, not implementation]
- [ ] [Testable criterion]
- [ ] All step test gates pass

---

## Out of Scope

Explicitly list what this plan does NOT cover:
- [thing excluded]
- [thing excluded]

---

## Risks Accepted

[From RESEARCH.md risks, list which are accepted and how they're mitigated]

---

## Rollback Plan

If implementation fails mid-way:
- [what to undo]
- [how to restore previous state]

---

**Plan approved?** [ ] YES — proceed to implementation
**Revision notes**: [human fills this in if changes needed]
```

### 审查计划

在批准之前，请仔细阅读 PLAN.md。目标是现在就发现设计问题，而不是在实现期间才发现。需要具体检查的事项：

- 实现步骤的顺序正确，没有隐藏的依赖关系
- 测试关卡是具体且可运行的（而非"看起来对"）
- 范围之外的内容是明确列出的（防止 Claude 过度构建）
- 任何涉及数据或共享状态的部分都有回滚计划

如果计划需要更改，请让 Claude 在批准前先行修订。这是免费的——批准之后再修订则要付出实现的时间成本。

---

## 阶段 3：实现

### 步骤关卡模式

实现是逐步进行的。每个步骤都有一个测试关卡。在当前关卡通过之前，Claude 不会开始下一个步骤。

```
/rpi:implement .claude/features/[feature-name]/PLAN.md
```

或者不使用 slash command：

```
Run RPI Phase 3 (Implement) using:
- Plan: .claude/features/[feature-name]/PLAN.md

Rules:
- Implement one step at a time
- After each step, run the test gate specified in the plan
- Do not start the next step until the test gate passes
- If a test gate fails, stop and report the failure — do not improvise a fix
- Commit after each step that passes its gate
```

### 实现期间会发生什么

Claude 按顺序执行计划中的各个步骤。对于每个步骤：

1. 实现指定的文件和更改
2. 运行测试关卡（单元测试、集成检查或手动验证）
3. 如果关卡通过：提交一条引用该步骤的提交信息，并宣布已准备好进入下一步
4. 如果关卡失败：报告失败情况、具体的测试输出以及可能的原因。除非你确认，否则不会尝试修复。

步骤-提交模式为你提供了一份与计划相对应的清晰 git 历史。如果第 4 步出了问题，你可以干净利落地回滚到第 3 步的提交。

### 步骤关卡失败协议

当测试关卡失败时，Claude 会报告：

```
Step [N] gate failed.

Gate: [what was supposed to pass]
Output:
[actual test output]

Likely cause: [Claude's diagnosis]
Options:
1. Fix: [specific change that would likely fix it]
2. Revise plan: [if the plan step itself has a flaw]
3. Stop and investigate: [if the failure reveals something unexpected]

Which should I do?
```

由你来决定。Claude 不会自动修复并继续推进——那正是实现偏离计划的根源。

---

## Slash Command 模板

将这些保存到 `.claude/commands/`，即可直接调用每个阶段。

### `/rpi:research`

保存到 `.claude/commands/rpi-research.md`：

```markdown
# RPI Phase 1: Research

Run feasibility research for the requested feature.

## Instructions

1. Enter Plan Mode (do not modify files during research)
2. Explore the codebase to answer these questions:
   - What already exists that's relevant?
   - What files will need to change or be created?
   - What are the technical risks?
   - What decisions need to be made before planning?
   - What is a rough effort estimate?
3. Save output to `.claude/features/$ARGUMENTS/RESEARCH.md` using the template below
4. End with a clear recommendation: GO, NO-GO, or NEEDS CLARIFICATION
5. Ask the user for their GO/NO-GO decision before proceeding

## Constraints

- Do NOT write any code
- Do NOT modify any files
- Do NOT start planning implementation steps
- If uncertain about scope, surface it as a decision point
```

### `/rpi:plan`

保存到 `.claude/commands/rpi-plan.md`：

```markdown
# RPI Phase 2: Plan

Create an implementation plan based on approved research.

## Pre-check

Before starting:
1. Read the RESEARCH.md file specified in $ARGUMENTS
2. Verify it has a GO decision marked
3. If no GO decision found, stop and ask the user to decide first

## Instructions

1. Read RESEARCH.md carefully
2. Create PLAN.md in the same feature folder
3. Architecture decisions: resolve all decision points from research
4. Implementation steps: each step must have a concrete test gate
5. Success criteria: observable, testable, not implementation-internal
6. Out-of-scope: explicit list of what this plan does NOT cover
7. Do NOT write any implementation code
8. After writing the plan, ask the user to review and approve

## Constraints

- Do NOT write implementation code
- Steps must be sequential and independently testable
- Test gates must be runnable commands or precise manual checks, not vague descriptions
- Each step should be achievable in a single focused session
```

### `/rpi:implement`

保存到 `.claude/commands/rpi-implement.md`：

```markdown
# RPI Phase 3: Implement

Implement the feature following an approved plan, one step at a time.

## Pre-check

Before starting:
1. Read the PLAN.md file specified in $ARGUMENTS
2. Verify it has an approval marked
3. If no approval found, stop and ask the user to approve first

## Instructions

For each step in the plan:
1. Read the step description carefully
2. Implement only what the step specifies — nothing more
3. Run the test gate exactly as written in the plan
4. If the gate passes:
   - Commit with message: "feat([feature]): step [N] — [step name]"
   - Announce step completion and readiness for next step
5. If the gate fails:
   - Report the exact failure output
   - Diagnose the likely cause
   - Present options (fix, revise plan, stop)
   - Wait for human decision before proceeding

## Constraints

- Never skip a test gate
- Never start the next step before the current gate passes
- Never modify files outside the scope of the current step
- If you encounter something unexpected that changes the plan, stop and report it
- Commit after each passing step — not at the end
```

---

## 完整示例

**需求**："为公开 API 端点添加限流（rate limiting）。"

### 阶段 1：研究产出（节选）

```markdown
# Research: API Rate Limiting

**Date**: 2026-03-12
**Status**: PENDING DECISION

## What Exists Today

- `src/middleware/` — has auth middleware, no rate limiting
- `package.json` — express-rate-limit not installed, redis available
- `src/routes/api.ts` — 14 public endpoints, unauthenticated routes mixed with authenticated ones

## What Needs to Be Built

- Rate limiter middleware for public endpoints
- Separate limits for authenticated vs unauthenticated users
- Redis store for distributed rate limiting (app runs on 3 instances)

## Risks

| Risk | Likelihood | Impact | Notes |
|------|-----------|--------|-------|
| Redis connection failure disables all API access | Low | High | Need fallback to in-memory if Redis unavailable |
| Rate limit too aggressive — breaks existing integrations | Medium | High | Need to survey current usage patterns first |

## Architecture Decision Points

1. **Library**: express-rate-limit (maintained, battle-tested) vs custom middleware
2. **Bypass for trusted IPs**: Allow internal services to bypass rate limiting?

## Effort Estimate

- Implementation: 2-4 hours
- Testing: 2 hours
- **Total**: 4-6 hours

**Recommendation**: GO — standard problem, good library options, main risk is Redis fallback which is solvable.
```

**人工决策**：GO。使用 express-rate-limit。暂不设置 IP 绕过。

### 阶段 2：计划（节选）

```markdown
# Plan: API Rate Limiting

**Risk level**: Medium (shared Redis state, potential to block legitimate traffic)

## Architecture Decisions

1. Library: express-rate-limit with rate-limit-redis store
2. No IP bypass initially — revisit if internal service issues arise
3. Unauthenticated: 100 requests/15 minutes. Authenticated: 1000 requests/15 minutes.
4. Redis failure fallback: in-memory store (accepts single-instance inconsistency)

## Implementation Steps

### Step 1: Install dependencies and configure Redis store

**Files**: `package.json`, `src/config/rate-limit.ts`
**Test gate**: `npm install` completes, `src/config/rate-limit.ts` exports config without errors

### Step 2: Implement rate limiter middleware

**Files**: `src/middleware/rate-limit.ts`
**Test gate**: Unit test — limiter blocks 101st request from same IP within 15 minutes

### Step 3: Apply to routes

**Files**: `src/routes/api.ts`
**Test gate**: Integration test — unauthenticated route returns 429 after 100 requests; authenticated route does not

### Step 4: Add Redis fallback

**Files**: `src/config/rate-limit.ts`
**Test gate**: Test with Redis unavailable — API still responds (200, not 500), in-memory limiting active
```

**人工审查**：已批准。

### 阶段 3：实现

Claude 实现 Step 1，运行测试关卡（`npm install` + 导入检查），提交 `feat(rate-limit): step 1 — dependencies and config`。然后依次进行 Step 2、Step 3、Step 4。每次提交都很干净。每个关卡都必须通过后才能继续。

---

## 与其他工作流的对比

| 工作流 | 阶段结构 | 人工关卡 | 最适用于 |
|----------|----------------|------------|----------|
| **RPI** | 研究 + 规划 + 实现 | GO/NO-GO + 计划批准 | 可行性未知、耗时 >1 天、方向走偏风险高 |
| **Dual-Instance** | 规划 + 实现（分离的 Claude 实例） | 计划批准 | 需要谨慎执行的已知功能、规范繁重的工作 |
| **Spec-First** | 规范 + 实现 | 无（规范即隐式关卡） | 以设计为重点的工作、API 契约、团队对齐 |
| **TDD** | 测试优先 + 实现 | 无（测试即关卡） | 以测试覆盖率为驱动、重构、增量式行为 |
| **Direct** | 无 | 无 | 简单变更、范围明确、少于 2 小时 |

### RPI 与 Dual-Instance

Dual-instance 将规划和实现分离到两个 Claude 实例中，并严格强制角色分工。当你已经清楚要构建什么、并希望得到一份高质量计划时，它效果很好。RPI 在规划之前增加了一个可行性阶段，这使它更适合需求模糊的情况。如果你已经有了清晰的规范，则可跳过研究阶段，改用 dual-instance 或 spec-first。

### RPI 与 Spec-First

Spec-first 以设计为导向：你定义系统应该做什么，然后 Claude 去实现它。RPI 以实现为导向，并带有验证关卡：你描述一个目标，Claude 研究如何实现它，然后你们二者在动手写代码之前就计划达成一致。当设计已经清晰时使用 spec-first；当技术路径尚不明确时使用 RPI。

### RPI 与直接编码

对于任何耗时不到 2 小时、范围明确的任务，直接让 Claude 去做就好。RPI 带来的额外开销对于小任务并不划算。单是研究阶段就需要 30-60 分钟。这种开销在跨多天的功能上才会得到回报——在那种场景里，过晚才发现某个错误假设的代价要高得多。

---

## 技巧与排错

### Claude 在研究阶段跳到了实现

**问题**：Claude 在研究阶段就开始写代码。

**解决方案**：明确地为研究阶段启用 Plan Mode（连按两次 Shift+Tab）。在研究命令中包含这行：

```
You are in Plan Mode. Do not modify files. Do not write implementation code.
Research only. Output goes to RESEARCH.md.
```

或者添加到你的 CLAUDE.md 中：

```markdown
## RPI Rules
- /rpi:research runs in Plan Mode only — no file modifications
- /rpi:plan produces only PLAN.md — no implementation code
- /rpi:implement runs one step at a time, waits for test gate before next step
```

### 研究阶段耗时过长

**问题**：Claude 探索了整个代码库，而不是聚焦于相关部分。

**解决方案**：明确界定研究范围：

```
/rpi:research payment-processing

Focus area: src/payments/, src/routes/checkout.ts
Do not explore: frontend, auth, unrelated backend modules
Time budget: complete research in one session
```

### 计划步骤过多

**问题**：PLAN.md 有 12 个步骤，导致实现过程难以驾驭。

**解决方案**：步骤超过 6-8 个的计划通常需要的是缩减范围，而不是更细粒度的实现。可以让 Claude：

```
The plan has too many steps. What is the minimal viable scope that delivers
the core value? Revise the plan to implement only that, with a clear
"Future work" section for the rest.
```

### 测试关卡含糊不清

**问题**：某个步骤的测试关卡写的是"验证它能工作"，而不是一条具体命令。

**解决方案**：在批准计划之前拒绝含糊的关卡。这样反推回去：

```
Step 3's test gate is "verify rate limiting works." Make it specific:
what command do I run, and what output do I expect to see when it passes?
```

一个好的测试关卡：

```
Test gate: `npm test src/middleware/rate-limit.test.ts` — all 4 tests pass
```

一个差的测试关卡：

```
Test gate: rate limiting is working correctly
```

### 某个步骤关卡反复失败

**问题**：即使尝试过修复，Step 2 的关卡仍持续失败。

**解决方案**：失败两次就意味着要去审查计划，而不是继续在修复上反复折腾。

```
Stop implementation. The Step 2 gate has failed twice.
Review the plan — is the test gate achievable given the Step 1 output?
Do we need to revise the plan before continuing?
```

---

## 文件结构概览

```
.claude/
└── features/
    └── [feature-name]/
        ├── RESEARCH.md     # Phase 1 output (human annotates GO/NO-GO)
        └── PLAN.md         # Phase 2 output (human annotates approval)

.claude/commands/
├── rpi-research.md         # /rpi:research slash command
├── rpi-plan.md             # /rpi:plan slash command
└── rpi-implement.md        # /rpi:implement slash command
```

归档已完成的功能：

```bash
mkdir -p .claude/features/_archive
mv .claude/features/payment-processing .claude/features/_archive/
```

归档是一种学习资源：已完成的 RESEARCH.md 和 PLAN.md 文件展示了以往的功能是如何被推敲的。

---

## 另见

- [dual-instance-planning.md](./dual-instance-planning.md) — 用于规范繁重型实现的双实例模式
- [spec-first.md](./spec-first.md) — 以 CLAUDE.md 作为契约的设计优先工作流
- [tdd-with-claude.md](./tdd-with-claude.md) — 与 TDD 结合实现测试关卡式实现
- [task-management.md](./task-management.md) — 跨会话管理多阶段任务
- **主指南**：Advanced Patterns 章节 — 多实例与规划模式概览
