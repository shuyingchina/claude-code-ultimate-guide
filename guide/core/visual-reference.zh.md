---
title: "Claude Code — 可视化参考"
description: "用 ASCII 图表将 Claude Code 的核心概念整合到一个可视化概览中"
tags: [reference, architecture, cheatsheet]
---

# Claude Code — 可视化参考

所有图表汇聚一处。快速可视化概览 Claude Code 的核心概念。
查看详细文档 → [终极指南](../ultimate-guide.md) | [速查表](../cheatsheet.md)

> **提供交互式 Mermaid 图表**：涵盖模型选择、agent 生命周期、内存层级、多 agent 模式、安全威胁等 40 张交互式图表，请参见 **[guide/diagrams/](../diagrams/)**。本文件包含核心概念的 ASCII 版本。

> **20 张图表**：8 张全新（本文件）+ 12 张来自现有指南，全部汇总于此。

---

## 目录

**新增图表：**
1. [上下文管理区间](#1-context-management-zones)
2. [权限模式循环](#2-permission-modes-cycle)
3. [工作流管线（9 步）](#3-workflow-pipeline-9-steps)
4. [快速决策树](#4-quick-decision-tree)

**架构与内部机制：**
5. [主循环](#5-master-loop)
6. [Hook 事件流](#6-hook-event-flow)
7. [数据隐私流](#7-data-privacy-flow)

**安全：**
8. [MCP Rug Pull 攻击](#8-mcp-rug-pull-attack)
9. [Docker 沙箱架构](#9-docker-sandbox-architecture)

**决策树：**
10. [搜索工具选择](#10-search-tool-selection)
11. [信任校准流](#11-trust-calibration-flow)
12. [采用决策树](#12-adoption-decision-tree)
13. [方法论选择](#13-methodology-selection)

**工作流：**
14. [研究 → 规格 → 代码](#14-research--spec--code)
15. [审查自动纠正循环](#15-review-auto-correction-loop)
16. [PDF 管线技术栈](#16-pdf-pipeline-stack)

**开发与学习：**
17. [TDD 红-绿-重构循环](#17-tdd-red-green-refactor-cycle)
18. [UVAL 协议流](#18-uval-protocol-flow)

**安全（扩展）：**
19. [安全三层防御](#19-security-3-layer-defense)
20. [密钥暴露时间线](#20-secret-exposure-timeline)

---

## 1. Context Management Zones

如何根据上下文窗口使用情况作出反应（用 `/status` 查看）：

```
Context Usage
0%          50%         70%         90%       100%
├───────────┼───────────┼───────────┼──────────┤
│   GREEN   │  YELLOW   │  ORANGE   │   RED    │
│  work     │ selective │ /compact  │  /clear  │
│  freely   │ with care │   NOW     │ required │
└───────────┴───────────┴───────────┴──────────┘
              ▲                       ▲
              │                       │
         Be selective            Risk: forgetting
         about reads             instructions,
         and tool use            hallucinations
```

**各区间对应操作：**
- **绿色（0-50%）** — 全速前进。自由读取文件、自由探索。
- **黄色（50-70%）** — 有所取舍。避免不必要的文件读取。
- **橙色（70-90%）** — 立即运行 `/compact`。上下文质量正在下降。
- **红色（90%+）** — 运行 `/clear` 并重新开始。响应已不可靠。

→ 来源：[ultimate-guide.md:1335](../ultimate-guide.md)

---

## 2. Permission Modes Cycle

用 `Shift+Tab` 在各模式间循环切换：

```
                 Shift+Tab              Shift+Tab
  ┌──────────┐ ────────────→ ┌───────────────┐ ────────────→ ┌───────────┐
  │ DEFAULT  │               │  AUTO-ACCEPT   │               │ PLAN MODE │
  │          │               │                │               │           │
  │ edit=ask │               │ edit=auto      │               │ edit=no   │
  │ exec=ask │               │ exec=ask       │               │ exec=no   │
  └──────────┘ ←──────────── └───────────────┘ ←──────────── └───────────┘
                 Shift+Tab              Shift+Tab
```

**各模式的使用时机：**

| 模式 | 何时使用…… | 风险等级 |
|------|-------------|------------|
| **Default** | 常规开发 — 逐项审查每处改动 | 低 |
| **Auto-accept** | 可信任务（格式化、重构） | 中 |
| **Plan mode** | 复杂/高风险操作 — 先安全地探索 | 无 |

**快捷键：**
- `Shift+Tab` — 切换到下一个模式
- `Shift+Tab × 2` — 从 default 直接跳到 plan mode
- `/plan` — 直接进入 plan mode
- `/execute` — 退出 plan mode

→ 来源：[ultimate-guide.md:760](../ultimate-guide.md)

---

## 3. Workflow Pipeline (9 Steps)

每个任务推荐的工作流：

```
  ┌─────────┐    ┌──────────┐    ┌────────────┐    ┌─────────────┐
  │ 1.START │───→│ 2./status│───→│ 3. plan?   │───→│ 4. describe │
  │ claude  │    │ check ctx│    │ Shift+Tab×2│    │ WHAT/WHERE  │
  └─────────┘    └──────────┘    │ (if risky) │    │ HOW/VERIFY  │
                                 └────────────┘    └──────┬──────┘
                                                          │
      ┌───────────────────────────────────────────────────┘
      │
      ▼
  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ 5.review │───→│ 6. y/n   │───→│ 7. test  │───→│ 8.commit │───→│9./compact│
  │   diff   │    │ accept?  │    │   run    │    │ when done│    │ when >70%│
  └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

**关键原则：**
- **第 2 步**：开始前务必检查上下文。若 >70%，先执行 `/compact`。
- **第 3 步**：对任何高风险、复杂或涉及多文件的操作使用 plan mode。
- **第 4 步**：要具体 — 含糊的提示词产生含糊的结果。
- **第 5 步**：审查每一处 diff。切勿盲目接受。
- **第 9 步**：每个任务后进行 compact，以保持在绿色区间内。

→ 来源：[ultimate-guide.md:277](../ultimate-guide.md)

---

## 4. Quick Decision Tree

根据你的具体情况该怎么做：

```
What do you need?
│
├─ Simple task ─────────────────→ Just ask Claude
│
├─ Complex task
│  ├─ Single session ───────────→ /plan + Tasks API
│  └─ Multi-session ────────────→ Tasks API + CLAUDE_CODE_TASK_LIST_ID
│
├─ Repeating task ──────────────→ Create agent or command
│
├─ Context >70% ────────────────→ /compact
│
├─ Context >90% ────────────────→ /clear (restart conversation)
│
├─ Need library docs ───────────→ Context7 MCP
│
├─ Deep debugging ──────────────→ Opus model + Alt+T (thinking)
│
├─ UI from design ──────────────→ Figma MCP or screenshot input
│
└─ Team rollout ────────────────→ Read adoption-approaches.md
```

→ 来源：[reference.yaml](../../machine-readable/reference.yaml)（decide 部分）

---

## 5. Master Loop

整个架构就是一个简单的 `while` 循环 — 没有 DAG，没有分类器，没有 RAG。

```
┌─────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE MASTER LOOP                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────────┐                                          │
│   │  Your Prompt │                                          │
│   └──────┬───────┘                                          │
│          │                                                  │
│          ▼                                                  │
│   ┌──────────────────────────────────────────────────────┐  │
│   │                                                      │  │
│   │                  CLAUDE REASONS                      │  │
│   │        (No classifier, no routing layer)             │  │
│   │                                                      │  │
│   └────────────────────────┬─────────────────────────────┘  │
│                            │                                │
│                            ▼                                │
│                   ┌────────────────┐                        │
│                   │  Tool Call?    │                        │
│                   └───────┬────────┘                        │
│                           │                                 │
│              YES          │           NO                    │
│         ┌─────────────────┴─────────────────┐               │
│         │                                   │               │
│         ▼                                   ▼               │
│  ┌────────────┐                      ┌────────────┐         │
│  │  Execute   │                      │   Text     │         │
│  │   Tool     │                      │  Response  │         │
│  │            │                      │   (DONE)   │         │
│  └─────┬──────┘                      └────────────┘         │
│        │                                                    │
│        ▼                                                    │
│  ┌─────────────┐                                            │
│  │ Feed Result │                                            │
│  │  to Claude  │──────────────────┐                         │
│  └─────────────┘                  │                         │
│                                   │                         │
│                                   ▼                         │
│                          ┌────────────────┐                 │
│                          │   LOOP BACK    │                 │
│                          │  (Next turn)   │                 │
│                          └────────────────┘                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

→ 来源：[architecture.md:84](./architecture.md)

---

## 6. Hook 事件流

hooks 如何拦截 Claude Code 的执行流水线：

```
┌─────────────────────────────────────────────────────────┐
│                      EVENT FLOW                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   User types message                                    │
│        │                                                │
│        ▼                                                │
│   ┌────────────────────┐                                │
│   │ UserPromptSubmit   │  ← Add context (git status)    │
│   └────────────────────┘                                │
│        │                                                │
│        ▼                                                │
│   Claude decides to run tool (e.g., Edit)               │
│        │                                                │
│        ▼                                                │
│   ┌────────────────────┐                                │
│   │ PreToolUse         │  ← Security check              │
│   └────────────────────┘                                │
│        │                                                │
│        ▼ (if allowed)                                   │
│   Tool executes                                         │
│        │                                                │
│        ▼                                                │
│   ┌────────────────────┐                                │
│   │ PostToolUse        │  ← Auto-format                 │
│   └────────────────────┘                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

→ 来源：[ultimate-guide.md:6327](../ultimate-guide.md)

---

## 7. 数据隐私流

使用 Claude Code 时哪些数据会离开你的机器：

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR LOCAL MACHINE                       │
├─────────────────────────────────────────────────────────────┤
│  • Prompts you type                                         │
│  • Files Claude reads (including .env if not excluded!)     │
│  • MCP server results (SQL queries, API responses)          │
│  • Bash command outputs                                     │
│  • Error messages and stack traces                          │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼ HTTPS
┌─────────────────────────────────────────────────────────────┐
│                    ANTHROPIC API                            │
├─────────────────────────────────────────────────────────────┤
│  • Processes your request                                   │
│  • Stores conversation based on retention policy            │
│  • May use data for model training (if not opted out)       │
└─────────────────────────────────────────────────────────────┘
```

→ 来源：[data-privacy.md:24](../security/data-privacy.md)

---

## 8. MCP Rug Pull 攻击

恶意 MCP 服务器如何利用一次性审批模型进行攻击：

```
┌─────────────────────────────────────────────────────────────┐
│  1. Attacker publishes benign MCP "code-formatter"          │
│                         ↓                                    │
│  2. User adds to ~/.claude.json, approves once               │
│                         ↓                                    │
│  3. MCP works normally for 2 weeks (builds trust)           │
│                         ↓                                    │
│  4. Attacker pushes malicious update (no re-approval!)      │
│                         ↓                                    │
│  5. MCP exfiltrates ~/.ssh/*, .env, credentials             │
└─────────────────────────────────────────────────────────────┘
MITIGATION: Version pinning + hash verification + monitoring
```

→ 来源：[security-hardening.md:33](../security/security-hardening.md)

---

## 9. Docker 沙箱架构

为自主运行的 Claude Code 会话提供完全隔离：

```
┌──────────────────────────────────────────────────────────┐
│                     HOST MACHINE                          │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │              DOCKER SANDBOX (microVM)               │  │
│  │                                                    │  │
│  │  ┌──────────────┐  ┌───────────────────────────┐  │  │
│  │  │ Claude Code   │  │ Private Docker daemon     │  │  │
│  │  │ (--dsp mode)  │  │ (isolated from host)      │  │  │
│  │  └──────────────┘  └───────────────────────────┘  │  │
│  │                                                    │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │ Workspace: ~/my-project (synced with host)   │  │  │
│  │  │ Same absolute path as host                   │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  │                                                    │  │
│  │  Base: Ubuntu, Node.js, Python 3, Go, Git,        │  │
│  │        Docker CLI, GitHub CLI, ripgrep, jq         │  │
│  │  User: non-root 'agent' with sudo                 │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  Host Docker daemon: NOT accessible from sandbox          │
│  Host filesystem: NOT accessible (except workspace)       │
└──────────────────────────────────────────────────────────┘
```

→ 来源：[sandbox-isolation.md:87](../security/sandbox-isolation.md)

---

## 10. 搜索工具选择

选择合适搜索工具的 3 层决策树：

**第 1 层：你已知什么？**

```
Do you know the EXACT text/pattern?
│
├─ YES → Use rg (ripgrep)
│  ├─ Known function name: rg "createSession"
│  ├─ Known import: rg "import.*React"
│  └─ Known pattern: rg "async function"
│
└─ NO → Go to Level 2
```

**第 2 层：你在找什么？**

```
What's your search intent?
│
├─ "Find by MEANING/CONCEPT"
│  → Use grepai
│  └─ Example: grepai search "payment validation logic"
│
├─ "Find FUNCTION/CLASS definition"
│  → Use Serena
│  └─ Example: serena find_symbol --name "UserController"
│
├─ "Find by CODE STRUCTURE"
│  → Use ast-grep
│  └─ Example: async without error handling
│
└─ "Understand DEPENDENCIES"
   → Use grepai trace
   └─ Example: grepai trace callers "validatePayment"
```

**第 3 层：优化**

```
Found too many results?
│
├─ rg → Add --type filter or narrow path
├─ grepai → Add --path filter or use trace
├─ Serena → Filter by symbol type (function/class)
└─ ast-grep → Add constraints to pattern
```

→ 来源：[search-tools-mastery.md:75](../workflows/search-tools-mastery.md)

---

## 11. 信任校准流

根据风险等级决定对 AI 生成代码的审查程度：

```
┌─────────────────────────────────────────────────────────┐
│                 TRUST CALIBRATION FLOW                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  AI generates code                                      │
│         │                                               │
│         ▼                                               │
│  ┌──────────────┐                                       │
│  │ What type?   │                                       │
│  └──────────────┘                                       │
│    │    │    │                                          │
│    ▼    ▼    ▼                                          │
│  Boiler Business Security                               │
│  -plate  logic   critical                               │
│    │      │        │                                    │
│    ▼      ▼        ▼                                    │
│  Skim   Test +   Full review                            │
│  only   review   + tools                                │
│    │      │        │                                    │
│    └──────┴────────┘                                    │
│            │                                            │
│            ▼                                            │
│    Tests pass? ──No──► Debug & fix                      │
│            │                                            │
│           Yes                                           │
│            │                                            │
│            ▼                                            │
│        Ship it                                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

→ 来源：[ultimate-guide.md:1182](../ultimate-guide.md)

---

## 12. 采用决策树

如何选择你的 Claude Code 采用策略：

```
Starting Claude Code?
│
├─ Need to ship today?
│   └─ YES → Turnkey Quickstart
│   └─ NO ↓
│
├─ Team needs shared conventions?
│   └─ YES → Turnkey + document what matters to you
│   └─ NO ↓
│
├─ Want to understand before configuring?
│   └─ YES → Autonomous Learning Path
│   └─ NO → Turnkey, adjust as you go
```

→ 来源：[adoption-approaches.md:51](../roles/adoption-approaches.md)

---

## 13. 方法论选择

应该采用哪种开发方法论：

```
┌─ "I want quality code" ────────────→ workflows/tdd-with-claude.md
│
├─ "I want to spec before code" ─────→ workflows/spec-first.md
│
├─ "I need to plan architecture" ────→ workflows/plan-driven.md
│
├─ "I'm iterating on something" ─────→ workflows/iterative-refinement.md
│
└─ "I need methodology theory" ──────→ methodologies.md
```

→ 来源：[methodologies.md:24](./methodologies.md)

---

## 14. 研究 → 规格 → 代码

先用 Perplexity 做研究，再用 Claude Code 实现：

```
┌─────────────────────────────────────────────────────────┐
│ 1. PERPLEXITY (Deep Research)                           │
│    "Research best practices for JWT refresh tokens      │
│     in Next.js 15. Include security considerations,     │
│     common pitfalls, and library recommendations."      │
│                                                         │
│    → Output: 2000-word spec with sources               │
└───────────────────────────┬─────────────────────────────┘
                            ↓ Export as spec.md
┌─────────────────────────────────────────────────────────┐
│ 2. CLAUDE CODE                                          │
│    > claude                                             │
│    "Implement JWT refresh tokens following spec.md.     │
│     Use the jose library as recommended."               │
│                                                         │
│    → Output: Working implementation with tests         │
└─────────────────────────────────────────────────────────┘
```

→ 来源：[ai-ecosystem.md:155](../ecosystem/ai-ecosystem.md)

---

## 15. 评审自动纠错循环

迭代式代码评审模式，Claude 进行评审、修复并再次评审：

```
┌─────────────────────────────────────────┐
│   Review Auto-Correction Loop           │
│                                          │
│   Review (identify issues)               │
│        ↓                                 │
│   Fix (apply corrections)                │
│        ↓                                 │
│   Re-Review (verify fixes)               │
│        ↓                                 │
│   Converge (minimal changes) → Done      │
│        ↑                                 │
│        └──── Repeat (max iterations)     │
└─────────────────────────────────────────┘
```

→ 来源：[iterative-refinement.md:354](../workflows/iterative-refinement.md)

---

## 16. PDF 流水线技术栈

用于生成专业 PDF 的 Quarto + Typst 技术栈：

```
┌─────────────────────────────────────────────────┐
│                  Your .qmd File                 │
│         (Markdown + YAML frontmatter)           │
└─────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│                    Quarto                       │
│           (Document rendering engine)           │
│         • Processes YAML metadata               │
│         • Handles extensions                    │
│         • Manages output formats                │
└─────────────────────────────────────────────────┘
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
┌─────────────────────┐    ┌─────────────────────┐
│       Pandoc        │    │       Typst         │
│   (MD → AST → ?)    │    │  (Typography/PDF)   │
│  • Markdown parser  │    │  • Modern engine    │
│  • AST transforms   │    │  • Fast compilation │
│  • Format bridges   │    │  • No LaTeX needed  │
└─────────────────────┘    └─────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│                  document.pdf                   │
│        (Professional typography output)         │
└─────────────────────────────────────────────────┘
```

→ 来源：[pdf-generation.md:58](../workflows/pdf-generation.md)

---

## 17. TDD 红-绿-重构循环

测试驱动开发核心的迭代循环：

```
                    ┌──────────────────────────┐
                    │                          │
                    ▼                          │
            ┌──────────────┐                   │
            │   🔴 RED      │                   │
            │              │                   │
            │  Write a     │                   │
            │  failing     │                   │
            │  test        │                   │
            └──────┬───────┘                   │
                   │                           │
                   │ Tests FAIL                │
                   │ (expected)                │
                   ▼                           │
            ┌──────────────┐                   │
            │   🟢 GREEN   │                   │
            │              │                   │
            │  Write       │                   │
            │  minimal     │                   │
            │  code to     │                   │
            │  pass        │                   │
            └──────┬───────┘                   │
                   │                           │
                   │ Tests PASS                │
                   │ (minimal)                 │
                   ▼                           │
            ┌──────────────┐                   │
            │   🔵 REFACTOR│                   │
            │              │                   │
            │  Clean up    │                   │
            │  while tests │                   │
            │  stay green  │                   │
            └──────┬───────┘                   │
                   │                           │
                   │ Next feature              │
                   └───────────────────────────┘

Key rules:
  RED    → Test must FAIL before writing implementation
  GREEN  → Write ONLY enough code to pass (no more)
  REFACTOR → Improve structure, tests must stay green
  REPEAT → One feature at a time, always in this order
```

> 来源：[workflows/tdd-with-claude.md:78](../workflows/tdd-with-claude.md)

---

## 18. UVAL 协议流程

在不丧失自身优势的前提下与 AI 一起学习的系统化框架：

```
  ┌────────────────────────────────────────────────────────────┐
  │                    UVAL PROTOCOL                           │
  │         (Use AI without losing your edge)                  │
  └────────────────────────────────────────────────────────────┘

  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
  │    U     │     │    V     │     │    A     │     │    L     │
  │UNDERSTAND│────→│  VERIFY  │────→│  APPLY   │────→│  LEARN   │
  │          │     │          │     │          │     │          │
  │ 15-min   │     │ Can you  │     │ Modify   │     │ Capture  │
  │ rule:    │     │ explain  │     │ the code │     │ insights │
  │          │     │ it back? │     │ yourself │     │ for long │
  │ 1.State  │     │          │     │          │     │ term     │
  │   problem│     │ Test:    │     │ Tasks:   │     │          │
  │ 2.Brain- │     │ explain  │     │ • Extend │     │ Methods: │
  │   storm  │     │ to a     │     │ • Modify │     │ • Notes  │
  │ 3.Find   │     │ colleague│     │ • Debug  │     │ • Teach  │
  │   gaps   │     │ without  │     │ • Adapt  │     │ • Blog   │
  │ 4.Ask    │     │ looking  │     │   to new │     │ • Review │
  │   smart  │     │ at code  │     │   context│     │   later  │
  └──────────┘     └──────────┘     └──────────┘     └──────────┘
       │                                                   │
       │              ◄── Repeat per concept ──►           │
       └───────────────────────────────────────────────────┘

  If VERIFY fails → go back to UNDERSTAND (you copied, didn't learn)
  If APPLY fails  → go back to VERIFY (you memorized, didn't understand)
```

> 来源：[learning-with-ai.md:208](../roles/learning-with-ai.md)

---

## 19. 安全三层防御

完整的安全文档（security-hardening.md）按 3 个防御层组织：

```
  ┌─────────────────────────────────────────────────────────────┐
  │                  SECURITY 3-LAYER DEFENSE                   │
  ├─────────────────────────────────────────────────────────────┤
  │                                                             │
  │  TIME ──────────────────────────────────────────────────►   │
  │         Before              During             After        │
  │                                                             │
  │  ┌─────────────────┐ ┌─────────────────┐ ┌───────────────┐ │
  │  │ LAYER 1         │ │ LAYER 2         │ │ LAYER 3       │ │
  │  │ PREVENTION      │ │ DETECTION       │ │ RESPONSE      │ │
  │  │                 │ │                 │ │               │ │
  │  │ • MCP vetting   │ │ • Prompt inject │ │ • Secret      │ │
  │  │   workflow      │ │   detection     │ │   rotation    │ │
  │  │ • Version       │ │ • Output        │ │ • MCP         │ │
  │  │   pinning       │ │   scanning      │ │   isolation   │ │
  │  │ • .claudeignore │ │ • Anomaly       │ │ • History     │ │
  │  │ • Input hooks   │ │   monitoring    │ │   rewriting   │ │
  │  │ • Safe MCP list │ │ • Secret leak   │ │ • Incident    │ │
  │  │ • Permissions   │ │   detection     │ │   reporting   │ │
  │  │ • Integrity     │ │ • Unicode/ANSI  │ │ • Post-mortem │ │
  │  │   scanning      │ │   filtering     │ │   & rotation  │ │
  │  │                 │ │                 │ │               │ │
  │  │  GOAL: Block    │ │  GOAL: Catch    │ │  GOAL: Limit  │ │
  │  │  threats at     │ │  attacks in     │ │  damage and   │ │
  │  │  entry points   │ │  real-time      │ │  recover fast │ │
  │  └─────────────────┘ └─────────────────┘ └───────────────┘ │
  │                                                             │
  │  Adoption path:                                             │
  │  Solo dev    → Layer 1 basics (output scanner)              │
  │  Team        → Layer 1 + 2 (+ injection hooks)              │
  │  Enterprise  → All 3 layers (+ ZDR + verification)          │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘
```

> 来源：[security-hardening.md:24/205/345](../security/security-hardening.md)

---

## 20. 密钥泄露时间线

当密钥（API key、token、密码）泄露时的应急响应：

```
  SECRET EXPOSED — Emergency Response Timeline
  ═══════════════════════════════════════════════════════════

  0 min                15 min              1 hour             24 hours
  │                    │                   │                  │
  ▼                    ▼                   ▼                  ▼
  ┌──────────────────┐ ┌─────────────────┐ ┌────────────────┐
  │ ⏱️ FIRST 15 MIN   │ │ ⏱️ FIRST HOUR    │ │ ⏱️ FIRST 24H    │
  │ Stop the         │ │ Assess damage   │ │ Remediate      │
  │ bleeding         │ │                 │ │                │
  │                  │ │ 3. Audit git    │ │ 6. Rotate ALL  │
  │ 1. REVOKE key    │ │    history      │ │    related     │
  │    immediately   │ │    (rewrite if  │ │    credentials │
  │    (AWS/GH/      │ │     pushed)     │ │                │
  │     Stripe)      │ │                 │ │ 7. Notify team │
  │                  │ │ 4. Scan deps    │ │    /compliance │
  │ 2. Confirm       │ │    for leaked   │ │    (GDPR/SOC2) │
  │    exposure      │ │    keys         │ │                │
  │    scope         │ │                 │ │ 8. Document    │
  │    (local or     │ │ 5. Check CI/CD  │ │    incident    │
  │     pushed?)     │ │    logs         │ │    timeline    │
  │                  │ │                 │ │                │
  └──────────────────┘ └─────────────────┘ └────────────────┘

  SEVERITY GUIDE:
  ┌─────────────────────────────────────────────────────────┐
  │ Local only (not pushed)  → Revoke + rotate (steps 1-2) │
  │ Pushed to remote         → Full timeline (steps 1-8)   │
  │ Public repo exposure     → Assume compromised, rotate  │
  │                            EVERYTHING, check for abuse  │
  └─────────────────────────────────────────────────────────┘
```

> 来源：[security-hardening.md:347](../security/security-hardening.md)

---

*返回 [指南 README](../README.md) | [速查表](../cheatsheet.md) | [主 README](../README.md)*
