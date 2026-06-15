---
title: "Claude Code — 可视化图表"
description: "48 张 Mermaid 交互式图表，覆盖所有主要的 Claude Code 概念"
tags: [reference, architecture, diagrams, mermaid]
---

# Claude Code — 可视化图表

48 张交互式 Mermaid 图表，按 10 个主题文件组织。每张图表都包含一个 Mermaid 版本（在 GitHub 上原生渲染）和一个 ASCII 备用版本。

> 如需纯 ASCII 图表和可打印的可视化参考 → [visual-reference.md](../core/visual-reference.md)

---

## 视觉配色

所有图表都使用一致的 Bold Guy 配色：

| 颜色 | Hex | 用途 |
|-------|-----|-------|
| 暖米色 | `#F5E6D3` | 用户操作、输入节点 |
| 焦橙色 | `#E87E2F` | 关键决策、Claude 操作 |
| 柔绿色 | `#7BC47F` | 成功路径、推荐做法 |
| 警示红 | `#E85D5D` | 危险、反模式、风险 |
| 中性灰 | `#B8B8B8` | 基础设施、被动元素 |
| 浅蓝色 | `#6DB3F2` | 信息、文档引用 |

## Mermaid 约定

| 形状 | 语法 | 含义 |
|-------|--------|---------|
| 圆角矩形 | `(text)` | 流程步骤、操作 |
| 菱形 | `{text}` | 决策点 |
| 体育场形 | `([text])` | 开始 / 结束终端节点 |
| 六边形 | `{{text}}` | 外部系统或 API |
| 子程序 | `[[text]]` | Claude Code 内部组件 |
| 圆柱体 | `[(text)]` | 数据存储、持久化状态 |

---

## 导航

| 文件 | 图表数 | 主题 |
|------|----------|--------|
| [01-foundations.md](./01-foundations.md) | 4 | 4 层模型、工作流流水线、决策树、权限模式 |
| [02-context-and-sessions.md](./02-context-and-sessions.md) | 4 | 上下文区域、记忆层级、会话传送、全新上下文 |
| [03-configuration-system.md](./03-configuration-system.md) | 4 | 配置优先级、skills 对比 commands 对比 agents、agent 生命周期、hooks |
| [04-architecture-internals.md](./04-architecture-internals.md) | 4 | 主循环、工具类别、系统提示词组装、sub-agent 隔离 |
| [05-mcp-ecosystem.md](./05-mcp-ecosystem.md) | 4 | MCP 生态地图、MCP 架构、rug pull 攻击、配置层级 |
| [06-development-workflows.md](./06-development-workflows.md) | 5 | TDD 循环、规范优先流水线、计划驱动、迭代精化、AI 熟练度路径 |
| [07-multi-agent-patterns.md](./07-multi-agent-patterns.md) | 5 | Agent 拓扑、worktree、双实例、横向扩展、决策矩阵 |
| [08-security-and-production.md](./08-security-and-production.md) | 4 | 三层防御、沙箱决策、验证悖论、CI/CD 流水线 |
| [09-cost-and-optimization.md](./09-cost-and-optimization.md) | 4 | 模型选择、成本优化、订阅层级、token 削减 |
| [10-adoption-and-learning.md](./10-adoption-and-learning.md) | 3 | 上手路径、UVAL 协议、信任校准 |
| [11-context-engineering.md](./11-context-engineering.md) | 4 | 三层上下文系统、遵循度退化、模块化架构、规则放置 |
| [12-enterprise-governance.md](./12-enterprise-governance.md) | 3 | 治理风险等级、MCP 审批工作流、数据分级 |
| **总计** | **48** | |

---

## 按使用场景导航

### "我刚接触 Claude Code — 从哪里开始？"
1. [快速决策树](./01-foundations.md#quick-decision-tree) — 我该使用 Claude Code 吗？
2. [9 步工作流流水线](./01-foundations.md#9-step-workflow-pipeline) — 它是如何工作的？
3. [权限模式](./01-foundations.md#permission-modes-comparison) — 都有哪些安全模式？
4. [上手路径](./10-adoption-and-learning.md#onboarding-adaptive-learning-paths) — 哪条路径适合我？

### "我想理解架构"
1. [主循环](./04-architecture-internals.md#the-master-loop) — 核心执行引擎
2. [系统提示词组装](./04-architecture-internals.md#system-prompt-assembly) — 上下文是如何构建的
3. [4 层上下文系统](./01-foundations.md#chatbot-to-context-system-4-layer-model) — 转化模型
4. [工具类别](./04-architecture-internals.md#tool-categories) — 有哪些工具可用

### "我担心安全问题"
1. [MCP Rug Pull 攻击](./05-mcp-ecosystem.md#mcp-rug-pull-attack-chain) — 主要威胁向量
2. [三层防御](./08-security-and-production.md#security-3-layer-defense) — 如何保护自己
3. [沙箱决策树](./08-security-and-production.md#sandbox-decision-tree) — 何时使用沙箱
4. [验证悖论](./08-security-and-production.md#the-verification-paradox) — 不要相信 Claude 会验证自己

### "我想降低 token 成本"
1. [模型选择决策流](./09-cost-and-optimization.md#model-selection-decision-flow) — 选择合适的模型
2. [成本优化树](./09-cost-and-optimization.md#cost-optimization-decision-tree) — 系统化降本
3. [Token 削减流水线](./09-cost-and-optimization.md#token-reduction-strategies-pipeline) — RTK + 会话卫生
4. [上下文管理区域](./02-context-and-sessions.md#context-management-zones) — 管理上下文大小

### "我想使用多个 agents"
1. [Agent 团队拓扑](./07-multi-agent-patterns.md#agent-teams-topology-3-patterns) — 3 种编排模式
2. [多实例决策矩阵](./07-multi-agent-patterns.md#multi-instance-decision-matrix) — 该用哪种模式？
3. [Git Worktree 多实例](./07-multi-agent-patterns.md#git-worktree-multi-instance-pattern) — 并行隔离
4. [Sub-Agent 上下文隔离](./04-architecture-internals.md#sub-agent-context-isolation) — agents 是如何隔离的

### "我想搭建 MCP 服务器"
1. [MCP 生态地图](./05-mcp-ecosystem.md#mcp-server-ecosystem-map) — 有哪些服务器
2. [MCP 架构](./05-mcp-ecosystem.md#mcp-architecture-client-server) — 它是如何工作的
3. [MCP 配置层级](./05-mcp-ecosystem.md#mcp-config-hierarchy) — 配置文件位于何处

### "我想在整个团队中治理 Claude Code"
1. [治理风险等级](./12-enterprise-governance.md#governance-risk-tiers) — 哪种控制级别适合你的场景？
2. [MCP 治理工作流](./12-enterprise-governance.md#mcp-governance-workflow) — MCP 服务器的审批流水线
3. [数据分级规则](./12-enterprise-governance.md#data-classification--claude-code-access-rules) — Claude 能访问什么、不能访问什么

### "我想提升 Claude 的上下文遵循度"
1. [规则放置决策树](./11-context-engineering.md#rule-placement-decision-tree) — 这条规则该放在哪里？
2. [三层上下文系统](./11-context-engineering.md#the-3-layer-context-system) — 全局 / 项目 / 会话
3. [上下文预算与遵循度](./11-context-engineering.md#context-budget--adherence-degradation) — 为什么规则会不再被遵循
4. [模块化架构](./11-context-engineering.md#monolithic-vs-modular-architecture) — 以路径限定范围作为解法

---

*返回 [guide/README.md](../README.md) | ASCII 图表 → [visual-reference.md](../core/visual-reference.md)*
