---
title: "Agent Teams Workflow"
description: "Multi-agent parallel coordination for complex tasks with autonomous team lead"
tags: [workflow, agents, architecture]
---

# Agent Teams 工作流

> **面向复杂任务的多 agent 并行协同**
> **状态**：实验性（v2.1.32+）| **模型**：需 Opus 4.6+ | **标志位**：`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

**是什么**：多个 Claude 实例在共享代码库上并行工作，无需人类主动干预即可自主协同。其中一个会话充当团队负责人（team lead），负责拆解任务并综合其他队友的发现。

**引入时间**：v2.1.32（2026-02-05），作为研究预览（research preview）
**阅读时间**：约 30 分钟
**前置要求**：Opus 4.6 模型、理解 [Sub-Agents](#split-role-sub-agents)、熟悉 Task Tool

**🚀 想快速上手？** 参见 **[Agent Teams 快速入门指南](./agent-teams-quick-start.md)**（8-10 分钟，可直接复制粘贴到你项目中的模式）

---

## 目录

1. [概述](#1-overview)
2. [架构深度剖析](#2-architecture-deep-dive)
3. [安装与配置](#3-setup--configuration)
4. [生产环境用例](#4-production-use-cases)
5. [工作流影响分析](#5-workflow-impact-analysis)
6. [局限与陷阱](#6-limitations--gotchas)
7. [决策框架](#7-decision-framework)
8. [最佳实践](#8-best-practices)
9. [故障排查](#9-troubleshooting)
10. [来源](#10-sources)

---

## 1. 概述

### 什么是 Agent Teams？

Agent teams 让**多个 Claude 实例并行处理**不同的子任务，同时通过一套基于 git 的系统进行协同。与那些需要你亲自编排多个独立 Claude 会话的手动多实例工作流不同，agent teams 提供内置的协同机制：agent 自行认领任务、持续合并改动、并自动解决冲突。

**关键特性**：
- ✅ **自主协同** —— 团队负责人负责委派任务，队友通过 mailbox 进行通信
- ✅ **点对点消息** —— agent 之间可直接通信（不仅限于层级式上报）
- ✅ **基于 git 的加锁** —— agent 通过向共享目录写入文件来认领任务
- ✅ **持续合并** —— 无需手动干预即可拉取/推送改动
- ✅ **独立上下文** —— 每个 agent 拥有自己的 1M token 上下文窗口（彼此隔离）
- ⚠️ **实验性** —— 研究预览，稳定性不作保证
- ⚠️ **高 token 消耗** —— 多个模型同时调用 = 高成本

### 引入时间

**版本**：v2.1.32（2026-02-05）
**模型**：最低 Opus 4.6
**状态**：研究预览（需启用实验性标志位）

**官方公告**：
> "We've introduced agent teams in Claude Code as a research preview. You can now spin up multiple agents that work in parallel as a team and coordinate autonomously on shared codebases."
> — [Anthropic, Introducing Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6)

> **📝 文档更新（2026-02-09）**：架构部分已根据 [Addy Osmani 的研究](https://addyosmani.com/blog/claude-code-agent-teams/)进行修正。关键澄清：agent 之间通过 mailbox 系统进行**点对点消息**通信，而不仅仅依赖团队负责人的综合汇总。上下文窗口仍然彼此隔离（每个 agent 各 1M token），但显式的消息机制使队友之间能够直接协同。

### Agent Teams 与其他模式的对比

| 模式 | 协同方式 | 配置 | 最适合 |
|---------|--------------|-------|----------|
| **Agent Teams** | 自动（内置） | 实验性标志位 | 需要协同的、读取密集型的复杂任务 |
| **多实例（Multi-Instance）** | 手动（人类编排） | 多个终端 | 相互独立的并行任务，无需协同 |
| **双实例（Dual-Instance）** | 手动（人类监督） | 2 个终端 | 质量保障，规划与执行分离 |
| **Task Tool** | 自动（sub-agents） | 原生功能 | 单 agent 任务委派，顺序工作 |

**关键区别**：
- **多实例** = 由你管理协同（独立项目，无共享状态）
- **Agent Teams** = 由 Claude 管理协同（共享代码库，基于 git 的通信）

---

## 📊 行业采用数据（Anthropic 2026）

> **来源**：[2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)

### 企业采用时间线

agent teams 代表了从"单 agent"到"协同团队"模式的演进，Anthropic 在 5000 多家组织中记录了这一过程：

| 采用阶段 | 时间线 | 特征 | 成功率 |
|---------------|----------|-----------------|--------------|
| **试点（Pilot）** | 第 1-2 月 | 1-2 个团队，实验性标志位 | 60-70% |
| **扩展（Expansion）** | 第 3-4 月 | 3-5 个团队，流程打磨 | 75-85% |
| **生产（Production）** | 第 5-6 月 | 全团队范围，集成 CI/CD | 85-90% |

**关键成功因素**：
- ✅ 模块化架构（在不产生冲突的前提下支持并行工作）
- ✅ 完善的测试（agent 可自主验证改动）
- ✅ 清晰的任务拆解（子任务边界定义明确）
- ❌ **阻碍因素**：单体代码库、测试覆盖薄弱

### 真实世界表现

**Fountain**（一线员工管理平台）：
- 通过层级式多 agent 编排实现**筛选速度提升 50%**
- 新履约中心**入职速度提升 40%**
- 通过自动化工作流实现**候选人转化率翻倍**
- **周期压缩**：新中心配齐人员从 1 周以上 → 72 小时

**Anthropic 内部**（来自研究团队）：
- 每位工程师每天**合并的 PR 多出 67%**
- **0-20% 的任务"完全委派"**（协作仍是核心）
- **27% 的新增工作**（这些任务若无 AI 则不会完成）

### 观察到的反模式

| 反模式 | 症状 | 解法 |
|-------------|---------|-----|
| **agent 过多** | >5 个 agent = 协同开销 > 生产力收益 | 从 2-3 个起步，逐步扩展 |
| **过度委派** | 上下文切换成本超过收益 | 对关键决策保持人类主动监督 |
| **过早自动化** | 自动化尚未手动掌握的工作流 | 手动 → 半自动 → 全自动（循序渐进） |

### 何时大型团队确实合理

上面的">5 个 agent"规则是一个合理的默认值，但在某些特定场景下它会失效——此时数学账反而更偏向更大的团队。真正的问题不是"用几个 agent？"，而是"协同开销是否比上下文溢出的代价更低？"

**上下文窗口才是决定因素**：单个 Claude Code agent 在 5 万行以上的代码库上，光是加载相关文件就会占满其上下文窗口的 80-90%（来源：atcyrus.com）。到那时，agent 几乎没有余量用于推理。把工作拆分到多个 agent，可以让每个 agent 的上下文使用率保持在约 40%，从而为真正的问题解决留出余地。

| 场景 | 单 agent | 3 个 agent 团队 | 5 个 agent 团队 |
|----------|-------------|--------------|--------------|
| 1 万行代码库 | 约 30% 上下文，从容 | 过度配置 | 过度配置 |
| 5 万行代码库 | 80-90% 上下文，推理能力下降 | 理想的拆分 | 若模块确实可并行则合理 |
| 10 万行以上代码库 | 上下文溢出，agent 漏读文件 | 每个 agent 仍可能溢出 | 合理，甚至可考虑更多 |

**何时增加 agent 更有意义**：
- 相互独立、零共享状态的模块（无需付出协同开销）
- 在彼此隔离的文件树上并行重构（前端 vs 后端 vs 基础设施）
- 读取密集型分析，每个 agent 负责不同的子系统
- 代码库在物理上无法连同充足余量装进单个 agent 的上下文

**何时增加 agent 反而有害**：如果 agent 不断需要读取彼此的输出或修改共享文件，增加 agent 只会带来更多合并冲突和协同消息，反而吞噬掉你本想节省的那部分上下文。

> **关于按角色选择模型的说明**：截至 2026 年 3 月，团队中的所有 agent 运行同一个模型（Opus 4.6，Agent Teams 必需）。社区已请求支持基于角色的模型选择——团队负责人用 Opus 做规划、实现类 agent 用 Sonnet 追求速度、测试类 agent 用 Haiku 控制成本。该功能尚未支持。当前的变通办法是用显式的 `--model` 标志位启动独立的 Claude Code 进程，但这样会失去内置的协同和共享任务列表。可将其作为一项社区功能请求持续关注。

更广阔的行业背景：Gartner 预测到 2026 年底，40% 的企业应用将整合任务专用 agent。如今在 Claude Code 及类似工具中确立的团队协同模式，很可能会成为标准实践。

### 成本-收益分析

**Agent Teams** vs **手动多实例**：

| 方面 | Agent Teams | 多实例（手动） |
|--------|-------------|------------------------|
| **配置时间** | 30-60 分钟（标志位 + git 配置） | 5-10 分钟（开新终端） |
| **协同** | 自动（基于 git） | 手动（人类编排） |
| **token 成本** | 高（持续消息通信） | 中（隔离的会话） |
| **最适合** | 读取密集型的复杂任务 | 相互独立的并行特性 |
| **采用时间线** | 3-6 个月达到生产可用 | 1-2 个月达到熟练 |

**Agent Teams 胜出的场景**：复杂重构、大规模分析、需协同的多文件改动
**多实例胜出的场景**：相互独立的特性、原型探索、简单并行化

---

## 2. 架构深度剖析

### 负责人-队友架构

```
┌─────────────────────────────────────────────────┐
│         Team Lead (Main Session)                │
│  - Breaks tasks into subtasks                   │
│  - Spawns teammate sessions                     │
│  - Synthesizes findings from all agents         │
│  - Coordinates via shared task list + mailbox   │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐  ┌───────▼────────┐
│  Teammate 1    │◄─┼────────────────►│  Teammate 2    │
│                │  │ Peer-to-peer    │                │
│ - Own context  │  │ messaging via   │ - Own context  │
│   (1M tokens)  │  │ mailbox system  │   (1M tokens)  │
│ - Claims tasks │  │                 │ - Claims tasks │
│ - Messages     │  │                 │ - Messages     │
│   team/peers   │  │                 │   team/peers   │
└────────────────┘  └─────────────────┘────────────────┘
```

### 基于 git 的协同

**工作原理**：

1. **任务认领**：agent 向共享目录（`.claude/tasks/`）写入锁文件
2. **执行工作**：每个 agent 在自己的上下文中独立工作
3. **持续合并**：agent 向共享 git 仓库拉取/推送改动
4. **冲突解决**：自动合并（有局限性，参见 [§6](#6-limitations--gotchas)）
5. **结果综合**：团队负责人收集各方发现，并给出统一的回应

**锁文件结构示例**：
```
.claude/tasks/
├── task-1.lock        # Agent A claimed
├── task-2.lock        # Agent B claimed
└── task-3.pending     # Not yet claimed
```

### 通信架构

**与 sub-agents 的关键区别**：agent teams 通过 mailbox 系统实现了**真正的点对点消息**，而不仅仅是层级式上报。

**架构组件**（来源：[Addy Osmani](https://addyosmani.com/blog/claude-code-agent-teams/)，2026 年 2 月）：

1. **团队负责人**：创建团队、派生队友、协调工作
2. **队友**：独立的 Claude Code 实例，各自拥有独立上下文（每个 1M token）
3. **任务列表**：带依赖追踪和自动解锁的共享工作项
4. **mailbox**：基于收件箱的消息系统，使 agent 之间能够直接通信

**通信模式**：
- **负责人 → 队友**：直接消息或向全员广播
- **队友 → 负责人**：进度更新、提问、发现
- **队友 ↔ 队友**：直接点对点消息（质疑方案、辩论解法）
- **最终综合**：团队负责人为用户汇总所有发现

**消息流示例**：
```
Team Lead: "Review this PR for security issues"
├─ Teammate 1 (Security): Analyzes → Messages Teammate 2: "Found auth issue in line 45"
├─ Teammate 2 (Code Quality): Reviews → Messages back: "Confirmed, also see OWASP violation"
└─ Team Lead: Synthesizes findings → Presents unified response to user
```

**这带来了什么**：
- ✅ agent 之间主动质疑彼此的方案
- ✅ 无需人类干预即可辩论解法
- ✅ 独立协同（自组织）
- ✅ 在工作流进行中分享发现（通过消息，而非上下文）

**局限**：上下文隔离依然存在——agent 之间不共享各自完整的上下文窗口，只共享显式的消息。

### 在 agent 之间切换导航

**内置导航**：
- **Shift+Down**：在 in-process 模式下循环切换队友
- **tmux/iTerm2**：通过 `teammateMode: "tmux"` 启用分屏模式（需要 tmux，或装有 `it2` CLI 的 iTerm2）
- **直接接管**：必要时你可以接管任意 agent 的工作

**示例**：
```bash
# Terminal 1: Team lead (with env var set)
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude

# Claude spawns teammates automatically
# You can navigate with Shift+Down to cycle through teammates (in-process mode)
```

### 上下文管理

**每个 agent 的上下文**：
- 每个 agent 拥有 **1M token 上下文窗口**（Opus 4.6）
- 每个会话约 30,000 行代码
- **上下文隔离**：agent 之间不共享各自完整的上下文窗口
- **通信**：通过 mailbox 系统（点对点 + 团队负责人综合）

**总上下文容量**（以 3 个 agent 为例）：
- 团队负责人：1M token
- 队友 1：1M token
- 队友 2：1M token
- **总计**：整个团队 3M token（上下文隔离，但通过消息通信）

**重要区别**：
- ❌ **上下文不共享**：agent 1 完整的 1M token 上下文对 agent 2 不可见
- ✅ **消息可共享**：agent 通过 mailbox 发送显式消息（发现、提问、辩论）

---

## 3. 安装与配置

### 前置条件

**必需项**：
- ✅ Claude Code v2.1.32 或更高版本
- ✅ Opus 4.6 模型（`/model opus`）
- ✅ Git 仓库（用于协调）

**推荐项**：
- ✅ 理解 [Sub-Agents](#split-role-sub-agents)
- ✅ 熟悉 git 工作流
- ✅ 预算意识（这是 token 密集型功能）

### 方法 1：环境变量

**最简单的方式** —— 在启动 Claude Code 之前设置环境变量：

```bash
# Enable agent teams for this session
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# Start Claude Code
claude
```

**持久化设置**（bash/zsh）：
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1' >> ~/.bashrc
source ~/.bashrc
```

### 方法 2：配置文件

**持久化配置** —— 编辑 `~/.claude/settings.json`：

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

**优势**：
- ✅ 跨会话持久化
- ✅ 无需记住环境变量
- ✅ 可在 dotfiles 中纳入版本控制

**编辑后**，重启 Claude Code 以使更改生效。

### 验证

**检查是否已启用**：

```bash
# In Claude Code session
> Are agent teams enabled?
```

Claude 应当确认：
> “是的，agent teams 已启用（实验性功能）。我可以在适当时机派生多个 agent 并行工作。”

**备用验证方式**（检查环境变量）：
```bash
echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS
# Should output: 1
```

### 多终端配置

**模式**（来自实践者报告）：

```bash
# Terminal 1: Research + bugfix
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude

# Terminal 2: Business ops
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude

# Terminal 3: Infrastructure
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude
```

**收益**：
- 上下文隔离（研究 vs 执行 vs 配置）
- 在彼此独立的工作流上并行推进
- 减少上下文切换的认知负担

**注意**：这与自动派生 teammate 不同 —— 这里你是手动创建多个 team lead 会话。每个会话都可以派生自己的 teammate。

---

## 4. 生产环境用例

### 已验证用例概览

| 用例 | 来源 | 指标 | 最适用于 |
|----------|--------|---------|----------|
| **多层代码审查** | Fountain（Anthropic 报告） | 筛选速度提升 50% | 安全 + API + 前端同时审查 |
| **完整开发生命周期** | CRED（Anthropic 报告） | 执行速度提升 2 倍 | 1500 万用户，金融服务合规 |
| **自主 C 编译器** | Anthropic Research | 项目完成 | 复杂的多阶段项目 |
| **求职应用** | Paul Rayner（LinkedIn） | “相当惊艳” | 设计调研 + 缺陷修复 |
| **业务运营自动化** | Paul Rayner（LinkedIn） | N/A | 运营系统 + 会议筹备 |

### 4.1 多层代码审查（Fountain）

**机构**：Fountain（一线员工管理平台）
**挑战**：跨多个关注点（安全、API 设计、前端）对代码库进行全面审查
**解决方案**：部署了分层多 agent 编排，使用聚焦特定范围的 sub-agent

**Agent 范围**（Fountain 的做法）：
- **范围 1（安全）**：扫描漏洞、认证问题、数据泄露
- **范围 2（API）**：审查端点设计、请求/响应校验、错误处理
- **范围 3（前端）**：检查 UI 模式、可访问性、性能

**结果**：
- ✅ 候选人筛选**速度提升 50%**
- ✅ 入职**速度加快 40%**
- ✅ 候选人转化率**提升 2 倍**

**为何奏效**：
- **读密集型任务**：代码审查 = 主要是阅读/分析（无写入冲突）
- **清晰的领域划分**：安全、API、前端之间几乎没有重叠
- **独立分析**：每个 agent 都可以在不等待其他 agent 的情况下工作

**示例 prompt**（team lead）：
```
Review this PR comprehensively with scope-focused analysis:
- Security Scope: Check for vulnerabilities and auth issues (context: auth code, input validation)
- API Design Scope: Review endpoint design and error handling (context: API routes, controllers)
- Frontend Scope: Check UI patterns and accessibility (context: components, styles)

PR: https://github.com/company/repo/pull/123
```

**来源**：[2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)，Anthropic，2026 年 1 月

### 4.2 完整开发生命周期（CRED）

**机构**：CRED（1500 万+ 用户，金融服务，印度）
**挑战**：在保持金融服务所必需的质量标准的同时加快交付
**解决方案**：在整个开发生命周期中部署 Claude Code，并对复杂任务使用 agent teams

**结果**：
- ✅ 整个开发生命周期**执行速度提升 2 倍**
- ✅ 保持合规（金融服务标准）
- ✅ 质量保障得以维持

**为何奏效**：
- **大型代码库**：1500 万用户 = 需要并行分析的复杂系统
- **质量至关重要**：金融服务 = 需要多层校验
- **紧迫的截止期限**：速度需求让 token 成本物有所值

**工作流模式**：
1. **规划阶段**：team lead 拆解功能
2. **实现阶段**：Teammate 1 = 后端，Teammate 2 = 前端，Teammate 3 = 测试
3. **质量保障**：team lead 进行整合并运行校验
4. **合规检查**：对照金融标准进行最终审查

**来源**：[2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)，Anthropic，2026 年 1 月

### 4.3 自主 C 编译器（Anthropic Research）

**项目**：自主构建一个完整的 C 编译器
**挑战**：需要协调的多阶段项目（词法分析器、语法分析器、AST、代码生成、优化）
**解决方案**：带有任务分解和进度跟踪的 agent teams

**已完成阶段**：
1. **词法分析器**：分词逻辑
2. **语法分析器**：语法树构建
3. **AST**：抽象语法树实现
4. **代码生成**：汇编输出
5. **优化**：性能改进
6. **测试**：编译器测试套件

**结果**：
- ✅ 在无人工干预的情况下**完成项目**
- ✅ 所有阶段协调成功
- ✅ 完成时测试全部通过

**为何奏效**：
- **清晰的阶段**：每个编译器阶段都定义明确（词法分析器 → 语法分析器 → 代码生成）
- **依赖最少**：各阶段之间有清晰的接口（tokens → AST → 汇编）
- **可测试的里程碑**：每个阶段都可独立验证

**架构洞见**：
> “各个 agent 将项目拆分为小块，跟踪进度，并确定下一步，直至完成。”
> —— [Building a C compiler with agent teams](https://www.anthropic.com/engineering/building-c-compiler)，Anthropic Engineering，2026 年 2 月

**关键经验**：
- ⚠️ **测试通过 ≠ 正确性**：人工监督对质量保障仍然重要
- ⚠️ **需要验证**：自动化的成功并不保证代码无错
- ✅ **可行性已证实**：复杂的多阶段项目可以通过 agent teams 实现

**来源**：[Building a C compiler with agent teams](https://www.anthropic.com/engineering/building-c-compiler)，Anthropic Engineering，2026 年 2 月

### 4.4 求职应用开发（Paul Rayner）

**实践者**：Paul Rayner（Virtual Genius CEO，EventStorming Handbook 作者，Explore DDD 创始人）
**配置**：在多个独立终端中并行运行 3 个 agent team 会话
**日期**：2026 年 2 月（v2.1.32 发布当天）

**工作流 1 - 求职应用**：
- **背景**：定制求职应用开发
- **任务**：
  - 设计方案调研（探索 UI/UX 模式）
  - 现有代码库中的缺陷修复
- **模式**：在同一工作流中进行研究 + 执行

**工作流 2 - 业务运营**：
- **背景**：运营系统开发 + 会议筹备
- **任务**：
  - 业务运营系统自动化
  - 会议筹备资源（Explore DDD）
- **模式**：跨领域业务工具

**工作流 3 - 基础设施 + 框架**：
- **背景**：测试基础设施 + 框架集成
- **任务**：
  - Playwright MCP 实例配置
  - Beads 框架管理（Steve Yegge）
- **模式**：基础设施 + 框架协调

**结果**：
- ✅ “相当惊艳”（主观评价，无指标）
- ✅ 优于以往缺乏协调的多终端工作流
- ✅ 3 个独立上下文同时运行

**为何值得关注**：
- **真实世界验证**：由经验丰富的实践者在生产环境中使用
- **多上下文**：3 个不同领域（产品、业务、基础设施）同时进行
- **早期采用**：与 v2.1.32 发布同日发帖（早期采用者信号）

**提出的开放性问题**：
> “我不太清楚 Claude 关于何时使用 beads 还是 agent team 会话的指导。有什么想法吗？”
> —— Paul Rayner，LinkedIn，2026 年 2 月

**来源**：[Paul Rayner LinkedIn](https://www.linkedin.com/posts/thepaulrayner_this-is-wild-i-just-upgraded-claude-code-activity-7425635159678414850-MNyv)，2026 年 2 月

### 4.5 并行假设测试（模式）

**场景**：调试一个有多个潜在根因的复杂生产问题

**配置**：
```
Team lead prompt:
"Production API is slow. Test these hypotheses in parallel:
- Hypothesis 1 (DB): Query performance issue
- Hypothesis 2 (Network): Latency spikes
- Hypothesis 3 (Cache): Invalidation problem
Each agent: profile, reproduce, report findings"
```

**Agent 分工**：
- **Agent 1**：数据库剖析（慢查询日志、执行计划）
- **Agent 2**：网络分析（延迟指标、路由追踪）
- **Agent 3**：缓存行为（命中率、失效模式）

**收益**：
- ✅ **并行调查**：3 个假设同时测试（相对于串行）
- ✅ **节省时间**：串行调试时间的 1/3
- ✅ **覆盖全面**：不会因时间限制而忽略任何假设

**何时使用**：
- 对观察到的行为存在多种合理解释
- 每个假设都可独立测试
- 时间紧迫的调试（生产问题）

### 4.6 大规模重构（模式）

**场景**：跨 47 个文件（前端 + 后端 + 测试）重构认证系统

**配置**：
```
Team lead prompt:
"Refactor auth system from JWT to OAuth2:
- Agent 1: Backend endpoints (/api/auth/*)
- Agent 2: Frontend components (src/components/auth/*)
- Agent 3: Integration tests (tests/auth/)
Coordinate changes via shared interfaces"
```

**Agent 分工**：
- **Agent 1**：后端实现（15 个文件）
- **Agent 2**：前端 UI 更新（20 个文件）
- **Agent 3**：测试套件更新（12 个文件）

**收益**：
- ✅ **上下文保留**：全部 47 个文件在一个协调的会话中（相对于约 15 个文件后丢失上下文）
- ✅ **接口一致性**：跨 agent 强制执行共享契约
- ✅ **原子化迁移**：所有层级协调更新

**陷阱**：
- ⚠️ **合并冲突**：如果多个 agent 修改相同文件（例如共享类型）
- ⚠️ **缓解措施**：明确接口边界，尽量减少对共享文件的修改

---

## 5. 工作流影响分析

### 前后对比

**背景**：使用 agent teams 相比单 agent 会话会带来哪些变化？

| 任务 | 单 Agent（之前） | Agent Teams（之后） |
|------|-----------------------|---------------------|
| **Bug 追踪** | 逐个喂入文件，每次都要重新解释架构 | 一次性看到整个代码库，跨所有层追踪完整数据流 |
| **代码评审** | 自己手动总结 PR，在 prompt 中解释上下文 | 喂入完整 diff + 周边代码，agents 直接阅读 |
| **新功能** | 在 prompt 中描述代码库结构（受限于你自己的理解） | 让 agents 直接阅读代码库，自行发现模式 |
| **重构** | 约 15 个文件后丢失上下文，被迫拆成多个会话 | 全部 47+ 个文件在一个协调会话中存活 |
| **多服务调试** | 一次调试一个服务，手动跟踪跨服务流程 | 跨所有相关服务并行调查 |

**来源**：[Claude Opus 4.6 for Developers](https://dev.to/thegdsks/claude-opus-46-for-developers-agent-teams-1m-context-and-what-actually-matters-4h8c), dev.to, Feb 2026

### 上下文管理改进

**单 agent 的局限**：
- 约 15 个文件后，上下文管理开始变得困难
- 大型代码库需要手动总结
- 对独立组件只能串行分析

**Agent teams 的能力**：
- **每个 agent 1M tokens** = 约 30,000 行代码
- **3 个 agents** = 团队整体有效约 90,000 行（隔离的上下文）
- **并行阅读**：agents 同时消化代码库的不同部分
- **综合汇总**：team lead 在不丢失上下文的情况下整合各方发现

**示例**：
```
Scenario: Analyze 28,000-line TypeScript service

Single agent:
- Read files sequentially
- Context pressure at ~15 files
- Manual summarization
- ~2-3 hours

Agent teams:
- Agent 1: Controllers layer (10K lines)
- Agent 2: Services layer (10K lines)
- Agent 3: Data layer (8K lines)
- Team lead: Synthesize architecture
- ~45 minutes
```

### 协调带来的收益

**内建协调 vs 手动协调**：

| 方面 | 手动多实例 | Agent Teams |
|--------|----------------------|-------------|
| **任务分派** | 由你决定如何拆分 | 由 team lead 决定 |
| **进度跟踪** | 手动签到 | 自动汇报 |
| **合并冲突** | 由你解决 | 自动（有局限） |
| **上下文共享** | 复制粘贴各方发现 | 基于 Git 的协调 |
| **认知负担** | 高（编排者角色） | 低（观察者角色） |

**协调何时重要**：
- ✅ 有依赖关系的任务（功能 A 需要功能 B 的 API）
- ✅ 共享接口（多个 agents 修改同一份契约）
- ✅ 质量门禁（所有 agents 必须通过才能合并）

**协调何时不必要**：
- ❌ 完全独立的任务（彼此独立的项目）
- ❌ 无共享状态（不同的代码仓库）
- ❌ 简单并行化（对不同数据运行相同脚本）

### 成本权衡

**Token 消耗对比**（估算）：

| 工作流 | 单 Agent | Agent Teams（3 个） | 倍数 |
|----------|-------------|-----------------|------------|
| **代码评审（小 PR）** | 10K tokens | 25K tokens | 2.5x |
| **代码评审（大 PR）** | 50K tokens | 90K tokens | 1.8x |
| **Bug 调查** | 30K tokens | 70K tokens | 2.3x |
| **功能实现** | 100K tokens | 200K tokens | 2x |
| **重构（大型）** | 150K tokens | 250K tokens | 1.7x |

**成本合理的场景**：
- ✅ **时间紧迫**：需要快速解决的生产问题
- ✅ **复杂度高**：多层分析（安全 + 性能 + 架构）
- ✅ **质量要求高**：需要多层验证的高风险变更
- ❌ **简单任务**：直白的实现（大材小用）
- ❌ **预算受限**：token 限额吃紧的个人项目

**经验法则**：当节省的时间价值 > token 成本增加 2 倍时，agent teams 才划算。

---

## 6. 局限与陷阱

### 读密集 vs 写密集的权衡

**核心局限**：agent teams 擅长读密集型任务，但在多个 agents 修改同一批文件的写密集型任务上表现吃力。

**为什么这很重要**：
```
Read-heavy (✅ Good for teams):
- Code review: Agents read code, provide analysis
- Bug tracing: Agents read logs, trace execution
- Architecture analysis: Agents read structure, identify patterns

Write-heavy (⚠️ Risky for teams):
- Refactoring shared types: Multiple agents modify same file → merge conflicts
- Database schema changes: Coordinated migrations across files
- API contract updates: Interface changes require synchronization
```

**缓解策略**：
1. **明确边界**：给各 agent 分配互不重叠的文件集
2. **接口优先**：在并行实现之前先定义好契约
3. **单写者模式**：由一个 agent 写共享文件，其他人只读
4. **人工评审**：发生合并冲突时手动解决

### 合并冲突场景

**自动解决有效的情况**：
- ✅ 不同 agents 修改不同文件
- ✅ 同一文件中的不同函数（干净的 git merge）
- ✅ 增量式改动（新增函数，无编辑）

**自动解决吃力的情况**：
- ❌ 修改了相同的行（经典合并冲突）
- ❌ 逻辑相互冲突（Agent A 删除校验，Agent B 添加校验）
- ❌ 循环依赖（Agent A 需要 Agent B 的产出，反之亦然）

**冲突示例**：
```typescript
// Agent 1 changes:
function processUser(user: User) {
  validateEmail(user.email); // Added validation
  return save(user);
}

// Agent 2 changes (same time):
function processUser(user: User) {
  return save(sanitize(user)); // Added sanitization
}

// Conflict: Both modified same function
// Resolution: Human decides order (validate → sanitize → save)
```

### Token 密集型的影响

**为什么消耗大量 token**：
- 每个 agent 都运行**独立的模型推理**（3 个 agents = 3 倍基础成本）
- 每个 agent 都要加载上下文（1M tokens × 3 = 3M token 容量）
- 协调开销（team lead 的综合汇总）

**预算影响示例**（Opus 4.6 定价）：
```
Single agent session:
- Input: 50K tokens @ $15/M = $0.75
- Output: 5K tokens @ $75/M = $0.38
- Total: $1.13

Agent teams (3 agents):
- Input: 150K tokens @ $15/M = $2.25
- Output: 15K tokens @ $75/M = $1.13
- Total: $3.38

Cost multiplier: 3x
```

**需要论证合理性的情形**：
- ✅ 节省的时间 > 成本增加（生产问题）
- ✅ 质量至关重要（金融服务、医疗健康）
- ✅ 复杂度足以支撑并行化（多层分析）
- ❌ 简单任务（用单 agent）
- ❌ 个人学习项目（预算受限）

### 实验性状态的注意事项

**"实验性"意味着什么**：
- ⚠️ **不保证稳定**：功能可能变更或被移除
- ⚠️ **预期会有 bug**：将问题反馈给 Anthropic（GitHub Issues）
- ⚠️ **性能波动**：协调速度可能起伏不定
- ⚠️ **文档仍在演进**：官方文档仍然很少

**生产使用注意事项**：
1. **回退方案**：随时准备好在出问题时回退到单 agent
2. **监控**：仔细跟踪 token 成本（可能快速飙升）
3. **验证**：人工评审 agent team 的产出（不要盲目信任）
4. **反馈**：反馈 bug 与使用体验，帮助 Anthropic 改进该功能

**从业者反馈**（截至 Feb 2026）：
- ✅ Paul Rayner："相当惊艳"（生产使用已验证）
- ✅ Fountain：速度提升 50%（已部署到生产）
- ✅ CRED：速度提升 2 倍（1500 万用户，金融服务）
- ⚠️ 社区：反馈不一（部分存在合并冲突问题）

### 上下文隔离

**agents 不能做的事**：
- ❌ **共享上下文窗口**：Agent 1 的完整上下文（1M tokens）对 Agent 2 不可见
- ❌ **自动同步发现**：Agent 2 不会看到 Agent 1 的发现，除非显式发消息告知
- ❌ **协调时序**：agents 各自独立工作，可能在不同时间完成

**agents 能做的事**：
- ✅ **发送消息**：通过 mailbox 系统（点对点或经由 team lead）
- ✅ **质疑方案**：辩论解决方案，互相提问
- ✅ **共享发现**：显式发消息（而非自动共享上下文）

**影响**：
```
Scenario: Agent 1 discovers critical bug that affects Agent 2's work

Without messaging:
- Agent 2 doesn't see Agent 1's discovery automatically
- Agent 2 may continue with flawed assumption

With messaging (built-in):
- Agent 1 messages Agent 2: "Found auth issue in line 45"
- Agent 2 adjusts approach based on message
- Team lead synthesizes all findings at end

Mitigation:
- Agents can message each other via mailbox system
- Team lead synthesizes findings after all agents complete
- Human can interrupt and redirect agents mid-workflow (Shift+Down to cycle teammates)
- Design tasks with minimal inter-agent dependencies
```

### 何时不该使用 Agent Teams

**单 agent 更适合的情况**：
- ❌ **简单任务**：直白的实现（大材小用）
- ❌ **小型代码库**：影响 <5 个文件（协调开销不划算）
- ❌ **写密集型任务**：大量共享文件修改（合并冲突风险）
- ❌ **串行依赖**：任务 B 需要任务 A 完成（无法从并行化获益）
- ❌ **预算受限**：个人项目、学习（token 成本倍增）
- ❌ **紧密相互依赖**：任务之间存在循环依赖

**不适合的示例**：
```
Task: Update authentication logic in shared auth.ts file

Why single agent better:
- One file modified (no parallelization benefit)
- Write-heavy (multiple changes to same file)
- No clear subtask boundaries (logic intertwined)
- Sequential flow (test after each change)

Result: Agent teams would create merge conflicts, no time savings
```

---

## 7. 决策框架

### Teams vs Multi-Instance vs Dual-Instance

**对比表**：

| 标准 | Agent Teams | Multi-Instance | Dual-Instance |
|-----------|-------------|----------------|---------------|
| **协调** | 自动（基于 git + 邮箱机制） | 手动（人工） | 手动（人工） |
| **设置** | 实验性 flag | 多个终端 | 2 个终端 |
| **最适合** | 需要协调的读密集型任务 | 独立的并行任务 | 质量保证（计划-执行分离） |
| **通信** | 点对点消息传递 + team lead 综合 | 手动复制粘贴 | 手动同步 |
| **上下文共享** | 隔离（每个 agent 1M，无自动同步） | 隔离（独立会话） | 隔离（2 个会话） |
| **成本** | 高（3x+ token） | 中（2x token） | 中（2x token） |
| **认知负荷** | 低（观察者） | 高（编排者） | 中（评审者） |
| **合并冲突** | 自动解决（有限） | 不适用（独立仓库） | 手动解决 |
| **成熟度** | 实验性（v2.1.32+） | 稳定 | 稳定 |

### 决策树：何时使用 Agent Teams

```
Start
  │
  ├─ Task is simple (<5 files)? ──YES──> Single agent
  │
  ├─ NO
  │
  ├─ Tasks completely independent? ──YES──> Multi-Instance
  │
  ├─ NO
  │
  ├─ Need quality assurance split? ──YES──> Dual-Instance
  │
  ├─ NO
  │
  ├─ Read-heavy (analysis, review)? ──YES──> Agent Teams ✓
  │
  ├─ NO
  │
  ├─ Write-heavy (many file mods)? ──YES──> Single agent
  │
  ├─ NO
  │
  ├─ Budget-constrained? ──YES──> Single agent
  │
  ├─ NO
  │
  └─ Complex coordination needed? ──YES──> Agent Teams ✓
                                   ──NO──> Single agent
```

### 用例映射

**Agent Teams（✅ 使用）**：
- 多层代码评审（安全 + API + 前端）
- 并行假设测试（调试）
- 大规模重构（边界清晰）
- 全代码库分析（架构评审）
- 复杂功能研究（探索多种方案）

**Multi-Instance（✅ 使用）**：
- 独立的项目（前端仓库 + 后端仓库）
- 独立的功能（无共享状态）
- 不同的技术栈（Python 微服务 + React 应用）
- 并行实验（尝试 3 种不同架构）

**Dual-Instance（✅ 使用）**：
- 计划-执行模式（规划会话 + 执行会话）
- 质量评审（实现 + 代码评审）
- 测试先行开发（编写测试 + 实现）

**Single Agent（✅ 使用）**：
- 简单的实现（<5 个文件）
- 写密集型任务（共享文件修改）
- 顺序工作流（逐步教程）
- 预算受限的项目

### Teams vs Beads Framework

**Beads Framework**（Steve Yegge）：
- **架构**：事件溯源的 MCP server（Gas Town）+ SQLite 数据库（beads.db）
- **协调**：持久化消息存储、历史回放
- **成熟度**：社区维护，实验性
- **设置**：需要安装 Gas Town + agent-chat UI
- **用例**：本地部署/隔离网络环境，对编排的完全控制

**Agent Teams**（Anthropic）：
- **架构**：原生 Claude Code 功能，基于 git 的协调
- **协调**：实时 git 锁定、自动合并
- **成熟度**：Anthropic 官方功能（实验性）
- **设置**：仅需 feature flag（`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`）
- **用例**：快速原型开发、基于云的开发

**对比**：

| 方面 | Beads Framework | Agent Teams |
|--------|----------------|-------------|
| **控制** | 完全（事件溯源、回放） | 有限（黑盒协调） |
| **设置** | 复杂（Gas Town + agent-chat） | 简单（feature flag） |
| **持久化** | SQLite（beads.db） | Git 提交 |
| **可见性** | agent-chat UI（类 Slack） | 原生 Claude Code 界面 |
| **环境** | 适合本地部署 | 云优先 |
| **成熟度** | 社区驱动 | Anthropic 官方 |

**何时使用 Beads**：
- ✅ 本地部署/隔离网络要求（无云端 API 调用）
- ✅ 需要事件回放（调试编排）
- ✅ 自定义编排逻辑（超出基于 git 的范围）
- ✅ 持久化的 agent 通信（审计追踪）

**何时使用 Agent Teams**：
- ✅ 云端开发（可访问 Anthropic API）
- ✅ 快速设置（无需基础设施）
- ✅ git 原生工作流（已在使用 git）
- ✅ 官方支持路径（Anthropic 维护）

**待解决的问题**（截至 2026 年 2 月）：
> "我不确定 Claude 对于何时使用 beads 而非 agent team 会话的指导意见。"
> — Paul Rayner，2026 年 2 月

**需要社区反馈**：Anthropic 尚未就这一选择发布官方指导。欢迎实践者在 [GitHub Discussions](https://github.com/anthropics/claude-code/discussions) 分享经验。

---

## 8. 最佳实践

### 任务分解策略

**清晰边界原则**：
```
Good decomposition:
- Agent 1: Backend API endpoints (/api/users/*)
- Agent 2: Frontend components (src/components/users/*)
- Agent 3: Database migrations (db/migrations/users/)

Why good:
- Non-overlapping file sets (no merge conflicts)
- Clear interfaces (API contracts)
- Independent testing (each layer testable)
```

```
Bad decomposition:
- Agent 1: User authentication
- Agent 2: User authorization
- Agent 3: User session management

Why bad:
- Overlapping files (auth.ts touched by all 3)
- Interdependencies (auth needs sessions, sessions need auth)
- Sequential coupling (can't parallelize effectively)
```

**接口先行方法**：
1. **定义契约**：在并行工作前就函数签名、API schema 达成一致
2. **类型桩**：先创建 TypeScript 类型/接口，再分别实现
3. **模拟边界**：每个 agent 初期使用模拟的依赖进行工作
4. **集成阶段**：team lead 协调最终集成

**示例**：
```typescript
// Team lead defines interface first
interface UserService {
  authenticate(email: string, password: string): Promise<User>;
  authorize(user: User, resource: string): Promise<boolean>;
}

// Agent 1 implements authenticate
// Agent 2 implements authorize
// No merge conflicts (different functions)
```

### 协调模式

**Fan-out, fan-in**：
```
Team lead
  │
  ├─ Agent 1: Task A ──┐
  ├─ Agent 2: Task B ──┼──> Team lead synthesizes
  └─ Agent 3: Task C ──┘
```

**带并行化的顺序阶段**：
```
Phase 1 (Sequential):
  Team lead: Define architecture

Phase 2 (Parallel):
  ├─ Agent 1: Implement backend
  ├─ Agent 2: Implement frontend
  └─ Agent 3: Write tests

Phase 3 (Sequential):
  Team lead: Integration + validation
```

**分层委派**：
```
Team lead
  │
  ├─ Agent 1 (Backend lead)
  │   ├─ Agent 1a: Controllers
  │   └─ Agent 1b: Services
  │
  └─ Agent 2 (Frontend lead)
      ├─ Agent 2a: Components
      └─ Agent 2b: State management
```

### 用于复合学习的 AGENTS.md

Agent teams 能从一个共享的上下文文件中受益，该文件累积跨会话的经验——行之有效的模式、需要规避的陷阱、代码库特有的坑。这个文件称为 `AGENTS.md`（类似于 `CLAUDE.md`，但作用域限定于 agentic 工作流）。

**应放入 AGENTS.md 的内容**：
```markdown

## 经过验证的模式
- 对该代码库使用接口优先（Interface-First）的拆分方式（参见 src/types/）
- 后端 agent 必须在测试前运行 `db:migrate` —— 环境不会自动填充种子数据

## 陷阱
- 不要并行修改 auth.ts 和 session.ts —— 循环导入会导致测试失败
- 保存时会运行 linter；不要在带有 lint 错误的情况下提交，CI 关卡非常严格

## 风格
- 所有 API 响应都必须遵循 ApiResponse<T> 包装类型
- 错误码存放于 src/constants/errors.ts —— 始终复用，永远不要硬编码字符串
```

**关键规则 —— 永远不要让 agent 直接编写 AGENTS.md**。苏黎世联邦理工学院（ETH Zürich）的研究（Gloaguen et al., 2026）证实，与开发者手写文件带来约 4% 的提升相比，由 LLM 生成的上下文文件会使任务成功率降低约 3%，并使推理成本增加 20% 以上。其机制在于：agent 生成的是通用、臃肿的上下文，给后续每一个读取它的 agent 都带来认知负担。

AGENTS.md 中的每一行都应由人类审批。如果某位团队成员发现了值得记录的新模式，它会向团队负责人发送一条建议 —— 由负责人决定是否将其加入。

**维护**：在每次团队会话之后审查 AGENTS.md（即 Factory Model 中的 Retro 步骤）。删除不再相关的条目 —— 过时的指令是会主动造成危害的，而非中性的。

### Git Worktree 管理

**为什么 worktree 很重要**：
- 每个 agent 在各自独立的 git worktree 中工作（隔离的文件系统）
- 防止文件锁冲突
- 支持并行的文件修改

**设置**：
```bash
# Main repository
git worktree add ../project-agent1 main

# Agent 1 works in project-agent1/
# Agent 2 works in project-agent2/
# Team lead works in project/

# All sync via git commits
```

**最佳实践**：
- ✅ 每个 agent 一个 worktree
- ✅ 频繁提交（持续合并）
- ✅ 具有描述性的分支名（`agent1-backend-api`、`agent2-frontend-ui`）
- ❌ 不要在没有协调的情况下跨 worktree 修改相同文件

### 成本优化

**节省 token 的策略**：

1. **惰性派生（Lazy spawning）**：仅在并行化明显有益时才派生 agent
   ```
   Bad: "Spawn 3 agents to implement this button"
   Good: "Spawn agents for multi-layer security review"
   ```

2. **上下文裁剪（Context pruning）**：从 agent 的上下文中移除无关文件
   ```
   # Tell agent what to ignore
   "Review backend API, ignore frontend files"
   ```

3. **渐进升级（Progressive escalation）**：先用单个 agent，必要时再升级为团队
   ```
   Step 1: Single agent attempts task
   Step 2: If complexity high, spawn team
   ```

4. **结果缓存（Result caching）**：在相似任务间复用 agent 的发现
   ```
   "Agent 1 found security issues in auth.ts.
   Agent 2, check if user.ts has same patterns."
   ```

5. **为每个 agent 设置硬性 token 预算**：分配特定领域的限额，以防止失控的消耗
   ```bash
   # In task brief to each teammate
   "Frontend agent: stay under 180k tokens total.
   Backend agent: stay under 280k tokens total.
   Auto-pause and report status at 85% of your budget."
   ```
   token 成本随团队规模线性增长 —— 一个 5 个 agent 的团队消耗的 token 可能是单个会话的 5 倍。设置上限可防止某个 agent 钻牛角尖而耗尽整个会话的预算。

### 质量保证

**验证清单**：
- [ ] **所有 agent 已完成**：没有悬挂的任务
- [ ] **合并冲突已解决**：干净的 git 历史
- [ ] **测试通过**：自动化测试套件全绿
- [ ] **人工审查**：代码审阅（不要盲目信任）
- [ ] **跨 agent 一致性**：命名、模式保持一致

**警示信号**：
- ⚠️ agent 在差异很大的时间点完成（负载不均衡）
- ⚠️ 大量合并冲突（任务拆分不当）
- ⚠️ 合并后测试失败（集成问题）
- ⚠️ 代码风格不一致（agent 未遵循共享标准）

**缓解措施**：
```bash
# After agent teams complete
git diff main..agent-teams-branch  # Review all changes
npm test                           # Run full test suite
npm run lint                       # Check code style
```

### 循环护栏

如果没有硬性的迭代限制，agent 团队可能会陷入无效的重试循环。有两种机制可以防止这种情况：

**每个团队成员的 MAX_ITERATIONS**：

在每位团队成员的任务简报中设置硬性上限：
```
"Maximum 8 attempts on any single failing task.
Before retrying, answer: What specifically failed? What one change would fix it?
If still blocked after 8 attempts, stop and report to team lead."
```

强制性的反思提示（"具体哪里失败了？哪一项改动能修复它？"）能大幅减少卡住的 agent —— 它迫使 agent 改变方法，而不是带着细微变化重复同样失败的操作。

**终止并重新分配的标准**：
- 在同一个阻塞点上卡了 3 次以上迭代 → 终止该任务，附带更具体的上下文重新分配
- 任务消耗了超过 85% 的 token 预算却没有任何提交 → 暂停并报告
- 经过 2 轮反思仍无进展 → 上报给团队负责人

### 专职审查员团队成员

对于生产级的 agent 团队，增加一个只读的审查员 agent 可以在不降低吞吐量的前提下提升输出质量：

**设置**：
```
Reviewer brief:
- Model: Claude Opus 4.6 (for thoroughness)
- Tools available: lint, run tests, security-scan only — no file writes
- Trigger: automatically review on every TaskCompleted event
- Scope: the specific files changed in that task, not the full codebase
- Output: structured findings (blocking / non-blocking) added to shared task list
```

**比例**：每 3-4 个构建者配 1 个审查员。构建者更少时，审查员会成为瓶颈；构建者更多时，审查队列会堆积。

**为什么只读很重要**：拥有写入权限的审查员会开始自行修复问题，这会造成合并冲突，并破坏并行隔离的目的。

---

## 9. 故障排查

### 常见问题

#### 问题：agent 未派生

**症状**：
- agent 团队提示被接受，但没有创建团队成员
- 只有团队负责人会话在运行

**原因**：
1. 特性开关（feature flag）未正确设置
2. 模型不是 Opus 4.6（团队功能需要 Opus）
3. 任务复杂度不够（Claude 判定单个 agent 已足够）

**解决方案**：
```bash
# Verify flag
echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS  # Should output "1" or "true"

# Check settings
cat ~/.claude/settings.json | grep agentTeams  # Should be true

# Force model
/model opus

# Explicit request
"Spawn 3 agents for this task (team lead + 2 teammates)"
```

#### 问题：合并冲突过多

**症状**：
- agent 完成后出现大量 git 冲突
- 频繁需要手动解决

**原因**：
- 任务拆分不当（文件集合重叠）
- 写入密集型任务（多个 agent 修改共享文件）

**解决方案**：
```
Prevention:
1. Clear boundaries: Non-overlapping file assignments
2. Interface-first: Define contracts before implementation
3. Single-writer: One agent writes shared files, others read

Recovery:
1. Revert: git reset --hard before-agent-teams
2. Sequential: Re-implement with single agent
3. Human merge: Manually resolve conflicts (git mergetool)
```

#### 问题：token 成本高

**症状**：
- token 用量比预期高 3 倍以上
- 预算迅速耗尽

**原因**：
- 过度派生 agent（简单任务用了 3 个以上 agent）
- 长时间运行的会话（agent 处于空闲状态）
- 每个 agent 的上下文过大（1M tokens × 3）

**解决方案**：
```
Immediate:
1. Kill extra agents: Shift+Down, exit agent session
2. Reduce scope: Narrow task boundaries
3. Switch to single agent: /model sonnet (cheaper)

Long-term:
1. Cost monitoring: Track token usage per session
2. Lazy spawning: Only spawn when needed
3. Progressive escalation: Start small, scale up if needed
```

#### 问题：agent 卡住/挂起

**症状**：
- 一个 agent 完成了，其他 agent 仍长时间处理中
- 没有进度更新

**原因**：
- 任务分配不均衡（某个 agent 承担了 80% 的工作）
- agent 在等待依赖项（顺序耦合）
- git 协调中的 bug（罕见）

**解决方案**：
```bash
# Navigate to stuck agent
Shift+Down  # Switch to agent

# Check status
"What are you working on? Progress update?"

# Manual takeover if needed
"Stop current task, report findings so far"

# Kill and redistribute
Exit agent → Team lead redistributes task
```

#### 问题：各 agent 之间结果不一致

**症状**：
- Agent 1 说"没有问题"，Agent 2 却发现了 10 个 bug（同一个代码库）
- 相互冲突的建议

**原因**：
- 上下文窗口不同（agent 看到的文件不同）
- 指令含糊（agent 理解各异）
- 模型的随机性（输出具有随机性）

**解决方案**：
```
Prevention:
1. Explicit instructions: "All agents: Check for SQL injection"
2. Shared context: Point all agents to same reference docs
3. Validation: Human reviews all agent outputs

Recovery:
1. Reconciliation: "Compare Agent 1 and Agent 2 findings, resolve conflicts"
2. Third opinion: Spawn Agent 3 to arbitrate
3. Human decision: You choose which agent's recommendation to follow
```

### 导航问题

**找不到 agent 会话**：
```bash
# List all sessions
claude --list

# Filter for agent sessions
claude --list | grep agent

# Resume specific agent
claude --resume <session-id>
```

**搞不清哪个 agent 是哪个**：
```
Solution: Name agents explicitly in team lead prompt

Good:
"Spawn 3 agents:
- Agent Security: Check vulnerabilities
- Agent Performance: Profile bottlenecks
- Agent Tests: Write test suite"

Bad:
"Spawn 3 agents for this codebase review"
```

**tmux 导航无效**：
```bash
# Verify tmux session
tmux list-sessions

# Attach to session
tmux attach -t claude-agents

# Navigate
Ctrl+b, n  # Next window
Ctrl+b, p  # Previous window
```

### 性能优化

**协调缓慢**：
```bash
# Check git repo size
du -sh .git/  # If >1GB, consider cleanup

# Clean up git objects
git gc --aggressive --prune=now

# Use shallow clone for agents
git clone --depth 1 <repo>
```

**上下文加载延迟**：
```
# Reduce context per agent
"Agent 1: Only load src/backend/* files"
"Agent 2: Only load src/frontend/* files"

# Prune irrelevant files
echo "node_modules/" >> .gitignore
echo "dist/" >> .gitignore
```

---

## 9. 面向子智能体的迭代式检索

当子智能体缺乏完成任务所需的上下文时，默认的失败模式是：它会做出假设，并生成看似合理却实际错误的输出。这种输出看上去足够合理，能通过快速审查，但会在下游环节崩溃。

**这个模式**：给子智能体一个检索预算——在给出最终响应前，它们最多可以请求 N 个周期的额外上下文。三个周期既能覆盖大多数情况，又能限制成本和延迟。

### 结构

```
Cycle 1: Agent receives task + initial context
         → If confident: produce output
         → If uncertain: identify what's missing, request specific files or symbols

Cycle 2: Agent receives requested context
         → If confident: produce output
         → If still uncertain: one final targeted request

Cycle 3: Agent receives final context
         → Produce best output regardless of remaining uncertainty
         → Flag explicit assumptions made
```

### 该向子智能体传递什么

最常见的错误：只给子智能体讲了 WHAT（做什么）而没讲 WHY（为什么）。一个知道自己是在"为支付服务实现重试机制"的智能体，拥有的上下文能够省去多轮纠正：

```markdown
## Objective
[WHY this task exists — the problem being solved, the constraint being met]

## Task
[WHAT to do, specifically]

## Context
Files you have access to: [...]
Known constraints: [...]
What NOT to touch: [...]

## If you need more information
You may request up to 2 additional context cycles. Be specific:
- Name the exact files or symbols you need
- Explain why they're required to complete the task accurately
State explicitly: "I need [X] because [Y]" — not "I might need more context"

## Output format
[...]
```

### 何时应用

| 场景 | 使用迭代式检索？ |
|-----------|------------------------|
| 子智能体修改 1–2 个已知文件 | 否——直接提供这些文件 |
| 子智能体需要理解系统行为 | 是——它可能需要追踪调用图 |
| 子智能体做架构决策 | 是——始终如此 |
| 子智能体为现有代码编写测试 | 通常需要——它需要读取被测对象 |

开销是实实在在的（每个周期都消耗 token 和延迟）。把它用在错误假设代价高于检索代价的任务上——通常是任何触及接口、契约或公共 API 的工作。

> **致谢**：面向子智能体的迭代式检索模式来自 [Everything Claude Code](https://github.com/affaan-m/everything-claude-code)（Affaan Mustafa）。最多 3 周期的上限以及 WHY/WHAT 分离的做法记录在他们的长文指南中。

---

## 10. 来源

### Anthropic 官方来源

1. **[Introducing Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6)**
   Anthropic，2026 年 2 月
   Opus 4.6 及 agent teams 研究预览的官方公告

2. **[Building a C compiler with agent teams](https://www.anthropic.com/engineering/building-c-compiler)**
   Anthropic Engineering，2026 年 2 月
   技术深度剖析：基于 git 的协调、自主 C 编译器案例研究

3. **[2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)**
   Anthropic，2026 年 1 月
   生产指标：Fountain（快 50%）、CRED（速度提升 2 倍）

### 社区来源

4. **[Claude Opus 4.6 for Developers: Agent Teams, 1M Context](https://dev.to/thegdsks/claude-opus-46-for-developers-agent-teams-1m-context-and-what-actually-matters-4h8c)**
   dev.to，2026 年 2 月
   配置说明、工作流影响表、读/写权衡

5. **[The best way to do agentic development in 2026](https://dev.to/chand1012/the-best-way-to-do-agentic-development-in-2026-14mn)**
   dev.to，2026 年 1 月
   集成模式：Claude Code + 插件（Conductor、Superpowers、Context7）

### 社区工具

6. **[Claude Agent Teams UI](https://github.com/777genius/claude_agent_teams_ui)**
   用于管理 Claude Code agent teams 的开源桌面应用（Electron + React + TypeScript）。
   带实时任务追踪的看板、代码审查 diff、跨团队沟通、深度会话分析与上下文监控。100% 免费，本地运行。

### 实践者证言

7. **[Paul Rayner LinkedIn Post](https://www.linkedin.com/posts/thepaulrayner_this-is-wild-i-just-upgraded-claude-code-activity-7425635159678414850-MNyv)**
   Paul Rayner（Virtual Genius 首席执行官，EventStorming Handbook 作者），2026 年 2 月
   生产使用：3 个并发工作流（求职应用、业务运营、基础设施）

### 相关文档

- [Claude Code Releases](../core/claude-code-releases.md) —— v2.1.32、v2.1.33 发布说明
- [子智能体](#split-role-sub-agents) —— 单智能体任务委派
- [多实例工作流](#917-scaling-patterns-multi-instance-workflows) —— 手动并行协调
- [双实例模式](#alternative-pattern-dual-instance-planning-vertical-separation) —— 规划-执行拆分
- [AI 生态系统：Beads Framework](../ecosystem/ai-ecosystem.md#beads-framework) —— 替代编排方案（Gas Town）

---

## 反馈与贡献

**遇到问题？** 请反馈至 [Anthropic GitHub Issues](https://github.com/anthropics/claude-code/issues)

**有生产实践心得？** 在 [GitHub Discussions](https://github.com/anthropics/claude-code/discussions) 分享

**有疑问？** 到 [Dev With AI Community](https://www.devw.ai/)（1500+ 开发者，Slack）提问

---

## 高级编排模式

这些模式针对多智能体流水线在规模化时出现的失败模式：协调者自己做了太多工作、智能体在前置条件未满足时就贸然执行、以及流水线无法从运行中途的失败中恢复。

---

### 中心辐射式协调者（Hub-and-Spoke Coordinator）

中心辐射式模式将协调与执行分离。协调者智能体负责分解任务、选择子智能体、派发工作、监控结果并汇总输出。它自己不做任何领域工作——不做研究、不做分析、不做生成。正是这种分离使协调者可以在不同任务类型间复用。

```python
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class SubagentResult:
    agent_id: str
    task: str
    result: Any
    success: bool
    error: str | None = None

class ResearchCoordinator:
    def __init__(self, subagents: dict[str, Callable]):
        self.subagents = subagents  # name -> callable

    def run(self, research_question: str) -> dict:
        # Decompose into parallel subtasks
        subtasks = self.decompose(research_question)

        # Dispatch to appropriate subagents
        results = []
        for subtask in subtasks:
            agent_name = self.select_agent(subtask)
            if agent_name not in self.subagents:
                results.append(SubagentResult(
                    agent_id=agent_name, task=subtask,
                    result=None, success=False,
                    error=f"No agent available for: {agent_name}"
                ))
                continue

            try:
                result = self.subagents[agent_name](subtask)
                results.append(SubagentResult(
                    agent_id=agent_name, task=subtask,
                    result=result, success=True
                ))
            except Exception as e:
                results.append(SubagentResult(
                    agent_id=agent_name, task=subtask,
                    result=None, success=False, error=str(e)
                ))

        # Aggregate — coordinator's only domain responsibility
        return self.aggregate(research_question, results)

    def decompose(self, question: str) -> list[str]:
        # Returns subtasks — coordinator decides structure, not domain content
        raise NotImplementedError

    def select_agent(self, subtask: str) -> str:
        # Routing logic — pattern matching or LLM-based selection
        raise NotImplementedError

    def aggregate(self, original_question: str, results: list[SubagentResult]) -> dict:
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]

        return {
            "question": original_question,
            "findings": [r.result for r in successful],
            "coverage": len(successful) / len(results) if results else 0.0,
            "failures": [{"task": r.task, "error": r.error} for r in failed]
        }
```

协调者从不接触结果的内容，只负责路由、计数，并把它们交给汇总步骤。如果你发现协调者代码中包含分析逻辑、业务规则或领域专属处理，那些逻辑应当归属于某个子智能体。

---

### 程序化前置条件（Programmatic Prerequisites）

前置条件检查应当是确定性的关卡，而非提示词指令。告诉模型"在继续之前确保数据已就绪"并不是前置条件，而只是一条建议。程序化前置条件是一种状态检查，它要么允许执行继续进行，要么返回一个结构化错误。

**模式 1：状态标志关卡**

```python
@dataclass
class PipelineState:
    data_ingested: bool = False
    schema_validated: bool = False
    permissions_checked: bool = False

    def can_proceed_to_analysis(self) -> tuple[bool, list[str]]:
        missing = []
        if not self.data_ingested:
            missing.append("data_ingested")
        if not self.schema_validated:
            missing.append("schema_validated")
        if not self.permissions_checked:
            missing.append("permissions_checked")
        return len(missing) == 0, missing

def run_analysis_phase(state: PipelineState, data: dict) -> dict:
    can_proceed, missing = state.can_proceed_to_analysis()
    if not can_proceed:
        return {
            "status": "blocked",
            "reason": f"Prerequisites not met: {', '.join(missing)}",
            "required": missing
        }

    # Proceed with analysis — all prerequisites confirmed
    return perform_analysis(data)
```

**模式 2：基于阶段的派发**

对于具有顺序阶段的流水线，编排器根据已完成的阶段来派发，而不是根据已经过的时间或轮次数：

```python
from enum import Enum

class PipelinePhase(Enum):
    INIT = "init"
    INGESTION = "ingestion"
    VALIDATION = "validation"
    PROCESSING = "processing"
    COMPLETE = "complete"
    FAILED = "failed"

@dataclass
class PipelineContext:
    phase: PipelinePhase = PipelinePhase.INIT
    phase_results: dict = None

    def __post_init__(self):
        if self.phase_results is None:
            self.phase_results = {}

def dispatch_next_phase(context: PipelineContext, agents: dict) -> PipelineContext:
    next_phase_map = {
        PipelinePhase.INIT: PipelinePhase.INGESTION,
        PipelinePhase.INGESTION: PipelinePhase.VALIDATION,
        PipelinePhase.VALIDATION: PipelinePhase.PROCESSING,
        PipelinePhase.PROCESSING: PipelinePhase.COMPLETE
    }

    next_phase = next_phase_map.get(context.phase)
    if next_phase is None:
        return context

    agent = agents.get(next_phase.value)
    if agent is None:
        context.phase = PipelinePhase.FAILED
        return context

    try:
        result = agent(context.phase_results)
        context.phase_results[next_phase.value] = result
        context.phase = next_phase
    except Exception as e:
        context.phase = PipelinePhase.FAILED
        context.phase_results["error"] = str(e)

    return context
```

---

### 动态子智能体选择（Dynamic Subagent Selection）

与其硬编码哪个智能体处理哪类任务，协调者可以根据任务特征动态选择子智能体。这让同一个协调者无需改动代码即可处理新的任务类型。

```python
@dataclass
class AgentCapability:
    name: str
    handles: list[str]  # task type keywords
    cost: float          # relative cost (1.0 = baseline)
    latency: float       # expected seconds

class DynamicSelector:
    def __init__(self, agents: list[AgentCapability]):
        self.agents = agents

    def select(self, task: str, budget_tier: str = "standard") -> str:
        candidates = [
            a for a in self.agents
            if any(keyword in task.lower() for keyword in a.handles)
        ]

        if not candidates:
            return "general"  # fallback agent

        if budget_tier == "economy":
            # Cheapest capable agent
            return min(candidates, key=lambda a: a.cost).name
        elif budget_tier == "performance":
            # Fastest capable agent
            return min(candidates, key=lambda a: a.latency).name
        else:
            # Balanced: cheapest among the fast agents
            fast = [a for a in candidates if a.latency < 10.0]
            pool = fast if fast else candidates
            return min(pool, key=lambda a: a.cost).name
```

---

### 研究空间划分（Research Space Partitioning）

当多个智能体研究同一个宽泛主题时，除非协调者明确划分搜索空间，否则它们会返回相互重叠的结果。重叠既浪费预算，又使汇总更加困难。

```python
def partition_research_space(
    topic: str,
    num_agents: int,
    partition_dimensions: list[str]
) -> list[dict]:
    """
    Divide a research topic into non-overlapping partitions.
    Each agent receives a partition with explicit scope boundaries.
    """
    if len(partition_dimensions) >= num_agents:
        dimensions = partition_dimensions[:num_agents]
    else:
        # Create additional partitions if not enough thematic dimensions
        dimensions = partition_dimensions + [
            f"recent_{i}" for i in range(num_agents - len(partition_dimensions))
        ]

    return [
        {
            "agent_id": f"researcher_{i}",
            "topic": topic,
            "scope": dimension,
            "exclusions": [d for j, d in enumerate(dimensions) if j != i],
            "instruction": (
                f"Research '{topic}' focusing exclusively on '{dimension}'. "
                f"Do NOT cover: {', '.join(dimensions[:i] + dimensions[i+1:])}. "
                f"This constraint prevents duplication with parallel researchers."
            )
        }
        for i, dimension in enumerate(dimensions)
    ]

# Example: 3-agent research on "vector database performance"
partitions = partition_research_space(
    topic="vector database performance",
    num_agents=3,
    partition_dimensions=["indexing algorithms", "query optimization", "hardware scaling"]
)
```

---

### 崩溃恢复清单（Crash Recovery Manifest）

长时间运行的智能体流水线（数小时、通宵作业）需要崩溃恢复机制。清单会在阶段边界处记录已完成的工作，以便重启时能从上一个检查点继续，而不是从头开始。

```python
import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime

@dataclass
class PipelineManifest:
    pipeline_id: str
    created_at: str
    task_description: str
    total_items: int
    completed_items: list[str] = field(default_factory=list)
    failed_items: list[dict] = field(default_factory=list)
    phase_checkpoints: dict = field(default_factory=dict)
    status: str = "in_progress"  # "in_progress" | "complete" | "failed"

    def save(self, path: str):
        with open(path, "w") as f:
            json.dump(asdict(self), f, indent=2)

    @classmethod
    def load(cls, path: str) -> "PipelineManifest":
        with open(path) as f:
            data = json.load(f)
        return cls(**data)

    def checkpoint(self, phase: str, result: dict, manifest_path: str):
        self.phase_checkpoints[phase] = {
            "completed_at": datetime.utcnow().isoformat(),
            "result_summary": result.get("summary", "")
        }
        self.save(manifest_path)

    def mark_item_complete(self, item_id: str, manifest_path: str):
        self.completed_items.append(item_id)
        self.save(manifest_path)  # write after every item

class RecoverableOrchestrator:
    def __init__(self, manifest_path: str):
        self.manifest_path = manifest_path

    def run(self, pipeline_id: str, items: list[str], processor) -> PipelineManifest:
        # Load or create manifest
        if os.path.exists(self.manifest_path):
            manifest = PipelineManifest.load(self.manifest_path)
            print(f"Resuming: {len(manifest.completed_items)}/{manifest.total_items} done")
        else:
            manifest = PipelineManifest(
                pipeline_id=pipeline_id,
                created_at=datetime.utcnow().isoformat(),
                task_description=f"Processing {len(items)} items",
                total_items=len(items)
            )

        for item_id in items:
            if item_id in manifest.completed_items:
                continue  # skip completed items

            try:
                processor(item_id)
                manifest.mark_item_complete(item_id, self.manifest_path)
            except Exception as e:
                manifest.failed_items.append({"id": item_id, "error": str(e)})
                manifest.save(self.manifest_path)

        manifest.status = "complete" if not manifest.failed_items else "partial"
        manifest.save(self.manifest_path)
        return manifest
```

应在阶段边界处设置检查点，而不仅仅在任务完成时。对于一个 3 阶段的流水线（摄取、分析、报告），分析中途崩溃应当从分析阶段的起点恢复，而非从摄取阶段的起点重来。

---

### 迭代式精炼循环

某些任务需要多轮处理才能达到可接受的质量。驱动迭代的是协调者（coordinator），而非 subagent。这种职责分离意味着 subagent 保持无状态，而由协调者控制停止条件。

```python
@dataclass
class RefinementState:
    iteration: int
    current_output: str
    quality_score: float
    feedback: str | None
    max_iterations: int = 5
    target_quality: float = 0.85

    def should_continue(self) -> bool:
        return (
            self.iteration < self.max_iterations
            and self.quality_score < self.target_quality
        )

def iterative_refine(
    initial_task: str,
    generator_fn,
    evaluator_fn,
    max_iterations: int = 5
) -> RefinementState:
    state = RefinementState(
        iteration=0,
        current_output="",
        quality_score=0.0,
        feedback=None,
        max_iterations=max_iterations
    )

    while True:
        # Generate (or refine based on feedback)
        if state.iteration == 0:
            state.current_output = generator_fn(initial_task)
        else:
            state.current_output = generator_fn(
                f"{initial_task}\n\nPrevious attempt:\n{state.current_output}\n\n"
                f"Feedback to address:\n{state.feedback}"
            )

        # Evaluate — separate pass with fresh context
        evaluation = evaluator_fn(state.current_output, initial_task)
        state.quality_score = evaluation["score"]
        state.feedback = evaluation["feedback"]
        state.iteration += 1

        if not state.should_continue():
            break

    return state
```

停止条件至关重要。"一直做到完美为止"并不是一个停止条件。请将 `target_quality` 定义为基于验证集的数值阈值，将 `max_iterations` 定义为硬性预算上限。如果二者缺一，循环要么过早终止，要么无限运行。

---

### 窄范围任务分解

宽泛的任务分解会产生成功标准不明确的 subagent。在派发任务前，使用 SPEC 测试来验证每个子任务：

**子任务的 SPEC 测试：**
- **S**pecific（具体）：任务描述对产出内容不留任何歧义
- **P**rogrammatically evaluable（可程序化评估）：无需人工判断即可检查成功或失败
- **E**xplicit scope（明确范围）：哪些在范围内、哪些在范围外都已明确说明，而非暗示
- **C**onstrained（受约束）：任务有明确定义的输出格式、长度或 schema

未能通过 SPEC 测试的子任务，应在派发前进一步分解或予以澄清。

| 子任务 | 通过 SPEC？ | 问题 |
|---|---|---|
| "研究这个主题" | 否 | 不具体，不可程序化评估 |
| "找出 3 篇 2022-2024 年间发表的关于向量索引的同行评审论文" | 是 | 具体、可计数、有范围、格式受约束 |
| "分析数据" | 否 | 不具体，无输出 schema |
| "从发票 001-050 中提取供应商名称，以 JSON 数组形式输出" | 是 | 具体、受 schema 约束、有范围 |
| "写点好东西" | 否 | 无质量标准，不可评估 |
| "写一份 150 字的执行摘要，包含：问题、方法、结果" | 是 | 字数、结构和内容均已指定 |

当一个子任务无法以通过 SPEC 测试的方式表述时，这通常意味着协调者尚未掌握足够的信息来分解这部分工作。请先收集更多上下文，再做进一步分解。

---

*Version 1.0.0 | Created: 2026-02-07 | Agent Teams (v2.1.32+, Experimental)*
