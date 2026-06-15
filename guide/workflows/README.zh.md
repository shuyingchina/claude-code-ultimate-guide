---
title: "Claude Code Workflows"
description: "Step-by-step guides for common development patterns with Claude Code"
tags: [workflow, guide, reference]
---

# Claude Code 工作流

使用 Claude Code 进行常见开发模式的分步指南。

---

## 🔍 搜索与发现

### [搜索工具精通](./search-tools-mastery.md) ⭐ NEW

**结合 rg、grepai、Serena 和 ast-grep，精通代码搜索的艺术**

学习何时使用每种工具、如何组合它们以实现最高效率，以及真实世界的工作流，包括：
- 探索陌生的代码库
- 大规模重构
- 安全审计
- 框架迁移
- 性能优化

**核心主题**：
- 快速决策矩阵
- 完整功能对比
- 5 个组合工作流
- 性能基准测试
- 常见陷阱
- 工具选择速查表

---

## 🎯 开发工作流

### [计划驱动开发](./plan-driven.md)

在执行之前使用规划模式来组织复杂任务的结构。

**何时使用**：多步骤功能、架构变更、对方法不确定时

### [使用 Claude 进行 TDD](./tdd-with-claude.md)

测试驱动开发工作流：先写测试，后做实现。

**何时使用**：关键功能、回归预防、API 设计

### [规范优先开发](./spec-first.md)

在编写代码之前先编写规范，以获得更清晰的需求。

**何时使用**：团队协作、复杂功能、文档优先的项目

### [迭代式精炼](./iterative-refinement.md)

通过多轮精炼周期改进代码。

**何时使用**：质量改进、性能优化、代码清理

### [骨架项目](./skeleton-projects.md) ⭐ NEW

使用经过实战检验的现有仓库作为新项目的脚手架。

**何时使用**：启动新项目、统一团队模式、基于成熟基础进行快速原型开发

### [团队 AI 指令](./team-ai-instructions.md)

通过基于配置档案的模块组装，将 CLAUDE.md 扩展到一个多开发者、多工具的团队。

**何时使用**：5 人以上的团队、多种 AI 工具（Claude Code + Cursor/Windsurf）、混合操作系统

### [Changelog 片段](./changelog-fragments.md) ⭐ NEW

**通过三层系统强制执行每个 PR 的文档记录：CLAUDE.md 规则 + UserPromptSubmit hook + CI 关卡**

消除 `CHANGELOG.md` 上的合并冲突，在实现时捕获上下文，并确保数据库迁移永远不会被悄无声息地部署。包含一个可复用的 `UserPromptSubmit` hook 模式，用于强制执行任何强制性的工作流步骤。

**核心主题**：
- 用于自主创建片段的 CLAUDE.md 工作流规则
- 具有三级优先级（强制、发现、上下文）的 `UserPromptSubmit` hook
- 条件建议模式："如果有 PR 意图但未提及片段"
- 带有独立迁移检查任务的 CI 强制执行

### [RPI：研究 → 计划 → 实现](./rpi.md) ⭐ NEW

**在各阶段之间设有明确验证关卡的三阶段功能开发**

在三个锁定的阶段中构建功能：首先研究可行性，其次规划实现，第三步编写代码。每个阶段产出一个具体的产物（RESEARCH.md → PLAN.md → 代码）。每道关卡都需要明确的 GO 才能开始下一阶段。

**何时使用**：可行性不明确的功能、超过一天工作量、未知的技术领域，或任何在后期发现错误假设代价高昂的场景

### [GitHub Actions 工作流](./github-actions.md) ⭐ NEW

**5 种用于自动化 PR 审查、issue 分类和质量关卡的生产级模式**

通过官方的 `claude-code-action` 将 Claude 直接接入你的 GitHub 工作流。两种模式：交互式（`@claude` 提及）和全自动化（push/schedule 触发）。

**核心主题**：
- 通过 `/install-github-app` 进行设置（30 秒快速上手）
- 模式 1：通过 `@claude` 提及按需进行 PR 审查
- 模式 2：每次 push 时自动审查
- 模式 3：issue 分类和打标签
- 模式 4：针对敏感路径的安全聚焦审查
- 模式 5：每周定时的仓库健康检查
- 成本控制、并发、fork 安全性

**何时使用**：任何希望获得 AI 驱动代码审查而无需管理基础设施的团队

---

### [认知模式切换](./gstack-workflow.md) ⭐ NEW

在整个发布周期中切换专家角色：战略产品关卡、架构审查、偏执式代码审查、自动化发布、原生浏览器 QA 和复盘。

**何时使用**：你希望在产品方向、工程严谨性、审查和发布之间有明确分工的发布周期——而不是用一个通用助手处理所有阶段

---

## 🎨 设计与内容

### [设计转代码](./design-to-code.md)

将设计稿（Figma、线框图）转换为可运行的代码。

**何时使用**：前端开发、UI 实现、设计系统工作

### [OG 图片生成](./og-image-generation.md)

在构建时使用 Satori 和 resvg 动态生成社交预览图片。

**何时使用**：Astro 项目、在不维护静态 PNG 的情况下保持社交预览准确

### [PDF 生成](./pdf-generation.md)

使用 Claude Code 配合 Quarto/Typst 生成专业的 PDF。

**何时使用**：报告、文档、白皮书、技术文档

### [演讲准备流水线](./talk-pipeline.md) ⭐ NEW

6 阶段 skill 流水线：原始素材 → 结构化演讲 → 通过 Kimi 生成 AI 幻灯片。

**何时使用**：会议演讲、技术聚会演示、内部技术分享——从文章、转录稿或笔记出发

### [TTS 设置](./tts-setup.md)

为 Claude Code 的响应配置文本转语音（Agent Vibes 集成）。

**何时使用**：音频反馈、无障碍、免手动编码

---

## 🔬 代码探索

### [探索工作流](./exploration-workflow.md)

系统性地探索和理解陌生的代码库。

**何时使用**：新项目、遗留代码、文档缺口

**相关**：高级多工具探索策略请参见[搜索工具精通](./search-tools-mastery.md)。

---

## 多 Agent 与进阶

### [Agent 团队](./agent-teams.md)

编排多个专业化 agent 在复杂任务上并行工作。

**何时使用**：能从并行性、专业能力或独立验证中受益的任务

### [Agent 团队快速上手](./agent-teams-quick-start.md)

在 30 分钟内搭建你的第一个 agent 团队的快速通道指南。

**何时使用**：刚接触多 agent 模式、想在投入完整配置前先做实验

### [双实例规划](./dual-instance-planning.md)

在两个协调的 Claude Code 实例中，用 Opus 进行规划、用 Sonnet 进行执行。

**何时使用**：需要深度推理进行架构设计、同时希望经济高效地执行的复杂功能

### [事件驱动的 Agent](./event-driven-agents.md)

通过 hook 事件而非直接编排来协调 agent。

**何时使用**：响应式工作流、hook 触发的自动化、松耦合的 agent 流水线

### [Plan 流水线](./plan-pipeline.md)

完整的端到端 plan 流水线：/plan-start、/plan-validate、/plan-execute 作为一个连贯的工作流。

**何时使用**：任何在编写代码前投入规划严谨性会带来回报的重要功能

### [任务管理](./task-management.md)

使用 TodoWrite、tasks API 以及跨会话的上下文持久化进行多会话任务跟踪。

**何时使用**：跨越多个会话的长期运行任务、团队协调、复杂的待办积压

---

## 快速选择指南

| 你的情况 | 推荐工作流 |
|----------------|---------------------|
| **初次接触代码库** | [探索工作流](./exploration-workflow.md) + [搜索工具精通](./search-tools-mastery.md) |
| **复杂功能** | [计划驱动](./plan-driven.md) 或 [规格优先](./spec-first.md) |
| **需要可靠性** | [使用 Claude 进行 TDD](./tdd-with-claude.md) |
| **大型重构** | [搜索工具精通](./search-tools-mastery.md) |
| **UI 实现** | [设计转代码](./design-to-code.md) |
| **代码质量** | [迭代优化](./iterative-refinement.md) |
| **从模板创建新项目** | [骨架项目](./skeleton-projects.md) |
| **团队 AI 指令** | [团队 AI 指令](./team-ai-instructions.md) |
| **强制执行必需的工作流步骤** | [Changelog 片段](./changelog-fragments.md) |
| **可行性未知、跨多日的功能** | [RPI：研究 → 计划 → 实现](./rpi.md) |
| **文档** | [PDF 生成](./pdf-generation.md) |
| **社交预览** | [OG 图片生成](./og-image-generation.md) |
| **从原始素材准备会议演讲** | [演讲准备流水线](./talk-pipeline.md) |
| **音频反馈** | [TTS 设置](./tts-setup.md) |
| **多 agent 任务** | [Agent 团队](./agent-teams.md) |
| **首个 agent 团队** | [Agent 团队快速入门](./agent-teams-quick-start.md) |
| **成本优化的规划** | [双实例规划](./dual-instance-planning.md) |
| **hook 驱动的自动化** | [事件驱动 agent](./event-driven-agents.md) |
| **完整计划工作流** | [计划流水线](./plan-pipeline.md) |
| **跨会话跟踪** | [任务管理](./task-management.md) |
| **编码前的策略关卡** | [认知模式切换](./gstack-workflow.md) |
| **非 MCP 浏览器自动化** | [认知模式切换](./gstack-workflow.md) |

---

## 贡献

有新的工作流想法？在主仓库中提交 issue 或 PR。

**工作流模板结构**：
1. 标题与目的
2. 何时使用
3. 前提条件
4. 分步指南
5. 真实案例
6. 常见陷阱
7. 相关工作流

---

**最后更新**：2026 年 3 月
