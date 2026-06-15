---
title: "Exploration Before Implementation"
description: "Ask Claude for multiple approaches with trade-offs before coding to prevent anchoring bias"
tags: [workflow, architecture, design-patterns]
---

# 先探索，后实现

> **可信度**：Tier 2 — 经从业者研究验证（决策质量提升 20-30%，可识别的备选方案增加 40%）。
> **来源**：[MetalBear Engineering Blog](https://metalbear.com/blog/engineering-ai-use/)、arXiv 从业者研究

在编写代码之前，先让 Claude 给出多种方案及其权衡取舍。这能避免锚定偏差——即倾向于固守第一个提出的方案。

---

## 目录

1. [TL;DR](#tldr)
2. [模式](#the-pattern)
3. [反锚定提示词](#anti-anchoring-prompts)
4. [何时使用](#when-to-use)
5. [与 Claude Code 集成](#integration-with-claude-code)
6. [反模式](#anti-patterns)
7. [另请参阅](#see-also)

---

## TL;DR

```
1. Describe problem (no code, no preconception)
2. Request 3-5 approaches with trade-offs
3. Ask for quantified comparison
4. Choose approach
5. Then implement
```

关键洞察：**一旦模型提出了某个具体方案，它可能会在无意中收窄你的思路。**

---

## 模式

### 第 1 步：只陈述问题

从问题入手，而不是某个解决方向：

```
I need to handle user sessions in a Node.js API.
Requirements:
- Support 10K concurrent users
- Session data: user ID, permissions, preferences
- Must survive server restarts
```

**不要这样**（这会锚定到 Redis）：
```
I'm thinking of using Redis for sessions. How should I implement it?
```

### 第 2 步：请求多种方案

```
Give me 4 different approaches to solve this.
For each, include:
- Architecture overview
- Pros and cons
- Performance characteristics
- Complexity to implement
```

### 第 3 步：量化对比

```
Now rank these approaches on a 1-10 scale for:
- Latency (lower is better)
- Scalability (10K → 100K users)
- Operational complexity
- Development time
```

### 第 4 步：先选定，再实现

```
I'll go with approach B (JWT + Redis hybrid).
Now implement it following our existing patterns in src/auth/.
```

---

## 反锚定提示词

LLM 可能会固守它的第一个建议。以下提示词可以对抗这一点：

| 提示词类型 | 模板 | 效果 |
|-------------|----------|--------|
| **重新开始** | "Ignore any prior ideas. Generate 4 novel approaches to [X]" | 强制多样性 |
| **反思循环** | "Generate 3 options, then critique each, then recommend" | 自我纠错（锚定偏差降低 25%） |
| **量化权衡** | "Rank by [metric1], [metric2], [metric3] with scores 1-10" | 客观对比 |
| **唱反调** | "What are the strongest arguments against your recommendation?" | 暴露隐藏的权衡取舍 |
| **约束变化** | "Now solve the same problem with [opposite constraint]" | 扩展解空间 |

### 示例：反锚定提示词

```
I need pagination for a REST API with 1M+ records.

IMPORTANT: Don't suggest offset-based pagination first.
Generate 4 different pagination strategies, including at least one
unconventional approach. For each:

1. How it works (2-3 sentences)
2. Best use case
3. Worst use case
4. Performance at 1M records

Then recommend one, explaining why it beats the others for my use case.
```

### 反思循环提示词

```
For implementing real-time notifications:

Phase 1: Generate 3 approaches (WebSockets, SSE, Long Polling)
Phase 2: For each, list 2 things that could go wrong in production
Phase 3: Based on Phase 2, which approach is most resilient?

Show your reasoning for each phase.
```

---

## 何时使用

### 适合探索的场景

| 场景 | 原因 |
|----------|-----|
| 全新功能 | 没有现成的模式可以遵循 |
| 架构决策 | 影响大、难以回退 |
| 存在多种有效方案 | 需要在充分了解后做出选择 |
| 不熟悉的领域 | 你不知道自己有哪些不知道 |
| 团队意见分歧 | 获得对各选项的中立分析 |

### 跳过探索的场景

| 场景 | 原因 |
|----------|-----|
| Bug 修复 | 解决方案通常从症状就能看出 |
| 只有一种有效方案 | 没有真正的选择余地 |
| 时间紧迫的热修复 | 速度优先于完美 |
| 遵循现有模式 | 决策已经做出 |
| 微小改动 | 不值得为此付出额外成本 |

---

## 与 Claude Code 集成

### 配合 Plan Mode

探索应发生在进入 Plan Mode **之前**：

```
# Step 1: Explore (not in Plan Mode yet)
I need to add caching to the API. What are my options?

# Claude responds with 4 approaches

# Step 2: Choose
Let's go with approach C (edge caching with Cloudflare).

# Step 3: Plan (press Shift+Tab twice to enter Plan Mode)
Implement edge caching using Cloudflare Workers.
Follow the patterns in our existing middleware.
```

### 配合 CLAUDE.md

在你的项目指令中加入探索触发条件：

```markdown
## Workflow Preferences

### Before New Features
When implementing new features, first explore 3-4 approaches
with trade-offs before committing to implementation.
Use quantified comparison (1-10 scale) for:
- Performance
- Maintainability
- Time to implement
```

### 配合 Task 工具

把探索作为任务来跟踪：

```
TaskCreate: "Explore caching approaches"
TaskCreate: "Choose approach based on analysis"
TaskCreate: "Implement cache invalidation"
TaskCreate: "Add cache headers to responses"
# Mark completed as you progress with TaskUpdate
```

---

## 反模式

### 过早锚定

```
# Wrong
"I want to use Redis for caching. How do I set it up?"

# Right
"I need caching for API responses. What are my options?"
```

你在探索之前就已经排除了 90% 的解决方案。

### 浅层对比

```
# Wrong
"Which is better: Redis or Memcached?"

# Right
"Compare Redis, Memcached, and in-process caching for:
- 50MB cache size
- Read-heavy workload (95% reads)
- Single server deployment
Include latency, memory overhead, and operational complexity."
```

### 忽视权衡

```
# Wrong
"Just tell me the best approach"

# Right
"What would I give up by choosing approach A over B?
What scenarios would make me regret this choice?"
```

### 分析瘫痪

```
# Wrong
Exploring 10 options for a simple feature

# Right
Set a limit: "Give me your top 3 approaches, no more"
Make a decision and iterate if needed
```

---

## 示例会话

### 初步探索

```
User: I need to implement real-time updates in our React dashboard.
      The dashboard shows ~50 metrics that update every 5 seconds.
      Currently we poll, but users complain about stale data.

Claude: Here are 4 approaches:

**A) WebSockets**
- Full duplex, server can push anytime
- Pros: Lowest latency, true real-time
- Cons: Connection management, scaling complexity
- Best for: Sub-second updates, bidirectional communication

**B) Server-Sent Events (SSE)**
- Unidirectional server → client stream
- Pros: Simple, HTTP-based, auto-reconnect
- Cons: One-way only, limited browser connections
- Best for: Dashboard feeds, notifications

**C) Long Polling**
- Client holds request until data ready
- Pros: Works everywhere, simple fallback
- Cons: Higher latency, more server load
- Best for: Legacy compatibility

**D) GraphQL Subscriptions**
- WebSocket-based with GraphQL schema
- Pros: Type-safe, selective updates
- Cons: Requires GraphQL infrastructure
- Best for: Existing GraphQL APIs

User: Rank these for our use case (React, 50 metrics, 5s refresh,
      team has no WebSocket experience).

Claude: Scores (1-10, higher is better):

| Approach | Latency | Complexity | Team Fit | Scalability |
|----------|---------|------------|----------|-------------|
| WebSockets | 10 | 4 | 3 | 7 |
| SSE | 8 | 8 | 8 | 8 |
| Long Polling | 5 | 9 | 9 | 5 |
| GraphQL Subs | 9 | 3 | 2 | 7 |

**Recommendation: SSE**
Best balance of simplicity and real-time capability.
Your team can implement it in a day, and it handles your
50 metrics × 5s updates easily. Upgrade to WebSockets later
if you need bidirectional or sub-second updates.

User: Let's go with SSE. Now implement it.
```

---

## 另见

- [plan-driven.md](./plan-driven.md) — 用于代码库探索（/plan 模式）
- [iterative-refinement.md](./iterative-refinement.md) — 选定方案后进行打磨
- [../examples/semantic-anchors/anchor-catalog.md](../../examples/semantic-anchors/anchor-catalog.md) — 提示词的精确词汇表
- [spec-first.md](./spec-first.md) — 在探索之前定义需求
