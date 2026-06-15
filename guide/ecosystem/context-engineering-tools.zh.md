---
title: "Context Engineering: Tools & Ecosystem"
description: "A practical map of the tools that compress, optimize, route, and observe LLM context — from CLI output filters to AI gateways to LLMOps platforms"
tags: [context, tokens, optimization, ecosystem, tools, advanced]
---

# Context Engineering：工具与生态

> **可信度**：Tier 1/2 — 核心概念基于已发表的研究和生产环境数据。第三方工具细节基于公开文档（2026 年 3 月）。
>
> **相关**：[Context Engineering（配置指南）](../core/context-engineering.md) | [第三方工具](./third-party-tools.md) | [MCP 服务器生态](./mcp-servers-ecosystem.md)

本页面梳理了帮助你管理"什么进入上下文窗口、什么不进入"的工具生态。它是对[聚焦配置的 context engineering 指南](../core/context-engineering.md)的补充——后者涵盖 CLAUDE.md 结构和路径作用域。这里的重点是更广阔的工具版图：输出压缩、prompt 压缩、AI gateway、RAG 优化、可观测性以及推理基础设施。

---

## 目录

1. [心智模型](#1-the-mental-model)
2. [核心概念](#2-core-concepts)
3. [输出压缩：CLI 与工具输出](#3-output-compression-cli--tool-output)（RTK、Headroom、context-mode、stacklit）
4. [Prompt 压缩](#4-prompt-compression)
5. [AI Gateway](#5-ai-gateways)
6. [RAG 优化](#6-rag-optimization)
7. [记忆系统](#7-memory-systems)
8. [KV Cache 基础设施](#8-kv-cache-infrastructure)
9. [LLMOps 与可观测性](#9-llmops--observability)
10. [按使用场景选择工具](#10-tool-selection-by-use-case)
11. [研究全景](#11-research-landscape)

---

## 1. The Mental Model

让其他一切都豁然开朗的框架是：**上下文窗口是 RAM，不是磁盘**。

RAM 快速、昂贵且有限。你不会在运行程序前把拥有的一切都加载进 RAM。你只加载程序需要的部分，并且恰好在它需要的时候加载。LLM 上下文同理：你放进去的每个 token 都会挤掉别的东西、花费金钱，并争夺模型的注意力。

这重新定义了工程挑战。问题不是"我如何给模型更多信息？"，而是"模型成功完成任务所需的最小可行信息集是什么？"本页面中的每项技术都是对第二个问题的回答。

与系统架构的类比还可以更进一步。没有良好内存管理的 CPU 会停滞。没有良好上下文管理的 LLM 会产生幻觉、丧失连贯性，并漂移向泛泛的输出。优化上下文不是一项削减成本的工作——它是一项可靠性投资。

---

## 2. Core Concepts

### Minimum Viable Context (MVC)

MVC 是这样一条原则：恰好提供任务所需的信息，不多不少。它有两种看似相反、实则源于同一原因的失败模式：

- **欠上下文（Under-context）**：模型缺少必要信息，产生幻觉或输出泛泛之言
- **过上下文（Over-context）**：模型被无关信息淹没，注意力分散，遵循度下降

关于遵循度下降的研究（见 [context engineering 指南第 2 节](../core/context-engineering.md#2-the-context-budget)）量化了过上下文失败：一份超过 400 行的 CLAUDE.md 通常会把遵循度降到约 60%。原因是注意力分散——太多可能相关的信号争夺模型有限的注意力预算。

MVC 不是为了极简而极简。它关乎精确。一份恰好覆盖模型所需内容的 300-token 系统提示，胜过一份把关键指令埋在第五页的 3,000-token 提示。

### Context Rot

Context rot 描述的是：随着会话中上下文长度增长，模型行为发生的退化。研究最多的一种形式是"lost-in-the-middle"（中段迷失）现象：模型始终会低估置于长上下文中段的信息，主要关注开头和结尾。

实践中的经验性后果：

- CLAUDE.md 文件顶部附近的指令比底部的指令被更一致地遵循
- 在长时间的 agentic 会话中，随着新内容把早期约束推向中段，这些约束逐渐失去显著性
- 会话开始时的工具输出在几轮交互后往往实际上被"遗忘"

缓解措施：在上下文用量达到 70%（而非 90%）时执行 `/compact`、结构化的笔记记录 hooks，以及为根本上全新的任务上下文重启会话。`/compact` 命令会汇总对话历史，把陈旧内容移出活跃注意力窗口，同时保持连续性。

### Semantic Priming Hypothesis

来自压缩研究、具有实际意义的一项观察：当你对上下文进行超级压缩（移除大部分 token）时，模型并不会逐字回忆被移除的信息。相反，压缩后的上下文起到*语义启动（semantic prime）*的作用——它激活了模型训练时权重中已存在的相关潜在知识。

这一点之所以重要，是因为它意味着高度压缩的上下文可以表现得比其信息密度所暗示的更好。模型不是从上下文中重建事实；它是被指引向自己已经拥有的相关知识。对于训练充分的领域，10 个 token 的提示可能比 100 个 token 的逐字摘录激活更多相关知识。

实际含义是：当上下文紧张时，优先使用关键词和结构性线索而非散文。"Use OpenAPI 3.1, strict mode, no nullable" 比用两段文字解释同样的内容能检索出更精确的行为。

### Context Rot vs. Token Cost：两股压力

上下文管理在两股同时存在、方向相反的压力下运作：

| 压力 | 成因 | 效果 | 缓解措施 |
|----------|-------|--------|------------|
| **Context Rot** | 内容过多 | 注意力分散、中段迷失 | 修剪、compact、限定作用域 |
| **Token Cost** | 每个 token 都计费 | 预算超支、延迟增加 | 压缩、过滤、缓存 |

压缩解决成本问题。修剪解决 rot 问题。良好的 context engineering 两者兼顾。

---

## 3. Output Compression: CLI & Tool Output

工具输出、shell 命令结果、测试日志和数据库查询响应有一个共同的结构性问题：它们包含 70–95% 的样板内容。一个通过的测试套件会为你真正关心的那一个失败记录数百行成功信息。一条 `git log` 在你只需要三个字段时却倾倒出每次提交的元数据。除非被拦截，这些噪音会原封不动地进入上下文窗口。

### RTK (Rust Token Killer)

RTK 是一个 CLI 代理，在命令输出到达 Claude 上下文之前拦截它，应用专门构建的过滤器以凸显信号、丢弃噪音。它通过 Claude Code hook 集成，因此标准命令会被透明地重写。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [github.com/rtk-ai/rtk](https://github.com/rtk-ai/rtk) |
| **安装** | `brew install rtk-ai/tap/rtk` 或 `cargo install rtk` |
| **Stars** | 446（2026 年 3 月） |
| **集成** | 通过 `rtk init --global` 的 Claude Code hook |

跨命令类别的实测节省：

| 命令 | 缩减幅度 |
|---------|-----------|
| `rtk git log` | 92% |
| `rtk git status` | 76% |
| `rtk vitest run` | 99%+ |
| `rtk cargo test` | 平均 89% |
| `rtk pnpm outdated` | 70–85% |

其设计理念是：抑制成功的输出，凸显失败。一个通过 300 个测试、失败 2 个的测试套件应该显示 2 行，而非 302 行。这与开发者阅读输出的方式一致——上下文应当匹配这种认知模型。

RTK 支持通过 TOML DSL（`.rtk/filters.toml`）自定义过滤器，无需编写 Rust 即可应对项目特定的输出模式。完整功能参考见 [第三方工具：RTK](./third-party-tools.md#rtk-rust-token-killer)。

### Headroom

Headroom 针对的是另一个问题：工具返回的结构化数据（JSON 负载、数据库结果、API 响应），它们体积庞大但又不能整个丢弃。

与 RTK 的关键区别在于：Headroom 是**无损的**。它不是丢弃内容，而是用压缩后的摘要替换冗长数据，并将原始数据连同一个检索句柄一起注册。如果模型判断需要完整数据，它可以调用一个工具去获取。这在不需要预先加载一切的前提下，保留了 agent 按需访问细节的能力。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [headroom.ai](https://headroom.ai) |
| **压缩** | 对结构化工具输出压缩 70–95% |
| **架构** | 无损——原始数据可通过检索句柄访问 |
| **压缩模型** | SmartCrusher（快速）、Kompress（高保真） |

何时选择 Headroom 而非 RTK：

- 工具输出包含模型可能只需部分使用的结构化数据（数据库结果、API 响应）
- 你无法预测模型会需要输出的哪些部分
- 无损检索是硬性要求（合规、调试、审计追踪）

何时 RTK 已足够：

- 输出是非结构化的命令行文本
- 成功运行产生的是你确定不需要的噪音
- 更看重简单性和零基础设施

### context-mode

context-mode 是一个 MCP 服务器，运行在工具与上下文的边界处，在工具调用输出到达对话窗口之前拦截它们，并应用压缩或选择性检索。它还使用带 FTS5 全文搜索的 SQLite 实现了一个会话跟踪层，使得在 `/compact` 丢弃原始历史之后仍能对更早的会话内容进行语义检索。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: mksglu/context-mode](https://github.com/mksglu/context-mode) |
| **Stars** | ~14,149（2026 年 5 月） |
| **许可证** | ELv2（计划推出商业 SaaS） |
| **平台** | Claude Code 插件、Gemini CLI、Copilot、Cursor、Kiro、Zed，以及其他 6 个（共 12 个） |
| **宣称** | 98% 的 MCP 输出压缩，65–75% 的响应压缩 |

**MCP 输出沙箱的工作原理**：context-mode 不会把原始工具调用输出直接路由进对话，而是拦截结果、应用压缩，并注入一个带检索句柄的摘要。如果模型请求，完整输出可按需访问，这在精神上类似于 Headroom 的无损架构，但专门作用于 MCP 工具边界。

**`/compact` 后的会话记忆**：context-mode 使用 SQLite + FTS5 为会话历史建立索引。当 `/compact` 运行并丢弃原始对话历史时，SQLite 索引会持续保留。后续的检索查询使用 BM25 排序来凸显相关的早期上下文，而无需重新加载完整记录。

**"Think in Code" 模式**：context-mode v1.0.64 记录了这样一种模式：模型不是为回答一个探索性问题而读取文件，而是编写并执行一个进行查询或计数的脚本，然后只读取结果。这一点作为一项命名技术在 [context engineering 指南](../core/context-engineering.md) 中有深入介绍。

**何时选择 context-mode**：如果你在 Claude Code 之外还同时运行其他平台（Cursor、Gemini CLI），并希望有一个能跨所有平台工作的统一上下文管理层。当 MCP 工具输出庞大且结构化，且你需要超出 `/compact` 本身所提供的 compact 后会话检索时，它也很有用。

**与 RTK 和 Headroom 的对比**：RTK 作用于 shell 命令层（CLI 输出），Headroom 作用于结构化数据/API 响应层。context-mode 专门作用于 MCP 工具边界，并增加了会话持久化。这些工具是互补的。

### stacklit

stacklit 生成一个机器可读的索引，描述某个仓库的包结构、导出的符号和依赖。agent 在单次调用中读取这个索引（约 250 token），而无需花费 50,000+ token 去探索文件来理解代码库结构。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [GitHub: glincker/stacklit](https://github.com/glincker/stacklit) |
| **安装** | `npm install -g stacklit` |
| **集成** | 通过 `stacklit setup` 自动配置 Claude Code、Cursor 和 Aider |
| **宣称缩减** | 把 50,000+ token 的探索压缩到约 250 token |

**工作原理**：`stacklit generate-json` 扫描仓库并写出 `stacklit.json`——一份结构化的映射，包含包、带类型签名的导出、依赖图、git 活动热力图和框架提示。`stacklit setup` 会自动把一份紧凑的代码库地图注入 agent 配置文件。`stacklit diff` 检测在文件增删后索引何时过期。

```bash
# One-time setup per repository
stacklit generate-json    # create the index
stacklit setup            # inject into Claude Code / Cursor / Aider config

# Maintenance
stacklit diff             # check if index is stale
stacklit generate-json    # re-index after structure changes
```

**Worktree 兼容性**：生成的是按仓库划分的索引，没有集中式状态。与 grepai（需要本地嵌入索引）或 Serena（连接到语言服务器）不同，stacklit 产生的是一个静态 JSON 文件，无需额外设置即可在 git worktree 和临时 CI 环境中工作。

**与 RTK 和 context-mode 的对比**：RTK 在会话期间拦截 CLI 输出。context-mode 实时拦截 MCP 工具输出。stacklit 则在会话开始前就消除探索阶段的 token 花费——通过让仓库结构从第一条消息起就为人所知。这三个工具针对会话生命周期中的不同时刻，彼此互补。

---

## 4. Prompt Compression

Prompt 压缩作用于模型输入层：在 prompt 被发送给 LLM 之前减少其本身的 token 数量。这与输出压缩（拦截工具响应）和上下文修剪（管理会话历史）不同。

### LLMLingua / LLMLingua-2

LLMLingua（Microsoft Research）是研究最多的 prompt 压缩框架。它使用一个小型语言模型来评估 prompt 中每个 token 的"重要性"，然后移除最不重要的 token，直至达到目标压缩比。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [github.com/microsoft/LLMLingua](https://github.com/microsoft/LLMLingua) |
| **最大压缩** | 20x |
| **性能损失** | 在 GSM8K 和 BBH 基准上约 1.5% |
| **方法（v1）** | 通过小型 LM 进行基于困惑度的 token 打分 |
| **方法（v2）** | 从 GPT-4 进行数据蒸馏，token 分类 |

LLMLingua-2 在原版基础上改进，将压缩视为分类问题（保留 vs. 丢弃）而非排序问题。该分类器通过从 GPT-4 标注进行蒸馏训练而成，使其更快、跨领域泛化能力更强。

Semantic Priming Hypothesis（见第 2 节）解释了为何 20x 压缩仍能保留 98.5% 的任务性能：模型并非逐字回忆压缩后的文本。它把压缩后的 token 当作通向自身预训练知识的语义锚点。高频 token（功能词、连接词）往往被丢弃；领域关键词和结构性标记则被保留。

**何时使用**：长系统提示、重复的 RAG 上下文、示例冗长的 few-shot 例子。不适用于代码（语法承载语义）或数值数据（每一位数字都重要）。

### AttnComp（研究方向）

AttnComp（截至 2026 年 3 月尚未成为可交付产品）提出用交叉注意力模式取代困惑度打分作为压缩指标。其论点是：困惑度衡量的是给定前文后某个 token 有多"令人意外"——这对语言建模有用，但与任务相关性只有松散的相关。交叉注意力模式直接显示模型针对某个输出关注了哪些 token，使其成为一个更有原则的重要性指标。

已发表的结果显示，在相同压缩比下 AttnComp 优于 LLMLingua。关注其 OSS 发布。

---

## 5. AI 网关

AI 网关位于你的应用程序与 LLM 提供商之间。它们负责路由、速率限制、成本管理，并且越来越多地承担主动的上下文转换工作。网关这一类别正是基础设施与上下文工程相互重叠的地方。

### Edgee

Edgee 将自身定位为面向 AI 应用的"可组合边缘层"。它的上下文工程功能在 HTTP 层透明运作：应用发出一个标准的 API 调用，Edgee 拦截它，应用压缩和路由策略，然后将优化后的请求转发给模型。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [edgee.cloud](https://www.edgee.cloud) |
| **上下文压缩** | 高达 50% 的主动压缩 |
| **部署** | 边缘（靠近用户，低延迟） |
| **功能** | 路由、护栏、压缩、成本策略 |

"边缘"定位是有意为之的：通过在靠近用户而非集中式服务器的位置运行，Edgee 在仍能拦截完整请求/响应周期的同时，降低了往返延迟。这在 token 压缩和延迟同时构成约束的交互式应用中尤为重要。

护栏在网关层应用，这意味着无论由哪个应用或客户端发起请求，护栏都会被强制执行。在多租户环境中，这将"哪些上下文会到达模型"这一关注点与生成上下文的应用代码分离开来。

### Portkey

Portkey 是 AI 网关类别中更为成熟的玩家，其功能集更为广泛，核心是跨多个 LLM 提供商的统一路由。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [portkey.ai](https://portkey.ai) |
| **模型支持** | 通过统一 API 支持 250+ 个 LLM |
| **功能** | 路由、回退、负载均衡、缓存、护栏 |
| **可观测性** | 内置追踪和成本跟踪 |

Portkey 的语义缓存层对上下文优化尤其有意义：相同或近乎相同的请求会被缓存并返回，而无需调用 LLM。在具有重复查询模式的应用中（帮助台、代码评审机器人、内部搜索），缓存命中率可将 LLM 总调用量减少 30–60%。

**网关与输出压缩的对比**：这两类相互补充。RTK/Headroom 压缩从工具输出进入上下文的内容。网关则在组装好的提示到达模型之前对其进行压缩或路由。两者都能降低 token 总开销，但它们在流水线的不同环节进行拦截。

---

## 6. RAG 优化

检索增强生成（RAG）有一个有据可查的失败模式：检索步骤返回的分块在孤立来看时语义相关，但缺乏使其有用所需的上下文。一个提到"第三季度营收增长 3%"的片段，如果没有公司名称和年份就毫无意义——而这两者很可能就在同一份文档里，只是处于不同的分块中。

### Anthropic 上下文检索（Contextual Retrieval）

Anthropic 的上下文检索方法通过在索引之前对每个片段进行预上下文化，来解决分块孤立的问题。每个分块前会被加上一段由 LLM 生成的简短前言，将其置于它所来自的文档语境之中。

```
Before: "Revenue grew 3% in Q3."

After: "From Acme Corp Q3 2024 earnings report: Revenue grew 3% in Q3."
```

前言在索引时按每个分块生成一次，而非在检索时生成。借助 prompt caching，为大型文档语料库生成前言的成本可降低约 90%（文档被缓存，只有每个分块的指令部分会变化）。

来自 Anthropic 评估的公开结果：

| 方法 | 失败率降低 |
|--------|----------------------|
| 仅上下文嵌入（Contextual embeddings） | 35% |
| 上下文 BM25（关键词 + 语义） | 49% |
| 上下文嵌入 + BM25 + 重排序 | 67% |

将语义搜索（嵌入）、关键词搜索（BM25）以及按与实际查询的相关性对结果重新排序的重排序步骤相结合，能产生最佳效果。重排序提供商包括 Cohere 和 Voyage AI。

规模化成本：为 100 万文档 token 生成上下文前言，在 prompt caching 之后约花费 1.02 美元。对于大多数生产语料库而言，这是一次性的索引成本。

### JIT / 智能体检索（Agentic Search）

传统 RAG 在请求开始时就加载检索结果。JIT（即时，Just-in-Time）检索则推迟这一步：智能体以最小上下文起步，随着任务揭示出它实际需要什么，再按需检索信息。

这对于信息需求难以预测的智能体工作流很重要。一个代码调试智能体可能在处理 Python 错误时需要一组文档，而在两步之后遇到数据库错误时却需要完全不同的另一组文档。一开始就把两者都加载进来会浪费上下文；两者都不加载又会迫使模型产生幻觉。JIT 检索恰好穿针引线、把握住了这个平衡。

用 Claude Code 的术语来说：这正是智能体在使用工具（`list_directory`、`read_file`、`grep`）而非接收一份预先组装好的上下文时自然而然所做的事。"需要时再搜索"这一模式是一项设计原则，而不仅仅是 Claude 的一项能力。

### RAG 三元组评估（RAG Triad Evaluation）

RAG 三元组是一个从三个维度评估 RAG 输出质量的框架：

| 维度 | 问题 | 它能捕捉什么 |
|-----------|----------|----------------|
| **上下文相关性** | 检索到的上下文与问题相关吗？ | 检索失败 |
| **答案相关性** | 答案与问题相关吗？ | 生成漂移 |
| **有据性（Groundedness）** | 答案是否得到检索上下文的支撑？ | 幻觉 |

这三者可能各自独立地失败。一个系统可以检索到完全相关的上下文却仍然产生幻觉（有据性失败）。它也可以生成一个相关却不被检索内容所支撑的答案。同时评估这三者，能识别出 RAG 流水线中哪一部分是薄弱环节。

Arize Phoenix 将 RAG 三元组实现为一个生产级评估框架（见第 9 节）。

---

## 7. 记忆系统（Memory Systems）

长期运行的智能体面临上下文腐烂（context rot）问题的一种变体：会话历史不断增长，直到超出上下文窗口，或直到早期上下文实际上被忽略。记忆系统通过将信息从上下文窗口移出、转入持久化存储，并按需检索来解决这一问题。

### 短期：compact 与结构化笔记

具体到 Claude Code，有两种机制处理会话级别的记忆：

**`/compact`** 会对对话历史进行摘要，用一份高密度的摘要替换原始往来内容。模型保留了连续性，但 token 计数大幅重置。应在上下文使用率达到 70% 时使用，而非 90%。

**通过 hooks 实现的结构化笔记** 是其智能体版本：一个 PostToolUse hook 将关键决策、已发现的事实和任务状态写入一个笔记文件。智能体在下一次会话开始时加载该文件。这彻底绕开了多会话工作中的上下文腐烂问题——笔记文件位于上下文的起始处（注意力最高），且只包含经过精心整理的信息。

**Auto Memory（v2.1.59+）** 和 **Auto Dream** 提供了原生的 CC 替代方案：Claude 在两次会话之间写入它自己的 `MEMORY.md`，并由一个后台 sub-agent 在累计 ≥5 次会话且 ≥24 小时后对其进行整合。见 [记忆系统：Auto Memory](../core/memory-systems.md#22-auto-memory-v21594)。

### 长期：外部记忆系统

对于多会话和多智能体工作流，持久化记忆系统将信息存储在上下文窗口之外，并有选择地检索。CC 生态拥有一个三层模型：

**个人（无团队）**：claude-mem（26.5K stars，基于 hooks 的自动捕获）、agentmemory（16K stars，BM25 + 向量 + 图融合，95.2% R@5）、ICM（Rust 二进制文件，双衰减 + 图架构，`brew install icm`）。

**团队共享**：将 CLAUDE.md + `.mcp.json` + skills 提交到仓库（即"三位一体"，零基础设施）。用于团队共享记忆池的 Mem0 Cloud MCP。用于时序知识图谱的 Zep/Graphiti。

**RAG 与 Memory 的区别**：RAG 是模型对外部世界知识（文档、代码库、网络）的访问。Memory 是它对用户特定和会话特定知识（偏好、过往决策、连续性）的访问。两者都是检索系统，服务于信息架构的不同部分。设计良好的智能体两者兼用。

> **权威参考**：[记忆系统指南](../core/memory-systems.md)——20 个工具的对比表、架构模式、风险矩阵、决策流程图和基准测试。

---

## 8. KV Cache 基础设施

本节分为两部分。第一部分介绍 Anthropic 的 prompt caching 机制及其在 Claude Code 中的应用，包括 Claude Code 如何构造请求以最大化命中率。第二部分介绍面向自行部署 LLM 的团队的自托管推理基础设施。

### 什么是 KV Cache？

在预填充阶段（处理输入时），transformer 会为上下文中的每个 token 计算键值对（Key-Value pairs）。这些对存储在 GPU VRAM 中，而非以原始文本或 token 哈希的形式存储。对于 Opus 上一个 100K-token 的前缀，KV 数据大约占据 500MB–1GB 的 VRAM。

对于后续共享同一前缀的请求（例如相同的系统提示），这些已存储的 KV 值可以被复用而无需重新计算。这就是 KV cache 复用。transformer 的自回归特性施加了一个严格约束：只有前缀可以被缓存。如果第 N 个 token 发生变化，那么从第 N+1 个 token 起的 KV 条目都必须重新计算。前缀中任何位置的修改都会使其下游的一切失效。

如果没有 KV cache 复用，每个请求都要从头处理完整上下文。借助有效的缓存，只有每个请求中独特的部分（用户消息、新的工具结果）需要重新计算。Anthropic 的 prompt caching 同时降低延迟和成本：Opus 上缓存的 token 计费约为 $0.50/M，而未缓存的输入 token 为 $5/M。缓存命中要求共享前缀足够长（通常 1,024+ token）且足够新（缓存在约 5 分钟无访问后过期）。

### Claude Code 如何使用 Prompt Caching

Claude Code 将每个请求都构造为最大化缓存命中率。请求顺序很重要，因为存在前缀约束：变化最频繁的项必须放在最后。

**请求结构（从最稳定到最不稳定）**：

1. **系统提示** —— 在同一版本下对所有 Claude Code 用户都是相同的。共享缓存：当 Anthropic 从共享 GPU 内存中提供系统提示时，同一版本下的所有用户都受益于相同的缓存 KV 条目。
2. **工具定义** —— 每个会话内是静态的。在会话开始时锁定。会话中途添加或移除工具会使整段对话缓存失效，这就是为什么 Claude Code 会在会话开始时锁定工具列表。
3. **项目配置 / CLAUDE.md** —— 作为消息内容注入（通过消息中的 `<system-reminder>` 块），而非放在系统提示里。
4. **对话历史** —— 滑动断点：只有新的回合需要重新计算。

**为什么 CLAUDE.md 不放在系统提示里**：如果将 CLAUDE.md 内容注入系统提示，每个用户的前缀都会变得独特（不同的项目、不同的配置），那么约 30K-token 系统提示的共享缓存收益就会消失。通过让所有用户的系统提示保持一致，并将 CLAUDE.md 作为消息内容注入，Anthropic 可以把系统提示的计算成本分摊到每一个并发的 Claude Code 会话上。CLAUDE.md 一旦出现在对话历史中仍会被缓存一次，但系统提示本身始终是全局共享的。

**生产环境命中率**：在真实的 Claude Code 会话中，prompt caching 达到约 96% 的命中率。原因很简单：系统提示、工具定义、CLAUDE.md 内容以及先前的对话回合全都命中缓存；只有新的用户回合和模型的响应才是新的计算。

### 缓存反模式

**系统提示中的时间戳**：系统提示前缀中任何频繁变化的值都会因使每个用户的前缀变得独特而破坏缓存。一位 Hacker News 用户报告，通过将一个时间戳字段从系统提示前缀移入消息中，恢复了超过 20 个百分点的缓存命中率。解决办法：将动态值（当前日期、git 分支、文件修改时间）移入消息内容，而非系统提示。

**会话中途添加或移除工具**：因为工具定义在请求前缀中位于系统提示与对话历史之间，对工具列表的任何更改都会使整段对话的缓存失效。Claude Code 通过在会话开始时锁定工具定义来避免这一点。

### Plan Mode：一种缓存稳定的设计模式

Plan Mode 在规划阶段限制写入访问。一种朴素的实现是在 Plan Mode 期间从工具列表中移除写入类工具。问题在于：从列表中移除工具会改变前缀，从而使整个会话缓存失效。

Claude Code 的实际实现是：不移除工具，而是新增两个工具（`EnterPlanMode` 和 `ExitPlanMode`）。完整的工具列表在模式切换时保持不变。模式行为通过消息中的指令来传达，而非通过更改工具定义。无论 Plan Mode 是开还是关，缓存前缀都保持一致。

这是一个更广泛设计原则的具体例子：优先采用指令级别的模式切换，而非对请求前缀做结构性更改。

### 为保持缓存连续性：compact 与 `/clear` 的对比

compact（`/compact`）会保留缓存。compact 请求复用相同的系统提示和工具定义前缀，因此会话早期的缓存 KV 条目在 compact 运行后仍然有效。只有对话历史部分被替换为摘要。

`/clear` 之后若超过约 5 分钟无活动，可能导致完全的冷启动。缓存条目的 TTL 在空闲期间过期，因此下一个请求找不到系统提示或工具定义的缓存 KV 条目。这是 Claude Code 在长会话中默认采用 compact 而非硬重置的原因之一：compact 在不触发缓存过期的情况下保留连续性。

### 自托管 KV Cache 基础设施

以下工具适用于自行部署 LLM 而非使用 Anthropic 托管 API 的团队。

### vLLM（PagedAttention）

vLLM 是自托管 LLM 领域占主导地位的开源推理引擎。它的关键创新是 PagedAttention：KV cache 内存以固定大小的页（类比于操作系统的虚拟内存页）而非连续块的方式分配。

传统的 KV cache 分配会因碎片化（为每个序列分配最坏情况下所需的空间）而浪费 60–80% 的 GPU 内存。PagedAttention 通过在请求间共享页并按需分配，将这种浪费降至 4% 以下。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [github.com/vllm-project/vllm](https://github.com/vllm-project/vllm) |
| **关键创新** | PagedAttention（非连续 KV cache） |
| **内存浪费** | 从 60–80% 降至 <4% |

### SGLang（RadixAttention）

SGLang 引入了 RadixAttention：KV cache 条目被组织为一棵以 token 序列为键的基数树（trie 结构）。当两个请求共享一个前缀时，它们共享前缀的 KV 条目会被自动复用。

这在以下场景中尤为强大：

- 多个请求共享同一系统提示（trie 只存储一次）
- 检索到的文档在众多查询间保持恒定的 RAG 流水线
- 一个基础上下文在各 subagent 间共享的多智能体系统

| 属性 | 详情 |
|-----------|---------|
| **来源** | [github.com/sgl-project/sglang](https://github.com/sgl-project/sglang) |
| **关键创新** | RadixAttention（基于 trie 的自动缓存复用） |
| **最适合** | 共享前缀的工作负载、多智能体系统 |

### 语义缓存

语义缓存运作在模型层之上：它不缓存 KV 激活值，而是缓存以请求语义相似度为键的完整 LLM 响应。一个在语义上与某个已缓存请求相近的新请求，会直接返回缓存的响应而无需调用 LLM。

带有向量搜索扩展的 Redis 是最常见的实现。在高重复度的工作负载中（FAQ 机器人、内部搜索、模式相似的代码评审流水线），可实现 30–60% 的语义缓存命中率，部分生产部署报告称成本降低了 73%。

风险在于：缓存的响应会变得陈旧。语义缓存需要与底层知识变化频率相匹配的 TTL 策略。

---

## 9. LLMOps 与可观测性

无法度量的东西就无法优化。LLMOps 工具类别提供了仪表化层：为 LLM 驱动的系统提供追踪、成本跟踪、质量评估和漂移检测。

### Langfuse

领先的开源选项。Langfuse 可以追踪跨复杂多步骤 agent 工作流的 LLM 调用，捕获每一步的输入/输出、延迟、每次调用的成本以及完整的执行树。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [github.com/langfuse/langfuse](https://github.com/langfuse/langfuse) |
| **许可证** | 开源（MIT） |
| **部署** | 自托管或云端 |
| **最适合** | 自托管需求、成本分析、追踪调试 |

面向上下文优化的关键特性：按会话的 token 成本细分、追踪对比（哪个 prompt 变体更便宜？），以及可以在已存储的追踪上运行的自定义评估指标，无需重新运行 agent。

### LangSmith

LangSmith 与 Anthropic 相邻（属于 LangChain 生态），如果你基于 LangChain 或 LangGraph 构建系统，它是标准选择。它擅长调试链式操作，在这些场景中理解执行图与理解单个 LLM 调用同样重要。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [smith.langchain.com](https://smith.langchain.com) |
| **最适合** | LangChain/LangGraph 工作负载、链式调试、A/B 测试 |
| **特性** | 数据集管理、自动化评估、回归测试 |

### Arize Phoenix

Phoenix 专注于 RAG 质量评估，原生实现了 RAG Triad。它在追踪检索操作的同时也追踪生成过程，因此你可以将检索质量与最终答案质量关联起来。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [github.com/Arize-ai/phoenix](https://github.com/Arize-ai/phoenix) |
| **许可证** | 开源 |
| **专长** | RAG 评估、LLM-as-judge 指标、嵌入漂移 |

特别有用之处在于：可以识别瓶颈究竟出在检索（上下文相关性失败）还是生成（接地性失败）。这一区分决定了你应该修复检索器还是修复 prompt。

### Maxim AI

Maxim AI 聚焦于持续评估：针对每一条生产追踪运行自动化评估，而不仅仅是离线测试集。它支持 LLM-as-a-judge 工作流（用一个 LLM 为另一个 LLM 的输出打分），并支持在生产流量上对 prompt 变体进行 A/B 测试。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [getmaxim.ai](https://www.getmaxim.ai) |
| **最适合** | 持续评估、生产环境 A/B 测试、回归检测 |

### TruLens

TruLens 以开源库的形式实现了 RAG Triad 评估框架。它可以直接嵌入到你的应用代码中，作为应用的一部分内联运行评估，而不是放在独立的可观测性平台上。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [github.com/truera/trulens](https://github.com/truera/trulens) |
| **许可证** | 开源 |
| **最适合** | 内联 RAG 评估、库集成、RAG Triad 评分 |

### 选择可观测性工具

| 需求 | 推荐 |
|------|------------|
| 全部自托管、成本分析 | Langfuse |
| LangChain 生态、链式调试 | LangSmith |
| 专门做 RAG 质量评估 | Arize Phoenix |
| 生产环境持续评估、A/B 测试 | Maxim AI |
| 在应用代码中嵌入 RAG Triad | TruLens |

这些工具并不互斥。用 Langfuse 做追踪，再加上 Phoenix 做 RAG 评估，是一种常见的组合。

---

## 10. 按使用场景选择工具

### 你是 Claude Code 用户（独立开发者）

| 问题 | 工具 |
|---------|------|
| 命令输出淹没上下文 | RTK |
| 监控 token 消耗 | ccusage（参见[第三方工具](./third-party-tools.md)） |
| 单次会话中上下文变得过长 | 在使用率达到 70% 时执行 `/compact` |
| 忘记过往会话的决策 | ICM 记忆系统 |
| Claude 忽略冗长 CLAUDE.md 中的规则 | 路径作用域（参见[上下文工程指南](../core/context-engineering.md)） |

### 你正在构建 AI 应用

| 问题 | 工具 |
|---------|------|
| 工具输出的 JSON 太冗长 | Headroom |
| prompt 太长，需要压缩 | LLMLingua |
| 在多个 LLM 提供商之间路由 | Portkey |
| 在边缘端进行压缩 + 防护栏 | Edgee |
| RAG 分块丢失上下文 | Anthropic Contextual Retrieval |
| 追踪 agent 执行 | Langfuse 或 LangSmith |
| 度量 RAG 质量 | Arize Phoenix |
| 持续评估 | Maxim AI |

### 你正在部署自托管 LLM

| 问题 | 工具 |
|---------|------|
| GPU 显存效率 | vLLM（PagedAttention） |
| 共享前缀缓存（多 agent、RAG） | SGLang（RadixAttention） |
| 在语义层面缓存重复查询 | 带向量搜索的 Redis |

---

## 11. 研究前沿

尚未作为生产工具落地的活跃研究领域（截至 2026 年 3 月）：

### SlimInfer（动态 Token 剪枝）

SlimInfer 识别 transformer 中间层中冗余的 token 表示，并在推理过程中将其剪除。已发表结果：在 LLaMA 3.1 上将首 token 时间（Time-to-First-Token）提速 2.53 倍，且无可测量的质量下降。其机制在于：许多 token 的中间层表示会收敛到几乎相同的值；剪除这些冗余表示可在不丢失信息的情况下节省计算量。

### TopV（视觉 Token 剪枝）

对于多模态模型（视觉-语言模型），图像 token 主导了上下文用量。一张 1024x1024 的图像可以生成数千个视觉 token，其中大多数编码的是无信息量的图块（背景、边缘）。TopV 将图块选择表述为一个优化问题（Sinkhorn 算法），仅保留与推理任务相关的视觉区域。已发表结果显示，在保持任务性能的同时显著降低了 VLM 推理的 TTFT。

### Token 缩减对幻觉的影响

一项贯穿多个研究方向的发现：生成式模型中的 token 缩减不仅能降低成本——它还能可测量地减少幻觉，并减少对简单查询的"过度思考"。其机制尚未被完全理解，但这种相关性在各项研究中是一致的。更简短、更精确的上下文会带来更有依据、更不啰嗦的输出。这强化了一个论点：MVC 是一项可靠性原则，而不仅仅是一项成本原则。

---

> **交叉引用**
>
> - [上下文工程（配置指南）](../core/context-engineering.md) —— CLAUDE.md 层级、路径作用域、预算管理
> - [第三方工具](./third-party-tools.md) —— RTK 完整参考、ccusage、ICM 及其他 CC 专用工具
> - [MCP 服务器生态](./mcp-servers-ecosystem.md) —— 作为动态上下文注入的 MCP
> - [可观测性](../ops/observability.md) —— 在生产环境中监控 Claude Code
> - [终极指南：记忆系统](.#memory-hierarchy) —— Claude Code 的完整记忆架构
