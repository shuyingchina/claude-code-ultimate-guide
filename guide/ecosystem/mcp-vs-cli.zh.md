---
title: "MCP vs CLI — 决策指南"
description: "在 Claude Code 工作流中何时使用 MCP 服务器 vs CLI 工具。权衡取舍、决策维度,以及按场景给出的指引。"
tags: [mcp, cli, tokens, architecture, decision]
---

# MCP vs CLI — 决策指南

**最后更新**:2026 年 5 月

> 包含指引表格和实践者引述的交互式版本:[cc.bruniaux.com/ecosystem/mcp-vs-cli/](https://cc.bruniaux.com/ecosystem/mcp-vs-cli/)

这场争论源于一连串快速更替的界面范式:基于浏览器的 AI(2022-23),随后是 IDE 中的 AI,通过 MCP 将 agent 连接到外部服务(2024-25),再后来是完整的 CLI agent,无需中间层即可执行命令并写入文件(2025-26)。这一演进过程解释了为什么这个问题会存在。

本页比较两种为 Claude Code 提供外部工具和服务访问能力的集成模式:MCP 服务器和 CLI 工具。两者没有谁普遍更优。正确的选择取决于你的具体场景——而大多数真实工作流最终会两者并用。

---

## 各方案的作用

**MCP 服务器** 在会话开始时将工具 schema 注入 Claude 的上下文。Claude 会看到一份结构化的可用工具列表,包含参数、类型和描述。然后它以原生方式调用这些工具,并接收结构化的响应。

**CLI 工具** 是 Claude 通过 Bash 调用的 shell 命令。Claude 驱动它们的方式与开发者完全一样:构造命令字符串、解析文本输出。启动时不注入 schema。shell 就是接口。

---

## 权衡取舍

### MCP 的优势

| 优势 | 详情 |
|-----------|--------|
| **结构化接口** | 工具 schema 精确地引导 Claude——更少出现臆造的 flag 或参数 |
| **复杂认证** | OAuth、token 刷新、密钥轮换由服务器处理,而非靠 prompt |
| **结构化输出** | JSON 响应可被 Claude 及下游 agent 直接解析 |
| **可观测性** | 远程 MCP 服务器可记录每一次调用——对企业级用量追踪和 ROI 归因至关重要 |
| **规模化分发** | 只需更新一次服务器,所有连接的客户端都获得变更。无需逐机做包管理。 |
| **非技术用户** | 从不接触终端的用户也可通过 MCP 连接器透明地访问工具 |
| **较弱的模型** | 当模型解析 CLI 帮助文本的能力较弱时,结构化 schema 可起到弥补作用 |

### CLI 的优势

| 优势 | 详情 |
|-----------|--------|
| **零上下文开销** | 启动时不注入 schema。自 v2.1.7 起,惰性加载已缩小了大部分差距,但 CLI 仍是绝对的最小开销选项。 |
| **确定性操作** | 显式命令配合可预测的输出,更易于审计和测试 |
| **人 + AI 通用** | 同一个 CLI 封装,开发者手动运行和 Claude 调用都能用 |
| **前沿模型** | Claude Opus/Sonnet 4.6 无需结构化 schema 即可驱动复杂 CLI(aws-cli、glab、gh) |
| **速度** | 无需建立连接,无需 MCP 握手——直接执行子进程 |
| **简单性** | 比远程服务器调用链更易于调试、记录和推理 |
| **Skills 封装** | 封装进 skill 的 CLI 对用户透明,并使工具逻辑保持在版本控制之下 |

### MCP 的弱点

| 弱点 | 详情 |
|----------|--------|
| **schema token 成本** | 自 v2.1.7 起,惰性加载(MCP Tool Search)意味着未使用的工具只注入其名称,而非完整 schema。成本仍非零:工具名称在启动时加载,完整 schema 在首次使用时加载。v2.1.7 之前的最坏情况(5 服务器配置约 55K tokens)如今平均约 8.7K——降低了 85%,但并非为零。 |
| **连接开销** | 连接大量 MCP 服务器会拉长会话启动时间 |
| **调试困难** | MCP 服务器内部的故障比失败的 shell 命令更难追踪 |
| **维护复杂性** | 运行、更新和保护远程 MCP 服务器会增加基础设施负担 |
| **对简单 API 是杀鸡用牛刀** | 一个只暴露 glab 20% 功能的 GitLab MCP,还不如 glab 本身 |

### CLI 的弱点

| 弱点 | 详情 |
|----------|--------|
| **无可观测性** | 本地机器上的 shell 命令对运维/管理工具链是不可见的 |
| **分发难题** | 让团队各成员的 CLI 保持更新需要包管理纪律(brew、scoop 等) |
| **较弱的模型吃力** | 能力较弱的模型可能臆造 flag 或误读帮助文本——schema 会有帮助 |
| **缺乏多 agent 结构** | CLI 输出需要解析;结构化的 MCP 响应在 agent 间交接时更可靠 |
| **非技术用户门槛** | 不能指望非技术用户拥有配置好的 CLI 环境 |

---

## API 封装模式

大多数面向 SaaS 工具的生产级 MCP 服务器都建立在既有的 REST 或 GraphQL API 之上。服务器将工具调用转换为针对这些 API 的 HTTP 请求,处理响应,并向 agent 返回结构化输出。它并不会增加底层 API 本身所不具备的后端能力。

来自四大主流提供商的官方文档直接证实了这一点:

- **Notion**:"将 MCP 工具调用转换为对 Notion 公共 API 的 HTTP API 调用"(Notion 工程博客)
- **Sentry**:"作为上游 Sentry API 的中间件,针对 Cursor 和 Claude Code 等编码助手做了优化"(sentry-mcp README)
- **Slack**:"对外部 API(如 Slack)的封装"(Slack 开发者文档)
- **GitHub**:"与 GitHub 集成,允许 LLM 通过 GitHub API 与仓库交互"(github-mcp-server README)

实际后果:一个调用相同 REST 或 GraphQL API 的 CLI 脚本具备相同的能力。MCP 和 CLI 触达同一后端,使用相同的凭证,触发相同的操作。区别在于接口层,而非后端能做什么。

MCP 能提供而 CLI 无法复制的部分:

- **OAuth token 管理**:服务器持有的认证,带浏览器重定向流程(Slack、Google Drive、Figma、托管版 Notion)。CLI 可以把 API key 放在环境变量里,但无法持有刷新 token 或完成 PKCE 交换,后者需要服务器端状态。
- **为 LLM 调优的 schema**:经过精选的工具集合,而非完整的 API 表面,其参数类型和描述都针对 agent 推理做了校准。
- **集中托管**:一次部署即可服务众多客户端;CLI 则需要逐机安装并逐用户配置凭证。
- **用量归因**:远程 MCP 服务器将每次工具调用与某个用户和会话关联起来,为可观测性仪表盘供数。开发者机器上的本地 CLI 调用则不可见。

这让决策标准更加清晰。如果某服务通过 API key 或环境 token 认证,那么调用相同 API 的 CLI 在功能上等同于 MCP 服务器。问题就归结为:你是否需要 OAuth、集中式可观测性,或跨客户端标准化。如果这些都不适用,CLI 既能避免 schema 开销,又能触达相同的后端。

---

## 四个决策维度

在问"MCP 还是 CLI?"之前,先回答以下四个问题。它们按约束力从强到弱排序。

### 1. 最终用户是谁?

这是最主导的变量。其他一切都次于它。

- **非技术用户**(使用聊天界面,无终端)→ **MCP 或 skill 封装的 CLI**。你无法向非开发者用户暴露裸 CLI。连接器必须基于 MCP,或被无形地封装进一个在内部处理 CLI 的 skill 中。
- **技术用户 / 开发者** → 继续看问题 2。

### 2. 由哪个模型驱动该工具?

- **前沿模型**(Claude Opus/Sonnet 4.6)→ 足够强,能直接驱动复杂 CLI。结构化的 MCP schema 带来的开销与收益不成比例。
- **更小或本地模型**(Qwen、Mistral、轻量部署)→ 结构化的 MCP schema 可弥补较弱的 CLI 解析能力。此处 MCP 更可靠。

### 3. 你的组织是否需要可观测性?

- **需要**(企业、面向高管的报告、合规、AI 支出的 ROI 归因)→ **MCP 远程服务器**。本地 CLI 调用不可见。远程 MCP 服务器可记录每次工具调用、将其关联到某个用户,并向仪表盘供数。这一点用本地机器上的 CLI 无法复制。
- **不需要**(个人开发者、本地工作流)→ 可观测性不是约束。CLI 即可。

### 4. 工具 schema 变化得多频繁?

- **稳定的 API**(成熟工具、带版本的接口)→ MCP 的投入会随时间回本。
- **快速变化** 或 **薄封装** → CLI 维护成本更低。一个只暴露你实际用到的 5 条命令的手写 glab 封装,比一个复制完整 API 表面的 GitLab MCP 更耐用。

---

## 按场景给出的指引

快速参考——不是规则,而是方向性的默认建议。

| 场景 | 倾向于 | 理由 |
|-----------|-------------|-----------|
| 非技术用户,聊天界面 | **MCP / Skill** | CLI 无法触达;连接器必须无形 |
| 前沿模型(Claude 4.x),开发者工作流 | **CLI** | 模型可原生处理;schema 是开销 |
| 更小/本地模型 | **MCP** | schema 可可靠地引导模型 |
| 企业级,需要可观测性 | **MCP Remote** | 记录、归因和报告用量的唯一途径 |
| 团队分发(10+ 开发者) | **MCP** | 集中更新 vs 逐机维护 CLI |
| 个人开发者,本地机器 | **CLI 或 skill** | 更简单、更快、无基础设施 |
| 确定性操作(git、CI、部署) | **CLI** | 显式命令、可预测输出、可审计 |
| 复杂认证(OAuth、token 刷新) | **MCP** | 服务器处理认证;CLI 则需自行铺设凭证管道 |
| 上下文预算紧张 / 加载了大量工具 | **CLI** | 仍是开销最小的选项。惰性加载(v2.1.7+)显著降低了 MCP 成本,但 CLI 的 schema 成本天然为零。 |
| agent 间结构化输出 | **MCP** | JSON 响应比解析后的 CLI 文本更可靠 |
| 调试 / 为新集成做原型 | **CLI** | 更易检查,迭代更快 |
| 浏览器自动化(非前沿模型) | **MCP** | Playwright MCP 可可靠地结构化交互 |
| 浏览器自动化(前沿模型,Claude Code) | **CLI + skill** | 实践中 playwright-cli + skill 被反馈更快、更高效 |
| GitLab / GitHub 访问 | **CLI**(glab、gh) | 官方 CLI 比大多数 MCP 封装更丰富 |
| 文档查询(Context7) | **MCP** | 没有 CLI 等价物;结构化文档检索无 shell 对应方案 |

---

## 逐服务器推荐

下表将四个决策维度应用于 18 个最常被讨论的 MCP 服务器。"裁定"针对的是在本地机器上使用前沿模型的开发者这一默认情形。你的具体场景(非技术用户、企业级可观测性,或更小的模型)可能会让任一行偏向 MCP。

| MCP 服务器 | 裁定 | CLI 替代方案 | 理由 |
|------------|---------|-----------------|--------|
| GitHub MCP | **用 CLI** | `gh` | `gh` 覆盖完整 API 表面;模型从训练中已熟知;官方 GitHub MCP 已归档 |
| GitLab MCP | **用 CLI** | `glab` | 官方 CLI 比 MCP 封装更丰富;实践者共识予以证实 |
| Git MCP (Anthropic) | **用 CLI** | `git` | git 是模型最熟悉的 CLI;在前沿模型上,MCP schema 增加成本却无结构性收益 |
| Filesystem MCP | **用 CLI** | `cat`、`ls`、`find` | shell 命令通用;从 schema 开销中得不到好处 |
| Docker MCP | **用 CLI** | `docker` | Docker CLI 人尽皆知;没有广泛采用的 MCP 能提供可比价值 |
| AWS MCP | **用 CLI** | `aws-cli` | aws-cli v2 覆盖完整表面;模型凭训练知识即可原生驱动 |
| Terraform MCP | **用 CLI** | `terraform` | 确定性的 plan/apply 工作流;CLI 输出结构化且可审计 |
| Semgrep MCP | **用 CLI** | `semgrep` | 成熟且文档完善的 CLI;MCP 主要在 CI/CD 可观测性场景中增值 |
| Playwright MCP | **视情况而定** | `playwright-cli` + skill | 前沿模型:CLI + skill 更快。更小的模型:MCP 可可靠地结构化浏览器交互 |
| Kubernetes MCP | **视情况而定** | `kubectl` | 认证复杂性和多集群配置利好 MCP;简单操作利好 kubectl |
| Vercel MCP | **视情况而定** | `vercel` CLI | CLI 用于部署、环境变量和域名;MCP 用于仪表盘集成和团队工作流评论 |
| Sentry MCP | **用 MCP** | `sentry-cli`(限于 CI/CD) | `sentry-cli` 处理发布、source map 上传和 CI/CD 操作,但对交互式问题查询没有等价物。MCP 为编码 agent 提供结构化的错误分诊。 |
| Slack MCP | **用 MCP** | 无 | 需要 OAuth;agent 没有可用的 CLI 来访问工作区 |
| Notion MCP | **用 MCP** | 无 | 需要 OAuth;API-key 访问仅限于集成,不能进行用户作用域的工作区访问 |
| Google Drive MCP | **用 MCP** | 无 | 带刷新 token 轮换的 OAuth 2.1;skill 或 CLI 无法复制 |
| Figma MCP | **用 MCP** | 无 | 需要 OAuth;设计文件访问没有 CLI 等价物 |
| Linear MCP | **用 MCP** | 无 | MCP 处理 GraphQL 的复杂性;无需裸 API 调用即可进行结构化项目管理 |
| Context7 MCP | **用 MCP** | 无 | 对于精选的、特定版本的文档检索,没有 CLI 等价物 |

规律:如果某服务有一个模型从训练中已熟知的成熟 CLI,就用 CLI。如果某服务需要 OAuth 或没有 CLI,就用 MCP。"视情况而定"意味着决策取决于模型能力或具体的工作流需求。

> 参加交互式测验(6 个问题,1 分钟内):[cc.bruniaux.com/mcp-or-cli/](https://cc.bruniaux.com/mcp-or-cli/)

---

## 混合方案才是默认选择

大多数生产级工作流并不二选一。它们两者并用,各自覆盖自己最擅长处理的层级。

**一个实际例子**(来自实践者):

- **内层**(本地开发迭代、git、文件操作、shell 脚本)→ CLI,快速、确定、无开销
- **外层**(CI/CD、共享基础设施、跨团队服务)→ MCP Remote,可观测、集中、可扩展
- **Skill 层**(面向用户的操作,为非技术用户封装的 CLI 工具)→ 封装进 skill 的 CLI,对最终用户透明

错误在于对两层套用同一个答案。一个为自己搭建 Claude Code 工作流的独立开发者应当主要使用 CLI。一个向非技术同事部署 AI 助手的团队则应当主要使用 MCP。

---

## MCP schema 的 token 成本——数字到底是什么样

自 v2.1.7(2026 年 1 月)起,Claude Code 默认使用 **MCP Tool Search**(惰性加载)。这显著改变了 token 的算法,但并未完全消除 schema 成本。

**惰性加载如何工作:** 与其在会话开始时注入所有工具 schema,Claude 只会在一个 `<available-deferred-tools>` 块中收到工具名称。完整 schema 仅在 Claude 决定调用某个特定工具时才通过 `ToolSearch` 获取。会话中未使用的工具在上下文里只花费其名称的成本(约 0 个 schema tokens),而非完整定义。

**实测影响**(Anthropic 基准测试,5 服务器配置):

| 场景 | token 开销 | 备注 |
|----------|---------------|------|
| v2.1.7 之前(急切加载) | 约 55,000 tokens | 所有 schema 预加载 |
| v2.1.7 之后(惰性加载) | 约 8,700 tokens | 降低 85% |
| CLI(无 MCP) | 约 0 tokens | 基线 |

旧的最坏情况说法"每服务器 500-2,000 tokens"描述的是急切加载,而它已不再是默认。在惰性加载下,每个未使用服务器的成本接近于零。每个*已使用*服务器的成本(每个按需加载的工具 schema 约 600 tokens)仍然真实存在,但如今是按使用付费,而非始终常驻。

**即便有惰性加载仍会增加的开销:**

- 工具名称仍在启动时注入(每个服务器的每个工具占一行)
- schema 在首次调用时加载——使用大量工具的长会话会累积成本
- 每个服务器的连接建立开销不变(是延迟,不是 tokens)
- 连接大量 MCP 服务器仍意味着上下文中有更多名称,即便 schema 保持延迟加载

**配置**(v2.1.9+):`ENABLE_TOOL_SEARCH` 环境变量控制阈值。`auto:N` 在 MCP 工具超过上下文的 N% 时触发惰性加载(默认 10%)。

**缓解策略**(仍然相关,但紧迫性降低):

- 按项目选择性地加载 MCP 服务器(项目级配置 vs 全局配置)
- 对任何开销都会累积放大的高频紧密循环(编译 → 测试 → 修复)使用 CLI 工具
- 监控每个会话的 token 用量,以识别在调用时被加载的是哪些 schema
- 对于你经常使用但不需要其结构化输出的工具,考虑使用 CLI 封装

---

## 该领域的工具

| 工具 | 作用 | 状态 |
|------|-------------|--------|
| **RTK** (Rust Token Killer) | 在 CLI 输出抵达 Claude 上下文之前对其进行过滤——减少响应的冗余程度，而非 schema 开销 | 生产可用，持续维护中 |
| **MCPorter** (steipete) | 用于从脚本调用 MCP 服务器、生成 CLI 包装器并输出带类型的 TS 客户端的 TypeScript 运行时。适合测试 MCP 服务器以及编写需要 MCP 访问的 hooks。 | 3K stars，MIT，2 周以上，可直接使用 |
| **mcp2cli** (knowsuchagency) | 将 MCP/OpenAPI/GraphQL 转换为运行时 CLI，消除 schema 注入。在拥有 43 个工具的 GitHub MCP 服务器上基准测试显示 token 减少 32 倍（44K → 1.4K tokens）。 | 约 1.9K stars，Show HN Best of March 2026——对于拥有 10 个以上工具的远程 MCP 服务器具备生产可用性。参见[完整分析](./third-party-tools.md#mcp2cli)。 |

关于 mcp2cli 的说明：对于直接调用 API、远程 MCP 服务器以及 CI/CD 流水线，token 节省是实实在在的——已由 Firecrawl、Scalekit 和 CircleCI 独立完成基准测试。而对于标准的 Claude Code 会话，由于惰性加载（v2.1.7+）已经推迟了大多数 schema 的加载，增益较小。mcp2cli 最明显的适用场景，是当你从脚本或未内置延迟加载机制的 agents 中驱动 MCP 工具时。

---

## MCP 与 Skills 对比

Skills（`.claude/skills/*.md`）是第三种集成范式——既不同于 MCP 服务器，也不同于 CLI 工具。把它们与 CLI 混为一谈，是该领域最常见的框定错误。

**每一层各自的作用：**

- **Skills** 编码的是 *agent 应当如何行事*——以 markdown 编写的分步工作流、决策树和 SOP。它们按需加载进 agent 的上下文，引导其推理，而不注入外部工具 schema。
- **MCP 服务器** 提供 *对外部系统的结构化访问*——API、数据库、文件系统——配备 agent 可直接调用的带类型工具接口。
- **CLI 工具** 提供 *对外部系统的命令行访问*——agent 构造 shell 命令并解析文本输出。

Skills 与 MCP 解决的是不同层面的问题，而非同一个问题。一个 skill 可以描述何时以及如何调用某个 MCP 工具（检查这个字段，然后调用那个工具），而由 MCP 服务器负责实际的连接。问出"我该写一个 skill 还是一个 MCP 服务器？"，通常意味着这些层面被混淆了。

### OAuth 边界

这是 MCP 相对于 skills 最明确的结构性优势，而且并非便利性问题。

一个 skill 可以指示 agent "在继续之前先通过 Google Drive 进行身份验证"。但它做不到的，是持有 refresh token、完成浏览器重定向，或管理 PKCE 交换。这些操作需要服务器端状态，而 markdown 文件并不具备。

企业级 SaaS API——Google Workspace、Salesforce、Slack、GitHub——要求采用带 refresh token 轮换的 OAuth 2.1。当身份验证机制是这种形式时，MCP 不仅仅是更方便：它是唯一无需用户在每次会话开始时手动粘贴凭据就能正常工作的选项。

实用判断法：如果服务通过 header 中的 API key 进行身份验证，那么 skill 或 CLI 就能搞定。如果它需要浏览器重定向或服务器持有的 refresh token，那它就属于 MCP 的范畴。

### 社区共识（2026）

这场争论如今已大体落定为一个三层模型，而非二选一：

- **Skills** 处理 *做什么以及何时做*——工作流编排、决策引导、可复现的 agent 行为
- **MCP** 处理 *连接性与认证*——那些需要结构化接口、OAuth 或企业级可观测性的外部系统
- **CLI** 处理 *确定性的本地操作*——git、文件操作、测试运行器，以及任何模型可凭训练知识直接驱动的事项

这种融合如今已成为规范的一部分：SEP-2640（"Skills Over MCP"）提议将 skills 作为 MCP 资源进行分发，从而让用户以安装工具服务器同样的方式来安装工作流。这两种范式正在被统一，而非被迫相互竞争。

---

## 实践者怎么说

来自资深 Claude Code 用户的一些代表性观点：

> "对于确定性操作我更偏好 CLI。在与 GitLab 交互时我使用 glab（GitLab MCP 太受限了），并将其包装进一个自定义 CLI——人类和 AI 都能用。" —— 一位实践者

> "在搭配前沿模型的 Claude Code 上，MCP 越少越好。我用 playwright-cli + skill 替换了 playwright-mcp——更快也更有效。我仍然只用 context7-mcp，仅仅是因为我还没找到对应的 CLI 替代品。" —— 一位实践者

> "CLI 与 MCP 之争只发生在做开发工作的开发者之间。但有一个根本性的约束：你不可能向一个只想简单地使用工具的非技术用户提出一个 CLI 方案。" —— 一位实践者

> "对于企业级工业化落地，可观测性是不容妥协的。本地机器上的 CLI 是一个黑盒。MCP Remote 能为你提供高管层归因投资所需的日志记录。" —— 一位实践者

> "前沿模型已经足够强大，可以直接驱动 CLI。较弱的本地模型则会力不从心——这正是 MCP schema 的开销物有所值之处。" —— 一位实践者

---

*返回 [MCP 服务器生态](./mcp-servers-ecosystem.md) | [第三方工具](./third-party-tools.md) | [主指南](../ultimate-guide.md)*
