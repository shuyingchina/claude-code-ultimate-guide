---
title: "Agent Harness Engineering"
description: "The nine-component infrastructure that turns a raw LLM into a reliable production agent — from while-loop engine to permission enforcement"
tags: [guide, agents, architecture, security, observability]
---

# Agent Harness 工程

> **可信度**：第 1 级 —— 多个独立来源（Martin Fowler、arXiv 2605.18747、Anthropic、O'Reilly、AWS、GitHub）在这一框架上达成一致。
>
> **阅读时间**：约 25 分钟

---

## 核心论点

一个原始的 LLM 并不是 agent。只有当它连接到 harness 时，它才会成为 agent。

Martin Fowler、Addy Osmani、O'Reilly 的 2026 AI Radar 以及 arXiv 2605.18747（2026 年 5 月）都得出了一致的结论：工程上真正相关的单元不是模型本身，而是包裹它的基础设施。Fowler 将 harness 定义为一种"控制论调节器"（cybernetic governor），它结合前馈与反馈，将 agent 的行为调控至期望状态。正是 harness 让"AI 生成大部分代码"在规模化场景下可持续，而不至于逐渐滑向难以维护的系统。

截至 2026 年 5 月，57% 的组织已有 agent 运行在生产环境中，而 32% 的组织将质量列为其首要障碍（LangChain State of Agent Engineering）。那些已经弥合这一差距的团队有一个共同点：他们工程化了 harness，而不仅仅是 prompt。

---

## 目录

1. [三大基础属性](#1-three-foundational-properties)
2. [九大组件](#2-the-nine-components)
3. [致命三要素：安全模型](#3-the-lethal-trifecta-security-model)
4. [CI/CD Agentic 模式](#4-cicd-agentic-patterns)
5. [数字孪生测试](#5-digital-twin-testing)
6. [可观测性技术栈](#6-observability-stack)
7. [测试分布反模式](#7-test-distribution-anti-pattern)
8. [创建者-验证者模式](#8-creator-verifier-pattern)
9. [参考架构](#9-reference-architecture)

---

## 1. 三大基础属性

arXiv 2605.18747（《Code as Agent Harness》，2026 年 5 月）形式化了三个区分 harness 与简单 LLM 包装层的属性：

**可执行性（Executability）**：harness 能够验证 agent 实际做了什么，而不仅仅是它声称要做什么。一个只记录 prompt 与 completion 的 harness 不具备可执行性，因为它无法区分一次成功的工具调用与一次幻觉出来的调用。

**可检视性（Inspectability）**：当某个环节失败时，harness 会产出可操作的诊断输出。指向 prompt 组装步骤的堆栈跟踪。标注了当时哪些规则与 skill 处于激活状态的摩擦事件（friction event）。按组件统计的 token 消耗。没有可检视性，调试一次 agent 失败就需要从日志中重建整个 session，这既昂贵又往往不完整。

**有状态性（Statefulness）**：harness 在多个 session 之间保持连续性。Session 状态被外部化保存，而不是留存在模型的上下文窗口里。当 agent 在一次上下文重置之后恢复运行时，它无需人类提供完整的情况说明，就能重建自己之前所处的位置。Anthropic 自己的遥测数据显示，session 时长的 99.9 分位数在 2026 年 1 月超过了 45 分钟，而 2025 年 10 月还只是 25 分钟。在这样的时长下，有状态性不再是可选项。

---

## 2. 九大组件

这九个组件在 Claude Code、Anthropic SDK、OpenAI Agents SDK、LangGraph、AWS Bedrock AgentCore 以及 Factory.ai Missions 中均有体现。没有哪一个工具会以完全相同的方式实现全部九项，但其结构足够一致，可以作为一份评估清单，用于针对新工具或新框架来衡量一个 harness。

### 2.1 While-Loop 引擎

主循环：感知（读取上下文、工具输出、最新的用户指令）、规划（用组装好的 prompt 调用 LLM）、行动（执行工具）。这是心跳。Anthropic SDK、OpenAI Agents SDK 和 LangGraph 各自以不同方式实现它（Anthropic 以流式优先，LangGraph 基于图），但三者都将这个循环作为核心抽象。

问题往往出在哪里：不对迭代次数设上限的循环；不处理 LLM 拒绝（refusal）或模糊工具调用的循环；任由上下文在没有摘要的情况下持续增长、直到撞上窗口上限而中止的循环。

### 2.2 上下文管理

在每一次循环迭代时进入 prompt 的内容：对话历史、工具输出、检索到的记忆、当前任务状态、来自 CLAUDE.md 的规则。难点在于上下文既有限又昂贵。相关策略：

- **压缩 / 摘要（Compaction / summarization）**：用一段压缩后的摘要替换较早的回合。Claude Code 的 `/compact` 是手动完成这件事的；健壮的 harness 会在用量越过阈值时自动执行。
- **滑动窗口（Sliding window）**：原文保留最近 N 个回合，其余全部摘要化。
- **检索增强上下文（Retrieval-augmented context）**：从长期存储中检索相关片段，而不是把所有内容都装进窗口。

ACE 流水线（参见 [context-engineering.md §6](./context-engineering.md#6-the-ace-pipeline)）是上下文管理之上的配置持久化（Config-Persistence）层：它管控哪些规则与 skill 在各个 session 之间被加载。

### 2.3 工具注册表（Tool Registry）

可用工具的目录：名称、schema、描述、权限、成本估算。静态工具注册表会在每次调用时加载所有工具的 schema。动态注册表（"按需工具搜索"）则只加载当前任务可能需要的部分。

Anthropic 的内部数据（引自 Fowler 的文章，来源：从业者帖子）指出，相比静态加载，动态工具分发可减少 37% 的 token 用量。这一数字尚未被独立复现，但其方向性结论是可信的：在模型只需要 4 个工具时却给它 40 个工具 schema，只会增加噪声和成本。

MCP（Model Context Protocol）工具必须经过一个网关，该网关在工具执行之前校验调用方 agent 的身份。这并非一个可选的加固步骤；它是防止通过链式工具调用实现权限提升的基线要求。

### 2.4 子 Agent 管理（Sub-Agent Management）

向拥有各自上下文窗口与任务范围的专门子 agent 进行委派。编排者（orchestrator）派生一个 worker，提供一段边界清晰的任务描述，并接收一份结构化结果。该 worker 并不共享编排者的完整上下文；它只接收自己所需的内容。

Factory.ai Missions 将这一点形式化：编排者 agent 拆解需求，把实现委派给 worker，再把完成的工作路由给对抗式的验证者（validator）agent。在一个有文档记录的 Slack 克隆项目中，独立的验证者在任何代码被合并之前就捕获了 81 个问题，由此产生的"修复型特性"占了 34% 的实现工作量。

关键约束：子 agent 的权限不得从父级继承。最小权限原则适用于委派边界。

### 2.5 内建 Skill（Built-in Skills）

无需 LLM 调用的原生操作：文件读写、网络搜索、代码执行、shell 命令。自 2025 年末起，Claude Code 将 skill 形式化为可加载的模块。这一区分很重要：skill 是确定性的（读取这个文件，运行这个测试），而一次 agent 行动则涉及 LLM 推理。

测试分布反模式（下文第 7 节）部分正是源于把 skill 测试（确定性的、可单元测试的）与 agent 推理测试（概率性的、需要 LLM-as-judge 或行为模拟）混为一谈。

### 2.6 Session 持久化（Session Persistence）

能够在上下文重置与 session 中断中存活的状态。它与长期记忆（一个更高层的概念）并不相同。在 harness 层面，持久化意味着：agent 能够从外部化的产物中重建其当前任务状态，而不必依赖上下文内的对话历史。

Factory.ai Missions 使用一个共享产物层（验证契约、特性清单、skill 定义）来跨越多日任务的上下文限制。E2B 和 Northflank 通过持久化的 sandbox 状态在基础设施层面提供这一能力。Anthropic Claude Managed Agents 则将其作为一项带检查点（checkpointing）的产品特性提供。

### 2.7 动态 Prompt 组装（Dynamic Prompt Assembly）

这一步把当前状态（任务描述 + 相关上下文 + 工具定义 + 记忆 + 规则）转化为实际发送给 LLM 的 prompt。它在各个框架之间并未标准化。LangChain、LangGraph 和 Anthropic SDK 各有不同的抽象。

组装出错的地方在于：与用户指令相冲突的规则注入；以会令模型选择困惑的方式相互重叠的工具 schema；浮现出过时上下文的记忆检索。那些让组装过程可见（记录最终组装好的 prompt，而不仅仅是响应）的 harness，调试起来要容易得多。

### 2.8 生命周期 Hook（Lifecycle Hooks）

在既定时刻触发的注入点：LLM 调用前、LLM 调用后、工具执行前、工具执行后、出错时。Claude Code 通过 settings.json 的 hooks 系统实现这一点。AWS Bedrock AgentCore 和 GitHub Agentic Workflows 各有其 hook 模型。

Hook 是你插入以下内容的地方：可观测性埋点、权限校验、限流、输出净化、审计日志。内联（阻塞）运行的 hook 可以在坏行为执行之前将其中止。异步（发后不理）运行的 hook 则适合那些无需打断循环的日志记录。

### 2.9 权限强制（Permission Enforcement）

每一个行动都要经过策略层。不是以人工审查的形式（关于它为何在规模化时失效，参见第 3 节），而是作为一种在工具调用执行之前发生的结构性强制。

两种行之有效的机制：

1. **Sandbox 隔离**：agent 运行在一个让破坏性行动在物理上不可能发生的环境中——不只是被策略禁止，而是在给定的网络、文件系统与进程约束下根本无法实现。Kubernetes agent-sandbox、E2B microVM 以及 Northflank BYOC runner 在硬件层面实现了这一点。

2. **身份网关**：每一次 MCP 工具调用都在调用时用一个按 session 颁发的凭证进行身份验证，而不是使用静态 API key。Strata Maverics 与 Microsoft Entra Agent ID 通过 OAuth OBO（On-Behalf-Of）流程实现这一点，将权限限定在当前任务上下文的范围内。

---

## 3. 致命三要素：安全模型

Simon Willison 在 2025 年创造了这一术语（参见 [martinfowler.com/articles/202508-ai-thoughts.html](https://martinfowler.com/articles/202508-ai-thoughts.html)）：

**私有数据 + 不可信内容 + 对外通信 = 有文档记录的数据外泄向量。**

三者中的任意两者都尚可管理。但三者凑齐、又缺乏结构性隔离时，便会形成一条路径：攻击者在 agent 将要读取的数据中植入指令（一份文档、一段代码注释、一张 Jira 工单），agent 借助其对私有数据的访问权限处理这些指令，随后又利用其通信能力将数据外泄。

这并非空谈。GitHub Security 已记录到在 Copilot 中经由恶意仓库内容发起的 prompt 注入攻击。其防御之道不是更好的 prompt 工程；而是结构性隔离。

### 防御层

| 层 | 机制 | 实现 |
|-------|-----------|---------------|
| 网络隔离 | 除一份显式 allowlist 外，agent 无法访问任何外部端点 | GitHub Agentic Workflows：基于 allowlist 的 Squid 代理；Northflank：出站防火墙 |
| 文件系统隔离 | agent 写入临时工作区，而非宿主文件系统 | Kubernetes agent-sandbox、E2B microVM |
| 身份范围限定 | 每一次工具调用都携带一个具备所需最小权限的按 session 凭证 | Strata Maverics、Microsoft Entra Agent ID |
| 输出校验 | agent 生成的内容在抵达任何生产面之前要先经过一个威胁检测步骤 | GitHub Agentic Workflows：Safe Outputs 模式（Semgrep + TruffleHog + LlamaGuard） |
| 只读执行上下文 | agent 读取代码库但不能直接写入；写入须经过 PR/审查关卡 | GitHub Agentic Workflows 的默认姿态 |

### 为何仅靠人工审查会失效

Anthropic 的内部数据（责任共担模型文档，2026 年 4 月）：生产环境中 93% 的 agent 权限请求是在缺乏充分审查的情况下被批准的。这并非对参与其中的人的指责；它是数量与认知负荷所导致的结构性后果。当一个人每小时批准 50 个权限对话框时，逐个批准便沦为一种形式。

能够规模化的防御：结构性隔离（让某些行动变得不可能）与第二 agent 验证（创建者-验证者模式，第 8 节）。人工审查仍适用于高风险、低频次的决策，而不适用于例行的 agent 行动。

---

## 4. CI/CD Agentic 模式

已有三个平台将 agent 产品化为一种 CI/CD 原语。在它们之间做选择是一项架构决策，而非功能对比。

### GitHub Agentic Workflows

核心概念：`gh aw compile` 接收一份以 Markdown 写成的 agent workflow 定义，并产出一个 `.lock.yml`——一个经过加固的 GitHub Actions 文件，它在强制隔离下执行该 workflow。安全属性是在编译这一步被固化进去的，而不是事后补加的。

**执行模型**：agent 运行在只读上下文中。它可以分析与生成。任何写入（提交、评论、部署）都要经过"Safe Outputs"——一个独立的 job，它在生成的产物触及生产面之前对其进行校验。Safe Outputs 会在 agent 生成的 diff 被应用之前，对其运行 Semgrep（SAST）、TruffleHog（密钥检测）和 LlamaGuard（有害内容检测）。

**代码审查集成**：截至 2026 年，GitHub Copilot Code Review 已处理超过 6000 万次代码审查。在 Code Review Bench（Martian，2026 年 3 月，超过 20 万个开源 PR，评测了 17 个工具）上，Augment Code 以 62.8% 的召回率领先，Copilot 为 53.3%。Graphite 在精确率上以 75% 领先，但召回率仅为 8.8%（高精确率意味着误报少，低召回率意味着漏掉了许多真实的 bug）。没有任何一个工具能在两项指标上同时领先。

**c-CRAB 基准**（arXiv 2603.23448）：在以可执行测试套件作为预言（oracle）的 pull request 上，Claude Code 取得了 32.1% 的通过率。四个工具的并集达到 41.5%。这些是上限数字；平均的生产使用表现更低。

**最适合**：希望获得 GitHub 原生审计轨迹、并与现有 Actions 流水线直接集成的组织。

### AWS Bedrock AgentCore

一个面向生产 agent 的托管运行时：agent 定义的版本管理、用于跨 session 状态持久化的 Memory、原生可观测性（兼容 OTel），以及在 1-2% 的线上流量上进行的持续评测。这一在流量上做评测的特性能够捕获静默退化：一次模型升级在不触发任何显式告警的情况下让质量回退。

**最适合**：已深度投入 AWS 生态、需要托管的状态持久化、并希望在不自建评测基础设施的前提下进行持续质量监控的组织。

### GitLab Duo

Fix CI/CD Pipeline 在 GitLab 18.8 中正式可用（General Availability）。当一条流水线失败时，Duo 会读取至多 150 KiB 的日志，诊断根因，并以一个 Merge Request 的形式提出修复方案。CI Expert Agent 自 18.11 起处于 beta 阶段，用于更广泛的流水线辅助。

**关键约束**：150 KiB 的日志上限。输出冗长、超过这一阈值的流水线会得到被截断的上下文，从而降低诊断质量。在把所有失败都路由到这条路径之前，值得了解这一点。

**最适合**：以 GitLab 为中心、希望获得 agent 辅助的 CI 诊断、又不想引入一个独立平台的组织。

---

## 5. 数字孪生测试

agent 无法在首次运行时就安全地在生产中接受测试。测试非 AI 软件的标准做法是使用 staging 环境。对于调用外部服务（Slack、Jira、Okta、Google Drive）的 agent 而言，staging 要么意味着烧掉真实的 API 配额，要么意味着使用行为型 mock——其对服务的模拟足够准确，足以暴露集成 bug。

**行为型 mock 的区别**：静态 mock 返回一个固定响应。行为型 mock 则维护一份内部状态，该状态会随交互序列在逻辑上演进，并复刻限流、延迟的状态传播以及条件依赖。一个在收到 429 响应后重试的 agent，面对一个准确复刻了 Slack 限流窗口的 mock，与面对一个对任何请求都只返回 200 的 mock，其表现会截然不同。

### 各服务当前的覆盖情况

| 服务 | 现有最佳 mock | 覆盖范围 |
|---------|---------------------|---------|
| Slack | Slack-Mock（github.com/Skellington-Closet/slack-mock） | 7 个交互通道：Web API、RTM、Events API、Slash Commands、Webhooks、Interactive Buttons、消息投递。含状态管理。最为完整。 |
| Google Drive | Mockoon 预配置样例 | REST API 面。行为状态有限。 |
| Okta | 社区模式、DevForum | 认证流程与身份生命周期。无官方 mock。需自行构建。 |
| Jira | Atlassian 推荐的 staging 环境 | 用于隔离的独立应用密钥。并非行为型 mock。 |
| 通用 HTTP | WireMock（有状态）、Beeceptor（AI 驱动、多协议） | 对特定服务没有行为状态，但可针对任意 HTTP 进行配置。 |

Materialize（"始终最新的数字孪生"）采取了一种不同的思路：与运营系统实时同步，并具备逻辑隔离。它更接近一个托管的 staging 环境，而非 mock。当 agent 需要真实的数据分布、而非看似合理但实属伪造的测试数据时，它很有用。

LangWatch Scenario SDK（[langwatch.ai/scenario](https://langwatch.ai/scenario)）是唯一一个无需真实运行服务、便能系统性地进行行为型 agent 测试的尝试：它针对一个会生成真实输入的 agent-user 模拟多轮对话，同时由一个 agent-judge 评估被测系统 agent 是否达成了其成功标准。

---

## 6. 可观测性技术栈

经独立组织验证、可在生产环境中运行的开源基线方案：

```
OpenLLMetry (Traceloop)       ← instrumentation layer (Python + TypeScript)
      +
OpenInference (Arize)         ← semantic schema for LLM/agent attributes
      ↓
Langfuse or Arize Phoenix      ← tracing backend + eval storage
      +
DeepEval or LangWatch Scenario ← quality evaluation
```

对于有治理要求的企业，可在身份层加入 Strata Maverics 或 Entra Agent ID。

### OTel GenAI 约定（2026 年 5 月状态）

| Span 类型 | 状态 | 关键属性 |
|-----------|--------|---------------|
| `gen_ai.client` | 稳定 | `gen_ai.request.model`、`gen_ai.usage.input_tokens`、`gen_ai.usage.output_tokens` |
| `gen_ai.agent` | 实验性 | `gen_ai.agent.name`、`gen_ai.agent.id` —— 可能变更 |
| Events | 稳定 | 以结构化事件形式记录的 prompt/completion 内容 |
| Metrics | 稳定 | Token 计数器、延迟直方图 |

`gen_ai.agent` span 的实验性状态值得关注：在规范稳定之前，其属性可能被重命名或重构。如今在生产 harness 中使用 agent span，应当预期到规范稳定后会有一笔重新映射的成本。OpenInference (Arize) 和 OpenLLMetry (Traceloop) 通过在不断演进的 OTel 规范之上提供一个稳定的 schema 来应对这一问题。

### 应优先埋点的内容

1. **每一次 LLM 调用**：延迟、输入 token、输出 token、模型名称、结束原因（finish reason）。
2. **每一次 tool 调用**：tool 名称、参数（敏感信息需脱敏）、执行成功/失败、延迟。
3. **会话级别**：每个会话的总 token、会话时长、任务完成情况（二元）。
4. **评估得分**：任务完成率、tool 正确率（使用正确的 tool 数 / 使用的 tool 总数）。

Datadog、Honeycomb、New Relic 和 MLflow 均支持 OTel GenAI 约定。Arize Phoenix 在 DoorDash、Instacart、Reddit、Uber 和 Booking.com 等公司每月处理 1 万亿条 span，是该领域开源选项中生产规模记录最完备的方案。

### LLM-as-judge 的局限性

JudgeBiasBench（arXiv 2604.23178，Hongli Zhou 等人，2026 年 4 月）测得前沿模型在高级偏见检测测试中的错误率超过 50%。风格偏见是主导模式：得分为 0.76-0.92，而位置偏见低于 0.04。其实际后果是：LLM judge 批准风格精致但内容错误的输出的频率，显著高于应有水平。识别无效输出的真负率通常低于 25%。

截至 2026 年 5 月，尚无任何商业平台（Arize、LangWatch、Openlayer、Langfuse）公开记录其评估器是如何中和风格偏见的。

可行的解决方案是：将 LLM-as-judge 用于无法以确定性方式评估的定性维度（语气、解释质量、上下文敏感度）；将基于代码的检查用于任何可机械评估的内容（tool 选择正确性、结构化输出的 schema 合规性、对已知样例的回归测试）。不要将 LLM-as-judge 单独用作生产流量的质量门禁。

---

## 7. 测试分布反模式

一项覆盖 39 个开源 agent 框架和 439 个 agentic 应用的实证研究（arXiv 2509.19185）发现，agentic 系统中超过 70% 的测试投入针对确定性组件（tool、API、工作流逻辑），而针对 Plan Body（即 LLM 推理核心）的投入不足 5%。尽管 DeepEval 等专用 LLM 评估工具营销曝光度很高，其采用率却低于 1%。

这在结构上是本末倒置的。确定性组件最适合用标准单元测试来验证，一旦损坏就会高调地报错。而 LLM 推理核心才是那些不显眼、非确定性故障的所在：它们会产生看似合理实则错误的输出、在 tool 选择上漏掉边界情况，或者凭空捏造能力声明。

**推荐的再平衡方案**：至少将 20-30% 的测试投入分配给 Plan Body。pass^k 模式可应对非确定性：将一项关键测试运行 3-5 次，并要求它在 k 次运行中通过 k 次。Promptfoo 的 `--repeat` 标志实现了这一点。LangWatch Scenario SDK 则在多轮模拟层面做到了这一点。

对于确定性组件：标准单元测试、schema 校验、显式的 tool 调用检查。对于 LLM 推理：行为模拟（LangWatch Scenario）、带偏见意识的 LLM-as-judge、基于生产中已知优良样例的回归套件。

---

## 8. Creator-Verifier 模式

有一种结构性模式能持续提升输出正确率：由一个 agent（或 agent 步骤）负责生成，由另一个独立的 agent 负责验证，两者之间不共享任何上下文。

数据如下：

- Microsoft Agent Framework、AutoGen Studio 和 Google ADK 均已将其采纳为标准模式。
- Playwright Test Agents 以三 agent 架构实现该模式：planner 设计测试策略，generator 编写测试代码，healer 修复失败。
- 在已记录的各类实现中，独立验证相比自我验证可将正确率提升 +12 至 +26%。
- Factory.ai Missions：对抗性验证器在一个 Slack 克隆项目中捕获了 81 个问题，由此产生的修复特性占了实现工作量的 34%。
- OpenAI Codex 的自动审查系统将所需的人工批准量相比人工审查减少了 200 倍。

自我验证之所以失败，根本原因在于：生成输出的模型与审查它的模型携带着相同的偏见和上下文。由一个全新的模型实例进行验证——上下文中只有产物本身和成功标准——这在结构上与自我审查截然不同。

实践实现方式：派生第二个 agent，向其提供输出产物和原始需求。逐项询问输出是否满足每一条需求。不要问"这个好不好？"，而要针对每一条问"这是否满足需求 X？"，并对每条给出明确的通过/不通过判定。

这并不能消除幻觉；它捕获的是与既定需求不一致的那部分幻觉。要捕获那些内部自洽但事实错误的幻觉，你需要领域特定的测试用例。

---

## 9. 参考架构

```
User instruction
      ↓
┌─────────────────────────────────────────────────────────────────┐
│                       HARNESS                                    │
│                                                                  │
│  ┌─────────────┐      ┌──────────────┐      ┌───────────────┐   │
│  │   Context   │      │  While-Loop  │      │  Permission   │   │
│  │  Management │◄────►│    Engine    │◄────►│  Enforcement  │   │
│  └─────────────┘      └──────┬───────┘      └───────────────┘   │
│                              │                                    │
│  ┌─────────────┐      ┌──────▼───────┐      ┌───────────────┐   │
│  │   Session   │      │   Dynamic    │      │   Lifecycle   │   │
│  │ Persistence │◄────►│   Prompt     │◄────►│    Hooks      │   │
│  └─────────────┘      │  Assembly   │      └───────────────┘   │
│                        └──────┬───────┘                          │
│  ┌─────────────┐             │              ┌───────────────┐   │
│  │    Tool     │      ┌──────▼───────┐      │  Sub-Agent    │   │
│  │  Registry   │◄────►│  LLM Call    │◄────►│  Management   │   │
│  └─────────────┘      └──────────────┘      └───────────────┘   │
│                                                                  │
│  ┌─────────────┐                                                  │
│  │  Built-in   │                                                  │
│  │   Skills    │                                                  │
│  └─────────────┘                                                  │
└─────────────────────────────────────────────────────────────────┘
      ↓
┌──────────────┐      ┌──────────────┐      ┌──────────────────┐
│   Sandbox    │      │   Identity   │      │  Observability   │
│  (E2B/k8s/  │      │  Gateway     │      │  (OTel + eval)   │
│  Northflank) │      │(Strata/Entra)│      │                  │
└──────────────┘      └──────────────┘      └──────────────────┘
```

---

## 另请参阅

- [上下文工程](./context-engineering.md) —— ACE 流水线、信号分类法、漂移管理
- [安全加固](../security/security-hardening.md) —— 生产安全、注入防御
- [DevOps & SRE](../ops/devops-sre.md) —— CI/CD 集成模式
- [AI 角色](../roles/ai-roles.md) —— Harness Engineer、Agent Identity Architect、AI Eval Engineer
- [Spec-First 开发](../workflows/spec-first.md) —— 将 spec 作为 harness 的输入

---

*最后更新：2026 年 5 月。arXiv 2605.18747（Code as Agent Harness）是关于这三大属性的主要学术来源。Martin Fowler 的 Harness Engineering 文章是主要的从业者参考资料。两者均发表于 2025-2026 年。*
