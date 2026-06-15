---
title: "Claude Cowork: Agentic Desktop for Knowledge Work"
description: "Summary of Claude's agentic desktop feature for non-technical knowledge workers"
tags: [guide, agents, workflows]
---

# Claude Cowork：面向知识工作的智能体桌面

> **📦 完整文档已迁移至专用仓库**
> 本文件为摘要。完整文档请参见：
> **https://github.com/FlorianBruniaux/claude-cowork-guide**

---

## 快速概览

**Cowork** 是 Claude 的智能体桌面功能，它通过 Claude Desktop 应用将自主 AI 能力扩展到非技术用户。Cowork 不依赖终端命令，而是直接访问本地文件夹和文件。

### 关键信息

| 方面 | 详情 |
|--------|---------|
| **状态** | 研究预览版（2026 年 1 月） |
| **使用门槛** | Pro（$20/月）或 Max（$100-200/月）订阅，仅限 macOS |
| **侧重点** | 文件操作、文档生成、整理归类 |
| **与 Code 的区别** | 不执行代码——仅处理文件 |

---

## 三款 Claude 工具：哪一款适合你？

三款工具，一个订阅（$20/月 Pro）。它们相辅相成，而非相互竞争。

| | Claude AI | Claude Code | Cowork |
|---|-----------|-------------|--------|
| **界面** | Web / 移动端 | 终端（CLI） | 桌面应用 |
| **标语** | 你来写作、思考、检索 | 你来规模化编码 | 你无需写代码即可自动化 |
| **定义** | 通用型对话助手 | 面向完整代码库的自主智能体 | 面向非开发者的智能体文件工作流 |
| **主要用例** | 写作、头脑风暴、研究 | 调试、重构、测试 | 文件整理、PDF 提取、跨应用工作流 |
| **执行代码** | 否 | 是 | 否 |
| **文件系统访问** | 仅上传 | 完全访问 | 文件夹沙箱 |
| **所需配置** | 无 | npm install -g @anthropic-ai/claude-code | 安装 macOS 应用 |
| **成熟度** | 正式版 | 正式版 | 研究预览版 |
| **理想用户画像** | 写作者 · 顾问 · 学生 | 开发者 · 工程师 · 技术负责人 | 运营 · 助理 · 中小企业非技术人员 |
| **主要取舍** | 无系统访问能力 | 大型项目上的 token 成本 | 仅限 macOS，配置有限 |

→ [完整的 Cowork 与 Code 对比](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/reference/comparison.md)

### 决策指南

- **撰写文档或做研究？** → Claude AI
- **编码：重构、调试、测试？** → Claude Code（你来对地方了）
- **整理文件、提取 PDF、无需写代码？** → Cowork

---

## 用例

- **文件整理** — 杂乱的文件夹 → 井然有序的结构
- **报销追踪** — 收据 → Excel 报表
- **报告汇总** — 多份文档 → 统一报告
- **会议准备** — 调研 → 简报文档

→ [详细工作流](https://github.com/FlorianBruniaux/claude-cowork-guide/tree/main/workflows)

---

## 安全要点

目前尚无官方安全文档。必备实践：

1. **专用工作区** — 切勿授予对 Documents/Desktop 的访问权限
2. **审查计划** — 在批准前检查每一项操作
3. **不放凭据** — 将敏感数据排除在工作区之外
4. **先备份** — 在执行破坏性操作之前

→ [完整安全指南](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/guide/03-security.md)

---

## 文档

| 资源 | 说明 |
|----------|-------------|
| **[完整文档](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/README.md)** | Cowork 完整指南中心 |
| **[快速上手](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/guide/01-getting-started.md)** | 配置与首个工作流 |
| **[功能能力](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/guide/02-capabilities.md)** | Cowork 能做什么/不能做什么 |
| **[提示词库](https://github.com/FlorianBruniaux/claude-cowork-guide/tree/main/prompts)** | 50+ 个即用型提示词 |
| **[速查表](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/reference/cheatsheet.md)** | 1 页快速参考 |
| **[FAQ](https://github.com/FlorianBruniaux/claude-cowork-guide/blob/main/reference/faq.md)** | 常见问题 |

---

*返回 [AI 生态系统指南](ecosystem/ai-ecosystem.md) | [终极指南](./ultimate-guide.md) | [主 README](../README.md)*
