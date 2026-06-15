---
title: "演讲准备流水线：借助 AI 从创意到幻灯片"
description: "6 阶段 skill 流水线，将原始素材转化为附带 AI 生成幻灯片的会议演讲"
tags: [workflow, skills, pipeline, presentation, ai-handoff]
---

# 演讲准备流水线：借助 AI 从创意到幻灯片

> **可信度**：Tier 2 —— 已在真实会议演讲的生产环境中验证（DevWithAI Lyon，2026）。

将一篇原始文章、转录稿或笔记转化为一场完整的会议演讲 —— 其中包含一个可直接用于 Kimi 的提示词，用于 AI 生成幻灯片。六个阶段、两种模式、一个 human-in-the-loop 检查点。

---

## 目录

1. [TL;DR](#tldr)
2. [何时使用](#when-to-use)
3. [前置条件](#prerequisites)
4. [流水线概览](#pipeline-overview)
5. [逐阶段指南](#stage-by-stage-guide)
6. [Kimi 交接](#the-kimi-handoff)
7. [Human-in-the-Loop 检查点](#human-in-the-loop-checkpoints)
8. [调整流水线](#adapting-the-pipeline)
9. [真实案例](#real-world-example)
10. [常见陷阱](#common-pitfalls)
11. [展示的设计模式](#design-patterns-showcased)
12. [另见](#see-also)

---

## TL;DR

```
Source Material (article / transcript / notes)
        │
        ▼
[Stage 1] EXTRACT ─────────────── {slug}-summary.md
        │
        ├──────────────────────────────────────┐
        │                                      │
        ▼ (--rex only)                         ▼
[Stage 2] RESEARCH               [Stage 3] CONCEPTS
  git-archaeology.md              concepts.md
  changelog-analysis.md           concepts-enriched.md
  timeline.md                         │
        │                             │
        └──────────────┬──────────────┘
                       │
                       ▼
              [Stage 4] POSITION
                angles.md
                titre.md
                descriptions.md
                feedback-draft.md
                       │
                  [CHECKPOINT]
             User selects angle + title
                       │
                       ▼
              [Stage 5] SCRIPT
                pitch.md
                slides.md
                kimi-prompt.md ──► Copy-paste into Kimi.com
                       │
                       ▼
             [Stage 6] REVISION
              revision-sheets.md
```

两种模式：**REX**（带真实世界证据的演讲 —— git 历史、指标）和 **Concept**（基于创意/论点 —— 跳过 Stage 2）。

---

## 何时使用

当你需要准备一场演讲，且符合以下任一情况时，这条流水线就很合适：

- **有一个 REX 要讲**：你构建了某个东西、把它上线了、拥有真实指标 —— 并想把它转化为一场结构化的会议演讲
- **有一个概念要展开**：你有一篇文章、一些笔记或想法，想把它转化为一场结构化的演示

适合的形式：
- 会议演讲（20-45 分钟）
- Meetup 演示（15-30 分钟）
- 内部技术分享
- Workshop 开场

不适合：周期性会议的幻灯片更新、10 分钟以内的简短闪电演讲，或者你完全没有现成素材可供参考的情况。

---

## 前置条件

**必需**：
- 已安装 skills 的 Claude Code（见 [examples/skills/talk-pipeline/](../../examples/skills/talk-pipeline/)）
- 源素材：文章 `.mdx`、转录稿 `.md`、笔记，或混合
- 演讲元数据：slug、活动名称、日期、时长、受众描述

**仅 REX 模式需要**：
- 访问你想要分析的 git 仓库的权限
- 可选：若 `CHANGELOG.md` 不在仓库根目录，则提供其路径

**Kimi 幻灯片生成需要（Stage 5 的输出）**：
- [kimi.com](https://kimi.com) 的免费账号（无需 API —— 直接复制粘贴即可）

**可选但推荐**：
- 在项目根目录下有一个 `talks/` 目录用于存放输出文件
- 有 1-2 位可信赖的同行可供反馈草稿征询意见（Stage 4）

---

## 流水线概览

### 各模式的输出文件

| 文件 | 阶段 | REX | Concept |
|------|-------|-----|---------|
| `{slug}-summary.md` | 1 | ✓ | ✓ |
| `{slug}-git-archaeology.md` | 2 | ✓ | — |
| `{slug}-changelog-analysis.md` | 2 | ✓ | — |
| `{slug}-timeline.md` | 2 | ✓ | — |
| `{slug}-concepts.md` | 3 | ✓ | ✓ |
| `{slug}-concepts-enriched.md` | 3 | ✓（若有仓库） | — |
| `{slug}-angles.md` | 4 | ✓ | ✓ |
| `{slug}-titre.md` | 4 | ✓ | ✓ |
| `{slug}-descriptions.md` | 4 | ✓ | ✓ |
| `{slug}-feedback-draft.md` | 4 | ✓ | ✓ |
| `{slug}-pitch.md` | 5 | ✓ | ✓ |
| `{slug}-slides.md` | 5 | ✓ | ✓ |
| `{slug}-kimi-prompt.md` | 5 | ✓ | ✓ |
| `{slug}-revision-sheets.md` | 6 | ✓ | ✓ |

REX 模式：13-14 个文件。Concept 模式：10 个文件。

### 命名约定

所有输出都遵循 `talks/{YYYY}-{slug}-{stage-label}.md`。以 2026 年 slug 为 `devwithai` 为例：

```
talks/2026-devwithai-summary.md
talks/2026-devwithai-git-archaeology.md
talks/2026-devwithai-concepts.md
talks/2026-devwithai-angles.md
...
```

---

## 逐阶段指南

### Stage 1：Extract（提取）

**作用**：读取源素材并产出一份结构化摘要 —— 叙事弧线、关键指标、主要主题、缺口。

| | |
|--|--|
| **输入** | 源文件 + 元数据（slug、活动、日期、时长、受众、模式） |
| **输出** | `{slug}-summary.md` |
| **使用的工具** | Read、Write、AskUserQuestion |
| **模式** | REX + Concept |

**关键规则**：
- 基于信号（日期、指标、"我已上线" vs "我认为"）自动检测源类型（REX vs Concept）
- 提取每一个可量化的指标及其来源 —— 绝不杜撰数字
- 显式标注缺口，而非隐藏它们

**调用方式**：
```
/talk-stage1-extract
```

或通过编排器调用：
```
/talk-pipeline --stage=extract --slug=my-talk --event="Conf 2026" --date=2026-06-15 --duration=30 --audience="senior devs"
```

**继续前请审查**：
- 叙事弧线连贯（而非泛泛而谈："这场演讲是关于 AI 的……"）
- 所有指标都有明确来源
- 缺口已列出（即便是"无重大缺口"）
- 类型检测正确（REX / Concept / Hybrid）

---

### Stage 2：Research（研究，仅 REX 模式）

**作用**：git 考古 —— 提取速度指标、交叉引用 CHANGELOG，构建一条由 git 验证（而非估算）的事实时间线。

| | |
|--|--|
| **输入** | `{slug}-summary.md` + 仓库路径 |
| **输出** | `git-archaeology.md`、`changelog-analysis.md`、`timeline.md` |
| **使用的工具** | Bash（只读 git 命令）、Read、Write |
| **模式** | 仅 REX —— **在 Concept 模式下自动跳过** |

**关键规则**：
- 仅使用只读 git 命令 —— 绝不修改仓库
- 在 git 中找不到的日期标记为 "unverified" —— 绝不估算
- 来源之间的矛盾会被标注，而非默默调和

**使用的 git 命令**（只读）：
```bash
git log --pretty=format:"%Y-%m" | sort | uniq -c   # velocity by month
git shortlog -sn --no-merges                         # contributors
git tag --sort=version:refname                       # releases
git log --merges --oneline | wc -l                   # PRs merged
```

**继续前请审查**：
- 时间线覆盖摘要中的整个时间段
- 没有估算的日期 —— 全部经过验证
- 速度峰值附有上下文注释

---

### Stage 3：Concepts（概念）

**作用**：构建一份对素材中所有概念进行编号、评分的目录。每个概念都获得一个演讲潜力评分（HIGH / MEDIUM / LOW）。

| | |
|--|--|
| **输入** | `{slug}-summary.md` + `{slug}-timeline.md`（可选） |
| **输出** | `{slug}-concepts.md`、`{slug}-concepts-enriched.md`（若有仓库可用） |
| **使用的工具** | Read、Write |
| **模式** | REX + Concept |

**评分标准**：
- **HIGH**：可论证、反直觉、有经过验证的数字、30 秒内可落地
- **MEDIUM**：有用但在意料之中、缺少证据或数字
- **LOW**：过于抽象、已被过度覆盖、难以在一张幻灯片中说明

**评分纪律**：HIGH 最多占 30% —— 保持挑剔正是关键所在。

**继续前请审查**：
- 识别出 15+ 个概念（带仓库访问的 REX 为 20+）
- 评分经过校准（不全是 HIGH，也不全是 LOW）
- 每个概念都有 1-2 句具体描述

---

### Stage 4：Position（定位）+ CHECKPOINT（检查点）

**作用**：生成战略角度、标题、描述和一份同行反馈草稿。然后**停下并等待**你对角度 + 标题的选择。

| | |
|--|--|
| **输入** | `{slug}-summary.md` + `{slug}-concepts.md` + 活动约束 |
| **输出** | `angles.md`、`titre.md`、`descriptions.md`、`feedback-draft.md` |
| **使用的工具** | Read、Write、AskUserQuestion |
| **模式** | REX + Concept |

**会生成什么**：
- **3-4 个角度**：每个都附有优势、弱点、受众契合度、结论（评分 /5）
- **推荐**：一个明确的选择，附结构化论证
- 每个角度 **3-5 个标题**
- **简短描述**（约 100 词的摘要）+ **详细描述**（约 250 词的 CFP）
- **反馈草稿**：可直接发送的同行验证消息（3 种格式：Slack 私信、邮件、LinkedIn 帖子）

**CHECKPOINT 显示**（Stage 5 之前必须）：

```
---
CHECKPOINT : Choix angle + titre

J'ai généré 4 fichiers :
- talks/{YYYY}-{slug}-angles.md    → {n} angles analysés
- talks/{YYYY}-{slug}-titre.md     → {n} options de titre
- talks/{YYYY}-{slug}-descriptions.md
- talks/{YYYY}-{slug}-feedback-draft.md

Avant de lancer le script (Stage 5), j'ai besoin de ton choix :

1. Quel angle tu retiens ? (recommandé : Angle {X} — {nom})
2. Quel titre tu préfères ? (recommandé : "{titre}")

Tu peux aussi modifier, mixer, ou proposer quelque chose d'autre.
---
```

**没有用户的显式确认，Stage 5 无法启动。**

**确认前请审查**：
- 你已阅读反馈草稿，并可选地将其发给了一位同行
- 推荐的角度足以支撑整个时长而不重复
- 标题具体（无行话、无标题党）

---

### Stage 5：Script（脚本）

**作用**：构建包含演讲者备注的完整演讲（5 幕结构）、幻灯片规格说明，以及 Kimi 提示词。

| | |
|--|--|
| **输入** | summary + concepts + timeline（可选）+ **已验证的角度 + 标题** |
| **输出** | `{slug}-pitch.md`、`{slug}-slides.md`、`{slug}-kimi-prompt.md` |
| **使用的工具** | Read、Write |
| **模式** | REX + Concept |

**三项交付物**：

1. **`pitch.md`**：5 幕叙事，附演讲者备注、计时、关键时刻。是你要"讲"的内容 —— 而不是你从幻灯片上读的内容。

2. **`slides.md`**：逐张幻灯片的规格：标题、视觉描述、关键文本（≤30 词）、演讲者备注、时长、幕号。可直接交给设计师或传递给 Kimi。

3. **`kimi-prompt.md`**：发给 [kimi.com](https://kimi.com) 的完整提示词 —— 包含设计系统、配色方案、字体规格、完整幻灯片内容和截图占位符。可直接复制粘贴。

**一张幻灯片一个想法规则**：如果一张幻灯片需要用"和/与"来描述它，就把它拆开。

**继续前请审查**：
- 计时检查：总时长 ≤ 时长 + 10% 缓冲
- 演讲者备注大声朗读起来自然（请实测这一点）
- Kimi 提示词中没有遗留未填充的 `{PLACEHOLDER}`

---

### Stage 6：Revision（复习）

**作用**：产出用于演讲过程中及之后的复习表 —— 按幕快速导航、概念主表、Q&A 速查表、术语表。

| | |
|--|--|
| **输入** | `pitch.md` + `slides.md` + `concepts.md` |
| **输出** | `{slug}-revision-sheets.md` |
| **使用的工具** | Read、Write |
| **模式** | REX + Concept |

**复习表中包含什么**：
- 按幕组织的带锚点链接的**导航**
- **逐幕拆解**：关键概念 + 指标 + 轶事 + 可能的 Q&A
- **主表**：概念 → 1-2 句定义 → 可分享的 URL
- **Q&A 速查表**：6-10 个可能的问题及简短答案（说出来 ≤20 秒）
- **指标区块**：所有数字汇聚一处
- **外部资源**：演讲中提到的链接
- **术语表**：技术术语，每条最多 10 词

**目的**：有人提问 → 找到对应章节 → 5 秒内分享 URL。

---

## 交接给 Kimi

阶段 5 会生成 `{slug}-kimi-prompt.md`——一份面向 [kimi.com](https://kimi.com) 的完整提示词。

**该如何使用它**:
1. 打开生成的文件
2. 确认没有残留的 `{PLACEHOLDER}`（在文件中搜索）
3. 前往 [kimi.com](https://kimi.com)——免费账户，无需 API
4. 开启一段新对话
5. 复制粘贴整段提示词
6. Kimi 生成演示文稿（PowerPoint 或 PDF）

**与 Kimi 迭代**:
- 首次生成后，对照你的 `slides.md` 规格检查幻灯片
- 通过追加消息进行单项调整:"第 7 张幻灯片:把数字放大，删掉项目符号列表"
- 对于截图:导出后手动替换 `SCREENSHOT AREA` 占位符

模板中内嵌的**设计系统**:
- 深色主题（#0a0a0a 背景）
- 橙色强调色（#f97316）用于关键数字和 CTA
- Inter/SF Pro 字体排印
- 每张幻灯片最多 30 个词，让数字成为主角
- WCAG AA 对比度（适合投影仪）

**为什么选 Kimi?** 在撰写本文时，相比大多数替代工具，Kimi 能根据详尽的提示词生成质量更高的会议演示文稿。该模板针对 Kimi 做了调优，但其设计系统与幻灯片结构适用于任何 AI 演示文稿工具。

---

## 人在回路（Human-in-the-Loop）检查点

该流水线设有两个人工检查点:

### 检查点 1:阶段 1 元数据收集

如果演讲元数据（slug、活动、日期、时长、受众、模式）未在一开始提供，阶段 1 会使用 `AskUserQuestion` 在继续之前收集它们。这样可以避免生成一份你最终会弃用的摘要。

### 检查点 2:阶段 4——角度 + 标题选择（强制）

这是整条流水线的关键关卡。没有明确的人工选择，阶段 5 无法启动。

**为何重要**:角度与标题决定了后续的一切——五幕结构、哪些概念浮现、Kimi 提示词的语气。在此处由自动选择会产出一场泛泛而谈的演讲。这是唯一一个必须由你来做的决定。

**在检查点该做什么**:
1. 阅读 `angles.md`——别跳过，对你的语境而言推荐可能是错的
2. 可选地把 `feedback-draft.md` 发给一位信得过的同行（花 10 分钟，省下 2 小时返工）
3. 回复你的选择（可以是推荐项、某种修改，或完全不同的东西）

---

## 调整流水线

### 闪电演讲（10-15 分钟）

- 保留阶段 1、3、4、5——即便在 REX 模式下也跳过阶段 2
- 在阶段 3:限制为 8-10 个概念（无情筛选，只留 HIGH）
- 在阶段 4:最多生成 2 个角度
- 在阶段 5:目标约 8-10 张幻灯片，约 2 分钟/张
- 跳过阶段 6（短格式不需要）

### 45 分钟演讲

- 完整流水线，所有阶段
- 在阶段 3:目标 25-35 个概念（足以填满 5 个扎实的幕）
- 在阶段 5:20-25 张幻灯片，平均允许 3 分钟/张
- 阶段 6 变得至关重要（问答持续 10-15 分钟）

### 工作坊（90 分钟以上）

- 流水线运行至阶段 4
- 在阶段 5:用一份活动规格（练习、计时、分组讨论）替换 slides.md
- Kimi 提示词部分变为可选（对工作坊材料而言相关性较低）

### 没有可用的 git 仓库（无代码的 REX）

- 如果你有来自其他来源的指标（分析数据、仪表板、事故报告），使用 `--rex` 模式
- 在阶段 2:用从那些来源手动收集数据来替换 git 命令
- 对来源把关更严格——"未经核实"的指标撑不过整场演讲

---

## 真实案例

**演讲**:"用 AI 开发" REX——我们如何借助 AI 工具链在 7 个月内交付一个复杂项目

**模式**:REX
**活动**:DevWithAI Lyon，2026 年 2 月
**时长**:30 分钟
**源材料**:一篇 12,000 词的 `.mdx` 文章

**生成的文件（共 16 个）**:

```
talks/2026-devwithai-summary.md              (Stage 1)
talks/2026-devwithai-git-archaeology.md      (Stage 2)
talks/2026-devwithai-changelog-analysis.md   (Stage 2)
talks/2026-devwithai-timeline.md             (Stage 2)
talks/2026-devwithai-concepts.md             (Stage 3)
talks/2026-devwithai-concepts-enriched.md    (Stage 3)
talks/2026-devwithai-angles.md               (Stage 4)
talks/2026-devwithai-titre.md                (Stage 4)
talks/2026-devwithai-descriptions.md         (Stage 4)
talks/2026-devwithai-feedback-draft.md       (Stage 4)
talks/2026-devwithai-pitch.md                (Stage 5)
talks/2026-devwithai-slides.md               (Stage 5)
talks/2026-devwithai-kimi-prompt.md          (Stage 5)
talks/2026-devwithai-revision-sheets.md      (Stage 6)
```

**阶段 2 浮现的关键指标**:
- 7 个月内提交 1,200 次（由 `git log` 核实）
- 3 名主要贡献者
- 某次特定迁移后流量减少 97%（来源于 CHANGELOG v1.1.0）
- 第 4 个月达到速度峰值（达到正常节奏的 2 倍）

**选定的角度**（从生成的 3 个中选出）:"构建者之旅"——展示数月间用 AI 工具链构建到底是什么体验的 REX 角度，而非功能演示

**Kimi 输出**:深色主题幻灯片，20 张，以数字为主角的设计，约 90 秒生成完毕

---

## 常见陷阱

### 没有来源的指标

阶段 1 会提取指标但不核实它们。阶段 2 负责核实。如果你处于 Concept 模式，演讲中提到的任何指标都必须在摘要里明确给出来源——否则就删掉。听众会问"那个数字从哪来的?"，而"我查过了"不是一个答案。

### 信息过载的幻灯片

Kimi 提示词强制每张幻灯片 30 个词，但你在阶段 5 写的 pitch.md 可能会偏向项目符号列表。用"每张幻灯片一个想法"规则来检验:如果你需要用"和"来描述一张幻灯片的内容，就把它拆开。

### 跳过 CHECKPOINT

在没有验证过角度 + 标题的情况下运行阶段 5，会为错误的演讲产出一份技术上正确的讲稿。阶段 4 的推荐是一个好的起点，而非最终答案——你对受众的了解才是关键。

### 反馈初稿发得太晚

反馈初稿在阶段 4 生成，那时讲稿还不存在。这是有意为之——在角度/标题阶段获得同行反馈是可付诸行动的。对一份已完成的讲稿提反馈，大多只会让人后悔。

### 泛泛而谈的演讲者备注

`pitch.md` 中的演讲者备注应当读起来像自然口语。如果你发现自己在写"在这张幻灯片中，我们讨论……"，就把它改写成你真正会对全场说的话。Kimi 提示词会照搬这些备注——它们需要是对话式的。

---

## 展示的设计模式

从 Claude Code 的视角看，这条流水线很有意思，因为它在一个连贯的系统中演示了若干高级模式。

### 基于文件状态的 Skill 链式调用

每个阶段写出文件，供下一阶段读取。状态通过文件系统在多次 skill 调用之间持久化——没有内存中的耦合。你可以在阶段 2 之后一周再运行阶段 3，而不会丢失上下文。

```
Stage 1 → writes {slug}-summary.md
Stage 2 → reads {slug}-summary.md → writes 3 new files
Stage 3 → reads summary + timeline → writes 2 new files
...
```

### 工具权限范围限定

阶段 2 是唯一需要 Bash 的阶段（用于 git 命令）。其他每个阶段都只用 Read + Write。这是有意为之——每个阶段的最小足迹意味着犯错的面更小。

```yaml
# Stage 2 only
allowed-tools:
  - Write
  - Read
  - Bash
```

### 人在回路关卡

阶段 4 使用 `AskUserQuestion` 来呈现 CHECKPOINT——不是为了方便，而是作为一项结构性要求。没有明确的人工响应，该 skill 不会推进到阶段 5。这正是"Claude 提议，人来决定"的模式。

### AI 到 AI 的交接

阶段 5 为第二个 AI 系统（Kimi）生成提示词。Claude 并不直接生成幻灯片——它生成由另一个 AI 执行的规格。这种模式让你能够结合各自的长处:Claude 负责结构化的叙事推理，Kimi 负责视觉演示文稿生成。

```
Claude (Stage 5) → kimi-prompt.md → Kimi.com → slides.pptx
```

### 两种执行模式与条件性阶段跳过

`--rex` / `--concept` 标志控制哪些阶段运行。在 Concept 模式下阶段 2 会自动跳过。编排器（`/talk-pipeline`）负责路由——各个阶段的 skill 本身与模式无关。

---

## 另见

- **Skill 模板**: [`examples/skills/talk-pipeline/`](../../examples/skills/talk-pipeline/)
- **PDF 生成工作流**: [`guide/workflows/pdf-generation.md`](./pdf-generation.md)——用于从演讲内容生成讲义
- **Spec-First 工作流**: [`guide/workflows/spec-first.md`](./spec-first.md)——与 Claude 进行结构化工作的互补模式
- **Skill 结构参考**: [`examples/skills/skill-creator/SKILL.md`](../../examples/skills/skill-creator/SKILL.md)

---

**最后更新**: 2026 年 2 月
