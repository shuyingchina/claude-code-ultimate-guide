---
title: "致谢与外部灵感来源"
description: "其工作为本指南中特定模式提供启发的开源项目与工程团队"
tags: [credits, attribution, open-source]
---

# 致谢与外部灵感来源

本指南记录了来自 Claude Code 社区的各种模式。部分章节直接受到开源仓库、博客文章或公开工程工作的启发。本页面将这些致谢信息集中归整到一处。

---

## Packmind 工程团队

**仓库**：[github.com/packmind/packmind](https://github.com/packmind/packmind)
**作者**：Cédric Teyton（CTO, Packmind）
**许可证**：Apache 2.0

Packmind 在其开源仓库中维护了一套生产级的 Claude Code 配置。本指南记录的多个模式正是受到他们 `.claude/` 配置的启发：

### 模式 1：MCP 参考文件

**指南章节**：[为 Claude 记录 MCP 文档](../ecosystem/mcp-servers-ecosystem.md#documenting-an-mcp-for-claude-the-reference-file-pattern)
**来源**：`.claude/skills/datadog-analysis/references/datadog_mcp.md`

一个 `references/<mcp-name>.md` 文件，由 skill 在任何 MCP 调用之前读取。它记录了查询语法的陷阱、必需的参数组合、可用示例，以及针对某个特定 MCP 服务器的噪声排除规则。

### 模式 2：怀疑型审查 Sub-Agent

**指南章节**：[模式：怀疑型审查 Sub-Agent](../ultimate-guide.md#pattern-skeptical-reviewer-sub-agent)
**来源**：`.claude/skills/playbook-audit/references/report-agent.md`

多智能体审计流水线中的第四个 agent，其职责是剔除前三个 agent 产生的误报。它依据明确的误报判定标准运作，并要求在保留任何结论之前同时提供两个产物中的证据。

### 模式 3：共享事实基线注入

**指南章节**：[Skill 设计模式](./skill-design-patterns.md#shared-ground-truth-injection)
**来源**：`.claude/skills/doc-audit/SKILL.md`

编排器先一次性计算出一份共享的事实基线（导航结构、CLI 命令、文件列表），然后将同一个信息块注入到所有并行 sub-agent 的提示词中。这样可以避免每个 sub-agent 各自独立地重新发现相同的事实。

### 模式 4：通过 frontmatter 路径预筛选参考资料

**指南章节**：[Skill 设计模式](./skill-design-patterns.md#pre-filtered-references-via-frontmatter-paths)
**来源**：`.claude/skills/qa-review/SKILL.md`

编排器读取规则文件，解析 `paths:` frontmatter 中的 glob 模式，将其与已修改的文件进行匹配，然后只把适用的规则传递给每个审查 agent。这是将渐进式披露应用到规范标准上，而不仅仅是文档。

### 模式 5：带合并语义的交接三件套

**指南章节**：[会话交接模式](../ultimate-guide.md#session-handoff-pattern)，以及位于 `examples/commands/handoff/` 的模板
**来源**：`.claude/commands/create-handoff.md`、`resume-handoff.md`、`update-handoff.md`

一个用于会话连续性的三命令协议：`create-handoff` 初始化一份结构化文档，`update-handoff` 应用针对特定章节的合并规则（工作日志采用仅追加，状态采用替换），`resume-handoff` 则将最新文档加载到上下文中。

### 模式 6：带上下文验证检查点的配方模板

**指南章节**：[Skill 设计模式](./skill-design-patterns.md#recipe-template-and-context-validation-checkpoints)，以及位于 `examples/commands/recipe-template.md` 的模板
**来源**：Packmind 各命令文件中反复出现的模式

一种命令模板结构，其中的"Context Validation Checkpoints"（上下文验证检查点）章节列出了 Claude 在执行配方步骤之前必须核实的前置条件。这能减少因上下文缺失或环境错误而导致的错误。

---

## Packmind context-evaluator

**仓库**：[github.com/PackmindHub/context-evaluator](https://github.com/PackmindHub/context-evaluator)
**作者**：Packmind 工程团队
**许可证**：MIT

context-evaluator 是一个开源的 CLAUDE.md / AGENTS.md 质量分析器。本指南从其源码中提取了两个模式：

### 模式 7：运行时提示词日志

**指南章节**：[Skill 设计模式](./skill-design-patterns.md#runtime-prompt-logging)
**来源**：`src/shared/evaluation/runtime-prompt-logger.ts`

在调用 AI 提供商之前，始终以阻塞方式将完整的评估器提示词写入 `prompts/debug/`。它能在提供商崩溃和超时的情况下保留下来，且永远不会抛出异常。它独立于 `--debug` 标志。

### 模式 8：自适应的统一/并行模式

**指南章节**：[Skill 设计模式](./skill-design-patterns.md#adaptive-unifiedparallel-mode)
**来源**：`src/shared/evaluation/runner.ts` — `canUseUnifiedMode()`

基于 token 阈值在两种模式之间切换：单智能体统一评估（用于跨文件检测）与每个文件独立的并行 agent。默认阈值为 100K tokens。

---

## Anthropic 工程团队

**skill-creator**：Packmind 仓库中内置（并在本指南的 skill 评估章节中引用）的 `skill-creator` skill 最初由 Anthropic 发布。它包含了用于测试 skills 的规范化评估框架：evals 文件系统约定、盲测 A/B 对比器、描述优化循环，以及基准聚合脚本。

---

## 向本文件添加条目

当某个指南章节直接受到外部开源工作的启发或改编时，请在此处添加一条记录。需包含：
- 仓库 URL
- 作者 / 组织名称
- 许可证
- 借鉴了哪个模式，以及来自哪个源文件
- 它出现在哪个指南章节
