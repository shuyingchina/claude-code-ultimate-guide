---
title: "Plan-Validate-Execute Pipeline"
description: "Production-grade 3-command workflow with dynamic agent teams, ADR learning loop, and automated execution from PRD to merged PR"
tags: [workflow, agents, architecture, advanced]
---

# Plan-Validate-Execute Pipeline

> **可信度**：Tier 2 —— 经大规模交付 AI-first 产品的生产团队实战验证。在原生 `/plan` 模式之上扩展了结构化的 agent 编排与机构记忆。

一套由 3 条命令构成的完整开发工作流：用动态研究团队做规划，用独立的专家评审做验证，用并行 agents 执行。每一次运行都会通过 ADR 学习循环改进下一次，逐步减少人工干预。

**阅读时间**：约 25 分钟
**前置知识**：Sub-agents、Task 工具、worktree、ADR 基本概念
**相关**：[Plan-Driven Development](./plan-driven.md)、[Agent Teams](./agent-teams.md)、[Spec-First](./spec-first.md)

---

## 目录

1. [TL;DR](#tldr)
2. [理念](#philosophy)
3. [三条命令](#the-three-commands)
4. [动态 Agent 池](#dynamic-agent-pool)
5. [ADR 学习循环](#adr-learning-loop)
6. [CLAUDE.md 纪律](#claudemd-discipline)
7. [上下文管理](#context-management)
8. [何时使用](#when-to-use)
9. [成本概况](#cost-profile)
10. [另请参阅](#see-also)

---

## TL;DR

```
/plan-start    → 5-phase planning: PRD analysis + dynamic research team + ADRs
/plan-validate → 2-layer review: structural checks + trigger-based specialist agents
/plan-execute  → worktree + TDD + parallel execution + PR + merge + cleanup
```

**它与 `/plan` 模式的区别在哪**：
- 研究由专门的 agents 并行完成，而非由一个 agent 顺序完成
- 验证独立于规划（避免确认偏误）
- 每一个重大决策都会生成一份 ADR，自动消解未来的同类决策
- 执行会在 git worktree 中为每个任务派生 agent，按任务提交，全程处理直至合并 PR

**在每条命令之间运行 `/clear`**，以重置上下文，避免 compact 的额外开销。

---

## 理念

### 非规定式（Non-Prescriptive）的 AI-First

告诉 Claude 要**达成什么**，永远不要规定**如何**实现。一旦你规定了实现细节，你就是在用自己的知识当天花板，而不是把 Claude 的知识当地板。

新项目的一个好的开场 prompt：
```
How should I use you most effectively to build this platform?
```

让 Claude 提出架构。你的职责是验证决策，而非命令决策。

### 不打补丁，不绕弯子

对流水线中每一个 agent 的硬性规则：

> 我们构建业界顶尖的软件。永远选择同类最佳的架构、最稳健的模式以及业界标准的做法。

构建时间与投入与架构决策无关。永远不要把实现复杂度纳入方案评估。正确的方案永远是最好的方案。

**执行检查清单**（实现前应用）：
- [ ] 我是否在使用向后兼容标志、shim 或遗留模式？
- [ ] 一个遵循当前官方文档的新项目会这样做吗？
- [ ] 我是否在移植旧模式，而不是学习新模式？
- [ ] 我是否在修补单个组件，而修复其实应在系统层面进行？

只要有任何一项答案为是：停下，在正确的层面修复。

### 为什么要独立验证？

没有参与撰写计划的验证者，不会被计划的假设锚定。研究表明，采用对抗性框架的多 agent 评审，比自我评审能发现明显更多的问题。一份普通计划在被独立团队挑战时会产生约 18 个问题——其中约 95% 可由现有 ADR 与第一性原理自动消解。

---

## 三条命令

### `/plan-start` —— 5 阶段规划

**阶段 1：PRD 与设计分析** *（交互式，无 agent）*

阅读 PRD，并在任何 agent 工作之前，从 3 个维度暴露问题：
- 缺失的需求（验收标准不清、边界情况未指定）
- 含糊的需求（存在多种有效解读）
- 合规顾虑（安全、数据隐私、API 契约）

给出带有优缺点的选项，记录决策。对于非 PRD 工作（重构、基础设施、缺陷修复）则跳过。

如果范围内涉及 UI 变更，则扩展到设计分析：屏幕清单、状态目录（空/加载中/有数据/错误）、交互规格、动画模式、无障碍（ARIA）、design token 更新。

**阶段 2：技术分析** *（1-2 个 Explore agent + 交互式）*

先检查现有的 ADR 和 PATTERNS.md。若有 3 个及以上已确认的 ADR 与该决策匹配 → 无需询问即自动消解。否则：
- 派生 Explore agents 进行有针对性的代码库研究
- 给出架构决策，附带选项与建议
- 为重大决策创建 ADR 文档（见 [ADR 学习循环](#adr-learning-loop)）
- 更新 PATTERNS.md

**阶段 3：范围评估** *（自动 + 用户批准）*

针对 agent 池应用触发规则（见 [动态 Agent 池](#dynamic-agent-pool)）。给出建议的团队组成，并为每个 agent 给出理由。用户可在研究开始前增删 agent。

| 层级 | Agent 数量 | 标签 |
|------|-------------|-------|
| 0 | 0 | Solo（内联研究） |
| 1 | 1-3 | Focused |
| 2 | 4-6 | Standard |
| 3 | 7-9 | Comprehensive |
| 4 | 10+ | Full Spectrum |

**阶段 4：研究与计划生成** *（动态团队）*

- Tier 0：内联研究，无 agent
- Tier 1+：并行（后台）派生已批准的 agent，主导者通过 TaskOutput 循环监控
- `planning-coordinator`（Opus）将所有报告综合为最终计划
- 提交计划文件、ADR 与生成产物

输出：`docs/plans/plan-{name}.md` + `docs/adr/ADR-XXXX.md` + `docs/plans/metrics/{name}.json`

**自动切换**：无未消解的含糊点 → 自动启动 `/plan-validate`

---

### `/plan-validate` —— 2 层验证

**第 1 层：结构性** *（内联，即时）*

不需要 agent 的机械检查：
- 计划格式与完整性（所有必需小节齐全）
- 任务排序与依赖链（无循环依赖）
- 文件存在性检查（列为待修改的文件确实存在）
- ADR 一致性（计划与其 ADR 对齐）
- CLAUDE.md 规则合规性

**第 2 层：专家评审** *（基于触发，0-8 个 agent）*

| Agent | 触发条件 | 模型 |
|-------|---------|-------|
| `security-reviewer` | 认证、支付、PII、RBAC、新 API | Opus |
| `db-migration-reviewer` | 新表、列、索引、迁移 | Opus |
| `performance-reviewer` | 新 resolver、查询、路由、新依赖 | Sonnet |
| `design-system-reviewer` | 新 UI 组件、视觉样式 | Sonnet |
| `ux-reviewer` | 新页面、表单、交互 | Sonnet |
| `cross-platform-reviewer` | Web + 移动端，或共享包 | Sonnet |
| `native-app-reviewer` | 移动端屏幕、原生 UI 包 | Sonnet |
| `integration-reviewer` | 新服务、库、OTEL 配置 | Opus |

对于琐碎的计划不会自动选择任何 agent。一个支付功能则可能触发 4 个以上。

**自动修复阶段**

每个问题都必须被解决——不允许跳过。分诊流程：
1. 与现有 ADR 决策匹配的问题 → 自动消解
2. 与已确认的 PATTERNS.md 条目匹配的问题 → 自动消解
3. 可由第一性原理解决的问题 → 自动消解
4. 剩余的 → 人工决策 → 新规则 → 下次自动消解

**自动切换**：所有问题已解决 → 自动启动 `/plan-execute`

---

### `/plan-execute` —— 执行直至合并 PR

单条命令处理一切：

1. **创建 worktree** —— 从当前分支隔离出一个分支
2. **TDD 脚手架** —— 为标记了 TDD 的任务先写失败的测试
3. **基于层级的并行执行** —— 检测互不依赖的任务，为每个任务派生 agent，按任务提交
4. **漂移检测** —— 若实现偏离计划则标记
5. **质量门** —— 并行测试 + 集成冒烟测试（GraphQL 探测、容器日志扫描、计划中定义的冒烟命令）
6. **PR 前文档更新** —— PRD 对账 + 计划归档（在 worktree 中）
7. **创建并合并 PR** —— squash 合并，整洁的提交信息
8. **合并后指标** —— 执行数据提交到 metrics 文件
9. **清理 worktree** —— 删除分支与 worktree

若质量门未通过：由专门的调试 agent 最多自动修复 3 次。仍失败 → 通知人工。

---

## 动态 Agent 池

agent **不会**硬编码在 CLAUDE.md 中。它们在调用时定义——描述、触发条件以及模型选择都内嵌在派生它们的规划阶段。这样既保持 CLAUDE.md 的轻量，又为每个 agent 提供其角色所需的完整上下文。

### 研究池（`/plan-start`）

| Agent | 触发条件 | 模型 |
|-------|---------|-------|
| `code-explorer` | 始终 | Sonnet |
| `arch-researcher` | 多层变更（2 层及以上） | Sonnet |
| `database-analyst` | 任何 DB schema 变更 | Sonnet |
| `security-analyst` | 认证、支付、PII、RBAC | Opus |
| `test-analyzer` | 非琐碎功能 | Sonnet |
| `cross-platform-specialist` | 需要移动端对等 | Sonnet |
| `native-app-specialist` | 任务涉及移动端/UI | Sonnet |
| `design-system-researcher` | 范围内含 UI 变更 | Sonnet |
| `dependency-researcher` | 正在新增包 | Sonnet |
| `devops-specialist` | Docker、env vars、CI/CD | Sonnet |
| `integration-researcher` | 新服务、库、OTEL | Opus |
| `planning-coordinator` | 始终（当 2 个及以上 agent 时） | Opus |

**关键设计选择**：
- Opus 仅用于高风险角色（安全、集成、协调）
- Sonnet 用于标准研究（质量好，成本更低）
- `planning-coordinator` 仅在选择了 2 个及以上 agent 时才派生——它负责综合，不做研究

### 验证池（`/plan-validate`）

见上文第 2 层表格。这些 agent 与研究池中的不同——验证者不会受创建过程的影响而产生偏见。

---

## ADR 学习循环

每一个重要的架构决策都会生成一份 ADR。随着时间推移，ADR 逐渐累积成组织级的记忆，从而减少对人工的打断。

### 什么情况下触发 ADR

**始终创建 ADR 的场景：**
- 在多种有效的交互模式之间做选择（overlay 还是 page、drawer 还是 modal）
- 现有约定中尚不存在的新动画或过渡模式
- 平台差异化决策（web 与 mobile 的行为差异）
- 引入新模式的加载状态策略
- 鉴权策略、DB schema 方案、服务边界决策
- 带有架构影响的新依赖选型

**不要创建 ADR 的场景：**
- 由已批准的来源或现有约定所决定的决策
- 既定模式内的次要布局选择
- 显而易见的状态目录条目（标准的 empty/loading/error 状态）

### 成熟度等级

```
1 ADR  → Watching   — tracked, not yet prescriptive
2 ADRs → Emerging   — presented as recommended default with precedent context
3+ ADRs → Confirmed — auto-resolved during planning (no human input needed)
          → Candidate for promotion to CLAUDE.md as hard rule
```

### 循环

```
/plan-start Phase 2     →  ADR created
                               ↓
                        PATTERNS.md updated
                               ↓
/adr-review (periodic)  →  Detect patterns across ADRs
                               ↓
                        Propose CLAUDE.md promotions
                               ↓
Future /plan-start      ←  Confirmed rules auto-resolve decisions
```

每 10-15 个计划运行一次 `/adr-review`，以批量分析模式并提出对 CLAUDE.md 的补充建议。

**复利效应**：一个拥有 20 个计划的项目可自动解决约 80% 的架构决策。人工投入只需聚焦于真正新颖的决策。

---

## CLAUDE.md 自律

### 硬性上限：120 行

CLAUDE.md 中的每一行都会在每次请求时消耗上下文。一份 300 行的 CLAUDE.md 是会在每一次提示之前都运行的额外开销。请设定并强制执行一个硬性上限。

**值得占用 CLAUDE.md 一行的内容：**
- 第一性原则（覆盖 agent 偏好的硬性规则）
- 已确认的 ADR 模式（出现 3 次以上）
- agent 无法从代码库推断出的项目专属约定
- 指向子文件的指针

**不应出现在 CLAUDE.md 中的内容：**
- 设计系统、环境配置、架构文档的完整内容
- 适用于不到 10% 任务的规则
- 解释和理由（这些应写在 ADR 中）

### 指针策略

不要把所有上下文都加载进 CLAUDE.md，而是使用指针：

```markdown
## Context Files (load only when relevant)
- @docs/DESIGN_SYSTEM.md    — when UI changes are in scope
- @docs/ARCHITECTURE.md     — when service boundaries are touched
- @docs/ENV_CONFIG.md       — when Docker or env vars are modified
- @docs/ADR_PATTERNS.md     — during planning phases
```

agent 只加载其任务所需的内容。后端任务永远不会加载设计系统。上下文保持干净。

### 定期精简

每 10-15 个计划，配合 `/adr-review` 一起审查 CLAUDE.md。将已确认的模式提升固化，删除那些已通过代码库约定变得显而易见的规则，剔除任何从未被引用过的内容。

---

## 上下文管理

### 在各步骤之间执行 `/clear`

在 `/plan-start`、`/plan-validate` 和 `/plan-execute` 之间运行 `/clear`。每条命令都是自包含的——磁盘上的计划文件才是交接产物，而非内存中的上下文。

不执行 `/clear` 时：上下文会在所有阶段间累积，compacting 会更早触发，agent 会从前一阶段继承无关的上下文，token 成本也会显著上升。

### 为什么这样有效

每条命令都从磁盘读取其输入（计划文件、ADR、代码库）。各步骤之间没有任何需要常驻于上下文窗口的状态。正是这种在各步骤间清理的自律，让整条流水线能够扩展到大型项目，而不会在执行中途撞上上下文上限。

---

## 何时使用

### ✅ 在以下情况使用本流水线

- 功能涉及多个文件和层次（API + DB + UI）
- 安全敏感的变更（auth、payments、PII）
- 复杂的 DB 迁移
- 新的外部服务集成
- 任何一旦规划失误就会代价高昂、难以回退的场景
- 决策历史很重要的团队项目

### ❌ 不要在以下情况使用

- 拼写修正、琐碎重构（使用标准的 `/plan` 模式）
- 需求尚不明确的探索性原型设计
- 时间压力下的热修复（改用双实例规划）
- 涉及文件不超过 2 个且无架构决策的变更

### ⚡ Tier 0 捷径

对于规模较小但并非琐碎的变更，仍然运行流水线，但系统会检测到 Tier 0 范围并跳过 agent 派生——研究内联进行，验证仅做 Layer 1，执行采用单 agent。命令相同，开销更低。

---

## 成本概览

| 阶段 | 成本驱动因素 | 大致区间 |
|-------|-------------|-------------------|
| `/plan-start` Tier 0 | 仅内联研究 | $0.10-0.30 |
| `/plan-start` Tier 1-2 | 2-6 个 Sonnet agent | $0.50-2.00 |
| `/plan-start` Tier 3 | 7+ 个 agent + Opus 协调器 | $2.00-8.00 |
| `/plan-validate` | 0-8 个 agent | $0.20-3.00 |
| `/plan-execute` | 按任务派生的 agent + 质量门 | $0.50-5.00 |
| **典型功能（Tier 2）** | 完整流水线 | **$2-10** |

成本会随着 ADR 覆盖率的增长而产生复利效应：所需 agent 更少、验证问题更少、执行更快。

定期使用 `/plan-metrics` 来回顾历史成本趋势并校准估算。

---

## 另见

- [计划驱动开发](./plan-driven.md) — 原生 `/plan` 模式，更轻量的替代方案
- [双实例规划](./dual-instance-planning.md) — 更简单的 2 实例模式
- [Agent 团队](./agent-teams.md) — 原生并行协调（实验性）
- [任务管理](./task-management.md) — 用于跨会话协调的 Tasks API
- [规范优先开发](./spec-first.md) — 将 CLAUDE.md 作为规范契约
- [ADR Writer Agent](../../examples/agents/adr-writer.md) — 独立的 ADR 生成
- [Plan Challenger Agent](../../examples/agents/plan-challenger.md) — 对抗式计划审查
