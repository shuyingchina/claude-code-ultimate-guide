---
title: "Development Methodologies Reference"
description: "Quick reference for 15 structured AI-assisted development methodologies including TDD, SDD, and BDD"
tags: [reference, tdd, design-patterns, workflows]
---

# 开发方法论参考

> **可信度**：Tier 2 — 由多份生产环境报告与官方文档验证。
>
> **最后更新**：2026 年 2 月

这是一份快速参考，涵盖了 2025-2026 年间为 AI 辅助开发而涌现出的 15 种结构化开发方法论。如需动手实践的工作流，参见 [workflows/](../workflows/)。

---

## 目录

1. [决策树](#decision-tree-what-do-you-need)
2. [15 种方法论](#the-15-methodologies)
3. [SDD 工具参考](#sdd-tools-reference)
4. [编写有效的规格说明](#writing-effective-specs)
5. [组合模式](#combination-patterns)
6. [来源](#sources)

---

## 决策树：你需要什么？

```
┌─ "I want quality code" ────────────→ workflows/tdd-with-claude.md
│
├─ "I want to spec before code" ─────→ workflows/spec-first.md
│
├─ "I need to plan architecture" ────→ workflows/plan-driven.md
│
├─ "I'm iterating on something" ─────→ workflows/iterative-refinement.md
│
└─ "I need methodology theory" ──────→ Continue reading below
```

---

## 方法论地图

每种方法论在两条坐标轴上的位置：**规格优先 vs 代码优先**（Y 轴）和 **精简/单人 vs 企业/受治理**（X 轴）。

```
                      SPEC / PLANNING FIRST
                                ▲
  ── lean · spec ──             │             ── governed · spec ──
                                │
  [Doc-Driven]  [SDD]           │    [BDD]  [ATDD]   [Req-Driven]
  [GSD]  [Plan-First]           │ [CDD] [ADR-Driven]  [DDD]  [BMAD]
                                │
  LEAN ─────────────────────────┼────────────────────────────────► ENTERPRISE
                                │
  ── lean · code ──             │             ── governed · code ──
                                │
  [Context Eng.]   [TDD]        │       [Multi-Agent]
  [Prompt Eng.]  [Iterative]    │       [Eval-Driven]       [FDD]
  [Ralph Loop]                  │           [JiTTesting]
                                │
                         CODE / EMERGENT
```

**如何阅读这张图：**

- **左上** — 规格优先且精简：`SDD`、`Doc-Driven`、`Plan-First`。对于正从"代码优先"转型的单人开发者和小团队来说，这是天然的切入点。
- **右上** — 规格优先且受治理：`BMAD`、`Req-Driven`、`ATDD`、`DDD`。具备真正的治理能力，但搭建成本高。ROI 由项目复杂度和需求稳定性驱动，而非仅由人数决定。
- **左下** — 代码优先且精简：Claude Code 的天然地盘。`TDD` + `Ralph Loop` + `Iterative` = 核心单人工作流。
- **右下** — 大规模的代码优先：`Multi-Agent`、`Eval-Driven`、`JiTTesting`（Meta，1 亿行以上代码）。面向高产出团队的新兴模式。
- **位于坐标轴上** — `Plan-First`、`CDD`、`ADR-Driven`、`GSD`：能适配任何场景的混合型方法。

---

## 15 种方法论

按一个 6 层金字塔组织，自上而下从战略编排到优化技巧。

### Tier 1：战略编排

| 名称 | 是什么 | 最适合 | Claude 契合度 |
|------|------|----------|------------|
| **BMAD** | 以 constitution 作为护栏的多 agent 治理 | 需求稳定、有合规或治理需求的高复杂度项目 | ⭐⭐ 小众但强大 |
| **GSD** | 元提示（meta-prompting）式 6 阶段工作流，每个任务使用全新上下文 | 单人开发者、Claude Code CLI | ⭐⭐ 与本指南中的模式类似 |

**BMAD（Breakthrough Method for Agile AI-Driven Development）** 颠覆了传统范式：文档成为唯一真相来源，而非代码。它使用一组专门的 agent（Analyst、PM、Architect、Developer、QA），并以严格的治理来编排。*注：BMAD 的基于角色的 agent 命名反映的是其方法论；以范围为中心的替代方案参见 §9.17 Agent 反模式。*

- **核心概念**：以 Constitution.md 作为战略护栏
- **何时使用**：需要治理的复杂企业项目
- **何时避免**：MVP、快速原型、需求不断演变的场景 — 当规格在项目中途发生变化时，BMAD 会变得脆弱

**GSD（Get Shit Done）** 通过系统化的 6 阶段工作流（Initialize → Discuss → Plan → Execute → Verify → Complete）来对抗上下文腐化（context rot），每个任务都使用全新的 20 万 token 上下文。其核心概念（多 agent 编排、全新上下文管理）与现有模式（如 Ralph Loop、Gas Town 和 BMAD）有大量重叠。详细对比参见[资源评估](../../docs/resource-evaluations/gsd-evaluation.md)。

> **新兴**：[Ralph Inferno](https://github.com/sandstream/ralph-inferno) 实现了自主的多人格工作流（Analyst→PM→UX→Architect→Business），具备基于 VM 的执行和自我纠正的 E2E 循环。尚属实验性质，但对于"规模化氛围编程（vibe coding at scale）"很有意思。

---

### 基础纪律：Plan-First 工作流

> **"一旦计划是好的，代码就是好的。"**
> — Boris Cherny，Claude Code 的创造者

**它不仅仅是一个功能（`/plan` 命令）——而是一种系统化的纪律。**

> **Context Engineering**：Thoughtworks 在其技术雷达（2025 年 11 月）[^thoughtworks2025] 中将这一更宽泛的方法命名为"Context Engineering"——即在推理期间系统化地设计提供给 LLM 的信息。三项核心技术：上下文搭建（最小化系统提示、few-shot 示例）、面向长周期任务的上下文管理（摘要化、外部记忆、sub-agent 架构）以及动态信息检索（JIT 上下文加载）。Claude Code 中的相关模式：AGENTS.md、MCP Context7、Plan Mode。

[^thoughtworks2025]: Thoughtworks Technology Radar Vol 33, Nov 2025. [PDF](https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2025/11/tr_technology_radar_vol_33_en.pdf). See also: [Macro trends blog post](https://www.thoughtworks.com/insights/blog/technology-strategy/macro-trends-tech-industry-november-2025).

**心智模型**：

对于复杂任务，规划不是可选项。它决定了你是处于：
- ❌ 8 次"尝试 → 修复 → 重试 → 再修复"的迭代
- ✅ 1 次"规划 → 验证 → 干净利落地执行"的迭代

**何时应该先规划**：

| 任务复杂度 | 是否先规划？ | 原因 |
|----------------|-------------|-----|
| 修改超过 3 个文件 | ✅ 是 | 跨文件依赖需要架构设计 |
| 改动超过 50 行 | ✅ 是 | 复杂度足以引发错误 |
| 架构性变更 | ✅ 是 | 需要影响分析 |
| 不熟悉的代码库 | ✅ 是 | 行动前需要先探索 |
| 拼写/显而易见的修复 | ❌ 否 | 规划开销 > 任务耗时 |
| 单行改动 | ❌ 否 | 直接做就行 |

**Plan-First 如何运作**：

1. **探索阶段**（通过 `Shift+Tab` 进入 Plan Mode）：
   - Claude 阅读文件、探索架构
   - 不允许编辑 → 强制在行动前思考
   - 提出带有权衡取舍的方案

2. **验证阶段**（由你审阅）：
   - 计划暴露出假设和缺口
   - 现在纠正方向比写完 100 行后再纠正更容易
   - 计划成为执行的契约

3. **执行阶段**（通过 `Shift+Tab` 切回 Normal Mode）：
   - 计划 → 代码变成机械化的翻译
   - 更少意外，实现更干净
   - 尽管起步"更慢"，整体却更快

**Boris Cherny 的工作流**：

> "我会运行很多会话，先从 plan mode 开始，等计划看起来对了再切换到执行。标志性的升级在于验证——给 Claude 一种方式去测试并确认它自己的输出。"

**相比"直接开始写代码"的好处**：

- **更少的纠正迭代**：计划在问题变成代码之前就将其捕获
- **更好的架构**：被迫先思考结构
- **更清晰的沟通**：计划是与团队/Claude 之间的共识
- **更低的成本**：一次干净的迭代 < 多次混乱的迭代（即便规划阶段会消耗 token）

**与 CLAUDE.md 的整合**：

记录下你团队的 plan-first 触发条件：
```markdown
## Planning Policy
- ALWAYS plan first: API changes, database migrations, new features
- OPTIONAL planning: Bug fixes <10 lines, test additions
- NEVER skip: Changes affecting >2 modules
```

**另见**：[Plan Mode 文档](#23-plan-mode)了解 `/plan` 命令的用法。

> **进阶模式**：关于一种基于标注的迭代式计划驱动开发方法，参见[自定义 Markdown 计划（Boris Tane 模式）](../workflows/plan-driven.md#advanced-custom-markdown-plans-boris-tane-pattern)。

---

### Tier 2：规格说明与架构

| 名称 | 是什么 | 最适合 | Claude 契合度 |
|------|------|----------|------------|
| **SDD** | 代码之前先有规格 | API、契约 | ⭐⭐⭐ 核心模式 |
| **Doc-Driven** | 文档 = 真相来源 | 跨团队对齐 | ⭐⭐⭐ CLAUDE.md 原生 |
| **Req-Driven** | 丰富的工件上下文（20+ 工件） | 复杂需求 | ⭐⭐ 搭建繁重 |
| **DDD** | 领域语言优先 | 业务逻辑 | ⭐⭐ 设计期 |

**SDD（Spec-Driven Development，规格驱动开发）** — 规格说明先于代码。一次结构良好的迭代抵得上 8 次无结构的迭代。CLAUDE.md 就是你的规格文件。

**Doc-Driven Development（文档驱动开发）** — 在 git 中受版本管理的活文档成为唯一真相来源。对规格的改动会触发实现。

**Requirements-Driven Development（需求驱动开发）** — 将 CLAUDE.md 用作综合性的实现指南，包含 20+ 个结构化工件。

**DDD（Domain-Driven Design，领域驱动设计）** — 通过以下方式让软件与业务语言对齐：
- 通用语言（Ubiquitous Language）：在代码中使用共享词汇
- 限界上下文（Bounded Contexts）：隔离的领域边界
- 领域提炼（Domain Distillation）：核心域 vs 支撑域 vs 通用域

---

### Tier 3：行为与验收

| 名称 | 是什么 | 最适合 | Claude 契合度 |
|------|------|----------|------------|
| **BDD** | Given-When-Then 场景 | 利益相关者协作 | ⭐⭐⭐ 测试与规格 |
| **ATDD** | 验收标准优先 | 合规、受监管 | ⭐⭐ 流程繁重 |
| **CDD** | 以 API 契约作为接口 | 微服务 | ⭐⭐⭐ OpenAPI 原生 |

**BDD（Behavior-Driven Development，行为驱动开发）** — 超越测试：一个协作过程。
1. 发现（Discovery）：让开发者和业务专家共同参与
2. 表述（Formulation）：编写 Given-When-Then 示例
3. 自动化（Automation）：转换为可执行测试（Gherkin/Cucumber）

```gherkin
Feature: Order Management
  Scenario: Cannot buy without stock
    Given product with 0 stock
    When customer attempts purchase
    Then system refuses with error message
```

**ATDD（Acceptance Test-Driven Development，验收测试驱动开发）** — 验收标准在编码之前协作式定义（"三剑客（Three Amigos）"：业务、开发、测试）。

在 agentic 开发中，ATDD 尤其有效，因为 agent 需要明确无歧义的成功条件。其流程能干净地映射到 agent 任务上：

1. **定义验收标准**，用 Gherkin 编写（人类可读、机器可执行）
2. **Agent 基于场景编写失败的测试**（而非基于实现）
3. **Agent 实现**直到测试通过

```gherkin
Feature: Password Reset
  Scenario: User resets via email
    Given a registered user with email "user@example.com"
    When they request a password reset
    Then they receive a reset email within 60 seconds
    And the reset link expires after 24 hours
```

这个 Gherkin 场景就是意图与实现之间的契约。Agent 无法误解范围，因为"完成"在写下一行代码之前就已被定义。

> **应用于 agent**：在实现之前把 Gherkin 文件传给 Claude Code。"为这个 feature 文件编写失败的测试，然后实现直到它们通过。"场景编写者角色（人或 agent）在执行开始前强制明确范围。

**CDD（Contract-Driven Development，契约驱动开发）** — 将 API 契约（OpenAPI 规格）作为团队间可执行的接口。模式：契约即测试（Contract as Test）、契约即桩（Contract as Stub）。

**JiTTesting（Just-in-Time Testing，即时测试）** — 测试在 PR 提交时即时生成、被设计为失败，并在合并后丢弃。没有维护成本，测试套件也不会膨胀。

TDD/BDD/ATDD 都假设开发者掌控着代码编写的节奏。Agentic 开发打破了这一假设：一个 agent 每小时可以生成 200 行代码，比任何人类的测试编写工作流都快。JiTTests 是对这种失配的工业化回应。

其机制是：在 PR 时，由一个 LLM 推断 diff 的意图，生成代码突变体（mutants，故意被破坏的变体），编写能捕获这些突变体的测试，运行基于规则和基于 LLM 的集成评估器来过滤误报，并只把真正的回归呈现给工程师。这些测试永远不会进入代码库。

Meta 大规模部署了这套方案（1 亿行以上代码）：相比传统的加固测试，捕获回归的能力提升 4 倍，人工审查负担减少 70%，在审查的 41 个候选项中阻止了 4 起严重的生产故障。

目前尚无开源实现。你今天就可以近似做到：在合并任何 agent 生成的 PR 之前，提示 Claude "生成专门能捕获这个 diff 所引入回归的测试——我会在本地运行它们，并在 PR 关闭后丢弃。"这种"短暂性"的措辞会把测试生成聚焦于真正改动的部分，而非泛泛的覆盖率。

> **参考**：[Just-in-Time Catching Test Generation at Meta](https://arxiv.org/abs/2601.22832) — Harman, 2026。

---

### Tier 4：功能交付

| 名称 | 是什么 | 最适合 | Claude 契合度 |
|------|------|----------|------------|
| **FDD** | 逐功能交付 | 并行交付的功能团队 | ⭐⭐ 结构 |
| **Context Eng.** | 将上下文作为一等设计要素 | 长会话 | ⭐⭐⭐ 基础性 |

**FDD（Feature-Driven Development，特性驱动开发）** — 五个过程：
1. 构建整体模型（Develop Overall Model）
2. 构建特性列表（Build Features List）
3. 按特性规划（Plan by Feature）
4. 按特性设计（Design by Feature）
5. 按特性构建（Build by Feature）

严格的迭代：每个特性最多 2 周。

**Context Engineering（上下文工程）** — 把上下文当作设计要素：
- 渐进式披露（Progressive Disclosure）：让 agent 逐步发现
- 记忆管理（Memory Management）：会话记忆 vs 持久记忆
- 动态刷新（Dynamic Refresh）：在响应前重写 TODO 列表

---

### Tier 5：实现

| 名称 | 是什么 | 最适合 | Claude 契合度 |
|------|------|----------|------------|
| **TDD** | Red-Green-Refactor | 高质量代码 | ⭐⭐⭐ 核心工作流 |
| **Eval-Driven** | 为 LLM 输出做评估 | AI 产品 | ⭐⭐⭐ Agent |
| **Multi-Agent** | 编排 sub-agent | 复杂任务 | ⭐⭐⭐ Task 工具 |

**TDD（Test-Driven Development，测试驱动开发）** — 经典循环：
1. **Red**：编写失败的测试
2. **Green**：写最少的代码让它通过
3. **Refactor**：清理代码，让测试保持绿色

与 Claude 配合时：要明确。"编写尚不存在的、会失败的（FAILING）测试。"

> **验证循环（Verification Loops）** — 一种用于自主迭代的形式化模式（比 TDD 更宽泛）：
>
> **核心原则**：给 Claude 一种机制去验证它自己的输出。
>
> ```
> Code generated → Verification tool → Feedback loop → Improvement
> ```
>
> **为什么有效**（Boris Cherny）：*"一个能'看见'自己做了什么的 agent 会产出更好的结果。"*
>
> **按领域划分的验证机制**：
>
> | 领域 | 验证工具 | Claude 能"看见"什么 |
> |--------|-------------------|-------------------|
> | **前端** | 浏览器预览（实时重载） | 视觉渲染、布局、交互 |
> | **后端** | 测试（单元/集成） | 通过/失败状态、错误信息 |
> | **类型** | TypeScript 编译器 | 类型错误、不兼容 |
> | **风格** | Linter（ESLint、Prettier） | 风格违规、格式问题 |
> | **性能** | 性能分析器、基准测试 | 执行时间、内存使用 |
> | **可访问性** | axe-core、屏幕阅读器 | WCAG 违规、导航问题 |
> | **安全** | 静态分析器（Semgrep） | 漏洞模式 |
> | **UX** | 用户测试、录屏 | 可用性问题、困惑点 |
>
> **TDD 作为典范示例**：
> 1. Claude 为该功能编写测试
> 2. Claude 迭代代码直到测试通过
> 3. 持续进行，直到满足明确的完成标准
>
> **官方指引**：*"告诉 Claude 持续推进，直到所有测试通过。它通常需要几次迭代。"* — [Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
>
> **实现模式**：
> - **Hooks**：PostToolUse hook 在每次编辑后运行验证
> - **浏览器扩展**：Claude in Chrome 能看到渲染后的输出
> - **测试监视器**：Jest/Vitest 的 watch 模式提供即时反馈
> - **CI/CD 门禁**：GitHub Actions 运行完整的验证套件
> - **多 Claude 验证**：一个 Claude 写代码，另一个审查
>
> **反模式**：没有反馈的盲目迭代。缺少验证机制，Claude 无法朝正确解收敛——它只能靠猜。

关于该模式所预防的实现侧失败模式，参见 TDD 工作流中的[验证缺口（The Verification Gap）](../workflows/tdd-with-claude.md#the-verification-gap)。

**Eval-Driven Development（评估驱动开发）** — 面向 LLM 的 TDD。通过评估来测试 agent 的行为：
- 基于代码：`output == golden_answer`
- 基于 LLM：由另一个 Claude 来评估
- 人工评分：作为基准，速度慢

> **Eval Harness（评估框架）** — 端到端运行评估的基础设施：提供指令与工具、并发运行任务、记录步骤、为输出评分并汇总结果。
>
> 参见 Anthropic 的全面指南：[Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

**Multi-Agent Orchestration（多 agent 编排）** — 从单个助手到编排出的团队：
```
Meta-Agent (Orchestrator)
├── Analyst (requirements)
├── Architect (design)
├── Developer (code)
└── Reviewer (validation)
```

### ADR-Driven Development（ADR 驱动开发）

**模式**：用平实英语编写 ADR → 喂给 implement-adr skill → 原生执行

架构决策记录（ADR）与 Claude Code skills 相结合，形成一种让架构决策直接驱动实现的工作流。

**工作流步骤**：
1. **记录决策**，采用 ADR 格式（背景、决策、后果）
2. **创建实现 skill**（通用的或专门的 `implement-adr`）
3. **将 ADR 作为提示喂入** skill，并附上清晰的验收标准
4. **Claude 执行**，依据 ADR 中的架构指引

**ADR 模板示例**：
```
# ADR-001: Database Migration Strategy

## 背景
遗留的 MySQL schema 需要迁移到 PostgreSQL，以获得更好的 JSON 支持。

## 决策
使用带 feature flags 的增量双写模式。

## 后果
- 正面：零停机迁移
- 负面：过渡期间临时的代码复杂度
```

**实现工作流**：
```bash
# 1. Write ADR (plain English)
vim docs/adr/001-database-migration.md

# 2. Feed to implementation skill
/implement-adr docs/adr/001-database-migration.md

# 3. Claude executes based on ADR guidance
# → Creates migration scripts
# → Updates ORM configuration
# → Adds feature flags
# → Implements dual-write logic
```

**收益**：
- ✅ **文档驱动**：架构与代码保持同步
- ✅ **原生执行**：无需外部框架
- ✅ **决策可追溯**：从决策到实现有清晰的审计轨迹
- ✅ **团队对齐**：ADR 将意图同时传达给人类和 AI

**来源**：[Gur Sannikov embedded engineering workflow](https://www.linkedin.com/posts/gursannikov_claudecode-embeddedengineering-aiagents-activity-7423851983331328001-DrFb)

---

### 第 6 层：优化

| 名称 | 内容 | 最适合 | Claude 适配度 |
|------|------|----------|------------|
| **Iterative Loops** | 自主迭代精炼 | 优化 | ⭐⭐⭐ 核心 |
| **Fresh Context** | 每个任务重置，状态存于文件 | 长时自主会话 | ⭐⭐⭐ 高级用户 |
| **Prompt Engineering** | 技术基础 | 一切 | ⭐⭐⭐ 前提条件 |

**迭代精炼循环（Iterative Refinement Loops）** — 自主收敛：
1. 执行 prompt
2. 观察结果
3. 如果结果 ≠ "DONE" → 精炼并重复

**Prompt Engineering** — 所有 Claude 使用的基础：
- 零样本思维链（Zero-Shot Chain of Thought）："Think step by step"
- 少样本学习（Few-Shot Learning）：2-3 个期望模式的示例
- 结构化 Prompt：用 XML 标签进行组织
- 位置很重要：对于长文档，把问题放在末尾

**Fresh Context 模式（Ralph Loop）** — 通过为每个任务派生全新的 agent 实例来解决上下文腐化（context rot）。状态持久化在 git + 进度文件中，而非聊天历史里。适合长时自主会话（迁移、通宵运行）。实现方式参见 [Ultimate Guide - Fresh Context Pattern](#fresh-context-pattern-ralph-loop)。

---

## SDD 工具参考

已出现三款工具用于将规范驱动开发（Spec-Driven Development）正规化：

| 工具 | 用例 | 官方文档 | Claude 集成 |
|------|----------|---------------|-------------------|
| **Spec Kit** | 全新项目、治理 | [github.blog/spec-kit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) | `/speckit.constitution`、`/speckit.specify`、`/speckit.plan` |
| **OpenSpec** | 既有项目、变更 | [github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | `/openspec:proposal`、`/openspec:apply`、`/openspec:archive` |
| **Specmatic** | API 契约测试 | [specmatic.io](https://specmatic.io) | 提供 MCP agent |
| **Spec-to-Code Factory** | 全新项目、工具化强制约束 | [github.com/SylvainChabaud/spec-to-code-factory](https://github.com/SylvainChabaud/spec-to-code-factory) | 多 agent 参考实现（BREAK→MODEL→ACT→DEBRIEF） |

### Spec Kit（全新项目）

5 阶段工作流：
1. Constitution：`/speckit.constitution` → 护栏
2. Specify：`/speckit.specify` → 需求
3. Plan：`/speckit.plan` → 架构
4. Tasks：`/speckit.tasks` → 分解
5. Implement：`/speckit.implement` → 代码

### OpenSpec（既有项目）

双文件夹架构：
```
openspec/
├── specs/      ← Current truth (stable)
└── changes/    ← Proposals (temporary)
```

工作流：Proposal → Review → Apply → Archive

### Specmatic（API 契约）

- **契约即测试（Contract as Test）**：从 OpenAPI spec 自动生成数千个测试
- **契约即桩（Contract as Stub）**：用于并行开发的 mock server
- **向后兼容（Backward Compatibility）**：检测破坏性变更

---

## 编写有效的规范

> 基于对 2,500+ 个 agent 配置文件的分析。
> 来源：[Addy Osmani](https://addyosmani.com/blog/good-spec/)

### 六个核心组成部分

| 组成部分 | 应包含的内容 | 示例 |
|-----------|-----------------|---------|
| **命令** | 带 flag 的可执行命令 | `npm test -- --coverage` |
| **测试** | 框架、覆盖率、位置 | `vitest, 80%, tests/` |
| **项目结构** | 明确的目录 | `src/`、`lib/`、`tests/` |
| **代码风格** | 一个示例胜过大段文字 | 展示一个真实的函数 |
| **Git 工作流** | 分支、commit、PR 格式 | `feat/name`、conventional commits |
| **边界** | 权限层级 | 见下文 |

### 权限层级

| 层级 | 符号 | 用于 |
|------|--------|---------|
| 总是执行 | ✅ | 安全操作，无需审批（lint、format） |
| 先询问 | ⚠️ | 高影响变更（删除、发布） |
| 绝不执行 | 🚫 | 硬性禁止（提交 secrets、强推 main） |

### 指令的诅咒

> ⚠️ 研究表明，**指令越多 = 对每一条的遵守度越差**。
>
> 解决方案：每个任务只投喂相关的规范片段，而非整份文档。

### 单体式规范 vs 模块化规范

| 项目规模 | 方法 |
|--------------|----------|
| 小型（<10 个文件） | 单一规范文件 |
| 中型（10-50 个文件） | 分节规范，按任务投喂 |
| 大型（50+ 个文件） | 按领域进行 sub-agent 路由 |

---

## 组合模式

按场景推荐的技术栈：

| 场景 | 推荐技术栈 | 备注 |
|-----------|-------------------|-------|
| 单人 MVP | SDD + TDD | 开销最小，专注质量 |
| 5-10 人团队，全新项目 | Spec Kit + TDD + BDD | 治理 + 质量 + 协作 |
| 微服务 | CDD + Specmatic | 契约优先，并行开发 |
| 既有 SaaS（100+ 功能） | OpenSpec + BDD | 变更追踪，无规范漂移 |
| 高复杂度 / 合规 | BMAD + Spec Kit + Specmatic | 完整治理 + 契约 |
| LLM 原生产品 | Eval-Driven + Multi-Agent | 自我改进系统 |

---

## 速查表

| 方法论 | 层级 | 主要关注点 | 最佳场景 | 学习曲线 |
|-------------|-------|---------------|--------------|----------------|
| BMAD | 编排 | 治理 | 高复杂度、稳定需求 | 高 |
| SDD | 规范 | 契约 | 任意 | 中 |
| Doc-Driven | 规范 | 对齐 | 任意 | 低 |
| Req-Driven | 规范 | 上下文 | 复杂需求、众多产物 | 中 |
| DDD | 规范 | 领域 | 复杂业务领域 | 极高 |
| BDD | 行为 | 协作 | 多角色利益相关方参与 | 中 |
| ATDD | 行为 | 合规 | 受监管、明确的验收标准 | 中 |
| CDD | 行为 | API | 服务边界、并行团队 | 中 |
| FDD | 交付 | 功能 | 功能团队、并行交付 | 中 |
| Context Eng. | 交付 | AI 会话 | 任意 | 低 |
| TDD | 实现 | 质量 | 任意 | 低 |
| Eval-Driven | 实现 | AI 输出 | 任意 | 中 |
| Multi-Agent | 实现 | 复杂度 | 任意 | 中 |
| Iterative | 优化 | 精炼 | 任意 | 低 |
| Prompt Eng. | 优化 | 基础 | 任意 | 极低 |

---

## 来源

### 官方文档（Tier 1）

- Anthropic：[Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- Anthropic：[Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic：[Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- GitHub：[Spec-Driven Development Toolkit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- Microsoft：[Spec-Driven Development with Spec Kit](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)

### 方法论参考（Tier 2）

**SDD & Spec-First**
- Addy Osmani：[How to Write Good Specs for AI Agents](https://addyosmani.com/blog/good-spec/)
- Addy Osmani：[My AI Coding Workflow in 2026](https://addyosmani.com/blog/ai-coding-workflow/) — 端到端工作流：spec-first、上下文打包、TDD、git 检查点
- Martin Fowler：[SDD Tools Analysis](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- InfoQ：[Spec-Driven Development](https://www.infoq.com/articles/spec-driven-development/)
- Kinde：[Beyond TDD - Why SDD is the Next Step](https://kinde.com/learn/ai-for-software-engineering/best-practice/beyond-tdd-why-spec-driven-development-is-the-next-step/)
- Tessl.io：[Spec-Driven Dev with Claude Code](https://tessl.io/blog/spec-driven-dev-with-claude-code/)

**BMAD**
- GMO Recruit：[The BMAD Method](https://recruit.group.gmo/engineer/jisedai/blog/the-bmad-method-a-framework-for-spec-oriented-ai-driven-development/)
- Benny Cheung：[BMAD - Reclaiming Control in AI Dev](https://bennycheung.github.io/bmad-reclaiming-control-in-ai-dev)
- GitHub：[BMAD-AT-CLAUDE](https://github.com/24601/BMAD-AT-CLAUDE)

**TDD with AI**
- Steve Kinney：[TDD with Claude](https://stevekinney.com/courses/ai-development/test-driven-development-with-claude)
- Nathan Fox：[Taming GenAI Agents](https://www.nathanfox.net/p/taming-genai-agents-like-claude-code)
- Alex Op：[Custom TDD Workflow Claude Code](https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/)

**BDD & DDD**
- Alex Soyes：[BDD Behavior-Driven Development](https://alexsoyes.com/bdd-behavior-driven-development/)
- Alex Soyes：[DDD Domain-Driven Design](https://alexsoyes.com/ddd-domain-driven-design/)
- Inflectra：[Behavior-Driven Development](https://www.inflectra.com/Ideas/Topic/Behavior-Driven-Development.aspx)

**Context Engineering**
- Intuition Labs：[What is Context Engineering](https://intuitionlabs.ai/articles/what-is-context-engineering)
- Manus.im：[Context Engineering for AI Agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)

**Eval-Driven & Multi-Agent**
- Fireworks AI：[Eval-Driven Development with Claude Code](https://fireworks.ai/blog/eval-driven-development-with-claude-code)
- Brandon Casci：[Transform into a Dev Team using Claude Code Agents](https://www.brandoncasci.com/2025/09/21/how-to-transform-yourself-into-a-dev-team-using-claude-codes-ai-agents.html)
- The Unwind AI：[Claude Code's Multi-Agent Orchestration](https://www.theunwindai.com/p/claude-code-s-hidden-multi-agent-orchestration-now-open-source)

### 工具文档（Tier 1）

- OpenSpec：[github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)
- Spec Kit：[github.com/github/spec-kit](https://github.com/github/spec-kit)
- Specmatic：[specmatic.io](https://specmatic.io)
- Specmatic Article：[Spec-Driven Development with GitHub Spec Kit and Specmatic MCP](https://specmatic.io/article/spec-driven-development-api-design-first-with-github-spec-kit-and-specmatic-mcp/)

### 其他参考

- Talent500：[Claude Code TDD Guide](https://talent500.com/blog/claude-code-test-driven-development-guide/)
- Testlio：[Acceptance Test-Driven Development](https://testlio.com/blog/what-is-acceptance-test-driven-development/)
- Monday.com：[Feature-Driven Development](https://monday.com/blog/rnd/feature-driven-development-fdd/)
- Paddo.dev：[Ralph Wiggum Autonomous Loops](https://paddo.dev/blog/ralph-wiggum-autonomous-loops/)
- Walturn：[Prompt Engineering for Claude](https://www.walturn.com/insights/mastering-prompt-engineering-for-claude)
- AWS：[Prompt Engineering with Claude on Bedrock](https://aws.amazon.com/blogs/machine-learning/prompt-engineering-techniques-and-best-practices-learn-by-doing-with-anthropics-claude-3-on-amazon-bedrock/)

---

## 另请参阅

- [workflows/tdd-with-claude.md](../workflows/tdd-with-claude.md) — 实用 TDD 指南
- [workflows/spec-first.md](../workflows/spec-first.md) — 规范优先开发
- [workflows/plan-driven.md](../workflows/plan-driven.md) — 使用 /plan 模式
- [workflows/iterative-refinement.md](../workflows/iterative-refinement.md) — 迭代优化循环
- [ultimate-guide.md#912](../ultimate-guide.md) — 第 9.12 节摘要
