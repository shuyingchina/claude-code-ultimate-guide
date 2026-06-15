---
title: "Skill Design Patterns"
description: "Architectural patterns for designing robust, token-efficient Claude Code skills with multi-agent pipelines"
tags: [skills, architecture, multi-agent, patterns, design]
---

# Skill 设计模式

> **相关阅读**：[开发方法论](./methodologies.md) | [多 Agent 协同](../ultimate-guide.md#920-agent-teams-multi-agent-coordination)

本文提供超越单 Agent、单文件提示词范畴的 skills 实用设计模式。这些模式专门应对若干典型失效场景：sub-agents 反复重新发现相同的事实、规则被应用到错误的文件上、以及把检测和修复混为一谈的 skills。

---

## 共享事实基线注入（Shared Ground Truth Injection）

**问题**：当你启动 N 个并行 sub-agents 来审计或分析一组产物时，每个 agent 都会各自独立地去发现同一批基线事实（文件列表、导航结构、CLI 命令、schema）。这意味着 N 次冗余读取、N 份需要分别信任的事实，以及 N 次某个 agent 可能读到陈旧文件状态的风险。

**模式**：由 orchestrator 一次性计算出共享的事实基线，然后将同一段内容原封不动地注入到每个 sub-agent 的提示词中。

```
Orchestrator (Phase 1)
  ├── Read nav structure → extract groups
  ├── Glob files → get current list
  ├── List CLI commands → get current commands
  └── Compile into "Ground Truth" string

Orchestrator (Phase 2)
  ├── Agent 1 prompt: "## Ground Truth\n{shared block}\n\n## Your Scope\nSection A"
  ├── Agent 2 prompt: "## Ground Truth\n{shared block}\n\n## Your Scope\nSection B"
  └── Agent 3 prompt: "## Ground Truth\n{shared block}\n\n## Your Scope\nSection C"
```

**共享块中应包含的内容**：
- 导航或文件层级结构（让每个 agent 都知道有哪些东西存在）
- 当前的 CLI 命令或 API 端点（以便捕获对已移除命令的引用）
- 领域实体列表（packages、modules、services）
- 当前日期（以便捕获已经过时的版本引用）

**为何有效**：每个 agent 都从同一份快照出发。如果事实基线列表显示某个 CLI 命令并不存在，agent 就无法凭空臆造出它。orchestrator 是结构的唯一可信来源；sub-agents 则是各自所分配章节内容的唯一可信来源。

**Token 取舍**：共享块会给每个 sub-agent 的提示词增加 token。对于一个 5 个 agent 的并行审计，一段 500 token 的事实基线块前期就要花掉 2,500 token。但消除每个 agent 的重复发现所节省的成本远不止于此。把共享块的体量裁剪到真正需要的程度，而不是把所有可能用到的内容都塞进去。

**实现要点**：事实基线块应当是一段字符串，而非一个文件引用。如果你让 agents 去“读取 `docs.json`”，那么每个 agent 都会各自独立地读取它。应在 orchestrator 中一次性编译好，然后直接粘贴进去。

> 见 [Packmind doc-audit skill](https://github.com/packmind/packmind)（.claude/skills/doc-audit/SKILL.md，Phase 1）。参见 [致谢](./credits.md)。

---

## 通过 Frontmatter 路径预筛选引用（Pre-filtered References via Frontmatter Paths）

**问题**：你有一组规则文件（编码规范、安全策略、风格指南）。每个文件只适用于代码库中特定的一部分文件。如果把所有规则都交给审查 agent，agent 就会把规则套用到并非为其编写的文件上，从而产生误报并浪费上下文。

**模式**：在每个规则文件中添加一个 `paths:` frontmatter 字段，使用 glob 模式。在启动审查 agents 之前，orchestrator 先读取该 frontmatter，将 glob 与已修改文件列表进行匹配，然后只把适用的规则传给各个 agent。

```yaml
# .claude/rules/standard-testing-good-practices.md
---
name: Testing Good Practices
paths: "**/*.spec.ts,**/*.test.ts"
alwaysApply: false
description: Testing conventions for TypeScript unit and integration tests
---

## Rules
- Use `describe` blocks for grouping related tests
...
```

Orchestrator 逻辑（明确步骤）：

```
1. Glob .claude/rules/**/*.md → list all rule files
2. For each rule file:
   a. Read YAML frontmatter → extract paths (glob pattern)
   b. If alwaysApply: true → include unconditionally
   c. If alwaysApply: false → match paths against modified files list
   d. Include if at least one modified file matches the glob
3. Pass the filtered rule set to each review agent
```

**核心收益**：
- 测试文件不会被拿去对照后端安全规则检查
- 迁移文件不会被拿去对照前端风格指南检查
- 每个 agent 的上下文只包含与其所审查内容真正相关、可落地的规则

**可扩展性**：在拥有 50 个规则文件的情况下，一个典型的、改动了 8 个 TypeScript spec 文件的 PR 可能只匹配 3 条规则。不做筛选时 agent 要读 50 条规则；做了筛选则只读 3 条。agent 的信噪比也随之成比例提升。

**何时添加 `paths:` frontmatter**：任何具有明确文件类型作用域的规则（测试文件、迁移文件、前端组件、API 路由）。真正全局适用的规则使用 `alwaysApply: true`，并跳过匹配步骤。

> 见 [Packmind qa-review skill](https://github.com/packmind/packmind)（.claude/skills/qa-review/SKILL.md，Phase 5）。参见 [致谢](./credits.md)。

---

## 仅检测的职责边界（Detection-Only Scope Boundary）

**问题**：一个既检测问题又修复问题的 skill 存在两种失效模式：误报（检测并修复了某个其实并不是问题的东西）和修复不彻底（检测正确，但修复有误）。把两者混在一起会让两种问题都更严重，而且让用户失去了一个审查检查点。

**模式**：明确地将 skills 的职责范围限定为仅检测。skill 产出一份报告。修复是一个独立的步骤，由用户在阅读报告之后再触发。

在 skill 的开头就声明这一点：

```markdown
**This skill only detects issues. It does not fix them.**
```

然后严格执行：skill 内部不做任何文件写入、不做编辑、不做 git commit。输出永远是一份 markdown 报告或控制台输出的结论。

**何时打破这条规则**：那些专门为自动化修复而设计的 skills（codemod 风格的 skills、依赖更新 skills）是例外。它们应当明确声明自己会写入改动，并且应当包含一个 dry-run 模式。

**实际价值**：仅检测的 skills 可以安全地在 main 分支上、在 CI 中、以及针对生产环境配置运行。用户可以放心地调用它，而无需担心意外改动，这也使它们更值得被频繁运行、并在更多代码库上运行。

> 这一模式在 [Packmind 仓库](https://github.com/packmind/packmind)（Apache 2.0）的 qa-review、playbook-audit 和 doc-audit 中反复出现。参见 [致谢](./credits.md)。

---

## 输入处理器分发（Input-Handler Dispatch）

**问题**：一个需要处理两种或更多异构输入类型（图像 vs 文本、GitHub issues vs 设计稿）的 skill，要么会让主文件长出复杂的分支逻辑，要么会因为太僵化而无法应对多样的入口。

**模式**：在 `inputs/` 子目录中为每种输入类型存放一个输入处理器文件。主 SKILL.md 先询问用户属于哪种类型，然后加载对应的处理器文件。

```
.claude/skills/my-skill/
├── SKILL.md                 # Orchestrator: asks user, dispatches to input handler
└── inputs/
    ├── github-issue.md      # Handler for GitHub issue input
    └── visual-mockup.md     # Handler for screenshot/image input
```

SKILL.md（节选）：

```markdown
## Step 1: Identify Input Type

Ask the user: "Are you providing a GitHub issue or a visual mockup?"

- If GitHub issue → follow the instructions in `inputs/github-issue.md`
- If visual mockup → follow the instructions in `inputs/visual-mockup.md`
```

每个处理器文件都包含针对该输入类型的完整解析说明，包括字段提取、格式归一化和校验。主文件则保持简洁。

**何时使用**：当不同输入类型需要差异巨大的解析逻辑时（而不仅仅是字段名不同）。如果两种输入的差异少于 5 个步骤，就直接内联处理。当各个处理器都会超过 100 行时，这一模式才划算。

> 见 [Packmind create-em-spec skill](https://github.com/packmind/packmind)（.claude/skills/create-em-spec/inputs/）。参见 [致谢](./credits.md)。

---

## 用版本化子目录应对工具版本耦合（Versioned Sub-directories for Tool-Version Coupling）

**问题**：一个 skill 封装了某个 CLI 工具，而该工具在不同版本之间会改变行为。skill 需要检测用户所使用的版本，并据此调整自己的指令。

**模式**：为每个工具版本存放一个子目录，每个目录中包含该版本专属的指令：

```
.claude/skills/update-playbook/
├── SKILL.md                         # Detects CLI version, dispatches
└── tool-versions/
    ├── v1.21/
    │   └── apply-changes.md         # Instructions for v1.21
    ├── v1.23/
    │   └── apply-changes.md         # Instructions for v1.23 (different API)
    └── v1.24/
        └── apply-changes.md         # Instructions for v1.24 (breaking change)
```

SKILL.md 在运行时检测版本：

```markdown
## Step 1: Detect Tool Version

Run: `my-cli --version`

- If output starts with "1.21" → read `tool-versions/v1.21/apply-changes.md`
- If output starts with "1.23" → read `tool-versions/v1.23/apply-changes.md`
- If output starts with "1.24" → read `tool-versions/v1.24/apply-changes.md`
- If version not recognized → stop and tell the user which versions are supported
```

**应避免的反模式**：不要在原有的 `my-skill/` 旁边再创建一个 `my-skill-v2/` 目录。应当对 skill *内部的内容*做版本化，而不是对 skill 本身做版本化。两个几乎相同的 skills 更难维护，调用时也容易混淆。

**何时使用**：当你所封装的 CLI 工具在不同版本之间存在破坏性变更，且你需要同时支持多个版本时。如果你只需要支持最新版本，就直接原地更新 skill 即可。

> 见 [Packmind update-playbook skill](https://github.com/packmind/packmind)（.claude/skills/packmind-update-playbook/）。参见 [致谢](./credits.md)。

---

## 双层规范（Two-Tier Standards）

**问题**：一份全面的编码规范篇幅很长（1,000–5,000 词）。在每次文件审查时都把完整规范加载进上下文，会推高 token 成本并稀释注意力。

**模式**：在 `.claude/rules/` 中存放一份简短摘要（100–300 词，带 `paths:` frontmatter glob）。把完整的权威规范放在另一个 Claude 可按需读取的位置。

```
.claude/rules/standard-testing.md          # Summary + paths glob (200 words)
.standards/standard-testing-full.md        # Full canonical standard (2,000 words)
```

`.claude/rules/` 中的摘要包含：
- 3–5 条祈使式规则（命令式语气：“Use X”“Do not Y”）
- `paths:` frontmatter，使其只在匹配的文件上加载
- 一个指向完整规范的链接，供需要细节的场景使用

完整的权威规范放在 `.claude/rules/` 之外，因此不会被自动加载。

**何时使用**：当团队拥有超过 10 个规则文件，或规则文件平均超过 500 词时。对于规模更小的配置，单层方案更简单。

**维护**：当你更新权威规范时，也要同步更新摘要。双层拆分带来了重复的风险。缓解办法是让摘要只保留要点式规则（不写大段散文），这样它就不需要经常改动。

> 见 [Packmind 规则配置](https://github.com/packmind/packmind)（.claude/rules/packmind/）。参见 [致谢](./credits.md)。

---

## 将计划与规格作为已提交的产物

**问题**：会话范围内的计划（`/plan` 模式、草稿文件）会在会话结束时消失。下一个会话没有任何可搜索的记录，无从得知某个设计决策为何作出、考虑过哪些方案，或上次完成到了哪一个实现步骤。

**模式**：将计划及其关联的设计规格直接以带日期的 markdown 配对文件形式提交到 `.claude/` 中：

```
.claude/
├── plans/
│   └── 2026-03-15-auth-refactor.md        # High-level plan: phases, tasks, commit messages
└── specs/
    └── 2026-03-15-auth-refactor-design.md  # Companion spec: context, alternatives, rationale
```

计划文件包含实现拆解，并为每个任务标注明确的 commit message：

```markdown
# Auth Refactor Plan

## Task 1: Extract token validation middleware
- Move validation logic from controller into `middleware/auth.ts`
- git commit -m "refactor(auth): extract token validation into middleware"

## Task 2: Add refresh token rotation
- Implement rotation logic with 7-day expiry
- git commit -m "feat(auth): add refresh token rotation with 7-day expiry"
```

规格文件记录的是促成该计划的依据：约束条件、被否决的备选方案，以及六个月后从代码中无法显而易见看出的推理过程：

```markdown
# Auth Refactor Design

## Context
Session token storage flagged by legal review (ISO 27001 compliance gap).
Rotation required per new internal security policy v2.3.

## Rejected approaches
- HttpOnly cookie approach: requires cross-domain config changes (deferred)
- Redis session store: ops team not ready to manage another stateful service
```

两个文件一起提交，并无限期保留在仓库中。

**为何优于仅限会话的计划**：已提交的计划可被 grep 检索、可 diff 比对、可恢复续接。新会话可以读取 `.claude/plans/` 来理解进行中的工作，无需从 git log 重新拼凑。规格记录了那些会从记忆中消失、但在六个月后重新审视某个决策时却至关重要的推理。

**命名约定**：计划用 `YYYY-MM-DD-<slug>.md`，配套规格用 `YYYY-MM-DD-<slug>-design.md`，两者使用相同的日期和 slug。这能让配对文件在目录列表中视觉上保持关联。

**何时使用**：跨多个会话、且连续性很重要的实现任务。对于一次会话即可完成、单次提交即可装下的任务，这套开销并不值得。门槛大致是：如果工作跨越超过一天，或超过一个 Claude 会话，就提交计划。

> 见于 [Packmind .claude/plans/](https://github.com/packmind/packmind) 约定（Apache 2.0）。参见 [Credits](./credits.md)。

---

## 运行时 Prompt 日志记录

**问题**：当一次 AI 服务商调用超时或崩溃时，发送出去的确切 prompt 就丢失了。如果你正在构建一个有多个 agents 并行运行的 skill 或评估流水线，你就失去了诊断每个 agent 被告知了什么的能力。`--debug` 标志只在你记得加上它时才有用。

**模式**：在调用服务商之前，以阻塞操作的方式把 prompt 写入磁盘。使用一个持久目录，文件名带时间戳。日志记录调用绝不能抛出异常。

```typescript
// Run BEFORE provider.invoke(), not after
await writeFile(
  `prompts/debug/${evaluatorName}-${timestamp}.md`,
  fullPrompt,
  "utf-8",
);
// Only now call the provider
const response = await provider.invoke(fullPrompt);
```

有三条约束让这个模式行之有效：

1. **阻塞式写入**（`await`，而非发了不管）：在服务商调用开始之前，文件已存在于磁盘上。服务商调用期间发生崩溃时，prompt 仍完好可供检查。
2. **始终开启**（不由 debug 标志门控）：开销只是每个 agent 一次文件写入。好处是任何意外结果都有一份永久记录。
3. **绝不抛出异常**：日志记录失败不得破坏评估。用 try/catch 包裹写入，失败时记录一条警告并继续。

**目录约定**：使用相对于项目根目录的路径（`prompts/debug/` 或 `claudedocs/debug/`），而非临时目录。临时目录会被清理；而你希望这些文件跨多次运行持续保留。

**Token 成本**：零（磁盘 I/O 发生在 AI 调用之外）。prompt 已经在内存中，你只是把它持久化。

**何时使用**：任何调用 AI 服务商、且 prompt 是动态拼装而成（不仅仅是静态字符串）的 skill。其价值与 prompt 的复杂度成正比：如果你的 prompt 注入了 ground truth、评估器指令和文件内容，那么在调用前写一次就是廉价的保险。

> 见于 [PackmindHub/context-evaluator](https://github.com/PackmindHub/context-evaluator)（`src/shared/evaluation/runtime-prompt-logger.ts`，MIT）。参见 [Credits](./credits.md)。

---

## 自适应统一/并行模式

**问题**：你有 N 个文件要评估，需要作出决定：把所有文件发给一个 agent（更利于发现跨文件问题，但 context 成本更高），还是把每个文件发给各自独立的并行 agent（更便宜、更快，但看不到文件之间的矛盾）？

**模式**：在确定策略之前，先估算合并后的 token 数量。如果总量落在某个门槛之内，使用统一模式（一个 agent 看到全部内容）。如果超过门槛，则退回到每个文件一个独立并行 agent。

```typescript
const DEFAULT_MAX_UNIFIED_TOKENS = 100_000;

function canUseUnifiedMode(context: MultiFileContext, maxTokens = DEFAULT_MAX_UNIFIED_TOKENS) {
  if (context.totalTokenEstimate > maxTokens) {
    return {
      viable: false,
      reason: `Combined content (~${context.totalTokenEstimate} tokens) exceeds limit (${maxTokens})`,
    };
  }
  return { viable: true };
}
```

在构建 agent prompts 之前调用它。该决策为流水线的其余部分把关：

```
estimateTokens(all files)
  ↓
< 100K → runUnifiedEvaluation(allFiles)   // 1 agent, cross-file detection
> 100K → runAllEvaluators(file)           // N agents, per-file, parallel
```

**为何门槛很重要**：在统一模式下，agent 能看到根目录 `CLAUDE.md` 与子目录 `CLAUDE.md` 之间的矛盾。在并行模式下，每个 agent 只看到一个文件，无法检测出这些矛盾。该门槛为较小的仓库保留了跨文件的智能，同时让较大的仓库保持在实际可行的 context 限制之内。

**门槛校准**：100K tokens 为评估器 prompt（通常 2-5K）和模型的响应缓冲区留出了空间。针对你自己的用例，把门槛设为 `model_context_window - evaluator_prompt_tokens - response_buffer`。Pac 的 `DEFAULT_MAX_UNIFIED_TOKENS = 100_000` 对当前大多数模型而言是一个保守的默认值。

**Token 估算**：你不需要精确计数。一个粗略估算（对大多数英文文本用 `chars / 4`）足以作出模式决策。偶尔在估算上误差 10% 的代价，远低于追求那份额外精度的代价。

> 见于 [PackmindHub/context-evaluator](https://github.com/PackmindHub/context-evaluator)（`src/shared/evaluation/runner.ts` 中的 `canUseUnifiedMode()`，MIT）。参见 [Credits](./credits.md)。

---

## 另请参阅

- [开发方法论](./methodologies.md)：TDD、SDD、BDD、多 agent 编排
- [§9.20 Agent Teams](../ultimate-guide.md#920-agent-teams-multi-agent-coordination)：包含 Skeptical Reviewer Pattern 的 Agent Teams
- [Credits](./credits.md)：外部来源的完整署名
- `examples/skills/mcp-integration-reference/`：MCP Reference File Pattern 模板
