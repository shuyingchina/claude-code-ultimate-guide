# 模块 05：Skills 与自动化

**时长**：1.5 小时 | **难度**：⭐⭐ 中级

## 目标

创建可复用的 skills，为 Claude 提供领域专属知识。把针对重复性问题的解决方案打包起来。

---

## 你将学到

- 什么是 skills，以及它们为何强大
- 用 SKILL.md 创建 skills
- skill 的 frontmatter 与元数据
- 自动调用 skills
- 构建知识库
- 将 skills 与你的项目捆绑在一起

---

## 什么是 Skills？

一个 **skill** 就是一个可复用的知识模块。它教会 Claude 如何做某件具体的事。

### 示例：测试 Skill

与其每次会话都解释你的测试方法，不如创建一个 skill：

```markdown
# Testing Best Practices for Our Project

## Framework: Jest

## Style
- Descriptive names: "should validate email with + symbols"
- Arrange-Act-Assert pattern
- Mock external dependencies
- Test behavior, not implementation

## Coverage Target
Minimum 80%
```

这样，每当 Claude 协助测试时，它都会读取这个 skill 并遵循你的方法。

### Skills 与 Agents 的对比

| 方面 | Skill | Agent |
|--------|-------|-------|
| 用途 | 传授知识 | 执行任务 |
| 范围 | 领域知识 | 专门的工作流 |
| 持久性 | 每次会话都记住 | 显式调用 |
| 自动调用 | 是（可选） | 仅手动 |
| 示例 | "我们如何测试代码" | "the test-writer agent" |

---

## 创建你的第一个 Skill

Skills 是位于 `.claude/skills/` 中的 markdown 文件。

### 基本结构

```markdown
---
name: testing-standards
description: Our project's testing practices and conventions
triggers: [test, testing, jest, spec]
auto_invoke: false
keywords: [jest, unit-test, integration-test, mocking]
version: 1.0.0
---

# Testing Standards

## Framework
Jest with @testing-library/react

## File Organization
- Tests live next to source code
- Naming: `[Component].test.tsx`
- Fixtures in `__fixtures__/`
- Mocks in `__mocks__/`

## Test Structure (AAA)
1. **Arrange**: Set up test data
2. **Act**: Call the function/component
3. **Assert**: Check results

## Example

```typescript
describe('validateEmail', () => {
  it('should accept valid email addresses', () => {
    // Arrange
    const email = 'user@example.com';
    
    // Act
    const result = validateEmail(email);
    
    // Assert
    expect(result).toBe(true);
  });
});
```

## Coverage Requirements
- Target: 80% minimum
- Critical paths: 100%
- Types of coverage: line, branch, function

## Mocking Strategy
- External APIs: use jest.mock()
- Database: use test fixtures
- Timers: use jest.useFakeTimers()

## Running Tests
```bash
npm test                 # Run all tests
npm test -- --coverage   # With coverage report
npm test -- --watch      # Watch mode
```
```

### 文件位置

```
my-project/
└── .claude/
    └── skills/
        └── testing-standards.md
```

---

## Skill 特性

### Triggers

当 Claude 看到某些关键词时自动调用该 skill：

```markdown
---
triggers: [test, jest, spec, coverage, mock]
---
```

如果 Claude 看到 "add tests to this function"，它就会自动读取这个测试 skill。

### Auto-Invoke

```markdown
---
auto_invoke: true
---
```

当设为 `true` 时，Claude 会在会话开始时加载该 skill（无需你主动要求）。可用于关键规则。

### Keywords

帮助 Claude 的搜索找到该 skill：

```markdown
---
keywords: [testing, jest, unit-test, mocking, assertions]
---
```

### Version

追踪 skill 的版本：

```markdown
---
version: 1.0.0
---
```

当 skill 发生重大变更时进行更新。

---

## 常见 Skill 模式

### 模式 1：编码规范

```markdown
---
name: python-standards
triggers: [python, flask, django]
---

# Python Coding Standards

## Style
- PEP 8 compliance (max 100 chars)
- Type hints on all functions
- Docstrings in Google format

## 测试
- 使用 pytest 进行单元测试
- 最低 80% 覆盖率
- Mock 外部依赖

## 文件组织
src/
├── models/
├── services/
├── controllers/
└── tests/

## 导入
```python
# ✅ Good: specific imports
from models import User
from services.auth import authenticate

# ❌ Bad: wildcard imports
from models import *
```
```

### 模式 2：领域知识

```markdown
---
name: payment-processing
description: Payment system rules and edge cases
auto_invoke: true
---

# Payment Processing Rules

## PCI Compliance
- Never log card numbers
- Use tokenization (Stripe)
- Encrypt sensitive data
- Audit all transactions

## Common Issues
1. Partial charges: Retry with exponential backoff
2. Currency conversion: Always round to 2 decimals
3. Timezone handling: Store all times in UTC

## Edge Cases
- Declined cards: Provide clear error message
- Expired cards: Suggest updating payment method
- 3D Secure: Handle verification flow
```

### 模式 3：流程文档

```markdown
---
name: code-review-checklist
triggers: [review, pull request, pr]
---

# Code Review Checklist

## Before Requesting Review
- [ ] Tests pass locally
- [ ] No console.log statements
- [ ] No secrets in code
- [ ] Commit messages are clear

## Security Checks
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] No exposed API keys
- [ ] Input is validated

## Performance
- [ ] No N+1 queries
- [ ] No infinite loops
- [ ] Load times acceptable

## Testing
- [ ] Unit tests added
- [ ] Integration tests updated
- [ ] Coverage >80%
```

---

## 打包 Skills

你可以将多个相关的 skills 打包在一起。

### 项目 Skill 包

```
my-project/
└── .claude/
    └── skills/
        ├── testing-standards.md
        ├── api-design.md
        ├── database-patterns.md
        └── security-checklist.md
```

在 CLAUDE.md 中引用它们：

```markdown
## Available Skills
Our custom skills are loaded automatically:
- **testing-standards**: How we write tests
- **api-design**: REST API conventions
- **database-patterns**: Common queries and migrations
- **security-checklist**: Security review process
```

### 分发 Skills

要与团队共享 skills，请将它们纳入 git 版本控制：

```bash
git add .claude/skills/
git commit -m "Add testing and API design skills"
git push
```

团队成员检出项目后会自动获得这些 skills。

---

## 练习：创建一个领域 Skill

### 场景

你正在构建一个电商网站。你希望 Claude 理解你的产品数据模型。

### 步骤 1：创建 Skill

```bash
cat > .claude/skills/product-data-model.md << 'EOF'
---
name: product-data-model
description: E-commerce product data structure and rules
triggers: [product, catalog, sku, price, inventory]
auto_invoke: false
version: 1.0.0
---

# Product Data Model

## Core Entities

### Product
```
{
  id: UUID,
  name: string,
  slug: string,  // URL-friendly
  description: string,
  category_id: UUID,
  created_at: timestamp,
  updated_at: timestamp
}
```

### SKU (Stock Keeping Unit)
```
{
  id: UUID,
  product_id: UUID,
  sku: string,  // e.g., "BLUE-XL-001"
  price: decimal,  // Always 2 decimals
  cost: decimal,
  inventory: integer,
  weight: float,  // In kg
}
```

### Inventory Rules
- Decrement on order placement
- Increment on return
- Low stock alert: <5 units
- Reorder level: Set per product

## Common Queries

### Get product with all SKUs
```sql
SELECT p.*, s.* 
FROM products p 
JOIN skus s ON p.id = s.product_id 
WHERE p.slug = ?
```

### Check inventory
```sql
SELECT sum(inventory) FROM skus WHERE product_id = ?
```

## Edge Cases
1. Out of stock: Return 404 or "unavailable"
2. Variant selection: Show price per SKU
3. Price changes: Update in SKU, not Product
EOF
```

### 步骤 2：在 CLAUDE.md 中引用

```markdown
## Skills
- **product-data-model**: 理解我们的产品结构
```

### Step 3: Use It

在会话中：

```
Add a query to find all products with low inventory (< 5 units)
```

Claude 将会：
1. 读取 product-data-model skill
2. 理解你的 schema
3. 编写正确的 SQL

---

## 最佳实践

### DO

✅ 为你重复执行的事情创建 skills

✅ 让 skills 保持聚焦（每个 skill 一个领域）

✅ 对你的 skills 进行版本控制

✅ 在 skills 中包含示例

✅ 当需求变化时更新 skills

✅ 与你的团队分享 skills

### DON'T

❌ 为一次性知识创建 skills（改用 CLAUDE.md）

❌ 让 skills 过长（>500 行 = 拆分为多个 skills）

❌ 把 skills 用于临时指令（使用 CLAUDE.md 或 AGENT.md）

❌ 把 skills 当作全面的文档

---

## Skill 生命周期

1. **Create**：识别重复出现的模式或领域知识
2. **Document**：编写带示例的 skill
3. **Test**：在会话中使用它并验证 Claude 是否遵循
4. **Refine**：根据反馈进行更新
5. **Share**：提交到 git 以供团队访问
6. **Maintain**：随着实践的演进进行更新

---

## 验证：如果满足以下条件，你就准备好了……

✓ 你已经创建了至少一个自定义 skill

✓ 你理解 triggers 和 auto-invoke

✓ 你知道 skills 和 agents 之间的区别

✓ 你能解释何时使用 skill 而非 CLAUDE.md

✓ 你的 skill 已在真实会话中经过测试

---

## 下一步是什么？

**Module 06: Hooks & Events** 涵盖：
- 自动响应系统事件
- 提交前验证
- 操作后通知
- 构建安全的自动化

这会教你如何在无需手动干预的情况下自动化重复性任务。

---

**完成了 Module 05？** → 准备进入 Module 06: Hooks & Events
