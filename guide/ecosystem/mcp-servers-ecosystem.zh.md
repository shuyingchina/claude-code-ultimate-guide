---
title: "MCP Servers Ecosystem"
description: "Validated community MCP servers evaluated for production readiness and security"
tags: [mcp, reference, integration]
---

# MCP 服务器生态系统

**最后更新**：2026 年 5 月 • **下次审查**：2026 年 6 月

本指南介绍除官方 Anthropic 服务器之外、经过验证的社区 MCP 服务器。所列出的所有服务器都已就生产就绪度、维护活跃度和安全性进行了评估。

> **不确定该用 MCP 服务器还是 CLI 工具？** 请参阅 [MCP vs CLI 决策指南](./mcp-vs-cli.md)，获取权衡取舍的完整剖析、决策矩阵以及针对不同情况的指导。

## 目录

- [官方服务器 vs 社区服务器](#official-vs-community-servers)
- [评估框架](#evaluation-framework)
- [生态系统演进](#ecosystem-evolution)
- [经过验证的社区服务器](#validated-community-servers)
  - [浏览器自动化](#browser-automation)
  - [DevOps 与基础设施](#devops--infrastructure)
  - [安全与代码分析](#security--code-analysis)
  - [代码搜索与分析](#code-search--analysis)
  - [文档与知识](#documentation--knowledge)
  - [项目管理](#project-management)
  - [编排](#orchestration)
- [生产部署](#production-deployment)
- [每月观察方法论](#monthly-watch-methodology)
- [已排除的服务器](#excluded-servers)

---

## 官方服务器 vs 社区服务器

| 类型 | 示例 | 特征 | 适用场景 |
|------|----------|-----------------|----------|
| **官方** | filesystem、memory、brave-search、github | Anthropic 维护，稳定性有保证 | 默认选择，核心功能 |
| **社区** | Playwright、Semgrep、Kubernetes | 由组织/个人维护，可能达到生产就绪 | 专业化需求、生态系统集成 |

**关键区别**：官方服务器有 Anthropic 的 SLA 背书，社区服务器需要逐一评估。

---

## 评估框架

所有社区服务器都按照以下标准进行评估：

| 标准 | 阈值 | 理由 |
|-----------|-----------|---------------|
| **GitHub Stars** | ≥50 | 最低限度的社区认可 |
| **近期发布** | <3 个月 | 维护活跃 |
| **文档** | README + 示例 + 配置 | 降低采用门槛 |
| **测试/CI** | ✅ 自动化 | 确保稳定性 |
| **用例** | 官方服务器未覆盖 | 避免冗余 |
| **许可证** | 必须为 OSS | 可持续性与可审计性 |

**质量评分构成**：
- 维护（10 分）：发布频率、issue 响应时间
- 文档（10 分）：README 完整性、示例、故障排查
- 测试（10 分）：测试覆盖率、CI/CD 自动化
- 性能（10 分）：响应时间、资源效率
- 采用度（10 分）：社区使用情况、生产部署

**总分**：`/50` → 归一化为 `/10` 作为最终评级。

---

## 生态系统演进

**重大进展（2026 年 1 月）**：

### Linux Foundation 标准化

MCP 通过 Linux Foundation 治理下的 **Agentic AI Foundation** 成为官方标准。

- **公告**：[YouTube - Linux Foundation](https://www.youtube.com/watch?v=btNbIY7KYwg)
- **影响**：企业采用、长期稳定性保证

### 高级 MCP 工具使用

Anthropic 部署了针对 MCP 上下文管理的优化：

- **延迟加载**：工具按需加载，而非一次性预先加载
- **基于搜索的工具**：在大型工具集中高效发现工具
- **公告**：[Josh Twist LinkedIn](https://www.linkedin.com/posts/joshtwist_anthropic-recently-dropped-advanced-mcp-activity-7399492619581718528-g-Ip)

### MCPB Bundle 格式

用于一键安装 MCP 服务器的标准化 bundle 格式（取代运行时依赖管理）。

- **讨论**：[Reddit - r/ClaudeAI](https://www.reddit.com/r/ClaudeAI/comments/1qkzdh0/mcp_server_installs_are_nondeterministic_heres/)
- **收益**：确定性安装，降低设置摩擦

### MCP Apps（交互式工作工具）

Claude 现在通过 MCP Apps 规范支持交互式工具：

- **示例**：Slack 草稿撰写、Figma 图表、Asana 时间线
- **公告**：[Smol.ai Newsletter](https://news.smol.ai/issues/26-01-26-mcp-apps)
- **深入了解**：参见 [guide/architecture.md:656](../core/architecture.md#mcp-extensions-apps-sep-1865)

### IDE 集成

**Visual Studio 2026** 原生集成了 Azure MCP Server、GitHub Copilot Chat 以及 MCP 客户端。

- **公告**：[Microsoft DevBlogs](https://devblogs.microsoft.com/visualstudio/azure-mcp-server-now-built-in-with-visual-studio-2026-a-new-era-for-agentic-workflows/)

---

## 版本控制（官方服务器）

这些基础性的 MCP 服务器为所有开发工作流提供版本控制自动化。属于**官方 Anthropic 服务器**，稳定性有保证。

### Git MCP (Anthropic)

**官方 Anthropic 服务器**，通过 Model Context Protocol 进行 Git 仓库交互。提供对 Git 操作的程序化访问，具备结构化输出和跨平台安全性。

**仓库**：[modelcontextprotocol/servers/git](https://github.com/modelcontextprotocol/servers/tree/main/src/git)
**许可证**：MIT
**状态**：早期开发（API 可能变更）
**Stars**：77,908+（父仓库）

**用例**：
- **自动化提交工作流**：AI 生成提交信息、暂存变更、提交
- **日志分析**：按日期、作者、分支过滤提交，并提供结构化输出
- **分支管理**：创建功能分支、checkout、按 SHA 过滤
- **token 高效的 diff**：控制上下文行数以聚焦代码审查
- **多仓库自动化**：在 monorepo 设置中管理多个仓库

#### 核心功能

| 工具 | 说明 | 参数 |
|------|-------------|------------|
| `git_status` | 工作树状态（已暂存、未暂存、未跟踪） | - |
| `git_log` | 带高级过滤的提交历史 | `max_count`、`skip`、`start_timestamp`、`end_timestamp`、`author` |
| `git_diff` | 提交/分支之间的 diff | `target`、`source`、`context_lines` |
| `git_diff_unstaged` | 未暂存的变更 | `context_lines` |
| `git_diff_staged` | 已暂存的变更 | `context_lines` |
| `git_commit` | 创建提交 | `message` |
| `git_add` | 暂存文件/模式 | `files` |
| `git_reset` | 取消暂存文件 | `files` |
| `git_branch` | 列出/过滤分支 | `contains`、`not_contains` |
| `git_create_branch` | 创建新分支 | `name` |
| `git_checkout` | 切换分支/提交 | `ref` |
| `git_show` | 显示提交详情 | `revision` |

**高级过滤**（`git_log`）：
- **ISO 8601 日期**：`2024-01-15T14:30:25`
- **相对日期**：`2 weeks ago`、`yesterday`、`last month`
- **绝对日期**：`2024-01-15`、`Jan 15 2024`
- **作者过滤**：`--author="John Doe"`

#### 设置

**安装（3 种方法）**：

```bash
# Method 1: UV (recommended) - one-liner
uvx mcp-server-git --repository /path/to/repo

# Method 2: pip + Python module
pip install mcp-server-git
python -m mcp_server_git

# Method 3: Docker (sandboxed)
docker run -v /path/to/repo:/repo ghcr.io/modelcontextprotocol/mcp-server-git
```

**Claude Code 配置**（`~/.claude.json`）：

```json
{
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/Users/you/projects/myrepo"]
    }
  }
}
```

**多仓库支持**：

```json
{
  "mcpServers": {
    "git-main": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/path/to/main-repo"]
    },
    "git-docs": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/path/to/docs-repo"]
    }
  }
}
```

#### IDE 集成

**提供一键安装按钮的对象**：
- **Claude Desktop**（macOS/Windows/Linux）
- **VS Code**（Stable + Insiders）
- **Zed**
- **Zencoder**

集成链接参见 [官方 README](https://github.com/modelcontextprotocol/servers/tree/main/src/git#quickstart)。

#### 质量评分

**8.5/10** ⭐⭐⭐⭐⭐

| 标准 | 评分 | 备注 |
|-----------|-------|-------|
| 维护 | 10/10 | Anthropic 背书，开发活跃 |
| 文档 | 9/10 | README 全面、有示例，但存在早期开发警告 |
| 测试 | 8/10 | 自动化 CI，覆盖率持续提升 |
| 性能 | 8/10 | 快速（<100ms），结构化输出减少 token |
| 采用度 | 8/10 | 官方服务器，77K+ stars，广泛的 IDE 支持 |

#### 局限性与变通方案

| 局限性 | 变通方案 |
|------------|-----------|
| **早期开发**（API 变更） | 在生产中固定版本，关注发布动态 |
| **不支持交互式 rebase**（`-i` 标志） | 使用 Bash 工具执行 `git rebase -i` |
| **不支持 reflog** | 使用 Bash 工具执行 `git reflog` |
| **不支持 git bisect** | 使用 Bash 工具执行 `git bisect` |
| **每个实例仅支持单个仓库** | 配置多个 MCP 服务器实例 |

#### 决策矩阵：Git MCP vs GitHub MCP vs Bash 工具

**何时使用哪个工具**：

| 操作 | Git MCP | GitHub MCP | Bash 工具 | 理由 |
|-----------|---------|------------|-----------|---------------|
| **本地提交** | ✅ 最佳 | ❌ | ⚠️ 尚可 | 结构化输出，跨平台安全 |
| **分支管理** | ✅ 最佳 | ❌ | ⚠️ 尚可 | `git_branch` 过滤，SHA contains/excludes |
| **Diff/log 分析** | ✅ 最佳 | ❌ | ⚠️ 尚可 | `context_lines` 控制，token 高效 |
| **暂存文件** | ✅ 最佳 | ❌ | ⚠️ 尚可 | 模式匹配（`git_add`），更安全 |
| **创建 PR** | ❌ | ✅ 最佳 | ⚠️ gh CLI | GitHub API、标签、指派人、审查者 |
| **issue 管理** | ❌ | ✅ 最佳 | ⚠️ gh CLI | GitHub 专属操作 |
| **CI/CD 状态检查** | ❌ | ✅ 最佳 | ⚠️ gh CLI | GitHub Actions 集成 |
| **交互式 rebase** | ❌ | ❌ | ✅ 最佳 | Git MCP 不支持 `-i` 标志 |
| **reflog 恢复** | ❌ | ❌ | ✅ 最佳 | 高级 Git 操作 |
| **git bisect 调试** | ❌ | ❌ | ✅ 最佳 | 复杂调试工作流 |
| **多工具流水线** | ✅ | ✅ | ❌ | MCP 服务器可与其他 MCP 工具组合 |

**决策树**：

```
Is it a GitHub-specific operation (PRs, Issues, Actions)?
├─ YES → Use GitHub MCP
└─ NO → Is it a core Git operation (commit, branch, diff, log)?
    ├─ YES → Use Git MCP (structured, safe, token-efficient)
    └─ NO → Is it an advanced Git feature (rebase -i, reflog, bisect)?
        ├─ YES → Use Bash tool (flexibility)
        └─ NO → Default to Git MCP (safer, structured)
```

**工作流示例**：

| 工作流 | 工具链 | 理由 |
|----------|-----------|---------------|
| **功能开发** | Git MCP（`git_create_branch` + `git_commit`）→ GitHub MCP（PR） | 原子化、结构化、完整生命周期 |
| **提交历史分析** | Git MCP（`git_log` 配合 `start_timestamp: "2 weeks ago"`） | token 高效的过滤，相对日期 |
| **代码审查准备** | Git MCP（`git_diff` 配合 `context_lines: 3`） | 聚焦上下文，减少 token |
| **清理提交（rebase）** | Bash 工具（`git rebase -i HEAD~5`） | Git MCP 不支持交互式模式 |
| **恢复丢失的提交** | Bash 工具（`git reflog`） | Git MCP 未暴露 reflog |
| **用 bisect 查找 bug** | Bash 工具（`git bisect start/good/bad`） | Git MCP 不支持 bisect 工作流 |
| **自动化发布流程** | Git MCP（commit + tag）→ GitHub MCP（创建 release） | 完整自动化、结构化 |

#### 资源

- **GitHub**：https://github.com/modelcontextprotocol/servers/tree/main/src/git
- **父仓库**：https://github.com/modelcontextprotocol/servers（77,908+ stars）
- **MCP Inspector**：支持调试工具，可进行实时测试
- **Docker Hub**：`ghcr.io/modelcontextprotocol/mcp-server-git`

---

## 经过验证的社区服务器

### 浏览器自动化

#### Playwright MCP (Microsoft)

**Microsoft 官方服务器**，用于针对 LLM 优化的浏览器自动化。使用无障碍树（accessibility trees）而非截图，从而降低 token 消耗。

**使用场景**：AI 编码 agent 在浏览器中验证自己的工作（E2E 测试、缺陷验证）。

**核心特性**：

| 能力 | 详情 |
|------------|---------|
| 浏览器自动化 | 导航、点击、填写、悬停（Playwright API） |
| 内容提取 | 通过无障碍树获取结构化数据 |
| 截图 | 整页 + 指定元素 |
| JavaScript 执行 | 在页面上下文中运行代码 |
| 会话管理 | 持久化浏览器状态 |
| 支持的浏览器 | Chromium、Firefox、WebKit |

**安装设置**：

```bash
# Installation
npm install @microsoft/playwright-mcp
# or
npx @microsoft/playwright-mcp
```

**Claude Code 配置** (`~/.claude.json`)：

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["--yes", "@microsoft/playwright-mcp"]
    }
  }
}
```

**用法示例**：

```
User: "Navigate to example.com, log in with email test@example.com, then take a screenshot"

Claude: [Uses playwright_navigate → playwright_type → playwright_click → playwright_screenshot]

Result: Screenshot + accessibility tree in context
```

**质量评分**：**8.8/10** ⭐⭐⭐⭐⭐

| 维度 | 评分 | 备注 |
|-----------|-------|-------|
| 维护 | 9/10 | 双周发布，Microsoft 团队活跃 |
| 文档 | 9/10 | README 完整，含示例、Playwright Live 视频 |
| 测试 | 10/10 | 测试套件全面，CI/CD 自动化 |
| 性能 | 8/10 | 快照速度快（约 200ms），内存占用高效 |
| 采用度 | 8/10 | 2890+ 次使用（Smithery.ai 统计） |

**局限与变通方案**：

| 局限 | 变通方案 |
|------------|-----------|
| 单一浏览器会话 | 使用 session ID 持久化状态 |
| 不支持跨域 iframe 访问 | 限制为同源内容 |
| 截图尺寸上限（最大 4K） | 大页面使用元素快照 |

**替代方案**：

| 服务器 | 优势 | 劣势 |
|--------|-----------|--------------|
| **Playwright MCP** | 无障碍树，LLM 原生 | 不支持视觉模型 |
| Browserbase MCP | 基于云端，隐身模式 | API 成本、延迟 |
| Puppeteer MCP | 轻量，仅 JS | 结构化数据较少 |

**资源**：
- **GitHub**: https://github.com/microsoft/playwright-mcp
- **Releases**: https://github.com/microsoft/playwright-mcp/releases
- **Playwright Live Demo**: https://youtu.be/CNzg1aPwrKI

---

#### Browserbase MCP

**Browserbase 官方服务器**，用于云端浏览器自动化。内置 Stagehand AI agent 实现自主任务执行。

**使用场景**：需要隐身模式、代理支持或自主执行的复杂网页交互（网页抓取、表单填写、数据提取）。

**核心特性**：

| 能力 | 详情 |
|------------|---------|
| 浏览器控制 | 通过 Browserbase 云端运行 Chromium |
| Stagehand Agent | 自主任务执行（例如"预订航班"） |
| 数据提取 | CSS 选择器 + 基于 schema 的结构化提取 |
| 反检测 | 隐身模式、代理支持、轮换 |
| 多模型 | OpenAI、Claude、Gemini、自定义 LLM |

**安装设置**：

```bash
npm install @browserbasehq/mcp-server-browserbase
```

**配置**：

```json
{
  "mcpServers": {
    "browserbase": {
      "command": "npx",
      "args": ["@browserbasehq/mcp-server-browserbase"],
      "env": {
        "BROWSERBASE_API_KEY": "YOUR_KEY",
        "BROWSERBASE_PROJECT_ID": "YOUR_PROJECT_ID",
        "GEMINI_API_KEY": "YOUR_GEMINI_KEY"
      }
    }
  }
}
```

**质量评分**：**7.6/10** ⭐⭐⭐⭐

**成本**：免费增值（按 API 用量付费），约 $0.10/会话

**局限**：

| 局限 | 变通方案 |
|------------|-----------|
| 延迟（云端约 500ms） | 批量操作，缓存结果 |
| API 成本 | 仅用于高价值提取 |
| Stagehand 局限 | 回退到手动的 playwright_* 工具 |

**资源**：
- **GitHub**: https://github.com/browserbase/mcp-server-browserbase
- **官方文档**: https://www.browserbase.com

---

#### Chrome DevTools MCP

**Anthropic 官方服务器**，用于集成 Chrome DevTools Protocol。通过 Chrome 原生 DevTools API 提供调试与检查能力。

**使用场景**：调试 Web 应用、检查运行时状态、监控网络请求、分析性能。以面向开发的调试能力补充 Playwright MCP（测试）。

**核心特性**：

| 能力 | 详情 |
|------------|---------|
| 控制台访问 | 读取浏览器控制台日志、错误、警告 |
| 网络监控 | 检查 HTTP 请求、响应、headers |
| DOM 检查 | 查询 DOM 结构、元素属性 |
| JavaScript 执行 | 在页面上下文中执行任意 JS |
| 性能剖析 | CPU 剖析、内存快照 |

**安装设置**：

```bash
npm install @modelcontextprotocol/server-chrome-devtools
```

**配置**：

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-chrome-devtools"]
    }
  }
}
```

**何时使用**：

| 场景 | 使用 Chrome DevTools MCP | 使用 Playwright MCP |
|----------|------------------------|-------------------|
| 调试运行时错误 | ✅ 控制台日志、堆栈跟踪 | ❌ 错误可见性有限 |
| 检查网络调用 | ✅ 完整的请求/响应详情 | ⚠️ 仅基础导航 |
| 测试用户交互 | ❌ 并非为测试设计 | ✅ 点击、输入、导航 |
| 剖析性能 | ✅ CPU/内存剖析 | ❌ 无剖析工具 |
| 自动化工作流 | ❌ 聚焦手动调试 | ✅ E2E 测试自动化 |

**局限**：
- 需要运行已启用 DevTools Protocol 的 Chrome 浏览器
- 需手动设置（以 `--remote-debugging-port` 启动 Chrome）
- 不适合自动化测试（请改用 Playwright）
- 启用剖析时存在性能开销

**资源**：
- **npm**: https://www.npmjs.com/package/@modelcontextprotocol/server-chrome-devtools
- **Chrome DevTools Protocol**: https://chromedevtools.github.io/devtools-protocol/

---

### DevOps 与基础设施

#### Kubernetes MCP (Red Hat)

**Containers 社区官方服务器**（由 Red Hat 支持），用于以自然语言管理 Kubernetes/OpenShift。

**使用场景**：DevOps/SRE 使用 Claude 查询/配置集群（"自然语言版 kubectl"）。

**核心特性**：

| 能力 | 详情 |
|------------|---------|
| 资源 CRUD | 对任意 K8s 资源进行创建、读取、更新、删除 |
| Pod 操作 | 日志、事件、exec、指标（top） |
| 部署管理 | 扩缩容、滚动更新、状态 |
| 配置管理 | 查看/更新 ConfigMaps、Secrets |
| CRD 支持 | 自定义资源定义 |
| 多集群 | 切换 kubeconfig 上下文 |
| OpenShift 支持 | 原生 OpenShift 资源 |

**安装设置**：

```bash
# Docker
docker run -it --rm \
  --mount type=bind,src=$HOME/.kube/config,dst=/home/mcp/.kube/config \
  ghcr.io/containers/kubernetes-mcp-server

# Native (Go binary)
go install github.com/containers/kubernetes-mcp-server@latest
kubernetes-mcp-server
```

**Claude Desktop 配置**：

```json
{
  "mcpServers": {
    "kubernetes": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--mount",
        "type=bind,src=/home/user/.kube/config,dst=/home/mcp/.kube/config",
        "ghcr.io/containers/kubernetes-mcp-server"
      ]
    }
  }
}
```

**用法示例**：

```
User: "Show me all pods in production namespace with memory usage >500Mi"
Claude: [Uses list_resources for pods + metrics]
Result: List of pods with memory stats

User: "Scale the backend deployment to 5 replicas"
Claude: [Uses patch_resource]
Result: Deployment scaled
```

**质量评分**：**8.4/10** ⭐⭐⭐⭐

**安全性**：RBAC 强制执行、kubeconfig 认证、无权限提升

**局限**：

| 局限 | 变通方案 |
|------------|-----------|
| 需要 kubeconfig 访问权限 | 使用 ServiceAccount + RBAC 以确保安全 |
| 节点 shell 访问受限 | 使用 `kubectl exec` 进行调试 |
| CRD 发现存在延迟 | 预先为 AI 上下文记录 CRD |

**资源**：
- **GitHub**: https://github.com/containers/kubernetes-mcp-server
- **Red Hat 文档**: https://developers.redhat.com/articles/2025/09/25/kubernetes-mcp-server-ai-powered-cluster-management

---

#### Vercel MCP

**社区服务器**，用于 Vercel 平台（部署、项目、环境变量、团队）。

**使用场景**：AI 助手生成 Next.js 代码、创建 Vercel 项目、配置环境变量、触发部署——无需离开 IDE 即可完成完整的 CI/CD 闭环。

**核心特性**：

| 能力 | 详情 |
|------------|---------|
| 部署 | 列出、获取详情、创建、监控状态 |
| 项目 | 列出、创建、更新设置 |
| 环境变量 | 获取、设置、管理 secrets |
| 团队 | 列出、创建、管理 |
| 域名 | 列出、配置、DNS 管理 |
| 函数 | 监控 Vercel Functions、日志 |

**安装设置**：

```bash
git clone https://github.com/nganiet/mcp-vercel
cd vercel-mcp
npm install
```

**配置**：

```json
{
  "mcpServers": {
    "vercel": {
      "command": "npm",
      "args": ["start"],
      "env": {
        "VERCEL_API_TOKEN": "YOUR_VERCEL_TOKEN"
      }
    }
  }
}
```

**质量评分**：**7.6/10** ⭐⭐⭐⭐

**注意**：Vercel 也提供官方 MCP 服务器。此社区版本提供了全面的 API 覆盖。

**资源**：
- **GitHub**: https://github.com/nganiet/mcp-vercel
- **Vercel 文档**: https://vercel.com/docs/mcp/deploy-mcp-servers-to-vercel
- **官方 Vercel MCP**: https://vercel.com/docs/mcp/vercel-mcp

#### Sentry MCP

**Sentry 官方服务器**，用于错误监控与可观测性。闭合诊断回路：Sentry 告警触发 → Claude 读取 issue + 堆栈跟踪 → 诊断根因 → 提出或编写补丁。

**仓库**：[getsentry/sentry-mcp](https://github.com/getsentry/sentry-mcp)
**许可证**：MIT
**维护者**：Sentry（官方）

**使用场景**：生产环境触发了一条 Sentry 告警。工程师问 Claude："是什么导致了 SEN-4521？"。Claude 读取完整堆栈跟踪，在代码库中追溯这次回归，并起草修复——全程无需离开 IDE。可观测性回路在 Claude Code 内部闭合。

**核心特性**：

| 工具 | 描述 |
|------|-------------|
| `list_issues` | 使用 Sentry 查询语法获取未解决的 issue（`is:unresolved level:error`） |
| `get_issue` | 完整 issue 详情——堆栈跟踪、受影响用户、首次/最近出现时间戳 |
| `get_event` | 按 ID 获取特定事件，适用于限定时间范围的调查 |
| `search_events` | 对原始事件进行全文搜索，支持字段过滤 |
| `list_projects` | 列出你 Sentry 组织中的项目 |

**安装设置**：

```bash
# Via npx (recommended — verify package name against official docs)
npx -y @sentry/mcp-server

# One-liner for Claude Code
claude mcp add sentry -- npx -y @sentry/mcp-server
```

**Claude Code 配置** (`~/.claude/settings.json`)：

```json
{
  "mcpServers": {
    "sentry": {
      "command": "npx",
      "args": ["-y", "@sentry/mcp-server"],
      "env": {
        "SENTRY_AUTH_TOKEN": "your_auth_token",
        "SENTRY_ORG": "your-org-slug"
      }
    }
  }
}
```

> 认证 token：[sentry.io/settings/account/api/auth-tokens/](https://sentry.io/settings/account/api/auth-tokens/) —— 所需 scopes：`project:read`、`event:read`、`org:read`

**用法示例**：

```
User: "What's causing SEN-4521? It's been firing since yesterday's deploy."

Claude:
  [list_issues: query="is:unresolved level:error project:api-service"]
  [get_issue: issue_id="4521"]

Result: NullPointerException in UserController.getProfile() at line 142.
  Introduced in commit a3f8c2 (yesterday 14:32 UTC) — null check removed
  in the profile refactor. Fix: restore Optional.ofNullable at line 142.
  Opening a PR now.
```

**查询语法**（有效使用的关键——也是调用失败最常见的根源）：

```
is:unresolved                         # unresolved issues only
is:unresolved level:error             # errors only (excludes warnings, info)
is:unresolved has:user                # issues with identified users
is:unresolved times_seen:>100         # high-frequency issues
project:api-service is:unresolved     # scope to one project
assigned:me is:unresolved             # issues assigned to you
!has:assignee is:unresolved           # unassigned issues
```

> **参考文件**：本仓库中的 `examples/skills/mcp-integration-reference/references/sentry-mcp.md` —— 包含完整的参数文档、注意事项、分页模式，以及一份精选的噪音排除列表。将其复制到你的 CLAUDE.md includes 或项目 skills 中。

**质量评分**：**8.5/10** ⭐⭐⭐⭐⭐

| 维度 | 评分 | 备注 |
|-----------|-------|-------|
| 维护 | 10/10 | Sentry 官方服务器，企业级支持 |
| 文档 | 8/10 | 优秀的 README + Sentry 文档覆盖边缘情况 |
| 测试 | 8/10 | 具备 CI，TypeScript 类型安全 |
| 性能 | 8/10 | 受 API 限制（约 200–400ms），大型组织需分页 |
| 采用度 | 9/10 | Sentry 是事实上的错误监控标准（10 万+ 组织） |

**局限与变通方案**：

| 局限 | 变通方案 |
|------------|-----------|
| `organization_slug` ≠ 显示名称 | 从 URL 读取 slug：`sentry.io/organizations/<slug>/` |
| `search_events` 在大型组织中超时 | 搜索事件时始终使用 `project_slug` 限定范围 |
| 每次调用最多 100 个 issue | 完整扫描时使用基于 cursor 的分页 |
| 默认只读 | 解决/分配操作需要额外的 token scopes |
| 90 天事件保留期 | 默认 Sentry 套餐下无法获取超过 90 天的事件 |

**何时使用 vs 替代方案**：

| 工具 | 最适合 | 不值得使用的情况 |
|------|----------|-------------------|
| **Sentry MCP** | 错误诊断回路：告警 → 堆栈跟踪 → 补丁 | 纯告警（直接用 webhooks 或 PagerDuty） |
| **Datadog MCP** | APM、分布式追踪、指标仪表盘 | 纯错误工作流——对此用例过度设计 |
| **Bash + Sentry CLI** | 批量操作、脚本化数据导出 | 交互式调试会话 |

**资源**：
- **GitHub**: https://github.com/getsentry/sentry-mcp
- **Sentry MCP 文档**: https://docs.sentry.io/product/sentry-mcp/
- **参考文件**: `examples/skills/mcp-integration-reference/references/sentry-mcp.md`
- **认证 token 设置**: https://sentry.io/settings/account/api/auth-tokens/

---

### 安全与代码分析

#### Semgrep MCP

**Semgrep 官方服务器**，用于漏洞扫描（SAST、secrets、供应链）。内置自定义规则引擎。

**使用场景**：Claude Code 生成代码，Semgrep 自动扫描安全问题并提出修复（"默认安全"）。

**核心特性**：

| 能力 | 详情 |
|------------|---------|
| 快速扫描 | 对代码片段进行快速安全检查 |
| 完整扫描 | 使用 p/ci 规则集进行全面 SAST |
| 自定义规则 | 使用用户提供的 Semgrep 规则扫描 |
| AST 生成 | 用于分析的抽象语法树 |
| 规则集支持 | 预构建规则集（OWASP、CWE 等） |
| 语言覆盖 | Python、JS/TS、Java、Go、C#、Rust、PHP 等 |

**安装设置**：

```bash
# Via uvx (recommended)
uvx semgrep-mcp

# Or pip
pip install semgrep-mcp
```

**Claude Code 配置**：

```bash
claude mcp add semgrep -- uvx semgrep-mcp
```

**Cursor 配置** (`~/.cursor/mcp.json`)：

```json
{
  "mcpServers": {
    "semgrep": {
      "command": "uvx",
      "args": ["semgrep-mcp"],
      "env": {
        "SEMGREP_APP_TOKEN": "your_token"
      }
    }
  }
}
```

**用法示例**：

```
User: "Scan this Python code for SQL injection vulnerabilities"

Code:
  def search(query):
      return db.execute(f"SELECT * FROM users WHERE name = '{query}'")

Claude: [Uses security_check tool]

Result: [VULNERABLE] SQL injection detected at line 2.
  Fix: Use parameterized queries:
  return db.execute("SELECT * FROM users WHERE name = ?", [query])
```

**质量评分**：**9.0/10** ⭐⭐⭐⭐⭐

| 维度 | 评分 | 备注 |
|-----------|-------|-------|
| 维护 | 10/10 | 官方，频繁发布 |
| 文档 | 9/10 | 文档全面，含示例 |
| 测试 | 10/10 | 测试覆盖广泛 |
| 性能 | 7/10 | 良好，取决于复杂度（每次扫描约 500ms） |
| 采用度 | 9/10 | 企业标准（5000+ 家公司） |

**替代方案**：

| 服务器 | 优势 | 劣势 |
|--------|-----------|--------------|
| **Semgrep** | 全面 SAST，自定义规则 | 在大型代码库上较慢 |
| GitGuardian | 聚焦 secrets，速度快 | SAST 覆盖有限 |
| SonarQube | 企业级，报告详尽 | 较重，设置更多 |

**资源**：
- **GitHub**: https://github.com/semgrep/mcp
- **官方文档**: https://semgrep.dev/docs/mcp
- **规则注册表**: https://semgrep.dev/r
- **定价**: https://semgrep.dev/pricing（MCP 免费层）

---

### 代码搜索与分析

#### Grepai MCP

**社区服务器**，通过本地 Ollama embeddings 实现语义代码搜索和调用图分析。它按意图搜索代码（如 "payment flow"、"auth logic"）而非精确模式，并追踪函数调用关系。

**仓库**：[yoanbernabeu/grepai](https://github.com/yoanbernabeu/grepai)
**许可证**：MIT
**状态**：活跃开发中
**隐私**：完全本地化（Ollama + nomic-embed-text），数据不会离开你的机器

**使用场景**：开发者需要理解不熟悉的代码库 → grepai 通过自然语言描述找到相关代码并映射函数依赖，无需阅读整个文件。

**核心特性**：

| 能力 | 详情 |
|------------|---------|
| `grepai_search` | 通过自然语言查询进行语义搜索（如 "error handling middleware"） |
| `grepai_trace_callers` | 查找调用给定符号的所有函数 |
| `grepai_trace_callees` | 查找被给定符号调用的所有函数 |
| `grepai_trace_graph` | 完整调用图（callers + callees），深度可配置 |
| `grepai_index_status` | 健康检查：已索引文件、分块、配置 |

**Token 效率**：

| 工作流 | Token | 评价 |
|----------|--------|---------|
| Grep + Read 文件（暴力穷举） | ~15K | 噪声大，大量无关上下文 |
| grepai search + trace | ~4K | 精准，仅返回相关结果 |
| 仅 grepai（无后续操作） | ~2-3K | 快速发现 |

**安装配置**：

```bash
# Install grepai
curl -sSL https://raw.githubusercontent.com/yoanbernabeu/grepai/main/install.sh | sh

# Install Ollama + embedding model
brew install ollama
ollama pull nomic-embed-text

# Initialize in your project
cd /path/to/project
grepai init  # Choose: ollama, nomic-embed-text, gob

# Index your codebase
grepai index

# Optional: watch for file changes (auto-reindex)
grepai watch
```

**Claude Code 配置**：

```bash
claude mcp add grepai -- grepai mcp
```

**`.mcp.json`（项目级）**：

```json
{
  "mcpServers": {
    "grepai": {
      "command": "grepai",
      "args": ["mcp"]
    }
  }
}
```

**使用示例**：

```
User: "Find the authentication flow in this codebase"

Claude: [Uses grepai_search query="authentication flow" limit=5]

Result: 3 relevant files with line numbers and similarity scores
  - src/auth/middleware.ts:12-45 (0.89)
  - src/routes/login.ts:8-32 (0.85)
  - src/utils/jwt.ts:1-28 (0.78)

User: "What calls the validateToken function?"

Claude: [Uses grepai_trace_callers symbol="validateToken"]

Result: Call graph showing 4 callers across 3 files
  - authMiddleware → validateToken
  - refreshHandler → validateToken
  - wsAuthGuard → validateToken
  - testHelper → validateToken
```

**质量评分**：**7.8/10** ⭐⭐⭐⭐

| 维度 | 评分 | 备注 |
|-----------|-------|-------|
| 维护 | 8/10 | 活跃开发，维护者响应及时 |
| 文档 | 7/10 | README 良好，含 MCP 集成文档 |
| 测试 | 7/10 | 已有 CI，覆盖率持续增长 |
| 性能 | 8/10 | 本地 embeddings 快速（搜索约 2s），无网络延迟 |
| 采用度 | 9/10 | 社区增长中，已在 Claude Code 配置中投入生产使用 |

**局限与变通方案**：

| 局限 | 变通方案 |
|------------|-----------|
| 需要本地运行 Ollama | `brew services start ollama`（自动启动） |
| 索引可能变陈旧 | 使用 `grepai watch` 自动重建索引 |
| 不适合精确模式匹配 | 用原生 Grep 工具处理正则模式 |
| Embedding 模型下载（~270MB） | 一次性执行 `ollama pull nomic-embed-text` |

**替代方案**：

| 服务器 | 优势 | 劣势 |
|--------|-----------|--------------|
| **Grepai** | 本地、私密、语义 + 调用图 | 需要配置 Ollama |
| **Semble** | 无需 Ollama，覆盖代码 + 文档 + 配置范围 | 无调用图分析 |
| 原生 Grep | 即时、精确模式 | 无语义理解 |
| GitHub Code Search | 基于云、跨仓库 | 需要 GitHub，无调用图 |

**交叉引用**：详见 [ultimate-guide.md — MCP Servers: Grepai](../ultimate-guide.md)，了解详细使用模式、提示策略以及与其他 MCP 服务器的集成。

**资源**：
- **GitHub**：https://github.com/yoanbernabeu/grepai
- **Ollama**：https://ollama.com
- **Embedding 模型**：nomic-embed-text (nomic-ai)

---

#### Semble

**社区服务器**，可跨代码、文档和配置文件进行语义代码搜索。它使用 Model2Vec embeddings，配合 BM25 排序和 RRF 融合，仅靠 CPU 运行，无任何外部服务依赖。

**仓库**：[MinishLab/semble](https://github.com/MinishLab/semble)
**许可证**：MIT
**状态**：活跃（v0.3.3，2026 年 6 月），约 5,000 stars
**隐私**：完全本地化（Model2Vec 仅 CPU），数据不会离开你的机器

**使用场景**：开发者想要语义代码搜索但不想本地运行 Ollama。Semble 在首次运行时构建本地索引（Model2Vec + BM25 + RRF）并缓存。它通过自然语言查询搜索代码、文档和配置文件。

**核心特性**：

| 能力 | 详情 |
|------------|---------|
| 语义搜索 | 跨代码、文档和配置文件的自然语言查询 |
| MCP 服务器 | 原生集成（`semble mcp`），无需 CLI 封装 |
| 无外部服务 | Model2Vec 仅 CPU 运行；无需 Ollama，无需 API key |
| 索引 | 首次运行时构建，自动缓存（每个新目录都需要构建一次） |

**Token 效率**：

| 工作流 | Token | 评价 |
|----------|--------|---------|
| Grep + Read 文件（暴力穷举） | ~15K | 噪声大，大量无关上下文 |
| Semble search（代码 + 文档 + 配置） | ~2-4K | 精准结果，范围比纯代码更广 |

**安装配置**：

```bash
pip install semble

# Start the MCP server
semble mcp
```

**Claude Code 配置**：

```bash
claude mcp add semble -- semble mcp
```

**与 Grepai 的对比**：

| 方面 | Grepai | Semble |
|--------|--------|--------|
| 外部服务 | 需要（Ollama + nomic-embed-text） | 不需要（仅 CPU 的 Model2Vec） |
| MCP 集成 | CLI 封装为 MCP | 原生 MCP 服务器 |
| 搜索范围 | 仅代码 | 代码 + 文档 + 配置 |
| 调用图分析 | 支持（trace_callers、trace_callees、trace_graph） | 不支持 |
| 社区热度 | 维护者活跃 | 约 5,000 GitHub stars |

**何时选择 Semble 而非 Grepai**：你想要语义代码搜索但不想本地运行 Ollama。Semble 更广的覆盖范围在 monorepo 中也很有帮助——那里浏览配置和文档与浏览代码同样重要。当调用图分析必不可少时选择 Grepai；Semble 不提供此能力。

> **关于"免索引"说法的说明**：一些社区帖子称 Semble 不需要索引。这是错误的。Semble 在首次运行时构建本地索引并缓存。每个新目录都需要单独构建一次索引。

**质量评分**：**7.2/10**（范围：评估较窄，待更广泛的社区信号）

**资源**：
- **GitHub**：https://github.com/MinishLab/semble
- **PyPI**：`pip install semble`
- **评估**：[docs/resource-evaluations/semble-code-search.md](../../docs/resource-evaluations/semble-code-search.md)

---

### 文档与知识

#### Context7 MCP

**Upstash 官方服务器**，提供实时库文档（LangChain、Anthropic SDK 等）。消除 API 幻觉。

**使用场景**：Claude Code 需要使用某个库的 API → Context7 提供最新文档 + 示例。

**核心特性**：

| 能力 | 详情 |
|------------|---------|
| 库搜索 | 查找 500+ 个库的文档 |
| 代码示例 | 特定语言的示例（Python、TS 等） |
| API 参考 | 详细的函数签名、参数 |
| 版本过滤 | 特定库版本的文档 |
| 智能排序 | 按相关性 + 项目使用情况进行 AI 排序 |

**安装配置**：

```bash
# Local
npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

**Claude Code 配置（本地）**：

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

**Claude Code 配置（远程/HTTP）**：

```bash
claude mcp add --transport http --header "CONTEXT7_API_KEY: YOUR_API_KEY" \
  context7 https://mcp.context7.com/mcp
```

**使用示例**：

```
User: "Show me how to use Claude's streaming API with the Python SDK"

Claude: [Uses context7 search]

Result: Official Python SDK docs + example code for streaming
```

**质量评分**：**8.2/10** ⭐⭐⭐⭐

**局限**：

| 局限 | 变通方案 |
|------------|-----------|
| 库覆盖有限 | 对冷门库回退到网络搜索 |
| 版本滞后（1-2 天） | 前沿内容使用官方仓库 |
| 幻觉风险（低但存在） | 与官方文档交叉验证 |

**替代方案**：

| 服务器 | 优势 | 劣势 |
|--------|-----------|--------------|
| **Context7** | 实时、特定版本 | 需要 API key |
| 网络搜索 | 全面、免费 | 慢、有幻觉风险 |
| 静态 RAG | 快速、本地 | 过时、无版本 |

**资源**：
- **GitHub**：https://github.com/upstash/context7
- **官方站点**：https://context7.com
- **LobeHub 注册表**：https://lobehub.com/mcp/upstash-context7

**ctx7 CLI 配套工具**：Context7 还附带一个 CLI（`npx ctx7`），可从终端处理 skill 发现和 MCP 设置。`ctx7 skills suggest` 会自动检测项目依赖并推荐匹配的 skills；`ctx7 setup --claude` 运行一个向导，自动配置 MCP 或 CLI+Skills 模式。完整工作流见 ultimate guide 的 §5.5。

---

### 项目管理

#### Linear MCP

**社区服务器**，用于 Linear（项目管理 SaaS）。基于 GraphQL API，提供 issue 管理、项目、团队、评论功能。

**使用场景**：Claude Code 自动在 Linear 中创建工单、更新状态、关联 issue（打通开发与项目管理之间的闭环）。

**核心特性**：

| 能力 | 详情 |
|------------|---------|
| Issue 管理 | 列出、获取、创建、更新、删除、搜索 |
| 项目 | 列出、创建、更新、分配 |
| 团队与用户 | 团队管理、成员分配 |
| 评论 | 添加、列出，带位置追踪 |
| Cycles | Sprint/cycle 管理 |
| Webhooks | 订阅 Linear 事件（可选） |

**安装配置**：

```bash
# NPM or uvx
npm install mcp-linear
# or
uvx mcp-linear
```

**Claude Code 配置**：

```bash
claude mcp add linear -- npx -y mcp-linear --api-key YOUR_LINEAR_API_KEY
```

**使用示例**：

```
User: "Create a bug ticket in Linear for the CSS layout issue I just found"

Claude: [Uses linear.issues.create with team key, title, description]

Result: Ticket created, issue ID returned

User: "Update ticket SOFT-123 status to 'In Progress'"

Claude: [Uses linear.issues.update]

Result: Status changed
```

**质量评分**：**7.6/10** ⭐⭐⭐⭐

**说明**：由社区维护（非 Linear Inc.），但活跃且文档完善。

**局限**：

| 局限 | 变通方案 |
|------------|-----------|
| 超时问题（1 小时后已修复） | 实现心跳、检查防火墙 |
| 65KB 字段限制 | 评论自动分块 |
| GraphQL 复杂度 | 自动拆分复杂查询 |

**替代方案**：

| 服务器 | 优势 | 劣势 |
|--------|-----------|--------------|
| **Linear MCP** | 现代 GraphQL、对初创团队友好 | 社区维护 |
| Jira MCP | 企业级、复杂工作流 | 更重、API 较旧 |
| GitHub Issues | 内置、免费 | 项目管理能力有限 |

**资源**：
- **GitHub**：https://github.com/tacticlaunch/mcp-linear
- **Linear API**：https://developers.linear.app
- **文档**：https://jan.ai/docs/desktop/mcp-examples/productivity/linear

---

### 编排

#### MCP-Compose

**社区工具**，以 Docker Compose 风格管理多个 MCP 服务器。声明式 YAML 配置，支持多传输方式（STDIO/HTTP/SSE）。

**使用场景**：开发者需要 5+ 个 MCP 服务器；类 Docker Compose 的配置简化了生命周期管理。

**核心特性**：

| 能力 | 详情 |
|------------|---------|
| YAML 配置 | Docker Compose 风格的服务器定义 |
| 多传输 | 支持 STDIO、HTTP、SSE、TCP |
| 容器运行时 | Docker、Podman、原生进程 |
| 网络管理 | 自动创建 Docker 网络 |
| 健康监控 | 连接池、会话管理 |
| HTTP 代理 | 单一统一 HTTP 端点 |
| 热重载 | 无需重启即可更新配置 |

**安装配置**：

```bash
git clone https://github.com/phildougherty/mcp-compose
cd mcp-compose
cargo build --release
```

**配置**（`mcp-compose.yaml`）：

```yaml
version: "1.0"
mcpServers:
  filesystem:
    command: npx
    args:
      - "@modelcontextprotocol/server-filesystem"
      - "/tmp"
    transport: stdio

  memory:
    command: npx
    args:
      - "@modelcontextprotocol/server-memory"
    transport: stdio
    env:
      DEBUG: "true"

  postgres:
    image: postgres:15
    transport: tcp
    port: 5432
    env:
      POSTGRES_PASSWORD: secret

proxy:
  port: 3000
  listen: "127.0.0.1"
```

**生成 Claude Desktop 配置**：

```bash
./mcp-compose create-config --type claude --output ~/.claude.json
```

**启动服务器**：

```bash
./mcp-compose up
# Single unified HTTP proxy at http://localhost:3000
```

**质量评分**：**7.4/10** ⭐⭐⭐⭐

**局限**：

| 局限 | 变通方案 |
|------------|-----------|
| 需要 Cargo 构建 | 使用预构建二进制（如有） |
| YAML 学习曲线 | 为常见配置提供模板 |
| 调试复杂度 | 使用 mcp-compose logs 排查问题 |

**资源**：
- **GitHub**：https://github.com/phildougherty/mcp-compose
- **Docker Compose 文档**：https://docs.docker.com/compose/
- **MCP 协议规范**：https://modelcontextprotocol.io

---

#### Packmind

**社区工具**，用于将工程规范作为 AI 上下文分发到多个 agent 和仓库。它暴露一个 MCP 服务器，可直接从 Claude Code（或任何支持 MCP 的 agent）创建和管理 playbook 规范。

**使用场景**：工程团队维护一份 playbook；Packmind MCP 服务器让 Claude Code 在会话期间无需离开编辑器即可提议新规范或更新现有规范。

**核心特性**：

| 能力 | 详情 |
|------------|---------|
| 规范创建 | 通过 MCP 工具创建/更新 playbook 条目 |
| 多 agent 输出 | 从单一来源生成 CLAUDE.md、.cursor/rules、Copilot instructions |
| 知识摄取 | 通过 GitHub、Slack、Jira、GitLab、Confluence、Notion 各自的 MCP 服务器拉取上下文 |
| 自托管 | Docker/Kubernetes，Apache-2.0 许可的 CLI |

**资源**：
- **GitHub**：https://github.com/PackmindHub/packmind
- **演示用例**：https://github.com/PackmindHub/demo-use-case-skills

> **交叉引用**：完整工具评估见 [third-party-tools.md — Engineering Standards Distribution](./third-party-tools.md#engineering-standards-distribution)。

---

## 生产环境部署

### 安全检查清单

- [ ] **API keys** 存储在 `.env` 中，而非配置文件里
- [ ] **RBAC/权限**已审查（尤其是 Kubernetes、Semgrep）
- [ ] 已理解 **速率限制**（Linear GraphQL 复杂度、Vercel API）
- [ ] 已实现针对 API 宕机的 **回退机制**
- [ ] 已为所有 MCP servers 启用 **监控 + 日志**

### 错误处理与可靠性

MCP 工具可能因多种原因失败，而你如何向 Claude 传达这些失败至关重要。协议提供了专门的机制：工具响应中的 `isError` 标志。

**`isError` 标志**

当工具调用失败时，应在响应中设置 `isError: true`，而不是抛出异常或返回伪装的成功结果。这会告知 Claude 调用失败了，并促使它决定下一步该做什么：重试、尝试不同的方法，或将问题反馈给用户。

```json
{
  "content": [
    {
      "type": "text",
      "text": "Database connection refused: ECONNREFUSED 127.0.0.1:5432"
    }
  ],
  "isError": true
}
```

如果没有 `isError: true`，Claude 可能会把错误信息当作数据，并在状态已损坏的情况下自信地继续执行。有了它，Claude 就能理解该步骤失败了，并对如何恢复进行推理。

**错误分类法：四个类别**

不同的失败类型需要不同的恢复策略。围绕这四个类别来组织你的错误信息，可以让 Claude 更容易选择正确的恢复操作：

| 类别 | 何时出现 | Claude 的预期响应 | 示例 |
|----------|------|---------------------------|---------|
| **瞬时性（Transient）** | 临时不可用、网络抖动、速率限制 | 延迟后重试 | `503 Service Unavailable`、超时 |
| **校验性（Validation）** | 输入错误——类型错误、字段缺失、格式错误 | 修正输入后立即重试 | `invalid date format: expected ISO8601` |
| **业务性（Business）** | 输入正确，但领域规则不允许该操作 | 上报或跳过 | `cannot delete: record has active dependencies` |
| **权限性（Permission）** | 调用方缺乏授权 | 停止并向用户解释 | `403 Forbidden: insufficient scope` |

**实现模式**

在错误信息中包含类别，让 Claude 无需猜测即可采取行动：

```python
def call_tool(params):
    try:
        result = execute(params)
        return {"content": [{"type": "text", "text": result}], "isError": False}
    except NetworkError as e:
        return {
            "content": [{"type": "text", "text": f"[transient] {e}. Retry in a few seconds."}],
            "isError": True
        }
    except ValidationError as e:
        return {
            "content": [{"type": "text", "text": f"[validation] {e}. Check the input format."}],
            "isError": True
        }
    except PermissionError as e:
        return {
            "content": [{"type": "text", "text": f"[permission] {e}. Cannot proceed without elevated access."}],
            "isError": True
        }
    except BusinessError as e:
        return {
            "content": [{"type": "text", "text": f"[business] {e}. Operation not permitted by domain rules."}],
            "isError": True
        }
```

瞬时性错误是唯一适合自动重试的类别。校验性错误应在修正输入后重试，而不是盲目重试。业务性和权限性错误应停止并反馈给用户，而非循环执行。

### 工具描述设计模式

工具描述是 MCP server 中影响最大的部分。Claude 依据它来决定调用哪个工具——而模糊或重叠的描述比任何其他设计错误都更容易导致路由错误。

**核心问题：重叠的描述导致路由错误**

两个描述听起来相似的工具会造成歧义。Claude 会从中选一个，而且常常前后不一致，因为它是在依据描述猜测哪个适用。

```json
// Bad — ambiguous, Claude will guess
{ "name": "analyze_content", "description": "Analyzes content" }
{ "name": "analyze_document", "description": "Analyzes document content" }

// Good — each description carves out a specific input type
{ "name": "analyze_content", "description": "Analyzes raw text strings or inline content (not files). Use for clipboard content, API responses, or text passed directly as a string." }
{ "name": "analyze_document", "description": "Analyzes content from a file path or URL. Use when the content lives on disk or at a remote endpoint, not when you already have the text in memory." }
```

检验标准：你能否仅凭描述就准确知道什么时候**不**该用这个工具？如果不能，就把边界补上。

**描述的结构剖析**

一个好的工具描述包含三部分，按以下顺序排列：

1. **它做什么**——一句话，现在时，动作动词
2. **它接收什么**——关键的输入类型或约束（文件路径还是字符串、单个还是批量）
3. **何时使用它而非相似工具**——明确陈述的决策边界

```json
{
  "name": "search_codebase",
  "description": "Searches source code files by regex pattern across the repository. Use for finding symbol definitions, function calls, and string literals in code. Not for searching documentation, configs, or prose — use search_docs for those."
}
```

**可防止路由错误的命名约定**

| 模式 | 示例配对 | 为何有效 |
|---------|-------------|--------------|
| 动词区分意图 | `get_user` vs `search_users` | 按已知 ID 获取 vs 按条件发现 |
| 名词区分输入类型 | `analyze_file` vs `analyze_text` | 磁盘上的路径 vs 内联字符串 |
| 范围后缀 | `list_tickets` vs `list_project_tickets` | 全局 vs 限定范围 |
| 操作粒度 | `create_record` vs `bulk_create_records` | 单个 vs 批量 |

避免用同义词作为工具名——`fetch`、`get`、`retrieve` 对 Claude 而言意思都一样。对每个语义操作只选用一个动词系列。

**应避免的反模式**

- **没有范围的泛化动词**：`process`、`handle`、`manage` 完全没有告诉 Claude 何时该调用该工具
- **缺少边界**："Searches the database"——哪个数据库？整个数据库？某个特定的表？
- **改变语义的布尔标志**：一个根据某个标志做完全不同事情的工具应当拆成两个工具
- **超过 3 句话的描述**：如果你需要更多，那这个工具做的事太多了

**`input_examples` 作为补充**

当 schema 不足以表达哪些参数组合是有效或典型的时，可添加 `input_examples`（Anthropic API 自 2026 年 2 月起支持）。它们向 Claude 展示具体的用法模式，对可选参数尤其有用：

```json
{
  "name": "create_ticket",
  "input_examples": [
    { "title": "Login page 500 error", "priority": "critical", "assignee": "oncall" },
    { "title": "Add dark mode toggle", "priority": "low" },
    { "title": "Update API docs for v2.1" }
  ]
}
```

示例能教会描述无法表达的东西：`assignee` 仅在关键项时才设置，而 `priority` 对于日常任务可以省略。

---

## 进阶 MCP 工具设计

除了基本的错误分类法之外，还有三个设计决策会显著影响 Claude 在生产环境中如何使用 MCP 工具：错误响应语义、Resources 与 Tools 的区别，以及工具命名。

---

### isRetryable：应用层约定

MCP 规范在错误响应 schema 中并未包含 `isRetryable` 字段。然而，在 `structuredContent` 中嵌入重试指引的约定，已成为那些调用易失败外部服务的工具的一种实用模式。

```json
{
    "isError": true,
    "content": [
        {
            "type": "text",
            "text": "Database query timed out after 30s. Retrying with the same parameters is likely to succeed."
        }
    ],
    "structuredContent": {
        "error": {
            "code": "DATABASE_TIMEOUT",
            "message": "Query timed out",
            "isRetryable": true,
            "retryAfterMs": 5000,
            "suggestedAction": "Retry the same query after 5 seconds"
        }
    }
}
```

对于不可重试的错误：

```json
{
    "isError": true,
    "content": [
        {
            "type": "text",
            "text": "Record not found. No record with ID 'usr_99999' exists in the database."
        }
    ],
    "structuredContent": {
        "error": {
            "code": "RECORD_NOT_FOUND",
            "message": "No record found for ID: usr_99999",
            "isRetryable": false,
            "suggestedAction": "Verify the ID is correct before retrying"
        }
    }
}
```

`isRetryable` 标志并不是 Claude 从 MCP 规范中原生读取的东西。它由你的编排层读取，由该层决定是重试还是上报。这个模式之所以有效，是因为 `structuredContent` 是机器可读的，你的代码可以在 Claude 之前先检查它。

---

### isError: false + 空内容 vs isError: true

这两种响应形态具有完全不同的语义。混淆它们会导致难以调试的静默失败。

| 响应 | 含义 |
|---|---|
| `isError: false` + 非空内容 | 工具成功，这是结果 |
| `isError: false` + 空内容 | 工具成功，但未找到任何结果（合法的空状态） |
| `isError: true` | 工具失败：操作无法完成 |

```json
// Search returning no results: NOT an error
{
    "isError": false,
    "content": [
        {
            "type": "text",
            "text": "No documents found matching query: 'quarterly report Q5 2024'"
        }
    ]
}

// Search that failed to execute: IS an error
{
    "isError": true,
    "content": [
        {
            "type": "text",
            "text": "Search service unavailable. Could not execute query."
        }
    ]
}
```

当搜索返回零结果时，Claude 应将此情况告知用户，并可能尝试不同的检索词。当搜索执行失败时，Claude 应报告工具失败，编排器应考虑重试或上报。这两条路径会分叉，而只有正确的错误语义才能让它们正确地分叉。

---

### MCP Resources vs Tools

Resources 和 Tools 用途不同，并由不同的角色控制。混淆它们会导致工具无法被索引、资源无法被参数化。

| 维度 | Resources | Tools |
|---|---|---|
| 谁控制访问 | 应用（预定义，非模型发起） | 模型（在对话中按需调用） |
| 参数 | 无（通过 URI 读取） | 完整的参数 schema |
| 用例 | 只读数据目录：配置文件、参考数据、文档 | 参数化操作：搜索、计算、写入、API 调用 |
| 发现方式 | 在启动时列出，可浏览 | 在系统提示中描述，按需调用 |
| 副作用 | 无（按约定为只读） | 允许 |
| 示例 | 公司政策文档 | `search_policy_documents(query, date_range)` |

```python
# Resource: static reference data, application-controlled
@server.list_resources()
async def list_resources():
    return [
        Resource(
            uri="config://database/schema",
            name="Database Schema",
            description="Current production database schema",
            mimeType="application/json"
        ),
        Resource(
            uri="docs://api/reference",
            name="API Reference",
            description="Internal API documentation",
            mimeType="text/markdown"
        )
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "config://database/schema":
        return json.dumps(get_current_schema())
    elif uri == "docs://api/reference":
        return read_file("docs/api-reference.md")
    raise ValueError(f"Unknown resource: {uri}")

# Tool: parameterized operation, model-controlled
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="search_database",
            description="Search the database with a structured query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "table": {"type": "string"},
                    "limit": {"type": "integer", "default": 10}
                },
                "required": ["query", "table"]
            }
        )
    ]
```

**ResourceLink 桥接：** 当工具返回的是对某个资源的引用（而非内联内容）时，使用 ResourceLink：

```json
{
    "isError": false,
    "content": [
        {
            "type": "resource",
            "resource": {
                "uri": "docs://reports/Q3-2024",
                "mimeType": "application/pdf",
                "text": "Q3 2024 Financial Report (use read_resource to access full content)"
            }
        }
    ]
}
```

---

### 工具命名与系统提示冲突

如果工具名以关键词的形式出现在系统提示中，会导致 Claude 把该工具与不相关的指令关联起来。一个名为 `process` 的工具，会在心理上与系统提示中出现的任何 "process" 一词产生关联，从而造成不可预测的激活模式。

工具命名规则：
- 使用具体的复合名称：用 `search_customer_records` 而非 `search`
- 避免会出现在系统提示中的泛化动词：`run`、`process`、`execute`、`handle`、`manage`
- 使用下划线，而非 camelCase 或连字符（MCP 约定）
- 当工具很多时，以领域为前缀：`crm_get_contact`、`crm_update_contact`、`crm_search`

```python
# Bad: generic names that conflict with system prompt keywords
tools = ["search", "process", "run", "execute", "get", "update"]

# Good: specific compound names with domain prefix
tools = [
    "crm_search_contacts",
    "crm_get_contact_by_id",
    "crm_update_contact_status",
    "billing_create_invoice",
    "billing_get_invoice_status"
]
```

---

### 任务范围工具配置（Task-Scoped Tool Profiles）

向每一次 agent 调用都提供所有可用工具，既浪费，又会增加在只读阶段发生意外写入的风险。任务范围工具配置会根据当前任务阶段限制可用的工具。

```python
TOOL_PROFILES = {
    "exploration": [
        "search_documents",
        "get_document_by_id",
        "list_categories",
        "read_config"
    ],
    "analysis": [
        "search_documents",
        "get_document_by_id",
        "calculate_metrics",
        "compare_versions"
    ],
    "execution": [
        "create_document",
        "update_document",
        "delete_document",
        "send_notification"
    ]
}

def get_tools_for_phase(phase: str) -> list[str]:
    return TOOL_PROFILES.get(phase, TOOL_PROFILES["exploration"])
```

探索（exploration）配置是只读的。执行（execution）配置增加了写操作。Claude 不可能在分析阶段意外调用 `delete_document`，因为该工具根本不在这次调用中出现。

对于不同用户角色可访问不同工具的多角色系统，应在角色层级进行范围限定，而非在调用后再过滤：

```python
ROLE_TOOL_ACCESS = {
    "viewer": ["search_documents", "get_document_by_id"],
    "editor": ["search_documents", "get_document_by_id", "create_document", "update_document"],
    "admin": ["*"]  # all tools
}

def get_tools_for_role(role: str, all_tools: list) -> list:
    if role == "admin":
        return all_tools
    allowed = ROLE_TOOL_ACCESS.get(role, [])
    return [t for t in all_tools if t.name in allowed]
```

范围限定访问对 `verify_fact` 工具模式尤其有价值：一个只需验证单条声明的 subagent，可以只被赋予 `verify_fact`，既降低了延迟（需要在上下文中描述的工具更少），也降低了风险（范围内没有写工具）。

---

### 快速上手技术栈

**MVP（必备）**：

1. **Playwright MCP** —— E2E 测试、Web 验证
2. **Semgrep MCP** —— 安全优先的编码

**重要补充**：

3. **Context7 MCP** —— API 参考准确性
4. **Linear MCP**（可选）—— 问题追踪集成

**DevOps/SRE 技术栈**：

5. **Kubernetes MCP** —— 集群管理
6. **Vercel MCP** —— Next.js 部署自动化

**复杂配置**：

7. **MCP-Compose** —— 多 server 编排
8. **Browserbase MCP** —— 重度 Web 自动化（付费）

### 安装示例

```bash
# Playwright (browser testing)
npm install @microsoft/playwright-mcp

# Semgrep (security)
uvx semgrep-mcp

# Context7 (documentation)
npx -y @upstash/context7-mcp --api-key YOUR_API_KEY

# Linear (project management)
npm install mcp-linear
```

### 性能指标

| 指标 | 中位数 | 范围 | 说明 |
|--------|--------|-------|-------|
| **响应时间** | ~200ms | 100-500ms | 取决于云端（Browserbase ~500ms） |
| **Token 开销** | ~200-500 tokens | 结构化输出时极小 | 可访问性树 vs 截图 |
| **配置时间** | ~5 分钟 | 2-10 分钟 | Cargo 构建（MCP-Compose）= 10 分钟 |

---

## 每月监测方法论

本节记录了通过每月生态系统更新来维护本指南的流程。

### 需要监测的来源

**官方来源**：
- [Anthropic MCP GitHub](https://github.com/modelcontextprotocol/servers)
- [Anthropic 博客](https://www.anthropic.com/news)
- [MCP Protocol Spec](https://modelcontextprotocol.io)

**社区来源**：
- [GitHub topic: mcp-servers](https://github.com/topics/mcp-servers)（7260+ 个服务器）
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)（75.5k stars）
- [MCP Registry](https://github.blog/ai-and-ml/generative-ai/how-to-find-install-and-manage-mcp-servers-with-the-github-mcp-registry/)

**讨论**：
- [Reddit r/ClaudeAI](https://www.reddit.com/r/ClaudeAI/)
- [Reddit r/mcp](https://www.reddit.com/r/mcp/)
- [X/Twitter #MCPServer](https://twitter.com/search?q=%23MCPServer)

**技术文章**：
- [Blog Skyvia](https://blog.skyvia.com/best-mcp-servers/)
- [Builder.io Blog](https://www.builder.io/blog/best-mcp-servers-2026)
- [Cyberpress](https://cyberpress.org/best-mcp-servers/)

### 每月评审清单

- [ ] **官方服务器**：检查 Anthropic GitHub 是否有新发布
- [ ] **社区服务器**：审查 GitHub topics 中的热门服务器（≥50 stars，发布时间 <3 个月）
- [ ] **生态系统变更**：关注 Anthropic 博客的协议更新
- [ ] **服务器健康度**：重新评估现有服务器（发布情况、issues、维护状态）
- [ ] **安全性**：检查已披露的漏洞（GitHub Security Advisories）
- [ ] **弃用情况**：识别已归档或无人维护的服务器
- [ ] **更新指南**：添加经过验证的新服务器，移除已弃用的服务器

### 评估模板

针对每个候选服务器：

1. **基础验证**：
   - GitHub stars ≥50？
   - 最近一次发布 <3 个月？
   - 文档是否完整（README + 示例 + 配置）？
   - 是否有测试/CI？

2. **质量评分**（参见 [评估框架](#evaluation-framework)）：
   - 维护：`/10`
   - 文档：`/10`
   - 测试：`/10`
   - 性能：`/10`
   - 采用度：`/10`
   - **总分**：`/50` → 归一化为 `/10`

3. **用例分析**：
   - 它填补了什么空白？
   - 是否已经被官方服务器覆盖？
   - 有哪些替代方案？

4. **决策**：
   - **集成**（得分 ≥8）：在指南中添加完整章节
   - **监测**（得分 6-7）：加入 [监测列表](../../docs/resource-evaluations/watch-list.md)，下个月重新评估
   - **拒绝**（得分 <6）：在 [被排除的服务器](#excluded-servers) 中记录原因

### 集成工作流

添加新服务器时：

1. 在合适的类别（浏览器自动化、DevOps 等）中创建章节
2. 包含：
   - 用例描述
   - 关键特性表
   - 安装说明
   - 配置示例
   - 质量评分
   - 局限性与变通方案
   - 替代方案对比
   - 资源（GitHub、文档、教程）
3. 如果与 MVP 相关，更新 [快速上手技术栈](#quick-start-stack)
4. 如果涉及安全关键问题，更新 [生产部署](#production-deployment) 清单

---

## 为 Claude 编写 MCP 文档：参考文件模式

当你将一个 MCP 服务器集成进 skill 时，Claude 必须自行摸索出查询语法、必需的参数组合以及各种古怪的行为。对于简单的 MCP，这没什么问题。但对于任何面向生产的场景（可观测性工具、项目管理 API、日志聚合器），这种方式很快就会失效。Claude 会猜测参数格式，得到一个晦涩的错误，再用另一种猜测重试，最后把你的预算消耗在无意义的噪音上。

来自 Packmind 工程团队的解决方案（以 Apache 2.0 协议开源）：在 skill 旁边添加一个 `references/<mcp-name>.md` 文件，并让 skill 在任何 MCP 调用之前，将读取该文件作为第一步。

### 参考文件中应包含哪些内容

三类 Claude 无法可靠地自行推断出的内容：

**1. 与工具名称不一致的参数语义**

例如，某个 Datadog 的 "search" 工具使用的是 Datadog 查询语法（而非正则表达式）。又或者某个 Sentry 工具需要一个 `organization_slug`（URL 中的 slug，而非显示名称）。这些并不是 MCP 的 bug，只是不够直观而已。

**2. 已知的错误模式及其触发条件**

例如："如果你在 DDSQL 中对 `GROUP BY` 使用 `SELECT` 别名，会得到一个晦涩的错误。请改为重复完整的表达式。" 这能把一次 10 分钟的调试过程变成一次零秒的查阅。

**3. 覆盖 80% 场景的可用查询示例**

可以复制粘贴的示例，覆盖最常见的查询。Claude 可以在此基础上改写，而无需从头构造。

### 文件结构

```
.claude/skills/my-mcp-skill/
├── SKILL.md                    # Main skill file
└── references/
    └── <mcp-name>.md           # MCP reference file (this pattern)
```

SKILL.md 在其第一步中读取参考文件：

```markdown
## Step 1: Read the MCP Reference File

Before doing anything else, read `references/<mcp-name>.md`.
This contains the query syntax and known gotchas for this MCP.
Do not skip this step.
```

### 为什么这样有效

参考文件并不是给人看的文档。它是一种结构化的上下文注入。其中的每一条信息都会降低 Claude 发出畸形 MCP 调用的概率。做得好的话，它能消除由语法错误引起的重试循环，并让 skill 可靠到足以在无人监督的情况下按计划定时运行。

这种模式可以推广到任何具有非直观行为的 MCP：Datadog、Sentry、PagerDuty、Linear、Jira、Mixpanel、Posthog。如果某个 MCP 拥有查询语言、分页方面的怪癖，或带有不直观名称的必需参数，那么一个参考文件在第一次运行时就能收回成本。

### 可直接 Fork 的模板

一个完整演示该模式的模板 skill（带有 Sentry 示例）可在以下位置获取：

本仓库中的 `examples/skills/mcp-integration-reference/`

该模板包含：
- 采用 5 步结构（读取参考、收集范围、抓取、分析、报告）的 `SKILL.md`
- `references/sentry-mcp.md`，包含完整的参数文档、注意事项、查询示例以及噪音排除列表
- 适配任何 MCP 服务器的说明

> 灵感来自 [Packmind 开源仓库](https://github.com/packmind/packmind) 中的 Datadog MCP 参考文件（Apache 2.0，Cédric Teyton）。完整署名参见 [Credits](../core/credits.md)。

---

## 被排除的服务器

已评估但未纳入验证列表的服务器：

| 服务器 | 原因 | 来源 | 评估日期 |
|--------|--------|--------|----------------|
| **X/Twitter MCP** | API 不稳定，频繁出现认证问题，维护不一致 | [Cursor Forum](https://forum.cursor.com/t/linear-mcp-commonly-errors-out-and-requires-turning-off-then-on/148816) | 2026 年 1 月 |
| **Vector Search MCP** | <50 stars，文档不完整 | [LobeHub](https://lobehub.com/mcp/hugoduncan-mcp-vector-search) | 2026 年 1 月 |
| **GitHub MCP** | 已归档，迁移至官方 Go SDK | [GitHub Changelog](https://github.blog/changelog/2025-12-10-the-github-mcp-server-adds-support-for-tool-specific-configuration-and-more/) | 2026 年 1 月 |
| **Jira MCP (sooperset)** | 近期无发布（最后一次：2025 年 6 月），稳定性不如 Linear | [GitHub Releases](https://github.com/sooperset/mcp-atlassian/releases) | 2026 年 1 月 |

---

## 统计与洞察

### 按类别分布

| 类别 | 服务器 | 用例 |
|----------|---------|-----------|
| **浏览器自动化** | 3 个（Playwright、Browserbase、Chrome DevTools） | 测试、调试、数据提取 |
| **DevOps/基础设施** | 3 个（Vercel、Kubernetes、Sentry） | 部署、集群管理、可观测性 |
| **安全/代码分析** | 1 个（Semgrep） | 漏洞扫描、安全编码 |
| **代码搜索/分析** | 1 个（Grepai） | 语义搜索、调用图分析 |
| **文档/知识** | 1 个（Context7） | API 参考、代码示例 |
| **项目管理** | 1 个（Linear） | issue 跟踪、sprint 规划 |
| **编排** | 1 个（MCP-Compose） | 多服务器管理 |

### 维护者类型

- **官方服务器**（6 个）：Playwright（Microsoft）、Browserbase、Semgrep、Context7、Kubernetes（Red Hat）、Chrome DevTools（Anthropic）
- **社区服务器**（4 个）：Linear、Vercel、MCP-Compose、Grepai（设计精良，积极维护）

---

**最后更新**：2026 年 5 月
**下次评审**：2026 年 6 月
**维护者**：Claude Code Ultimate Guide 团队

---

*返回 [主指南](../ultimate-guide.md) | [README](../README.md)*
