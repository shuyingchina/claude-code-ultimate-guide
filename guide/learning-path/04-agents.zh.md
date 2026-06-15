# Module 04: Agents & Specialization

**时间**：1.5 小时 | **复杂度**：⭐⭐ 中级

## 目标

为特定任务创建专门的 agents。学习如何将 AI 能力聚焦到有针对性的问题上。

---

## 你将学到什么

- agents 是什么以及它们为什么有用
- 使用 AGENT.md 创建自定义 agents
- 限制 agent 的能力（沙箱化）
- 将 agents 用于特定任务
- 何时使用 agents 还是直接使用 Claude

---

## 什么是 Agents？

**agent** 是为某一特定任务而配置的 Claude Code 专门版本。

### 示例：代码审查 agent

与其向常规 Claude 请求代码审查（这需要心理上的上下文切换），你可以使用：

```bash
/agent code-reviewer
Review this function for bugs and performance issues
```

code-reviewer agent：
- 只处理代码审查
- 拥有审查专用的工具
- 了解安全漏洞模式
- 不会被其他任务分散注意力

### 常规 Claude vs Agents

| 方面 | 常规 Claude | Agent |
|--------|---------------|-------|
| 范围 | 通用 | 专门化 |
| 上下文 | 记住一切 | 聚焦任务的记忆 |
| 工具 | 全部可用 | 受限集合 |
| 速度 | 可多任务 | 专注一件事时很快 |
| 用途 | 探索、学习 | 重复性、特定任务 |

---

## 创建你的第一个 Agent

agents 定义在 `.claude/agents/AGENT.md` 文件中。

### 基本结构

```markdown
---
name: code-reviewer
type: agent
description: Reviews code for bugs, performance, and security
auto_invoke: false
requires_approval: true
---

# Code Reviewer Agent

## Purpose
Review code for:
- Bugs and logical errors
- Performance issues
- Security vulnerabilities
- Code style consistency
- Test coverage

## Tools
- Code analysis
- Git diff viewer
- Test runner
- Linting tools

## Instructions
When reviewing:
1. Check for null pointers and edge cases
2. Look for performance bottlenecks (O(n²), nested loops)
3. Scan for security issues (SQL injection, XSS)
4. Verify tests cover the change
5. Suggest improvements without being harsh

## Example Usage
/agent code-reviewer
Review src/auth.js for security issues
```

### 文件位置

将它放在你的项目中：

```
my-project/
└── .claude/
    └── agents/
        └── code-reviewer.md
```

### 使其可用

在你项目的 CLAUDE.md 中引用它：

```markdown
## Available Agents
Run agents with: /agent [name]

- **code-reviewer** - Code quality and security review
  Usage: /agent code-reviewer <description>
  
- **test-writer** - Generate tests for code
  Usage: /agent test-writer <file path>
```

---

## Agent 设计模式

### 模式 1：质量检查器

```markdown
---
name: quality-auditor
description: Audits code quality metrics
---

# Quality Auditor

## Purpose
Check code for:
- Test coverage (<80% = fail)
- Type safety (TypeScript strict mode)
- Code duplication
- Cyclomatic complexity

## Tools
- Code analysis
- Coverage reporter
- Type checker

## Output Format
- ✅ Passed: [metric] = X
- ⚠️ Warning: [metric] = X
- ❌ Failed: [metric] = X

## Scoring
Score /100 based on all metrics.
```

### 模式 2：安全专家

```markdown
---
name: security-auditor
description: Scans code for vulnerabilities
requires_approval: true
---

# Security Auditor

## Purpose
Find security vulnerabilities:
- Injection attacks (SQL, NoSQL, command)
- Authentication/authorization issues
- Cryptography mistakes
- Data exposure risks
- OWASP Top 10

## Tools
- Static analysis
- Dependency checker
- Secret detection

## Severity Levels
- CRITICAL: Stop work immediately
- HIGH: Fix before merge
- MEDIUM: Fix in next sprint
- LOW: Consider fixing
```

### 模式 3：文档编写器

```markdown
---
name: doc-writer
description: Generates documentation
---

# Documentation Writer

## Purpose
Create or improve:
- README files
- API documentation
- Architecture docs
- User guides
- CHANGELOG entries

## 输出格式
- 清晰的标题
- 每个功能都附带代码示例
- 链接到相关文档
- 用编号列表表示步骤顺序

## 风格
- 对初学者友好
- 不使用未经解释的术语
- 展示前后对比示例
```

---

## 智能体能力与限制

### 默认能力

所有智能体都可以：
- 读取文件（具备 git 感知能力）
- 分析代码
- 编写文档
- 检查语法
- 运行测试

### 限制能力

使用 `capabilities` 对智能体进行沙箱限制：

```markdown
---
name: code-reviewer
capabilities:
  - read_files      # Can read code
  - run_tests       # Can run test suites
  - check_syntax    # Can lint
  - write_comments  # Can suggest changes but...
  - NO: commit      # ...cannot commit
  - NO: push        # ...cannot push to git
---
```

这个智能体可以审查代码，但不会意外地推送有问题的代码。

### 常见限制

```markdown
# Analyzer (read-only)
capabilities:
  - read_files
  - run_tests
# Can't modify anything

# Refactoring Agent (write, no push)
capabilities:
  - read_files
  - write_files
  - run_tests
  - NO: commit
  - NO: push
# Can change code but you review before pushing

# Full Agent (unrestricted)
capabilities:
  - all
# Can do anything (use with caution)
```

---

## 在工作流中使用智能体

### 调用智能体

```bash
/agent code-reviewer
Review the changes I just made to src/auth.js
```

Claude 切换到 code-reviewer 智能体并作出响应。

### 串联智能体

按顺序使用多个智能体：

```bash
# Step 1: Test Writer generates tests
/agent test-writer
Write tests for src/utils/validators.js

# Step 2: Code Reviewer checks the tests
/agent code-reviewer
Review the tests that were just written

# Step 3: Security Auditor scans
/agent security-auditor
Check the tests and code for vulnerabilities
```

### 配合 Plan Mode 使用智能体

对于有风险的操作，在智能体内使用 `/plan`：

```bash
/agent refactoring-specialist
/plan
Refactor the payment processing module to use async/await
```

---

## 练习：创建一个 Test-Writer 智能体

### 第 1 步：创建智能体文件

```bash
cat > .claude/agents/test-writer.md << 'EOF'
---
name: test-writer
description: Generates comprehensive tests
capabilities:
  - read_files
  - write_files
  - run_tests
---

# Test Writer Agent

## Purpose
Generate high-quality tests for:
- Unit tests (pure functions)
- Integration tests (component interactions)
- Edge cases and error conditions
- Performance tests

## Style
- Arrange-Act-Assert pattern
- Descriptive test names
- Each test focuses on ONE behavior
- 70%+ code coverage target

## Tools
- Test framework (Jest, pytest, etc)
- Mock libraries
- Assertion libraries

## Output
- Tests in same directory as source
- Naming: [file].test.js or [file].spec.js
- Include setup/teardown code
EOF
```

### 第 2 步：在 CLAUDE.md 中引用

```markdown
## Available Agents
- test-writer: Generate tests for any function or module
  Usage: /agent test-writer <file path>
```

### 第 3 步：使用它

```bash
/agent test-writer
Write tests for src/utils/formatDate.js
```

该智能体将会：
1. 读取 formatDate.js
2. 理解它的功能
3. 生成全面的测试
4. 向你展示测试文件

### 第 4 步：审查

在接受之前检查这些测试：
- 它们是否覆盖了边界情况？
- 命名是否清晰？
- 它们是否真的能运行？

---

## 何时使用智能体

### 在以下情况使用智能体：

✅ 你反复执行同一项任务（代码审查、测试、安全审计）
✅ 你想要专注于单一工作的 AI
✅ 你想要限制能力（安全考虑）
✅ 你正在构建团队工作流
✅ 任务有明确的成功标准

### 在以下情况使用常规 Claude：

✅ 你正在探索/学习
✅ 任务是全新的
✅ 你需要通用型帮助
✅ 你正在调试某个复杂问题
✅ 你想要对话式的来回交流

---

## 最佳实践

### 应该做

✅ 为 agents 赋予清晰、聚焦的用途

✅ 在 agent 定义中记录输出格式

✅ 限制你不需要的能力

✅ 先用示例任务测试 agents

✅ 对你的 agents 做版本控制（放在 .claude/agents/ 中）

### 不应该做

❌ 创建用途重叠的 agents（容易混淆）

❌ 把 agents 做得过于通用（违背了使用初衷）

❌ 完全信任某个 agent（始终要审查）

❌ 为一次性任务创建 agent（直接用 Claude 即可）

---

## 验证：如果满足以下条件，你就准备好了……

✓ 你已至少创建了一个自定义 agent

✓ 你理解 agents 相对于 Claude 的用途

✓ 你能够限制 agent 的能力

✓ 你知道如何调用一个 agent（/agent name）

✓ 你已在真实任务上测试过你的 agent

---

## 下一步是什么？

**模块 05：Skills 与自动化** 涵盖：
- 创建可复用的 skills（知识模块）
- 打包能力以便分发
- skill 的自动调用
- 构建你的自定义知识库

这部分教你如何打包知识，让 Claude 在多个会话之间记住它。

---

**完成模块 04 了吗？** → 准备进入模块 05：Skills 与自动化
