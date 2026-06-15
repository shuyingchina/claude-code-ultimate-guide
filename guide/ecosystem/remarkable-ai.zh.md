---
title: "reMarkable 2 + AI：技巧、工具与工作流"
description: "reMarkable 2 的 AI 集成全景图谱 — MCP server、OCR、Obsidian/Notion 管道与自动化"
tags: [mcp, integration, hardware, workflow, remarkable]
---

# reMarkable 2 + AI：技巧、工具与工作流的完整图谱

> **Last verified**: February 2026

reMarkable 2 是一款拥有完整 root 权限的 Linux e-ink 平板。其零干扰的设计理念使它成为一款思考工具，但它的原生集成能力非常简陋。本页涵盖了所有可用于以 AI 增强它的方案 — 从最简单到最技术化的。

## Table of Contents

1. [remarkable-mcp：颠覆性方案](#1-remarkable-mcp--le-game-changer)
2. [Ghostwriter：Vision-LLM 界面](#2-ghostwriter--interface-vision-llm)
3. [将 reMarkable 同步到 Obsidian](#3-sync-remarkable--obsidian)
4. [自定义 OCR + AI 管道](#4-ocr--ai-pipeline-custom)
5. [SSH 访问与社区工具](#5-accès-ssh-et-outils-communautaires)
6. [被低估的原生功能](#6-features-natives-sous-exploitées)
7. [官方 API 与 Developer Portal](#7-api-et-developer-portal-officiel)
8. [Zapier 自动化](#8-automatisation-zapier)
9. [稍后阅读：Web → reMarkable](#9-read-it-later--web--remarkable)
10. [会议记录 → AI 摘要](#10-meeting-notes--ai-summary)
11. [Zotero → reMarkable（研究）](#11-zotero--remarkable-recherche)
12. [将屏幕共享作为 AI 辅助白板](#12-screen-sharing-comme-whiteboard-ai-assisté)
13. [自定义应用与有趣的技巧](#13-apps-custom-et-hacks-fun)
14. [可构建的 AI 增强工作流](#14-workflows-ai-augmentés-à-construire)
15. [从何处入手](#15-par-où-commencer)

---

## 1. remarkable-mcp：颠覆性方案

**ROI：最高 | 投入：中等 | 连接：SSH over USB（无需云端）**

Sam Morrow 创建了一个 **MCP server**，它将 reMarkable 直接连接到 Claude Code、VS Code Copilot 以及任何兼容 MCP 的 AI 助手。

| 属性 | 详情 |
|---------|---------|
| **Repo** | https://github.com/SamMorrowDrums/remarkable-mcp |
| **Blog** | https://sam-morrow.com/blog/building-an-mcp-server-for-remarkable |
| **连接** | SSH over USB — 无需云端，无需订阅 |
| **语言** | Python (FastMCP) |

### 它能做什么

- **原生提取已键入的文本**（Type Folio / 虚拟键盘）— 即时，无需 OCR
- **手写 OCR** 通过 Google Cloud Vision（每月 1000 次免费请求）
- **智能搜索** 遍历你的整个文库
- **文本提取** 从 PDF 和 EPUB + 标注中提取
- **完整遍历** 文档

### 为什么它是 #1

你可以问 Claude “我在 1 月 15 日的会议上关于 X 记了什么？” — 它会在你的手写笔记中检索。reMarkable 由此变成一个 **可查询的 second brain**。

### 技术栈

```
FastMCP + rmscene (parsing .rm natif) + PyMuPDF (PDF)
+ Google Cloud Vision (OCR) + Paramiko (SSH)
```

### 快速安装

```bash
# 1. Activer SSH sur la reMarkable
# Settings → Help → Copyrights and licenses → IP + mot de passe root

# 2. Cloner le repo
git clone https://github.com/SamMorrowDrums/remarkable-mcp
cd remarkable-mcp && pip install -e .

# 3. Ajouter à Claude Code
# Dans ~/.claude.json ou via "claude mcp add"
```

### 在 Claude Code 中的配置

```json
{
  "mcpServers": {
    "remarkable": {
      "command": "python",
      "args": ["-m", "remarkable_mcp"],
      "env": {
        "REMARKABLE_HOST": "10.11.99.1",
        "REMARKABLE_PASSWORD": "<root-password>"
      }
    }
  }
}
```

---

## 2. Ghostwriter：Vision-LLM 界面

**ROI：实验性 | 投入：低（只需复制一个 Rust binary）**

| 属性 | 详情 |
|---------|---------|
| **Repo** | https://github.com/awwaiid/ghostwriter |
| **模型** | GPT-4o Vision |
| **HN discussion** | https://news.ycombinator.com/item?id=42979986 |

### 概念

你在 reMarkable 上手写一个 prompt。一个 vision-LLM（GPT-4o）读取你的笔迹 + 绘图，并 **直接在平板上** 作答。

### 安装

```bash
# 1. Télécharger le binary Rust compilé
scp ghostwriter root@10.11.99.1:/home/root/

# 2. SSH + lancer
ssh root@10.11.99.1
chmod +x ghostwriter && ./ghostwriter
```

### 支持的交互方式

- 手写识别
- 草图分析（wireframes、示意图）
- 小型图标化语言
- 手势

### 具体用例

你画一张架构示意图，写上 “optimise ça”（优化这个）— LLM 会进行视觉分析并作答。这是一个引人入胜的、通过手写笔实现人机交互的原型。

**坦诚的局限**：reMarkable 的原生绘图应用很简陋（无法在回答中自由放置文本）。

---

## 3. 将 reMarkable 同步到 Obsidian

**ROI：如果你使用 Obsidian 则较高 | 投入：低到中等**

### 方案 A：Scrybble（功能最完整）

| 属性 | 详情 |
|---------|---------|
| **Site** | scrybble.ink |
| **Obsidian 插件** | 社区插件（vault settings） |
| **托管** | Self-hosted 或 Scrybble 服务器 |
| **讨论** | https://forum.obsidian.md/t/scrybble-sync-plugin/103194 |

**它能做什么：**

- 将 notebooks、PDF、ePub 同步到 Obsidian vault
- 将 PDF/ePub 的高亮提取为 Markdown
- 将已键入的文本提取为 Markdown
- 在 vault 中将 notebooks 完整渲染为 PDF
- 按页组织并附带 tags

**用例**：学术研究、会议记录，背后配合 Obsidian 搜索。

### 方案 B：自定义 Cloud Sync 插件

- **演示**：https://www.youtube.com/watch?v=EsRdi8J9Cnc
- “remarkable insert” 命令 → 从 reMarkable 云端拉取文件
- `rm/` 文件夹中的 PDF → 嵌入到 Obsidian 笔记中
- 当你在平板上修改时自动重新拉取

---

## 4. 自定义 OCR + AI 管道

**ROI：对于定制化工作流较高 | 投入：中到高**

### rmirror + Claude API（推荐方案）

来源：https://news.ycombinator.com/item?id=47110872（2026 年 2 月）

**概念**：一个 macOS 后台 agent，它会：
1. 从 reMarkable 同步 notebooks
2. 通过 Claude API 进行 OCR（处理带上下文的手写内容时优于 Tesseract）
3. 将转录后的笔记作为可搜索页面推送到 Notion

**为什么 OCR 用 Claude > Tesseract**：Claude 理解上下文，会纠正成形不良的单词，并自动构建列表和表格。

### DIY 管道

```
reMarkable → SSH/USB
  → extract .rm files
  → rmscene parse (texte natif si Type Folio)
  → Claude Vision API (screenshot des pages pour handwriting)
  → texte structuré + tags auto
  → Notion/Obsidian/GitHub via API
```

### 解析工具

| 工具 | 用途 | 链接 |
|-------|-------|------|
| **rmscene** | 原生解析 .rm 文件 | https://github.com/ricklupton/rmscene |
| **rmc** | 将 .rm 转换为 SVG/PNG | https://github.com/ricklupton/rmc |
| **rmapi** | 用 Go 编写的 Cloud API 接口 | https://github.com/juruen/rmapi |

---

## 5. SSH 访问与社区工具

**这是其他一切的必备基础**

### 启用 SSH

```bash
# Via l'interface tablette :
# Settings → Help → Copyrights and licenses
# → Affiche : IP + mot de passe root

# USB (connexion directe)
ssh root@10.11.99.1

# WiFi (après activation)
rm-ssh-over-wlan on
# ou via "Simply Customize It"
```

### 核心工具

| 工具 | 用途 | 链接 |
|-------|-------|------|
| **RMHacks/xovi** | 适用于 rM1/2/Paper Pro 的 mod 框架 | https://www.nilorea.net/2025/08/11/latest-rmhacks-with-xovi-for-remarkable-1-2-paper-pro/ |
| **Simply Customize It** | 用于切换功能的 GUI（WLAN SSH 等） | 第三方应用 |
| **ReMy** | 通过 SSH 浏览/预览/导出文档的 GUI（无需云） | https://github.com/bordaigorl/remy |
| **rmirro** | 平板 ↔ 本地文件夹双向同步 PDF | https://github.com/hersle/rmirro |
| **reStream** | 将 reMarkable 屏幕串流到 Mac/PC | https://github.com/rien/reStream |
| **KOReader** | 替代阅读器（支持更多格式，可定制） | 通过 SSH |
| **reGitable** | 通过 git 自动备份 | awesome-reMarkable |

### 自定义模板

```bash
# Créer un SVG template → copier via SSH
scp mon-template.svg root@10.11.99.1:/usr/share/remarkable/templates/

# Editer templates.json pour l'enregistrer
ssh root@10.11.99.1 'vi /usr/share/remarkable/templates/templates.json'
```

**生成工具**：ReCalendar.me、Remarkable Grid Generator、Remarkably Planner Builder

---

## 6. 被低估的原生功能

**投入成本：零 | 包含在 Connect 订阅中（约 6 欧元/月）**

| 功能 | 用途 |
|---------|-------|
| **Handwriting conversion** | 选择 → 转换 → 复制/粘贴到任意应用 |
| **Cloud sync** | Google Drive、Dropbox、OneDrive |
| **Send to Slack** | 将会议记录直接分享到某个 channel |
| **Handwriting search**（beta AI） | 在你过去的手写笔记中搜索 |
| **Screen sharing** | 将屏幕分享到 PC（演示、会议） |
| **Send to email** | 以 PDF 或 PNG 形式发送 |

**小技巧**：手写 → 文字的转换对独立单词效果不错，但对密集的连笔句子效果较差。优先使用印刷体以获得更好的转换效果。

---

## 7. API 与官方 Developer Portal

| 资源 | 链接 |
|-----------|------|
| **Developer Portal** | https://developer.remarkable.com |
| **Cloud API docs** | https://github.com/splitbrain/ReMarkableAPI |
| **Community guide** | https://remarkable.guide/ |
| **rmfakecloud** | 自托管云（无需 Connect 订阅） |

**操作系统**：Linux（Codex），完整的 SSH root 访问权限，符合 GPL。交叉编译工具链可用于部署自定义原生应用。

**rmfakecloud**：reMarkable 云的开源替代方案，可自托管同步并摆脱 Connect 订阅。

---

## 8. Zapier 自动化

**投资回报：中等 | 投入成本：低 | 无需任何代码**

**机制**：reMarkable → 邮件（my@remarkable.com）→ Zapier 拦截 → 自动化操作

### 可能的目标平台

Google Drive、Asana、ClickUp、Trello、Slack、WordPress、Evernote、Notion

### 免费方案

- 100 个任务/月
- 2 步 Zaps
- 每 15 分钟检查一次

### 具体工作流

```
Notes de réunion → PDF auto-uploadé dans Google Drive
Croquis → Fichier envoyé dans un channel Slack
Action items → Tâches créées dans Asana/ClickUp
```

**来源**：https://myremarkable.substack.com/p/integrating-remarkable

---

## 9. 稍后阅读：Web → reMarkable

**投资回报：阅读场景下很高 | 投入成本：几乎为零**

| 工具 | 描述 |
|-------|-------------|
| **Chrome 扩展 "Read on reMarkable"** | 将任意网页保存为平板上的 EPUB/PDF（去除广告） |
| **Goosepaper** | RSS 流 + 新闻 + 每日 Wikipedia → 针对 e-ink 排版 |
| **remarkable_news** | 将每日新闻/漫画/图片作为待机屏幕 |
| **Instapaper workaround** | 将文章下载为 EPUB → 通过桌面应用导入 |

**PDF 选项**：右键点击扩展 → "Read on reMarkable as PDF"（边距可调，便于批注）。

---

## 10. 会议记录 → AI 摘要

**投资回报：高 | 投入成本：极低**

### 手动工作流（不使用 MCP）

```
1. Notes manuscrites pendant la réunion
2. Screenshot via l'app mobile reMarkable (ou sync cloud)
3. Upload l'image dans Claude/ChatGPT
4. Prompt : "Résume ces notes, extrais les action items avec deadlines et responsables"
```

### MCP 工作流（已安装 remarkable-mcp）

```
Claude, résume mes notes de la réunion d'aujourd'hui
→ Claude fetch les fichiers via SSH
→ OCR si nécessaire
→ Résumé structuré directement
```

**MCP 的优势**：跳过截图和上传步骤。即使没有 Connect 订阅也能运行。

### 推荐模板

Paper Pro Move Meeting Notebook：60 场会议，每场会议 5 个相互关联的页面（概览 + 笔记 + 行动项 + 后续跟进）。

---

## 11. Zotero → reMarkable（研究）

**投资回报：如果你阅读论文则很高 | 投入成本：中等**

| 工具 | 用途 |
|-------|-------|
| **Zotero2reMarkable Bridge** | 从 Zotero 同步 PDF，支持 highlights |
| **KOReader + Toltec + Zotero 插件** | 更好的双栏 PDF 阅读，双向同步 |
| **sync_zotero_remarkable** | 更轻量的替代方案 |

**诚实的局限**：reMarkable 是一个封闭系统。Zotero 集成需要一些变通手段。不如带原生 Zotero 的 Android 电子阅读器那样流畅。可用，但有摩擦。

---

## 12. 将屏幕共享当作 AI 辅助白板

**投资回报：演示/引导场景 | 投入成本：零（Connect 原生功能）**

- **Screen Share**：你的实时书写会显示在外接屏幕/虚拟会议上
- **Laser pointer**：手写笔靠近屏幕顶部 → 激活激光指针
- **组合工作流**：Screen Share + 一位同事实时将你的笔记发送到 ChatGPT = 增强版白板

**价格**：包含在 Connect 中（美国约 30 美元/年，欧洲约 6 欧元/月）。

---

## 13. 自定义应用与有趣的 hack

| 应用/Hack | 描述 |
|----------|-------------|
| **Ephemeris** | 从你的日历生成每日议程（Python） |
| **Remarcal** | 将 Google/Outlook/Apple 日历同步到 reMarkable |
| **reMarkable keywriter** | 无干扰的键盘记事应用 |
| **remarkable-wikipedia** | 离线 Wikipedia 阅读器 |
| **whiteboard-hypercard** | 实时协作，共享绘图 |
| **NetSurf** | 极简网页浏览器（通过 SSH） |
| **pdf2remarkable** | 从命令行上传 PDF 到云 |
| **send-to-remarkable** | 通过邮件上传文档（类似 send-to-Kindle 风格） |
| **libreMarkable** | 用于开发原生应用的框架 |
| **oxide/remux/draft** | 用于多任务的启动器 |
| **latex-yearly-planner** | 用 LaTeX 生成的年度计划本 |

**完整目录**：https://github.com/reHackable/awesome-reMarkable

---

## 14. 待构建的 AI 增强工作流

这些工作流尚未打包，但利用现有的构建模块即可实现。

### A. AI 分析的日志/日记

```
Chaque soir → écrire 1 page de réflexion sur la reMarkable
→ remarkable-mcp + Claude → analyse hebdo des patterns, émotions, décisions
→ Output : insights dans Obsidian avec graph de connexions
```

### B. 辅助式收件箱处理

```
Papiers/articles lus et annotés sur reMarkable
→ OCR via Claude Vision → résumés structurés
→ Tags automatiques + classement dans Obsidian/Notion
```

### C. 草图转代码

```
Dessiner un wireframe UI sur reMarkable
→ Screenshot → Claude Vision → code HTML/React
```

### D. 自动生成抽认卡

```
Notes de cours/lectures sur reMarkable
→ remarkable-mcp → Claude extrait les concepts clés
→ Génère des flashcards Anki automatiquement
```

### E. 自动化的每日站会

```
TODOs écrits chaque matin (template custom)
→ OCR → Slack/email formaté automatiquement
→ Fin de journée : cocher les items, diff envoyé
```

### F. 头脑风暴捕获 → 思维导图

```
Idées griffonnées librement
→ Claude Vision analyse le layout spatial + le texte
→ Génère une mind map structurée (Mermaid/Markmap)
```

---

## 15. 从何处开始

### 阶段 1 — 这个周末（2 小时）

1. 通过 Settings → Help → Copyrights and licenses 启用 SSH
2. 安装 **remarkable-mcp** 并将其连接到 Claude Code
3. 测试：让 Claude 在你的笔记中进行搜索

### 阶段 2 — 接下来的一周

4. 如果你使用 Obsidian → 安装 Scrybble
5. 试用 **Ghostwriter**（安装 10 分钟，乐趣十足）

### 阶段 3 — 当你想更进一步时

6. 用 Claude Vision API 搭建自定义 OCR 流水线
7. 探索 rmfakecloud，摆脱 Connect 订阅

---

## 来源

**GitHub 项目**

- https://github.com/SamMorrowDrums/remarkable-mcp (MCP server, nov 2025)
- https://github.com/awwaiid/ghostwriter (Vision-LLM interface)
- https://github.com/reHackable/awesome-reMarkable (社区目录)
- https://github.com/hersle/rmirro (无云同步)
- https://github.com/bordaigorl/remy (GUI SSH)
- https://github.com/rien/reStream (屏幕串流)
- https://github.com/splitbrain/ReMarkableAPI (Cloud API docs)
- https://github.com/ricklupton/rmscene (原生 .rm 解析)

**文章与讨论**

- https://sam-morrow.com/blog/building-an-mcp-server-for-remarkable
- https://news.ycombinator.com/item?id=47110872 (rmirror + Claude OCR, fév 2026)
- https://news.ycombinator.com/item?id=42979986 (Ghostwriter HN)
- https://news.ycombinator.com/item?id=46099997 (Hacking reMarkable 2, HN 2025)
- https://sgt.hootr.club/blog/hacking-on-the-remarkable-2/ (SSH hacking 指南)
- https://myremarkable.substack.com/p/integrating-remarkable (Zapier integration)

**Obsidian**

- https://forum.obsidian.md/t/scrybble-sync-plugin/103194
- https://www.youtube.com/watch?v=EsRdi8J9Cnc (云同步演示)

**官方**

- https://developer.remarkable.com (Developer Portal, SDK, API)
- https://remarkable.guide/ (Community guide)
