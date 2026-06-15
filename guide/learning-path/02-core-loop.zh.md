# 模块 02：核心循环

**时长**：45 分钟 | **难度**：⭐ 入门

## 目标

理解 Claude Code 实际是如何工作的——决策循环、上下文，以及如何高效地组织你的请求。

---

## 你将学到什么

- 完整的交互循环（提示 → 分析 → 决策 → 行动）
- Claude 如何阅读并理解你的项目
- 上下文如何运作，以及为什么它很重要
- 模式：Normal、Plan 和 Think 模式
- 如何组织高效的请求

---

## 完整循环（深入剖析）

与 Claude Code 的每一次交互都遵循以下顺序：

```
┌──────────────────────────────────────────────────────────────┐
│ 1. YOU PROMPT                                                │
│    "Fix the bug in auth.js on line 45"                      │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 2. CLAUDE READS                                              │
│    - Reads auth.js (full file)                              │
│    - Reads related files (auth-test.js, config.js, etc)     │
│    - Understands the error context                          │
│    - Analyzes call sites where auth.js is used              │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 3. CLAUDE ANALYZES                                           │
│    - Identifies the root cause                              │
│    - Considers side effects                                 │
│    - Plans minimal changes                                  │
│    - Checks for tests                                       │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 4. CLAUDE DECIDES                                            │
│    Does the change need tests? → Suggest test updates       │
│    Is the change safe? → Proceed or ask for confirmation    │
│    Should multiple files change? → Show full scope           │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 5. CLAUDE PROPOSES                                           │
│    Shows you:                                               │
│    - Description of changes                                 │
│    - diff view (what's changing)                            │
│    - Reasoning                                              │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 6. YOU REVIEW                                                │
│    - Read the diff carefully                                │
│    - Ask questions if unclear                               │
│    - Accept or reject the changes                           │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│ 7. CHANGES APPLIED                                           │
│    - Files updated on disk                                  │
│    - You can now test/run the code                          │
│    - Next iteration begins                                  │
└──────────────────────────────────────────────────────────────┘
```

---

## Claude 如何阅读你的项目

Claude 不会阅读所有内容。它对**范围的把握很智能**。

### 示例：你提问"修复登录 bug"

Claude 会：

1. **在你的代码库中搜索 "login"**
2. **找到 auth.js、login.js、auth-controller.js**
3. **优先阅读这些文件**（完整内容）
4. **查找调用方**（哪些代码调用了这些文件？）
5. **阅读测试**（如果存在）
6. **查找相关配置**（环境变量、常量）

Claude **不会**阅读：
- node_modules（自动排除）
- .git 历史记录（数据量太大）
- 项目中的每一个文件（太慢）
- 你的整个代码库，除非相关

### 专业提示

明确说明范围：
- ❌ "Fix the bugs" → Claude 只能猜测是哪些文件
- ✅ "Fix the login bug in auth.js on line 45" → Claude 精确阅读真正重要的内容

---

## 上下文：核心概念

**上下文**是指 Claude 能记住你对话内容的多少。它是有限的（约 200K tokens）。

### 什么会消耗上下文？

```
Your prompt:           50 tokens
Claude's response:     500 tokens
File reads:            2000 tokens per file
Previous messages:     accumulated tokens
```

### 上下文计量表

```bash
/status
```

显示：
```
Context: 67%
```

这意味着：
- 0-50%：剩余空间充足，可以自由工作
- 50-70%：已用一半，需要留意
- 70-90%：开始紧张，使用 `/compact`
- 90%+：临界状态，你必须清理

### `/compact` —— 你的安全阀

当上下文达到 70%+ 时，使用：

```bash
/compact
```

它会：
1. 总结之前的对话
2. 丢弃旧消息
3. 释放约 40% 的上下文
4. 让你在同一会话中继续工作

你可以在一次会话中多次执行 compact。

---

## 模式：Normal、Plan 与 Think

Claude Code 有三种交互模式。

### Normal 模式（默认）

Claude 在分析后立即进行修改。适用于：
- 简单的 bug 修复
- 小型功能新增
- 重构小段代码

**流程**：提问 → 分析（1-2 秒）→ 提议 → 应用

### Plan 模式（`/plan`）

Claude 先思考，提出一个计划，在进行修改前等待批准。适用于：
- 复杂功能
- 高风险改动
- 系统级重构
- 当你对方案不确定时

**流程**：提问 → 思考 → 提议计划 → 你批准 → 分析 → 应用

**示例**：
```bash
/plan
Refactor the authentication system to use JWT instead of sessions
```

Claude 会回复一份分步计划供你审阅。

### Think 模式（`/think`）

Claude 会展示扩展推理，逐步思考问题。适用于：
- 理解复杂的 bug
- 架构决策
- 安全分析
- 性能优化

**流程**：提问 → 扩展推理 → 分析 → 提议

---

## 构建高效请求

### 框架：WHAT、WHERE、HOW、VERIFY

好的请求遵循这一模式：

| 部分 | 用途 | 示例 |
|------|---------|---------|
| **WHAT** | 目标 | "修复空指针 bug" |
| **WHERE** | 范围 | "在 `src/auth/login.js` 的第 45 行" |
| **HOW** | 约束 | "不改变 API 签名" |
| **VERIFY** | 预期结果 | "所有现有测试应通过" |

### 优质请求示例

```
Fix the bug where login fails for emails with + symbols
WHERE: src/controllers/auth.js, line 78 (email validation regex)
HOW: Update the regex to allow + in emails, but keep existing validation otherwise
VERIFY: Existing tests in tests/auth.test.js should pass
```

### 劣质请求示例

```
Fix the bugs
```

Claude 不得不反过来询问后续问题，而无法立即解决问题。

---

## 会话上下文

**会话**（session）就是你当前与 Claude 的对话。

### 会话要点

- 运行 `claude` 时开始
- 退出或运行 `/clear` 时结束
- 默认不保存
- 作用域限定于单个项目
- 可用 `/rewind` 管理（回退 N 步）

### 检查点会话

保存会话（可选）：
```bash
/checkpoint save "fixed login, added tests"
```

之后恢复：
```bash
/checkpoint load "fixed login, added tests"
```

---

## 练习：完整循环

### 任务：创建一个简单的工具函数

1. **用 WHAT/WHERE/HOW/VERIFY 提出请求：**

```
Create a utility function to validate email addresses
WHERE: in src/utils/validators.js
HOW: export as validateEmail(email), return boolean, handle edge cases
VERIFY: Write tests in tests/validators.test.js
```

2. **Claude 进行分析：**
   - 找到 src/utils/
   - 读取现有的 validators
   - 检查测试目录结构
   - 提出解决方案

3. **审查 diff：**
   - 检查函数签名
   - 检查校验逻辑
   - 审查测试用例

4. **接受或迭代：**
   ```
   Looks good, but make the regex more permissive for + symbols
   ```

5. **Claude 更新** 后你再次审查

6. **完成：** 你得到了一个经过测试、可正常工作的函数

---

## 关键要点

✓ 每个请求都遵循：读取 → 分析 → 决策 → 提议 → 应用

✓ 保持具体（WHAT/WHERE/HOW/VERIFY）以获得更快的结果

✓ 上下文是有限的——关注你的百分比，在 70%+ 时执行 `/compact`

✓ 风险较高的改动用 `/plan`，安全的改动用普通模式

✓ 会话是临时的——用 `/checkpoint` 保存重要工作

---

## 验证：如果满足以下条件，你就准备好了……

✓ 你能向别人解释这 7 步循环
✓ 你理解"上下文"是什么以及它为何重要
✓ 你知道 Plan 模式和普通模式的区别
✓ 你已为某个复杂任务用过 `/plan`
✓ 你能查看 `/status` 并理解其输出

---

## 下一步？

**模块 03：Memory & Config** 涵盖：
- 创建你的第一个 CLAUDE.md
- Claude 如何记住偏好
- 项目级 vs 全局级设置
- 自定义配置

这将教你如何让 Claude Code 记住你的风格和偏好。

---

**完成了模块 02？** → 准备进入模块 03：Memory & Config
