---
title: "Design-to-Code Workflow with Figma MCP"
description: "Automated design system implementation using Figma MCP Server for 1:1 design-code parity"
tags: [workflow, mcp, integration]
---

# 借助 Figma MCP 的设计到代码工作流

> **可信度**：Tier 2 —— 基于已记录的生产案例研究（Parallel HQ、builder.io）、MCP server 规格说明以及社区工作流。

使用 Figma MCP Server 实现自动化的设计系统落地，使产品设计师能够将可用于生产的规格说明移交给 Claude Code，由其实现组件并保持设计与代码 1:1 的一致性。

---

## 目录

1. [TL;DR](#tldr)
2. [已记录的成效](#documented-impact)
3. [架构概览](#architecture-overview)
4. [三层 Token 层级](#3-tier-token-hierarchy)
5. [前置条件](#prerequisites)
6. [核心工作流](#core-workflows)
7. [Code Connect 配置](#code-connect-setup)
8. [示例 Prompt](#example-prompts)
9. [团队采用模式](#team-adoption-patterns)
10. [反模式](#anti-patterns)
11. [实施路线图](#implementation-roadmap)
12. [资源](#resources)

---

## TL;DR

```
Designer (Figma Make) → Export (Figma Design) → Claude (Figma MCP) → Production Code

Key insight: Design system = source of truth
Claude consumes tokens/components directly from Figma
Implementation maintains design parity automatically
```

---

## 已记录的成效

基于 2026 年 1 月的生产案例研究：

| 指标 | 改善幅度 | 来源 |
|--------|-------------|--------|
| 设计不一致 | 减少 62% | Parallel HQ 研究 |
| 工作流效率 | 提升 78% | builder.io 案例研究 |
| 节省的工程时间 | 75 天（6 个月内） | Parallel HQ 生产数据 |
| 上市时间 | 缩短 56% | 多组织综合数据 |
| 设计技术债务 | 减少 82% | 实施后审计 |

**典型工作流耗时**：
- 单个 frame → 生产组件：2-3 分钟
- 设计系统漂移审计：3 周 → 3 分钟
- Token 更新传播：手动数小时 → 自动数秒

*来源：builder.io/blog/claude-code-figma-mcp-server、parallelhq.com/blog/automating-design-systems-with-ai、composio.dev/blog/how-to-use-figma-mcp-with-claude-code*

---

## 架构概览

### 完整技术栈

```
[Figma Design File]
    ↓ (Variables & Styles)
[Tokens Studio Plugin] (optional but recommended)
    ↓ (JSON export)
[GitHub Repository]
    ↓ (CI/CD)
[Style Dictionary]
    ↓ (Transform)
[CSS Custom Properties / Tailwind Config]
    ↓ (Consumed by)
[Component Library]
    ↑ (Reads via)
[Claude Code + Figma MCP]
```

### MCP 集成点

Claude Code 通过 Figma MCP Server 访问 Figma：

```
Claude Code
    ↓ (uses)
Figma MCP Server (mcp-server-figma)
    ↓ (authenticates via)
Figma Personal Access Token
    ↓ (reads)
Figma File (Dev Mode data)
```

**Claude 可以访问的内容**：
- 文件结构和 frames
- 颜色／文本／效果样式
- 组件属性
- Variables（tokens）
- Dev Mode 注释
- Code Connect 代码片段（如已配置）

**Claude 无法访问的内容**：
- 没有 token 权限的私有文件
- 编辑能力（只读）
- 实时协作数据
- 版本历史（仅当前状态）

---

## 三层 Token 层级

现代设计系统使用分层的 token 结构。Claude Code 在消费 Figma 数据时能够理解这一层级。

| 层级 | 定义 | Figma 实现 | 代码输出 |
|------|------------|----------------------|-------------|
| **Base** | 原始基础值 | Figma Variables（例如 `blue-600: #0066CC`、`spacing-2: 8px`） | CSS custom properties（`--blue-600`、`--spacing-2`） |
| **Composite** | 组合后的基础值 | 引用 variables 的组件填充 | Tailwind config 或 CSS classes |
| **Semantic** | 上下文语义 | 上下文 variable 别名（例如 `color-interactive-primary` → `blue-600`） | 组件 props 或 theme tokens |

### 层级示例

```
Base:
  --color-blue-600: #0066CC
  --spacing-2: 8px
  --radius-md: 4px

Composite:
  --button-padding: var(--spacing-2) var(--spacing-4)
  --button-border-radius: var(--radius-md)

Semantic:
  --interactive-primary: var(--color-blue-600)
  --interactive-primary-hover: var(--color-blue-700)
```

**Claude Code 的行为**：给定一个 Figma 组件时，Claude 会：
1. 提取被引用的 variables（base 层）
2. 识别 composite 模式（间距、尺寸）
3. 按照你的 token 约定应用语义化命名
4. 生成与该层级匹配的代码

---

## 前置条件

### 面向设计师

| 要求 | 详情 |
|-------------|---------|
| **Figma 许可证** | Dev Mode 席位（启用 variable 检视、code snippets） |
| **有组织的 Variables** | 使用 Figma Variables 或 Tokens Studio plugin 进行 token 管理 |
| **组件结构** | Auto Layout、命名图层、一致的命名约定 |
| **Frame 命名** | 描述性的 frame 名称（Claude 用它们作为组件名） |

### 面向开发者

| 要求 | 详情 |
|-------------|---------|
| **Claude Code** | 版本 1.5.0+（支持 MCP） |
| **Figma MCP Server** | `npm install -g @modelcontextprotocol/server-figma` |
| **Personal Access Token** | 从 Figma 账户设置 → Tokens 生成 |
| **MCP 配置** | 在 Claude Code 设置中配置 token |

### MCP 配置

添加到你的 Claude Code MCP 设置（`.claude/mcp.json` 或设置界面）：

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-figma"],
      "env": {
        "FIGMA_PERSONAL_ACCESS_TOKEN": "your-token-here"
      }
    }
  }
}
```

**安全提示**：生产环境请使用环境变量：
```json
{
  "env": {
    "FIGMA_PERSONAL_ACCESS_TOKEN": "${FIGMA_TOKEN}"
  }
}
```

然后在你的 shell 中导出：`export FIGMA_TOKEN="figd_..."`

---

## 核心工作流

### 工作流 A：单个 Frame → 生产组件

**耗时**：每个组件 2-3 分钟

**步骤**：

1. **设计师**：在 Figma 中使用恰当的 variables／styles 创建组件
2. **设计师**：将 Figma 文件 URL 分享给开发者／Claude
3. **开发者**：向 Claude Code 发出 prompt：

```
Read the "Button/Primary" component from Figma file:
https://www.figma.com/design/FILE_KEY

Implement as a React component with TypeScript.
Use Tailwind for styling, mapping Figma variables to our design tokens.
Ensure responsive behavior matches Figma's Auto Layout constraints.
```

4. **Claude**：
   - 通过 Figma MCP 获取组件
   - 提取样式、尺寸、间距
   - 将 variables 映射到代码 tokens
   - 生成 props 与 Figma variants 匹配的组件

5. **验证**：`npm run dev` → 与 Figma 进行视觉对比

**示例输出**：
```tsx
// components/Button/Primary.tsx
interface ButtonProps {
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  children: React.ReactNode;
}

export function PrimaryButton({ size = 'md', disabled, children }: ButtonProps) {
  return (
    <button
      className={cn(
        'rounded-md font-medium transition-colors',
        'bg-interactive-primary text-white',
        'hover:bg-interactive-primary-hover',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        {
          'px-3 py-1.5 text-sm': size === 'sm',
          'px-4 py-2 text-base': size === 'md',
          'px-6 py-3 text-lg': size === 'lg',
        }
      )}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
```

---

### 工作流 B：设计系统漂移审计

**耗时**：手动审查 3 周 → 自动化 3 分钟

**问题**：随着时间推移，代码会偏离设计系统（魔法数字、硬编码颜色、不一致的间距）。

**解决方案**：Claude 以 Figma 作为事实来源对代码库进行审计。

**Prompt**：
```
Audit src/components for design system compliance.
Compare against our Figma design system:
https://www.figma.com/design/FILE_KEY

Report:
1. Hardcoded colors not using design tokens
2. Magic number spacing values
3. Components not matching Figma structure
4. Missing responsive patterns

Then propose fixes with token replacements.
```

**Claude 输出**：
```markdown

## 设计系统审计结果

### 发现的问题（共 23 个）

#### 硬编码颜色（8 处）
- `src/components/Card.tsx:45` → `#0066CC` 应改为 `var(--interactive-primary)`
- `src/components/Header.tsx:12` → `#F3F4F6` 应改为 `var(--surface-secondary)`
...

#### 魔法数字（11 处）
- `src/components/Modal.tsx:23` → `padding: 16px 24px` 应改为 `var(--spacing-4) var(--spacing-6)`
...

#### 结构不匹配（4 处）
- `src/components/Button.tsx` → 缺少 Figma 中存在的 `icon-left` 变体
...
```

---

### 工作流 C：Token 自动化流水线

**目标**：Figma 变量的变更自动传播到代码中。

**架构**：

```
Figma Variables
    ↓ (Tokens Studio export or Figma API)
GitHub Repository (tokens.json)
    ↓ (GitHub Actions CI/CD)
Style Dictionary Transform
    ↓ (generates)
CSS / Tailwind / Platform-specific tokens
    ↓ (commit & deploy)
Production
```

**配置**（一次性）：

1. **Tokens Studio Plugin**：连接到 GitHub 仓库
2. **Style Dictionary Config**：定义转换规则
3. **GitHub Actions**：在 token 更新时自动运行
4. **Claude Role**：审查并验证生成的 token

**开发者 Prompt**（在 CI 运行之后）：
```
Review the token update from commit abc1234.
Check if any components need updates to consume new tokens.
Generate migration guide if breaking changes exist.
```

**Claude 输出**：
```markdown
## Token Update Review (v2.3.0 → v2.4.0)

### Changes
- Added: `--spacing-7`, `--spacing-8` (requested by design)
- Changed: `--interactive-secondary` hue shift 5° (brand refresh)
- Deprecated: `--legacy-blue` (remove by Q3)

### Impact Analysis
- 12 components reference `--interactive-secondary` → Auto-updated via token reference
- 3 components use deprecated `--legacy-blue` → Migration needed

### Migration Required
1. `src/components/LegacyButton.tsx:34` → Replace `--legacy-blue` with `--interactive-primary`
2. `src/components/OldCard.tsx:67` → Replace with new token
3. `src/utils/theme.ts:12` → Update theme export

### Migration Script
[Claude generates codemod or find/replace script]
```

---

### 工作流 D：视觉迭代循环（Figma + Playwright）

**目标**：针对 Figma 设计进行自动化视觉回归测试。

**MCP 技术栈**：Figma MCP + Playwright MCP

**配置**：
```
Claude Code accesses:
- Figma (design source of truth)
- Playwright (automated browser testing)
```

**Prompt**：
```
Take a screenshot of our Button component in all variants.
Compare against Figma frames from:
https://www.figma.com/design/FILE_KEY → "Button Tests" page

Report any visual differences (color, spacing, typography).
```

**工作流**：
1. Claude 读取 Figma 框架（期望状态）
2. Claude 使用 Playwright 对实时组件进行截图（实际状态）
3. Claude 进行对比（像素差异或视觉检查）
4. 报告差异并附上修复建议

**示例输出**：
```markdown
## Visual Regression Report

### ✅ Matching (5/7)
- Button/Primary/Default
- Button/Primary/Hover
- Button/Secondary/Default
...

### ❌ Mismatches (2/7)

#### Button/Primary/Disabled
- **Issue**: Text opacity 0.4 in code, 0.5 in Figma
- **Fix**: Update `disabled:opacity-50` → `disabled:opacity-40`
- **File**: `src/components/Button.tsx:23`

#### Button/Large
- **Issue**: Padding 12px in code, 16px in Figma
- **Fix**: Update `py-3` → `py-4` (16px)
- **File**: `src/components/Button.tsx:18`
```

---

## Code Connect 配置

**Code Connect** 是 Figma 的无代码工具，用于将设计组件链接到代码片段。这增强了 Claude 生成正确代码的能力。

### 它的作用

- 设计师用代码示例为 Figma 组件添加注解
- Claude 通过 MCP 读取这些注解
- 生成的代码自动符合团队约定

### 配置（面向设计师）

1. 在 Figma Dev Mode 中 → 选择组件 → Code Connect 面板
2. 添加展示组件用法的代码片段：

```tsx
// Example Code Connect annotation in Figma
<Button variant="primary" size="lg">
  Click me
</Button>
```

3. 当被要求实现时，Claude 会看到这段代码，并使用团队的确切模式

### 优势

| 没有 Code Connect | 有 Code Connect |
|---------------------|-------------------|
| Claude 生成通用代码 | Claude 使用团队约定 |
| Prop 命名不一致 | Prop 与 Figma 变体完全匹配 |
| 需要手动修正 | 首次生成即可用于生产 |

**参考**：在 parallelhq.com/blog 上了解更多（Code Connect UI 文章）

---

## 替代方案：Pencil（IDE 原生画布）

**概述**：[Pencil](https://pencil.dev) 将无限设计画布直接带入 Claude Code/Cursor/VSCode，消除了外部工具切换，并支持设计即代码（design-as-code）的工作流。

### 架构

**核心创新**：与 Figma（基于云）或 Excalidraw（独立工具）不同，Pencil 将设计画布直接嵌入到 Claude 和代码所在的 IDE 中。

```
Traditional Workflow:
Figma (design) → Export → Claude Code → Implementation → Manual sync

Pencil Workflow:
IDE Canvas (design + AI agents + code) → Git commit → Continuous alignment
```

**核心特性**：
- **WebGL Canvas**：无限、高性能、完全可编辑
- **AI Multiplayer Agents**：多个并行 agent 协作处理设计
- **Git-Native**：`.pen` 文件（JSON 格式）与代码一同纳入版本控制
- **MCP 双向**：完整的读+写访问（不像 Figma MCP 那样只读）
- **Figma 导入**：直接从 Figma 复制粘贴，保留矢量图形和样式

### Pencil 与 Figma MCP 对比

| 方面 | Pencil | Figma MCP |
|--------|--------|-----------|
| **位置** | IDE 原生（Cursor/VSCode/Claude Code） | 外部云端 |
| **格式** | `.pen` JSON（开放） | 专有二进制 |
| **版本控制** | Git 原生（分支/合并/历史） | Figma 云端版本 |
| **AI Agents** | 多人并行 | 通过 MCP 的单线程 |
| **协作** | 代码优先（开发者 + 设计师） | 设计优先（设计师 + 开发者） |
| **MCP 访问** | 双向（读+写） | 只读 |
| **工作流** | 在同一环境中 设计 → 提交 → 编码 | 设计 → 导出 → 交接 → 编码 |
| **最适合** | 工程师型设计师、以代码为中心的团队 | 传统的设计-开发分离模式 |
| **成熟度** | 新兴（2026 年 1 月发布） | 成熟（2024 年起） |
| **定价** | 当前免费，未来待定 | 免费增值（提供免费层级） |

### 何时使用 Pencil

✅ **适合**：
- 团队以 Cursor 或 VSCode + Claude Code 作为主要环境
- 工程师型设计师对终端/IDE 工作流得心应手
- 需要设计与代码紧密对齐的项目（设计即代码范式）
- 希望实现 Git 原生的设计版本控制（分支保护、回滚等）
- 想利用并行 AI agent 进行设计自动化

⚠️ **需谨慎考虑**：
- 传统设计团队（非技术型）→ Figma 可能更合适
- 需要企业级 SLA/支持 → Pencil 仍在成熟中
- 拥有 50+ 组件的复杂设计系统 → Figma 生态更成熟
- 团队不使用 Cursor/VSCode → 兼容性有限

### 配置

1. **安装 Pencil 扩展**：
   - 访问 [pencil.dev](https://pencil.dev)
   - 按照说明为 Cursor/VSCode/Claude Code 安装
   - 创建账户（当前免费）

2. **创建第一个画布**：
   ```bash
   # Open IDE, launch Pencil extension
   # Create new .pen file in your repo
   # Design on infinite canvas
   ```

3. **Git 工作流**：
   ```bash
   git add design/homepage.pen
   git commit -m "feat(design): add homepage hero section"
   git push
   ```

4. **Claude 集成**：
   - Claude 可通过 MCP 读取 .pen 文件
   - Prompt: "Implement the Button component from design/components.pen"
   - Claude 提取设计规格并生成代码

### 示例 Prompt

```
Read the "Hero Section" from design/homepage.pen.

Implement as React component with:
- Responsive behavior matching canvas breakpoints
- Animations from design (fade-in, slide-up)
- Copy exactly as specified in canvas
- Use Tailwind for styling

Ensure pixel-perfect match with design specs.
```

### 创始人与背书

**Tom Krcha**（Pencil CEO）：
- Adobe XD 联合创始人（2014-2018），在 Adobe 工作 10 年
- 此前的退出案例：Alter Avatars（被 Google 收购）、Around（被 Miro 收购）
- 14+ 年开发经验

**融资**：a16z Speedrun（约 100 万美元）+ KAYA VC

**进展**：发布时获得 100 万+ 浏览量，数千次注册，包括 Microsoft、Shopify、Uber 的高管。

### 成熟度说明

**⚠️ 状态**：2026 年 1 月发布（非常新）。早期信号强劲，但文档和生态系统仍在成熟中。

**建议**：
- **生产项目**：先用 1-2 个非关键功能进行试点
- **新项目**：对于使用 Cursor/Claude Code 的团队可安全采用
- **传统工作流**：在 Pencil 成熟之前（3-6 个月）继续使用 Figma MCP

**关注**：定价公告、公开的 GitHub 仓库、预计 2026 年 Q2 推出的成熟文档。

---

## 示例提示词

### 组件实现
```
Implement the "Card/Product" component from our Figma design system:
[Figma URL]

Requirements:
- Use our existing design tokens from tailwind.config.ts
- Include hover states matching Figma interactions
- Implement all variants (default, featured, compact)
- Add TypeScript types for all props
```

### 设计系统扩展
```
Our design team added a new "Badge" component to Figma:
[Figma URL → Badge frame]

Generate:
1. React component with all variants
2. Storybook stories
3. Unit tests for prop combinations
4. Update design system docs
```

### Token 校验
```
Compare the color tokens in our Tailwind config against
Figma variables from: [Figma URL]

Report any mismatches and generate update script.
```

### 响应式实现
```
Implement the "Hero" section from Figma with exact responsive behavior:
[Figma URL → Hero/Responsive frame]

Figma has 3 breakpoints configured. Match these precisely.
```

### 无障碍审计
```
Review the "Modal" component implementation against Figma specs:
[Figma URL]

Check:
- Focus management matches Figma's interaction flow
- Color contrast meets WCAG AA (Figma has contrast checker)
- Keyboard navigation (Figma annotations specify tab order)
```

### 交付前的设计 QA
```
Review the "Checkout Flow" frames for implementation readiness:
[Figma URL → Checkout Flow page]

Check:
- All interactive states defined (hover, focus, disabled, error)
- Variables used consistently (no magic values)
- Auto Layout constraints are implementable
- Missing anything needed for production code?
```

### 多组件原子化实现
```
Implement the atomic design system components in order:

1. Atoms: [Figma URL → Atoms page]
   - Button, Input, Label, Badge

2. Molecules: [Figma URL → Molecules page]
   - FormField (Label + Input + Error)
   - SearchBar (Input + Button)

3. Organisms: [Figma URL → Organisms page]
   - LoginForm (using molecules)

Ensure each level only imports from lower levels.
```

---

## 团队采用模式

### 面向产品设计师

**新工作流**：
1. 在 Figma 中使用合理的变量结构进行设计
2. 使用 Figma Make 进行快速原型设计
3. 启用 Dev Mode 后导出到 Figma Design
4. 与开发团队共享文件 URL + 特定 frame
5. Claude 消费设计 → 生成实现
6. 设计师以可视化方式审查代码输出（而非阅读代码）

**关键洞察**：设计师无需学习代码。他们通过与 Figma 的可视化对比来审查实现。

### 面向开发者

**新工作流**：
1. 从设计师处接收 Figma URL
2. 提示 Claude 从 Figma 源进行实现
3. 审查生成的代码是否契合架构
4. 运行可视化对比（Playwright 或手动）
5. 提交可用于生产的组件

**节省的时间**：跳过手动的像素级精确实现。专注于逻辑，而非布局匹配。

### 面向产品经理

**新能力**：基于 Figma frame 请求设计实现的工作量评估。

**面向 PM 的提示词**：
```
Review the "Dashboard Redesign" Figma file:
[Figma URL]

Estimate implementation complexity:
- How many new components needed?
- Which existing components can be reused?
- Any technical blockers?

Provide rough timeline for dev implementation.
```

Claude 输出：
```markdown
## Implementation Analysis

### Scope
- 12 frames total
- 4 new components (DataTable, MetricCard, FilterPanel, DateRangePicker)
- 8 existing components reused

### Complexity Assessment
- **Low**: MetricCard (similar to existing Card, 1-2h)
- **Medium**: FilterPanel (multi-select logic, 4-6h)
- **High**: DataTable (sorting, pagination, virtualization, 2-3 days)
- **High**: DateRangePicker (third-party library integration, 1-2 days)

### Technical Considerations
- DataTable needs backend API for server-side pagination
- DateRangePicker: evaluate date-fns vs dayjs vs native
- FilterPanel state management (local vs global)

### Estimated Timeline
- Development: 5-7 days
- Code review + QA: 2 days
- Total: 1.5-2 weeks
```

---

## 反模式

| ❌ 反模式 | 为何失败 | ✅ 正确做法 |
|----------------|-------------|-------------------|
| **手动转录设计** | 易出错、耗时，偏移不可避免 | 让 Claude 通过 MCP 直接读取 Figma |
| **以截图作为规格** | 没有 token 数据、没有交互性、含糊不清 | 共享 Figma URL，让 Claude 访问结构化数据 |
| **硬编码值** | 设计系统更新时会失效 | 使用来自 Figma 变量的 design tokens |
| **设计师写代码** | 浪费设计师技能 | 设计师设计 → Claude 写代码 → 开发审查 |
| **开发者猜间距** | 与设计系统不一致 | Claude 从 Figma 提取精确值 |
| **没有 Code Connect 标注** | 输出通用代码 | 标注一次 → Claude 使用团队约定 |
| **跳过可视化对比** | 实现偏移 | 始终与 Figma 源进行核验 |
| **Token 命名不匹配** | Figma 变量 ≠ 代码 token | 建立命名约定，使用 Style Dictionary |
| **缺少响应式规格** | 开发者猜测断点 | Figma 有响应式 frame → Claude 读取精确规格 |
| **单层 token** | 不灵活，难以做主题化 | 使用三层层级（base/composite/semantic） |

---

## 实施路线图

### 第一阶段：基础（第 1-2 周）

**目标**：建立基础的 Figma → Claude → 代码流水线

- [ ] 安装 Figma MCP Server
- [ ] 配置个人访问令牌
- [ ] 测试连接：Claude 读取公开的 Figma 文件
- [ ] 创建包含设计系统约定的项目 CLAUDE.md
- [ ] 实现 3-5 个简单组件（Button、Input、Badge）
- [ ] 建立可视化 QA 流程（手动对比）

**成功标准**：
- Claude 从 Figma URL 生成组件
- 输出在视觉上与设计一致
- 开发团队理解该工作流

---

### 第二阶段：扩展（第 3-4 周）

**目标**：完整的设计系统实现 + 自动化

- [ ] 从 Figma 库实现 20+ 个组件
- [ ] 搭建 token 自动化（Tokens Studio + Style Dictionary）
- [ ] 创建组件测试套件（Storybook + 视觉回归）
- [ ] 培训设计师做好变量卫生
- [ ] 在 CLAUDE.md 中记录团队约定
- [ ] 运行首次设计系统偏移审计

**成功标准**：
- 80%+ 的 UI 组件自动生成
- token 更新自动传播
- 设计师对交付流程有信心

---

### 第三阶段：编排（第 5 周及以后）

**目标**：多 MCP 工作流 + 持续同步

- [ ] 集成 Playwright MCP 实现自动化视觉测试
- [ ] 为设计-代码一致性检查搭建 CI/CD
- [ ] 创建 Figma → GitHub → 生产 流水线
- [ ] 实施设计系统治理（linting、审计）
- [ ] 让非开发者也能触发 Claude 实现（工单、Slack）
- [ ] 度量指标（TTM、不一致率、节省的开发时间）

**成功标准**：
- 设计更新 → 生产，在 1 天内完成
- 零手动设计转录
- 可度量的团队速度提升

---

## 资源

### 官方文档

- **Figma MCP Server**: [@modelcontextprotocol/server-figma](https://github.com/modelcontextprotocol/servers/tree/main/src/figma) (GitHub)
- **Figma 开发者文档**: [figma.com/developers](https://www.figma.com/developers)
- **Style Dictionary**: [amzn.github.io/style-dictionary](https://amzn.github.io/style-dictionary/)
- **Tokens Studio 插件**: [tokens.studio](https://tokens.studio/)

### 案例研究与教程

- **builder.io**："Claude Code + Figma MCP Server: AI Design-to-Code Workflow"（2026 年 1 月）
  - [builder.io/blog/claude-code-figma-mcp-server](https://www.builder.io/blog/claude-code-figma-mcp-server)
  - 生产环境指标、工作流示例

- **Vladimir Siedykh**："Multi-MCP Orchestration with Claude Code"
  - [vladimirsiedykh.com/blog/claude-code-mcp-workflow](https://vladimirsiedykh.com/)
  - Figma + Playwright + Linear 集成

- **Parallel HQ**："Automating Design Systems with AI"
  - [parallelhq.com/blog/automating-design-systems-with-ai](https://parallelhq.com/)
  - 节省 75 天，Code Connect UI 指南

- **Composio**："How to Use Figma MCP with Claude Code"
  - [composio.dev/blog/how-to-use-figma-mcp-with-claude-code](https://composio.dev/)
  - 令牌层级模式、配置指南

### 社区资源

- **Figma Community**：搜索 "Design System Tokens" 以获取起步模板
- **MCP Registry**: [mcp.run](https://mcp.run/) → Figma server 示例
- **Discord**: Anthropic Discord → #mcp-servers 频道

### 相关工作流

- [图片处理](#working-with-images-and-screenshots) — Claude Code 图片分析
- [ASCII Art 与线框图](#wireframing-tools-for-ai-development) — 低保真设计迭代
- [Playwright MCP](#playwright-browser-automation) — 视觉回归测试

---

## 另请参阅

- [Figma MCP 章节](#figma-mcp-integration) — 主指南 Figma MCP 章节
- [examples/claude-md/product-designer.md](../../examples/claude-md/product-designer.md) — Product Designer CLAUDE.md 模板
- [../cheatsheet.md](../cheatsheet.md) — 快速参考
