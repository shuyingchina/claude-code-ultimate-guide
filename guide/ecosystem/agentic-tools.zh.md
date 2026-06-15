---
title: "Agent Tools: Beyond Claude Code"
description: "Comparative guide to terminal coding agents, autonomous coders, and multi-agent frameworks. Covers Hermes Agent, Codex CLI, Aider, Devin, SWE-agent, CrewAI, LangGraph, and AutoGen with a decision framework."
tags: [agents, hermes, codex-cli, aider, devin, swe-agent, crewai, langgraph, autogen, comparison]
---

# Agent 工具：超越 Claude Code

Claude Code 只是这一领域中的一种工具，而该领域自 2024 年以来已经急剧扩张。数十种 agent 框架、自主编码器和多 agent 系统相继问世，各有不同的取舍。本页梳理了这一领域，帮助你判断何时 Claude Code 是正确的选择，何时换用其他工具更合适。

**本页涵盖的内容**：terminal 编码 agent、自主编码器、多 agent 编排框架，以及 agent 编排工具。Claude Code 自身的多 agent 能力（agent 团队、事件驱动工作流、编程式用法）另有专门文档，全文均有链接。

**本页不涵盖的内容**：基于 GUI 的 AI 编码 IDE（Cursor、Windsurf、Cline），这些内容在 [AI Ecosystem §6](./ai-ecosystem.md#section-6) 中介绍。多 Claude 编排工具（Gas Town、multiclaude、Conductor 桌面应用）则在 [Third-Party Tools: Multi-Agent Orchestration](./third-party-tools.md#multi-agent-orchestration) 中介绍。

---

## 谱系

Agent 工具落在从交互式到自主式的一条谱系上：

```
Interactive pair programmer
  Claude Code, Codex CLI, Aider, Goose
        |
  Hermes Agent (interactive + scheduled + messaging gateways)
        |
Autonomous issue fixer
  SWE-agent, Devin, claude -p in CI
        |
Multi-agent framework (build your own)
  CrewAI, LangGraph, AutoGen/MAF
```

**交互式 agent**：你始终处于回路之中，审批操作、引导 agent 方向。最适合日常编码、调试，以及需求会变动的探索性工作。

**自主式 agent**：你指派一项任务，然后回来查看结果。最适合明确界定、边界清晰的任务：修复这个 bug、实现这份规格、审查这个 PR。任务描述的质量对输出质量的影响，比选择哪个 agent 更大。

**多 agent 框架**：用于构建自定义 agent 系统的库，本身并非编码工具。你用 LangGraph 来构建一个 agent，而不是用它来写代码。

---

## 第 1 节：Terminal 编码 Agent

这些工具做的事情和 Claude Code 一样：驻留在你的 terminal 中，读取你的代码库、编写代码、运行命令。区别在于模型支持、成本模型和具体能力。

---

### 1.1 Codex CLI (OpenAI)

OpenAI 对 Claude Code 的直接回应。2025 年 4 月发布，用 Rust 构建，以 Apache 2.0 协议开源。

| 属性 | 详情 |
|-----------|---------|
| **GitHub** | [openai/codex](https://github.com/openai/codex) |
| **Stars** | 86,200+（2026 年 5 月） |
| **Install** | `npm install -g @openai/codex` |
| **Language** | Rust (96%) |
| **License** | Apache 2.0 |
| **Version** | v0.134.0（2026 年 5 月 26 日） |
| **Releases** | 自 2025 年 4 月以来 800+ |
| **Contributors** | 400+ |

#### 什么是 Codex CLI？

一个用于编写、编辑和运行代码的 terminal AI agent，构建于 OpenAI 的模型家族之上。其架构与 Claude Code 高度相似：你描述一项任务，agent 读取文件、做出编辑、运行测试并迭代。主要区别在于模型提供方：Codex CLI 对接的是 GPT-4o、o3、o4-mini 以及其他 OpenAI 模型，而非 Claude。

ChatGPT Pro 和 Team 订阅用户的套餐中已包含 Codex CLI 的使用额度，对于已经在为 OpenAI 付费的团队来说，它是一种零边际成本的工具。

#### Claude Code 对比 Codex CLI

| 方面 | Claude Code | Codex CLI |
|--------|-------------|-----------|
| **模型** | 仅 Claude 3.5/4 家族 | GPT-4o、o3、o3-mini、o4-mini，以及未来的 OpenAI 模型 |
| **语言** | TypeScript | Rust |
| **许可证** | 开源 | Apache 2.0 |
| **订阅** | Anthropic Claude Max（$20-$200/月） | OpenAI ChatGPT Pro/Team（$20-$30/月） |
| **MCP 支持** | 原生，生态不断增长 | 兼容 MCP |
| **发布节奏** | 每周 | 非常高（13 个月内 800+ 个版本） |
| **记忆** | CLAUDE.md + Auto Memory | AGENTS.md 约定 |
| **Skills/Hooks** | 完整系统 | 兼容 agentskills.io 标准 |

#### 何时选择 Codex CLI

如果你已经订阅了 ChatGPT Pro 或 Team 套餐，并希望避免第二份订阅，那么它很合适。如果你在特定任务（推理、长上下文分析）上更偏好 GPT-4o 或 o3，并希望有一个原生使用这些模型的 terminal agent，它同样是正确的选择。

如果你的团队已经在 Claude Code 工作流、CLAUDE.md 文件以及 Anthropic 特有的模式上投入了精力，那么它并不合适。在两个 agent 环境之间来回切换的认知成本是真实存在的。

#### 快速上手

```bash
npm install -g @openai/codex
export OPENAI_API_KEY=sk-...
codex
```

OpenAI 的 [Codex docs](https://github.com/openai/codex/blob/main/README.md) 详细介绍了配置步骤。

---

### 1.2 Hermes Agent（原名 OpenClaw）

截至 2026 年 5 月，Stars 最多的开源 agent 框架。由 Nous Research 创建，这家 AI 实验室以其 Hermes 系列微调模型而闻名。在 2025 年底之前一直叫 OpenClaw，当时正值 Anthropic 恢复订阅支持，于是它完成了品牌重塑。

| 属性 | 详情 |
|-----------|---------|
| **GitHub** | [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) |
| **Stars** | 170,000+（2026 年 5 月） |
| **Install** | `pip install hermes-agent` 或 `curl -sSL install.hermes-agent.dev \| sh` |
| **Language** | Python (89%)、TypeScript (8%) |
| **License** | MIT |
| **Version** | v0.14.0（2026 年 5 月 16 日） |
| **发布节奏** | 每周（v0.10 4 月 16 日 → v0.14 5 月 16 日） |
| **Contributors** | 215+ |
| **Creator** | Nous Research（Teknium，@teknium1） |

#### 什么是 Hermes Agent？

一个自我改进的 terminal agent，支持 200+ 个 LLM 提供方，可在任意平台运行，并接入 22 个消息平台（Telegram、Discord、Slack、WhatsApp、Signal、Teams、LINE、SimpleX 等）。其与众不同之处在于学习回路：完成任务后，Hermes 会分析哪些做法有效，提取可复用的模式，并自动生成 skills。每一次 session 都会让 agent 在你特定的工作流上略有进步。

OpenClaw 的历史有两点很重要。其一，迁移路径很干净：`hermes-agent` 在配置过程中会导入 OpenClaw 的记忆、skills 和设置，因此切换成本很低。其二，2026 年初的 Anthropic 计费争议正是因为 OpenClaw/Hermes 被用在 Claude Max 订阅上、却没有正确的编程式计费归属。Anthropic 现在已明确将 Hermes 归入编程式用量类别（参见 [Billing: Programmatic vs Interactive](../ultimate-guide.md#the-interactiveprogrammatic-billing-split-effective-june-15-2026)）。

#### Claude Code 对比 Hermes Agent

| 方面 | Claude Code | Hermes Agent |
|--------|-------------|--------------|
| **模型** | 仅 Claude | 通过 OpenRouter、OpenAI、Anthropic、HuggingFace、本地模型支持 200+ |
| **自我改进** | 每次 session 都从零开始 | 从反复出现的模式中自动生成 skills |
| **消息接入** | Terminal + IDE | Terminal + 22 个聊天平台 |
| **Cron 调度** | Routines（Anthropic 云端） | 内置 cron，本地运行 |
| **计费** | 订阅或 API | 直接向你的 LLM 提供方付费 |
| **Agent SDK** | Anthropic 专属 | 面向任意提供方的 `ctx.llm` 插件 |
| **Skills** | SKILL.md 系统 | Skills Hub（agentskills.io）+ 自动生成 |
| **记忆** | CLAUDE.md + Auto Memory | 跨 session 持久化记忆，由 agent 自行整理 |

#### 何时选择 Hermes Agent

模型无关性是最有力的论据。如果你想用 Claude 来生成代码、用 GPT-4o 处理特定推理任务、再用本地模型（通过 Ollama）来做离线工作，Hermes 能在单个 agent 中同时处理这三者。Claude Code 做不到。

自我改进回路是真正的差异化优势。在同一代码库上经过 30-40 次 session 后，Hermes 会构建出一个专属于你项目模式的 skills 库。这种方式会以静态 CLAUDE.md 文件无法实现的方式产生复利效应——尽管这种比较很复杂，因为 CLAUDE.md 是人工编写、有意为之的，而 Hermes 的 skills 是机器生成的。

22 个消息平台集成对于那些希望通过 Telegram 或 Slack 而非 terminal 与 agent 交互的团队很有用。对大多数开发者而言这并非优先项，但对某些工作流来说至关重要。

如果你已经深度投入 Anthropic 生态（Claude Max 订阅、Routines、Agent SDK），那么它并不合适。用 Claude 模型运行 Hermes 会落入编程式计费类别，这意味着你 $200/月 Max 订阅里的 $200 额度会同时被交互式 terminal 使用和 Hermes API 调用消耗。请把这一点考虑进去。

#### 快速上手

```bash
pip install hermes-agent

# Or one-line installer
curl -sSL install.hermes-agent.dev | sh

# Import from OpenClaw if migrating
hermes import --from openclaw

# Start
hermes
```

---

### 1.3 Aider

最早的 terminal AI 结对编程工具。由 Paul Gauthier 于 2023 年发布，早于 Claude Code 出现。Aider 确立了许多后来被其他工具采纳的约定：直接编辑文件、自动 git 提交、多文件上下文窗口。

| 属性 | 详情 |
|-----------|---------|
| **GitHub** | [Aider-AI/aider](https://github.com/Aider-AI/aider) |
| **Stars** | 45,400+（2026 年 5 月） |
| **Install** | `pip install aider-install && aider-install` |
| **Language** | Python (80%) |
| **License** | Apache 2.0 |
| **Creator** | Paul Gauthier（paul-gauthier） |
| **PyPI downloads** | 5.3M+ |

#### 什么是 Aider？

一个基于 Python 的编码助手，在你本地的 git 仓库中编辑文件，并自动以描述性提交信息提交。关键特点：通过 LiteLLM 实现近乎通用的模型支持，覆盖 GPT-4o、Claude 3.5/4、Gemini、Ollama 以及数十种其他提供方。Aider 推广了"整文件"和"diff"两种编辑格式，影响了后来 agent 处理文件修改的方式。

SWE-Bench 基准测试的走势很好地讲述了这段历史：在 2024-2025 年间，Aider 在 SWE-Bench Verified 上保持榜首数月，之后才被上下文更大的模型和能力更强的 agent 超越。这一基准记录确立了它作为一款严肃工具的声誉，而不仅仅是一个图方便的封装层。

#### Claude Code 对比 Aider

| 方面 | Claude Code | Aider |
|--------|-------------|-------|
| **模型支持** | 仅 Claude | GPT-4o、Claude、Gemini、Ollama，50+ 个提供方 |
| **Git 集成** | 原生（读取 .git，运行 git） | 深度（自动提交、提交信息、blame 上下文） |
| **架构** | Anthropic 专有 | 开源，底层使用 LiteLLM |
| **文件编辑** | 基于工具（Edit、Write） | 向模型发送整文件或 diff 格式 |
| **Web 搜索** | 通过 MCP | 非原生（需要插件） |
| **Agent 回路** | 完整（多轮、工具使用） | 完整（在 architect 模式下自动接受变更） |
| **发布节奏** | 每周 | 每月（最近一次：v0.86.0，2025 年 8 月） |

最近一次发布日期（2025 年 8 月）值得留意。Aider 仍在维护、功能正常，但相对于 Claude Code 和 Hermes，其发布节奏已经放缓。这本身并非警示信号，但如果你需要最前沿的功能，值得核实。

#### 何时选择 Aider

最佳情形：你需要在一款成熟、经过实战检验的工具中获得多模型支持，又不想承担 Hermes 的运维开销。Aider 比 Hermes 更易配置，占用更小，并且有多年积累的社区文档。

它也很适合那些有良好 git 纪律、希望每一次 AI 变更都以清晰信息显式提交的团队。Aider 的自动提交行为比 Claude Code 更激进（后者默认在提交前会先询问）。

#### 快速上手

```bash
pip install aider-install && aider-install

# With Claude
export ANTHROPIC_API_KEY=sk-ant-...
aider --model claude-sonnet-4-6

# With GPT-4o
export OPENAI_API_KEY=sk-...
aider
```

完整的模型列表和配置选项参见 [aider.chat](https://aider.chat)。

---

### 1.4 Goose (AAIF/Block)

一款通用 agent，而不仅仅是编码工具。最初由 Block（前身为 Square）构建，后转交给 Linux Foundation 旗下的 AAIF（Agentic AI Infrastructure Foundation），以确保长期治理的中立性。

**完整介绍见 [AI Ecosystem §11.1: Goose](./ai-ecosystem.md#111-goose-open-source-alternative-block)。**

速览数据：45,900+ stars（2026 年 5 月），Rust (63%) + TypeScript (30%)，Apache 2.0，每日活跃开发，368+ 贡献者。相对 Claude Code 的标志性区别：提供方无关（Claude、GPT、Gemini、Ollama，15+ 个提供方），支持基于 recipe 的可复用工作流，以及异构 subagent 团队——其中每个 subagent 都可以运行不同的模型。

---

## 第 2 节：自主编码代理

这些工具无需你盯着就能运行。你给它们一段任务描述（一个 GitHub issue、一份规格说明、一份缺陷报告），它们便产出一个 pull request。其交互模型与终端代理有根本区别：迭代更少，更像是把工作分配给一位同事。

---

### 2.1 Devin (Cognition)

第一个商业化的完全自主软件工程师。闭源、云端托管、企业级定价。

| 属性 | 详情 |
|-----------|---------|
| **官网** | [devin.ai](https://devin.ai) |
| **类型** | 云 SaaS，专有 |
| **定价** | Core: $20/mo（按用量付费的 ACU），Team: $500/mo（250 ACU），Enterprise：定制 |
| **发布时间** | 2024 |
| **估值** | $25B（2026 年 4 月一轮融资） |
| **重要收购** | Windsurf AI 原生 IDE（2025 年 7 月） |
| **企业客户** | Goldman Sachs、Microsoft、Palantir、Citi、Dell |

#### 什么是 Devin？

一个自主软件工程师，运行在基于云的 Linux VM 中，拥有自己的 shell、代码编辑器和浏览器。Devin 会规划自己的方案、编写代码、运行测试、阅读错误信息，并不断迭代，直到任务完成或陷入困境。主要界面是 Slack：你发送一条诸如 "fix issue #342" 的消息，Devin 完成后会开一个 PR。

计费以 ACU（Agent Compute Units，代理计算单元）为单位，1 ACU 大致对应 15 分钟的代理工作。一个复杂功能可能消耗 10-20 个 ACU；一个简单缺陷修复可能用掉 1-3 个。

#### Claude Code 对比 Devin

| 方面 | Claude Code | Devin |
|--------|-------------|-------|
| **执行环境** | 你的本地机器 | 云端 Linux VM（沙箱化） |
| **交互模型** | 交互式（你盯着看） | 异步（分配后再回来检查） |
| **状态** | 会话范围内 | 在整个任务中持久保持 |
| **定价** | 订阅制（$20-$200/mo） | 按任务的 ACU 计费（约 $0.07-$0.15/ACU） |
| **谁主导** | 你（结对编程） | 代理（自主运行，你来审查） |
| **任务规格** | 对话式、迭代式 | 预先给出（规格越好，输出越好） |
| **浏览器访问** | 通过 MCP（Playwright） | 内置、原生 |
| **代码审查集成** | 你在自己的 IDE 中审查 | Devin 发布一个 PR，你在 GitHub 上审查 |

#### 何时选择 Devin

当任务规格清晰、边界明确、且不需要持续的判断决策时，Devin 表现最佳。重构某个特定模块、实现一个有文档说明的 API 端点、修复一个已知根因的回归：这些都是 Devin 的任务。设计一套新的系统架构、调试一个晦涩的生产问题、或编写依赖代码库中隐式上下文的代码：这些则需要更具交互性的循环。

$500/月的 Team 套餐（250 ACU）相当可观。在这个价位上，你购买的是异步价值：开发者不会被卡住等待代理输出、多个代理并行处理多项任务、无需上下文切换。如果你的瓶颈是开发者的注意力而非纯粹的吞吐量，那么 Devin 值得这笔账。如果你希望保持在循环中并进行交互式迭代，$200/月的 Claude Code 在每一美元上能提供更多价值。

Windsurf 收购（2025 年 7 月）标志着 Cognition 正在向一个完整的开发者环境迈进，而不仅仅是一个后台代理。请关注将交互式编码（Windsurf IDE）与自主任务执行（Devin）整合在同一产品中的工作流。

---

### 2.2 SWE-agent (Princeton)

一个专门为仅凭 issue 描述就解决 GitHub issue 而设计的学术型代理。NeurIPS 2024 论文，普林斯顿 NLP 组与斯坦福。

| 属性 | 详情 |
|-----------|---------|
| **GitHub** | [SWE-agent/SWE-agent](https://github.com/SWE-agent/SWE-agent) |
| **Star 数** | 19,300+（2026 年 5 月） |
| **论文** | NeurIPS 2024 |
| **许可证** | MIT |
| **语言** | Python (95%) |
| **版本** | v1.1.0（2025 年 5 月） |
| **维护方** | 普林斯顿 NLP 组 + 斯坦福 |

#### 什么是 SWE-agent？

一个代理流水线，接收一个 GitHub issue URL 和一个模型，然后尝试复现缺陷、编写修复并产出补丁。它的架构使用了一个 Agent-Computer Interface (ACI) 层，将终端、文件编辑和测试运行抽象为一套一致的命令，而不论底层环境如何。这种 ACI 设计是其主要的学术贡献：它表明代理性能与环境暴露信息的好坏强相关，而不仅仅取决于模型的原始能力。

SWE-agent + Claude 3.7 在 SWE-Bench Full（开放权重）上保持着最先进水平。该基准是关键背景：SWE-Bench 衡量代理能端到端解决的真实 GitHub issue 的百分比，而 SWE-agent 正是以该基准作为优化目标而设计的。

#### 何时选择 SWE-agent

主要用于学术和研究用途。如果你想系统地评估不同模型在真实 GitHub issue 上的表现，SWE-agent 是合适的工具，因为它具备生产工具会跳过的可复现性基础设施（轨迹日志、评估框架、配置 YAML）。

对于生产环境的批量 issue 解决，Devin 的云沙箱和更好的错误恢复使其更为实用。SWE-agent 要求你自行搭建环境并手动处理失败。

其研究价值是实实在在的：构建代理系统的团队可以使用 SWE-agent 的轨迹数据（在 issue 解决运行中生成）来微调模型。Nous Research 的 SWE-agent-LM-32b（开放权重，在开放模型中于 SWE-Bench 上达到 SoTA）就是在 SWE-agent 生成的轨迹上训练的。

```bash
pip install swe-agent

# Run on a GitHub issue
sweagent run \
  --agent.model.name=claude-sonnet-4-6 \
  --env.repo.github_url=https://github.com/org/repo \
  --problem_statement.github_url=https://github.com/org/repo/issues/123
```

---

### 2.3 无头模式下的 Claude Code

Claude Code 自身的自主模式：`claude -p "task"` 以非交互方式运行单条指令并退出。与 CI/CD 结合后，它便成为一个自主代理，可由 GitHub 事件触发、通过 Routines 按计划运行、或通过 Agent SDK 以编程方式处理任务。

**自 2026 年 6 月 15 日起，这归入程序化计费类别。** 关于额度上限和超额费率，参见 [计费：程序化 vs 交互式](../ultimate-guide.md#the-interactiveprogrammatic-billing-split-effective-june-15-2026)。

模式：

```bash
# Single task, exits when done
claude -p "Write tests for src/auth.ts, aim for 80% coverage"

# GitHub Actions: triggered by issue label
# See workflows/event-driven-agents.md for the full pattern

# Agent SDK: programmatic with tools
# See ai-ecosystem.md §14 (Claude Managed Agents)
```

交叉引用：
- **事件驱动模式**：[workflows/event-driven-agents.md](../workflows/event-driven-agents.md)
- **代理团队**：[workflows/agent-teams.md](../workflows/agent-teams.md)
- **托管代理（云端）**：[ai-ecosystem.md §14](./ai-ecosystem.md#14-claude-managed-agents)

---

## 第 3 节：多代理框架

这些不是编码工具。它们是用于从零构建自定义多代理应用的库：营销流水线、研究自动化、文档处理、客户支持机器人。如果你正在构建一个内部带有 AI 代理的产品，你会用到它们；如果你是一名希望让代理替你写代码的开发者，则不会。

与 Claude Code 的关系：Claude（模型）可以作为驱动这些框架所构建代理的 LLM 之一。这些框架本身与 Claude Code 并不构成竞争，正如 Express.js 不与浏览器竞争一样。

---

### 3.1 CrewAI

基于角色的多代理编排。对于希望按工作职能（Researcher、Writer、Editor）定义代理并让它们在结构化任务上协作的团队，这是占主导地位的选择。

| 属性 | 详情 |
|-----------|---------|
| **GitHub** | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) |
| **Star 数** | 52,300+（2026 年 5 月） |
| **语言** | Python (99%) |
| **许可证** | MIT |
| **版本** | v1.14.5（2026 年 5 月 18 日） |
| **执行量** | 据报告超过 20 亿次代理任务执行 |
| **下载量** | 2700 万+ |
| **企业客户** | 150+ |

#### 什么是 CrewAI？

你用一个角色（role）、一个目标（goal）和一段背景故事（backstory）来定义代理（即 "crew"）。你定义任务并将其分配给代理。CrewAI 负责路由：顺序式（A 完成后 B 才开始）、并行式（A 和 B 同时运行）或层级式（一个管理者代理向专家代理委派）。每个代理都可以使用工具，包括 MCP 服务器和网页搜索。支持多个 LLM 提供商（Claude、GPT、Gemini、Ollama）。

它与 LangChain（那个它经常被拿来比较的更老的框架）截然不同，因为它完全不依赖 LangChain。它是一个独立的 Python 库。

#### 何时使用 CrewAI

对于能用人类角色来描述工作流的团队，这是恰到好处的抽象层级。如果你能说出 "我想要一个收集信息的研究员、一个起草内容的写作者和一个润色内容的编辑"，CrewAI 就会处理编排和代理间通信。你编写的是代理定义，而非编排代码。

当你的工作流具有复杂的条件分支、需要在失败之间持久执行、或需要对状态如何在代理间传递进行细粒度控制时，请避免使用它。LangGraph 在这些场景下处理得更好。

```python
from crewai import Agent, Task, Crew, Process

researcher = Agent(
    role="Technical Researcher",
    goal="Find accurate technical information",
    backstory="Expert at synthesizing documentation and research papers",
    llm="claude-sonnet-4-6"
)

writer = Agent(
    role="Technical Writer",
    goal="Write clear, accurate documentation",
    backstory="Experienced at translating technical concepts",
    llm="claude-sonnet-4-6"
)

task = Task(
    description="Research and document the new auth API endpoints",
    expected_output="Markdown documentation with examples",
    agent=writer,
    context=[research_task]  # researcher's output feeds writer
)

crew = Crew(agents=[researcher, writer], tasks=[task], process=Process.sequential)
result = crew.kickoff()
```

---

### 3.2 LangGraph

来自 LangChain 的基于图的代理编排。比 CrewAI 更底层、更灵活，更适合复杂的有状态工作流。

| 属性 | 详情 |
|-----------|---------|
| **GitHub** | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) |
| **Star 数** | 33,100+（2026 年 5 月） |
| **语言** | Python (99%) + 提供 JS 版本 |
| **许可证** | MIT |
| **版本** | v1.2.2（2026 年 5 月 26 日） |
| **生产用户** | Klarna、Replit、Elastic |

#### 什么是 LangGraph？

一个代理构建框架，将工作流建模为带有节点（代理步骤）和边（转换）的有向图。其关键原语是状态（一个在所有节点间持久存在的带类型字典）、条件边（基于状态的分支）和持久化（检查点机制，使被中断的工作流从上一个检查点恢复，而非从头开始）。人在环路（Human-in-the-loop）是一等模式：你可以在任意节点暂停执行，等待人类决策后再继续。

LangGraph 不捆绑代理。你定义工作流逻辑，并接入你想要的任何 LLM。该框架确保状态转换可预测、失败可恢复、且工作流可以逐步调试。

#### 何时使用 LangGraph

当你的代理需要在失败中存活、需要根据运行时条件分支、或需要在特定决策点获得人类批准时，它是合适的工具。例如：一个代码审查流水线，当代理检测到与安全相关的变更时升级给人类处理；一个数据处理工作流，在每个昂贵步骤后设置检查点，使重启时不会重新处理已完成的阶段；一个多步骤研究代理，在遇到含糊的来源材料时暂停以获取人类指导。

学习曲线比 CrewAI 更陡。当工作流的复杂度足以证明这项投入是值得的时候，它便物有所值。

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    task_complete: bool

graph = StateGraph(AgentState)
graph.add_node("agent", call_agent)
graph.add_node("tools", call_tools)
graph.add_conditional_edges("agent", should_continue, {"continue": "tools", "end": END})
graph.add_edge("tools", "agent")
graph.set_entry_point("agent")

app = graph.compile(checkpointer=MemorySaver())  # Durable execution
```

LangSmith（LangChain 的可观测性产品）原生集成，用于调试和追踪代理运行。

---

### 3.3 AutoGen / Microsoft Agent Framework

Microsoft 的多代理框架，正处于从原始 AutoGen 库（自 2025 年 9 月起进入维护模式）向 Microsoft Agent Framework (MAF) 过渡的中途，后者将 AutoGen 与 Semantic Kernel 合并为一个 SDK。

| 属性 | 详情（MAF） |
|-----------|---------|
| **GitHub** | [microsoft/agent-framework](https://github.com/microsoft/agent-framework) |
| **Star 数** | 10,800+（MAF，活跃） |
| **遗留 GitHub** | [microsoft/autogen](https://github.com/microsoft/autogen)（58,400 stars，自 2025 年 9 月起进入维护模式） |
| **语言** | Python + C# + TypeScript |
| **许可证** | MIT |
| **版本** | python-1.6.0（2026 年 5 月 22 日） |
| **生产发布** | v1.0（2026 年 4 月） |

#### 什么是 Microsoft Agent Framework？

MAF 是 AutoGen（Python，对话式多代理）与 Semantic Kernel（C# + Python，函数调用抽象）的合并。其成果是一个跨运行时框架：Python 代理可以与 .NET 代理协作，全部由同一个消息层支撑。它实现了 A2A（Agent-to-Agent）协议——Microsoft 对代理互操作性的贡献——并支持 MCP。

AutoGen 的 star 数（58,400）反映了它的历史声誉。AutoGen 开创了 "可对话代理"（conversable agent）模式，即代理在结构化的对话循环中相互交谈。即便实现已经演进，该模式仍是该框架中占主导地位的思维模型。

#### 何时使用 MAF

非常适合 Microsoft 生态系统的团队：.NET + Python 团队、Azure 部署、以及已经确立 Semantic Kernel 的企业环境。其跨运行时的说法名副其实：一个 Python 代理可以调用以 .NET Semantic Kernel 函数实现的工具。

对于没有现成 .NET 投入的团队，吸引力较小。如果你只用 Python，CrewAI 或 LangGraph 拥有更大的社区和更多教程。

---

### 3.4 Anthropic Agent SDK

Anthropic 自己的、用于以编程方式构建多代理系统的框架，与 Claude Code 有别。详见 [AI 生态系统 §14：Claude 托管代理](./ai-ecosystem.md#14-claude-managed-agents)。

关键区别在于：Claude Code 是一个你作为开发者直接使用的成品；而 Agent SDK 是一个库，你用它来构建内部含有 Claude 的产品。Agent SDK 通过 Messages API 处理工具使用、上下文管理和多代理协调。它同样归入程序化计费类别（参见上文的计费交叉引用）。

---

## 第 4 节：Agent 编排工具

位于 agent 框架之上、用于管理 agent 如何大规模部署、路由和运行的工具。不要与多 Claude 编排工具（Gas Town、multiclaude）混淆，后者在 [Third-Party Tools](./third-party-tools.md#multi-agent-orchestration) 中介绍。

---

### 4.1 Conductor（Gemini CLI 方法论）

这是一种开发方法论，而非产品。"Conductor" 最初是 Gemini CLI 的一个扩展，它强制执行 Context、Spec、Plan、Implement 的工作流：在编写任何代码之前，agent 先创建并提交一份 spec 文档，然后是一份 plan 文档，最后再依照这两者进行实现。

| 属性 | 详情 |
|-----------|---------|
| **GitHub** | [gemini-cli-extensions/conductor](https://github.com/gemini-cli-extensions/conductor) |
| **Stars** | 3,600+（2026 年 5 月） |
| **License** | Apache 2.0 |

该方法论已通过社区仓库移植到 Claude Code：[lackeyjb/claude-conductor](https://github.com/lackeyjb/claude-conductor)、[ryanmac/code-conductor](https://github.com/ryanmac/code-conductor)，以及 wshobson/agents 插件市场。这些项目单独来看都没有形成显著的影响力，但其模式本身（先 spec 后代码、提交文档）直接对应 Claude Code 的 [Spec-First Development workflow](../workflows/spec-first.md)。

---

### 4.2 Conductor（Microsoft CLI）

这是一个与 Gemini 版本完全独立的项目。它是一个 YAML 优先的 CLI，用于确定性的多 agent 工作流，其中路由逻辑是静态配置，而非 LLM 的决策。

| 属性 | 详情 |
|-----------|---------|
| **GitHub** | [microsoft/conductor](https://github.com/microsoft/conductor) |
| **Stars** | 158（2026 年 5 月，全新项目） |
| **License** | MIT |
| **发布时间** | 2026 年 5 月 14 日（Microsoft Open Source Blog） |

核心理念：用 YAML 定义你的 agent 工作流（哪些 agent 按顺序运行、哪些并行运行、每个使用哪个模型、各阶段之间传递什么），并以确定性方式执行。编排循环中没有 LLM，只有 agent 步骤中才有。同时支持 GitHub Copilot SDK 和 Anthropic Agent SDK 作为提供方。处于非常早期的阶段（撰写时仅 158 stars、发布才几天），但有 Microsoft 开源团队作后盾。

---

### 4.3 Hermes Control Room

这是 Shann（@shannhk，里斯本）制作的一个社区模板，用于在 VPS 上管理一支 Hermes agent 团队。并非 Nous Research 的项目。

| 属性 | 详情 |
|-----------|---------|
| **GitHub** | [shannhk/hermes-agent-control-room](https://github.com/shannhk/hermes-agent-control-room) |
| **Stars** | 474（2026 年 5 月） |
| **存在时长** | 12 天（截至 2026 年 5 月 27 日） |
| **类型** | 模板/文档，而非可执行软件 |

其概念是：一套文件夹结构，包含治理文档、已部署 agent 的注册表、常见操作的运行手册（runbook），以及 8 个捆绑的 Hermes skills，用于 VPS 配置、任务路由、备份、安全审计和 cron 规划。各 agent 共享一个基于文件系统的任务总线（按专长划分的 inbox/working/outbox/archive）。编排器读取 control room 文档以了解 agent 的能力，通过该总线路由任务，并综合处理结果。

对于任何运行 3 个以上 Hermes agent 的人来说，这种模式是合理的。但该具体仓库太新（7 次提交），不建议作为生产依赖。可关注未来带有更多运行加固的 v1.0 版本。

---

## 第 5 节：决策框架

### 完整对比矩阵

| 工具 | 开源 | Stars | 模型支持 | 模式 | 语言 | 成本 |
|------|------------|-------|---------------|------|----------|------|
| **Claude Code** | 是（TS） | 112K | 仅 Claude | 交互式 + headless | TypeScript | $20-$200/月 |
| **Codex CLI** | 是 | 86K | GPT-4o、o3、o4-mini | 交互式 + headless | Rust | 包含在 ChatGPT Pro/Team 中 |
| **Hermes Agent** | 是（MIT） | 170K | 200+ 提供方 | 交互式 + cron + 消息传递 | Python | 按 LLM 调用付费 |
| **Aider** | 是 | 45K | 50+ 提供方 | 交互式 | Python | 按 LLM 调用付费 |
| **Goose** | 是 | 46K | 15+ 提供方 | 交互式 + subagents | Rust | 按 LLM 调用付费 |
| **Devin** | 否 | N/A | 专有 | 完全自主 | 专有 | $20-$500/月 |
| **SWE-agent** | 是（MIT） | 19K | 任意（Claude、GPT……） | 自主（issue → PR） | Python | 按 LLM 调用付费 |
| **CrewAI** | 是（MIT） | 52K | 50+ 提供方 | 框架（自行构建） | Python | 框架免费 |
| **LangGraph** | 是（MIT） | 33K | 任意 | 框架 | Python/JS | 框架免费 |
| **AutoGen/MAF** | 是（MIT） | 58K/11K | 任意 | 框架 | Python/C#/TS | 框架免费 |

### 场景到工具指南

| 场景 | 推荐 |
|-----------|-------------|
| 日常编码，已订阅 Claude Max | Claude Code |
| 日常编码，已订阅 ChatGPT Pro | Codex CLI |
| 日常编码，想用任意模型 | Hermes Agent 或 Aider |
| 日常编码，通用 agent | Goose |
| 分派一个任务，回来时拿到一个 PR | Devin（$500/月）或 CI 中的 `claude -p` |
| 自主修复 GitHub issue、研究/基准测试 | SWE-agent |
| 编排多个 Claude Code 实例 | Gas Town、multiclaude、Ruflo（见 [Third-Party Tools](./third-party-tools.md#multi-agent-orchestration)） |
| 构建带角色的多 agent 产品 | CrewAI |
| 构建有状态、可恢复的工作流 | LangGraph |
| 用 Microsoft 技术栈在 .NET + Python 中构建 | AutoGen/MAF |
| Anthropic 生态系统、云托管 agent | Anthropic Agent SDK（见 [ai-ecosystem.md §14](./ai-ecosystem.md#14-claude-managed-agents)） |
| 在 VPS 上管理一支 Hermes agent 团队 | Hermes Control Room 模式 |

### 模型锁定问题

在 Claude Code、Codex CLI、Hermes、Aider 和 Goose 之间做选择时，最能厘清思路的一个问题是：该工具是只需配合一家模型提供方工作，还是需要配合多家？

如果你已经投入 Claude 及 Anthropic 生态系统（订阅、Routines、Agent SDK、CLAUDE.md 工具链），那么 Claude Code 毫无疑问是正确的选择。其集成是原生的，且 Anthropic 的功能迭代速度很快。

如果你需要模型灵活性（用本地模型处理敏感代码、用更便宜的模型处理常规任务、用特定模型进行基准测试），Hermes Agent 以最高的自动化程度覆盖了最广的范围。Aider 和 Goose 是更简单、占用更小的替代方案。

如果你的团队是 OpenAI 优先且已经在为 ChatGPT Pro 付费，那么 Codex CLI 不会产生任何额外成本。

### 自主性与控制权的权衡

更高的自主性意味着 agent 能在你不盯着的情况下完成更多工作，但也意味着在模糊任务上有更多偏离正轨的可能。合适的自主性级别取决于你的任务被定义得有多清晰，而非取决于哪个工具"更强大"。

Claude Code 的 headless 模式（`claude -p`）和 SWE-agent 给你的是受控的自主性：你设定任务，agent 运行，你审查输出。Devin 通过云端沙箱给你最大化的自主性：agent 拥有完整的 Linux 环境，并可能采取你未曾预料到的行动。能力更强，但合并前需要更多审查。

交互式 agent（Claude Code 终端、Hermes、Aider、Goose）给你实时的控制权。你看着 agent 思考，在它出错时纠正它，并批准破坏性操作。对于需求在会话中途发生变化的探索性工作，交互式虽然看起来更费手工，却比自主式更快。

---

## 交叉引用

- **多 Claude 编排**（Gas Town、multiclaude、Ruflo、Conductor 桌面版）：[Third-Party Tools: Multi-Agent Orchestration](./third-party-tools.md#multi-agent-orchestration)
- **Goose 深度解析**：[AI Ecosystem §11.1](./ai-ecosystem.md#111-goose-open-source-alternative-block)
- **用 Anthropic SDK 构建自定义 agent**：[AI Ecosystem §14](./ai-ecosystem.md#14-claude-managed-agents)
- **Claude Code 自身的 agent 团队模式**：[workflows/agent-teams.md](../workflows/agent-teams.md)
- **事件驱动的自主模式**：[workflows/event-driven-agents.md](../workflows/event-driven-agents.md)
- **编程式计费（Hermes、Codex CLI、第三方框架）**：[Ultimate Guide: Billing Split](../ultimate-guide.md#the-interactiveprogrammatic-billing-split-effective-june-15-2026)
- **Agent 框架工程（理论框架）**：[core/agent-harness.md](../core/agent-harness.md)
- **编码 agent 对比矩阵**（23 个工具，11 项标准）：[coding-agents-matrix.dev](https://coding-agents-matrix.dev)
