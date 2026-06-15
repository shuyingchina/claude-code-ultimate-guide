---
title: "Agent Teams 快速上手指南"
description: "实用的 5 分钟配置指南，附带可直接复制粘贴的 agent teams 模式"
tags: [workflow, agents, tutorial]
---

# Agent Teams 快速上手指南

> **在你的项目中使用 agent teams 的实用指南**
> **阅读时间**：8-10 分钟 | **完整文档**：[Agent Teams](./agent-teams.md)（30 分钟概览）

## 这是什么？

你知道 agent teams 的存在。你也读过相关理论。但**你究竟应该在什么时候在自己的项目里使用它们？**

本指南为你提供：
- ✅ **5 分钟配置**（环境 → 首次测试）
- ✅ **4 个可复制粘贴的模式**，面向真实项目（Guide + RTK）
- ✅ **决策矩阵**（什么时候该用，什么时候不该用）
- ✅ **衡量 ROI 的指标**
- ✅ **避免浪费的危险信号**

**如果你想看理论可以跳过本文**：直接阅读 [Agent Teams 完整文档](./agent-teams.md)。

---

## 目录

1. [5 分钟配置](#1-5-minute-setup)
2. [面向你的项目的模式](#2-patterns-for-your-projects)
   - 2.1 [Claude Code Guide - 发布前评审](#21-claude-code-guide---pre-release-review)
   - 2.2 [Claude Code Guide - Landing 同步](#22-claude-code-guide---landing-sync)
   - 2.3 [Claude Code Guide - 多文件文档更新](#23-claude-code-guide---multi-file-doc-update)
   - 2.4 [RTK - 安全 PR 评审](#24-rtk---security-pr-review)
3. [决策矩阵：何时使用](#3-decision-matrix-when-to-use)
4. [极简工作流模板](#4-minimal-workflow-template)
5. [成功指标](#5-success-metrics)
6. [局限与危险信号](#6-limitations--red-flags)

---

## 1. 5 分钟配置

### 步骤 1：前提条件检查

```bash
# Check Claude Code version (v2.1.32+ required)
claude --version

# Check model availability
claude
> /model opus
# Should show: "Model changed to opus (claude-opus-4-6-20250624)"
```

**最低要求**：
- Claude Code v2.1.32+
- Opus 4.6 模型
- Git 仓库（agent teams 使用 git 进行协调）

### 步骤 2：启用功能

```bash
# Set environment variable (add to ~/.bashrc or ~/.zshrc for persistence)
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# Launch Claude Code
claude
```

### 步骤 3：验证

```
> Are agent teams enabled?
```

**预期回复**：
```
Yes, agent teams are enabled in this session. I can create teams
of agents to work in parallel on complex tasks using:
- Multi-agent coordination
- Git-based task claiming
- Autonomous team coordination
```

**如果未启用**：检查环境变量是否已设置（`echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`）。

### 步骤 4：首次测试（2 个 agent）

```
> Create a simple test team to analyze this README:
> - Agent 1: Check structure (sections, TOC, badges)
> - Agent 2: Check content quality (clarity, examples, completeness)
```

**会发生什么**：
1. Claude 派生出 2 个 agent（你会看到 "Creating team..." 消息）
2. 两个 agent 并行工作（你可能会看到 "Idle" 消息——这是正常的）
3. Claude 呈现整合后的发现（趋同点 + 各自独有的洞见）

**导航**：
- `Shift+Down`：在各个队友的输出之间循环切换（进程内模式）
- 主视图：整合后的综合结论

**耗时**：简单的 2-agent 任务约 1-2 分钟。

---

## 2. 面向你的项目的模式

### 2.1 Claude Code Guide - 发布前评审

**使用场景**：在版本号提升前进行系统化审计，以捕捉一致性问题（链接失效、计数不同步、版本号错误）

**触发时机**：每次执行 `/release` 命令之前

**耗时**：3-5 分钟

**团队构成**：
```
Team: pre-release-audit (3 agents)
├─ accuracy-auditor → Verify claims, stats, versions, external links
├─ consistency-checker → Check template count, eval count, guide lines match across files
└─ breaking-checker → Identify breaking changes vs last release
```

**可复制粘贴的提示词**：
```
> Create a pre-release audit team:
> - Accuracy: Check all claims, stats, version numbers, external links in CHANGELOG.md, README.md, and guide/ultimate-guide.md
> - Consistency: Verify template count (count examples/ files), eval count (count docs/resource-evaluations/ files), guide lines (wc -l guide/ultimate-guide.md) match across README.md, guide/cheatsheet.md, machine-readable/reference.yaml
> - Breaking: Identify breaking changes vs v3.23.0 by analyzing CHANGELOG.md [Unreleased] section
```

**ROI**：能捕捉到诸如以下的 bug：
- LinkedIn URL 损坏（在今天的真实审计中被捕捉到）
- guide/landing 之间的不同步（模板计数）
- 多个文件中的版本号错误
- 失效的外部链接

**何时跳过**：简单的拼写修正（不涉及版本/计数/链接变更）。

**真实示例**（2026-02-08 的测试）：
```
Findings:
- Accuracy: 1 critical (LinkedIn URL malformed), 3 warnings (external links to verify)
- Consistency: 2 criticals (template count mismatch README vs landing, line numbers outdated in reference.yaml)
- Breaking: 0 breaking changes detected vs v3.23.0 (clean release)

Convergence: 2 agents flagged template count issue (high confidence)
Time: 4 min 12 sec
Verdict: ✅ High value, found 3 criticals that would've shipped
```

---

### 2.2 Claude Code Guide - Landing 同步

**使用场景**：验证 guide/landing 的同步状态（版本、计数、内容），无需运行手动脚本

**触发时机**：在对 guide 进行重大修改之后（版本提升、新增模板、FAQ 变更）

**耗时**：2-3 分钟

**团队构成**：
```
Team: landing-sync (2 agents)
├─ guide-scanner → Extract version, template count, eval count, guide lines, FAQ content
└─ landing-scanner → Compare with index.html, examples.html, check sync status
```

**可复制粘贴的提示词**：
```
> Validate guide/landing synchronization:
> - Guide scanner: Extract version from VERSION file, template count (find examples/ -type f | wc -l), eval count (find docs/resource-evaluations/ -name "*.md" | wc -l), guide lines (wc -l guide/ultimate-guide.md), FAQ entries from README.md
> - Landing scanner: Check /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing/index.html and examples.html for version in footer+FAQ, template count in badges, eval count, guide lines approximation (~9800+)
>
> Report: Synced ✅ / Mismatches with line numbers
```

**ROI**：
- 零不同步内容流入生产环境
- 避免手动执行 `./scripts/check-landing-sync.sh`
- 比脚本更快（2 分钟 vs 运行脚本 + 修复需 5 分钟）

**何时跳过**：纯代码变更（不影响文档/计数）。

**成功标准**：
```
✅ All synced: Version, template count, eval count match
⚠️ Mismatch: Specific line numbers in index.html to fix
```

---

### 2.3 Claude Code Guide - 多文件文档更新

**使用场景**：在多个文件（ultimate-guide.md、reference.yaml、README.md）中添加新功能文档，并保持交叉引用的一致性

**触发时机**：新增功能章节（>50 行）、破坏性变更、架构更新

**耗时**：5-8 分钟

**团队构成**：
```
Team: doc-update (3 agents)
├─ content-writer → Write main section in ultimate-guide.md with examples
├─ index-updater → Update TOC, reference.yaml entries, README navigation
└─ consistency-checker → Verify cross-references, line numbers, anchors work
```

**可复制粘贴的提示词**：
```
> Update documentation for new "[FEATURE NAME]" feature:
> - Content Scope: Write section [X.Y] in guide/ultimate-guide.md with:
>   - Overview (what/why/when)
>   - 2-3 concrete examples
>   - Best practices + gotchas
>   - Links to related sections
>   Context: guide/ultimate-guide.md section [X.Y] only
> - Index Scope: Update:
>   - guide/ultimate-guide.md TOC (add section [X.Y])
>   - machine-readable/reference.yaml (add entry with line numbers)
>   - README.md navigation (add link if major feature)
>   Context: Index files only (TOC, reference.yaml, README.md)
> - Consistency Scope: Verify:
>   - All cross-references resolve correctly
>   - Line numbers in reference.yaml match actual content
>   - Anchors in README point to correct sections
>   - No broken internal links
>   Context: All modified files for cross-reference validation
```

**ROI**：
- 零链接失效（consistency-checker 会全部捕捉）
- 比顺序执行快 60%（编写 → 建索引 → 验证）
- 并行工作减少等待时间

**何时跳过**：单文件编辑（<50 行），无需交叉引用。

**真实示例**（新增 Agent Teams 章节）：
```
Task: Add "Agent Teams" as section 9.20 (300 lines)
Files touched: 3 (ultimate-guide.md, reference.yaml, README.md)

Sequential estimate: 12-15 min (write → index → verify)
Agent Teams: 7 min 30 sec (3 agents parallel)
Savings: 40% time + zero manual cross-ref checks
```

---

### 2.4 RTK - 安全 PR 评审

**使用场景**：评审外部贡献者的 PR，检查安全问题（注入、token 泄露）、Rust 惯用法以及性能

**触发时机**：非核心贡献者提交的 PR；PR 涉及敏感代码（认证、外部命令、正则表达式）

**耗时**：5-8 分钟

**团队构成**：
```
Team: security-pr-review (3 agents)
├─ rust-expert → Check ownership patterns, error handling (anyhow/thiserror), idiomatic code
├─ security-auditor → Scan for injection risks, token leaks, input sanitization
└─ perf-analyzer → Review allocations, async patterns, compiled regex
```

**可复制粘贴的提示词**：
```
> Review PR #[NUMBER] with scope-focused analysis:
> - Rust Scope: Check:
>   - Ownership patterns (prefer &str over String, minimize clones)
>   - Error handling (anyhow::Result with .context(), no unwrap outside tests)
>   - Idiomatic code (impl after type, #[cfg(test)] mod tests)
>   - Clippy compliance (zero warnings)
>   Context: All modified .rs files
> - Security Scope: Scan for:
>   - Command injection (shell escapes, argument sanitization)
>   - Token/credential leaks (hardcoded secrets, logs, error messages)
>   - Input sanitization (path traversal, regex DoS)
>   - File operations (path validation, permissions)
>   Context: Input handling, auth, file I/O code
> - Performance Scope: Review:
>   - Unnecessary allocations (String::from vs &str)
>   - Async patterns (spawn_blocking for CPU-bound work)
>   - Compiled regex (lazy_static! for hot paths)
>   - Algorithm complexity (O(n) vs O(n²))
>   Context: Hot paths, loops, async functions
```

**ROI**：
- 盲点检测：Security + Rust + Perf = 单人评审者会遗漏的领域
- 一致的评审质量（不依赖评审者的心情/专注度）
- 比顺序执行更快（3 个 agent 并行 vs 三轮评审）

**何时跳过**：来自可信贡献者的内部 PR、琐碎变更（仅文档、注释、测试）。

**成功标准**：
```
✅ Convergence: 2+ agents flag same critical issue (high confidence)
✅ Unique insights: Each agent finds domain-specific issues (Rust/Security/Perf)
❌ False positives: <20% of findings are invalid
```

**真实示例**（假设的外部 PR）：
```
PR: Add new git filter command
Agents findings:
- Rust: 3 issues (unwrap in production code, missing .context(), non-idiomatic error handling)
- Security: 2 criticals (shell injection via user input, token leak in error message)
- Perf: 1 issue (regex compiled on every call, not lazy_static)

Convergence: Security + Rust both flagged missing input sanitization (high confidence)
Time: 6 min 40 sec
Verdict: ✅ Critical security issues caught, PR requires revision
```

---

## 3. 决策矩阵：何时使用

| 场景 | Agent Teams？ | 原因 |
|-----------|---------------|--------|
| **发布前评审（指南）** | ✅ YES | 多层审计（准确性 + 一致性 + 破坏性变更）需要并行视角 |
| **简单的拼写修正** | ❌ NO | 杀鸡用牛刀，1 个 agent = 10 秒，3 个 agent = 成本膨胀 |
| **外部 PR（RTK）** | ✅ YES | 安全 + Rust + 性能 = 盲点检测，高风险评审 |
| **多文件文档更新（指南）** | ✅ YES | 内容 + 索引 + 一致性 = 零失效链接，并行工作 |
| **Landing 同步检查** | ⚠️ MAYBE | 怀疑失同步时用 agent teams，否则 `./scripts/check-landing-sync.sh` 更快 |
| **CHANGELOG 更新** | ❌ NO | 顺序任务（线性写作），无并行化收益 |
| **单文件编辑（RTK）** | ❌ NO | 无需协调，顺序执行即可 |
| **小幅 README 调整（<50 行）** | ❌ NO | 无交叉引用，无复杂度，单 agent 更快 |
| **架构设计** | ✅ YES | 多重视角（前端、后端、基础设施、安全）能揭示盲点 |
| **缺陷调查** | ⚠️ MAYBE | 简单缺陷 → NO，复杂的多组件故障 → YES |

### 经验法则

**在以下情况使用 Agent Teams**：
- ✅ 你会自然地想到"我应该检查 X、Y 和 Z"
- ✅ 高风险（生产发布、外部贡献者、安全敏感）
- ✅ 需要多范围分析（Rust 范围 + 安全范围 + 性能范围）
- ✅ 跨文件一致性很重要（链接、计数、版本同步）
- ✅ 可以并行工作（独立任务，无顺序依赖）

**在以下情况不要使用 Agent Teams**：
- ❌ 简单任务（<5 个文件，<100 行，1 个领域）
- ❌ 顺序工作流（步骤 B 依赖步骤 A 的结果）
- ❌ 预算紧张（3 倍 token，留给高价值任务）
- ❌ 写入密集（对相同文件的大量编辑 = 合并冲突）

---

## 4. 最小工作流模板

### Bash 模板（可复用）

```bash
# 1. Setup (once per session)
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# 2. Launch Claude
claude

# 3. Create team (prompt template)
> Create a team to [TASK]:
> - Agent 1 ([SCOPE/CONTEXT]): [SPECIFIC MISSION]
> - Agent 2 ([SCOPE/CONTEXT]): [SPECIFIC MISSION]
> - Agent 3 ([SCOPE/CONTEXT]): [SPECIFIC MISSION]
>
> [FILES/DIRECTORIES TO ANALYZE]

# 4. Observe (optional)
# Shift+Down to cycle through teammate outputs (in-process mode)

# 5. Synthesis
# Claude presents consolidated findings automatically

# 6. Act
# Fix critical findings, skip minor ones
```

### 示例提示词（可直接复制粘贴）

#### 发布前指南审计

```
> Create a pre-release audit team:
> - Accuracy: Check all claims, stats, version numbers, external links in CHANGELOG.md, README.md, and guide/ultimate-guide.md
> - Consistency: Verify template count (count examples/ files), eval count (count docs/resource-evaluations/ files), guide lines (wc -l guide/ultimate-guide.md) match across README.md, guide/cheatsheet.md, machine-readable/reference.yaml
> - Breaking: Identify breaking changes vs v3.23.0 by analyzing CHANGELOG.md [Unreleased] section
```

#### 安全 PR 评审（RTK）

```
> Review PR #42 with scope-focused analysis:
> - Rust Scope: Check ownership patterns, error handling (anyhow/thiserror), idiomatic code in modified files (context: src/**/*.rs)
> - Security Scope: Scan for injection risks, token leaks, input sanitization (context: auth, input handling code)
> - Performance Scope: Review allocations, async patterns, compiled regex (context: hot paths, loops)
```

#### 多文件文档更新

```
> Update documentation for new "Agent Teams Quick Start" feature:
> - Content Scope: Write guide/workflows/agent-teams-quick-start.md with overview, 4 patterns, decision matrix, metrics
> - Index Scope: Update guide/ultimate-guide.md (add reference section 9.20), machine-readable/reference.yaml (add entry), CHANGELOG.md (add "Added" entry)
> - Consistency Scope: Verify all cross-refs work, line numbers match, no broken links (context: all modified files)
```

#### Landing 同步校验

```
> Validate guide/landing synchronization:
> - Guide scanner: Extract version from VERSION file, template count (find examples/ -type f | wc -l), eval count (find docs/resource-evaluations/ -name "*.md" | wc -l), guide lines (wc -l guide/ultimate-guide.md)
> - Landing scanner: Check /Users/florianbruniaux/Sites/perso/claude-code-ultimate-guide-landing/index.html and examples.html for version, counts, guide lines approximation
```

---

## 5. 成功指标

### 如何衡量 Agent Teams 的 ROI

| 指标 | 目标 | 如何衡量 |
|--------|--------|----------------|
| **收敛率** | >50% | 被 2 个以上 agent 标记的发现数 / 总发现数。高收敛 = 高置信度。 |
| **独特洞察** | 每个 agent ≥1 | 每个 agent 必须在其领域内至少发现 1 个独特问题。若某 agent 发现 0 个独特问题 = 浪费 token。 |
| **误报率** | <20% | 无效发现数 / 总发现数。误报过多 = 提示词质量差。 |
| **节省时间** | 60-70% | 对比 agent teams 耗时与顺序执行（按 3 个任务估算为单 agent 耗时的 3 倍）。 |
| **缺陷捕获率** | >80% | agent 发现的关键缺陷数 / 上线后发现的缺陷总数。高 = 有效预防。 |

### 真实示例：发布前评审测试（2026-02-08）

```
Task: Pre-release audit for v3.23.1
Agents: 3 (accuracy-auditor, consistency-checker, breaking-checker)
Duration: 4 min 12 sec

Findings (raw): 45 total
├─ Accuracy: 12 (1 critical: LinkedIn URL malformed, 11 warnings)
├─ Consistency: 18 (2 criticals: template count desync, line numbers outdated)
└─ Breaking: 15 (0 breaking changes, 15 informational notes)

Findings (deduplicated): ~30 unique issues

Convergence analysis:
├─ High confidence (2-3 agents): 4 issues
│   ├─ Template count mismatch (consistency + accuracy)
│   ├─ Line numbers outdated (consistency + accuracy)
│   ├─ External link verification needed (accuracy + breaking)
│   └─ Version sync across files (all 3 agents)
└─ Unique insights:
    ├─ Accuracy: LinkedIn URL corruption (only this agent caught it)
    ├─ Consistency: TOC structure deviation (only this agent)
    └─ Breaking: Changelog format improvement suggestion (only this agent)

Metrics:
├─ Convergence rate: 4/30 = 13% (lower than target, but 4 criticals flagged by multiple agents = high confidence on what matters)
├─ Unique insights: 3/3 agents = 100% (each agent found unique issues in their domain)
├─ False positive rate: 2/30 = 6.6% (below 20% target ✅)
├─ Time saving: 4 min vs estimated 12 min sequential = 66% savings ✅
├─ Bug catch rate: 3 critical bugs caught that would've shipped = prevented production issues ✅

Verdict: ✅ High value for pre-release audits
```

### 如何追踪你的指标

**在每次 agent teams 任务之后**：

1. **统计发现数**：记录每个 agent 的原始发现数，然后去重
2. **标记收敛**：哪些问题被 2 个以上 agent 标记？
3. **检查独特洞察**：每个 agent 是否至少发现 1 个领域专属问题？
4. **核实误报**：有多少发现是无效的／噪声？
5. **时间对比**：agent teams 耗时与估算的顺序执行耗时
6. **上线后验证**：agent teams 是否捕获了本会上线的缺陷？

**保留日志**（项目文档中的 Markdown 表格）：

```markdown
| Date | Task | Agents | Duration | Findings | Convergence | Unique | False+ | Time Saved | Bugs Caught |
|------|------|--------|----------|----------|-------------|--------|--------|------------|-------------|
| 2026-02-08 | Pre-release v3.23.1 | 3 | 4m12s | 30 | 13% (4 critical) | 3/3 | 6.6% | 66% | 3 |
```

**若指标未达标，调整提示词**：
- 收敛率低（<30%）→ 范围过窄，让上下文边界有更多重叠
- 无独特洞察 → 范围过于相似，让分析角度更多样化
- 误报率高（>20%）→ 提示词过于模糊，添加具体标准

---

## 6. 局限与警示信号

### Agent Teams 不能做什么

| 局限 | 含义 | 缓解措施 |
|------------|---------------|-----------|
| **3 倍 token** | 每个 agent = 一次独立的模型调用 = 3 倍成本 | 留给高风险任务（发布前、安全 PR，而非拼写修正） |
| **空闲刷屏** | agent 在协调期间会显示 "Idle" 消息 | 正常行为，不是缺陷，忽略刷屏即可 |
| **实验性** | 研究预览 = 不保证稳定性 | 预期会有缺陷，不要在生产关键工作流中依赖 agent teams |
| **协调开销** | 最多 3-5 个 agent，而非 10 个（协调复杂度会增长） | 坚持使用 2-4 个 agent，避免"10 人团队"式的提示词 |
| **上下文隔离** | agent 看不到彼此的发现（独立工作） | Claude 会综合各项发现，但 agent 无法在任务进行中基于彼此的工作展开 |

### 警示信号：何时不要使用

❌ **简单任务**（<5 个文件，<100 行，1 个领域）
- 示例：修正 README.md 中的拼写错误
- 为何避免：为一个 10 秒的任务花费 3 倍 token = 浪费

❌ **顺序工作流**（步骤 B 依赖步骤 A 的结果）
- 示例：实现功能 → 编写测试 → 部署
- 为何避免：agent 并行工作，无法处理依赖关系

❌ **预算紧张**（3 倍 token，需优化成本）
- 示例：API 额度有限的个人项目
- 为何避免：agent teams = 高风险任务的奢侈品，而非日常工作流

❌ **写入密集**（对相同文件的大量编辑）
- 示例：重构整个代码库结构
- 为何避免：合并冲突、协调开销、agent 互相干扰

❌ **低风险评审**（内部 PR、可信贡献者、简单变更）
- 示例：团队成员修复一个小缺陷
- 为何避免：杀鸡用牛刀，单 agent 评审更快 + 更便宜

### 何时你应该使用（尽管有成本）

✅ **高风险**（生产发布、安全敏感、外部贡献者）
✅ **多领域**（Rust + 安全 + 性能 = 盲点）
✅ **适合并行**（独立任务，无顺序依赖）
✅ **一致性关键**（跨文件同步、计数、版本）
✅ **学习机会**（理解盲点，改进提示词）

---

## 总结：快速参考

### 设置（一次性 5 分钟）

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude
> Are agent teams enabled?  # Verify
```

### 何时使用（决策规则）

**用，如果**：
- 高风险 + 多领域 + 适合并行

**不用，如果**：
- 简单任务 + 顺序执行 + 预算紧张

### 模式（4 个开箱即用）

1. **发布前评审**（Guide）→ 准确性 + 一致性 + 破坏性变更
2. **Landing 同步**（Guide）→ Guide 扫描器 + Landing 扫描器
3. **多文件文档更新**（Guide）→ 内容 + 索引 + 一致性
4. **安全 PR 评审**（RTK）→ Rust + 安全 + 性能

### 指标（追踪 ROI）

- 收敛度：>50%（被 2 个以上 agent 发现的问题）
- 独特洞见：每个 agent ≥1
- 误报：<20%
- 时间节省：60-70%
- 缺陷捕获：>80%

### 警示信号（避免浪费）

- ❌ 简单任务（<5 个文件）
- ❌ 顺序工作流
- ❌ 预算紧张
- ❌ 写操作密集（合并冲突）

---

## 后续步骤

1. **尝试第一次测试**（5 分钟设置 + 简单的 2-agent 任务）
2. **从你的项目中挑选 1 个模式**（Guide 或 RTK）
3. **测量指标**（收敛度、独特洞见、节省的时间）
4. **根据结果调整提示词**
5. **阅读完整文档**了解高级模式：[Agent Teams](./agent-teams.md)

**有疑问？** 查看[完整文档](./agent-teams.md)了解：
- 架构深度剖析（git 协调如何工作）
- 高级用例（15 个以上生产场景）
- 故障排查（常见问题 + 解决方案）
- 最佳实践（团队规模、提示词设计、冲突解决）
