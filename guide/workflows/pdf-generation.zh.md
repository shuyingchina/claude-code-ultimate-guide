---
title: "PDF Generation with Claude Code"
description: "Generate professional PDFs using Claude Code with Quarto and Typst stack"
tags: [workflow, guide, integration]
---

# 使用 Claude Code 生成 PDF

> **可信度**：Tier 2 — 基于经过生产环境验证的 Quarto/Typst 技术栈工作流。

使用 Claude Code 配合现代排版与设计，生成专业的 PDF（文档、白皮书、报告）。

---

## 目录

1. [TL;DR](#tldr)
2. [何时使用](#when-to-use)
3. [技术栈概览](#stack-overview)
4. [安装配置](#setup)
5. [工作流](#workflow)
6. [与 Claude Code 集成](#integration-with-claude-code)
7. [自定义](#customization)
8. [故障排查](#troubleshooting)
9. [另请参阅](#see-also)

---

## TL;DR

```bash
# Install
brew install quarto  # macOS

# Generate
quarto render document.qmd  # → document.pdf

# Preview
quarto preview document.qmd  # Hot-reload
```

**技术栈**：Quarto（编排）+ Typst（排版）+ Pandoc（markdown）

---

## 何时使用

| 使用场景 | 适配度 | 替代方案 |
|----------|----------|-------------|
| 技术文档 | ✅ | — |
| 白皮书 / 报告 | ✅ | — |
| API 文档 | ⚠️ | OpenAPI + Redoc |
| 幻灯片 / 演示文稿 | ⚠️ | Quarto Revealjs |
| 速记笔记 | ❌ | 纯 Markdown |
| 协同编辑 | ❌ | Google Docs、Notion |

**最适合**：需要专业排版、版本控制和可复现性的长篇技术内容。

---

## 技术栈概览

```
┌─────────────────────────────────────────────────┐
│                  Your .qmd File                 │
│         (Markdown + YAML frontmatter)           │
└─────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│                    Quarto                       │
│           (Document rendering engine)           │
│         • Processes YAML metadata               │
│         • Handles extensions                    │
│         • Manages output formats                │
└─────────────────────────────────────────────────┘
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
┌─────────────────────┐    ┌─────────────────────┐
│       Pandoc        │    │       Typst         │
│   (MD → AST → ?)    │    │  (Typography/PDF)   │
│  • Markdown parser  │    │  • Modern engine    │
│  • AST transforms   │    │  • Fast compilation │
│  • Format bridges   │    │  • No LaTeX needed  │
└─────────────────────┘    └─────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│                  document.pdf                   │
│        (Professional typography output)         │
└─────────────────────────────────────────────────┘
```

### 输出格式与命令

```
  FORMAT                COMMANDE                      SORTIE
  ──────                ────────                      ──────

  PDF standard    →  quarto render doc.qmd            doc.pdf
                     --to typst                       (sans template custom)

  PDF stylé ✅    →  quarto render doc.qmd            doc.pdf
                     --to whitepaper-typst            (~270K–1.7M, Bold Guy)
                     (format custom via _extensions/)

  EPUB            →  quarto render doc.qmd            doc.epub
                     --to epub

  Preview         →  quarto preview doc.qmd           hot-reload navigateur
```

### 扩展结构

```
  _extensions/
  └── whitepaper/
      ├── _extension.yml       ← déclare le format "whitepaper-typst"
      ├── typst-template.typ   ← design system (couleurs, typo, callouts)
      └── typst-show.typ       ← bridge Quarto → Typst

  ⚠️  Si tu maintiens des copies dans fr/ en/ et racine :
      garder les 3 fichiers typst-template.typ synchronisés
```

### 快速故障排查

```
  SYMPTÔME                        CAUSE                    FIX
  ────────                        ─────                    ───
  PDF petit (~80-190K), non stylé  --to pdf au lieu de      Utiliser --to whitepaper-typst
                                   --to whitepaper-typst

  Erreur "bibliography"            @ref dans titre callout   Supprimer le @ du titre
                                   → interprété comme cit.

  Table rendue comme code          Backtick ``` non fermé    Compter les ``` (doit être pair)

  "Extension not found"            Mauvais répertoire        Vérifier _extensions/ path
```

| 组件 | 版本 | 角色 |
|-----------|---------|------|
| **Quarto** | ≥1.4.0 | 编排、扩展、多格式输出 |
| **Typst** | 0.13.0 | 现代排版（替代 LaTeX） |
| **Pandoc** | 3.x | Markdown 解析（随 Quarto 捆绑） |

---

## 安装配置

### 安装

**macOS**：
```bash
brew install quarto
```

**Linux (Debian/Ubuntu)**：
```bash
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.555/quarto-1.4.555-linux-amd64.deb
sudo dpkg -i quarto-1.4.555-linux-amd64.deb
```

**Windows**：
```powershell
winget install Posit.Quarto
```

**验证**：
```bash
quarto --version  # Should be ≥1.4.0
```

### 项目结构

```
project/
├── _extensions/           # Quarto extensions (templates)
│   └── custom-template/
│       ├── _extension.yml
│       ├── typst-template.typ
│       └── typst-show.typ
├── documents/
│   ├── guide.qmd          # Source file
│   └── guide.pdf          # Generated output
└── assets/
    └── logo.png           # Shared assets
```

### 最小化文档

创建 `document.qmd`：

```yaml
---
title: "My Document"
author: "Author Name"
date: 2026-01-17
format:
  typst:
    toc: true
lang: en
---

# Introduction

Your content here...

## 第 1 节

更多内容，带 **粗体** 和 `code`。

```bash
echo "Code blocks work!"
```

## 第 2 节

| Column A | Column B |
|----------|----------|
| Data 1   | Data 2   |
```

生成：
```bash
quarto render document.qmd  # Creates document.pdf
```

---

## 工作流

### 1. 内容优先方法

```
1. Write content in Markdown (.qmd)
2. Add YAML frontmatter for metadata
3. Preview with hot-reload
4. Generate final PDF
5. Version control both source and PDF
```

### 2. 可用的 YAML 参数

| 参数 | 类型 | 说明 | 示例 |
|-----------|------|-------------|---------|
| `title` | string | 主标题 | `"Technical Guide"` |
| `subtitle` | string | 副标题 | `"v2.0 Edition"` |
| `author` | string/array | 作者 | `"John Doe"` |
| `date` | date | 文档日期 | `2026-01-17` |
| `date-format` | string | 显示格式 | `"MMMM YYYY"` |
| `toc` | boolean | 目录 | `true` |
| `toc-depth` | number | 目录层级 (1-3) | `2` |
| `lang` | string | 语言 | `fr` or `en` |
| `section-numbering` | string | 编号格式 | `"1.1"` |

### 3. Markdown 特性

**分页符**：
```markdown
{{< pagebreak >}}
```

**代码块**（带语法高亮）：
````markdown
```typescript
function hello(): string {
  return "world";
}
```
````

**表格**：
```markdown
| Feature | Supported |
|---------|-----------|
| Tables  | ✅        |
| Images  | ✅        |
| Links   | ✅        |
```

**图片**：
```markdown
![Alt text](path/to/image.png){width=50%}
```

---

## 与 Claude Code 集成

### 使用 pdf-generator Skill

调用该 skill 进行引导式 PDF 生成：

```
/pdf-generator
```

该 skill 提供：
- 带 YAML frontmatter 的模板
- 设计系统配置
- 常见故障排查修复
- 生成命令

### 提示词示例

**生成文档**：
```
Create a technical guide for our API as a Quarto document.
Use the Typst format with a table of contents.
Include sections for: Authentication, Endpoints, Error Codes.
```

**转换已有的 Markdown**：
```
Convert README.md to a professional PDF.
Add a cover page with title and date.
Use Quarto/Typst format.
```

**创建模板**：
```
Create a Quarto extension for our company's document style:
- Logo in header
- Custom colors: primary #0f172a, accent #6366f1
- Inter font for body, JetBrains Mono for code
```

### 配合 Plan Mode

针对复杂文档：
```
[Press Shift+Tab to enter Plan Mode]

I need to create a series of 5 technical whitepapers.
Plan the structure:
1. Common template/extension
2. Shared assets
3. Build automation
4. Version management
```

### 配合 Hooks

使用 PostToolUse hook 在编辑后自动生成 PDF：

```json
// In .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "if echo \"$TOOL_INPUT\" | grep -q '.qmd'; then quarto render \"$FILE\"; fi"
      }
    ]
  }
}
```

---

## 自定义

### 自定义模板扩展

创建 `_extensions/mytemplate/_extension.yml`：

```yaml
title: My Template
author: Your Name
version: 1.0.0
contributes:
  formats:
    typst:
      template: typst-template.typ
      template-partials:
        - typst-show.typ
```

### Typst 模板变量

在 `typst-template.typ` 中：

```typst
// Colors
#let primary = rgb("#0f172a")      // Dark text
#let secondary = rgb("#334155")    // Lighter text
#let accent = rgb("#6366f1")       // Highlights

// Typography
#set text(
  font: ("Inter", "Helvetica Neue", "Arial"),
  size: 11pt,
)

#set par(
  leading: 0.75em,  // Line height
  justify: true,
)

// Code blocks
#show raw.where(block: true): it => {
  block(
    fill: rgb("#f8fafc"),
    stroke: (left: 3pt + accent),
    inset: 10pt,
    radius: 4pt,
    it,
  )
}
```

### 标注框

在模板中定义：

```typst
#let info(title: "Note", body) = {
  block(
    fill: rgb("#E0F2FE"),
    stroke: (left: 3pt + rgb("#0284C7")),
    inset: 12pt,
    radius: 4pt,
    [*#title*: #body]
  )
}

#let warning(title: "Warning", body) = { ... }
#let success(title: "Success", body) = { ... }
#let danger(title: "Danger", body) = { ... }
```

在文档中使用：
```typst
#info[This is an informational note.]
#warning(title: "Attention")[Check your configuration.]
```

---

## 故障排查

### 快速检查

```bash
# Verify Quarto
quarto --version

# Check extension exists
ls _extensions/*/

# Validate code block pairs (must be even)
grep -c '^```' document.qmd

# Check encoding
file -i document.qmd  # Should show utf-8
```

### 常见问题

| 问题 | 症状 | 修复方法 |
|-------|---------|-----|
| 嵌套代码块 | 内容溢出代码块 | 外层代码块使用 4 个以上反引号 |
| 表格被当作代码 | 灰色背景 | 检查上方是否有未配对的 ` ``` ` |
| 缺少 extension | "Extension not found" | 核实 `_extensions/` 路径 |
| 字体警告 | "unknown font family" | 正常现象；会使用回退字体 |
| 特殊字符损坏 | `?` 或乱码 | 转换为 UTF-8 |

### 嵌套代码块

**问题**：内层代码块过早地关闭了外层代码块。

**解决方案**：外层代码块使用更多反引号：

`````markdown
````markdown
# Outer block with 4 backticks

```bash
echo "Inner block with 3 backticks"
```

Outer block continues...
````
`````

### 校验脚本

```bash
#!/bin/bash
# validate-qmd.sh

for f in *.qmd; do
  count=$(grep -c '^```' "$f")
  if [ $((count % 2)) -ne 0 ]; then
    echo "ERROR: $f has odd code block count ($count)"
  fi
done
```

---

## 参见

- [Quarto 文档](https://quarto.org/docs/guide/)
- [Typst 文档](https://typst.app/docs/)
- [Quarto + Typst 指南](https://quarto.org/docs/output-formats/typst.html)
- [examples/skills/pdf-generator.md](../../examples/skills/pdf-generator.md) — Skill 模板
- [whitepapers/README.md](../../whitepapers/README.md) — 生产环境示例
