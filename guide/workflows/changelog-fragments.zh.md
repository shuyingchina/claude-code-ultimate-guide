# Changelog 片段：强制执行的逐 PR 文档化

一种 3 层强制执行模式，确保每个 PR 在编写时即被文档化，而不是等到发版时才补。

---

## 问题所在

单一的 `CHANGELOG.md` 文件在活跃团队中会出问题。三个开放的功能分支都改动同一个文件，意味着每次合并都会产生冲突。有人去解决冲突，丢掉了一行，于是发版说明在发布前就已经错了。

更深层的问题在于时机。"发版时再文档化"听起来很合理，直到你在 PR #840 合并三周后盯着它，试图重建对用户而言到底改了什么。提交信息写的是 `fix session handling`。开发者在另一个时区。上下文已经丢失。

没有 CI 门禁的强制执行会让 changelog 变成一份催活儿。每次发版前都得有人在时间压力下追着别人，从 git log 里把空白填上。

解决方案：每个 PR 一份 YAML 片段，在实现过程中编写，由 CI 校验，在发版时自动组装。

---

## 3 层架构

这套系统之所以有效，是因为强制执行发生在三个独立的层级上。每一层捕获一种不同的失败模式。

### 第 1 层：CLAUDE.md 工作流规则

第一层是一条在每次会话时加载进 Claude Code 上下文的规则。它编码了完整的片段工作流，因此当被要求创建 PR 时，Claude 可以自主完成它。

```markdown
# git-workflow.md (loaded via CLAUDE.md)

## Changelog Fragment — Required Before Every PR

Before creating a PR, always generate a changelog fragment.

### Steps

1. **Infer from git diff** — analyze `git diff main...HEAD` to determine:
   - `type`: feat | fix | perf | refactor | security | docs | chore
   - `scope`: the functional area affected (auth, sessions, api, etc.)
   - `title`: one-line user-facing summary (< 80 chars)

2. **Create the fragment** — run `pnpm changelog:add` or write directly:
   ```
   changelog/fragments/{PR_NUMBER}-{slug}.yml
   ```

3. **Validate** — run `pnpm changelog:validate changelog/fragments/{file}.yml`

4. **Commit alongside the PR** — include the fragment in the same branch

### Fragment schema

```yaml
pr: 886                    # must match filename prefix
type: fix                  # feat|fix|perf|refactor|security|docs|chore
scope: "visiochat"
title: "Fix empty chat after SSE race condition"   # < 80 chars
description: |             # optional — explain user impact, not implementation
  SSE workplan fires before AI stream completes, causing ChatWrapper
  to mount with 0 messages.
breaking: false
migration: false           # set true if PR adds a DB migration
```

### Bypass

Add label `skip-changelog` for PRs with no user impact (CI config, deps updates, release commits).
```

这条规则让 Claude Code 成为强制执行的参与者，而不仅仅是一个编码工具。当开发者说"创建这个 PR"时，Claude 会从 diff 中推断出片段内容，并在打开 PR 之前创建它。

### 第 2 层：UserPromptSubmit Hook（行为检测）

第二层在意图转化为动作之前进行拦截。当开发者输入某些信号表明有创建 PR 的意图时，该 hook 会检查是否提及了 changelog 片段。

```bash
# .claude/hooks/smart-suggest.sh (excerpt — Tier 0 enforcement)

# PR creation intent detected
if echo "$PROMPT_LC" | grep -qE '(create.*pr|open.*pr|make.*pr|pull.?request|push.*pr)'; then
    # Fragment not mentioned → redirect to creation step first
    if ! echo "$PROMPT_LC" | grep -qE '(changelog|fragment|skip-changelog)'; then
        suggest "pnpm changelog:add" \
            "REQUIRED before merge — creates changelog/fragments/{PR}-{slug}.yml"
    else
        # Already mentioned → suggest the PR command normally
        suggest "/pr" "PR creation with structured description"
    fi
fi
```

该 hook 是 `UserPromptSubmit`：非阻塞，每个提示最多一条建议，无匹配时保持静默。它在 Claude Code 处理提示之前运行，因此开发者会在 Claude 开始做任何事情之前就内联看到这条提醒。

这里的条件逻辑（`if X without Y`）是关键模式。它不是一刀切的拦截器——它会根据上下文自适应。如果开发者已经提及了片段，他们会收到常规建议。如果没有，他们会收到强制执行提醒。

**带 3 层架构的完整 hook**：[`examples/hooks/bash/smart-suggest.sh`](../../examples/hooks/bash/smart-suggest.sh)

### 第 3 层：CI 强制执行（GitHub Actions）

第三层是硬门禁。每个以主分支为目标的 PR 都会运行两个独立的作业。

**`check-fragment` 作业**：先检查绕过标签（封闭清单），然后要求 `changelog/fragments/{PR_NUMBER}-*.yml` 存在并通过结构校验。

```yaml
- name: Check fragment exists and is valid
  env:
    PR_NUMBER: ${{ github.event.pull_request.number }}
    PR_LABELS: ${{ toJson(github.event.pull_request.labels.*.name) }}
  run: |
    SKIP_LABELS=("skip-changelog" "dependencies" "release" "chore: deps")
    for LABEL in "${SKIP_LABELS[@]}"; do
      if echo "$PR_LABELS" | grep -q "\"$LABEL\""; then
        echo "Bypass label detected — fragment not required"
        exit 0
      fi
    done

    FRAGMENT=$(ls "changelog/fragments/${PR_NUMBER}-"*.yml 2>/dev/null | head -1)
    if [ -z "$FRAGMENT" ]; then
      echo "Fragment missing. Run: pnpm changelog:add"
      exit 1
    fi

    pnpm tsx changelog/scripts/validate.ts "$FRAGMENT"
```

**`check-migration-flag` 作业**（独立运行，无绕过）：用 `git diff --name-only --diff-filter=A` 检测新的 SQL 迁移文件。如果存在迁移而片段中 `migration: false`，则失败。该作业无法通过标签绕过——一个添加了迁移的 `skip-changelog` PR 仍然会触发检查。

这两个作业在设计上是相互独立的。一个 PR 可以（通过标签）绕过片段创建，但仍可能无法通过迁移检查。

---

## 发版时的片段组装

随着 PR 合并，片段在 `changelog/fragments/` 中累积。在发版时，一条命令将它们组装成一个带版本号的 CHANGELOG 章节。

```bash
pnpm changelog:assemble --version 1.8.0 [--dry-run]
```

它的作用：
1. 读取所有 `changelog/fragments/*.yml`
2. 按固定顺序（feat、fix、perf、refactor、security、docs、chore）按类型分组
3. 将 `breaking: true` 的条目提取到专门的 `🔨 Breaking Changes` 章节
4. 对 `migration: true` 的条目内联标注 `⚠️ Migration DB.`
5. 替换 `CHANGELOG.md` 中的 `## [Next Release]` 占位符
6. 将片段归档到 `changelog/fragments/released/{version}/`

输出：
```markdown
## [1.8.0] - 2026-03-15

### 🔨 Breaking Changes
- **Remove legacy token format (#871)** — Tokens issued before v1.6.0 are invalid.

### ✨ New Features
- **Add real-time presence indicators (#892)**

### 🔧 Bug Fixes
- **Fix empty chat after SSE race condition (#886)** — SSE workplan fires before
  AI stream completes, causing ChatWrapper to mount with 0 messages.
```

---

## 为什么是 3 层，而非 1 层

每一层捕获一种不同的失败模式：

| 层 | 捕获的失败 | 何时 |
|-------|---------------|------|
| CLAUDE.md 规则 | Claude 忘记工作流 | 每次会话 |
| UserPromptSubmit hook | 开发者不假思索地输入"创建这个 PR" | 提示前 |
| CI 门禁 | 片段被跳过或已损坏 | 合并前 |

单一的 CI 门禁捕获问题太晚——开发者必须在 PR 已经打开之后切回上下文。hook 在意图产生时就捕获它。CLAUDE.md 规则意味着当任务交给 Claude 时，它会自主处理。

这些层不会相互冲突。它们相互强化。看到 hook 建议的开发者会运行 `pnpm changelog:add`。Claude 会遵循 CLAUDE.md 规则并校验输出。CI 在合并前确认一切就绪。

---

## 采用这一模式

这些 TypeScript 脚本（add、validate、assemble、audit）是 Méthode Aristote 技术栈专属的。但 3 层强制执行模式不是——它适用于任何片段格式、任何 CI 系统、任何组装器。

**最小可行配置：**

1. **定义你的片段 schema**（YAML、JSON，任何适合你技术栈的格式）
2. **添加一条 CLAUDE.md 规则**，编码创建工作流，使 Claude 能自主处理
3. **添加一个 `UserPromptSubmit` hook**，采用 `if PR-intent without fragment-mention → suggest` 模式
4. **添加一个 CI 作业**，在合并前检查片段是否存在

该 hook 模式可推广到任何强制性的工作流步骤。把"changelog 片段"替换成"ADR"、"迁移标志"、"测试覆盖率检查"——条件检测逻辑是相同的。

---

## 相关内容

- Hook 示例：[`examples/hooks/bash/smart-suggest.sh`](../../examples/hooks/bash/smart-suggest.sh)
- Hook 文档：[UserPromptSubmit Hooks](../ultimate-guide.md)（搜索 "UserPromptSubmit"）
- 片段校验器和组装器脚本：可在 Méthode Aristote 仓库中获取
