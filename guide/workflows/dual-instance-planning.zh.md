---
title: "Dual-Instance Planning Workflow"
description: "Use two Claude instances with distinct roles for planning and implementation"
tags: [workflow, architecture, design-patterns]
---

# 双实例规划工作流

> **可信度**：Tier 2 —— 基于实践者经验（Jon Williams，2026 年 2 月）。该模式通过个人在 6 个月内从 Cursor 迁移到 Claude Code 的过程得到验证。

使用两个角色明确区分的 Claude 实例：一个负责规划与审查（Claude Zero），一个负责实现（Claude One）。关注点分离能提升计划质量并减少实现错误。

---

## 目录

1. [TL;DR](#tldr)
2. [何时使用此模式](#when-to-use-this-pattern)
3. [设置](#setup)
4. [完整工作流](#complete-workflow)
5. [计划模板](#plan-template)
6. [成本分析](#cost-analysis)
7. [技巧与故障排查](#tips-and-troubleshooting)
8. [另请参阅](#see-also)

---

## TL;DR

```
1. Launch Claude Zero (planner): explores, writes plans, reviews
2. Launch Claude One (implementer): reads plans, codes, commits
3. Human gatekeeper: approve plans before implementation
4. Plans directory: Review/ → Active/ → Completed/
5. Cost: ~$100-200/month (vs $500-1K for Boris horizontal pattern)
```

**最适合**：独立开发者、规格密集型工作、质量优先于速度、预算低于 $300/月

---

## 何时使用此模式

### ✅ 适用场景

- **复杂规格**：需求需要通过访谈式提问来澄清
- **质量关键型功能**：安全、支付、数据迁移
- **学习阶段**：新代码库、不熟悉的模式
- **产品设计师编码**：非开发背景，需要规划的严谨性
- **预算约束**：$100-200/月（相比并行多实例的 $500-1K）
- **规格密集型工作流**：详细需求、众多边界情况

### ❌ 不适用场景

- **简单改动**：错别字修复、琐碎重构（使用单实例）
- **探索性编码**：问题空间未知（规划开销不划算）
- **紧张的截止日期**：速度优先于质量（接受纠错循环）
- **高并发量的功能开发**：改用 Boris 模式（第 9.17 节）
- **预算非常有限**：低于 $100/月（使用 Sonnet、单实例）

### 与其他模式的对比

| 模式 | 扩展维度 | 成本/月 | 最适合 |
|---------|--------------|------------|----------|
| **单实例** | 无 | $50-100 | 大多数开发者、通用场景 |
| **双实例（Jon）** | 纵向（计划 ↔ 实现） | $100-200 | 规格密集型、注重质量 |
| **多实例（Boris）** | 横向（5-15 个并行） | $500-1,000 | 团队、高产量交付 |

---

## 设置

### 第 1 步：创建目录结构

```bash
cd ~/projects/your-project
mkdir -p .claude/plans/{Review,Active,Completed}
```

**目录职责**：
- `Review/` —— 等待人工审批的计划
- `Active/` —— 已批准、正在实现的计划
- `Completed/` —— 已归档的计划（学习资源）

**添加到 .gitignore**：
```bash
# .gitignore
.claude/plans/Review/
.claude/plans/Active/
# Optional: commit Completed/ for team learning
```

### 第 2 步：启动 Claude Zero（规划者）

**终端 1**：
```bash
cd ~/projects/your-project
claude
```

**首条消息**（角色强制约束）：
```
You are Claude Zero (Planner).

Your role:
- Explore codebase using Plan Mode (Shift+Tab twice)
- Interview user about requirements
- Write detailed plans to .claude/plans/Review/
- Review implementations after Claude One completes them
- NEVER edit code directly
- NEVER commit changes

Start by acknowledging this role.
```

Claude Zero 确认："Understood. I am Claude Zero (Planner). I will explore, plan, and review, but never touch code."

### 第 3 步：启动 Claude One（实现者）

**终端 2**（新会话）：
```bash
cd ~/projects/your-project
claude
```

**首条消息**（角色强制约束）：
```
You are Claude One (Implementer).

Your role:
- Read approved plans from .claude/plans/Active/
- Implement exactly as specified
- Commit changes after each logical step
- Report completion back to user
- NEVER create plans
- NEVER skip approval steps

Start by acknowledging this role.
```

Claude One 确认："Understood. I am Claude One (Implementer). I execute approved plans only."

---

## 完整工作流

### 阶段 1：规划（Claude Zero）

#### 第 1.1 步：发起规划

**你**（对 Claude Zero）：
```
# Enter Plan Mode (Shift+Tab twice), then:

Implement JWT authentication for the API:
- Access tokens (15min expiry)
- Refresh tokens (7 day expiry)
- Middleware to protect routes
- Logout capability (revoke refresh tokens)
```

#### 第 1.2 步：Claude Zero 探索

Claude Zero（在 Plan Mode 中）：
- 阅读现有的认证代码
- 在代码库中搜索认证模式
- 识别依赖项（库、env vars）

#### 第 1.3 步：Claude Zero 对你进行访谈

Claude Zero 提出澄清性问题：
```
Before I draft the plan, I need to clarify:

1. Should we support multiple concurrent sessions per user?
   (e.g., user logged in on phone + laptop simultaneously)

2. Where should refresh tokens be stored?
   - Database table
   - Redis
   - Other

3. Which routes should be protected?
   - All /api/* routes?
   - Specific routes only?

4. Do you want rate limiting on login attempts?

5. Success criteria for "done"?
   - Tests passing?
   - Postman collection?
   - Documentation updated?
```

**你回答后**，Claude Zero 完善理解。

#### 第 1.4 步：Claude Zero 编写计划

Claude Zero 创建 `.claude/plans/Review/auth-jwt.md`：

```markdown
# Plan: JWT Authentication

**Created**: 2026-02-04
**Author**: Claude Zero
**Estimated effort**: 3-4 hours
**Risk level**: Medium (security-critical)

## 摘要
实现基于 JWT 的认证，采用 access/refresh token 模式。
支持每个用户多个并发会话。
Refresh token 存储在数据库中，并具备撤销能力。

## 已澄清的需求
- 每个用户多个会话：是
- Refresh token 存储：数据库（新建表）
- 受保护的路由：除 /api/auth/* 外的所有 /api/*
- 速率限制：是（每 15min 5 次尝试）
- 成功标准：测试通过 + Postman collection

## 待创建的文件

### 1. src/auth/jwt.ts（约 120 行）
**用途**：JWT 工具函数

**导出**：
- `generateAccessToken(userId: string): string`
  - Payload：{ userId, type: 'access' }
  - 过期时间：15 分钟
  - 使用 JWT_SECRET 签名

- `generateRefreshToken(userId: string): string`
  - Payload：{ userId, type: 'refresh', jti: uuid() }
  - 过期时间：7 天
  - 使用 JWT_REFRESH_SECRET 签名
  - jti = 用于撤销的唯一 token ID

- `verifyAccessToken(token: string): { userId: string } | null`
  - 验证签名
  - 检查过期时间
  - 返回 payload 或 null

- `verifyRefreshToken(token: string): { userId: string, jti: string } | null`
  - 验证签名
  - 检查过期时间
  - 检查是否未被撤销（数据库查询）
  - 返回 payload 或 null

**依赖**：jsonwebtoken、uuid

### 2. src/middleware/auth.ts（约 60 行）
**用途**：认证中间件

**导出**：
- `requireAuth(req, res, next)`
  - 从 Authorization header 中提取 token（Bearer 格式）
  - 使用 verifyAccessToken() 验证
  - 将 userId 附加到 req.userId
  - 无效/缺失时返回 401

**依赖**：jwt.ts

### 3. src/db/migrations/YYYYMMDD_create_refresh_tokens.ts（约 40 行）
**用途**：refresh token 的数据库表

**Schema**：
```sql
CREATE TABLE refresh_tokens (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  jti UUID NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP NOT NULL,
  revoked_at TIMESTAMP
);
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_jti ON refresh_tokens(jti);
```

## 待修改的文件

### 1. src/routes/api.ts
**位置**：第 23 行（imports 之后）
**变更**：为除 /auth/* 外的所有路由添加 requireAuth 中间件

**修改前**：
```typescript
router.get('/profile', profileController);
router.post('/posts', createPostController);
```

**修改后**：
```typescript
import { requireAuth } from '../middleware/auth';
router.get('/profile', requireAuth, profileController);
router.post('/posts', requireAuth, createPostController);
```

### 2. src/routes/auth.ts
**位置**：创建新文件，或添加到现有的 auth 路由中
**变更**：
- POST /auth/login → 返回 { accessToken, refreshToken }
- POST /auth/refresh → 用 refresh token 换取新的 access token
- POST /auth/logout → 撤销 refresh token

### 3. src/config/env.ts
**位置**：第 15 行（现有密钥之后）
**添加**：
```typescript
JWT_SECRET: process.env.JWT_SECRET || '',
JWT_REFRESH_SECRET: process.env.JWT_REFRESH_SECRET || '',
```

### 4. .env.example
**添加**：
```
JWT_SECRET=your-secret-here-min-32-chars
JWT_REFRESH_SECRET=your-refresh-secret-here-min-32-chars
```

## 实现步骤（按顺序）

1. **安装依赖**
   ```bash
   npm install jsonwebtoken uuid
   npm install --save-dev @types/jsonwebtoken @types/uuid
   ```

2. **创建 JWT 工具**（jwt.ts）
   - 实现全部 4 个函数
   - 添加错误处理（在 verify 上使用 try/catch）

3. **运行数据库迁移**（refresh_tokens 表）
   - 测试迁移的 up/down

4. **创建 auth 中间件**（auth.ts）
   - 实现 requireAuth
   - 用 mock token 测试

5. **创建/更新 auth 路由**（auth.ts 路由）
   - POST /auth/login
   - POST /auth/refresh
   - POST /auth/logout

6. **保护现有路由**（api.ts）
   - 为所有 /api/* 路由应用 requireAuth

7. **将 JWT 密钥添加到 .env**
   - 生成安全的随机字符串（64 字符）

8. **编写测试**
   - jwt.ts 函数的单元测试
   - auth 流程的集成测试
   - 测试 token 过期
   - 测试撤销

9. **创建 Postman collection**
   - Login → 获取 token
   - 用 access token 访问受保护的路由
   - 刷新 access token
   - Logout → 撤销 refresh token
   - 验证被撤销的 token 被拒绝

## 成功标准

- [ ] POST /auth/login 返回 accessToken + refreshToken
- [ ] 没有有效 access token 时，受保护的路由返回 401
- [ ] 有有效 access token 时，受保护的路由返回 200
- [ ] POST /auth/refresh 用 refresh token 换取新的 access token
- [ ] POST /auth/logout 撤销 refresh token
- [ ] 被撤销的 refresh token 在 /auth/refresh 上被拒绝
- [ ] 过期的 access token 被拒绝
- [ ] 每个用户多个会话可用（不同的 refresh token）
- [ ] 所有测试通过（npm test）
- [ ] Postman collection 端到端可用

## 安全检查清单

- [ ] JWT 密钥存放在 .env 中（绝不提交）
- [ ] JWT 密钥 ≥32 字符
- [ ] Refresh token 存储在数据库中（不仅仅在 JWT 里）
- [ ] Refresh token 具有用于撤销的唯一 jti
- [ ] Access token 过期时间较短（15min）
- [ ] Authorization header 经过校验（Bearer 格式）
- [ ] Token 验证错误被捕获（不崩溃）

## 风险与缓解

| 风险 | 影响 | 缓解 |
|------|--------|------------|
| JWT 密钥泄露 | 高 | .env 加入 .gitignore，绝不记录密钥日志 |
| Token 过期时间过长 | 中 | access 15min，refresh 7 天（足够短） |
| 登录无速率限制 | 中 | 添加速率限制（每 15min 5 次尝试） |
| Refresh token 表无限增长 | 低 | 添加清理任务（删除过期 token） |

## 给实现者的问题（Claude One）

如果你在实现过程中遇到这些场景：

1. **现有用户登录流程**：与现有登录逻辑集成，不要替换整个认证系统
2. **数据库 ORM**：为 refresh_tokens 表使用现有的 ORM（Prisma/TypeORM/Knex）
3. **错误信息**：返回通用的 "Invalid token"（不要泄露 token 是过期还是签名无效）

## 预估工作量分解

- JWT 工具：45 分钟
- 数据库迁移：15 分钟
- 中间件：30 分钟
- Auth 路由：60 分钟
- 保护现有路由：15 分钟
- 测试：90 分钟
- Postman collection：15 分钟

**总计**：约 4 小时

---

**计划已批准？** → 移动到 `.claude/plans/Active/auth-jwt.md`
```

### 阶段 2：人工审查

**你审查** `.claude/plans/Review/auth-jwt.md`：

**检查清单**：
- [ ] 是否覆盖了所有需求？
- [ ] 方案对该代码库是否合理？
- [ ] 是否处理了安全方面的考量？
- [ ] 预估的工作量是否现实？
- [ ] 成功标准是否清晰且可测试？
- [ ] 待创建/修改的文件路径是否正确？

**如果批准**：
```bash
mv .claude/plans/Review/auth-jwt.md .claude/plans/Active/
```

**如果需要修改**，让 Claude Zero 修订：
```
（对 Claude Zero）：更新计划：
- 将 refresh token 过期时间从 7 天改为 30 天
- 将密码重置流程加入范围
```

### 阶段 3：实现（Claude One）

**你**（对 Claude One）：
```
Implement .claude/plans/Active/auth-jwt.md

Follow the plan exactly. Commit after each logical step.
Report back when complete.
```

Claude One：
1. 读取计划文件
2. 安装依赖
3. 创建 jwt.ts
4. 创建数据库迁移
5. 运行迁移
6. 创建 auth 中间件
7. 更新路由
8. 添加环境变量
9. 编写测试
10. 创建 Postman collection

**Claude One 在每一步之后提交**：
```
feat: add JWT utility functions
feat: create refresh_tokens table migration
feat: add auth middleware
feat: protect API routes with JWT auth
test: add JWT auth flow tests
```

### 阶段 4：验证（Claude Zero）

**你**（对 Claude Zero）：
```
Review the JWT implementation Claude One just completed.
Check against the plan in .claude/plans/Active/auth-jwt.md.
```

Claude Zero 审查：
- 代码结构是否与计划一致？
- 是否满足所有成功标准？
- 安全检查清单是否完成？
- 测试是否通过？
- 是否有代码异味或问题？

**Claude Zero 报告**：
```
✅ Review complete: auth-jwt.md

Code Quality: 9/10
- All files created as planned
- Success criteria met (9/9)
- Security checklist complete
- Tests pass (15/15)

Minor suggestions:
1. Consider adding refresh token rotation (security best practice)
2. Add JSDoc comments to jwt.ts functions
3. Consider extracting magic numbers (15min, 7 days) to config

Critical issues: None

Ready to archive plan to Completed/.
```

### 阶段 5：归档

**如果批准**：
```bash
mv .claude/plans/Active/auth-jwt.md .claude/plans/Completed/
```

**计划现已归档**，供日后参考和团队学习。

---

## 计划模板

将此模板保存到 `.claude/plan-template.md`，以保持计划结构的一致性：

```markdown
# Plan: [Feature Name]

**Created**: [Date]
**Author**: Claude Zero
**Estimated effort**: [Hours]
**Risk level**: Low | Medium | High

## Summary
[2-3 sentence overview of what this plan accomplishes]

## Requirements Clarified
[List of requirements confirmed through interview]
- Requirement 1: [Answer]
- Requirement 2: [Answer]

## Files to Create

### 1. [File path] (~[Lines] lines)
**Purpose**: [What this file does]

**Exports**:
- `functionName(params): returnType`
  - [What it does]
  - [Key implementation details]

**Dependencies**: [Libraries, other files]

## Files to Modify

### 1. [File path]
**Location**: Line [N] ([Context: after what, before what])
**Change**: [What to change]

**Before**:
```[language]
[Existing code snippet]
```

**After**:
```[language]
[Modified code snippet]
```

## Implementation Steps (Sequential)

1. **[Step name]**
   - [Substep]
   - [Substep]

2. **[Step name]**
   - [Substep]

## Success Criteria

- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]

## Security Checklist (if applicable)

- [ ] [Security item 1]
- [ ] [Security item 2]

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [High/Med/Low] | [How to prevent/handle] |

## Questions for Implementer (Claude One)

If you encounter these scenarios during implementation:
1. [Scenario]: [Guidance]

## Estimated Effort Breakdown

- [Task 1]: [Time]
- [Task 2]: [Time]

**Total**: [Hours]

---

**Plan approved?** → Move to `.claude/plans/Active/[filename].md`
```

---

## 成本分析

### 双实例 vs 带返工的单实例

| 场景 | 单实例 | 双实例 | 节省 |
|----------|----------------|---------------|---------|
| **简单功能**（登录表单） | 1 个会话 × $5 = **$5** | 2 个会话 × $3 = $6 | +$1（单实例胜出） |
| **中等功能**（认证系统） | 1 个会话 × $15 + 2 次返工 × $10 = **$35** | 2 个会话 × $12 = $24 | **节省 $11** |
| **复杂功能**（规格模糊） | 1 个会话 × $20 + 3 次返工 × $15 = **$65** | 2 个会话 × $18 = $36 | **节省 $29** |

**盈亏平衡点**：需要 ≥2 次返工循环的功能 → 双实例更便宜。

### 月度预算估算

**假设条件**：
- 每月 20 个工作日
- 每天 2 个功能（简单 + 复杂混合）
- Opus 4.5 定价（约 $15/1M 输入，$75/1M 输出）

| 画像 | 每月功能数 | 单实例 | 双实例 | 节省 |
|---------|----------------|----------------|---------------|---------|
| **轻度用户** | 20 个简单 | $100 | $120 | -$20（单实例胜出） |
| **中度用户** | 30 个混合（60% 中等，40% 简单） | $650 | $480 | **节省 $170** |
| **重度用户** | 40 个复杂 | $2,000 | $1,200 | **节省 $800** |

**建议**：
- 仅有简单功能 → 单实例
- 中等/复杂功能 → 双实例既省钱又省时

---

## 技巧与故障排查

### 角色强制约束

**问题**：Claude Zero 开始编辑代码。

**解决方案**：在每次请求中提醒：
```
(to Claude Zero): Remember: you are Claude Zero (Planner only).
Do not edit code. Write plan to .claude/plans/Review/
```

**预防措施**：使用 CLAUDE.md 来强制角色约束：

```markdown
# .claude/CLAUDE.md

## If you are Claude Zero (Planner):
- Use Plan Mode (Shift+Tab twice) for all exploration
- Save all plans to .claude/plans/Review/[feature].md
- NEVER edit code
- NEVER commit changes
- Review implementations after Claude One completes them

## If you are Claude One (Implementer):
- Read plans from .claude/plans/Active/
- Implement exactly as specified
- Commit after each logical step
- NEVER create plans
```

### 上下文污染

**问题**：Claude One 的上下文被规划讨论污染。

**解决方案**：使用独立的终端会话（独立的上下文）：
- Terminal 1 = Claude Zero（规划上下文）
- Terminal 2 = Claude One（实现上下文）

**绝不要在** Claude Zero 和 Claude One 之间**共享上下文**。

### 计划偏移

**问题**：Claude One 在实现过程中偏离计划。

**解决方案**：在计划中包含以下内容：
```markdown
## Implementation Rules for Claude One

- Follow plan steps sequentially (don't skip or reorder)
- If you encounter blockers, STOP and report (don't improvise)
- Commit after each step (granular history)
- If unclear, ask user (don't guess)
```

### 开销管理

**问题**：在目录之间移动文件是手动开销。

**解决方案**：创建 bash 别名：

```bash
# Add to ~/.bashrc or ~/.zshrc

# Move plan to Active (approve)
approve-plan() {
    mv ".claude/plans/Review/$1.md" ".claude/plans/Active/"
    echo "✅ Approved: $1.md → Active/"
}

# Move plan to Completed (archive)
complete-plan() {
    mv ".claude/plans/Active/$1.md" ".claude/plans/Completed/"
    echo "✅ Completed: $1.md → Archived"
}

# List plans by status
plans() {
    echo "📋 Review:"
    ls -1 .claude/plans/Review/ 2>/dev/null || echo "  (empty)"
    echo ""
    echo "🔄 Active:"
    ls -1 .claude/plans/Active/ 2>/dev/null || echo "  (empty)"
    echo ""
    echo "✅ Completed:"
    ls -1 .claude/plans/Completed/ 2>/dev/null | tail -5 || echo "  (empty)"
}
```

**用法**：
```bash
plans                     # List all plans
approve-plan auth-jwt     # Approve plan
complete-plan auth-jwt    # Archive completed plan
```

---

## 参见

- **主指南**：[第 9.17.1 节](#alternative-pattern-dual-instance-planning-vertical-separation) — 概述与对比
- **Plan Mode**：[plan-driven.md](plan-driven.md) — 规划工作流的基础
- **多实例（Boris）**：[第 9.17 节](#917-scaling-patterns-multi-instance-workflows) — 横向扩展替代方案
- **成本优化**：[第 8.10 节](#cost-optimization-tips) — 预算管理

**外部资源**：
- [Jon Williams LinkedIn 帖子](https://www.linkedin.com/posts/thatjonwilliams_ive-been-using-cursor-for-six-months-now-activity-7424481861802033153-k8bu) — 原始模式描述（2026 年 2 月 3 日）
- [Claude Code 团队的 10 条技巧](https://paddo.dev/blog/claude-code-team-tips/) — 包含 plan-first 方法在内的团队工作流
