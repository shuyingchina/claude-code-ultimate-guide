---
title: "Search Tools Mastery: Combining rg, grepai, Serena, ast-grep, scip-search & lilmd"
description: "Master code search and documentation navigation by combining the right tools for maximum efficiency"
tags: [workflow, search, guide, mcp]
---

# 搜索工具精通：组合使用 rg、grepai、Serena、ast-grep、scip-search 与 lilmd

> **通过组合合适的工具，精通代码搜索与文档导航，实现最高效率**

**作者**：Florian BRUNIAUX | 由 Claude (Anthropic) 贡献
**阅读时间**：约 25 分钟
**最后更新**：2026 年 5 月

---

## 目录

1. [快速参考矩阵](#quick-reference-matrix)
2. [工具对比](#tool-comparison)
3. [决策树](#decision-tree)
4. [组合工作流](#combined-workflows)
5. [真实场景](#real-world-scenarios)
6. [性能优化](#performance-optimization)
7. [常见陷阱](#common-pitfalls)
8. [扩展工具箱：scip-search 与 lilmd](#extended-toolkit-scip-search--lilmd)

---

## 快速参考矩阵

| 我需要…… | 使用此工具 | 命令示例 |
|--------------|---------------|-----------------|
| 查找精确文本 | `rg`（Grep 工具） | `rg "authenticate" --type ts` |
| 按含义查找 | `grepai` | `grepai search "user login flow"` |
| 查找函数定义 | `Serena` | `serena find_symbol --name "login"` |
| 查找结构化模式 | `ast-grep` | `ast-grep "async function $F"` |
| 查看谁调用了函数 | `grepai` | `grepai trace callers "login"` |
| 获取文件结构 | `Serena` | `serena get_symbols_overview` |
| 跨文件重构 | `Serena + ast-grep` | 组合工作流 |
| 探索未知代码库 | `grepai → Serena` | 发现模式 |
| 不依赖 MCP 查找符号引用（worktree 安全） | `scip-search` | `scip-search refs AuthService.login` |
| 导航大型 Markdown 文档 | `lilmd` | `lilmd read docs/arch.md "Authentication"` |

---

## 工具对比

### 完整功能矩阵

| 功能 | rg (ripgrep) | grepai | Serena | ast-grep |
|---------|--------------|--------|--------|----------|
| **搜索类型** | 正则/文本 | 语义（含义） | 符号感知 | AST 结构 |
| **技术** | 模式匹配 | 嵌入向量 (Ollama) | 符号解析 | 抽象语法树 |
| **速度** | ⚡ 约 20ms | 🐢 约 500ms | ⚡ 约 100ms | 🕐 约 200ms |
| **配置** | ✅ 无（内置） | ⚠️ Ollama + 安装 | ⚠️ MCP 配置 | ⚠️ npm install |
| **集成** | ✅ 原生（`Grep`） | ⚠️ MCP 服务器 | ⚠️ MCP 服务器 | ⚠️ 插件 |
| **隐私** | ✅ 100% 本地 | ✅ 100% 本地 | ✅ 100% 本地 | ✅ 100% 本地 |
| **所需上下文** | 无 | 无 | 项目索引 | 无 |
| **语言** | 全部（文本） | 全部 | TS/JS/Py/Rust/Go | TS/JS/Py/Rust/Go/C++ |
| **调用图** | ❌ 否 | ✅ 是 | ❌ 否 | ❌ 否 |
| **符号跟踪** | ❌ 否 | ❌ 否 | ✅ 是 | ❌ 否 |
| **会话记忆** | ❌ 否 | ❌ 否 | ✅ 是 | ❌ 否 |
| **误报率** | 中 | 低 | 极低 | 极低 |
| **学习曲线** | 低 | 中 | 低 | 高 |

### Token 成本对比

| 工具 | 典型查询 | 消耗的 Token | 返回的结果 |
|------|---------------|-----------------|------------------|
| **rg** | "authenticate" | 约 500 | 仅精确匹配 |
| **grepai** | "auth flow" | 约 2000 | 基于意图的匹配 |
| **Serena** | find_symbol | 约 1000 | 符号 + 上下文 |
| **ast-grep** | AST 模式 | 约 1500 | 结构化匹配 |

**关键洞察**：rg 的 Token 效率高出 4 倍，但智能程度比语义工具低 10 倍。

### 扩展工具参考

有两个工具弥补了核心工具栈中的空缺，在 [§ 扩展工具箱](#extended-toolkit-scip-search--lilmd) 中有深入介绍：

| 工具 | 类别 | 与现有工具栈的对比 |
|------|----------|-------------------|
| **scip-search** | 符号索引搜索 (SCIP) | 类似 Serena 但无状态、不依赖 MCP、worktree 安全 |
| **lilmd** | Markdown 章节导航 | 工具栈中无对应工具（面向文档，而非代码） |

---

## 决策树

### 第 1 层：你已知什么？

```
Do you know the EXACT text/pattern?
│
├─ YES → Use rg (ripgrep)
│  ├─ Known function name: rg "createSession"
│  ├─ Known import: rg "import.*React"
│  └─ Known pattern: rg "async function"
│
└─ NO → Go to Level 2
```

### 第 2 层：你在查找什么？

```
What's your search intent?
│
├─ "Find by MEANING/CONCEPT"
│  → Use grepai
│  └─ Example: grepai search "payment validation logic"
│
├─ "Find FUNCTION/CLASS definition"
│  → Use Serena
│  └─ Example: serena find_symbol --name "UserController"
│
├─ "Find by CODE STRUCTURE"
│  → Use ast-grep
│  └─ Example: async without error handling
│
└─ "Understand DEPENDENCIES"
   → Use grepai trace
   └─ Example: grepai trace callers "validatePayment"
```

### 第 2 层（Worktree / 无 MCP）

当运行在 CI 环境、git worktree，或任何 MCP 服务器不可用的场景时：

```
Known symbol name, no MCP available?
│
└─ Use scip-search (pre-built SCIP index, millisecond cold start)
   └─ scip-search refs "AuthService.login" --format json
```

### 第 3 层：优化

```
Found too many results?
│
├─ rg → Add --type filter or narrow path
├─ grepai → Add --path filter or use trace
├─ Serena → Filter by symbol type (function/class)
└─ ast-grep → Add constraints to pattern
```

---

## 组合工作流

### 工作流 1：探索未知代码库

**目标**：快速理解一个新项目

**分步操作**：

```bash
# 1. SEMANTIC DISCOVERY (grepai)
# Find files related to authentication
grepai search "user authentication and session management"
# → Output: auth.service.ts, session.middleware.ts, user.controller.ts

# 2. STRUCTURAL OVERVIEW (Serena)
# Understand each file's structure
serena get_symbols_overview --file auth.service.ts
# → Output:
#   - class AuthService
#     - login(email, password)
#     - logout(sessionId)
#     - validateSession(token)

# 3. DEPENDENCY MAPPING (grepai trace)
# See how login is used
grepai trace callers "login"
# → Output: Called by UserController, ApiGateway, AdminPanel

# 4. EXACT SEARCH (rg)
# Find specific implementation details
rg "validateSession" --type ts -A 5
# → Output: Full function with 5 lines of context
```

**结果**：4 条命令即可完整理解（相比之下需读取 30 多个文件）

---

### 工作流 2：大规模重构

**目标**：在 50 多个文件中将 `createSession` → `initializeUserSession` 重命名

**分步操作**：

```bash
# 1. IMPACT ANALYSIS (grepai trace)
# Understand full scope
grepai trace callers "createSession"
# → Output: 47 callers across 23 files
grepai trace callees "createSession"
# → Output: Calls validateUser, createToken, storeSession

# 2. STRUCTURAL VALIDATION (ast-grep)
# Ensure consistent usage pattern
ast-grep "createSession($$$ARGS)"
# → Output: All invocations with their argument patterns

# 3. SYMBOL-AWARE REFACTORING (Serena)
# Precise renaming
serena find_symbol --name "createSession" --include-body true
# → Get exact definition + all references

serena replace_symbol_body \
  --name "createSession" \
  --new-name "initializeUserSession"
# → Rename across all files maintaining structure

# 4. VERIFICATION (rg)
# Confirm no old references remain
rg "createSession" --type ts
# → Should return 0 results
```

**结果**：在充分掌握依赖关系的前提下安全重构

---

### 工作流 3：安全审计

**目标**：查找安全漏洞

**分步操作**：

```bash
# 1. SEMANTIC DISCOVERY (grepai)
# Find security-sensitive code
grepai search "SQL query construction"
grepai search "user input validation"
grepai search "password handling"

# 2. STRUCTURAL PATTERNS (ast-grep)
# Find specific vulnerability patterns

# SQL injection risks
ast-grep 'db.query(`${$VAR}`)'

# XSS risks
ast-grep 'innerHTML = $VAR'

# Missing error handling
ast-grep -p 'async function $F($$$) { $$$BODY }' \
  --without 'try { $$$TRY } catch'

# 3. DEPENDENCY TRACING (grepai)
# See where vulnerable code is called
grepai trace callers "executeQuery"
# → Identify all entry points

# 4. EXACT VERIFICATION (rg)
# Confirm findings
rg "innerHTML\s*=" --type ts
rg "password" --type ts | rg -v "hashed"
```

**结果**：几分钟内完成全面的安全审计

---

## 真实世界基准测试

### grepai vs grep（2026 年 1 月）

**背景**：在 Excalidraw（15.5 万行 TypeScript）上的基准测试
**作者**：YoanDev（grepai 维护者 - 存在潜在偏见）
**方法论**：5 个相同的代码发现问题

| 指标 | grep | grepai | 差异 |
|----------|------|--------|------------|
| Tool calls | 139 | 62 | **-55%** |
| Input tokens | 51k | 1.3k | **-97%** |

**要点**：语义搜索通过在第一次尝试时就识别出相关文件，避免了迭代式探索，从而大幅减少了 token 消耗。

**局限性**：
- 由工具维护者进行的基准测试
- 单项目验证（仅 TypeScript）
- 迄今为止尚无独立验证

**来源**：[yoandev.co/grepai-benchmark](https://yoandev.co/grepai-benchmark)

> **注意**：此基准测试反映的是 2026 年 1 月的状态。随着 Claude Code 和 grepai 的更新，性能可能会发生变化。

---

### 工作流 4：框架迁移

**目标**：将 React class components 迁移到 hooks

**分步操作**：

```bash
# 1. INVENTORY (ast-grep)
# Find all class components
ast-grep 'class $C extends React.Component'
# → Output: 34 components to migrate

# 2. DEPENDENCY ANALYSIS (grepai)
# Understand component relationships
for component in $(ast-grep 'class $C extends' --json | jq -r '.[].name'); do
  grepai trace callers "$component"
done
# → Build migration order (leaf components first)

# 3. PATTERN DETECTION (ast-grep)
# Identify lifecycle methods used
ast-grep 'componentDidMount() { $$$BODY }'
ast-grep 'componentWillReceiveProps($$$) { $$$BODY }'
# → Map to equivalent hooks

# 4. INCREMENTAL MIGRATION (Serena + ast-grep)
# Migrate one component at a time
serena find_symbol --name "UserProfile" --include-body true
# → Get full component code

# Use ast-grep to transform
ast-grep --rewrite \
  --from 'class $C extends React.Component' \
  --to 'const $C = () => { }'

# 5. VERIFICATION (rg + grepai)
# Ensure migration successful
rg "React.Component" --type tsx  # Should decrease
grepai search "component lifecycle methods"  # Find any missed
```

**结果**：系统化的迁移，破坏性影响最小

---

### 工作流 5：性能优化

**目标**：识别并修复性能瓶颈

**分步操作**：

```bash
# 1. HOTSPOT DISCOVERY (grepai)
# Find performance-critical code
grepai search "heavy computation or loops"
grepai search "database queries in loops"

# 2. PATTERN DETECTION (ast-grep)
# Find N+1 query patterns
ast-grep 'for ($$$) { await db.query($$$) }'

# Find missing memoization
ast-grep 'useMemo' --invert-match \
  --in 'const $VAR = $$$'

# 3. CALL GRAPH ANALYSIS (grepai trace)
# Find hot paths
grepai trace graph "renderUserList" --depth 3
# → Visualize dependency tree

# 4. SYMBOL TRACKING (Serena)
# Track function changes
serena write_memory "perf_baseline" \
  "renderUserList: 450ms avg"

# After optimization
serena write_memory "perf_optimized" \
  "renderUserList: 45ms avg (10x improvement)"

# 5. VERIFICATION (rg)
# Confirm optimizations applied
rg "useMemo|useCallback" --type tsx
```

**结果**：数据驱动的性能改进

---

## 真实世界场景

### 场景 1："我不知道自己在找什么"

**问题**：新项目，没有文档，需要添加功能

**解决方案**：语义优先的发现

```bash
# Start broad with meaning
grepai search "user profile management"
# → Discover relevant files

# Then narrow with structure
serena get_symbols_overview --file user-profile.service.ts
# → Understand available functions

# Finally, exact search for details
rg "updateProfile" --type ts -C 3
```

---

### 场景 2："这个函数到处都在被调用"

**问题**：需要修改一个函数，但担心破坏其他东西

**解决方案**：先做依赖映射

```bash
# 1. See all callers
grepai trace callers "calculateTotal"
# → 47 callers found

# 2. Analyze caller contexts
for file in $(grepai trace callers "calculateTotal" --json | jq -r '.[].file'); do
  serena get_symbols_overview --file "$file"
done

# 3. Identify safe vs risky call sites
ast-grep 'calculateTotal($ARGS)' --json
# → Group by argument patterns

# 4. Make change with confidence
# Now you know all impact points
```

---

### 场景 3："找出所有执行 X 操作的代码"

**问题**：需要在整个代码库中应用一致的模式

**解决方案**：结合语义 + 结构

```bash
# Example: Find all error handling code

# 1. Semantic discovery
grepai search "error handling and exception management"

# 2. Structural patterns
ast-grep 'try { $$$TRY } catch ($ERR) { $$$CATCH }'
ast-grep 'throw new Error($MSG)'

# 3. Verify consistency
rg "catch\s*\(" --type ts | wc -l
# Compare with ast-grep count to find anomalies
```

---

### 场景 4："我需要理解这个模块"

**问题**：复杂的模块，职责不清晰

**解决方案**：多工具分析

```bash
# 1. Get symbol overview (Serena)
serena get_symbols_overview --file payment.module.ts
# → See all exports, classes, functions

# 2. Understand dependencies (grepai)
grepai trace callees "PaymentModule"
# → What does this module use?

grepai trace callers "PaymentModule"
# → Who uses this module?

# 3. Find implementation patterns (ast-grep)
ast-grep 'export class $C' --file payment.module.ts
ast-grep 'async $METHOD($$$)' --file payment.module.ts

# 4. Read specific implementations (rg)
rg "processPayment" --type ts -A 20
```

---

## 性能优化

### 选择最快的工具

**通用规则**：

1. **已知确切文本** → 始终先用 rg
2. **未知确切文本** → 先用 grepai，再用 rg 验证
3. **重构** → Serena 保障符号安全
4. **大规模迁移** → ast-grep 提供结构级精度

### 性能基准测试

**测试**：在 50 万行代码库中查找认证代码

| 策略 | 耗时 | 结果质量 |
|----------|------|-----------------|
| 仅用 rg "auth" | 0.2s | 5000+ 误报 |
| 仅用 grepai "auth" | 2.5s | 50 条相关结果 |
| grepai → rg（组合） | 2.7s | 50 条相关且已验证 |
| 仅用 Serena symbols | 1.5s | 12 个 auth 函数 |
| ast-grep patterns | 3.0s | 8 条 auth 流程 |

**胜出者**：对于已知函数名，Serena symbols（最快 + 高质量）

### 并行化策略

**适用于大型代码库（>10 万行）**：

```bash
# Run searches in parallel

# Terminal 1: Semantic discovery
grepai search "authentication flow" > /tmp/grepai-results.json &

# Terminal 2: Symbol indexing
serena get_symbols_overview --file src/**/*.ts > /tmp/symbols.json &

# Terminal 3: Pattern detection
ast-grep 'async function $F' --json > /tmp/ast-results.json &

# Wait for all, then combine results
wait
jq -s '.[0] + .[1] + .[2]' \
  /tmp/grepai-results.json \
  /tmp/symbols.json \
  /tmp/ast-results.json
```

---

## 常见陷阱

### 陷阱 1：用语义搜索做精确匹配

❌ **错误**：
```bash
grepai search "createSession"  # Slow, overkill
```

✅ **正确**：
```bash
rg "createSession" --type ts  # Fast, precise
```

**规则**：如果你知道确切文本，永远不要使用语义搜索。

---

### 陷阱 2：用 rg 做概念性搜索

❌ **错误**：
```bash
rg "auth.*login.*session" --type ts  # Misses variations
```

✅ **正确**：
```bash
grepai search "authentication and session management"
```

**规则**：正则表达式不理解含义，应使用语义工具。

---

### 陷阱 3：重构前忽略调用图

❌ **错误**：
```bash
# Directly refactor without checking callers
rg "oldFunction" --type ts | sed 's/oldFunction/newFunction/g'
```

✅ **正确**：
```bash
# Check impact first
grepai trace callers "oldFunction"
# See 47 callers across 23 files
# Then plan refactoring strategy
```

**规则**：修改共享代码前，始终先追踪依赖关系。

---

### 陷阱 4：不组合使用工具

❌ **错误**：
```bash
# Use only one tool for complex task
ast-grep 'async function $F' --json | jq '.[].file' | xargs -I {} vim {}
# Blindly edit without understanding context
```

✅ **正确**：
```bash
# Combine for full understanding
ast-grep 'async function $F' --json > /tmp/async.json
for file in $(jq -r '.[].file' /tmp/async.json); do
  serena get_symbols_overview --file "$file"  # Context
  grepai trace callers "$(jq -r '.[].name' /tmp/async.json)"  # Usage
done
```

**规则**：复杂任务需要多个视角。

---

### 陷阱 5：对简单搜索过度设计

❌ **错误**：
```bash
# Setup grepai + Ollama just to find a TODO comment
grepai search "TODO comments in the code"
```

✅ **正确**：
```bash
rg "TODO" --type ts
```

**规则**：使用能解决问题的最简单工具。

---

## 工具选择速查表

### 快速决策矩阵

| 你的情况 | 用这个 | 而不是这个 |
|----------------|----------|----------|
| "查找函数 `login`" | rg "login" | grepai search "login" |
| "查找 login 相关代码" | grepai "login flow" | rg "login.*" |
| "安全地重命名函数" | Serena find_symbol | rg + sed |
| "谁调用了这个函数？" | grepai trace callers | rg + grep |
| "获取文件结构" | Serena overview | rg "class\|function" |
| "查找没有 try/catch 的 async" | ast-grep | rg "async.*{" |
| "迁移 React 类组件" | ast-grep | rg + 手动 |
| "查找 TODO" | rg "TODO" | 任何其他工具 |

---

## 扩展工具集：scip-search 与 lilmd

两个 CLI 工具，弥补了 rg/grepai/Serena 技术栈中的空白。

### scip-search

scip-search 查询预构建的 SCIP（Sourcegraph Code Intelligence Protocol）符号索引。grepai 按语义含义搜索、Serena 需要实时的 MCP 连接，而 scip-search 针对静态二进制索引运行，冷启动仅需毫秒级。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [github.com/liza-mas/scip-search](https://github.com/liza-mas/scip-search) |
| **安装** | `curl -fsSL https://raw.githubusercontent.com/liza-mas/scip-search/main/install.sh \| bash` |
| **索引格式** | SCIP（Go、TypeScript、Python、Java、Rust 等） |
| **输出** | 单行文本、JSON 或仅位置 |

**工作流**：scip-search 取代了符号发现通常所需的 5-10 次 rg/read 往返。

```bash
# Step 1: generate SCIP index once per language
scip-typescript index --output index.scip

# Step 2: find a symbol definition
scip-search find AuthService

# Step 3: get all references with line numbers
scip-search refs AuthService.login --format json

# Step 4: read only the returned line ranges
```

**对比 Serena**：Serena 连接到语言服务器并具有会话记忆。scip-search 是无状态的，针对快照运行：没有 MCP，没有常驻进程。这使其在 worktree 和临时 CI 环境中更可靠——在这些场景中 Serena 的 LSP 后端可能不可用。

**对比 grepai**：grepai 按语义意图查找（"payment validation logic"）。scip-search 按精确或近似精确的符号标识符查找。二者可以串联使用：grepai 发现概念，scip-search 确认符号。

**Worktree 兼容性**：索引是每个仓库的本地文件，没有共享状态。在 worktree 内运行 `scip-typescript index` 会为该 worktree 生成一个本地索引。

---

### lilmd

lilmd 将 Markdown 文件视为数据库。它返回带行号范围的目录，并支持定向读取章节。读取一份 2,000 行的指南时，agent 只需一次调用即可获取某个章节，而无需读取整个文件。

| 属性 | 详情 |
|-----------|---------|
| **来源** | [github.com/molefrog/lilmd](https://github.com/molefrog/lilmd) |
| **安装** | `npm install -g lilmd` |
| **运行时** | Node 或 Bun |

**关键命令**：

```bash
# TOC with line ranges (inclusive, 1-indexed)
lilmd docs/architecture.md

# Read a section by name (fuzzy match by default)
lilmd read docs/architecture.md "Authentication"

# Read a nested section
lilmd read docs/architecture.md "Security > JWT"

# Exact match (prefix with =)
lilmd read docs/architecture.md "=Authentication Flow"
```

**对 agent 的特定价值**：TOC 输出包含每个标题的行号范围。agent 解析这些范围后只请求相关章节，而非加载整个文件。自然的流程是：`rg`（找到是哪个文件）然后 `lilmd`（获取带范围的 TOC）然后 `Read lines:N-M`（加载特定章节）。这同样适用于 CHANGELOG.md、大型 README 文件和知识库文档。

**Worktree 兼容性**：无状态、无索引、按文件运行。在任何地方都能工作。

---

## 配置优先级

**推荐的配置顺序**:

1. **开始**: rg(已通过 Grep 工具内置）✅
2. **接下来**: Serena MCP(符号感知、会话记忆）
3. **然后**: grepai(语义搜索 + 调用图）
4. **如果 worktree 是你工作流的一部分**: scip-search(无状态符号查找，无需 MCP）
5. **针对大型文档**: lilmd(定向读取 Markdown 章节，无需配置）
6. **最后**: ast-grep(结构化模式、大规模重构）

**理由**: 90% 的搜索用 rg + Serena 就能完成。有语义需求时加上 grepai。在 MCP 不可用的 worktree 或 CI 环境中加上 scip-search。仅在大规模重构时才加上 ast-grep。

---

## 总结：6 工具工具箱

```
┌─────────────────────────────────────────────────────────┐
│                   SEARCH TOOL MASTERY                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  rg (ripgrep)     →  Fast, exact text matching         │
│  ├─ Use: 90% of searches                               │
│  └─ Speed: ~20ms                                        │
│                                                         │
│  grepai           →  Semantic + Call graph             │
│  ├─ Use: Concept discovery, dependency tracing         │
│  └─ Speed: ~500ms (finds what rg cannot)               │
│                                                         │
│  Serena           →  Symbol-aware + Session memory     │
│  ├─ Use: Refactoring, structure understanding          │
│  └─ Speed: ~100ms                                       │
│                                                         │
│  ast-grep         →  AST structural patterns           │
│  ├─ Use: Large migrations, complex patterns            │
│  └─ Speed: ~200ms                                       │
│                                                         │
│  scip-search      →  Symbol index (stateless, SCIP)   │
│  ├─ Use: CI / worktrees / no MCP environments          │
│  └─ Speed: ~5ms cold start                             │
│                                                         │
│  lilmd            →  Markdown section navigation       │
│  ├─ Use: Large docs, TOC + line ranges per section     │
│  └─ Speed: instant, no index                           │
│                                                         │
│  ═══════════════════════════════════════════════════   │
│                                                         │
│  Master the combination, not individual tools.          │
│  Each tool has a sweet spot. Use the right one.        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 延伸阅读

- [Serena MCP 指南](#serena-semantic-code-analysis)
- [grepai 文档](#grepai-recommended-semantic-search)
- [ast-grep 模式技能](../../examples/skills/ast-grep-patterns.md)
- [架构：Grep vs RAG 历史](../core/architecture.md#search-strategy-evolution)
- [scip-search GitHub](https://github.com/liza-mas/scip-search)
- [lilmd GitHub](https://github.com/molefrog/lilmd)

---

**最后更新**: 2026 年 5 月
**兼容版本**: Claude Code 2.1.7+
