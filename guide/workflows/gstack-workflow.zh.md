---
title: "认知模式切换"
description: "在交付周期中切换专家角色——战略关卡、架构、偏执评审、发布、浏览器 QA、复盘"
tags: [workflow, skills, planning, review, shipping, browser-automation]
---

# 认知模式切换

> **可信度**：Tier 2——参考实现：[gstack](https://github.com/garrytan/gstack)，作者 Garry Tan（Y Combinator CEO），发布 24 小时内即获得 1100+ stars（2026 年 3 月）。

**阅读时间**：约 10 分钟
**前置条件**：Claude Code skills 基础、plan mode
**相关**：[Plan Pipeline](./plan-pipeline.md)、[Plan-Driven Development](./plan-driven.md)

---

## TL;DR

一个通用助手会把所有阶段混为一谈。这个模式为每个阶段赋予独特的认知模式：你为当前工作召唤对应的「大脑」，当工作发生变化时再切换。

```
/plan-ceo-review  → "我们做的是对的东西吗？"
/plan-eng-review  → "我们如何让它可被构建？"
/review           → "什么会在生产环境炸掉？"
/ship             → 执行发布，不再争论
/browse           → 它在浏览器里真的能用吗？
/retro            → 我们这周交付得怎么样？
```

核心洞察在于：规划、评审和交付需要根本不同的认知姿态——而一个停留在通用模式下的助手会把它们糟糕地混在一起。

---

## 六个挡位

| 命令 | 角色 | 核心问题 | 何时切换 |
|---------|------|---------------|----------------|
| `/plan-ceo-review` | 创始人 / CEO | "我们做的是对的东西吗？" | 在写任何代码之前 |
| `/plan-eng-review` | 工程经理 / 技术负责人 | "我们如何让它可被构建？" | 方向锁定之后 |
| `/review` | 偏执的资深工程师 | "什么仍可能在生产环境炸掉？" | 合并之前 |
| `/ship` | 发布工程师 | "把飞机降落下来" | 分支就绪，不再争论 |
| `/browse` | QA 工程师 | "它真的能用吗？" | 部署后，针对预发布或生产环境 |
| `/retro` | 工程经理 | "我们交付得怎么样？" | 每周或上线后 |

---

## 它填补的空白：实现前的战略关卡

使用 AI 编码助手最难做对的事情不是实现本身，而是在此之前的那个问题：**我们做的是对的东西吗？**

Claude Code 被优化为构建你所要求的东西。如果你说「添加照片上传」，它就会添加照片上传。它不会去问照片上传是否真的就是这个产品。这正是 `/plan-ceo-review` 要解决的问题。

**示例**：你正在构建一个 Craigslist 风格的商品发布应用。

- 需求："让卖家为他们的物品上传一张照片"
- 字面实现：文件选择器 + 图片保存
- 真正的产品是什么：帮助卖家创建真正能卖出去的商品列表

如果你先运行 `/plan-ceo-review`，助手会被明确要求挑战这个字面需求，找出隐藏在其中的产品。输出会变成一份完全不同的简报：从照片自动识别商品、拉取规格参数和定价对比、起草标题和描述、推荐主图、在低质量照片上线前检测出来。

那是一个不同的功能，一个更好的功能。而你只有在实现开始之前插入一个明确的关卡，才能得到它。

**`/plan-ceo-review` 内部的三种模式**：
- **SCOPE EXPANSION（范围扩展）**——寻找十星级产品，问"用 2 倍的投入怎样让它好 10 倍？"
- **HOLD SCOPE（保持范围）**——接受这个方向，把计划打磨到无懈可击
- **SCOPE REDUCTION（范围收缩）**——无情地削减到最小可行版本

由用户选择模式。助手会承诺执行该模式，不会偏移。

---

## /plan-eng-review：让想法可被构建

一旦方向锁定，认知模式就从产品直觉转向工程严谨。`/plan-eng-review` 是构思结束、架构开始的地方。

它应当产出：
- 架构图（组件、边界、数据流）
- 核心流程的状态机
- 同步与异步边界决策
- 故障模式与重试逻辑
- 信任边界（你在哪里接受外部输入？）
- 测试矩阵

关键突破在于**强制生成图表**。图表会暴露出散文所掩盖的隐藏假设。一张序列图迫使你指明谁调用了谁。一个状态机迫使你枚举每一种故障模式。没有它们，"系统会处理好的"就会无限期地含糊下去。

---

## /review：偏执资深工程师模式

测试通过并不意味着分支是安全的。`/review` 的存在正是为了那一类能熬过 CI、却照样打到生产环境的 bug。

它检查的内容：
- N+1 查询
- 竞态条件（两个标签页覆盖同一份状态）
- 信任边界违规（未经校验就接受客户端提供的元数据）
- 失败路径上的孤儿数据
- 缺失的索引
- 糟糕的重试逻辑
- 通过了却漏掉真实故障模式的测试
- 当 LLM 输出流入后续处理时的 prompt injection

这种姿态是刻意的：在生产事故发生之前先想象它。

---

## /browse：非 MCP 的原生浏览器自动化

`/browse` 是 gstack 中技术上最独特的部分。它不是一个 MCP 服务器，而是一个编译后的原生二进制文件（TypeScript + Bun），运行一个常驻的无头 Chromium 守护进程。

**为什么架构很重要**：

| 方案 | 冷启动 | 后续调用 | 状态持久化 |
|----------|-----------|-----------------|-------------------|
| MCP 浏览器服务器 | 每个会话新建连接 | ~500ms+ | 会话之间丢失 |
| `/browse` 原生守护进程 | ~3s（一次性） | ~100-200ms | cookies、标签页、认证均持久保留 |

这对 QA 工作流很重要：登录预发布环境一次，然后运行完整的导航序列依然很快，因为守护进程从不重启。没有 MCP socket 开销，没有会话重置。

**可用操作**：导航、读取页面文本、截图、带 refs 的可访问性树快照、按 ref 点击/填写、运行 JavaScript、检查 console 日志、捕获网络请求。

**何时应优先选择它而非 MCP 浏览器工具**：
- 对延迟敏感的 QA 循环（连续 10+ 个页面检查）
- MCP 服务器连接受限的环境
- 当你需要浏览器状态（认证、cookies）在一个会话中跨多个命令持久保留时

**何时应坚持使用 MCP**：单页检查、更简单的环境，或当 MCP 浏览器工具链已经就位时。

---

## 完整周期演示

```
# 1. Strategic gate — challenge the brief
[plan mode]
You: I want to add seller photo upload to the listing app.
     Sellers should be able to upload a photo and we create the listing from it.

You: /plan-ceo-review   (select SCOPE EXPANSION mode)

Claude: "Photo upload" is not the feature. The real job is helping sellers
        create listings that actually sell. Here's the 10-star version:
        auto-identify the product, pull specs and pricing comps from the web,
        draft title and description, suggest the best hero image...

# 2. Engineering gate — lock the architecture
You: /plan-eng-review

Claude: [Architecture diagram, async job boundaries, state machine for
        upload → classify → enrich → draft pipeline, failure modes,
        trust boundaries, test matrix]

# 3. Implement the plan
[exit plan mode, write code]

# 4. Paranoid review — find what tests missed
You: /review

Claude: Race condition: two tabs can overwrite cover-photo selection.
        Trust boundary: pulling web data into draft generation creates
        a prompt injection vector.
        Missing: orphan cleanup for failed uploads.

You: [fix the issues]

# 5. Ship
You: /ship

Claude: [Syncs main, runs tests, pushes branch, opens PR — done]

# 6. Browser QA against staging
You: /browse staging.myapp.com — test the listing flow

Claude: [Navigates routes, fills upload form, verifies enrichment renders,
        checks console for errors, screenshots each step]
        All pages load correctly. Listing flow works end to end.
```

---

## 安装

```bash
# Install globally (~/.claude/skills/)
git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack
cd ~/.claude/skills/gstack && ./setup
```

或者直接把这段粘贴进 Claude Code，它会处理好其余部分：

> 安装 gstack：运行 `git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup`

对于团队安装（提交到仓库，这样队友只需 `git clone` 即可使用），参见 [gstack README](https://github.com/garrytan/gstack)。

> **注意（2026 年 3 月）**：gstack 于 2026 年 3 月 11 日发布。模式是扎实的；实现是新的。在生产工作流中采用之前，请先确认该仓库处于积极维护状态。

---

## 何时使用本工作流 vs. 其他工作流

| 场景 | 本工作流 | 替代方案 |
|-----------|---------------|-------------|
| 复杂功能，方向不确定 | 先用 `/plan-ceo-review` | [Spec-First](./spec-first.md) |
| 方向清晰，架构复杂 | `/plan-eng-review` | [Plan Pipeline](./plan-pipeline.md) |
| 需要对计划进行独立验证 | [Plan Pipeline](./plan-pipeline.md) `/plan-validate` | — |
| 浏览器自动化，单页检查 | 任意 MCP 浏览器工具 | `/browse`（杀鸡用牛刀） |
| 浏览器自动化，多步 QA 循环 | `/browse` | MCP 工具（更慢） |
| 想要结构化的 ADR 学习循环 | [Plan Pipeline](./plan-pipeline.md) | — |

与 [Plan Pipeline](./plan-pipeline.md) 的主要区别：gstack 是一个由你手动控制的线性挡位序列。Plan Pipeline 则是带有 ADR 记忆和并行 agent 团队的更自动化的编排。对于想要对每个阶段拥有显式控制的独立开发者，gstack 上手更快。

---

## 参见

- [Plan Pipeline](./plan-pipeline.md) — 带 ADR 学习循环的自动化三命令工作流
- [Plan-Driven Development](./plan-driven.md) — 编码前规划的基础知识
- [Iterative Refinement](./iterative-refinement.md) — 质量改进循环
- [gstack on GitHub](https://github.com/garrytan/gstack) — 源码、安装说明、完整的 skill 提示词
