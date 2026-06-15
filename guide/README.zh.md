---
title: "Guide Documentation"
description: "Index of all core documentation files for mastering Claude Code"
tags: [guide, reference]
---

# 指南文档

掌握 Claude Code 的核心文档，按主题组织。

---

## 入门

| 文件 | 说明 | 时长 |
|------|-------------|------|
| [**learning-path/**](./learning-path/README.md) | 面向初学者的**结构化 7 模块学习路径**：安装、核心循环、记忆、agents、skills、hooks、高级模式 | 8-11 小时 |
| [learning-path/01-installation.md](./learning-path/01-installation.md) | 模块 01：安装 Claude Code 并验证其正常工作 | 15 分钟 |
| [learning-path/02-core-loop.md](./learning-path/02-core-loop.md) | 模块 02：理解交互循环与上下文 | 45 分钟 |
| [learning-path/03-memory.md](./learning-path/03-memory.md) | 模块 03：创建 CLAUDE.md 并配置记忆 | 1 小时 |
| [learning-path/04-agents.md](./learning-path/04-agents.md) | 模块 04：创建专用 agents | 1.5 小时 |
| [learning-path/05-skills.md](./learning-path/05-skills.md) | 模块 05：构建可复用的 skills | 1.5 小时 |
| [learning-path/06-hooks.md](./learning-path/06-hooks.md) | 模块 06：创建自动化 hooks | 1 小时 |
| [learning-path/07-advanced.md](./learning-path/07-advanced.md) | 模块 07：多 agent 编排 | 2-3 小时 |

---

## 核心参考

| 文件 | 说明 | 时长 |
|------|-------------|------|
| [ultimate-guide.md](./ultimate-guide.md) | 涵盖所有 Claude Code 功能的完整参考 | ~3 小时 |
| [cheatsheet.md](./cheatsheet.md) | 1 页可打印的快速参考 | 5 分钟 |
| [core/architecture.md](./core/architecture.md) | Claude Code 的内部工作原理（主循环、工具、上下文） | 25 分钟 |
| [core/tools-reference.md](./core/tools-reference.md) | **完整工具参考**：全部 40 个内置工具、权限规则格式、各工具行为（Bash 超时、Edit 编辑前读取、Glob 上限、WebFetch 有损）、以及 Monitor、Workflow、agent teams、Cron、Tasks API 的使用方法 | 20 分钟 |
| [core/methodologies.md](./core/methodologies.md) | 15 种开发方法论参考（TDD、SDD、BDD 等） | 20 分钟 |
| [core/visual-reference.md](./core/visual-reference.md) | 可视化速查表 —— 关键概念的 ASCII 图示 | 5 分钟 |
| [core/claude-code-releases.md](./core/claude-code-releases.md) | 官方发布历史（精简版） | 10 分钟 |
| [core/known-issues.md](./core/known-issues.md) | **关键 bug 追踪器**：安全问题、token 消耗、经核实的社区报告 | 15 分钟 |
| [core/context-engineering.md](./core/context-engineering.md) | **上下文工程**：token 预算、模块化架构、团队组建、ACE 流水线、质量度量 | 25 分钟 |
| [core/memory-systems.md](./core/memory-systems.md) | **记忆系统**：原生技术栈（CLAUDE.md、Auto Memory、Auto Dream）、跨会话工具（claude-mem、agentmemory、ICM）、团队共享、多 agent 模式、架构、风险、决策流程图 | 30 分钟 |
| [core/glossary.md](./core/glossary.md) | **术语表**：Claude Code 官方术语（31 个术语，段落格式，附指南章节链接） | 5 分钟 |
| [core/community-patterns.md](./core/community-patterns.md) | **社区模式**：约 130 个社区创造的模式、工作流术语、AI 工程概念以及快速参考定义 | 10 分钟 |
| [diagrams/](./diagrams/) | **可视化图表系列**：41 个 Mermaid 交互式图表，涵盖模型选择、agent 生命周期、安全、多 agent 模式 | 15 分钟 |

---

## 安全

| 文件 | 说明 | 时长 |
|------|-------------|------|
| [security/security-hardening.md](./security/security-hardening.md) | 安全威胁、MCP 审查、注入防御 | 25 分钟 |
| [security/sandbox-isolation.md](./security/sandbox-isolation.md) | Docker Sandboxes、云端替代方案、安全自治工作流 | 10 分钟 |
| [security/sandbox-native.md](./security/sandbox-native.md) | 原生 Claude Code 沙箱：配置与安全模型 | 10 分钟 |
| [security/production-safety.md](./security/production-safety.md) | 生产安全：护栏、审查关卡、回滚策略 | 15 分钟 |
| [security/data-privacy.md](./security/data-privacy.md) | 数据保留与隐私指南 | 10 分钟 |
| [security/enterprise-governance.md](./security/enterprise-governance.md) | **组织级治理**：使用章程、MCP 审批工作流、护栏分级（Starter/Standard/Strict/Regulated）、合规 | 25 分钟 |

---

## 生态系统

| 文件 | 说明 | 时长 |
|------|-------------|------|
| [ecosystem/ai-ecosystem.md](./ecosystem/ai-ecosystem.md) | 互补的 AI 工具（Perplexity、Gemini、Kimi、NotebookLM、TTS） | 30 分钟 |
| [ecosystem/agentic-tools.md](./ecosystem/agentic-tools.md) | **Agent 工具对比**：Hermes Agent、Codex CLI、Aider、Devin、SWE-agent、CrewAI、LangGraph、AutoGen、决策框架 | 20 分钟 |
| [ecosystem/mcp-servers-ecosystem.md](./ecosystem/mcp-servers-ecosystem.md) | **社区 MCP 服务器**：8 个经验证的服务器（Playwright、Semgrep、Kubernetes 等）及生产配置 | 25 分钟 |
| [ecosystem/third-party-tools.md](./ecosystem/third-party-tools.md) | **社区工具**：GUI、TUI、配置管理器、token 追踪器、替代 UI | 15 分钟 |
| [ecosystem/context-engineering-tools.md](./ecosystem/context-engineering-tools.md) | **上下文与 token 优化**：输出压缩（RTK、Headroom）、prompt 压缩（LLMLingua）、AI 网关（Edgee、Portkey）、RAG、LLMOps | 20 分钟 |
| [ecosystem/remarkable-ai.md](./ecosystem/remarkable-ai.md) | Remarkable AI 使用模式与高级用户技巧 | 10 分钟 |

---

## 角色与采用

| 文件 | 说明 | 时长 |
|------|-------------|------|
| [roles/ai-roles.md](./roles/ai-roles.md) | AI 角色映射：何时使用 Claude Code、Claude Desktop 或 API | 10 分钟 |
| [roles/adoption-approaches.md](./roles/adoption-approaches.md) | 面向团队的实施策略 | 15 分钟 |
| [roles/learning-with-ai.md](./roles/learning-with-ai.md) | 帮助初级开发者在使用 AI 的同时不丢失技能的指南 | 15 分钟 |
| [roles/agent-evaluation.md](./roles/agent-evaluation.md) | **Agent 质量指标**：通过 hooks、测试和反馈循环衡量自定义 agent 的有效性 | 20 分钟 |

---

## 运维

| 文件 | 说明 | 时长 |
|------|-------------|------|
| [ops/devops-sre.md](./ops/devops-sre.md) | 用于基础设施诊断和事故响应的 FIRE 框架 | 30 分钟 |
| [ops/observability.md](./ops/observability.md) | 会话监控与成本追踪 | 15 分钟 |
| [ops/ai-traceability.md](./ops/ai-traceability.md) | AI 归因、披露策略、git-ai、合规 | 20 分钟 |
| [ops/team-metrics.md](./ops/team-metrics.md) | **面向 AI 增强工程的团队指标**：DORA、SPACE、DX Core 4、AI 特有信号，按团队规模划分（5–25 人） | 20 分钟 |

---

## 工作流

高效开发模式的实操指南：

| 文件 | 说明 |
|------|-------------|
| [workflows/tdd-with-claude.md](./workflows/tdd-with-claude.md) | 使用 Claude 进行测试驱动开发 |
| [workflows/spec-first.md](./workflows/spec-first.md) | 规格优先开发（SDD） |
| [workflows/plan-driven.md](./workflows/plan-driven.md) | 高效使用 /plan mode |
| [workflows/iterative-refinement.md](./workflows/iterative-refinement.md) | 迭代改进循环 |
| [workflows/tts-setup.md](./workflows/tts-setup.md) | 为 Claude Code 添加文本转语音旁白（18 分钟） |
| [workflows/task-management.md](./workflows/task-management.md) | 多会话任务追踪、TodoWrite 迁移 |
| [workflows/agent-teams.md](./workflows/agent-teams.md) | 为复杂任务编排多 agent 团队 |
| [workflows/agent-teams-quick-start.md](./workflows/agent-teams-quick-start.md) | agent team 模式快速入门指南 |
| [workflows/dual-instance-planning.md](./workflows/dual-instance-planning.md) | 双实例规划：Opus 规划，Sonnet 执行 |
| [workflows/event-driven-agents.md](./workflows/event-driven-agents.md) | 事件驱动的 agent 协调模式 |
| [workflows/plan-pipeline.md](./workflows/plan-pipeline.md) | 端到端规划流水线：启动、验证、执行 |
| [workflows/design-to-code.md](./workflows/design-to-code.md) | 将 Figma/线框图转换为可运行代码 |
| [workflows/exploration-workflow.md](./workflows/exploration-workflow.md) | 系统化探索陌生代码库 |
| [workflows/pdf-generation.md](./workflows/pdf-generation.md) | 使用 Quarto/Typst 生成专业 PDF |
| [workflows/search-tools-mastery.md](./workflows/search-tools-mastery.md) | 精通 rg、grepai、Serena、ast-grep 组合工作流 |
| [workflows/skeleton-projects.md](./workflows/skeleton-projects.md) | 将久经考验的仓库用作新项目的脚手架 |
| [workflows/talk-pipeline.md](./workflows/talk-pipeline.md) | 6 阶段演讲准备：从原始素材到幻灯片 |
| [workflows/team-ai-instructions.md](./workflows/team-ai-instructions.md) | 在多开发者团队中规模化应用 CLAUDE.md |

---

## Cowork 文档

面向使用 Claude Cowork（agentic 桌面端）的知识工作者：

| 资源 | 说明 |
|----------|-------------|
| **[Cowork Hub](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/README.md)** | 完整的 Cowork 文档 |
| [入门](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/guide/01-getting-started.md) | 安装与首个工作流 |
| [能力](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/guide/02-capabilities.md) | Cowork 能做什么、不能做什么 |
| [安全指南](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/guide/03-security.md) | 安全使用实践 |
| [Prompt 库](https://github.com/FlorianBruniaux/claude-cowork-guide/tree/main/prompts) | 50+ 个开箱即用的 prompt |
| [速查表](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/reference/cheatsheet.md) | 1 页快速参考 |

---

## 推荐阅读顺序

1. **新用户**：从 `ultimate-guide.md` 的 Quick Start 部分开始
2. **日常参考**：打印 `cheatsheet.md`
3. **团队负责人**：阅读 `roles/adoption-approaches.md` 了解推广策略
4. **安全重点**：先看 `security/security-hardening.md`，再看 `security/sandbox-isolation.md`
5. **深入架构**：先看 `core/architecture.md`，再看 `diagrams/`

---

*返回 [主 README](../README.md)*
