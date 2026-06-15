---
title: "团队 AI 指令管理"
description: "使用基于配置档案的模块组装方式，将 CLAUDE.md 扩展到多人开发团队"
tags: [workflow, team, claude-md, configuration]
---

# 团队 AI 指令管理

在团队中管理 AI 指令（CLAUDE.md、.cursorrules），避免碎片化。

**模式**：基于配置档案的模块组装（Profile-Based Module Assembly）——共享模块 + 每位开发者的配置档案 + 自动化组装器。

**何时使用**：团队有 5 名以上开发者、使用多种 AI 工具（Claude Code + Cursor/Windsurf）、操作系统不统一。
**何时跳过**：单人开发者、同质化团队（同一工具、同一操作系统）、短期项目（少于 3 个月）。

---

## 问题所在：N x M x P 碎片化

当团队扩张时，AI 指令会迅速碎片化：

| 因素 | 取值 | 示例 |
|--------|--------|---------|
| **N 名开发者** | 5-20 | Alice、Bob、Charlie…… |
| **M 种工具** | 2-4 | Claude Code、Cursor、Windsurf、Copilot |
| **P 种操作系统** | 2-3 | macOS、Linux、WSL |

**变体总数**：N x M x P = 5 x 3 x 2 = **30 种可能的配置**。

如果没有一套体系，会发生什么：

```
Week 1: Team agrees on shared CLAUDE.md
Week 3: Alice adds TypeScript strict rules locally
Week 5: Bob copies Alice's file, removes half the rules
Week 8: New hire Charlie gets Bob's outdated copy
Week 12: 5 developers, 5 different CLAUDE.md files, nobody knows what's canonical
```

**根本原因**：CLAUDE.md 被当作一个单体文件，而不是一份组合而成的配置。

---

## 架构概览

```
profiles/                    modules/
├── alice.yaml               ├── core-standards.md
├── bob.yaml                 ├── git-workflow.md
├── charlie.yaml             ├── typescript-rules.md
│                            ├── test-conventions.md
│                            ├── macos-paths.md
│                            ├── linux-paths.md
│                            ├── cursor-rules.md
│                            └── communication-verbose.md
│
├── skeleton/
│   └── claude-skeleton.md   ← Template with {{MODULE:name}} placeholders
│
└── sync-ai-instructions.ts  ← Reads profile → injects modules → writes output
        │
        ▼
output/
├── alice/CLAUDE.md          ← Generated (read-only)
├── bob/CLAUDE.md
└── charlie/CLAUDE.md
```

**流程**：配置档案（YAML）+ 骨架（模板）+ 模块（片段）→ 组装器 → 生成的 CLAUDE.md

---

## 阶段 1：审计你当前的 CLAUDE.md

**目标**：将每一行归类为通用、条件性或个人化。

```markdown
# Audit template

## Universal (all devs, all tools)
- Architecture: hexagonal
- Tests: must pass before PR
- Naming: kebab-case for files

## Conditional (depends on tool or OS)
- Cursor: use @filename syntax → module: cursor-rules
- macOS paths: /opt/homebrew → module: macos-paths
- Linux paths: /usr/local → module: linux-paths

## Personal (individual preference)
- Style: verbose explanations → profile preference
- Language: French comments → profile preference
```

**用于度量的命令**：
```bash
wc -l CLAUDE.md  # Total lines before modularization
# Tag each line with [U]niversal, [C]onditional, [P]ersonal
# Count by category to estimate module split
```

**典型结果**：60% 通用，25% 条件性，15% 个人化。

---

## 阶段 2：提取模块

**目标**：每个主题分组对应一个 `.md` 文件。

**推荐的结构**：

```
modules/
├── core-standards.md         # Architecture, naming, patterns (all devs)
├── git-workflow.md           # Git conventions (all devs)
├── typescript-rules.md       # TS strict config (if TypeScript)
├── test-conventions.md       # Testing patterns (all devs)
├── macos-paths.md            # macOS-specific paths (if macOS)
├── linux-paths.md            # Linux paths (if Linux)
├── cursor-rules.md           # Cursor-specific rules (if Cursor)
└── communication-verbose.md  # Verbose explanation style (if preferred)
```

**模块格式**（每个模块都是一个独立的 Markdown 片段）：

```markdown
<!-- modules/typescript-rules.md -->
## TypeScript Rules

- Use strict mode: `"strict": true` in tsconfig
- Prefer `type` over `interface` for unions
- No `any` — use `unknown` + type guards
- Zod for runtime validation at boundaries
```

**准则**：
- 保持模块自包含（模块之间不要相互引用）
- 每个模块 15-50 行是最佳区间
- 按领域命名模块，而非按受众命名
- 一个模块 = 一个变更理由

---

## 阶段 3：创建开发者配置档案

**目标**：每位开发者对应一个 YAML，列出其使用的模块。

```yaml
# profiles/alice.yaml
name: "Alice"
os: "macos"
tools:
  - claude-code
  - cursor
communication_style: "concise"
modules:
  core:
    - core-standards
    - git-workflow
    - typescript-rules
    - test-conventions
  conditional:
    - macos-paths          # auto-included when os: macos
    - cursor-rules         # auto-included when cursor in tools
preferences:
  language: "english"
```

**配置档案规则**：
- `core` 模块：为每位开发者都包含（团队标准）
- `conditional` 模块：根据 `os` 和 `tools` 字段决定是否包含
- `preferences`：注入到骨架变量中的个人设置

**新团队成员模板**：参见 [profile-template.yaml](../../examples/team-config/profile-template.yaml)

---

## 阶段 4：编写组装器脚本

**目标**：读取配置档案、注入模块、输出 CLAUDE.md 的脚本。

```typescript
// sync-ai-instructions.ts (simplified ~30 lines)
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { parse } from 'yaml';
import { join } from 'path';

const profile = parse(readFileSync(`profiles/${process.argv[2]}.yaml`, 'utf8'));
let skeleton = readFileSync('skeleton/claude-skeleton.md', 'utf8');

// Collect modules from profile
const modules = [...profile.modules.core, ...profile.modules.conditional];

// Replace each placeholder with module content
for (const mod of modules) {
  const content = readFileSync(`modules/${mod}.md`, 'utf8');
  skeleton = skeleton.replace(`{{MODULE:${mod}}}`, content);
}

// Remove unused placeholders
skeleton = skeleton.replace(/\{\{MODULE:\w+\}\}/g, '');

// Write output
const outDir = `output/${process.argv[2]}`;
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'CLAUDE.md'), skeleton);
console.log(`Generated ${outDir}/CLAUDE.md (${modules.length} modules)`);
```

**运行**：
```bash
npx ts-node sync-ai-instructions.ts alice   # Single dev
npx ts-node sync-ai-instructions.ts --all   # Generate all profiles
npx ts-node sync-ai-instructions.ts --check # Verify no drift
```

完整模板：[sync-script.ts](../../examples/team-config/sync-script.ts)

---

## 阶段 5：CI 漂移检测

**目标**：捕捉输出文件与 profiles/modules 不同步的情况。

```yaml
# .github/workflows/ai-instructions-check.yml
name: AI Instructions Drift Check
on:
  push:
    paths:
      - 'modules/**'
      - 'profiles/**'
      - 'skeleton/**'
  schedule:
    - cron: '0 9 * * 1-5'  # Weekdays at 9am

jobs:
  check-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx ts-node sync-ai-instructions.ts --check
      - name: Fail if drift detected
        run: |
          if git diff --quiet output/; then
            echo "No drift detected"
          else
            echo "::error::AI instructions are out of sync!"
            git diff output/
            exit 1
          fi
```

**它能检测到什么**：
- 某个 module 被编辑过，但 assembler 没有重新运行
- 添加了某个 profile，但不存在对应的输出 CLAUDE.md
- 某位开发者手动编辑了自己生成的 CLAUDE.md

**策略**：生成的文件是只读的。所有改动都要通过 profiles/modules 进行，然后重新运行 assembler。

---

## 阶段 6：新开发者上手

**目标**：新开发者在 5 分钟内拿到自己的 CLAUDE.md。

```bash
# 1. Clone repo
git clone <repo>

# 2. Copy profile template
cp examples/team-config/profile-template.yaml profiles/dave.yaml
# Edit: name, os, tools, modules

# 3. Generate
npx ts-node sync-ai-instructions.ts dave

# 4. Install
cp output/dave/CLAUDE.md .claude/CLAUDE.md
```

**CLAUDE.md 放置位置提醒**：
- 项目全局：`project/CLAUDE.md`（提交到仓库，用于团队约定）
- 个人覆盖：`.claude/CLAUDE.md`（gitignored，用于个人偏好）

---

## 故障排查

| 问题 | 原因 | 修复方法 |
|---------|-------|-----|
| 生成的文件过长 | 包含的 modules 太多 | 检查 profile：移除很少使用的 modules |
| 输出中缺少某个 module | skeleton 中的占位符拼写错误 | 检查 `{{MODULE:name}}` 是否与文件名匹配 |
| CI 漂移告警 | 编辑 module 后未重新生成输出 | 运行 `sync-ai-instructions.ts` 并提交 |
| 开发者 A 有的规则开发者 B 没有 | 符合预期——这正是设计目的 | 确认该开发者的 profile 是否正确 |
| 合并后输出过时 | 合并未触发重新生成 | 合并后运行 assembler（添加 git hook） |

---

## 扩展阈值

| 团队规模 | 做法 |
|-----------|----------|
| 1-2 名开发者 | 共享 CLAUDE.md + 优先级规则（[第 3.4 节](#34-precedence-rules)） |
| 3-5 名开发者，工具相同 | 可选：仅用 modules，不用 profiles |
| 5 名以上开发者或多工具 | 基于 Profile 的模块组装（本工作流） |
| 20 名以上开发者 | 考虑 CLAUDE.md 配置服务器 + 基于 PR 的模块变更 |

---

## 实测结果

来自一个生产团队（5 名开发者、3 种工具、2 种操作系统）：

| 指标 | 之前 | 之后 |
|--------|--------|-------|
| 每个 CLAUDE.md 的行数 | ~380（单体式） | ~185（组装式） |
| Token 缩减 | — | 消耗的上下文减少 59% |
| 抽取出的 modules | 0 | 12 |
| 上手时间 | "复制别人的文件" | 5 分钟（模板 + 生成） |
| 漂移事件 | 每周 | 0（CI 捕获） |

---

## 相关内容

- [第 3.5 节 规模化团队配置](#35-team-configuration-at-scale) —— 概念概览与实测结果
- [第 3.4 节 优先级规则](#34-precedence-rules) —— Claude 如何读取多个 CLAUDE.md 文件
- [profile-template.yaml](../../examples/team-config/profile-template.yaml) —— Profile 模板
- [claude-skeleton.md](../../examples/team-config/claude-skeleton.md) —— Skeleton 模板
- [sync-script.ts](../../examples/team-config/sync-script.ts) —— 完整的 assembler 脚本
