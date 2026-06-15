---
title: "Production Safety Rules"
description: "Non-negotiable safety rules for teams deploying Claude Code in production environments"
tags: [security, guide, devops]
---

# 生产环境安全规则

> **适用对象**：在生产环境中部署 Claude Code 的团队。
> **个人学习者**：请改为参阅 [Getting Started](#getting-started)。

---

## TL;DR（30 秒速览）

**面向生产团队的 6 条不可妥协规则**：

1. ✅ **端口稳定性**：绝不更改后端/前端端口
2. ✅ **数据库安全**：执行破坏性操作前务必备份
3. ✅ **功能完整性**：绝不交付半成品功能
4. ✅ **基础设施锁定**：Docker/环境变更需要授权
5. ✅ **依赖安全**：未经批准不得引入新依赖
6. ✅ **遵循模式**：符合现有代码库的约定

---

## 何时使用这些规则

| 项目类型 | 是否使用这些规则？ | 原因 |
|--------------|------------------|-----|
| 学习 / 教程 | ❌ 否 | 对探索而言过于严格 |
| 个人原型 | ❌ 否 | 开销不值得 |
| 小团队（2-3 人）、预发布环境 | ⚠️ 部分 | 仅规则 1、3、6 |
| 生产应用、多开发者团队 | ✅ 是 | 全部 6 条规则 |
| 受监管行业（HIPAA、SOC2） | ✅ 是 + 增加合规规则 | 关键安全 |

---

## 规则 1：端口稳定性

### 问题所在

更改端口会破坏：
- 本地开发环境
- Docker Compose 配置
- 已部署的服务配置
- 团队成员的设置

**真实事故**：重构期间后端端口从 3000 → 8080 更改。所有开发者花了一天重新配置本地环境。预发布部署静默失败，因为 nginx 代理仍指向 3000。

### 规则

**未经团队明确许可，绝不修改后端/前端端口。**

### 实现方式

**方案 A：在 `settings.json` 中拒绝权限**

```json
{
  "permissions": {
    "deny": [
      "Edit(docker-compose.yml:*ports*)",
      "Edit(package.json:*PORT*)",
      "Edit(.env.example:*PORT*)",
      "Edit(vite.config.ts:*port*)"
    ]
  }
}
```

**方案 B：预提交 hook**

```bash
# .claude/hooks/PreToolUse.sh
if [[ "$TOOL" == "Edit" ]]; then
    FILE=$(echo "$INPUT" | jq -r '.tool.input.file_path')
    CONTENT=$(echo "$INPUT" | jq -r '.tool.input.new_string')

    if [[ "$FILE" =~ (docker-compose|vite.config|package.json) ]] && \
       [[ "$CONTENT" =~ (port|PORT):[[:space:]]*[0-9] ]]; then
        echo "⚠️ BLOCKED: Port modification detected in $FILE"
        echo "Ports must remain stable across team. Request permission first."
        exit 2
    fi
fi
```

**方案 C：CLAUDE.md 约束**

```markdown
## Port Configuration

**CRITICAL**: Ports are locked for team coordination.

Current ports:
- Frontend (Vite): 5173
- Backend (Express): 3000
- Database: 5432

To change ports:
1. Create RFC document in `/docs/rfcs/`
2. Get team approval (3+ reviewers)
3. Update all environments simultaneously
4. Notify team 48h in advance
```

### 边界情况

| 场景 | 行为 |
|----------|----------|
| 添加全新服务 | OK（不会破坏现有服务） |
| 更改测试环境端口 | OK（与开发/生产隔离） |
| 机器上的端口冲突 | 请用户在本地解决（.env.local） |

---

## 规则 2：数据库安全

### 问题所在

生产环境中的误删除 = 数据丢失。

**真实事故**：
- `DELETE FROM users WHERE id = 123` → 忘记 `WHERE` → 所有用户被删除
- 清理期间执行 `DROP TABLE sessions` → 生产表被删除
- 迁移回滚 → 因无备份导致数据丢失

### 规则

**执行破坏性操作前务必备份。**

破坏性操作：
- `DELETE FROM`（不带 `LIMIT 1`）
- `DROP TABLE`
- `TRUNCATE`
- `ALTER TABLE ... DROP COLUMN`
- 无法回滚的数据库迁移

### 实现方式

**方案 A：强制备份的预工具 hook**

```bash
# .claude/hooks/PreToolUse.sh
#!/bin/bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool.name')

if [[ "$TOOL" == "Bash" ]]; then
    COMMAND=$(echo "$INPUT" | jq -r '.tool.input.command')

    # Detect destructive database operations
    if [[ "$COMMAND" =~ (DROP TABLE|DELETE FROM|TRUNCATE|ALTER.*DROP) ]]; then
        echo "🚨 BLOCKED: Destructive database operation detected"
        echo ""
        echo "Required steps:"
        echo "1. Create backup: pg_dump -U user dbname > backup_\$(date +%Y%m%d_%H%M%S).sql"
        echo "2. Verify backup size is reasonable"
        echo "3. Re-run after backup confirmation"
        exit 2
    fi
fi

exit 0
```

**方案 B：迁移安全包装器**

```bash
# scripts/safe-migrate.sh
#!/bin/bash
set -e

echo "🔍 Pre-migration checks..."

# 1. Check environment
if [[ "$NODE_ENV" == "production" ]]; then
    echo "❌ BLOCKED: Use migration service for production"
    exit 1
fi

# 2. Create backup
BACKUP_FILE="backups/pre-migration-$(date +%Y%m%d_%H%M%S).sql"
mkdir -p backups
pg_dump $DATABASE_URL > "$BACKUP_FILE"
echo "✅ Backup created: $BACKUP_FILE"

# 3. Run migration
echo "🚀 Running migration..."
npm run prisma:migrate:dev

# 4. Verify
echo "🔍 Verifying database state..."
npm run prisma:validate

echo "✅ Migration complete. Backup: $BACKUP_FILE"
```

**方案 C：CLAUDE.md 协议**

```markdown

## 数据库操作

### 破坏性操作规程

**没有备份时绝不运行以下操作**：
- DELETE、DROP、TRUNCATE、ALTER...DROP

**必须执行的步骤**：
1. 在 #dev-ops Slack 频道发布通知
2. 创建备份：`./scripts/backup-db.sh`
3. 验证备份：`ls -lh backups/`（应大于 0 字节）
4. 先在 staging 环境执行
5. 等待 24 小时观察是否出现问题
6. 在 on-call 工程师在场的情况下在生产环境执行

**紧急回滚**：
```bash
psql $DATABASE_URL < backups/[latest].sql
```
```

### MCP 数据库安全

如果使用 MCP 数据库服务器（Postgres、MySQL 等）：

```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_URL": "postgres://readonly:***@dev-db.example.com:5432/appdb"
      },
      "comment": "READ-ONLY user for safety"
    }
  }
}
```

**关键**：为 MCP 使用只读数据库用户。参见 [数据隐私指南](./data-privacy.md#risk-2-mcp-database-access)。

---

## 规则 3：功能完整性

### 问题所在

当上下文不足时，Claude Code 有时会"敷衍了事"地实现功能：
- 删除现有功能，而不是修复 bug
- 为核心功能添加 `TODO` 注释
- 不处理错误状态
- 创建 mock 实现

**真实事故**：
- 通过完全移除校验来"修复"支付校验
- 用 `throw new Error("Not implemented")` 来"添加"错误处理
- 用 `// TODO: Add actual logic here` 来"完成"功能

### 规则

**绝不交付半成品功能。一旦开始，就要做到可正常工作的状态。**

### 实现方式

**方案 A：CLAUDE.md 约束**

```markdown
## Feature Implementation Standards

### NON-NEGOTIABLE

1. **No TODOs for core functionality**
   - TODOs allowed ONLY for future enhancements
   - Core features must be complete and working

2. **No mock implementations**
   - No `throw new Error("Not implemented")`
   - No fake data generators in production code paths

3. **Complete error handling**
   - Every async call has try/catch
   - Every user input is validated
   - Every API call has timeout and retry logic

4. **Downgrade = Delete the feature entirely**
   - If you can't fix properly, remove the feature
   - Document why in commit message
   - Create issue for proper implementation

### Validation

Before accepting changes, verify:
- [ ] No `TODO` in modified files (except future enhancements)
- [ ] No `throw new Error("Not implemented")`
- [ ] No commented-out code without explanation
- [ ] All new functions have error handling
```

**方案 B：pre-commit git hook**

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Check staged files for "half-assing" patterns
STAGED=$(git diff --cached --name-only --diff-filter=ACM)

for FILE in $STAGED; do
    if [[ "$FILE" =~ \.(ts|tsx|js|jsx|py)$ ]]; then
        # Check for TODOs in core logic (not tests)
        if ! [[ "$FILE" =~ test|spec ]]; then
            if git diff --cached "$FILE" | grep -E "^\+.*TODO.*implement|^\+.*Not implemented"; then
                echo "❌ COMMIT BLOCKED: TODO/Not implemented in $FILE"
                echo "   Complete the feature or remove it entirely."
                exit 1
            fi
        fi

        # Check for mock placeholders
        if git diff --cached "$FILE" | grep -E "^\+.*(MOCK_DATA|fakeData|placeholder)"; then
            echo "⚠️ WARNING: Mock data detected in $FILE"
            echo "   Ensure this is intentional for staging/dev only."
        fi
    fi
done

exit 0
```

**方案 C：输出评估命令**

```bash
# Before committing
/validate-changes

# This runs the output-evaluator agent (see examples/agents/output-evaluator.md)
# which scores changes on:
# - Correctness (10/10)
# - Completeness (10/10)  ← Detects half-assing
# - Safety (10/10)
```

---

## 规则 4：基础设施锁定

### 问题所在

Claude 可能在不了解生产环境影响的情况下修改基础设施配置：
- 修改 Docker Compose 卷 → 数据丢失
- 修改 `.env.example` → 破坏新成员上手流程
- 更新 Terraform → 意外的资源变更
- 调整 Kubernetes manifest → 服务中断

### 规则

**修改基础设施需要团队的明确许可。**

需要保护的文件：
- `docker-compose.yml`、`Dockerfile`
- `.env.example`（模板，不是个人的 .env.local）
- `kubernetes/`、`k8s/`、`terraform/`、`helm/`
- CI/CD 配置（`.github/workflows/`、`.gitlab-ci.yml`）
- 数据库 schema（需要 migration 评审）

### 实现方式

**方案 A：权限拒绝**

```json
{
  "permissions": {
    "deny": [
      "Edit(docker-compose.yml)",
      "Edit(Dockerfile)",
      "Edit(.env.example)",
      "Edit(terraform/**)",
      "Edit(kubernetes/**)",
      "Edit(.github/workflows/**)",
      "Edit(prisma/schema.prisma)"
    ]
  }
}
```

**方案 B：CLAUDE.md 规则**

```markdown
## Infrastructure Changes

You are **FORBIDDEN** from modifying these without explicit permission:

- `docker-compose.yml`, `Dockerfile`
- `.env.example` (template for new developers)
- `terraform/`, `kubernetes/` (infrastructure as code)
- `.github/workflows/` (CI/CD pipelines)
- `prisma/schema.prisma` (database schema)

**If infrastructure change is needed**:
1. Ask user: "This requires infrastructure change. Should I create an RFC?"
2. Create RFC document in `docs/rfcs/YYYYMMDD-<title>.md`
3. Do NOT modify files until RFC approved
```

**注意**：个人的 `.env.local` 文件可以修改（它们已被 gitignore）。

---

## 规则 5：依赖安全

### 问题

未经团队批准就添加依赖：
- 增大打包体积（影响性能）
- 引入安全漏洞
- 造成许可证合规问题
- 增加维护负担

**真实事故**：
- 在项目已有 `date-fns`（极小）的情况下添加了 `moment.js`（200KB）
- 项目使用 `ramda` 却安装了 `lodash`
- 添加 GPL 库 → 对专有代码库构成许可证违规

### 规则

**未经明确批准，不得添加新依赖。**

### 实现方式

**方案 A：对包管理器使用 permission deny**

```json
{
  "permissions": {
    "deny": [
      "Bash(npm install *)",
      "Bash(npm i *)",
      "Bash(pnpm add *)",
      "Bash(yarn add *)",
      "Bash(pip install *)",
      "Bash(poetry add *)"
    ],
    "allow": [
      "Bash(npm install)",
      "Bash(pnpm install)",
      "Bash(pip install -r requirements.txt)"
    ]
  }
}
```

**方案 B：CLAUDE.md 协议**

```markdown
## Dependency Management

### Immutable Stack Rule

**You are FORBIDDEN from adding new dependencies** (`npm install <package>`).

**If new dependency is needed**:
1. Check if existing dependency solves it:
   - Date manipulation? Use existing `date-fns`
   - HTTP requests? Use existing `axios`
   - State management? Use existing `zustand`
2. If genuinely needed, ASK:
   - "I need [package] for [reason]. Existing alternatives: [X, Y]. Should I add it?"
3. Wait for explicit approval
4. User will run: `npm install <package>` manually

**Allowed without asking**:
- `npm install` (installs existing package.json deps)
- Dev dependencies for testing (`-D` flag after approval)
```

**方案 C：pre-tool hook**

```bash
# .claude/hooks/PreToolUse.sh
if [[ "$TOOL" == "Bash" ]]; then
    COMMAND=$(echo "$INPUT" | jq -r '.tool.input.command')

    # Block dependency installation
    if [[ "$COMMAND" =~ (npm|pnpm|yarn)[[:space:]]+(install|add|i)[[:space:]]+[a-zA-Z] ]]; then
        echo "🚨 BLOCKED: New dependency installation"
        echo ""
        echo "Dependencies must be approved by team lead."
        echo "Create PR with RFC explaining:"
        echo "1. Why this dependency is needed"
        echo "2. Alternatives considered"
        echo "3. Bundle size impact"
        echo "4. License compatibility"
        exit 2
    fi

    # Allow: npm install (no args), npm install -g, pnpm install
    if [[ "$COMMAND" =~ ^(npm|pnpm|yarn)[[:space:]]+install$ ]]; then
        exit 0
    fi
fi
```

---

## 规则 6：遵循既有模式

### 问题

Claude 引入与代码库不一致的新模式：
- 项目使用函数式 React 时却使用 `class` 组件
- 项目使用 `ramda` 时却导入 `lodash`
- 项目是 GraphQL 时却编写 REST 端点
- 项目已统一使用 `axios` 时却使用 `fetch`

### 规则

**遵循既有代码库约定。实现前先检查。**

### 实现方式

**方案 A：CLAUDE.md 约定**

```markdown
## Code Conventions

### Tech Stack (DO NOT DEVIATE)

**Frontend**:
- React 18 with **function components + hooks** (NO class components)
- State: Zustand (NOT Redux, Context)
- HTTP: axios (NOT fetch)
- Styling: Tailwind CSS (NOT styled-components, emotion)
- Forms: React Hook Form + Zod

**Backend**:
- Node.js + Express
- Database: Prisma ORM (NOT raw SQL, TypeORM)
- Auth: JWT via jose library
- Validation: Zod schemas

**Testing**:
- Unit: Vitest (NOT Jest)
- E2E: Playwright (NOT Cypress)

### Import Patterns

**Always use**:
```typescript
import { useState } from 'react'           // ✅ Named imports
import axios from 'axios'                  // ✅ Default import
```

**Never use**:
```typescript
import React from 'react'                  // ❌ Deprecated pattern
import * as axios from 'axios'             // ❌ Namespace import
```

### File Structure

```
src/
  features/          ← Group by feature (NOT by type)
    auth/
      components/
      hooks/
      api/
  shared/            ← Shared utilities
    components/
    hooks/
```

### Design System

UI changes MUST use existing design system:
- Check `src/shared/components/` for existing components
- Use Tailwind utility classes from `tailwind.config.js`
- Colors from `colors.ts` palette ONLY
- Typography from `typography.config.js`

**Before creating new component**:
1. Search: `rg "Button" src/shared/components/`
2. If exists, use it
3. If doesn't exist, ask: "Should I create new Button component or use existing primitive?"
```

**方案 B：实现前分析**

```markdown
## Before Implementing

**ALWAYS** run these checks:

1. **Pattern check**:
```bash
# How does codebase handle X?
rg "import.*useState" src/  # Check React patterns
rg "axios\." src/           # Check HTTP patterns
rg "prisma\." src/          # Check DB patterns
```

2. **Existing components**:
```bash
# Does component already exist?
find src/shared/components -name "*Button*"
find src/shared/components -name "*Modal*"
```

3. **Ask user if unclear**:
   - "I see project uses [X]. Should I follow this pattern or use [Y]?"
```

**方案 C：自动化校验**

```bash
# .claude/hooks/PostToolUse.sh
#!/bin/bash
if [[ "$TOOL" == "Write" ]] || [[ "$TOOL" == "Edit" ]]; then
    FILE=$(echo "$INPUT" | jq -r '.tool.input.file_path')

    # Check for pattern violations
    if [[ "$FILE" =~ \.(tsx?)$ ]]; then
        CONTENT=$(cat "$FILE")

        # Violation: class components in React
        if echo "$CONTENT" | grep -q "class.*extends.*Component"; then
            echo "⚠️ WARNING: Class component detected in $FILE"
            echo "   Project uses function components. Consider refactoring."
        fi

        # Violation: wrong HTTP library
        if echo "$CONTENT" | grep -q "import.*fetch\|window.fetch"; then
            echo "⚠️ WARNING: fetch() detected in $FILE"
            echo "   Project uses axios. Use: import axios from 'axios'"
        fi
    fi
fi
```

---

## 规则 7：验证悖论

### 问题所在

当 AI 有 99% 的成功率时，传统的人工验证会变得脆弱：

**悖论所在**：随着 AI 可靠性的提升，人工审查的质量反而下降。

- **警觉性疲劳**：当人类不自觉地信任那些通常有效的模式时，罕见的错误（1%）就会蒙混过关
- **依赖模式的行为**：当审查者不再预期会出现错误时，人工审查就会退化
- **虚假的信心**："前 50 次都没问题"为第 51 次失败埋下了盲点
- **认知负荷**：人类并不擅长稳定地捕捉百分之一概率的错误

**真实事故**：
- 200 笔交易成功后绕过了支付校验 → 第 201 笔交易发生欺诈
- 因为"AI 总是能正确处理鉴权"而跳过安全检查 → 凭据泄露
- 测试套件通过率 99% → 那未被测试的 1% 情况导致了生产环境 bug

**来源**：[Alan Engineering Team (Charles Gorintin, Maxime Le Bras), Feb 2026](https://www.linkedin.com/pulse/le-principe-de-la-tour-eiffel-et-ralph-wiggum-maxime-le-bras-psmxe/)

### 规则内容

**构建自动化的安全系统，而不是依赖人工警觉。**

当 AI 可靠性超过约 95% 时，应从人工审查转向自动化护栏。

### 反模式与更优做法

| 反模式 | 更优做法 |
|--------------|-----------------|
| 对每一份 AI 输出都进行人工审查 | 自动化测试套件 + 选择性审查 |
| 因为"上次没问题"就信任 | 验证契约（测试、类型、lint） |
| 人类作为唯一的错误检测者 | 快速失败的护栏（CI/CD 关卡） |
| 对高频 AI 操作采用"抽查"策略 | 全面的自动化校验 |
| 审查者疲劳 = 标准随时间下降 | 一致的自动化质量标准 |

### 实现方式

**方案 A：自动化护栏栈**

```yaml
# .github/workflows/ai-safety.yml
name: AI Output Validation

on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Type safety
        run: npm run typecheck      # Catch type errors AI missed

      - name: Lint rules
        run: npm run lint            # Enforce code standards

      - name: Unit tests
        run: npm run test            # Verify behavior contracts

      - name: E2E tests
        run: npm run test:e2e        # Catch integration failures

      - name: Security audit
        run: npm audit               # Detect vulnerable dependencies

      - name: Bundle analysis
        run: npm run analyze         # Catch bloat/regressions

      # Human review ONLY after all automation passes
```

**方案 B：在 CLAUDE.md 中定义验证契约**

```markdown
## Verification Protocol

### NEVER rely on human review alone

**Automated verification required**:
1. **Type safety**: `npm run typecheck` must pass (zero errors)
2. **Tests**: `npm run test` coverage ≥ 80% for new code
3. **Lint**: `npm run lint` must pass (zero warnings)
4. **Security**: `npm audit` must show zero high/critical vulnerabilities
5. **Performance**: Lighthouse score ≥ 90 for affected pages

**Human review is for**:
- Architecture decisions
- UX/design choices
- Business logic validation
- Edge cases automation can't catch

**Human review is NOT for**:
- Syntax errors (use linters)
- Type errors (use TypeScript)
- Performance regressions (use benchmarks)
- Security issues (use automated scanners)
```

**方案 C：合并前检查清单（自动化）**

```bash
# .claude/hooks/PreCommit.sh
#!/bin/bash

echo "🔍 Running automated verification (Verification Paradox defense)..."

# 1. Type safety
npm run typecheck || { echo "❌ Type errors detected"; exit 1; }

# 2. Lint
npm run lint || { echo "❌ Lint errors detected"; exit 1; }

# 3. Tests
npm run test || { echo "❌ Tests failing"; exit 1; }

# 4. Security
npm audit --audit-level=high || { echo "❌ Security vulnerabilities detected"; exit 1; }

echo "✅ All automated checks passed"
echo "💡 Human review can now focus on architecture/UX/business logic"
```

### 边界情况

| 场景 | 行为 |
|----------|----------|
| AI 在 99.9% 的情况下写出完美代码 | 仍然运行自动化（即便在 99.9% 时悖论依旧成立） |
| 时间压力，"先发了再说" | 自动化没有商量余地（快 ≠ 跳过安全） |
| 琐碎改动（修正错别字） | 运行自动化（错别字也能搞垮生产环境） |
| 紧急热修复 | 必须运行自动化（高压 = 更高的出错率） |

### 为何重要

**旧模式（AI 之前）**：
- 代码质量 = 人类专业能力 + 细致审查
- 错误由经验丰富的开发者捕捉
- 审查质量保持稳定

**新模式（AI 辅助）**：
- AI 在 95%+ 的情况下产出高质量代码
- 人类变得自满（"AI 通常都能搞对"）
- 5% 的错误率在疲劳的审查中蒙混过关

**解决方案**：将枯燥的验证（语法、类型、测试）自动化，把人类的注意力留给创造性/战略性的审查。

### 与其他规则的结合

- **规则 3（功能完整性）**：自动化测试验证功能是否真正完成
- **规则 2（数据库安全）**：迁移测试捕捉破坏性操作
- **规则 6（遵循模式）**：linter 自动强制执行项目约定

这个悖论在 agent 侧的对应物，是 [TDD 工作流](../workflows/tdd-with-claude.md#the-verification-gap) 中记录的验证缺口（Verification Gap）模式。

---

## 与现有工作流的结合

### 与 Plan Mode 结合

```bash
# Before multi-file changes
/plan

# Claude enters read-only mode, explores codebase
# Identifies patterns, conventions, existing implementations
# Proposes plan following project conventions
# You review before execution
```

### 与 Git Hooks 结合

这些规则可与现有的 git 工作流集成：

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Run safety checks
./.claude/hooks/production-safety-check.sh

# If blocked, commit fails
exit $?
```

### 与 CI/CD 结合

添加一个校验步骤：

```yaml
# .github/workflows/pr-validation.yml
name: PR Validation
on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check for half-assing
        run: |
          if git diff origin/main...HEAD | grep -E "TODO.*implement|Not implemented"; then
            echo "❌ PR contains incomplete features"
            exit 1
          fi

      - name: Check for unauthorized deps
        run: |
          git diff origin/main...HEAD -- package.json | grep -E '^\+.*"[^"]+": "[^"]+"' || exit 0
          echo "⚠️ New dependencies detected. Review required."
```

---

## 故障排查

### “这些规则太严格了”

**解决方案**：根据团队规模和所处阶段进行调整。

| 团队规模 | 推荐规则 |
|-----------|-------------------|
| 1-2 名开发者 | 仅规则 1、3、6 |
| 3-10 名开发者 | 规则 1、3、5、6 |
| 10 名以上开发者或生产环境 | 全部 6 条规则 |

### “Claude 总是被拦截”

**解决方案**：规则正在生效！可选方案：

1. **授予临时权限**：
   ```bash
   # In CLAUDE.md
   ## Temporary Override (expires 2026-01-25)
   For this feature only: infrastructure changes allowed.
   Reason: Setting up new microservice.
   ```

2. **创建例外**：
   ```json
   {
     "permissions": {
       "allow": ["Edit(docker-compose.dev.yml)"],
       "deny": ["Edit(docker-compose.prod.yml)"]
     }
   }
   ```

3. **检查规则是否合适**：
   - 单人开发者把自己拦住了？→ 移除该规则
   - 团队需要灵活性？→ 用 “ask” 替代 “deny”

### “如何在整个团队中强制执行规则？”

**解决方案**：提交到代码仓库，而非个人配置。

```bash
# Shared team rules
/project/.claude/settings.json        # Committed
/project/CLAUDE.md                    # Committed

# Personal overrides
/project/.claude/settings.local.json  # Gitignored
/project/.claude/CLAUDE.md            # Gitignored
```

团队设置优先级更高，但个人可以主动选择更严格的规则。

---

## 参见

- [Ultimate Guide §9.12 Git 最佳实践](#912-git-best-practices-workflows) — 提交工作流，Plan → Act 模式
- [安全加固指南](./security-hardening.md) — MCP 安全、密钥保护、hook 栈
- [数据隐私指南](./data-privacy.md) — MCP 数据库风险、保留策略
- [企业 AI 治理](./enterprise-governance.md) — 组织级治理：使用章程、MCP 审批工作流、护栏分层、合规
- [采用方法](../roles/adoption-approaches.md) — 团队搭建、共享约定、企业级推广
- [Plan Mode](#23-plan-mode) — 执行前的安全探索
- [权限系统](#33-settings-permissions) — 允许/拒绝规则、hooks

---

## 快速参考

### 规则严重级别

| 规则 | 严重级别 | 违反后果 |
|------|----------|----------------------|
| 1. 端口稳定性 | 🔴 严重 | 团队停摆、部署失败 |
| 2. 数据库安全 | 🔴 严重 | 数据丢失、影响客户 |
| 3. 功能完整性 | 🟡 高 | 生产环境 bug、技术债 |
| 4. 基础设施锁定 | 🟠 高 | 停机、安全问题 |
| 5. 依赖安全 | 🟡 中 | 包体积膨胀、许可证问题 |
| 6. 遵循既有模式 | 🟢 低 | 代码不一致、维护负担 |

### 强制执行方法

| 方法 | 严格程度 | 配置耗时 | 最适合 |
|--------|------------|------------|----------|
| **权限 deny** | 100%（拦截） | 2 分钟 | 关键规则（1、2、4） |
| **Pre-tool hooks** | 100%（拦截） | 10 分钟 | 自定义逻辑、团队专属 |
| **CLAUDE.md 规则** | ~70%（Claude 会遵守） | 5 分钟 | 约定、指南 |
| **Post-tool 警告** | ~30%（仅警告） | 5 分钟 | 最佳实践、建议 |
| **Git hooks** | 100%（拦截提交） | 15 分钟 | 推送前的最后一道安全网 |

### 常见模式

**允许 staging 变更，拦截生产环境**：
```json
{
  "permissions": {
    "allow": ["Edit(docker-compose.dev.yml)"],
    "deny": ["Edit(docker-compose.prod.yml)"]
  }
}
```

**对敏感操作要求确认**：
```json
{
  "permissions": {
    "ask": ["Bash(rm -rf *)", "Bash(DROP TABLE *)"]
  }
}
```

**带过期时间的临时覆盖**：
```markdown
## Temporary Override (expires 2026-02-01)
Infrastructure changes allowed for migration project.
After expiry: revert to standard rules.
```

---

## 规则 6：自主循环安全

### 问题所在

自主 agent 循环——一个无人值守运行数小时、处理队列、监控系统的 Claude 会话——存在一种难以调试的失效模式：进程*看似*在运行，实则已悄然停滞。没有报错。没有退出码。什么都没发生，却在持续消耗你的 API 预算。

发生这种情况的原因包括：
- Claude 进入了没有退出条件的推理循环
- 某个工具调用因等待一个已经消失的资源而挂起
- 会话遇到了既不产生输出、也不报失败的边界情况

### 规则内容

对于任何预期运行时间超过几分钟的自主会话，都要实现一个心跳（heartbeat）机制。一旦心跳停止，就杀掉整个**进程组**——而不仅仅是父进程。

**为什么是进程组而非仅父进程**：Claude Code 会派生子进程（shell 命令、工具调用）。只杀父进程会留下孤儿子进程，它们仍在消耗资源，并可能在无人监督的情况下执行操作。

### 实现方式

**心跳写入器**——作为 PostToolUse hook 在自主循环内部运行：

```bash
#!/bin/bash
# .claude/hooks/autonomous-heartbeat.sh
# PostToolUse hook: write timestamp after every tool use

HEARTBEAT_FILE="${CLAUDE_HEARTBEAT_FILE:-/tmp/claude-heartbeat-$$}"
date +%s > "$HEARTBEAT_FILE"
```

**死人开关看门狗（dead-man watchdog）**——作为独立进程与 Claude 并行运行：

```bash
#!/bin/bash
# scripts/watchdog.sh
# Usage: ./scripts/watchdog.sh <timeout_seconds> <pid>

TIMEOUT="${1:-30}"
TARGET_PID="${2:-}"
HEARTBEAT_FILE="${CLAUDE_HEARTBEAT_FILE:-/tmp/claude-heartbeat-$TARGET_PID}"

if [[ -z "$TARGET_PID" ]]; then
  echo "Usage: watchdog.sh <timeout_seconds> <pid>" >&2
  exit 1
fi

while true; do
  sleep 5

  if ! kill -0 "$TARGET_PID" 2>/dev/null; then
    echo "Watchdog: process $TARGET_PID has exited cleanly"
    exit 0
  fi

  if [[ -f "$HEARTBEAT_FILE" ]]; then
    LAST_BEAT=$(cat "$HEARTBEAT_FILE")
    NOW=$(date +%s)
    AGE=$(( NOW - LAST_BEAT ))

    if [[ "$AGE" -gt "$TIMEOUT" ]]; then
      echo "Watchdog: no heartbeat for ${AGE}s (limit: ${TIMEOUT}s) — killing process group"
      kill -TERM -"$TARGET_PID" 2>/dev/null || kill -TERM "$TARGET_PID"
      sleep 2
      kill -KILL -"$TARGET_PID" 2>/dev/null || true
      rm -f "$HEARTBEAT_FILE"
      exit 1
    fi
  fi
done
```

**将两者串联起来的启动脚本**：

```bash
#!/bin/bash
export CLAUDE_HEARTBEAT_FILE="/tmp/claude-heartbeat-$$"

claude --print "Process the task queue in tasks.json" &
CLAUDE_PID=$!

./scripts/watchdog.sh 30 "$CLAUDE_PID" &
WATCHDOG_PID=$!

wait "$CLAUDE_PID"
EXIT_CODE=$?

kill "$WATCHDOG_PID" 2>/dev/null
rm -f "$CLAUDE_HEARTBEAT_FILE"
exit "$EXIT_CODE"
```

### 调整超时时间

| 任务类型 | 推荐超时 |
|-----------|-------------------|
| 简单文件操作 | 15–30s |
| Web 请求、API 调用 | 60s |
| 代码编译、测试运行 | 120s |
| 长时间运行的研究任务 | 300s |

从 30s 起步，只有当你观察到合理停顿确实超过超时时间时，才逐步增大。

### 何时不应使用

- 交互式会话（你正在盯着看）——看门狗没有任何价值
- 5 分钟以内的任务——配置开销不值得
- 失败是预期内、且由重试逻辑处理的流水线

> **致谢**：用于自主 agent 的心跳死人开关模式来自 [Everything Claude Code Security Guide](https://github.com/affaan-m/everything-claude-code)（Affaan Mustafa）。进程组杀进程以及看门狗分离的设计是他们的贡献。

---

**版本**：1.0.0
**最后更新**：2026-01-21
**变更日志**：基于社区验证的生产模式的初始版本
