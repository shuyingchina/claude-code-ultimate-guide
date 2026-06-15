---
title: "GitHub Actions Workflows with Claude Code"
description: "Production-ready patterns for automating PR reviews, issue triage, and quality gates with claude-code-action"
tags: [workflow, ci-cd, github-actions, automation]
---

# GitHub Actions Workflows with Claude Code

> **可信度**：Tier 1 —— Anthropic 官方 action（`anthropics/claude-code-action`，6.2k stars，v1.0）。

通过将 Claude 直接接入你的 GitHub 工作流，实现代码审查、issue 分类和质量门禁的自动化。两种触发模型：`@claude` 提及（由人发起）和定时/事件自动化（完全自主）。

---

## 目录

1. [TL;DR](#tldr)
2. [两种模型](#two-models)
3. [配置](#setup)
4. [模式 1：在 @claude 提及时进行 PR 代码审查](#pattern-1-pr-code-review-on-claude-mention)
5. [模式 2：推送时自动审查 PR](#pattern-2-automatic-pr-review-on-push)
6. [模式 3：Issue 分类与打标签](#pattern-3-issue-triage-and-labeling)
7. [模式 4：安全聚焦审查](#pattern-4-security-focused-review)
8. [模式 5：定时仓库维护](#pattern-5-scheduled-repo-maintenance)
9. [认证备选方案](#authentication-alternatives)
10. [成本控制](#cost-control)
11. [安全检查清单](#security-checklist)
12. [参见](#see-also)

---

## TL;DR

```yaml
# Minimal working example — paste into .github/workflows/claude.yml
name: Claude Code Review
on:
  issue_comment:
    types: [created]

jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

在任意 PR 上评论 `@claude review this PR` → Claude 会读取 diff 并发布一条审查意见。

---

## 两种模型

| 模型 | 触发方式 | 使用场景 |
|-------|---------|----------|
| **交互式** | 在 PR/issue 评论中提及 `@claude` | 按需审查、提问、修复 |
| **自动化** | push、PR 打开、定时、打标签 | 持续质量门禁、分类 |

两者使用同一个 action —— 区别在于 `on:` 块以及是否包含 `if:` 条件。

---

## 配置

### 快速开始（30 秒）

在你的 Claude Code 终端中，进入任意已连接 GitHub 仓库的项目：

```
/install-github-app
```

它会引导你完成创建 GitHub App、将 `ANTHROPIC_API_KEY` 添加到仓库 secrets，以及生成基础的 `claude.yml` 工作流。

### 手动配置

1. 将 `ANTHROPIC_API_KEY` 添加到你的 GitHub 仓库 secrets
2. 创建 `.github/workflows/claude.yml`（参见下方各模式）
3. 授予工作流权限：`contents: write`、`pull-requests: write`、`issues: write`

---

## 模式 1：在 @claude 提及时进行 PR 代码审查

由人发起。开发者评论 `@claude review this PR`，Claude 在评论中行内回复。

```yaml
# .github/workflows/claude-review.yml
name: Claude Interactive Review
on:
  issue_comment:
    types: [created, edited]
  pull_request_review_comment:
    types: [created]

jobs:
  claude:
    if: |
      contains(github.event.comment.body, '@claude') ||
      contains(github.event.review_comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          claude_env: |
            GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}
```

**用法示例：**
- `@claude review this PR` —— 完整 diff 分析并给出建议
- `@claude is this change backwards compatible?` —— 针对性提问
- `@claude fix the failing test in src/auth.test.ts` —— Claude 会开一个后续 PR 提交修复

---

## 模式 2：推送时自动审查 PR

每个 PR 在打开或更新的那一刻都会获得一次审查。无需提及。

```yaml
# .github/workflows/claude-auto-review.yml
name: Claude Auto PR Review
on:
  pull_request:
    types: [opened, synchronize]
    # Optional: only trigger on specific paths
    # paths:
    #   - 'src/**'
    #   - '!**/*.md'

jobs:
  claude-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Review this pull request. Focus on:
            - Logic errors and edge cases
            - Security issues (injection, auth, secrets)
            - Performance regressions
            - Missing error handling

            Format your response as:
            ## Summary
            One paragraph describing the change.

            ## Issues Found
            Numbered list, severity (Critical/Major/Minor), file:line reference.

            ## Suggestions
            Optional improvements.

            Keep it under 400 words. Be direct.
```

**提示**：添加 `paths:` 以避免在纯文档 PR 上触发，或用 `if: github.event.pull_request.draft == false` 跳过草稿 PR。

---

## 模式 3：Issue 分类与打标签

Claude 读取新 issue，分配标签，并发布一条结构化的分类评论。

```yaml
# .github/workflows/claude-triage.yml
name: Issue Triage
on:
  issues:
    types: [opened]

jobs:
  triage:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      contents: read
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Triage this GitHub issue:

            1. Assign one label from: bug, enhancement, question, documentation, performance, security
            2. Assign a priority label: priority:critical, priority:high, priority:medium, priority:low
            3. Post a comment with:
               - Issue type classification
               - Which component is likely affected (based on the issue description)
               - Next step recommendation for the reporter (reproduce steps needed? version info missing?)

            Be brief. One sentence per point.
```

---

## 模式 4：以安全为中心的审查

专门针对涉及敏感路径（认证、支付、配置）的 PR 运行。

```yaml
# .github/workflows/claude-security.yml
name: Security Review
on:
  pull_request:
    paths:
      - 'src/auth/**'
      - 'src/payments/**'
      - '**/config/**'
      - '**/.env*'
      - '**/secrets/**'

jobs:
  security-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Perform a security-focused review of this PR. Check for:

            - Injection vulnerabilities (SQL, command, LDAP)
            - Authentication and authorization bypasses
            - Secrets or credentials in code or comments
            - Insecure direct object references
            - Missing input validation
            - Unsafe deserialization
            - OWASP Top 10 patterns

            Rate overall risk: Low / Medium / High / Critical.
            If High or Critical, add the label 'security-review-required'.
            List each finding with: file:line, vulnerability type, and recommended fix.
```

---

## 模式 5：定时仓库维护

每周健康检查——无需任何人工触发即可运行。

```yaml
# .github/workflows/claude-maintenance.yml
name: Weekly Repo Health Check
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9am UTC
  workflow_dispatch:       # Also allows manual trigger

jobs:
  maintenance:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
    steps:
      - uses: actions/checkout@v4

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Perform a weekly repository health check:

            1. Scan package.json (or equivalent) for outdated major dependencies
            2. Check for TODO/FIXME comments older than 30 days in src/
            3. Identify any test files without corresponding implementation files
            4. List any documentation files that reference deleted or renamed files

            Open a GitHub issue titled "Weekly Health Check - [date]" with your findings.
            If nothing requires attention, post a comment "Health check passed — no issues found."
```

---

## 认证替代方案

上述示例直接使用 `ANTHROPIC_API_KEY`。对于使用云服务提供商的团队：

**Amazon Bedrock：**
```yaml
- uses: anthropics/claude-code-action@v1
  with:
    use_bedrock: 'true'
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    AWS_REGION: us-east-1
    ANTHROPIC_MODEL: 'anthropic.claude-3-5-sonnet-20241022-v2:0'
```

**Google Vertex AI：**
```yaml
- uses: anthropics/claude-code-action@v1
  with:
    use_vertex: 'true'
  env:
    ANTHROPIC_VERTEX_PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
    CLOUD_ML_REGION: us-east5
    ANTHROPIC_MODEL: 'claude-3-5-sonnet-v2@20241022'
```

云服务提供商可受益于数据驻留合规性，并能利用现有的 IAM 策略，而无需单独管理一个 API key。

---

## 成本控制

自动化工作流在没有人工介入的情况下运行——请设置明确的限额。

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    # Cap spend per workflow run
    claude_args: '--max-budget-usd 0.50'
    # Use Haiku for triage, Sonnet for reviews — don't default to Opus
    prompt: |
      ...
```

**各模式的预算指引：**

| 模式 | 模型 | 每次运行约计成本 |
|---------|-------|--------------------|
| PR 审查（中等规模 PR） | Sonnet | $0.05–0.15 |
| Issue 分类 | Haiku | $0.01–0.03 |
| 安全审查（大型 PR） | Sonnet | $0.10–0.25 |
| 定时维护 | Sonnet | $0.05–0.20 |

使用 `ccusage` 或 Anthropic Console 用量仪表板监控实际开销。

**防止成本失控：**
- 使用 `paths:` 过滤器，避免在无关变更上触发
- 添加 `if: github.event.pull_request.draft == false` 以跳过草稿 PR
- 设置 `concurrency:` 以防止在同一 PR 上并行运行

```yaml
jobs:
  claude-review:
    concurrency:
      group: claude-${{ github.event.pull_request.number }}
      cancel-in-progress: true
```

---

## 安全检查清单

在部署到团队仓库之前：

- [ ] `ANTHROPIC_API_KEY` 作为 GitHub secret 存储，绝不写入工作流 YAML 中
- [ ] 工作流权限保持最小化——除非确实需要写入，否则使用 `contents: read`
- [ ] 对于公开仓库：添加 `if: github.event.pull_request.head.repo.full_name == github.repository`，以防止来自 fork 的 PR 触发 API 调用
- [ ] 审查工作流公开发布的内容——Claude 的评论对所有贡献者可见
- [ ] 谨慎使用 `pull_request_target`——即使来自 fork，它也会以写入权限运行

**Fork 安全模式（公开仓库）：**
```yaml
jobs:
  claude:
    # Only run on PRs from the same repo, not forks
    if: github.event.pull_request.head.repo.full_name == github.repository
```

---

## 另见

- [第 9.3 节 CI/CD 集成](#93-cicd-integration) —— headless 模式、Unix 管道、`--output-format json`
- [生产环境安全](../security/production-safety.md) —— 自动化 agent 的护栏
- [安全加固](../security/security-hardening.md) —— MCP 与 webhook 安全
- [官方 action 文档](https://github.com/anthropics/claude-code-action) —— 解决方案指南、迁移、云服务提供商
- [社区工作流蓝图](https://github.com/alirezarezvani/claude-code-github-workflow) —— 面向进阶团队的 8 个工作流 + 4 个自主 agent
