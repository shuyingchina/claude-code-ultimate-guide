---
title: "Data Privacy & Retention Guide"
description: "What data Claude Code sends to Anthropic servers and how to protect sensitive information"
tags: [privacy, security, guide]
---

# 数据隐私与保留指南

> **关键**：你与 Claude Code 分享的一切都会被发送到 Anthropic 服务器。本指南解释哪些数据会离开你的机器，以及如何保护敏感信息。

## TL;DR——保留策略概览

| 配置 | 保留期限 | 是否用于训练 | 如何启用 |
|---------------|------------------|----------|---------------|
| **消费者版（默认）** | 5 年 | 是 | （默认状态） |
| **消费者版（退出）** | 30 天 | 否 | [claude.ai/settings](https://claude.ai/settings/data-privacy-controls) |
| **Team / Enterprise / API** | 30 天 | 否（默认） | 使用 Team、Enterprise 计划或 API 密钥 |
| **ZDR（零数据保留）** | 服务端 0 天 | 否 | 适当配置的 API 密钥 |

**立即行动**：[禁用训练数据使用](https://claude.ai/settings/data-privacy-controls)，将保留期限从 5 年缩短到 30 天。

---

## 1. 理解数据流向

### 哪些数据会离开你的机器

当你使用 Claude Code 时，以下数据会被发送到 Anthropic：

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR LOCAL MACHINE                       │
├─────────────────────────────────────────────────────────────┤
│  • Prompts you type                                         │
│  • Files Claude reads (including .env if not excluded!)     │
│  • MCP server results (SQL queries, API responses)          │
│  • Bash command outputs                                     │
│  • Error messages and stack traces                          │
└───────────┬──────────────────┬──────────────┬───────────────┘
            │                  │              │
            ▼ HTTPS/TLS       ▼ HTTPS        ▼ HTTPS
┌───────────────────┐ ┌──────────────┐ ┌─────────────────────┐
│   ANTHROPIC API   │ │   STATSIG    │ │       SENTRY        │
├───────────────────┤ ├──────────────┤ ├─────────────────────┤
│ • Your prompts    │ │ • Latency,   │ │ • Error logs        │
│ • Model responses │ │   reliability│ │ • No code or        │
│ • Retention per   │ │ • No code or │ │   file paths        │
│   your tier       │ │   file paths │ │                     │
└───────────────────┘ └──────────────┘ └─────────────────────┘
                       (opt-out:        (opt-out:
                       DISABLE_         DISABLE_ERROR_
                       TELEMETRY=1)     REPORTING=1)
```

### 这在实践中意味着什么

| 场景 | 发送到 Anthropic 的数据 |
|----------|------------------------|
| 你要求 Claude 读取 `src/app.ts` | 完整文件内容 |
| 你通过 Claude 运行 `git status` | 命令输出 |
| MCP 执行 `SELECT * FROM users` | 包含用户数据的查询结果 |
| Claude 读取 `.env` 文件 | API 密钥、密码、机密信息 |
| 你的代码中发生错误 | 包含路径的完整堆栈跟踪 |

---

## 2. Anthropic 保留策略

### 第 1 档：消费者版默认（启用训练）

- **保留**：5 年
- **用途**：模型改进、训练数据
- **适用于**：开启了训练设置的 Free、Pro、Max 计划

### 第 2 档：消费者版退出（禁用训练）

- **保留**：30 天
- **用途**：仅用于安全监控、滥用防护
- **如何启用**：
  1. 前往 https://claude.ai/settings/data-privacy-controls
  2. 禁用 "Allow model training on your conversations"
  3. 更改立即生效

### 第 3 档：商业版（Team / Enterprise / API）

- **保留**：30 天
- **用途**：仅用于安全监控、滥用防护
- **训练**：默认不用于训练（无需退出）
- **适用于**：Team 计划、Enterprise 计划、API 用户、第三方平台、Claude Gov

### 第 4 档：零数据保留（ZDR）

- **保留**：服务端 0 天（本地客户端缓存可能保留长达 30 天）
- **用途**：在 Anthropic 服务器上不保留任何内容
- **要求**：适当配置的 API 密钥（参见 [Anthropic 文档](https://www.anthropic.com/enterprise)）
- **使用场景**：HIPAA（需要单独签署 BAA）、GDPR、PCI-DSS 合规、政府合同

> **重要**：数据在传输过程中通过 TLS 加密，但在 Anthropic 服务器上**静态存储时不加密**。请在安全评估中将此因素考虑在内。

---

## 3. 已知风险

### 风险 1：自动读取文件

Claude Code 会读取文件以理解上下文。默认情况下，这包括：

- `.env` 和 `.env.local` 文件（API 密钥、密码）
- `credentials.json`、`secrets.yaml`（服务账户）
- 工作区范围内的 SSH 密钥
- 数据库连接字符串

**缓解措施**：配置 `excludePatterns`（参见第 4 节）。

### 风险 2：MCP 数据库访问

当你配置数据库 MCP 服务器（Neon、Supabase、PlanetScale）时：

```
Your Query: "Show me recent orders"
            ↓
MCP Executes: SELECT * FROM orders LIMIT 100
            ↓
Results Sent: 100 rows with customer names, emails, addresses
            ↓
Stored at Anthropic: According to your retention tier
```

**缓解措施**：切勿连接生产数据库。使用带匿名化数据的开发/预发布环境。

### 风险 3：Shell 命令输出

Bash 命令及其输出会被包含在上下文中：

```bash
# This output goes to Anthropic:
$ env | grep API
OPENAI_API_KEY=sk-abc123...
STRIPE_SECRET_KEY=sk_live_...
```

**缓解措施**：使用 hooks 过滤敏感的命令输出。

### 风险 4：`/bug` 命令会发送所有内容（保留 5 年）

当你在 Claude Code 中运行 `/bug` 时，你的**完整对话历史**（包括所有代码、文件内容以及可能的机密信息）会被发送到 Anthropic 用于缺陷分类。这些数据会保留 **5 年**，无论你是否退出了训练设置。

这独立于你的隐私偏好：即使禁用了训练并采用 30 天保留期，缺陷报告也遵循其自有的 5 年保留策略。

**缓解措施**：如果你处理敏感代码库，请完全禁用该命令：

```bash
export DISABLE_BUG_COMMAND=1
```

或者将其添加到你的 shell 配置文件（`~/.zshrc`、`~/.bashrc`）以使其永久生效。

### 风险 5：已记录的社区事件

| 事件 | 来源 |
|----------|--------|
| Claude 默认读取 `.env` | r/ClaudeAI、GitHub issues |
| 在配置不当的 MCP 上尝试 DROP TABLE | r/ClaudeAI |
| 凭据通过环境变量泄露 | GitHub issues |
| 通过恶意 MCP 服务器进行提示词注入 | r/programming |

### 风险 6：Claude Desktop 浏览器集成——静默安装 Native Messaging Host

Claude Desktop 会将 native messaging host 清单文件安装到浏览器的 `NativeMessagingHosts` 目录中，以启用其 "Claude in Chrome" 功能。截至 2026 年 4 月，这一行为在没有向用户明确征求同意提示的情况下发生。

**安装的内容：**

```
~/Library/Application Support/Google/Chrome/NativeMessagingHosts/
  com.anthropic.claude_browser_extension.json

/Applications/Claude.app/Contents/MacOS/
  claude_browser_native_host  (helper binary)
```

Claude Desktop 会将这些文件写入**系统上找到的所有基于 Chromium 的浏览器**——Chrome、Brave、Edge、Arc、Vivaldi、Opera、Chromium——包括在 Claude Desktop 安装时尚未安装的浏览器。Claude Desktop 偏好设置中的 "Don't ask" 退出选项并不能可靠地阻止这一行为（[GitHub #53864](https://github.com/anthropics/claude-code/issues/53864)，2026 年 4 月）。

**native messaging 实际做什么（以及不做什么）：**

Native messaging 是一种标准的 Chrome 机制，被密码管理器、VPN 以及许多其他合法应用使用。native host 只能接收由明确以它为目标的 Chrome 扩展发送的消息。它无法主动向浏览器发起连接、读取标签页或未经请求地访问浏览器数据。这在架构上与间谍软件不同。

真正的问题在于**同意机制的缺失**，而非机制本身。一个应用静默修改另一家厂商的应用目录，无论出于何种意图，都违反了最小惊讶原则。

**如果你有顾虑，应检查什么：**

```bash
# List all native messaging hosts installed for Chrome
ls ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/

# Check if Anthropic's host is present
cat ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_browser_extension.json

# Check other browsers
ls ~/Library/Application\ Support/BraveSoftware/Brave-Browser/NativeMessagingHosts/
ls ~/Library/Application\ Support/Microsoft\ Edge/NativeMessagingHosts/
```

**如何移除：**

```bash
# Remove from Chrome (repeat for each browser as needed)
rm ~/Library/Application\ Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_browser_extension.json

# Restart Chrome after deletion
```

卸载 Claude Desktop 会移除 helper binary，但在某些浏览器目录中可能会遗留过时的清单文件。清理后请重启受影响的浏览器。

**与 Claude Code 的冲突：** 当 Claude Desktop 和 Claude Code CLI 都已安装时，Chrome 扩展始终绑定到 Claude Desktop 的 native host，导致 Claude Code 的 `claude-in-chrome` MCP 工具无法访问（[GitHub #51949](https://github.com/anthropics/claude-code/issues/51949)）。截至 2026 年 4 月，这是一个已知缺陷，除卸载 Claude Desktop 外没有其他变通方法。

**缓解措施：**

如果你不使用浏览器集成功能，可以安全地删除清单文件。Anthropic 尚未提供能够可靠阻止安装的官方退出机制。请关注 [GitHub #53864](https://github.com/anthropics/claude-code/issues/53864) 获取更新。

---

## 4. 防护措施

### 立即行动

#### 4.1 退出训练

1. 访问 https://claude.ai/settings/data-privacy-controls
2. 关闭 "Allow model training"
3. 数据保留时长从 5 年缩短至 30 天

#### 4.2 配置文件排除

在 `.claude/settings.json` 中，使用 `permissions.deny` 阻止对敏感文件的访问：

```json
{
  "permissions": {
    "deny": [
      "Read(./.env*)",
      "Edit(./.env*)",
      "Write(./.env*)",
      "Bash(cat .env*)",
      "Bash(head .env*)",
      "Read(./secrets/**)",
      "Read(./**/credentials*)",
      "Read(./**/*.pem)",
      "Read(./**/*.key)",
      "Read(./**/service-account*.json)"
    ]
  }
}
```

> **注意**：旧的 `excludePatterns` 和 `ignorePatterns` 设置已于 2025 年 10 月弃用。请改用 `permissions.deny`。

> **警告**：`permissions.deny` 存在[已知限制](./security-hardening.md#known-limitations-of-permissionsdeny)。为实现纵深防御，请将其与安全 hooks 及外部密钥管理相结合。

#### 4.3 使用安全 Hooks

创建 `.claude/hooks/PreToolUse.sh`：

```bash
#!/bin/bash
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool.name')

if [[ "$TOOL_NAME" == "Read" ]]; then
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool.input.file_path')

    # Block reading sensitive files
    if [[ "$FILE_PATH" =~ \.env|credentials|secrets|\.pem|\.key ]]; then
        echo "BLOCKED: Attempted to read sensitive file: $FILE_PATH" >&2
        exit 2  # Block the operation
    fi
fi
```

#### 4.4 退出遥测与错误上报

Claude Code 会连接第三方服务以收集运行指标（Statsig）和记录错误日志（Sentry）。这些数据不包含你的代码或文件路径，但你可以将其完全禁用：

| 变量 | 禁用内容 |
|----------|-----------------|
| `DISABLE_TELEMETRY=1` | Statsig 运行指标（延迟、可靠性、使用模式） |
| `DISABLE_ERROR_REPORTING=1` | Sentry 错误日志 |
| `DISABLE_BUG_COMMAND=1` | `/bug` 命令（防止发送完整对话历史） |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` | 一次性禁用所有非必要网络流量 |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` | 会话质量调查（注意：调查仅发送你的数字评分，绝不发送对话记录） |

将这些变量添加到你的 shell 配置文件中以永久生效：

```bash
# In ~/.zshrc or ~/.bashrc
export DISABLE_TELEMETRY=1
export DISABLE_ERROR_REPORTING=1
export DISABLE_BUG_COMMAND=1
```

> **注意**：使用 Bedrock、Vertex 或 Foundry 提供商时，所有非必要流量（遥测、错误上报、bug 命令、调查）默认均被禁用。

### MCP 最佳实践

| 规则 | 理由 |
|------|-----------|
| **绝不连接生产数据库** | 所有查询结果都会发送给 Anthropic |
| **使用只读数据库用户** | 防止 DROP/DELETE/UPDATE 意外操作 |
| **匿名化开发数据** | 降低 PII 泄露风险 |
| **创建最小化测试数据集** | 数据越少，风险越小 |
| **审计 MCP 服务器来源** | 第三方 MCP 可能存在漏洞 |

### 面向团队

| 环境 | 建议 |
|-------------|----------------|
| **开发** | 退出训练 + 文件排除 + 匿名化数据 |
| **预发布** | 若处理真实数据，考虑使用企业 API |
| **生产** | 绝不直接连接 Claude Code |

---

## 5. 与其他工具的对比

| 特性 | Claude Code + MCP | Cursor | GitHub Copilot |
|---------|-------------------|--------|----------------|
| 发送的数据范围 | 完整 SQL 结果、文件 | 代码片段 | 代码片段 |
| 生产数据库访问 | 是（通过 MCP） | 受限 | 并非为此设计 |
| 默认保留时长 | 5 年 | 不定 | 30 天 |
| 默认参与训练 | 是 | 需主动开启 | 需主动开启 |

**关键区别**：MCP 创造了独特的攻击面，因为 MCP 服务器是拥有独立网络/文件系统访问权限的独立进程。

---

## 6. 企业级考量

### 何时使用企业 API（ZDR）

- 处理 PII（姓名、邮箱、地址）
- 受监管行业（HIPAA、GDPR、PCI-DSS）
- 客户数据处理
- 政府合同
- 金融服务

### 评估清单

- [ ] 你的组织已制定数据分类策略
- [ ] API 层级与数据敏感度要求相匹配
- [ ] 团队已接受隐私控制培训
- [ ] 针对潜在数据泄露制定了事件响应计划
- [ ] 已完成法务/合规审查

---

## 7. 快速参考

### 链接

| 资源 | URL |
|----------|-----|
| 隐私设置 | https://claude.ai/settings/data-privacy-controls |
| Anthropic 使用政策 | https://www.anthropic.com/policies |
| 企业信息 | https://www.anthropic.com/enterprise |
| 服务条款 | https://www.anthropic.com/legal/consumer-terms |

### 命令

```bash
# Check current Claude config
claude /config

# Verify exclusions are loaded
claude /status

# Run privacy audit
./examples/scripts/audit-scan.sh
```

### 快速清单

- [ ] 已在 claude.ai/settings 启用退出训练
- [ ] 已通过 settings.json 中的 `permissions.deny` 阻止 `.env*` 文件
- [ ] 没有通过 MCP 连接生产数据库
- [ ] 已安装针对敏感文件访问的安全 hooks
- [ ] 团队已知晓数据流向 Anthropic 的情况

---

## 8. 知识产权考量

> **免责声明**：本节内容不构成法律建议。请就你的具体情况咨询合格的律师。

使用 AI 代码生成工具时，请与你的法务团队讨论以下要点：

| 考量 | 讨论内容 |
|---------------|-----------------|
| **所有权** | AI 生成代码的版权归属在大多数司法管辖区仍属法律未决问题 |
| **许可证污染** | 训练数据可能包含带有 copyleft 许可证（GPL、AGPL）的开源代码，这可能影响你的代码库 |
| **供应商赔偿** | 部分企业计划提供法律保护（例如 Microsoft Copilot Enterprise 包含知识产权赔偿） |
| **行业合规** | 受监管行业（医疗、金融、政府）可能有额外的知识产权要求 |

本指南聚焦于 Claude Code 的使用，而非法律策略。如需知识产权方面的指导，请咨询专业法律资源或你所在组织的法律顾问。

---

## 9. Claude 的治理与价值观

### Constitutional AI 框架

Anthropic 于 2026 年 1 月发布了 Claude 的章程（CC0 许可证——公有领域）。该文件定义了指导 Claude 行为的价值观层级：

**优先级顺序**（用于解决冲突）：

1. **广义安全** —— 绝不损害人类的监督与控制
2. **广义伦理** —— 诚实、避免伤害、行为端正
3. **Anthropic 合规** —— 内部准则与政策
4. **真正有用** —— 为用户和社会带来切实价值

### 这对 Claude Code 用户意味着什么

| 场景 | 预期行为 |
|----------|-------------------|
| 涉及安全敏感的请求 | Claude 将安全置于有用性之上（可能更为保守） |
| 处于边界的生物/化学问题 | 可能拒绝，或要求提供背景以评估安全影响 |
| 伦理冲突 | 将遵循层级：安全 > 伦理 > 合规 > 有用性 |

### 为何重要

- **训练数据来源**：章程被用于生成合成训练样本
- **行为规范**：作为参考文档，解释何为预期输出、何为意外输出
- **审计与治理**：为合规审查提供法律/伦理基础
- **你自己的 agents**：CC0 许可证允许为自定义模型复用/改编

### 资源

- 章程全文：https://www.anthropic.com/constitution
- PDF 版本：https://www-cdn.anthropic.com/.../claudes-constitution.pdf
- 公告：https://www.anthropic.com/news/claude-new-constitution
- 对齐研究：https://alignment.anthropic.com/

---

## 变更日志

- 2026-02：修正数据留存模型（从 3 层调整为 4 层），新增 /bug command 警告、遥测退出（opt-out）变量、静态加密披露，更新 ZDR 条件
- 2026-01：新增 Claude 的治理与宪法式 AI（constitutional AI）框架章节
- 2026-01：新增知识产权考量章节
- 2026-01：初始版本——记录数据留存政策与保护措施
