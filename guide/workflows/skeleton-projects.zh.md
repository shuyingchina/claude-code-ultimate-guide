---
title: "Skeleton Projects Workflow"
description: "Use existing battle-tested repositories as scaffolding for new projects"
tags: [workflow, architecture, template]
---

# 骨架项目工作流

复用现有的、经过实战检验的仓库作为新项目的脚手架，而不是从零开始。

---

## 何时使用

- **启动一个新项目**，且技术栈已经确定
- 在多个服务之间**标准化团队模式**
- 架构决策已经做好的**快速原型开发**
- 通过一个可运行的参考项目**帮助新团队成员入门**

**不要使用的场景**：探索未知技术（请改用 [Vibe Coding](#98-vibe-coding-skeleton-projects)），或者需求过于独特、现有模板无法匹配时。

---

## 前置条件

- 已安装并配置好 Claude Code
- 拥有访问参考仓库的 Git 权限
- 对目标项目需求有清晰的理解

---

## 分步指南

### 阶段 1：寻找并评估一个骨架

不要从零构建。找到一个与你目标架构相匹配的现有仓库。

**第 1 步：搜索候选项**

```bash
# Ask Claude to help find reference repos
claude -p "I need a skeleton for a Next.js 15 app with:
- App Router
- Prisma ORM with PostgreSQL
- tRPC for type-safe API
- Tailwind CSS
- Jest + Playwright testing

Search GitHub for well-maintained starter templates.
Evaluate the top 3 by: last commit date, stars, dependency freshness, test coverage."
```

**第 2 步：克隆并审计**

```bash
git clone <candidate-repo> skeleton-eval
cd skeleton-eval
claude
```

```markdown
User: Audit this repository as a potential skeleton for our project:
1. List all dependencies and their versions (flag outdated ones)
2. Assess code quality: patterns, consistency, test coverage
3. Identify what we'd keep vs. what we'd remove
4. Flag any security concerns (vulnerable deps, exposed secrets)
5. Rate overall suitability (1-5) with specific justification
```

**第 3 步：使用 sub-agents 评估**（用于深入分析）

```markdown
User: Run a multi-perspective evaluation of this skeleton:

Agent 1 (Security): Check for vulnerabilities, hardcoded secrets, unsafe patterns
Agent 2 (Architecture): Assess modularity, separation of concerns, scalability
Agent 3 (DX): Evaluate developer experience - setup time, documentation, tooling

Synthesize findings into a go/no-go recommendation.
```

### 阶段 2：Fork 并定制

**第 4 步：从骨架创建你的项目**

```bash
# Create new repo from skeleton
mkdir my-project
cp -r skeleton-eval/. my-project/
cd my-project
rm -rf .git
git init
```

**第 5 步：用 Claude 精简并适配**

```markdown
User: Customize this skeleton for our project "Acme Dashboard":

1. Remove: example routes, demo data, sample tests
2. Keep: config structure, auth setup, database schema pattern, CI pipeline
3. Update: package.json (name, description, version 0.1.0)
4. Add: our CLAUDE.md with project conventions
5. Verify: `pnpm install && pnpm build && pnpm test` all pass after changes

Important: Don't break the working skeleton. Each removal should be followed
by a build check.
```

### 阶段 3：从骨架扩展到 MVP

**第 6 步：构建第一个真实功能**

```markdown
User: Using the patterns established in this skeleton, implement our first feature:
User Authentication (login + registration + password reset)

Follow the skeleton's existing patterns for:
- Route structure (match the example routes pattern)
- Service layer (match the existing service pattern)
- Test structure (match the example test pattern)
- Error handling (match the existing error pattern)

Create a task plan before starting implementation.
```

**第 7 步：验证骨架完整性**

```markdown
User: Now that we have one real feature, verify the skeleton still works:
1. Run full test suite
2. Check that the CI pipeline passes
3. Verify no skeleton patterns were broken
4. Confirm new code follows skeleton conventions consistently
```

### 阶段 4：记录并迭代

**第 8 步：在 CLAUDE.md 中记录决策**

```markdown
User: Update CLAUDE.md with:
1. Which skeleton we started from (repo URL, commit hash)
2. What we kept and why
3. What we removed and why
4. Any pattern deviations from the original skeleton
5. Conventions we've added on top
```

---

## 骨架扩展时间线

```
Skeleton (Day 1)     →    MVP (Week 1)      →    Production (Month 1)
──────────────────────────────────────────────────────────────────────
1 example route      →    5 real routes      →    20+ routes
1 example test       →    30 tests           →    200+ tests
Basic config         →    Env-based config   →    Multi-env + secrets
SQLite/local DB      →    Docker PostgreSQL  →    Managed DB + migrations
No CI                →    Basic CI           →    Full CI/CD pipeline
README only          →    CLAUDE.md + ADRs   →    Full documentation
```

---

## 真实案例：从骨架构建微服务

```bash
# 1. Clone proven skeleton
git clone https://github.com/example/express-prisma-starter skeleton
cd skeleton && claude

# 2. Audit (2 minutes)
User: "Audit this skeleton. Is it suitable for a billing microservice?"
# Claude: Reports deps, patterns, suitability score

# 3. Customize (5 minutes)
User: "Strip examples, rename to billing-service, add our CLAUDE.md"
# Claude: Removes demo code, updates config, adds project context

# 4. First feature (30 minutes)
User: "Implement invoice creation endpoint following skeleton patterns"
# Claude: Creates route, service, repo, tests matching skeleton conventions

# 5. Verify (2 minutes)
User: "Run all tests, verify build, check skeleton patterns preserved"
# Claude: All green, patterns consistent
```

---

## 常见陷阱

| 陷阱 | 症状 | 解决方法 |
|---------|---------|-----|
| 骨架过于复杂 | 花在精简上的时间比构建还多 | 选择更简单的骨架，或自己构建一个最小化的骨架 |
| 依赖过时 | 安装时出现安全警告 | 克隆前检查最后提交日期（理想情况 < 6 个月） |
| 破坏骨架模式 | 新代码偏离了骨架约定 | 将骨架模式作为约束写入 CLAUDE.md |
| 保留死代码 | 未使用的示例代码使项目变得杂乱 | 在阶段 2 中彻底精简，每次删除后验证构建 |
| 缺少文档 | 忘记为什么选择该骨架 | 立即在 CLAUDE.md 中记录（阶段 4） |

---

## 相关工作流

- **[Vibe Coding](#98-vibe-coding-skeleton-projects)**：在选择骨架之前先进行探索
- **[计划驱动开发](./plan-driven.md)**：在执行之前规划骨架的定制化
- **[与 Claude 进行 TDD](./tdd-with-claude.md)**：以测试优先的方式扩展骨架功能
- **[排列组合框架](#919-permutation-frameworks)**：在最终确定之前测试多个骨架变体

---

**最后更新**：2026 年 1 月
