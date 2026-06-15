---
title: "Context Engineering"
description: "Comprehensive guide to filling Claude's context window with the right information at the right time — configuration hierarchy, budget management, modular architecture, team assembly, and quality measurement"
tags: [context, configuration, architecture, team, advanced]
---

# Context Engineering

> **置信度**：第 1 级 —— 基于官方文档、实测生产数据以及社区验证。
>
> **最后更新**：2026 年 3 月

"Context engineering is the art of filling the context window with the right information at the right time." —— Andrej Karpathy

本指南涵盖从上下文预算背后的 token 数学，到构建模块化、团队规模的配置系统的方方面面。它是终极指南中更宏观的配置章节的补充——那些章节展示单项技术，而本文档展示如何将它们组合成一套连贯的系统。

---

## 目录

1. [什么是 Context Engineering](#1-what-is-context-engineering)
2. [上下文预算](#2-the-context-budget)
3. [配置层级](#3-configuration-hierarchy)
4. [模块化架构](#4-modular-architecture)
5. [团队组建](#5-team-assembly)
6. [上下文生命周期](#6-context-lifecycle)
7. [质量度量](#7-quality-measurement)
8. [上下文精简技术](#8-context-reduction-techniques)
9. [成熟度评估](#9-maturity-assessment)
10. [Token 审计工作流](#10-token-audit-workflow)
11. [研究模式](#11-research-patterns-what-the-literature-shows)
12. [注意力机制与可靠性](#17-attention-mechanics--reliability)
13. [Token 压缩工具](#18-token-compression-tools)

---

## 1. What is Context Engineering

### 定义

Andrej Karpathy 提出了这句话：**"Context engineering is the art of filling the context window with the right information at the right time."**

这一句话包含三个并不显而易见的要求：

- **填充（Filling）**：上下文窗口应当被有意识地填充，而非随意堆砌。让它大部分空着会浪费模型的能力；让它杂乱地塞满则会浪费你的 token 并降低输出质量。
- **正确的信息（Right information）**：并非所有信息都同等重要。架构决策比代码风格偏好更有价值。否定型约束（"绝不向客户端返回原始 SQL 错误"）比愿景型目标（"写干净的代码"）更具可操作性。
- **正确的时机（Right time）**：针对后端代码的路径作用域规则，在编辑前端组件时毫无价值。永远加载所有内容是一种偷懒的做法，会损害规则的遵循度。

### Prompt Engineering 与 Context Engineering

这两个术语常被混为一谈，但其区别很重要：

| 维度 | Prompt Engineering | Context Engineering |
|-----------|-------------------|---------------------|
| 范围 | 单次请求 | 整个会话或系统 |
| 持续时间 | 单次交互 | 跨交互持久存在 |
| 投入方式 | 每次请求逐一打磨 | 前期系统设计 |
| 规模 | 个人 | 团队级或组织级 |
| 产物 | 一个 prompt 字符串 | 一套配置系统 |

**Prompt engineering** 关注的是为单个任务构造正确的问题。**Context engineering** 则是确保 Claude 在任何任务开始之前就具备正确背景知识的系统。你可以在糟糕的 context engineering 之上写出出色的 prompt，但结果依然平庸——因为模型缺乏对你的项目、约定和约束的结构性理解。

一个实用的类比：prompt engineering 是给承包商写一封好邮件。context engineering 则是入职流程、代码风格指南、架构文档以及团队规范，它们确保承包商在读到任何一封邮件之前就理解了项目。

### Context Engineering 与 Context Optimization

这两个术语都出现在文献中，有时被交替使用，但它们并不相同。

| 维度 | Context Engineering | Context Optimization |
|-----------|--------------------|--------------------|
| 核心问题 | 上下文中应该包含哪些信息？ | 能让结果最优的高信号 token 最小集合是什么？ |
| 目标 | 完整性与正确性 | 效率与信号密度 |
| 方法 | 识别模型需要知道什么 | 移除一切它不需要知道的内容 |
| 失败模式 | 缺失关键信息 | 过头——无关内容过多 |
| 输出 | 一套上下文系统 | 一份精简、高保真的 prompt 或配置 |

一个有用的心智模型：context engineering 回答"包含什么"，context optimization 回答"砍掉什么"。

实践中两者都要做。工程化这一步构建完整图景：架构决策、约定、约束。优化这一步对其进行裁剪：移除冗余、压缩冗长规则、归档过时条目、对子系统专属内容做路径作用域。第 8 节中的精简技术就是优化这一步。

**综合（synthesis）与推理（reasoning）**

还有一个值得明确命名的相关区别：

- **上下文综合（context synthesis）**是有状态且迭代的。它跨会话积累知识，在约定变化时更新，并反映项目历史。CLAUDE.md 就是上下文综合。
- **推理（reasoning）**是短暂且可丢弃的。每一步推断都使用上下文来产生输出，然后丢弃中间状态。Claude 的思维链就是推理。

把推理产物（中间想法、调试轨迹、错误输出）当作上下文综合材料是一个常见错误。它会用短暂状态污染上下文，加速上下文腐化（context rot）。要把应当持久保留的内容（综合）与应当丢弃的内容（推理噪声）分开。

### 为什么它很重要

LLM 是上下文窗口计算机。输出的质量受限于输入的质量。这不是一个软性论断——它有坚实的技术基础：

1. 模型在会话之间没有持久记忆（在没有显式工具的情况下）。除非有意提供上下文，否则每次会话都从零开始。
2. 模型无法推断未陈述的约定。如果你想要 TypeScript interface 而不是 `type` 别名，就必须明说。如果你想要错误在抛出前先被记录，就必须明说。
3. 模型对指令的位置和措辞很敏感。埋在一个 500 行 CLAUDE.md 第 400 行的指令，比放在前 50 行的指令更不容易被遵循。

投入 context engineering 的团队一致反馈：修订轮次更少、约定遵循度更好、输出更可预测。这项投入是前置的（构建系统），但回报会在每一次交互中复利累积。

一个有用的诊断式重构思路：**大多数 AI 输出失败是上下文失败，而非模型失败。**当 Claude 生成泛泛的回答、忽略某个约定，或产出与你技术栈不匹配的代码时，模型几乎从不是坏掉了——而是它收到的上下文不完整、自相矛盾，或缺少在正确时机出现的正确信息。这一重构思路把排错从"AI 不擅长这个"转向"上下文里缺了什么？"

### 三个层级

Claude Code 中的 context engineering 跨越三个不同的层级运作：

| 层级 | 机制 | 范围 | 加载时机 |
|-------|-----------|-------|-------------|
| **全局配置** | `~/.claude/CLAUDE.md` | 所有项目 | 始终 |
| **项目配置** | `./CLAUDE.md` + 路径作用域模块 | 当前项目 | 每次会话 |
| **会话** | 内联指令、`/add`、flag | 仅当前会话 | 运行时 |

每个层级都有不同的权衡。全局配置始终生效，但无法引用项目专属细节。会话指令灵活但短暂。项目配置是主力：结构化、有版本管理、可审查。

良好的 context engineering 意味着把每一条信息放在正确的层级——而不是把所有东西塞进一个文件，也不是把关键知识留在会话层，让它在每次对话后蒸发。

### 静态上下文与动态上下文

上面的三层系统是*静态上下文*——在会话开始前就组装好、并在整个过程中保持稳定的配置文件。Claude Code 主要是一个静态上下文系统，这也是为什么 CLAUDE.md 结构和路径作用域如此重要。

当你转向 agent 工作流时，会出现第二个类别：*动态上下文*，它在推理时随着 agent 的运作而组装。

| 类型 | 如何组装 | Claude Code 中的示例 |
|------|--------------|-------------------------|
| **静态** | 会话前，来自文件 | CLAUDE.md、路径作用域模块、skills |
| **动态** | 运行时，来自工具 | 工具输出、文件读取、web 抓取、MCP 数据 |

实践中，每一次 Claude Code 会话都同时使用两者。静态上下文（你的配置）设定行为边界；动态上下文（Claude 读取的文件、它处理的工具结果）为每个任务提供具体信息。Context engineering 涵盖两者，但失败模式不同：静态上下文问题表现为持续违反约定；动态上下文问题表现为 Claude 在任务中途基于过时或不完整的信息行事。

对于构建自动化流水线和 agent 的团队，Anthropic 2025 年 9 月的工程博文 ["Effective context engineering for AI agents"](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) 深入讨论了动态这一侧。

### 为什么上下文腐化是结构性的，而非偶然的

Transformer 模型会对所有 token 两两进行注意力计算。这意味着上下文窗口中注意力关系的数量按 n² 增长，而非 n。把上下文长度翻倍，模型必须权衡的关系数量就翻了四倍。在 200K token 时，这意味着数十亿次的两两计算，模型的注意力会变得越来越分散。

这不是未来模型能消除的 bug。它是架构本身的后果。上下文腐化——随着上下文增长，指令遵循度逐步退化——在结构上就已注定。其含义是：你无法靠更大的上下文窗口来解决上下文腐化。你解决它的办法是保持上下文精简，并在恰当的时机即时加载信息。

**即时检索与预加载**

给 Claude 提供所需信息有两种策略：

| 策略 | 机制 | 何时使用 |
|----------|-----------|-------------|
| **预加载（RAG）** | 在推理前检索并注入所有可能相关的上下文 | 已知、稳定的上下文需求 |
| **即时检索（Just-in-time）** | 按需检索上下文，恰好在需要时、且仅在需要时 | 动态、任务专属的上下文 |

预加载是我们熟悉的 RAG 模式：构建检索索引，预先把相关片段拉进 prompt。当你事先知道模型会需要哪些信息时，它行之有效。

即时检索实现起来更费力，但在规模上更有效：模型在任务需要时通过工具调用、MCP server 或文件读取动态检索信息。上下文中只有当前步骤所需的信息。

Claude Code 的行为体现了这一模式：CLAUDE.md 在前期加载（预加载，始终相关），而文件内容和工具结果在推理时通过 `read_file`、`glob`、`grep` 和 MCP 调用检索。glob 和 grep 工具就是 JIT 检索层。它们只在任务触及某些文件时，才把这些文件的具体内容放入上下文。

**Memory tool（beta）**

从 Claude Sonnet 4.5 起，Anthropic 发布了公开 beta 版的 Memory tool。它让 Claude 能够跨会话存储和检索持久事实，而无需手动管理 CLAUDE.md。该工具维护一个结构化的知识库，Claude 在需要相关上下文时进行查询。

这与 CLAUDE.md 不同：CLAUDE.md 是静态配置（始终加载），而 Memory tool 是动态检索（按需查询）。对于构建 agent 的团队，Memory tool 减少了在配置文件中手动编码知识的需要。

**长任务中的思维链**

思维链（CoT）提示能改善模型在孤立任务上的推理。然而 Anthropic 的工程数据显示，它在长 agentic 任务中可能损害性能。其机制是：CoT 会生成额外的 token，从而拉长上下文，进而为后续步骤加速上下文腐化。在跨越 20 次以上工具调用的任务中，这种效应是可测量的。

实用规则是：把 CoT 用于复杂的孤立推理步骤，而不要把它当作 agentic 工作流的一揽子策略。在长流程中，优先使用压缩后的中间输出，而非冗长的推理轨迹。

---

## 2. The Context Budget

### Token 数学

一个中型项目的具体基线：

| 来源 | 典型 token 范围 |
|--------|---------------------|
| 全局 CLAUDE.md | 1,000 – 3,000 tokens |
| 项目 CLAUDE.md（根目录） | 2,000 – 8,000 tokens |
| 路径作用域模块（全部激活） | 1,000 – 5,000 tokens |
| 导入的 skills / commands | 500 – 3,000 tokens |
| **始终生效的上下文总计** | **~5,000 – 20,000 tokens** |

Claude Sonnet 4.6 拥有 200K token 的上下文窗口。这意味着即便是一个较大的始终生效配置预算（20K tokens），也只占窗口约 10%——为实际工作留出 180K tokens：代码文件、对话历史、工具输出。

实用规则是：**始终生效的上下文应保持在上下文窗口的 5% 以下。**超过这个比例，你就在挤占实际的任务内容，而后者按 token 计算比常驻指令更重要。

### 150 条指令上限

来自运行大型 CLAUDE.md 文件团队的经验观察：超过约 150 条不同的规则后，模型会开始选择性地忽略其中一些。这不是一个硬性截断——它取决于规则的复杂度、重叠程度和位置——但它是一个可靠的信号，表明规则更多并不等于遵循度更好。

其机制是注意力扩散：当一个 prompt 包含数百条可能相关的约束时，模型的注意力会被分散到它们之间。高显著性的规则（较新的、措辞强烈的、靠前放置的）会挤掉低显著性的规则。

HumanLayer 的生产数据显示，拥有结构化上下文的团队——更少、更具体、按层级组织的规则——比规则是无差别长列表的团队，遵循度高出 15-25%。

含义是：**规则质量胜过规则数量。**二十条具体、可操作的规则胜过两百条泛泛的愿景型规则。

### 遵循度随文件大小的退化

```
Lines in CLAUDE.md    Adherence (estimated)
─────────────────     ─────────────────────
1 – 100               ~95%
100 – 200             ~88%
200 – 400             ~75%
400 – 600             ~60%
600+                  ~45% and falling
```

这些是估计的基线，而非保证。通过确保任意时刻只有相关规则进入上下文，路径作用域和模块化架构可以在更大的总规则数下维持更高的遵循度。

### 上下文过载的迹象

当始终生效的上下文变得过大或过于嘈杂时，你会看到可预测的失败模式：

- **规则失声**：Claude 一贯遵循 80% 的约定，却忽略某些本应适用的特定规则。
- **行为自相矛盾**：Claude 在某些文件中应用某条规则，在其他文件中却不应用；或根据措辞应用相互矛盾的规则。
- **首次响应变慢**：模型在生成输出前要花更多时间处理庞大的上下文（在简单任务上表现为更长的延迟）。
- **泛泛的输出**：Claude 不再应用项目专属的模式，而是退回到通用最佳实践——这是项目上下文没有被保留的信号。

当你看到这些模式时，诊断方案是：运行一次上下文审计（见第 7 节），而不是增加更多指令。

### MECW：最大有效上下文窗口

宣传的上下文窗口与有效的上下文窗口不是同一个数字。企业级 context engineering 部署一致发现，明显的准确率退化在达到宣称上限之前就已开始。来自生产经验的常被引用的数字是：约为宣传上限的 92%。

对于 Claude Opus 4（宣传 200K），这把实际上限定在约 185K token，超过此值后复杂推理任务的准确率会出现可测量的退化。其机制就是第 1 节（为什么上下文腐化是结构性的）所述的 n² 注意力缩放：随着上下文增长，注意力运算按平方级增长，而窗口中部位置获得的有效权重逐渐减少。

在重度上下文负载下，上下文腐化会使窗口中部位置的准确率下降 30% 以上。其实际含义是：一个内容高质量、维护良好的 128K token 上下文窗口，胜过一个塞满过时、堆积内容的 1M token 窗口。1M 窗口并不能消除该问题；它只是延缓问题，同时抬高每次请求的成本。

"我是不是干脆用 1M 上下文窗口就好了？"这个问题本质上是关于信噪比，而非能力。一个堆积了工具输出噪声、过期对话轮次和冗余指令的更大窗口，并不比一个更小、经过精心整理的窗口更强大。它只是更贵、更慢。

**实用的 MECW 目标**：

| 窗口 | 宣传值 | 实际上限（92%） | 腐化退化准确率的临界点 |
|--------|-----------|------------------------|--------------------------|
| Claude Sonnet 4.6 | 200K | ~184K | ~150K+ |
| Claude Opus 4 | 200K | ~185K | ~150K+ |

这些是工程估计值，而非保证值。把它们当作规划数字：如果你的会话经常逼近 150K token，那么就该在准确率成为问题之前——而非之后——实施 compaction、分级卸载或路径作用域。

### 路径作用域与预算效率

路径作用域是降低始终生效上下文的最有效的单项技术。你不再为代码库的所有部分加载所有规则，而只加载与当前上下文中文件相关的规则。

一个没有路径作用域的典型项目：

```
Always-on: root CLAUDE.md with backend + frontend + database + API rules = 8,000 tokens
```

同一个项目采用路径作用域后：

```
Always-on: root CLAUDE.md with shared rules = 2,000 tokens
Active when in src/api/: api module = +1,500 tokens
Active when in src/components/: frontend module = +1,200 tokens
Active when in prisma/: database module = +800 tokens
```

结果：始终生效的上下文减少 40-50%，且覆盖范围无损失。每个子系统都获得其完整的规则集，但只在工作于该子系统时才生效。

---

## 3. 配置层级

### 三层堆栈

```
┌──────────────────────────────────────────────┐
│  Global (~/.claude/CLAUDE.md)                │
│  Identity, tone, universal tools, cross-      │
│  project conventions                          │
├──────────────────────────────────────────────┤
│  Project (./CLAUDE.md + path modules)         │
│  Architecture decisions, stack conventions,   │
│  team rules, deployment procedures            │
├──────────────────────────────────────────────┤
│  Session (inline instructions, flags)         │
│  Ad-hoc overrides, experiment constraints,    │
│  one-off task parameters                      │
└──────────────────────────────────────────────┘
```

后面的层会覆盖前面的层。一条 session 指令可以覆盖项目规则；一条项目规则可以覆盖全局默认值。这为你提供了应急出口，而无需对共享配置做永久性更改。

### 全局配置

**位置**：`~/.claude/CLAUDE.md`

**应放在这里的内容**：
- 身份和沟通风格偏好
- 通用工具偏好（RTK、首选 CLI 工具）
- 跨项目的编码约定（commit message 格式、PR 风格）
- 适用于所有场景的安全约束
- 语气和输出格式的默认值

**不应放在这里的内容**：
- 项目特定的架构决策
- 技术栈特定的规则（React hooks、Prisma 模式）
- 部署或环境的具体细节
- 任何因项目而异的内容

**规模目标**：将全局配置控制在 200 行以内。这是你在每个项目的每次 session 中都要承担的常驻开销。让它臃肿会对所有项目造成同等程度的伤害。

```markdown
# Example: Minimal effective global CLAUDE.md

## Communication
- Respond in the same language the user writes in
- Prefer direct answers over preamble
- No em dashes in written output

## Git
- Commit messages: imperative mood, <72 chars subject line
- Never commit without being asked

## Code Style
- Prefer explicit error handling over silent failure
- Add TODO comments only when referencing a tracked issue
```

### 项目配置

**位置**：`./CLAUDE.md`（项目根目录）

**应放在这里的内容**：
- 正在使用的技术栈及其版本
- 架构决策及其依据
- 针对本代码库的团队约定
- 文件组织模式
- 测试要求和覆盖率目标
- 针对本项目的安全约束
- 用于子系统模块的路径作用域导入

**结构模式**：

```markdown
# Project: [Name]

## Stack
- Language: TypeScript 5.3
- Framework: Next.js 14 (App Router)
- Database: PostgreSQL 16 via Prisma
- Testing: Vitest + React Testing Library

## Architecture
- Server Components by default; use `"use client"` only when interactivity requires it
- API routes in /app/api; no business logic in route handlers
- Business logic in /lib/services; each service is a plain function module

## Conventions
- File naming: kebab-case for files, PascalCase for React components
- Error handling: wrap service calls in Result<T, E> pattern (see lib/result.ts)
- Never expose raw database IDs in API responses; use UUIDs

## Path-Scoped Modules
@src/api/CLAUDE-api.md
@src/components/CLAUDE-components.md
@prisma/CLAUDE-db.md
```

**"金发姑娘"难题：抽象高度**

在生产环境的 CLAUDE.md 文件中，有两种失效模式反复出现：

**太模糊**："编写整洁的代码"、"遵循最佳实践"、"保持函数简短"。这些指令会从模型旁滑过而不改变其行为。模型早在你的指令之前就已经有了"整洁代码"的概念，它会默认采用那个概念，而那未必符合你的项目需要。空洞的理想化规则会被忽略。

**太琐碎**："使用 2 个空格缩进"、"在 import 块后加一个空行"、"私有方法以下划线开头"。这些是 linter 规则，不是认知决策。它们应放在 `.eslintrc`、`.editorconfig` 或 `prettier.config.js` 中，由工具确定性地强制执行，而不是由 LLM 概率性地执行。把它们放进 CLAUDE.md 会浪费上下文预算，并产生不可靠的执行效果。

**有效的抽象高度**：捕捉那些模型在没有指令时会做出不同选择的决策。检验标准是："如果 Claude 没有任何项目上下文，它在这里是否会合理地做出不同的事情？"如果是，这条规则就属于 CLAUDE.md。如果答案是理想化的空话，删掉它。如果有 linter 能强制执行它，删掉它。

| 抽象高度 | 示例 | 裁定 |
|----------|---------|---------|
| 太模糊 | "编写整洁的代码" | 删除 —— 模型会忽略，不改变行为 |
| 太模糊 | "遵循安全最佳实践" | 删除 —— 替换为具体约束 |
| 有效 | "切勿在 API 响应中暴露原始数据库 ID；使用 UUID" | 保留 —— 具体，否则模型会用默认做法 |
| 有效 | "服务函数使用 Result<T, E> 模式，而非 try/catch" | 保留 —— 具体，覆盖了常见默认做法 |
| 太琐碎 | "使用 2 个空格缩进" | 删除 —— 交给 Prettier |
| 太琐碎 | "为每个函数添加 JSDoc 注释" | 删除 —— 交给 lint 规则 |

架构选择、质量标准，以及明确的"不要做什么以及为什么"规则，才是有效的抽象高度。理想化的空话和机械性的细节都是噪音。

### Session 配置

**机制**：当前 session 的内联指令、`/add-dir`，或系统提示词标志。

**应放在这里的内容**：
- 一次性任务约束（"本次重构中，不要改动公共 API 接口"）
- 实验参数（"在这个文件里使用我正在测试的新错误格式"）
- 调试约束（"本次 session 记录每一次工具调用"）
- 对项目约定的临时覆盖

Session 指令不会被持久化。它们会在 session 结束时消失。任何你发现自己在多次 session 中反复给出的指令，都应放进项目配置，而非 session 层。

### 决策树：这条规则该放在哪里？

```
Is this rule relevant to every project I work on?
├── Yes → Global CLAUDE.md
└── No ↓

Is this rule relevant to specific files or subsystems?
├── Yes → Path-scoped module (e.g., src/api/CLAUDE-api.md)
└── No ↓

Is this rule relevant to the whole project?
├── Yes → Project CLAUDE.md (root)
└── No ↓

Does this rule apply only to the current task or session?
├── Yes → Inline session instruction
└── No → Revisit: is it really a rule, or just a one-time preference?
```

### 导入链与覆盖语义

导入链的流向是：`global → project root → path-scoped modules → session`。

当存在冲突时：
- 更具体的覆盖更不具体的（路径作用域胜过根，根胜过全局）
- 在同一层级，后声明的胜过先声明的
- Session 指令覆盖所有持久化配置

**实际示例**：你的全局配置说"使用两个空格缩进"。你的项目配置说"Python 使用四个空格缩进"。你的 session 说"匹配现有文件的风格"。本次 session 中 session 指令胜出，Python 文件默认四个空格，其他一切默认两个空格。

明确记录你的覆盖。一条未记录、且与父级规则矛盾的覆盖，会在审计时造成困惑。

---

## 4. 模块化架构

### 单体配置的问题

一个 600 行、毫无结构的 CLAUDE.md 是生产环境中最常见的失效模式。症状包括：

1. 来自不同领域的规则混杂在一起 —— 一条 React 组件约定紧挨着一条数据库迁移规则
2. Claude 会读完全部 600 行，但注意力预算意味着第 5 页上的规则比第 1 页上的规则权重更低
3. 新团队成员无法快速找到相关规则
4. 更新时需要扫描整个文件，才能在编辑前找到相关规则
5. 随着文件增长，遵守度逐步下降

解决方案是架构性的：把单体拆解为聚焦的模块，然后用路径作用域，仅在相关时才加载每个模块。

### 路径作用域模式

**机制**：Claude Code 支持在 CLAUDE.md 中使用 `@path/to/file.md` 导入。当路径作用域导入处于激活状态时，只有当指定路径下的文件进入作用域时，该模块中的规则才会被添加到上下文中。

**文件结构**：

```
project/
├── CLAUDE.md                       # Root config, shared rules + @imports
├── src/
│   ├── api/
│   │   └── CLAUDE-api.md           # API-specific rules
│   ├── components/
│   │   └── CLAUDE-components.md    # React/UI-specific rules
│   └── lib/
│       └── CLAUDE-lib.md           # Utility/shared library rules
├── prisma/
│   └── CLAUDE-db.md                # Database and migration rules
└── tests/
    └── CLAUDE-tests.md             # Testing conventions
```

**带导入的根 CLAUDE.md**：

```markdown
# Project Config

## 共享规则
[...shared rules here...]

## 子系统模块
@src/api/CLAUDE-api.md
@src/components/CLAUDE-components.md
@src/lib/CLAUDE-lib.md
@prisma/CLAUDE-db.md
@tests/CLAUDE-tests.md
```

**路径作用域模块示例**（`src/api/CLAUDE-api.md`）：

```markdown
# API Rules

- Route handlers in /app/api only; no business logic inline
- All endpoints must validate input with Zod before processing
- Error responses use the standard format: { error: string, code: string }
- Never log request bodies that may contain PII; log IDs only
- Rate limiting headers must be present on all public endpoints
- Authentication: verify JWT in middleware, not in individual handlers
```

该模块的 6 条规则仅在 `src/api/` 中工作时才进入上下文。在 `src/components/` 中工作时，它们不会消耗任何上下文预算。

### Skills 与 Rules 的对比

这一区别被严重低估，但却至关重要：

| 维度 | Rules | Skills |
|-----------|-------|--------|
| 本质 | 约束、标准、规范 | 能力、流程、工作流 |
| 何时生效 | 始终强制执行 | 按需调用 |
| 示例 | "Never use `any` in TypeScript" | "如何新增一个 API 端点" |
| 位置 | CLAUDE.md | `.claude/skills/` |
| Token 成本 | 始终占用 | 仅在调用时加载 |

**Rules** 定义 Claude 在默认情况下应该做什么、不应该做什么。它们设定了可接受输出的边界。

**Skills** 定义如何完成需要了解项目特定模式的复杂多步骤任务。它们在 Claude 需要执行某类特定任务时才加载，而非始终加载。

**实践示例**：一条规则说"API 端点必须有 Zod 校验"。而一个 skill 则说"这是在本项目中创建新 API 端点的分步模式，包括 Zod schema 模式、错误处理包装器、auth 中间件 hook，以及测试文件结构。"

把端点创建流程放进规则，意味着每个会话都要加载 40 行流程性指令，哪怕你根本不在创建端点。而把它放进 skill，则意味着只在创建端点时才加载这 40 行内容。

**Rule**：`Never expose raw database IDs in API responses.`
**Skill**：`How to generate and use UUID-based public identifiers for entities.`

**社区 skill 库**

预构建的 skill 集合可以降低模块化上下文工程的前期投入：

- `anthropics/claude-code-skills`（官方）：由 Anthropic 维护的 skill 模板，覆盖常见开发工作流
- `ibelick/ui-skills`：面向前端项目的 UI 组件与设计系统 skill

这些都可以克隆、检视，并按你的项目规范进行改造，而不必从零构建。把它们当作起点——fork 并修改以匹配你的技术栈和命名规范，而不要原样照搬。

### 渐进式披露（Progressive Disclosure）

核心原则：不要一次性全部加载。只加载当前任务所需的内容。

**核心配置（始终加载）**：
- 架构决策及其理由
- 编码标准与命名规范
- 安全约束
- 工具偏好

**上下文模块（按任务加载）**：
- 部署流程（部署时加载）
- API 模式（在 API 层工作时加载）
- 测试模板（编写测试时加载）
- 数据库迁移流程（涉及 schema 时加载）

**使用 skills 的实现模式**：

```
.claude/
├── skills/
│   ├── deploy-production.md      # Loaded when: "deploy this"
│   ├── add-api-endpoint.md       # Loaded when: "add endpoint for X"
│   ├── write-migration.md        # Loaded when: "add DB column"
│   └── create-component.md      # Loaded when: "create component for X"
```

每个 skill 文件都包含带有项目特定模式的分步流程。Claude 在检测到对应任务类型时加载它，而非主动加载。

**MCP 工具数量与上下文预算**

MCP 服务器会将工具定义注入系统提示。每个服务器都会加入它的工具 schema，这些 schema 在任何用户内容出现之前就已消耗上下文预算。Anthropic 的工程指南建议：

- 每个项目激活的 MCP 服务器少于 10 个
- 所有激活服务器的工具总数少于 80 个

超过这些阈值后，工具定义的开销会明显减少可用于实际任务内容的 token。当工具数量达到 80 以上时，你仅在工具 schema 上就要烧掉 15-20K token——这些预算本可用于代码上下文、对话历史和文件内容。

渐进式披露原则对 MCP 服务器同样适用，就像对规则一样。应按上下文有选择地加载 MCP 服务器，而不是为每个项目激活所有可用服务器：

```json
{
  "mcpServers": {
    "database": { },
    "github": { }
  }
}
```

要抵制那种"以防万一"把每个可用 MCP 服务器都加进项目配置的做法。每个未使用却被加载的服务器都是纯粹的开销。如果某个服务器在项目中不到 20% 的会话里用到，它就不应出现在默认的项目配置中。

### 反模式：单体式的 CLAUDE.md

**它长什么样**：

```markdown
# CLAUDE.md (600 lines)

## Rules
1. Use TypeScript
2. No any types
3. Run tests before committing
4. API endpoints need auth
5. Use Prisma for DB queries
6. React components in PascalCase
7. Deploy with ./scripts/deploy.sh
8. Check OWASP Top 10 before shipping
[...492 more rules...]
```

**为什么会失败**：

- 第 1-20 条规则获得约 95% 的注意力权重；第 500 条之后的规则只有约 30%
- 前端开发者要读他们不需要的后端 DB 规则，反之亦然
- 缺乏逻辑分组意味着要找到相关规则就得通读全文
- 新增一条规则需要检查整个文件以排查冲突
- 随着文件不断变大，遵循度会持续下降

**解决方法**：

1. 按领域把规则提取到路径作用域模块中
2. 让根 CLAUDE.md 只保留共享规则 + 导入声明
3. 把流程性知识移到 skills 中
4. 提取后将根 CLAUDE.md 控制在 150 行以内

### 结构性元数据文件

规则与结构是两种不同类型的上下文。把二者混为一谈会产生既大到无法始终加载、又重要到无法跳过的文件。

**规则性上下文**回答的是：*我应该如何在这个项目中工作？* 它存在于 CLAUDE.md 和路径作用域模块中。它相对稳定，且几乎总是相关。

**结构性上下文**回答的是：*这个项目的形态是什么样的？* 有多少个 API 路由、哪些领域有组件、嵌套的 CLAUDE.md 文件位于何处、有多少个 Prisma 模型。这类信息只在实现类任务中才需要——创建新文件、新增路由、在陌生领域中导航——而对调试、文档或代码审查类会话而言毫无意义。

始终加载结构性上下文是在浪费 token。完全不加载则意味着 Claude 在每次实现任务开始时都要手动浏览文件系统，消耗轮次并产生噪声。

模式如下：一个小型、自动生成的 YAML 文件（约 1K token），用于捕获代码库的结构形态，并在 CLAUDE.md 中以指针方式注册，而非自动导入。

**应包含什么**——五个部分，仅此而已：

| 部分 | 内容 | 示例 |
|---------|----------|---------|
| `layers` | 架构层级，含根路径与文件数 | `routers: { root: "src/api", count: 33 }` |
| `component_domains` | 功能领域，含路径与组件数 | `{ name: "chat", count: 66 }` |
| `nested_contexts` | src/ 下所有 CLAUDE.md / AI_INSTRUCTIONS.md，含行数与关注点 | `{ path: "src/server/CLAUDE.md", lines: 45 }` |
| `stats` | 汇总数字：文件总数、测试数、schema 模型数 | `total_ts_files: 543` |
| `key_paths` | Claude 经常搞错的规范路径 | `prisma_schema: "src/server/db/prisma/schema.prisma"` |

把文件控制在 1K token 以下。超过这个量，你就是在添加本应放在实际源文件中的细节。

**指针注册模式**

不要在 CLAUDE.md 中用 `@machine-readable/code-map.yaml` 自动加载该文件。而应将它注册在一个引用表中，告诉 Claude 文件包含什么、何时应该取用它：

```markdown
## Context Indexes (load on demand)

| File | Contents | When to load |
|------|----------|--------------|
| machine-readable/code-map.yaml | Architecture layers (counts + roots), component domains, nested context files, project stats | Before any implementation task: new file, new route, new component |
| machine-readable/ai-config.yaml | Full AI tooling config: rules, skills, commands, agents, hooks | When auditing or modifying AI configuration |
| PROJECT_INDEX.md | Detailed architecture narrative, ADRs, domain glossary | Deep architectural work only |
```

这种模式可以扩展：Claude 在会话开始时读取该表，知道有哪些引用文件存在以及为什么存在，并只在当前任务需要时加载它们。调试会话永远不会触及代码地图。而实现任务只需一次工具调用即可加载它。

**"自动生成"在实践中意味着什么**

生成脚本只应做三件事：对每个层级根目录调用 `readdirSync` 以统计文件数、遍历 src 树以汇总 `.ts`/`.tsx` 文件数，并用 glob 搜索嵌套的 CLAUDE.md 文件来填充 `nested_contexts`。不做 AST 解析，不做数据库查询，不做网络调用。整个脚本在一秒内即可跑完。把它加入你的 `pnpm ai:sync`（或等价）任务中。

关键的设计约束是：**绝不要向该文件添加手工维护的内容。** 一旦这么做，你就有了一个会漂移的文件。自动生成的文件不会谎报代码库的当前状态；而带有手工内容的文件则会、也终将这么做。

**生产示例**（Méthode Aristote EdTech 平台，约 1,300 个源文件）：

```yaml
version: "1.0.0"
architecture: "Client → tRPC → Router → Service → Repository → Prisma"

layers:
  routers:
    root: "src/server/api/routers"
    description: "Tier 1 — Zod validation, delegate to service"
    count: 33
  services:
    root: "src/server/api/services"
    description: "Tier 2 — business logic, enforcePermission()"
    count: 61
  repositories:
    root: "src/server/api/repositories"
    description: "Tier 3 — CRUD Prisma only"
    count: 38

stats:
  total_ts_files: 543
  total_tsx_files: 798
  prisma_models: 48
  unit_tests: 268
```

将该文件注册为指针后，Claude 回答"存在多少个 tRPC router？"只需一次查找，而无需手动遍历 `src/server/api/routers/`。对于"新增一个 payment router"这类实现任务，它在读取任何一个源文件之前就能立即知道正确的根目录、数量以及架构约束。

一个开箱即用的模板可在 [`examples/context-engineering/code-map-template.yaml`](../../examples/context-engineering/code-map-template.yaml) 获取。

---

## 5. 团队组装

### N × M × P 问题

在团队规模下，上下文工程面临一个组合爆炸式的挑战：

- **N 名开发者**：不同的角色、工具、沟通偏好
- **M 个项目**：不同的技术栈、约定、部署目标
- **P 套配置**：每名开发者 × 每个项目都需要一套配置

手动维护 N × M 个独立的 CLAUDE.md 文件是不可持续的。当某条共享约定发生变化时，你需要更新 N × M 个文件。当创建一个新项目时，你要从零开始搭建。当某名开发者转换角色时，你又要重建他们的配置。

解决方案是**基于 profile 的组装**：用一套共享的模块基底，配合各自的 profile 来声明要包含哪些模块、叠加哪些个人偏好。

N × M × P 就变成了 N 个 profile × 1 套共享模块基底 —— 可管理了。

### Profile YAML 结构

每名团队成员都有一份 profile YAML，用声明式的方式指定其配置：

```yaml
# profiles/alice.yaml

profile:
  name: "Alice"
  role: "frontend"
  tools:
    - typescript
    - react
    - tailwind
  conventions:
    - atomic-design
    - accessibility-first
  communication:
    language: "en"
    verbosity: "concise"

modules:
  include:
    - shared/core-rules.md
    - shared/git-conventions.md
    - shared/security-baseline.md
    - frontend/react-patterns.md
    - frontend/tailwind-conventions.md
    - frontend/testing-rtl.md
    - frontend/accessibility-checklist.md
  exclude:
    - backend/database-rules.md
    - backend/api-design.md
    - devops/deployment-procedures.md

overrides:
  - "Prefer named exports over default exports"
  - "Use Radix UI primitives before writing custom components"
```

```yaml
# profiles/bob.yaml

profile:
  name: "Bob"
  role: "backend"
  tools:
    - typescript
    - nodejs
    - postgresql
    - prisma
  communication:
    language: "en"
    verbosity: "detailed"

modules:
  include:
    - shared/core-rules.md
    - shared/git-conventions.md
    - shared/security-baseline.md
    - backend/api-design.md
    - backend/database-rules.md
    - backend/error-handling.md
    - backend/performance-patterns.md
  exclude:
    - frontend/react-patterns.md
    - frontend/tailwind-conventions.md

overrides:
  - "Use structured logging (pino) with request context IDs"
  - "Always measure before optimizing; profile first"
```

### 模块库结构

共享模块库存放在仓库中，并纳入版本控制：

```
.claude/
├── modules/
│   ├── shared/
│   │   ├── core-rules.md           # Universal team standards
│   │   ├── git-conventions.md      # Commit and PR conventions
│   │   ├── security-baseline.md    # Non-negotiable security rules
│   │   └── testing-standards.md   # Coverage and test quality rules
│   ├── frontend/
│   │   ├── react-patterns.md
│   │   ├── tailwind-conventions.md
│   │   ├── testing-rtl.md
│   │   └── accessibility-checklist.md
│   ├── backend/
│   │   ├── api-design.md
│   │   ├── database-rules.md
│   │   ├── error-handling.md
│   │   └── performance-patterns.md
│   └── devops/
│       ├── deployment-procedures.md
│       ├── monitoring-conventions.md
│       └── infrastructure-rules.md
├── profiles/
│   ├── alice.yaml
│   ├── bob.yaml
│   └── carol.yaml
└── scripts/
    └── assemble-context.sh
```

### 组装脚本

组装脚本读取一份 profile，并将其指定的模块拼接为一个 CLAUDE.md：

```bash
#!/usr/bin/env bash
# scripts/assemble-context.sh

set -euo pipefail

PROFILE="${1:-}"
CHECK_MODE="${2:-}"

if [[ -z "$PROFILE" ]]; then
  echo "Usage: ./assemble-context.sh <profile-name> [--check]"
  exit 1
fi

PROFILE_FILE=".claude/profiles/${PROFILE}.yaml"
OUTPUT_FILE="CLAUDE.md"
MODULES_DIR=".claude/modules"

if [[ ! -f "$PROFILE_FILE" ]]; then
  echo "Profile not found: $PROFILE_FILE"
  exit 1
fi

# Parse profile with yq or python
MODULES=$(python3 -c "
import yaml
with open('$PROFILE_FILE') as f:
    profile = yaml.safe_load(f)
for m in profile['modules']['include']:
    print(m)
")

# Assemble output
ASSEMBLED=$(mktemp)

echo "# Claude Code Configuration" > "$ASSEMBLED"
echo "# Generated from profile: $PROFILE" >> "$ASSEMBLED"
echo "# Generated at: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$ASSEMBLED"
echo "" >> "$ASSEMBLED"

while IFS= read -r module; do
  MODULE_PATH="${MODULES_DIR}/${module}"
  if [[ -f "$MODULE_PATH" ]]; then
    echo "## From: ${module}" >> "$ASSEMBLED"
    cat "$MODULE_PATH" >> "$ASSEMBLED"
    echo "" >> "$ASSEMBLED"
  else
    echo "WARNING: module not found: $MODULE_PATH" >&2
  fi
done <<< "$MODULES"

# Append personal overrides
python3 -c "
import yaml
with open('$PROFILE_FILE') as f:
    profile = yaml.safe_load(f)
overrides = profile.get('overrides', [])
if overrides:
    print('## Personal Overrides')
    for o in overrides:
        print(f'- {o}')
" >> "$ASSEMBLED"

if [[ "$CHECK_MODE" == "--check" ]]; then
  if diff -q "$OUTPUT_FILE" "$ASSEMBLED" > /dev/null 2>&1; then
    echo "OK: CLAUDE.md matches profile $PROFILE"
    rm "$ASSEMBLED"
    exit 0
  else
    echo "DRIFT: CLAUDE.md does not match profile $PROFILE"
    diff "$OUTPUT_FILE" "$ASSEMBLED"
    rm "$ASSEMBLED"
    exit 1
  fi
fi

mv "$ASSEMBLED" "$OUTPUT_FILE"
echo "Assembled CLAUDE.md from profile: $PROFILE"
```

**用法**：

```bash
# Generate CLAUDE.md from a profile
./scripts/assemble-context.sh alice

# Check for drift (used in CI)
./scripts/assemble-context.sh alice --check
```

### CI 漂移检测

团队成员会从各自的 profile 重新生成 CLAUDE.md，但基础模块会随时间演进。如果没有漂移检测，开发者可能正运行着一份过时的配置 —— 一份早于某条安全规则新增、或某项约定更新之前的配置。

一个 GitHub Actions 作业可以检测到这种情况：

```yaml
# .github/workflows/context-drift.yml

name: Context Drift Detection

on:
  schedule:
    - cron: '0 9 * * 1'   # Weekly, Monday 9am UTC
  push:
    paths:
      - '.claude/modules/**'

jobs:
  check-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: pip install pyyaml

      - name: Check all profiles for drift
        run: |
          DRIFT=0
          for profile_file in .claude/profiles/*.yaml; do
            profile=$(basename "$profile_file" .yaml)
            echo "Checking profile: $profile"
            if ! ./scripts/assemble-context.sh "$profile" --check; then
              echo "DRIFT detected in profile: $profile"
              DRIFT=1
            fi
          done
          exit $DRIFT

      - name: Notify on drift
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Context drift detected — CLAUDE.md needs regeneration',
              body: 'One or more team profiles are out of sync with the current module library. Run `./scripts/assemble-context.sh <profile>` to regenerate.',
              labels: ['context-engineering']
            })
```

### 用 Profile 完成新人入职

对于新加入的团队成员，入职流程变成了：

```bash
# 1. Copy a starter profile appropriate for your role
cp .claude/profiles/template-frontend.yaml .claude/profiles/yourname.yaml

# 2. Edit the profile for your preferences
vim .claude/profiles/yourname.yaml

# 3. Generate your CLAUDE.md
./scripts/assemble-context.sh yourname

# 4. Verify the output
cat CLAUDE.md

# 5. Commit your profile (not the generated CLAUDE.md — it's gitignored)
git add .claude/profiles/yourname.yaml
git commit -m "chore: add context profile for yourname"
```

在项目根目录的 `.gitignore` 中加入 `CLAUDE.md`。profile YAML 才是唯一可信来源，而非生成出来的文件。

---

## 6. 上下文生命周期

### 指令债务

规则会不断累积，却很少被移除。这就是指令债务：过时、冗余或相互矛盾的规则逐渐堆积——而每一条都仍在消耗上下文预算。

指令债务的征兆：

- 某条规则引用了你六个月前就已停用的库
- 两条规则对同一模式给出了相反的说法
- 某条规则覆盖的边界情况只在某次特定迁移期间适用
- 同一项约束在不同章节中被重复陈述了三次
- 开发者注释掉或忽略特定规则，因为它们与当前实践相冲突

指令债务会带来复合成本：每一条冲突或无关的规则都会挤占一条有用规则的位置，而当规则相互冲突时，模型的行为会变得不可预测。

**季度审计节奏**：每季度（或在重大项目里程碑之后）安排一次上下文审计。审计提示词：

```
Review every rule in CLAUDE.md for:
1. Relevance: Does this still apply to the current stack and patterns?
2. Specificity: Is this actionable, or is it too vague to enforce?
3. Conflicts: Does this contradict another rule?
4. Coverage: Is this already covered by a more general rule?

For each rule, classify as: KEEP | UPDATE | ARCHIVE | DELETE
```

把它作为一个真实的 Claude 会话来运行，输入当前的 CLAUDE.md 并要求得到结构化的审计结果。

### 更新循环

在 Claude 给出糟糕输出后，最常见的错误就是手动修正输出然后继续往前走。这白白浪费了一次学习机会。

**糟糕的循环**：
```
Claude generates wrong pattern
→ Developer manually fixes it
→ Next session: Claude generates wrong pattern again
→ Developer manually fixes it again
→ Repeat indefinitely
```

**良好的循环**：
```
Claude generates wrong pattern
→ Developer identifies the root cause (missing rule? vague rule? conflicting rules?)
→ Developer updates CLAUDE.md with a corrected or new rule
→ Next session: Claude generates correct pattern
→ Rule stays in config permanently
```

更新循环是你的配置系统从经验中学习的方式。每一次糟糕的输出都是一个信号，说明你的上下文工程中缺失了或损坏了某些东西。把它当作针对 CLAUDE.md 的缺陷报告，而不仅仅是一次性的失败。

**规则更新的实用格式**：

当从一次失败中添加规则时，把理由内联写进去：

```markdown
- Use the `Result<T, E>` type for service functions, not try/catch
  (Rationale: try/catch at service level hides error types from callers;
   Result forces explicit error handling at the call site)
```

理由有两个作用：它帮助未来的审计者理解这条规则为何存在，也为 Claude 提供了更好的上下文以正确地应用规则。

### 冲刺后的知识喂养

在每个冲刺或发布周期结束时，运行一次简短的知识喂养会话：

1. **新模式**："本次冲刺中，我们对 Y 类问题统一采用了 X 方法。把这一点加入 CLAUDE.md。"
2. **发现的反模式**："我们尝试了 X，结果导致了 Y。添加一条规则来避免它。"
3. **架构决策**："我们决定采用 X 而非 Y，因为 Z。把它记录下来，这样 Claude 就不会再建议 Y。"
4. **已弃用模式**："我们正在弃用 X。添加一条规则改用 Y，并标记现有的 X 用法。"

这能让上下文系统保持最新，而无需进行大规模的周期性彻底改造。

### ACE 流水线

对于在自动化或半自动化工作流中运行 Claude Code 的团队，ACE 流水线提供了一个结构化的执行模型。这是一个跨会话运作的配置持久化循环。它有别于 arXiv:2510.04618（Stanford/SambaNova，2025 年 10 月），后者用同一缩写指代一种推理期上下文演化技术。关于建立在此流水线之上的运营改进，参见第 10 节（信号分类法）和第 11 节（闭环）。

```
Assemble → Check → Execute
```

**Assemble（组装）**：从团队画像 + 项目模块构建上下文。生成一份针对具体开发者和任务上下文的 CLAUDE.md。

**Check（检查）**：运行金丝雀验证——一组 3-5 个测试提示词，在执行实际任务之前先验证关键行为。如果金丝雀检查失败，就在继续之前先修复上下文问题。

**Execute（执行）**：用经过验证的上下文在实际任务上运行 Claude。

```bash
#!/usr/bin/env bash
# ace.sh — Assemble, Check, Execute

PROFILE="${1:-}"
TASK="${2:-}"

if [[ -z "$PROFILE" || -z "$TASK" ]]; then
  echo "Usage: ./ace.sh <profile> <task-description>"
  exit 1
fi

echo "=== ASSEMBLE ==="
./scripts/assemble-context.sh "$PROFILE"

echo "=== CHECK ==="
./scripts/run-canaries.sh
CANARY_EXIT=$?

if [[ $CANARY_EXIT -ne 0 ]]; then
  echo "Canary checks failed. Fix context issues before executing."
  exit 1
fi

echo "=== EXECUTE ==="
claude "$TASK"
```

### 会话复盘

在每个 Claude Code 会话结束、关闭之前，问一问：

```
Looking at what we built or changed in this session:
1. What patterns did we use that aren't in CLAUDE.md?
2. What did I have to correct that could become a rule?
3. What decisions did we make that should be documented?

Generate 3-5 candidate rules for CLAUDE.md based on this session.
```

这只需 2-3 分钟，就能产出具体的改进候选项。你审阅它们并决定要添加哪些。随着时间推移，这就是配置系统积累真正的项目知识、而非仅仅堆积通用规则的方式。

### 上下文链接

上下文链接是一种模式，其中一个上下文窗口的输出成为下一个上下文窗口的结构化输入。每个会话都建立在上一个会话之上，向前传递一份经过精心整理的摘要，而不是丢弃状态。

这有别于"按关注点分会话"流水线（见"全新上下文模式"一节），后者将不同关注点拆分到相互隔离的会话中。上下文链接则允许视角不断累积：每个会话的洞见都丰富了下一个会话的起始上下文。

**模式结构**：

```
Session 1:
  Input: Task definition + CLAUDE.md
  Work: Research, exploration, initial implementation
  Output: summary.md (decisions, open questions, validated patterns)

Session 2:
  Input: Task definition + CLAUDE.md + summary.md from Session 1
  Work: Implementation building on Session 1 findings
  Output: updated summary.md + code artifacts

Session 3:
  Input: Task definition + CLAUDE.md + updated summary.md
  Work: Review, refinement, integration
  Output: final artifacts + lessons.md for CLAUDE.md update
```

关键纪律在于：向前传递的摘要必须是经过整理的，而不是原始的对话记录。原始记录会重新引入上下文腐化。一份经过整理的摘要是 200-500 个 token 的提炼成果：已做出的决策、已验证的方法、已标记的死胡同。

**何时使用**：
- 跨多天的任务，每个会话都从零重建上下文会代价高昂
- 研究型任务，早期会话产出的发现会约束后续会话
- 迭代式设计任务，跨会话累积的理解很重要

**何时不要使用**：
- 具有清晰原子边界的任务（一个会话、一份交付物，下一次全新开始）
- 早期会话的假设被证明是错误的、你希望干净利落地另起炉灶的情况

上下文链接是有意地延展上下文。它与丢弃状态的 Ralph Loop 正好相反。当累积的理解是一项资产时使用链接；当累积的状态是一项负担时使用 Ralph Loop。

---

## 7. 质量度量

### 自我评估问题

定期（至少每季度一次）针对你的 CLAUDE.md 运行以下问题：

**相关性**：
- 这条规则是否仍适用于当前的技术栈、库和团队实践？
- 这条规则是否是为一个已不复存在的问题而写的？
- 新加入的团队成员能否理解这条规则为何存在？

**具体性**：
- 这条规则是否足够具体，让 Claude 知道它何时适用？
- 这条规则是否至少有一个具体的正例或反例？
- 两名开发者是否可能对这条规则有不同的解读？

**冲突**：
- 这条规则是否与同一文件中的另一条规则相矛盾？
- 这条规则是否与某个按路径作用域生效的模块中的规则相矛盾？
- 这条规则是否在没有显式覆盖的情况下与某条全局规则相矛盾？

**覆盖**：
- 这条规则是否只是某条已存在的、更通用规则的一个具体情形？
- 这条规则是否已被别处陈述的架构决策所隐含？

未能通过其中一项以上检查的规则，就是更新或移除的候选对象。

### 金丝雀检查

金丝雀检查是一些简单的测试提示词，用于验证 Claude 是否遵循关键约定。在对 CLAUDE.md 进行重大改动前后运行它们，以捕捉回退。

**结构**：3-5 个提示词，简单到能快速作答，但又具体到足以暴露遵从性失败。

**针对 React/TypeScript 项目的金丝雀集示例**：

```bash
# scripts/run-canaries.sh

PASS=0
FAIL=0

check() {
  local name="$1"
  local prompt="$2"
  local expected_pattern="$3"

  result=$(claude "$prompt" --output-format text 2>/dev/null)

  if echo "$result" | grep -qE "$expected_pattern"; then
    echo "PASS: $name"
    PASS=$((PASS + 1))
  else
    echo "FAIL: $name"
    echo "  Expected pattern: $expected_pattern"
    echo "  Got: $(echo "$result" | head -5)"
    FAIL=$((FAIL + 1))
  fi
}

check "TypeScript interfaces" \
  "Generate a React component that accepts a name and age prop" \
  "interface.*Props"

check "Named exports" \
  "Create a utility function that formats a date" \
  "^export (function|const)"

check "No any type" \
  "Write a function that processes user data" \
  "^((?!: any).)*$"

check "Error result type" \
  "Write a service function that fetches user data from an API" \
  "Result<"

echo ""
echo "Canaries: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]]
```

**何时运行金丝雀检查**：
- 在合并对 CLAUDE.md 的改动之前
- 在添加新的按路径作用域生效的模块之后
- 当团队成员报告 Claude 出现意外行为时
- 作为 CI 漂移检测作业的一部分

### 遵从度追踪

非正式但有效：针对 CLAUDE.md 中的每条关键规则，统计在该规则本应适用的 10 次连续交互中，Claude 违反它的频率。

| 规则 | 违反次数 / 10 | 状态 |
|------|----------------|--------|
| props 使用 TypeScript 接口 | 1/10 | 健康 |
| 服务函数使用 Result 类型 | 0/10 | 健康 |
| API 响应中不暴露原始数据库 ID | 3/10 | 需复查规则 |
| 带请求上下文的结构化日志 | 5/10 | 规则过于含糊 |
| 发布前进行 OWASP Top 10 检查 | 8/10 | 如此陈述无法落地执行 |

违反率 >20% 的规则，问题出在以下三种之一：
1. 太含糊，无法一致地应用
2. 与另一条规则相冲突
3. 在文件中位置过于靠后，无法获得足够的关注

**针对"太含糊"的修复**：添加一个合规的具体正例和一个违反的反例。

**针对"相冲突"的修复**：找到冲突点，决定哪条规则应当胜出，更新或移除落败的规则，并加上一条显式说明。

**针对"位置过于靠后"的修复**：把规则移到文件的前三分之一处，或移到其所在章节中更显眼的位置。

### 上下文债务分数

衡量你的上下文工程系统健康状况的单一指标：

```
Context Debt Score = (total_rules / 150) × (conflicts_found / total_rules) × 100
```

其中：
- `total_rules` = 所有已加载配置文件中不同规则的数量
- `150` = 大致的注意力上限
- `conflicts_found` = 与另一条规则相矛盾的规则数

| 分数区间 | 状态 | 行动 |
|-------------|--------|--------|
| < 30 | 健康 | 标准的季度审计 |
| 30 – 60 | 退化 | 修剪并去重；修复冲突 |
| 60 – 80 | 不佳 | 需要大规模重构 |
| > 80 | 危急 | 用排名前 30 的规则从头开始 |

**运行分数计算**：

```bash
# Count rules (approximate: lines starting with -)
TOTAL_RULES=$(grep -c "^- " CLAUDE.md 2>/dev/null || echo 0)

# Count conflicts requires manual review or an LLM audit pass
# Use: claude "Scan CLAUDE.md and count rules that contradict each other. Return the count."

echo "Total rules: $TOTAL_RULES"
echo "Run conflict audit manually or with Claude"
```

### 上下文漂移检测

现有的遵从度指标（金丝雀检查、违反率）需要人工解读：你是在注意到的时候才知道某条规则被违反了。系统化的漂移检测则是一个互补层，它能自动检测行为上的偏移，在它们以糟糕输出的形式浮现之前就发现问题。

这些方法来自 ML 可观测性领域。对于在自动化流水线中运行 Claude 的团队，它们比交互式使用更具相关性，但相关概念在两种场景下都适用。

**余弦距离方法**

最简单的、可用于生产的方法。把模型输出（对固定探针提示词的响应）嵌入向量化，并测量其与一个已知良好的基线嵌入之间的余弦距离。

1. 定义 5-10 个固定的探针提示词，用于测试关键约定（等同于金丝雀提示词）。
2. 在一个稳定的时间点（"黄金基线"），捕获输出并计算其嵌入。
3. 在后续每次运行中，对相同提示词计算输出，并测量其与基线的余弦距离。
4. 当平均距离超过某个阈值（对于句级嵌入通常为 0.15-0.20）时告警。

它能捕捉到的：渐进的风格漂移、约定侵蚀、输出结构的变化——全都在违反率上升之前。

**漂移特征占比**

比余弦距离更细粒度。不再用单一的距离指标，而是追踪具体哪些嵌入维度的偏移超出了阈值。这能告诉你输出的哪些方面发生了变化（长度、正式度、代码风格），而不仅仅是"发生了某种变化"。

实际落地需要一个嵌入模型和一个监控存储。先从余弦距离入手；只有当你需要诊断到底是什么在漂移时，再加上特征级追踪。

**最大均值差异（MMD）**

一种基于核的方法，用于比较两组输出分布。MMD 回答的是："这一时段的输出在统计上是否与基线时段不同？"它能稳健地处理高维嵌入，并且不要求指定要追踪哪些特征。

MMD 的搭建成本高于余弦距离，但当输出方差天然较高时，它产生的误报更少。对于输出量大（每天数百次 Claude 运行）的团队而言具有相关性。

**统计距离阈值**

无论采用哪种方法，阈值都很重要：

| 距离指标 | 告警阈值 | 备注 |
|----------------|-----------------|------|
| 余弦距离 | > 0.15 | 适用于大多数句级嵌入 |
| 欧氏距离 | 随维度而变 | 先对嵌入做归一化 |
| 曼哈顿距离 | 随维度而变 | 比欧氏距离更能抵御离群值 |

这些只是起点。请根据你的基线方差来校准：如果你的输出天然变化很大（创意类任务），就使用更宽松的阈值。

**何时使用漂移检测**

- 并非逐条输出都有人工审查的自动化流水线
- 在 CLAUDE.md 改动之后，用以验证行为保持稳定
- 在升级 Claude 模型版本时（不同版本之间行为会偏移）
- 在任何上下文配置改动之后进行回退检测

对于有定期人工审查的交互式开发，金丝雀检查和违反率追踪（见上文）就已足够。

### 值得长期追踪的有用指标

| 指标 | 如何测量 | 目标 |
|--------|---------------|--------|
| 常驻上下文大小 | `wc -w CLAUDE.md ~/.claude/CLAUDE.md` | < 5,000 词 |
| 规则数量 | `grep -c "^- " CLAUDE.md` | < 150 |
| 文件年龄 | `git log --follow -p CLAUDE.md | head -20` | 每 6 个月做一次大检 |
| 每条关键规则的违反率 | 人工抽查 | < 20% 违反 |
| 金丝雀通过率 | `./scripts/run-canaries.sh` | 100%（全部通过） |

---

## 8. 上下文缩减技术

### 路径作用域：杠杆率最高的技术

路径作用域可在不损失任何覆盖范围的前提下，将常驻上下文缩减 40-50%。对于配置超过约 200 行的项目，这是影响最大的结构性改动。

实施步骤：

1. 识别代码库中天然的领域边界（API、前端、数据库、测试、基础设施）
2. 为每个领域在其所在目录创建一个 `CLAUDE-{domain}.md` 文件
3. 将领域专属规则从根 CLAUDE.md 移到对应的模块
4. 在根 CLAUDE.md 中用 `@path/to/CLAUDE-domain.md` 导入来替换被移走的内容
5. 通过金丝雀检查（canary checks）验证遵循情况

重构后的目标：根 CLAUDE.md 控制在 150 行以内（仅保留共享规则 + 导入声明）。

### 否定式约束

经验表明，在防止不良模式方面，否定式约束（"never do X"）比肯定式指令（"do X"）的效果高出 15-25%。这有违直觉——你可能以为"do X"会更清晰。但实践中，模型需要主动抵制做出错误行为的诱惑；明确点名错误行为并说"never"会更显著。

| 模式 | 表述 | 遵循率 |
|---------|-------------|-----------|
| 肯定式（较弱） | "Use structured logging for all backend services" | ~75% |
| 否定式（较强） | "Never use console.log in backend services; use the structured logger (pino)" | ~90% |

**技巧**：对于任何错误模式属于常见默认行为的规则（裸 try/catch、console.log、默认导出、any 类型），将该规则表述为点名具体待避免模式的否定式约束。

### 规则压缩

冗长的解释性规则会消耗 token 并稀释注意力。把解释压缩到本质：

**压缩前**（冗长，38 词）：
```markdown
- When creating React components, always make sure to use TypeScript interfaces
  for props, and define them before the component declaration, not inline, to
  improve readability and enable reuse.
```

**压缩后**（精简，9 词）：
```markdown
- React props: TypeScript interface, declared before component, never inline.
```

压缩后的版本遵循率更高——较短的规则在处理时每条规则分配到的注意力权重更高。只有在确实需要帮助理解时，才把解释保留为带原理（rationale）格式的内容。

**压缩启发法**：如果一条规则超过一行，就问问额外内容是约束还是解释。把解释移到注释中（以 `#` 为前缀或用 `>` 引用块），或移到原理注解中。强制执行的约束保持在一行以内。

### 去重

同一条约束以多种措辞重复出现并不会强化它——反而会稀释总的注意力预算。找出并删除语义重复项。

**重复的常见来源**：
- 通用章节中有一条规则，路径作用域模块中又有一个更具体的版本
- 为修复某个问题而新增的规则，却未删除被它取代的、表述更模糊的原规则
- 合并时从不同团队成员配置中复制而来的规则

**去重工作流**：

```
Scan CLAUDE.md for semantic duplicates. Two rules are duplicates if they
constrain the same behavior, even if worded differently. List all duplicate
pairs and recommend which version to keep based on specificity and clarity.
```

把它作为一个 Claude prompt 针对你的 CLAUDE.md 运行。审阅建议并合并。

### 归档模式

删除一条规则时，你也丢失了它存在原因的相关知识。那份组织记忆可能很有价值——半年后，可能有人试图重新引入该规则原本在防止的同一模式。

与其删除过时规则，不如将其归档：

```
.claude/
├── CLAUDE.md              # Active rules
└── CLAUDE-archive.md      # Historical rules with retirement notes
```

**归档条目格式**：

```markdown
## Archived Rules

### [Retired 2026-01] Use MongoDB for session storage
Replaced by: Use PostgreSQL with the sessions table for session storage.
Reason: Standardized on single database; MongoDB was only used for sessions and added operational complexity.
```

该归档不会被 Claude 加载——它是供人类参考的文档。它能防止同样的争论和错误反复发生。

### 规则的 80/20 法则

在大多数生产配置中，20% 的规则决定了 Claude 80% 的关键决策。其余 80% 的规则覆盖的是边缘情况、风格偏好以及很少出现的场景。

识别你的头部 20%：

1. 列出 CLAUDE.md 中的每一条规则
2. 对每条规则估计："这条规则在一次会话中真正改变 Claude 输出的频率有多高？"
3. 每天都适用的规则：保留、优先、靠前放置
4. 每周适用的规则：保留、放在中间
5. 每月适用的规则：考虑归档或移到按需加载的 skill
6. 极少适用的规则：归档

目标不是消除覆盖范围——而是确保最重要的规则不被最不重要的规则稀释。

**位置很重要**：把你的头部 20% 规则放在 CLAUDE.md 的前三分之一。注意力权重在一篇长文档中并非均匀分布——靠前的内容显著性更高。

### 用代码思考（Think in Code）

这一模式由 context-mode v1.0.64 命名，并由 Contieri 在 2026 年 4 月独立描述为"要分析师，不要分析结果"（Ask for the Analyst, Not the Analysis），它针对的是探索类任务中常见的 token 浪费来源。

**问题**：要回答"哪些文件导入了模块 X？"，一个朴素的 agent 会逐个打开并读取文件。若有 30 个候选文件，那就是 30 次工具调用，并可能向上下文加载 15,000+ token 的文件内容，而其中绝大部分与实际问题无关。

**模式**：与其读取文件，不如指示 agent 编写并运行一个用于查询、计数或过滤的小脚本（bash、Python、jq），然后只返回结果。结果是 1 次工具调用、约 50 token，而非 30 次调用、15,000 token。

**示例**：

查找哪些文件导入了某个模块：
```bash
grep -r "import X" src/ --include="*.ts" | wc -l
```

识别超过某个大小阈值的文件：
```bash
find src/ -name "*.ts" -size +50k | sort
```

按目录统计测试覆盖：
```bash
find src/ -name "*.test.ts" | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn
```

**何时使用**：任何属于"探索并报告"而非"编辑"的任务。发现类任务、计数、模式匹配、依赖分析以及按内容查找文件都是候选场景。如果你发现自己在写描述"读取大量文件以收集统计数据"的 agent 指令，那么"用代码思考"模式通常就适用。

**与 sub-agent 的关系**：sub-agent 在隔离环境中执行，拥有自己的上下文预算。"用代码思考"则把一切都保留在主 agent 中，但用脚本作为探索手段。两种方法都避免把无关的文件内容加载进上下文。对于确实需要读取文件内容的任务（编辑、代码审查、理解逻辑），sub-agent 更合适。对于可归结为计数或列表的纯发现类任务，单次脚本调用更快、更省钱。

### 分级上下文卸载

源自 LangGraph 的 Deep Agents SDK 对长时运行 agent 的研究，这套三层级联在不丢失信息访问能力的前提下，应对随时间积累的上下文。

**问题**：处理大量文件、API 调用和工具结果的长时运行 agent 会不断积累上下文，直到触及窗口上限或因上下文腐化（context rot）而降低准确度。截断（丢失数据）和无限积累（丢失准确度）都不正确。

**三层级联**：

**第 1 层——大型工具输出（阈值：20K token）**：卸载到文件系统。将完整输出写入临时文件，只向上下文注入文件路径和 10 行预览。agent 如有需要可请求完整内容。

**第 2 层——积累的工具调用参数（阈值：上下文接近中点）**：卸载旧的工具调用。只完整保留最近 N 次工具调用；对更旧调用的参数进行摘要或丢弃。对于继续任务而言，工具结果比工具调用参数更有价值。

**第 3 层——消息历史（阈值：上下文接近上限）**：对消息历史进行有损摘要。仅作最后手段——这会引入第 11 节（渐进式摘要风险）中所述的风险。仅在第 1、2 层都用尽时才采用。

**使用 PostToolUse hook 的 Claude Code 等效做法**：

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.claude/hooks/offload-large-output.py"
      }]
    }]
  }
}
```

```python
# ~/.claude/hooks/offload-large-output.py
import json, sys, tempfile, os

data = json.load(sys.stdin)
output = data.get("tool_result", {}).get("content", "")

THRESHOLD = 20_000  # characters, roughly 5K tokens

if len(output) > THRESHOLD:
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False,
        prefix="/tmp/claude-output-"
    )
    tmp.write(output)
    tmp.close()
    preview = "\n".join(output.splitlines()[:10])
    print(json.dumps({
        "tool_result": {
            "content": (
                f"[Output too large — saved to {tmp.name}]\n"
                f"Preview (first 10 lines):\n{preview}\n"
                f"Use: cat {tmp.name}"
            )
        }
    }))
else:
    print(json.dumps(data))
```

这个 hook 会透明地拦截大型 bash 输出，将其写入临时文件，并注入带预览的路径。agent 看到的是一份紧凑摘要，并知道如有需要去哪里找完整内容。同一模式适用于任何工具类型：MCP 工具结果、文件读取或 API 响应都可以卸载到文件系统并按路径引用。

### 小结：按影响排序的缩减技术

| 技术 | 上下文缩减 | 投入 | 遵循率影响 |
|-----------|------------------|--------|-----------------|
| 路径作用域 | 40-50% | 中 | +15-25% |
| 否定式约束 | 0%（重新表述） | 低 | 每条规则 +15-25% |
| 规则压缩 | 20-30% | 低 | +5-10% |
| 去重 | 10-20% | 低 | +5-15% |
| 归档模式 | 10-30% | 低 | +5-10% |
| 80/20 优先级排序 | 0%（重新排序） | 低 | +10-20% |
| 用代码思考 | 探索类任务上 90%+ | 低 | 不适用（替换调用） |
| 分级卸载 | 可变（取决于层级） | 中 | 防止腐化 |

对于存在上下文债务的项目，杠杆率最高的执行顺序：

1. 路径作用域化（最大的结构性收益）
2. 去重（移除噪声）
3. 压缩（让剩余规则更锐利）
4. 归档（安全清除过时规则）
5. 重新排序（优先呈现最重要的规则）
6. 分级卸载（用于长时运行或多步骤的 agent 工作流）

---

## 9. 成熟度评估

Context engineering 能力是分阶段发展的。大多数团队达到 Level 2 后就止步不前——并非因为更高的层级有多复杂，而是因为 Level 2 的失败是隐形的。输出质量尚可接受，所以继续推进的压力从未出现。这套评估让这一差距变得可见。

### 六个层级

| 层级 | 名称 | 已具备 | 失败模式 |
|-------|------|-------------|--------------|
| **0** | 无配置 | 没有 CLAUDE.md 的 LLM | 通用化输出，对项目零认知 |
| **1** | 扁平配置 | 单个 CLAUDE.md，无结构 | 规则不断堆积，超过约 100 行后遵循度下降 |
| **2** | 结构化配置 | 分章节、组织清晰、global/project 分离 | 单人可用，团队规模下失效 |
| **3** | 模块化配置 | 按路径限定作用域的模块，刻意分层 | 规则得到维护但缺乏验证 |
| **4** | 可度量配置 | canary 测试、遵循度追踪、生命周期管理 | 系统能运转但会随时间悄然漂移 |
| **5** | 工程化系统 | profile、CI 漂移检测、ACE pipeline、季度审计节奏 | — |

### 自我评估

逐一回答每个问题。在第一个"否"处停下——那就是你当前的层级。

**Level 0 → 1**：你的项目中有 CLAUDE.md 文件吗？

**Level 1 → 2**：你的配置是否区分了全局约定（位于 `~/.claude/CLAUDE.md`）和项目特定规则（位于 `./CLAUDE.md`）？各章节是否划分清晰？

**Level 2 → 3**：子系统特定的规则是否放在按路径限定作用域的模块中，而非根 CLAUDE.md 里？你的根 CLAUDE.md 是否保持在 150 行以内？

**Level 3 → 4**：你是否有用于验证关键约定的 canary 检查？你是否追踪最重要规则的违规率？你是否在重大里程碑后运行 context 审计？

**Level 4 → 5**：团队成员是否从 profile 组装各自的 CLAUDE.md，而非直接编辑它？是否有 CI 漂移检测，在配置偏离源模块时发出告警？你是否运行会话复盘，将新模式反馈回配置中？

### 各层级该做什么

| 你的层级 | 下一步行动 |
|------------|-------------|
| 0 | 创建一个含 5-10 条规则的最小 CLAUDE.md。哪些内容该放进去见 §3。 |
| 1 | 拆分全局配置与项目配置。将跨项目偏好移至 `~/.claude/CLAUDE.md`。 |
| 2 | 识别 2-3 个流量最高的子系统。为它们创建按路径限定作用域的模块。 |
| 3 | 为最常被违反的规则编写 3-5 条 canary prompt。将其自动化。 |
| 4 | 为团队成员引入 profile。增加 CI 漂移检测。开始会话复盘。 |
| 5 | 维持季度审计。系统已建成——工作转为持续的校准。 |

大多数团队在一个下午内就从 Level 0 推进到 Level 2。从 Level 3 推进到 Level 4 需要的是度量习惯，而非更多配置。更高层级的瓶颈不在于知识——而在于把配置当作一个活的系统而非一次性设置来对待的纪律。

---

## 10. 信号分类法与因果归因

一个扁平的摩擦分数（errors × 3 + retries × 2）能告诉你发生了多少摩擦，却无法说明是配置的哪一部分造成的。在一个运行 ACE-v1 循环长达十周的项目中，这一缺口产生了一份具有误导性的优先级队列：Bash 工具产生了 3,377 次 retry，而 Read 为 597 次、Edit 为 254 次。原始数量指向 Bash 是问题所在，但实际的模式是缺少批处理指令，而非某条糟糕的 Bash 规则。没有分类信号，curator 就会去修错误的层。

> 关于命名的一点说明：arXiv:2510.04618（Stanford/SambaNova，2025 年 10 月）用 "ACE" 指代一种推理时的 context 演化技术。本文描述的 ACE 是一个跨会话运行的配置持久化循环，而非会话内运行。概念不同，缩写相同。下文的 v2 改进适用于本指南的定义。

### 信号类别

用五类分类法替换扁平分数。每个事件都获得一个类别和一个归因候选。

| 类别 | 定义 | 示例 |
|---|---|---|
| **syntactic（语法）** | 工具报错、解析失败、调用格式错误 | `Invalid JSON in tool call` |
| **semantic（语义）** | 输出被用户拒绝、需澄清后重试 | "不，我指的是另一种格式" |
| **procedural（流程）** | 规则冲突、缺少步骤、执行阶段错误 | Write-before-Read 违规 |
| **alignment（对齐）** | 语气违规、超出范围的改动、凭空捏造的说法 | Claude 添加了未被要求的重构 |
| **performance（性能）** | token 超限、context 溢出、任务中途被迫 `/compact` | 会话在 85% context 时性能下降 |

权重应反映影响，而非频率。在一个生产关键流程中发生的一次 alignment 违规，其代价高于在本地脚本上发生 50 次 syntactic 重试。

### 因果归因

对于每个摩擦事件，记录当时活跃的 context：加载了哪些规则文件、调用了哪些 skill、哪个 profile 处于激活状态。这让 Curator 能够构建一张规则到摩擦的关联表，而无需对整个会话历史运行 LLM-as-judge。

```yaml
# friction-event schema
id: evt_20260519_bash_batching_001
timestamp: "2026-05-19T14:32:00Z"
session_id: "2094ff6d"
category: procedural
tool: Bash
retry_count: 4
description: "Three sequential Bash calls where one batched call would have sufficed"
active_rules:
  - .claude/rules/lean-ctx.md
  - .claude/rules/bash-safety.md
active_skills: []
profile: default
suspected_cause: "lean-ctx.md missing explicit Bash batching instruction"
resolved: false
```

将事件存储为仅追加（append-only）的 YAML 文件或换行分隔的 JSON。它们是 Curator 的原始素材；默认将其保留在本地并加入 gitignore，除非你的团队选择共享的信号存储（见 Section 11）。

### 按模式追踪

除单个事件之外，还要随时间按模式追踪摩擦。用一个字典替换每周总量：

```yaml
friction_patterns:
  week: "2026-W20"
  write_before_read: 10
  gitignore_violation: 10
  exit_code_1_unchecked: 38
  bash_no_batching: 47
  permission_denied_hook: 12
```

模式时间序列正是让你能够衡量一条合并后的规则是否产生了任何效果的依据。没有它，你只是在猜。

---

## 11. 闭环：基于 PR 的策展

Level 5 隐藏的失败模式是开环：Curator 生成了建议，却没有任何东西被合并。在 Aristote 项目运行 ACE-v1 的十周里，相隔十周的两份 curator 报告提出了同样的两个规则候选。两者都没有被合并。循环是开的，系统产出的是报告而非进展。

闭环要求让 Curator 的输出易于付诸行动。其机制是：Curator 生成一个 Git PR，而非一份普通报告。

### PR 剖析

每个 Curator PR 包含四样东西：

1. **配置 diff**：提议的具体规则或 skill 变更（一个可直接 `git diff` 的补丁，而非散文）
2. **摩擦证据**：驱动该建议的 3-5 个摩擦事件，事件 ID 链接回信号文件
3. **canary 结果**：在 10-20 个探针 prompt 上的前后对比（见下文）
4. **升级说明**：如果该建议在之前的报告中已被提出且未被采纳，PR 中包含一个计数器（"该建议已在 2 份此前的报告中出现而未获处理"）

由人类审阅并合并或关闭。Curator 从不直接修改规则。这正是成熟的 context engineering 工作流中"增强（Augmented）"的含义：循环通过人类判断而非自动化来闭合。

### A/B canary 探针

在提议变更之前，Curator 会针对当前配置和提议配置各运行一小组探针 prompt。探针是简单的、能代表任务的输入，用于触发正在被更改的那条规则。

```bash
# canary-ab.sh
OLD_CONFIG="$1"
NEW_CONFIG="$2"
PROBES_FILE="${3:-canary-probes.yaml}"

for probe in $(yq '.probes[].id' "$PROBES_FILE"); do
  question=$(yq ".probes[] | select(.id == \"$probe\") | .prompt" "$PROBES_FILE")
  old_out=$(run_with_config "$OLD_CONFIG" "$question")
  new_out=$(run_with_config "$NEW_CONFIG" "$question")
  compare_outputs "$probe" "$old_out" "$new_out"
done
```

每个 PR 用十到二十个探针就足够了。第一遍用余弦相似度；仅在相似度低于 0.85 的探针上运行 LLM-as-judge。这让大多数 PR 的 canary 成本接近于零，把判断保留给真正值得的边缘情况。

### 多时间尺度运行

在单一节奏上运行 Curator 会产生两种失败模式：太频繁会让审阅者不堪重负，太稀疏则会让摩擦无形累积。使用三个循环：

| 循环 | 触发条件 | 动作 |
|---|---|---|
| 实时 | PostStop hook 触发 | 将摩擦事件追加到本地信号存储 |
| 每周 | Cron（周六 02:00） | Curator 汇总本周，若达到信号阈值则生成 PR |
| 季度 | 手动 | 宪法式审计：检查规则重叠、归档休眠 skill、审查 profile 整合候选 |

季度循环无法以任何有用的方式自动化。它需要阅读系统的实际行为，而不仅仅是其记录的信号。

### 信号存放位置的决策

摩擦信号存放在哪里，决定了 Curator 能访问到什么。三种选项：

| 选项 | 工作方式 | 适合 |
|---|---|---|
| **A. 本地 cron** | 信号保留在开发者机器上；Curator 作为 macOS launchd 作业或本地 cron 运行 | 单人开发、隐私优先、无需维护基础设施 |
| **B. 推送式信号存储** | PostStop hook 将匿名化信号推送到私有 repo 或 S3 bucket；Curator 在 CI 中运行 | 5 人以上团队，需要多开发者协调（Section 14） |
| **C. 托管开发环境** | 信号默认落入共享环境（Codespaces、Coder） | 已在使用托管开发基础设施的团队 |

选项 A 是单人开发者的正确默认值。对于任何想要跨开发者模式分析或多开发者 profile 协调的团队，选项 B 是必需的；信号存储应当是一个私有 repo，而非 SaaS 平台，以将敏感的路径和工具数据排除在第三方服务器之外。只有当团队已出于其他原因投入托管开发环境时，选项 C 才值得考虑。

### 建议抑制

一个在连续三份报告中出现而未采取任何行动的建议应当改变状态：它要么在下一个 PR 中带阻塞标记进入"待人类决策"，要么带着记录在案的理由被关闭为"won't fix"。允许建议悄无声息地重复，与开环是同一种失败模式，只是更隐蔽。

---

## 12. 弹出（Ejection）：有纪律的去工程化

context engineering 技术栈的每个部分都在帮你添加更多：更多规则、更多 skill、更多 profile 章节。但没有一部分帮你移除那些已经失效的东西。这是这门纪律缺失的另一半，而它的缺失正是 Level 5 系统悄然退化的原因。

context 债务通过添加而累积。半年前为某个 sprint 编写的一条规则，可能与三条更新的规则冲突，在作者从未预料到的边缘情况上触发，并在每次会话中产生摩擦。没有弹出机制，它会永远留存，因为移除它感觉有风险，而审计它又要花费没人有的时间。

### 弹出启发式

三个指标驱动弹出候选：

**激活阈值**：在过去 N 个月内未触发过的规则很可能是死重。信号是：如果它们所防止的模式没有出现在摩擦日志中，那么要么这条规则完美起作用，要么没人写会触发它的代码。两种情况都暗示休眠。默认值：skill 为 3 个月，规则为 6 个月。

**ROI 追踪**：那些它们产生的摩擦（来自过于严格的强制执行、错误 context 触发）超过它们防止的摩擦的 skill。信号是：该 skill 出现在摩擦事件的 `active_skills` 字段中的次数，多于它出现在 "resolved" 事件中的次数。连续 4 周以上的负 ROI 即为弹出候选。

**profile 重叠**：当一条规则出现在超过 80% 的开发者个人 profile 中时，它应当归入共享配置，而非每个 profile。这是一个整合提议，而非弹出，但它能减少重复的维护面。

### 弹出 vs. 归档

弹出并不意味着删除。归档模式（Section 8）确立了保留退役规则并附退役说明的机构记忆理由。弹出是对应归档对象的*自动检测*。Curator 标记候选；由人类做出最终决定，并将规则移至 `CLAUDE-archive.md`，附上日期和理由。

没有任何商业可观测性工具（Braintrust、Langfuse、Helicone、LangSmith）实现了这一模式。它们追踪发生了什么；它们既不追踪你的配置包含什么，也不建议移除其中正在造成损害的部分。弹出机制是商业工具跳过的那门纪律，因为它需要了解你的配置 schema，而不仅仅是你的 prompt 历史。

---

## 13. 宪法式审计与自洽性审计

一个不受约束地增长的配置最终会自相矛盾。规则 A 说"格式化始终使用 ESLint"。规则 B 说"为了速度优先使用 Biome"。新来的开发者读了两条，结果两条都不照做，因为规则相互冲突，而系统没有给出它们冲突的任何信号。宪法式审计能在它积重难返之前抓住这一点。

### 宪法式审计

在每个 Curator PR 落地之前，针对两个目标运行约束检查：提议的变更 vs. 现有规则集，以及提议的变更 vs. 一份明确的 `constitution.md`。

```yaml
# .claude/constitution.md (example)
invariants:
  - id: no-auto-commit
    rule: "Never commit without explicit user request"
    rationale: "2024-incident: automated commit bypassed review gate"
  - id: no-destructive-without-confirm
    rule: "Never run rm, DROP, or force-push without confirmation"
    rationale: "Production safety baseline"
  - id: diff-before-merge
    rule: "Always show diff before applying multi-file changes"
    rationale: "Preserves human review in the loop"
```

宪法式检查是两个查询：提议的规则是否与任何不变量矛盾，以及它是否与 `.claude/rules/` 中任何现有规则冲突。两个查询都可以作为 Claude prompt 运行，以 constitution 和规则列表作为 context。每次 Curator 运行这会花费几百个 token，并防止规则冲突悄然累积。

这一模式的血脉源自 Constitutional AI（Anthropic，2022）和 RLAIF：用一份高层价值文档来约束一个较低层的生成过程。此处的转置是从输出对齐（检查模型的回应）转向配置对齐（检查规则系统的内部一致性）。机制更简单，因为输入更短且完全确定。

### 自洽性检查

会修改自身的系统会累积一种特定的失败模式：文档声称的状态已不再与现实相符。在一个生产环境的 ACE 安装中，文件 `ace-improvement-loop.md` 声称"截至 2026-03-04，skills 版本化 100% 完成"。而六周后测得的实际状态是 114 个 skill 中有 20 个完成版本化（17%）。这一差距持续存在，因为没人审计系统对自身做出的声明。

自洽性检查每周运行，与 Curator 分开。它读取你 ACE 文档中的声明，并对照测得的状态进行验证：

| 声明类型 | 如何验证 |
|---|---|
| "N 条规则激活" | `find .claude/rules -name "*.md" \| wc -l` |
| "skills 版本化 X% 完成" | `grep -l "^version:" .claude/skills/*/SKILL.md \| wc -l` 除以 skill 总数 |
| "上次 curator 运行：日期" | 在 git log 中检查最近的 Curator PR 创建日期 |
| "摩擦呈下降趋势" | 对比信号存储中的 4 周移动平均 |

当某个声明与测得的状态偏离超过 10% 时，检查会在下一份 Curator 报告中追加一个 "Self-consistency violations" 章节。这不是一种失败状态；这是系统在尽其职责。文档腐化是正常的。每周抓住它则不正常。

---

## 14. 多开发者 Profile 协调

基于 Profile 的组装（第 5 节）通过为每位开发者提供个人 profile，解决了 N 个开发者 × M 个工具的碎片化问题。随着时间推移，一个新问题浮现：各人的 profile 开始分化。开发者 A 的 profile 加了一条禁止直接访问生产数据库的规则。两周后，开发者 B 加了同样的规则，但措辞略有不同。开发者 C 则从未添加。本应放在共享配置里的那条规则，最终变得重复、不一致且无法强制执行。

这是 Claude Code 这类分层配置系统（三层结构：用户级 `~/.claude/CLAUDE.md` + 项目级 `CLAUDE.md` + 插件规则）特有的问题。没有任何商业 LLMOps 工具能解决它，因为它们都不会在团队配置层级中以单条规则文件的粒度运作。

### 检测

协调检查会扫描所有活跃的开发者 profile，识别出现在超过 50% profile 中的规则：

```bash
# profile-reconcile.sh
PROFILES_DIR="${1:-.claude/profiles}"
THRESHOLD="${2:-0.5}"

all_rules=$(find "$PROFILES_DIR" -name "*.yaml" -exec yq '.includes[]' {} \; | sort | uniq -c | sort -rn)
total_profiles=$(find "$PROFILES_DIR" -name "*.yaml" | wc -l)

while IFS= read -r line; do
  count=$(echo "$line" | awk '{print $1}')
  rule=$(echo "$line" | awk '{print $2}')
  ratio=$(echo "scale=2; $count / $total_profiles" | bc)
  if (( $(echo "$ratio >= $THRESHOLD" | bc -l) )); then
    echo "HOIST CANDIDATE ($count/$total_profiles profiles): $rule"
  fi
done <<< "$all_rules"
```

一条出现在 5 个开发者 profile 中 4 个里的规则，应当放进项目级 `CLAUDE.md`，而不是分散在四个独立的 profile 中。

### 保留

并非所有内容都应当被上提。个人偏好仍归个人：语气设置、详略程度、偏好的解释深度、语言选择。协调检查会区分行为规则（Claude 做什么）与偏好规则（Claude 如何沟通）。超过阈值的行为规则是上提候选；偏好规则则永不触碰。

对于 5 人及以上的团队，每月运行一次协调检查。对于 10 人以上的团队，将其作为季度宪法审计的一部分运行。其输出是一份上提候选清单，并附带针对共享配置的建议 diff；由人工审查并应用。该检查不会自动修改任何文件。

---

## 15. Token 审计工作流

只有当你测量出自己实际的开销后，上下文工程理论才能转化为真实收益。大多数开发者会发现，在任何用户任务开始之前，他们就已经加载了 40-60K token 的固定上下文：配置文件、规则、hooks 输出、记忆文件，以及 Claude Code 系统提示词层层叠加。本节提供一套可复现的审计工作流，耗时不到五分钟，并产出一份可执行的方案。

### 真实会话基准

在审计你自己的开销之前，先对照从业者在真实代码库上观察到的数据进行校准。下面的数字来自 Max 200 套餐、以 high effort 运行 Opus 4.7 的重度用户。请将它们视为上限参考：同样的任务在 Sonnet 级别的 effort 下会低 30-50%。

**每轮（输入 + 输出合计）**

| 任务类型 | 典型范围 |
|-----------|---------------|
| 简单问题，1-2 次工具调用 | 10-30K tokens |
| 带文件读取的定向编辑 | 30-80K tokens |
| 带探索的功能实现 | 100-300K tokens |
| 重度调查（MCP、多 agent、Datadog） | 300K-1M+ tokens |

**每个会话（完整对话）**

| 会话类型 | 典型范围 |
|--------------|---------------|
| 快速修复 | 100-300K tokens |
| 带测试的完整 PR | 500K-2M tokens |
| 带 compaction 的长会话 | 5M-20M+ tokens |

最主要的成本驱动因素是输入 token，而非输出。在同一会话中把一个 1000 行的文件重复读取五次，仅此一项就会增加大约 50K 输入 token。返回冗长 JSON 的 MCP 工具（Notion、Datadog、GitHub API 响应）会迅速放大这一点：单次 Datadog 查询就可能在模型处理数据之前往上下文中塞进 20-50K token。

团队层面的视角：在一次针对 Claude Code 重度用户的 Slack 社区调查中（2026 年 5 月），个别重度用户报告在复杂的 agentic 工作流上每天消耗 300-430M token；混合团队（简单和复杂任务合计）每个请求的中位数用量更接近 40K token，而重度用户达到 85K+。

Sub-agent 改变了这套算法。每个 sub-agent 在更短、更聚焦的上下文窗口中运作，因此单个 agent 的 token 成本更低。在复杂工作流中所有 agent 的总成本通常高于单个长会话，因为你启动了许多 agent。提升的是质量和并行度，而非原始的 token 效率。

### 什么算作固定上下文

每个会话开始时都有一个 token 基线，Claude 会在处理任何用户消息之前加载它们：

| 组成部分 | 何时加载 | 典型大小 |
|-----------|-------------|--------------|
| `~/.claude/CLAUDE.md` + `@imports` | 始终 | 5-15K tokens |
| 项目 `CLAUDE.md` | 始终 | 2-8K tokens |
| `.claude/rules/*.md`（自动加载） | 始终 | 5-40K tokens |
| `MEMORY.md`（项目记忆） | 始终 | 1-3K tokens |
| Claude Code 系统提示词 | 始终 | ~7,500 tokens |
| Hook 输出 | 每次工具调用 | 0.1-2K tokens × 调用频率 |
| `.claude/commands/*.md` | 仅在调用时 | 默认为 0 |
| `.claude/agents/*.md` | 仅在调用时 | 默认为 0 |

关键区别在于：`.claude/rules/` 会在会话开始时加载每一个 `.md` 文件，无论是否相关。命令和 agent 是惰性加载的——在被调用之前不产生任何成本。规则文件是最常见的意外开销来源。

### 第 1 步——测量各组成部分

从项目根目录运行这些命令，按组成部分得到明细：

```bash
# Project CLAUDE.md
echo "=== PROJECT CLAUDE.md ===" && wc -c CLAUDE.md

# Rules files sorted by size (your biggest opportunity)
echo "=== RULES FILES ===" && find .claude/rules -name "*.md" 2>/dev/null \
  | xargs wc -c 2>/dev/null | sort -rn | head -20

# Global config files
echo "=== GLOBAL ~/.claude ===" && ls -la ~/.claude/*.md 2>/dev/null \
  | awk '{print $5, $9}' | sort -rn
```

### 第 2 步——计算你的 Token 预算

Tokens ≈ 字符数 ÷ 4（粗略，但对英文/代码混合内容相当可靠）。

```bash
# Full budget estimate
GLOBAL=$(cat ~/.claude/CLAUDE.md ~/.claude/*.md 2>/dev/null | wc -c)
PROJECT=$(wc -c < CLAUDE.md 2>/dev/null || echo 0)
RULES=$(find .claude/rules -name "*.md" 2>/dev/null | xargs cat | wc -c)
MEMORY=$(find ~/.claude/projects -name "MEMORY.md" -path "*$(pwd | tr '/' '-')*" \
  2>/dev/null | xargs cat 2>/dev/null | wc -c || echo 0)
TOTAL=$(( GLOBAL + PROJECT + RULES + MEMORY + 30000 ))

echo "Global ~/.claude   : ~$(( GLOBAL / 4 )) tokens"
echo "Project CLAUDE.md  : ~$(( PROJECT / 4 )) tokens"
echo "Rules (auto-loaded): ~$(( RULES / 4 )) tokens"
echo "MEMORY.md          : ~$(( MEMORY / 4 )) tokens"
echo "System prompt      : ~7,500 tokens (estimate)"
echo "---"
echo "TOTAL              : ~$(( TOTAL / 4 )) tokens"
```

作为参考：Claude 的窗口为 200K token。60K 的固定开销意味着在任何工作开始之前就消耗了 30%。再加上一个典型编码任务额外使用的 20-40K token，留给实际输出的窗口已不足一半。

### 第 3 步——按使用频率对规则分类

规则文件通常是节省空间最多的地方。对于 `.claude/rules/` 中的每个文件，问一个问题：在一个典型会话中，它有多大概率是相关的？

| 类别 | 定义 | 操作 |
|-------|------------|--------|
| **始终关键** | 适用于每个任务（编码约定、输出格式、安全规则） | 保持自动加载 |
| **有时需要** | 在 20-40% 的会话中相关（调试方法论、任务管理） | 体积小则保持自动加载；体积大则考虑按需加载 |
| **极少需要** | 在不到 10% 的会话中相关（Figma 工作流、Windows 兼容性、设计系统） | 从自动加载中移除 |
| **从不需要** | 已过时、在别处已涵盖，或与本项目无关 | 删除或归档 |

将这一分类作为提示词运行：

```
Read every file in .claude/rules/. For each file, classify it as:
- ALWAYS: applies to most tasks in a typical session
- SOMETIMES: applies in 20-40% of sessions
- RARELY: applies in under 10% of sessions

Output a table: | File | Size (chars) | Class | Reasoning |
Sort by size descending within each class.
Calculate: total chars that could be removed from auto-load if RARELY files
are excluded.
```

### 第 4 步——审计 Hook 开销

在 `PreToolUse` 或 `PostToolUse` 上触发的 hooks 会在每次工具调用时运行。每次调用都会把其 stdout 注入上下文。一个每次调用输出 500 个字符、每个会话运行 150 次的 hook，会向会话上下文增加 75K 个字符（约 19K token）。

检查你的 hooks：

```bash
# List all hooks and their event types
cat ~/.claude/settings.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
hooks = data.get('hooks', {})
for event, hook_list in hooks.items():
    for h in hook_list:
        cmd = h.get('command', h.get('hooks', [{}])[0].get('command', '?'))
        print(f'{event}: {cmd[:80]}')
"
```

对于每个 `PreToolUse` 或 `PostToolUse` hook，通过手动运行并测量 stdout 来估算其输出大小。再乘以你每个会话的平均工具调用次数（在一个典型会话之后运行 `/cost` 即可获得工具调用计数）。

**需要留意的高开销模式：**
- 在每次调用时 `cat` 文件或打印多行摘要的 hooks
- 无条件运行 `git status` 或 `git log` 的 hooks
- 用于调试但一直没删掉的 `echo` 语句

### 第 5 步——制定行动方案

在不使用 RAG 或自定义基础设施的情况下，典型的节省：

| 操作 | 工作量 | 风险 | 典型节省 |
|--------|--------|------|----------------|
| 从极少使用的规则中移除"自动加载" | 30 分钟 | 低 | 5-20K tokens |
| 将大型规则文件拆分为核心 + 细节 | 1-2 小时 | 低 | 3-8K tokens |
| 将 hook 的 stdout 精简为必要字段 | 1 小时 | 低 | 2-10K tokens |
| 压缩冗长的规则（见 §8） | 1-2 小时 | 低 | 2-5K tokens |
| 归档过时的 MEMORY.md 条目 | 30 分钟 | 低 | 1-2K tokens |

一次切合实际的首轮处理，通常能在不触及任何需要基础设施的内容的情况下，将固定上下文减少 30-50%。

### 关于 RAG 的问题

你可能会遇到这样的建议：把规则文件放进向量数据库并动态检索（RAG）。在规模化场景下这是一种有效的优化——它把固定开销转化为按查询检索，并实现精确的惰性加载。

在投入这套基础设施之前，老实地核算一下：

- 你实际能省下多少 token？（先用第 1-3 步测量）
- 搭建成本是多少？一套带自定义 MCP 服务器的 pgvector 或 Chroma 方案，对一个运转中的团队来说是为期 1-2 周的工程项目
- 在哪个点上能达到收支平衡？如果经过简单清理后你的固定上下文已经低于 20K token，那么 RAG 增加的复杂度只换来微薄的收益

对大多数个人开发者和小团队而言，基于分类的惰性加载（从极少使用的文件上去掉自动加载标记）能以 2% 的基础设施成本实现 80% 的收益。当你拥有 50 个以上规则文件、需要自动化、基于意图的加载时，RAG 才配得上它的复杂度。

### 审计提示词模板

在项目内运行时，以下提示词会产出一份完整的审计报告。根据需要替换路径变量：

```
# Token Audit — [PROJECT NAME]

Audit this Claude Code project configuration for token overhead.
Be systematic and exhaustive, not superficial.

**Step 1 — Inventory**
List every file that is loaded at session start:
- ~/.claude/CLAUDE.md and all @imported files (with line counts)
- ./CLAUDE.md (line count)
- .claude/rules/*.md (all files, sorted by size)
- Project MEMORY.md (line count)

For each file, note: lines, approximate tokens (chars ÷ 4), and one-sentence
description of what it contains.

**Step 2 — Budget calculation**
Calculate: total fixed-context tokens before any user task.
Show the breakdown by component. Express as % of Claude's 200K window.

**Step 3 — Signal/noise classification**
For every rules file, classify as ALWAYS / SOMETIMES / RARELY based on how
often it would apply in a typical session on this project.
Flag any file over 5K chars that is classified SOMETIMES or RARELY.

**Step 4 — Hook audit**
Read .claude/settings.json (and ~/.claude/settings.json).
For each hook: event type, command, estimated stdout per invocation, and
whether it fires on every tool call or only at session boundaries.
Flag hooks that inject more than 200 chars per PreToolUse or PostToolUse call.

**Step 5 — Action plan**
Produce a prioritized table:
| Action | Estimated token savings | Effort | Risk |
Sort by: savings descending, then effort ascending.
Include only actions achievable without external infrastructure (no RAG, no
vector databases, no custom MCP servers).

**Step 6 — RAG verdict**
Based on the remaining savings after Step 5, calculate whether RAG would be
worth it: estimate residual savings, estimate setup cost in hours, and state
clearly whether the infrastructure investment is justified.
```

---

## 16. 研究模式：文献揭示了什么

应用型上下文工程借鉴了关于语言模型如何处理长输入的学术研究。有四项发现对你在生产环境的 agents 中构建上下文的方式具有实际意义。

### 迷失在中间效应（Lost-in-the-Middle）

**来源**：Liu et al. (2023)，斯坦福大学 ——《Lost in the Middle: How Language Models Use Long Contexts》

当相关信息被放置在长上下文窗口的中间位置时，模型在检索和推理任务上的表现会下降。当关键信息出现在上下文的开头（首因效应）或结尾（近因效应）时，模型表现最佳；而当信息被埋在中间时，表现最差。

这一效应在不同模型规模和上下文长度下都是一致的。一个 20 文档的检索任务，当答案位于位置 1 时准确率约为 70%，当答案位于位置 10 时可能降至约 40%，而到位置 20 时又回升至接近 70%。

**对 agents 的实际意义：**

- 把对决策最关键的信息放在系统提示的开头或结尾，而不是埋在冗长的 CLAUDE.md 中间
- 在汇总多个来源时，应以最相关的发现开篇，而非以最新的发现开篇
- 如果你有一组工具结果，第一个和最后一个结果会比中间的结果被更可靠地回忆起来
- 对于 Claude 需要审查 N 个条目的评估任务，应拆分成更小的批次，而不是一次性发送全部内容

其含义并不是说你应该把上下文做得更短 —— 而是说，上下文窗口中的位置是一个设计变量，而非偶然因素。

### 渐进式摘要的风险

将摘要的摘要逐层压缩的摘要流水线，会以模型无法察觉的方式丢失信息。每一次压缩都会去除细节，但模型的置信度并不会成比例地下降。到第三或第四次压缩之后，模型仍能流畅地回答有关原始内容的问题，但答案可能已不再准确 —— 它是在根据它所保留的压缩模式之后通常会出现的内容进行虚构。

**具体风险：**

- **事务性事实最先消失**：具体的数字、日期、名称和条件在早期的压缩过程中被抽象掉，而叙事结构得以保留
- **置信度保持高位**：模型并不知道自己是在基于压缩后的信息工作；它回答时的确定性与拥有原始内容时别无二致
- **没有检索信号**：与 RAG 不同 —— RAG 中检索失败是可见的 —— 摘要失败是无声的：无论如何模型都会产出流畅的文本

**缓解措施：**

```markdown
<!-- In CLAUDE.md for research/summarization agents -->
## Summarization Rules
- Always retain exact numbers, dates, and proper nouns in summaries — never paraphrase them
- Mark summaries with their compression level: [summary-level-1], [summary-level-2]
- If you cannot find a specific fact in the summary you have access to, say so — do not reconstruct from plausible inference
```

对于为保持在预算内而压缩上下文的多步骤 agents，应将压缩链限制在 2 次压缩之内，超过后就回到原始材料。

### 用于校准的分层抽样

在评估某个上下文工程方案是否有效时，随机抽样会遗漏系统性的失败。从一个 100 条目的测试集中随机抽样可能显示 85% 的准确率 —— 但如果那 15 个失败集中在某个特定的难度层级（长文档、含糊不清的指令、边缘情况），你就无法发现这个规律。

分层抽样按某个相关属性（文档长度、指令含糊度、来源质量）将评估集划分为多个层，并独立测试每一层。

**专门针对上下文工程而言：**

| 层级 | 为何重要 |
|---------|----------------|
| 短上下文（< 5K tokens） | 基准 —— 应接近 100% |
| 中等上下文（5K–50K） | 大部分真实工作发生的地方 |
| 长上下文（50K+） | 退化最先出现的地方 |
| 位置关键型（关键信息在中间） | 直接测试迷失在中间效应 |
| 高指令密度 | 测试 150 条指令的上限 |

如果你在长上下文层上的准确率比短上下文层低 20 个百分点，那就是一个信号 —— 应增加基于位置的结构化处理，或实现分块处理。聚合指标会掩盖掉这个差距。

### 论断-来源映射（溯源追踪）

在那些从多个来源（网络搜索、文件读取、工具结果）综合信息的 agents 中，最终输出中的论断应该可以追溯到其来源。如果没有溯源追踪，幻觉与准确的综合就无法区分，且错误会跨 agent 步骤累积放大。

**论断-来源映射是什么样的：**

与其让 agent 产出一份没有来源归属的摘要，不如对中间表示进行结构化处理，使论断与其来源保持关联：

```python
# Each synthesis step preserves provenance
claims = [
    {"claim": "The API rate limit is 1000 req/min", "source": "tool:get_api_docs", "confidence": "direct"},
    {"claim": "The rate limit was increased in v2.3", "source": "web:release-notes-url", "confidence": "direct"},
    {"claim": "Rate limits reset every 60 seconds", "source": "inferred", "confidence": "inferred"},
]
```

被标记为 "inferred"（推断）或缺乏来源的论断，应在最终输出中标注为不确定，而不应以与直接来源论断相同的置信度呈现。

**多步骤 agents 的实现模式：**

```markdown
<!-- In research agent system prompt -->
For every factual claim you include in your response:
- Tag it with the source (tool name, file path, URL, or "inferred")
- If you cannot identify the source, mark the claim as uncertain
- Do not present inferred conclusions with the same certainty as directly-observed facts
```

论断-来源映射作为质检（QA）机制与作为合规机制之间的区别在于：合规追踪问的是"我们是否使用了授权来源？"，而质检追踪问的是"这条具体论断是否准确？"—— 两者都有价值，但针对不同的失败模式。处理事实性查询或生成报告的 agents 需要质检版本。

---

## 17. 注意力机制与可靠性

Claude 的注意力在整个上下文窗口中并非均匀分布。提示中的位置会以可衡量的方式影响信息是否被使用。本节介绍其机制、背后的证据，以及用于弥补的模式。

---

### 迷失在中间问题

Liu et al. (2023, arXiv:2307.03172) 的研究考察了大语言模型如何使用长上下文中不同位置的信息。其发现是：检索准确率呈 U 形曲线。放置在长上下文开头或结尾的信息，被回忆的准确度显著高于放置在中间的信息。

具体到 Claude，在 100K 上下文窗口上的 NIAH（Needle-in-a-Haystack，大海捞针）基准测试显示，段落检索准确率从放置在开头或结尾的文档的 98% 下降到放置在中间的文档的 27%，相差 71 个百分点。后续的模型版本改善了中间上下文的回忆能力，但在大规模下 U 形偏差依然存在。

**实际后果：** 模型需要可靠使用的任何信息，都不应被埋在长上下文的中间。

---

### 首因与近因位置放置

两个高注意力区域是上下文窗口的开头（首因）和结尾（近因）。三明治模式同时利用了这两者：

```
[System prompt — persistent constraints, persona, critical rules]
[User's long document or retrieved context — middle zone]
[End of user message — restate the task + any constraints that must hold]
```

对于长到中间区域惩罚已变得重要的文档（大致超过 20,000 tokens），应在两端都放置最关键的信息：

```python
def build_analysis_prompt(document: str, critical_facts: list[str]) -> str:
    facts_block = "\n".join(f"- {f}" for f in critical_facts)
    
    return f"""CRITICAL FACTS (reference throughout your analysis):
{facts_block}

DOCUMENT TO ANALYZE:
{document}

REMINDER — apply these critical facts in your analysis:
{facts_block}

Now produce the analysis."""
```

在结尾重复关键事实并非冗余。它弥补了主文档在中间区域注意力下降的问题。

**针对超长文档的逐节处理：**

对于超过 50,000 tokens 的文档，单遍分析有遗漏中间各节内容的风险。逐节 + 整合模式：

```python
def analyze_long_document(client, document: str, section_size: int = 8000) -> str:
    sections = split_into_sections(document, max_tokens=section_size)
    section_analyses = []
    
    for i, section in enumerate(sections):
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": (
                    f"Analyze section {i+1} of {len(sections)}:\n\n{section}\n\n"
                    f"Focus on key facts, risks, and obligations. "
                    f"Note: this is one section of a longer document."
                )
            }]
        )
        section_analyses.append(response.content[0].text)
    
    # Integration pass with all section summaries in scope
    integration_prompt = "\n\n".join([
        f"SECTION {i+1} ANALYSIS:\n{analysis}"
        for i, analysis in enumerate(section_analyses)
    ])
    
    final_response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": (
                f"You have {len(sections)} section analyses from a single document. "
                f"Synthesize them into a complete analysis:\n\n{integration_prompt}"
            )
        }]
    )
    
    return final_response.content[0].text
```

每节分析都很短，并将相关内容保持在首因位置。整合环节处理的是各节摘要而非完整文档，从而使所有内容都保持在高注意力范围内。

---

### 上下文窗口大小 vs 注意力质量

更大的上下文窗口并不意味着对大输入有更好的理解。注意力质量在上下文窗口填满之前就已开始退化。在实践中：

- Claude 3.5 Sonnet：在有效内容约 50,000-70,000 tokens 时开始出现明显的质量退化
- Claude 3 Opus：退化阈值相近，但中间区域的惩罚更强
- 拥有 100 万 token 窗口的模型：窗口大小使更多数据得以呈现，但不一定意味着更好地使用这些数据

一个误区是把上下文窗口大小当作质量保证。一个 200K token 的输入并不会获得与 10K token 输入相同的每 token 注意力质量。对于需要精确使用分散事实的任务，一个结构良好的 30K 提示往往胜过一个原始堆砌的 200K 提示。

**设计原则：** 让上下文适配任务，而不是让任务适配上下文。

---

### 持久事实块

持久事实块是一个结构化的章节，放置在系统提示的开头，包含模型在整个对话中都必须引用的事实。与检索不同，它是逐字纳入的：这些事实始终处于首因位置、始终在作用范围内，并且与 prompt caching 兼容。

```python
PERSISTENT_FACTS = """

## 参考：公司背景

Entity: Acme Corp (Delaware C-Corp, EIN: 12-3456789)
Fiscal year end: December 31
Applicable law: Delaware corporate law, US federal regulations
Jurisdiction for disputes: Court of Chancery, Delaware
Authorized shares: 10,000,000 common @ $0.001 par
"""

system_prompt = f"""{PERSISTENT_FACTS}

You are a contract analysis assistant. Use the company context above for all entity references.
[rest of system prompt]
"""
```

持久化事实块对 prompt-cache 友好：因为它们出现在固定位置且内容是静态的，Anthropic 的 prompt caching 会在第一次调用后将其缓存，从而降低后续轮次的成本和延迟。

将持久化事实块控制在 500 tokens 以内。超过这个量后，带重排序的检索会更有效，因为该块本身开始落入中间区域。

---

### Scratchpad 模式

scratchpad 模式让模型跨轮次拥有持久化的工作记忆，而无需依赖上下文累积。对话开头的一条合成 assistant 消息保存结构化状态；orchestrator 在每一轮之后以编程方式更新它。

```python
def initialize_scratchpad(task_spec: dict) -> str:
    return f"""<scratchpad>
<task>{task_spec['description']}</task>
<status>in_progress</status>
<completed_steps>[]</completed_steps>
<pending_steps>{json.dumps(task_spec['steps'])}</pending_steps>
<working_notes></working_notes>
</scratchpad>"""

def update_scratchpad(scratchpad: str, updates: dict) -> str:
    for key, value in updates.items():
        scratchpad = re.sub(
            f"<{key}>.*?</{key}>",
            f"<{key}>{value}</{key}>",
            scratchpad,
            flags=re.DOTALL
        )
    return scratchpad

# Conversation structure:
messages = [
    {"role": "assistant", "content": initialize_scratchpad(task)},
    {"role": "user", "content": "Continue the task from your scratchpad."}
]

# After each turn, update the scratchpad with new state
new_scratchpad = update_scratchpad(
    messages[0]["content"],
    {
        "completed_steps": json.dumps(completed),
        "pending_steps": json.dumps(remaining),
        "working_notes": latest_notes
    }
)
messages[0]["content"] = new_scratchpad
```

scratchpad 在所有轮次中始终保持在首要位置（它是第一条消息）。工作笔记累积在那里，而不是让对话历史不断增长。

**Scratchpad 与滚动摘要的对比：** 当你需要可通过编程方式更新的结构化状态时，使用 scratchpad。当累积的上下文是非结构化的对话且需要压缩时，使用滚动摘要。

---

### 滚动上下文摘要

随着对话历史增长，较早的轮次失去相关性却仍占用 tokens。滚动上下文摘要会在已完成的阶段漂移进中间区域之前，将其压缩成紧凑的记录。

```python
SUMMARY_TRIGGER_RATIO = 0.65  # summarize when context reaches 65% capacity

def maybe_summarize_history(
    client,
    messages: list[dict],
    context_limit: int,
    current_tokens: int
) -> list[dict]:
    if current_tokens / context_limit < SUMMARY_TRIGGER_RATIO:
        return messages
    
    # Separate messages to summarize from recent messages to keep verbatim
    keep_recent = 4  # keep last 4 turns verbatim
    to_summarize = messages[:-keep_recent]
    to_keep = messages[-keep_recent:]
    
    # Extract key facts before summarizing
    facts_response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Extract key facts, decisions, and open items from this conversation "
                    f"history as a compact list:\n\n"
                    + "\n".join(f"{m['role']}: {m['content']}" for m in to_summarize)
                )
            }
        ]
    )
    key_facts = facts_response.content[0].text
    
    summary_message = {
        "role": "assistant",
        "content": f"<conversation_summary>\n{key_facts}\n</conversation_summary>"
    }
    
    return [summary_message] + to_keep
```

在摘要之前提取关键事实，而不是从摘要中提取。摘要会丢失那些往往很重要的边缘情况和边界条件。用更小的模型（Haiku）做一次事实提取既便宜又能保留更多信号。

在达到上下文上限的 65% 时触发，而不是等到 80% 的 auto-compact 阈值。主动压缩让你能掌控哪些内容被保留。

---

## 18. Token 压缩工具

前面几节关注的是该往上下文里放什么。本节介绍在管线层面压缩进入上下文内容的工具——在 Claude 处理之前就减少 token 量。这些工具是对 CLAUDE.md 编写工作的补充：好的上下文工程在设计时减少噪声，压缩工具在运行时减少体量。

两个独立的工具在 Claude Code 工具管线的不同层运作。

---

### Layer 1 —— CLI 输出：RTK

RTK (Rust Token Killer) 是一个 CLI 代理，它拦截 shell 命令输出并在 Claude 读取之前对其进行压缩。它通过一个 `PreToolUse` hook 运作，将 `git log` 之类的命令重写为 `rtk git log`。

**它压缩什么**：git、cargo、npm、pnpm、tsc、vitest、playwright、docker、kubectl 等。实测节省：在受支持的命令上达到 60-90%。

**它不压缩什么**：文件读取、MCP 工具结果，以及任何不经过 Bash 工具调用的内容。

```bash
brew install rtk-ai/tap/rtk   # or: cargo install rtk
rtk init --global              # installs PreToolUse hook + settings.json patch
rtk gain                       # dashboard: tokens saved per command
```

> **交叉引用**：完整命令参考和 TOML 过滤器 DSL 见 [third-party-tools.md §RTK](../ecosystem/third-party-tools.md#rtk-rust-token-killer)。

---

### Layer 2 —— 文件读取与会话记忆：lean-ctx

lean-ctx 作为一个全局 MCP 服务器运行，在工具层拦截 Read 调用和 Bash 调用，位于 RTK 的 shell hook 之下。它使用 tree-sitter AST 解析，只提取文件的相关结构，而非发送完整内容。

**安装**（一次性，全局）：

```bash
curl -fsSL https://raw.githubusercontent.com/yvgude/lean-ctx/main/skills/lean-ctx/scripts/install.sh | bash
lean-ctx setup   # registers MCP server + hooks in ~/.claude.json and ~/.claude/settings.json
```

无需逐项目设置。

**10 种读取模式**

| 模式 | 返回内容 | 最适用于 |
|------|----------------|----------|
| `signatures` | 仅类型和函数签名 | 为获取上下文而读取的大型 TypeScript/Rust 文件 |
| `map` | 导出项和导入依赖 | 理解模块间关系 |
| `auto` | 系统根据文件类型和上下文用量进行选择 | 默认，对大多数情况安全 |
| `full` | 完整文件，已缓存 | 你即将编辑的文件 |
| `diff` | 仅变更的行 | 编辑后重新读取文件 |
| `lines:N-M` | 指定行范围 | 定向检查 |
| `aggressive` | 最大化压缩，剥离语法 | 仅供参考的大型文件 |
| `entropy` | 仅高熵片段 | 扫描异常 |
| `task` | 任务相关的行 | 已定义活动任务集 |

**规则**：对你将要编辑的文件使用 `full`。对你为获取上下文而读取的文件使用 `signatures` 或 `map`。在一个 2364 行的文件上，差异是：`full` 花费约 19,000 tokens，`signatures` 花费约 200 tokens。

**缓存**：重新读取一个未更改的文件，无论文件大小，都花费约 13 tokens。缓存由文件 mtime 失效。

**CCP (Context Continuity Protocol)**：会话结束时，lean-ctx 写入一份约 400-token 的摘要，记录读取了什么、发现了什么、决定了什么。下一个会话会自动加载它，消除重新读取先前上下文的冷启动成本。

**实测基准（TypeScript/T3 monorepo，2455 个文件，7063 个节点的图）**

| 指标 | 值 |
|--------|-------|
| 整体压缩率 | 57.8% |
| ctx_read 节省率 | 86% |
| 单日节省的 tokens | 1.3M |
| schema.prisma 2364L → signatures | ~200 tokens (99%) |
| 文件重读（缓存命中） | 13 tokens |

**监控你的效率**

```bash
lean-ctx gain            # overall dashboard
lean-ctx gain --daily    # day-by-day savings
lean-ctx cep             # CEP score /100: compression, cache hit rate, consistency, mode diversity
lean-ctx sessions list   # session history with token counts
```

`/lean-ctx-audit` slash command 会一次性运行上述全部内容并综合生成一份报告。将它添加到 `~/.claude/commands/lean-ctx-audit.md`，即可在每个项目中使用它。

---

### 在两者之间做选择

RTK 和 lean-ctx 没有实质性的重叠。它们在实测会话中的实际节省分布：

| 来源 | 工具 | 占总节省的 % |
|--------|------|--------------------|
| 文件读取 (AST) | lean-ctx | ~85% |
| 搜索结果 | lean-ctx | ~5% |
| Shell 输出 | RTK | 其余部分 |
| 经 lean-ctx 的 Shell 输出 | lean-ctx | <1%（此处 RTK 更好） |

两者都装。RTK 处理 CLI 输出；lean-ctx 处理文件读取和会话记忆。

**lean-ctx 价值最高的场景**：TypeScript、Rust、Python 项目，其中大型源文件被反复读取，会话运行时间足够长以致在完成前上下文就已填满，且跨会话连续性很重要。

**lean-ctx 价值较低的场景**：以 Markdown 为主的文档仓库。AST 解析器找到的是嵌入在 Markdown 中的代码示例，而非源码结构。收益存在，但低于以代码为主的项目。

> **交叉引用**：完整工具简介见 [third-party-tools.md §Context Compression](../ecosystem/third-party-tools.md#context-compression)。

---

## 交叉引用

- 架构与项目结构模式：`guide/core/architecture.md`
- AI 辅助开发的方法论框架：`guide/core/methodologies.md`
- 用于上下文管理的 hooks 与自动化：`guide/ultimate-guide.md` §5（Hooks）
- 用于扩展上下文的 MCP server 集成：`guide/ultimate-guide.md` §7（MCP）
- 上下文内容的安全考量：`guide/security/`
- 路径作用域模块示例：`examples/` 目录
- PRP 方法论（Product Requirements Prompt，五层结构）：由 Wirasm/Widing 提出的社区框架 —— 完整摘要见 `guide/core/methodologies.md`，或在指南中搜索 "PRP" 查看实践示例

---

*本文是 Claude Code Ultimate Guide 的一部分。完整参考请见 `guide/ultimate-guide.md`。*
