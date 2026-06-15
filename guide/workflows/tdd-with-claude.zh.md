---
title: "TDD with Claude Code"
description: "Test-Driven Development workflow with explicit prompting for red-green-refactor cycles"
tags: [workflow, tdd, testing]
---

# 使用 Claude Code 进行 TDD

> **可信度**：Tier 1 — 基于 Anthropic 官方最佳实践以及广泛的社区验证。

使用 Claude 进行测试驱动开发（TDD）需要显式提示。Claude 天然倾向于先编写实现代码，再编写测试。而 TDD 要求的恰好相反。

---

## 目录

1. [TL;DR](#tldr)
2. [问题所在](#the-problem)
3. [设置](#setup)
4. [红-绿-重构循环](#the-red-green-refactor-cycle)
5. [与 Claude Code 功能的集成](#integration-with-claude-code-features)
6. [反模式](#anti-patterns)
7. [高级模式](#advanced-patterns)
8. [另请参阅](#see-also)

---

## TL;DR

```
Red → Green → Refactor

But you MUST prompt Claude explicitly:
"Write a FAILING test for [feature]. Do NOT write implementation yet."
```

---

## 问题所在

如果没有显式指示，Claude 会：
1. 先编写实现代码
2. 然后编写能够通过该实现的测试

这违背了 TDD 的初衷：测试应当驱动设计，而不是验证已有的代码。

---

## 设置

### CLAUDE.md 配置

在项目的 CLAUDE.md 中添加：

```markdown
## Testing Conventions

### TDD Workflow
- Always write failing tests BEFORE implementation
- Use AAA pattern: Arrange-Act-Assert
- One assertion per test when possible
- Test names describe behavior: "should_return_empty_when_no_items"

### Test-First Rules
- When I ask for a feature, write tests first
- Tests should FAIL initially (no implementation exists)
- Only after tests are written, implement minimal code to pass
```

### 用于自动运行测试的 Hook（可选）

创建 `.claude/hooks/test-on-save.sh`：

```bash
#!/bin/bash
# Auto-run tests when test files change
if [[ "$1" == *test* ]] || [[ "$1" == *spec* ]]; then
  npm test --watchAll=false 2>&1 | head -20
fi
```

---

## 红-绿-重构循环

### 阶段 1：Red（编写失败的测试）

**提示**：
```
Write a failing test for [feature description].
Do NOT write the implementation yet.
The test should fail because the function/method doesn't exist.
```

**示例**：
```
Write a failing test for a function that calculates the total price
of items in a cart, applying a 10% discount if total exceeds $100.
Do NOT implement the function yet.
```

**Claude 的预期行为**：
- 创建包含测试用例的测试文件
- 测试引用一个尚不存在的函数
- 运行测试会以 "function not defined" 或类似信息失败

**验证**：
```bash
npm test  # Should fail with "calculateCartTotal is not defined"
```

### 阶段 2：Green（最小化实现）

**提示**：
```
Now implement the minimum code to make these tests pass.
Only write enough code to pass the current tests, nothing more.
```

**Claude 的预期行为**：
- 创建实现文件
- 编写满足测试所需的最小代码
- 避免过度设计

**验证**：
```bash
npm test  # Should pass
```

### 阶段 3：Refactor（清理）

**提示**：
```
Refactor the implementation to improve code quality.
Tests must stay green after refactoring.
Focus on: [readability / performance / removing duplication]
```

**Claude 的预期行为**：
- 在不改变行为的前提下改进代码
- 运行测试以验证它们仍然通过
- 记录任何重大改动

---

## 与 Claude Code 功能的集成

### 配合 TodoWrite

在任务列表中跟踪 TDD 各个阶段：

```
User: "Implement user authentication with TDD"

Claude creates todos:
- [ ] RED: Write failing tests for login
- [ ] GREEN: Implement login to pass tests
- [ ] REFACTOR: Clean up login implementation
- [ ] RED: Write failing tests for logout
- [ ] GREEN: Implement logout
- [ ] REFACTOR: Clean up
```

### 配合 Plan Mode

使用规划来制定测试策略：

```
[Press Shift+Tab to enter Plan Mode]

I need to implement a shopping cart with TDD.
Plan the test cases before we start writing any code.
```

Claude 会以只读模式探索代码库，然后在进行任何实现之前提出测试计划。

### 配合 Hooks

使用 PostToolUse hook 在编辑后自动运行测试：

```json
// In .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "npm test --watchAll=false 2>&1 | head -20"
      }
    ]
  }
}
```

### 配合 Sub-Agents

将测试编写委托给专注于特定范围的 agent：

```
Use the test-writer agent to create comprehensive tests for
the UserService class, covering all edge cases.
Then I'll implement to pass those tests.
```

---

## 反模式

### 验证缺口（The Verification Gap）

验证缺口是指 agent 在验证套件确认功能完成之前就报告该功能已完成的失败模式。它是多会话 agent 工作中最常见的可靠性失败，而通过正确的 harness 设计完全可以避免。

三个可观察的症状：agent 在任何测试命令运行之前就打印成功消息；测试运行了，但 stderr 被丢弃或没有被读取；当验收标准要求端到端行为时，却只有单元测试通过。

修复方法是一个三层验证栈，在任何功能在功能列表中被标记为 `passing` 之前，这三层都必须通过：

1. **Lint** —— 语法和风格检查（最快，在运行测试前捕获明显的错误）
2. **单元和集成测试** —— 各个组件的功能正确性
3. **端到端测试** —— 用户或外部调用者所看到的行为契约

每一层捕获不同类别的失败。单元测试可能通过，但组件边界却出现问题。端到端测试会暴露状态传播错误和生命周期问题，这些是单元测试无法看到的。跳过任何一层都会留下缺口。

独立评估者原则：编写代码的 agent 不能是认证其完成的同一次调用。这并非出于对模型的不信任，而是因为上下文会影响评估。一个刚花了两个小时构建某项功能的 agent，会对含糊的输出做出宽容的解读。而一个独立读取退出码的 PostToolUse hook 或第二个 agent 则不会。`examples/hooks/bash/verification-gate.sh` 中的 hook 实现了这一模式。

Anthropic 在其 harness 设计研究中记录了这一失败：在裸运行（无 harness）中，他们的 agent 在 20 分钟后报告游戏编辑器已完成。但什么都跑不起来。在 harness 中加入独立评估者后，同一个模型运行了 6 个小时并交付了一个可用的结果。（来源：[https://www.anthropic.com/engineering/harness-design-long-running-apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)）

WIP=1 规则与此相关：每次只保持一个功能处于 `active` 状态，意味着验证缺口一旦发生，只会影响一个功能，而非同时影响多个。

### 不应该做的事

| 反模式 | 为什么错误 | 正确做法 |
|--------------|----------------|------------------|
| "为这个功能编写测试" | Claude 会先实现 | "编写尚不存在的、会 FAILING 的测试" |
| "添加测试和实现" | 失去测试优先的好处 | 拆分成两个 prompt |
| "确保测试通过" | 鼓励实现优先 | "先写测试，然后做最小化实现" |
| 跳过重构阶段 | 积累技术债 | 始终在 green 之后重构 |
| 一次做多个功能 | 失去专注 | 每个 TDD 循环只做一个功能 |

### 常见错误

**错误**：要求 Claude 为现有代码"编写测试"。
```
# Wrong
"Write tests for the existing calculateTotal function"

# Right
"Write tests for calculateTotal behavior, assuming function doesn't exist.
Then we'll verify the existing implementation passes."
```

**错误**：合并 red 和 green 阶段。
```
# Wrong
"Implement calculateTotal with tests"

# Right
"Write failing tests for calculateTotal. Stop there."
[After tests written]
"Now implement to pass those tests."
```

---

## 高级模式

### 基于属性的测试（Property-Based Testing）

```
Write property-based tests for the sort function.
Properties to test:
- Output length equals input length
- All input elements exist in output
- Output is ordered
Use fast-check or similar library.
```

### 变异测试（Mutation Testing）

```
After tests pass, run mutation testing to find weak spots.
Identify tests that don't catch mutations.
```

> **更进一步**：JiTTesting 在 PR 时自动应用变异测试 —— 由 LLM 生成、临时性、零维护。Meta 大规模部署了这一方案，相比传统测试，回归捕获能力提升了 4 倍。参见 [Just-in-Time Catching Test Generation at Meta](https://arxiv.org/abs/2601.22832) 以及[方法论指南](../core/methodologies.md#jittesting-just-in-time-testing)，了解今天如何用 Claude Code 实现这一近似模式。

### 遗留代码的 TDD

```
I need to refactor legacyFunction.
First, write characterization tests that capture current behavior.
Then we'll refactor with confidence.
```

---

## 示例会话

### 用户请求
```
Implement a URL shortener service with TDD.
```

### 第 1 阶段：Red
```
Let's use TDD. First, write failing tests for:
1. Shortening a URL returns a short code
2. Retrieving a short code returns original URL
3. Invalid URLs are rejected
4. Expired links return error

Do NOT implement anything yet.
```

### 第 2 阶段：Green
```
Tests are written and failing. Now implement the minimum
code to make them pass. Use an in-memory store for now.
```

### 第 3 阶段：Refactor
```
Tests pass. Now refactor:
- Extract URL validation to separate function
- Add proper error types
- Improve variable names

Run tests after each change to ensure they stay green.
```

---

## 另请参阅

- [../core/methodologies.md](../core/methodologies.md) —— 完整的方法论参考
- [紧密反馈循环](../ultimate-guide.md) —— 第 9.5 节
- [examples/skills/tdd-workflow.md](../../examples/skills/tdd-workflow.md) —— TDD skill 模板
- [Anthropic 最佳实践](https://www.anthropic.com/engineering/claude-code-best-practices)
- [task-management.md](./task-management.md) —— 使用 Tasks API 跨会话跟踪 TDD 循环
- [Superpowers](https://github.com/obra/superpowers) —— 将 TDD 强制作为必经关卡的插件套件：在 failing 测试存在之前编写的代码会被删除并从头重做。比手动 prompting 的强制力更严格。
