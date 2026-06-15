---
title: "Code Review (Claude Code feature)"
description: "Automated multi-agent PR review for Teams and Enterprise — setup, triggers, REVIEW.md configuration, and cost management"
tags: [feature, teams, enterprise, github, code-review]
---

# Code Review

> **可用性**：研究预览（Research preview）——仅限 Teams 和 Enterprise 套餐。Free/Pro 账户不可用，启用了零数据保留（Zero Data Retention，ZDR）的组织也不可用。
> **发布时间**：2026 年 3 月 9 日

Claude Code 的 Code Review 功能会对每一个 GitHub pull request 运行多 agent 审查。一队专门的 agents 会在完整代码库的语境中检查 diff，每个 agent 负责寻找一类不同的问题（逻辑错误、安全漏洞、边界情况、回归），随后再进行一轮验证以过滤误报。

发现的问题会作为内联 PR 评论发布在出现问题的具体行上，并按严重程度标记。审查不会批准或阻止 PR，因此现有的审查工作流保持不变。

---

## 工作原理

1. 触发器触发（PR 打开、推送，或手动 `@claude review` 评论）
2. 多个 agents 在 Anthropic 基础设施上并行分析 diff 及其周边代码
3. 每个 agent 针对一类不同的问题
4. 一个验证步骤将候选问题与实际代码行为进行核对，以剔除误报
5. 结果经过去重、按严重程度排序，并作为内联 PR 评论发布
6. 如果没有发现问题，Claude 会发布一条简短的确认评论

审查平均在 **20 分钟内**完成，时长随 PR 规模和复杂度而变化。

### 严重程度分级

| 标记 | 严重程度 | 含义 |
|:-------|:---------|:--------|
| 🔴 | Normal | 应在合并前修复的 bug |
| 🟡 | Nit | 小问题，值得修复但不阻塞 |
| 🟣 | Pre-existing | 代码库中已存在、并非本 PR 引入的 bug |

每条发现都包含一个可折叠的扩展推理区，解释 Claude 为何标记该问题，以及它是如何验证这个问题的。

---

## 设置

由管理员为整个组织一次性启用 Code Review，并选择要纳入的代码仓库。

### 1. 打开管理员设置

前往 [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) 并找到 **Code Review** 部分。需要同时拥有 Claude 组织的管理员权限，以及在你的 GitHub 组织中安装 GitHub Apps 的权限。

### 2. 点击 Setup

这将启动 GitHub App 安装流程。

### 3. 安装 Claude GitHub App

按照提示在你的 GitHub 组织中安装 Claude GitHub App。该 app 请求以下权限：

- **Contents**：read and write
- **Issues**：read and write
- **Pull requests**：read and write

Code Review 使用对 contents 的读取权限和对 pull requests 的写入权限。这套权限集也支持 [GitHub Actions](./github-actions.md)，以便你日后启用。

### 4. 选择代码仓库

选择要启用的代码仓库。如果某个仓库缺失，请确认你在安装时已为 GitHub App 授予了访问权限。你之后可以从管理员设置表格中添加更多仓库。

### 5. 为每个仓库设置审查触发器

为每个代码仓库选择审查何时运行：

| 触发器 | 何时运行 | 成本特征 |
|---------|-------------|--------------|
| **Once after PR creation** | 在 PR 打开或被标记为 ready 时运行一次 | 最低 |
| **After every push** | 每次向 PR 分支推送时运行 | 最高（按推送次数倍增） |
| **Manual** | 仅当有人评论 `@claude review` 时运行 | 受控 |

在发出 `@claude review` 评论之后，无论配置的触发器是什么，该 PR 后续的推送都会自动触发审查。

**Manual 模式**适用于高流量仓库——你希望对特定 PR 主动开启审查，或仅在 PR 准备好审查后才开始审查。

---

## 手动触发

在任何已打开、非草稿（non-draft）的 PR 上评论 `@claude review`，即可立即启动审查。要求：

- 顶层 PR 评论（不是内联 diff 评论）
- 评论开头为 `@claude review`
- 在该仓库拥有 owner、member 或 collaborator 访问权限

如果已有审查正在运行，该请求会排队，直到正在进行的审查完成。

---

## 配置审查

有两个文件控制 Claude 标记哪些内容。两者都是在默认正确性检查之上的叠加。

### CLAUDE.md

Claude 会读取你目录层级中的所有 `CLAUDE.md` 文件。新引入的违规会被标记为 nit 级别的发现。这是双向的：如果某个 PR 使某条 `CLAUDE.md` 陈述过时，Claude 也会标记文档需要更新。

将 `CLAUDE.md` 用于那些同样适用于交互式 Claude Code 会话的指引。

### REVIEW.md

将 `REVIEW.md` 添加到你的**仓库根目录**，用于仅限审查的规则。会被自动发现，无需任何配置。

```markdown
# Code Review Guidelines

## Always check
- New API endpoints have corresponding integration tests
- Database migrations are backward-compatible
- Error messages don't leak internal details to users

## Style
- Prefer early returns over nested conditionals
- Use structured logging, not f-string interpolation in log calls

## Skip
- Generated files under `src/gen/`
- Formatting-only changes in `*.lock` files
- Migration files in `db/migrations/`
```

将 `REVIEW.md` 用于那些会让 `CLAUDE.md` 在通用会话中显得杂乱的规则（linter 约定、跳过列表、团队特定模式）。

---

## 定价

Code Review 按 token 用量计费，**与你套餐内包含的用量分开计算**（通过[额外用量](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)）。

- 平均成本：**每次审查 $15–25**，随 PR 规模、代码库复杂度，以及需要验证的问题数量而变化
- "After every push" 会使成本按推送次数倍增
- 设置每月支出上限：[claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) → 为 "Claude Code Review" 服务配置限额
- 监控支出：[claude.ai/analytics/code-review](https://claude.ai/analytics/code-review)（每日 PR 数、每周支出、按仓库细分）

---

## 交叉引用

针对手动代码审查工作流（CLI，无需 Teams/Enterprise）：
- [多 agent 代码审查工作流](#split-role-sub-agents) —— 通过 CLI 自建 agent 团队
- [GitHub Actions 集成](./github-actions.md) —— 自定义 CI/CD 自动化（本托管服务的自托管替代方案）
- GitLab CI/CD —— 用于 GitLab 流水线的自托管 Claude 集成
- Code Review 插件 —— 推送前的按需本地审查（可在插件市场获取）

---

## 已知限制（研究预览）

- 仅限 Teams 和 Enterprise —— Free/Pro 无法访问
- 启用了零数据保留（Zero Data Retention，ZDR）的组织不可用
- 托管服务仅支持 GitHub（GitLab 通过 CI/CD 集成支持，而非本功能）
- 大型仓库首次激活时存在全仓库索引延迟
- Anthropic 内部统计：在 >1000 行的 PR 中平均发现约 7.5 个问题，误报率 <1% —— 自行报告，未经独立验证
