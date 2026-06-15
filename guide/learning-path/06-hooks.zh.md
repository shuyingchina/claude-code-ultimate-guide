# 模块 06：Hooks 与事件

**时长**：1 小时 | **难度**：⭐⭐ 中级

## 目标

自动响应系统事件。创建在 Claude Code 操作之前或之后运行的脚本。

---

## 你将学到

- hooks 的工作原理及其触发时机
- 创建提交前校验
- 构建操作后通知
- 编写安全的自动化脚本
- 常见的 hook 模式

---

## 什么是 Hooks？

**hook** 是一个响应事件而自动运行的脚本。

### 示例：提交前 Hook

在你提交更改之前：

```
You run: git commit -m "Fix bug"
       ↓
Hook runs: Check version number consistency
       ↓
If version wrong:
  ❌ Commit blocked
  Error message shows what's wrong
       ↓
You fix: Update VERSION file
       ↓
Commit succeeds
```

hooks 能在常见错误进入 git 之前就将其拦截。

### Hook 事件

hooks 可以在以下时机触发：

| 事件 | 触发时机 | 适用场景 |
|-------|--------|----------|
| PreToolUse | Claude 运行某个工具之前 | 校验请求 |
| PostToolUse | Claude 运行某个工具之后 | 记录结果、检查输出 |
| PreCommit | git commit 之前 | 校验更改 |
| PostPush | git push 之后 | 通知团队 |

---

## 创建你的第一个 Hook

hooks 是位于 `.claude/hooks/` 中的 bash（或 PowerShell）脚本。

### 基本 Hook 结构

```bash
#!/bin/bash

# Hook: validate-version
# Event: PreCommit
# Description: Check that VERSION file is updated with other changes

# Get the files being committed
FILES=$(git diff --cached --name-only)

# Check if guide files were changed
if echo "$FILES" | grep -q "guide/"; then
  # If guide/ changed, VERSION must also be changed
  if ! echo "$FILES" | grep -q "VERSION"; then
    echo "❌ Error: guide/ was modified but VERSION wasn't updated"
    echo "Run: echo '3.x.x' > VERSION"
    exit 1  # Block commit
  fi
fi

exit 0  # Allow commit
```

### 文件位置

```
my-project/
└── .claude/
    └── hooks/
        ├── validate-version.sh
        └── notify-team.sh
```

### Hook 退出码

```bash
exit 0   # Success - allow operation to proceed
exit 1   # Failure - block operation and show error
exit 2   # Warning - allow but show warning message
```

---

## Hook 模式

### 模式 1：提交前校验

拦截未通过校验的提交：

```bash
#!/bin/bash
# Hook: security-check.sh
# Block commits if security issues found

# Check for hardcoded API keys
if grep -r "sk_live_" .; then
  echo "❌ ERROR: Found hardcoded Stripe key"
  exit 1
fi

# Check for console.log in production code (not tests)
if grep -r "console.log" src/ --exclude-dir=tests; then
  echo "❌ ERROR: Found console.log in source code"
  exit 1
fi

# Check for TODO comments (warning, not block)
if grep -r "TODO:" src/; then
  echo "⚠️  Warning: TODO comments found (not blocking)"
fi

exit 0
```

### 模式 2：提交后通知

在提交成功之后：

```bash
#!/bin/bash
# Hook: notify-team.sh
# Notify team after certain commits

COMMIT_MSG=$(git log -1 --pretty=%B)

# If security-related commit
if echo "$COMMIT_MSG" | grep -i "security"; then
  echo "🔐 Security commit: $COMMIT_MSG"
  # Send to Slack (optional)
  # curl -X POST $SLACK_WEBHOOK -d "Security update: $COMMIT_MSG"
fi

exit 0
```

### 模式 3：依赖检查

当依赖需要更新时发出警告：

```bash
#!/bin/bash
# Hook: check-deps.sh
# Check if package.json changed without updating lock file

FILES=$(git diff --cached --name-only)

if echo "$FILES" | grep -q "package.json"; then
  if ! echo "$FILES" | grep -q "package-lock.json"; then
    echo "⚠️  Warning: package.json changed but lock file wasn't updated"
    echo "Run: npm install"
  fi
fi

exit 0
```

---

## 注册 Hooks

hooks 在 `.claude/settings.json` 中注册：

```json
{
  "hooks": {
    "pre_commit": ["validate-version.sh", "security-check.sh"],
    "post_commit": ["notify-team.sh"],
    "post_push": ["deploy-staging.sh"]
  }
}
```

或在 `settings.yaml` 中：

```yaml
hooks:
  pre_commit:
    - path: hooks/validate-version.sh
      description: "Check VERSION file updated"
      blocking: true
    - path: hooks/security-check.sh
      blocking: true
  post_commit:
    - path: hooks/notify-team.sh
      blocking: false
```

---

## 安全 hooks 的最佳实践

### 应该做

✅ 让 hooks 具备**幂等性**（可以安全地多次运行）
✅ 记录 hook 正在做什么
✅ 退出时给出清晰的错误信息
✅ 在顶部使用 `set -e`，在第一个错误处即失败
✅ 让 hooks 可执行：`chmod +x hook.sh`

### 不应该做

❌ 让 hooks 耗时超过 5 秒（会阻塞工作流）
❌ 让 hooks 发起网络调用（不可靠）
❌ 让 hooks 修改文件（它们只做校验）
❌ 让 hooks 过于严格（会让开发者抓狂）
❌ 忘记先在本地测试 hooks

---

## 安全 Hook 模板

```bash
#!/bin/bash
set -euo pipefail

# Hook template for safe, clear automation

HOOK_NAME="my-hook"
HOOK_VERSION="1.0.0"

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

log_error() {
  echo -e "${RED}❌ $1${NC}"
}

log_warn() {
  echo -e "${YELLOW}⚠️  $1${NC}"
}

log_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

# Main validation logic
main() {
  echo "Running: $HOOK_NAME ($HOOK_VERSION)"
  
  # Your checks here
  if some_check_fails; then
    log_error "Check failed because X"
    return 1
  fi
  
  log_success "All checks passed"
  return 0
}

# Run and exit
main
exit $?
```

---

## 练习：创建一个校验 Hook

### 场景

你希望阻止那些包含以下问题的意外提交：
- 行尾空白
- 新代码缺少测试文件
- 未解决的合并冲突

### 第 1 步：创建 Hook

```bash
cat > .claude/hooks/pre-commit-validation.sh << 'EOF'
#!/bin/bash
set -euo pipefail

echo "🔍 Running pre-commit validation..."

# Check 1: No trailing whitespace
if git diff --cached | grep -E '^[+].*\s+$' > /dev/null; then
  echo "❌ Trailing whitespace found:"
  git diff --cached | grep -E '^[+].*\s+$'
  exit 1
fi

# Check 2: No merge conflict markers
if git diff --cached | grep -E '^[+].*<<<<<<|^[+].*======|^[+].*>>>>>>' > /dev/null; then
  echo "❌ Merge conflict markers found"
  exit 1
fi

# Check 3: New files should have tests
STAGED_FILES=$(git diff --cached --name-only)
for file in $STAGED_FILES; do
  if [[ $file == src/*.ts && $file != *test* ]]; then
    TEST_FILE="${file%.ts}.test.ts"
    if ! git ls-files | grep -q "$TEST_FILE"; then
      echo "⚠️  Warning: New file $file has no test file"
    fi
  fi
done

echo "✅ Pre-commit validation passed"
exit 0
EOF

chmod +x .claude/hooks/pre-commit-validation.sh
```

### 第 2 步：在 settings.json 中注册

```json
{
  "hooks": {
    "pre_commit": ["hooks/pre-commit-validation.sh"]
  }
}
```

### 第 3 步：测试它

创建一个带有行尾空白的文件：

```bash
echo "test line   " > test.txt  # Note the trailing spaces
git add test.txt
```

尝试提交：

```bash
git commit -m "Test hook"
```

Hook 会阻止提交：

```
❌ Trailing whitespace found:
+test line
```

### 第 4 步：修复并重试

```bash
echo "test line" > test.txt  # Remove trailing spaces
git add test.txt
git commit -m "Test hook (fixed)"
```

现在它成功了：

```
✅ Pre-commit validation passed
```

---

## 调试 Hooks

如果某个 hook 莫名其妙地失败：

1. **手动运行**：
```bash
bash .claude/hooks/my-hook.sh
```

2. **添加调试输出**：
```bash
set -x  # Print every command
```

3. **检查退出码**：
```bash
bash .claude/hooks/my-hook.sh; echo "Exit: $?"
```

4. **测试 hook 的条件**：
```bash
# Test if a file was changed
git diff --cached --name-only | grep "VERSION"
echo $?  # 0 = found, 1 = not found
```

---

## 验证：如果满足以下条件，你就准备好了……

✓ 你已经创建了至少一个 hook 脚本

✓ 你理解 hook 的事件类型（pre-commit、post-commit 等）

✓ 你能在 settings.json 或 settings.yaml 中注册 hooks

✓ 你已经在本地测试过一个 hook

✓ 你知道退出码的含义（0 = 成功，1 = 失败）

---

## 下一步是什么？

**模块 07：高级模式** 涵盖：
- 多 agent 编排
- 构建复杂工作流
- 错误处理与恢复
- 生产级自动化
- 团队协作模式

本模块教你如何将之前所有的概念组合成复杂的多 agent 系统。

---

**完成模块 06 了吗？** → 准备进入模块 07：高级模式
