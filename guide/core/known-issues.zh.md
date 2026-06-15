---
title: "Known Issues & Critical Bugs"
description: "Verified critical issues affecting Claude Code users from community reports and official communications"
tags: [reference, security, debugging]
---

# 已知问题与严重 Bug

本文档基于社区报告和官方沟通，追踪影响 Claude Code 用户的已验证严重问题。

> **最后更新**：2026 年 4 月 23 日
> **来源**：[GitHub Issues](https://github.com/anthropics/claude-code/issues) + [Anthropic 官方沟通](https://www.anthropic.com/engineering)

---

## 🚨 活跃的严重问题

### 0. Prompt 缓存 Bug —— 隐性成本膨胀（2026 年 3 月至今）

**严重程度**：🔴 **高 —— 成本影响**
**状态**：⚠️ 部分修复（截至 v2.1.88，Bug 3 和 Bug 2 仍然活跃）
**问题**：[#40524](https://github.com/anthropics/claude-code/issues/40524)
**首次报告**：2026 年 3 月
**受影响版本**：v2.1.69+（Bug 2 和 3）、v2.1.36+ 独立二进制文件（Bug 1）

#### 问题

三个独立的 Bug 破坏了 Anthropic 基于前缀的 prompt 缓存，导致产生 `cache_creation` 费用
（全额 token 成本）而非 `cache_read`（折扣价）。实测的成本影响取决于使用模式：

- **仅 Bug 3（attribution header）**：在每次会话启动和每次 subagent 调用时，对约 12K token 的系统 prompt 造成 2-5 倍膨胀
- **Bug 2 活跃（resume + 10 个以上 skills）**：每次 resume 重建 87-118K token；有 3-4 次 resume 的会话实测 **缓存读取比为 4.3-34.6%**（健康状态为 95-99%），在最糟糕的会话中相当于 **每轮成本高出 10-20 倍**
- **综合效应**：应用临时方案后，缓存命中率从 48% 提升至 99.98%（社区实测，CC#40524）

> **依据**：通过社区逆向工程（CC#40524）、对泄露的 npm sourcemap 的源码分析，
> 以及独立的会话 JSONL 分析（ArkNill，2026 年 4 月）确认。Anthropic 在 v2.1.88 中
> 发布了部分修复（tool schema 字节）。Bug 2 和 3 仍未修补。

#### Bug 2 —— 在 --resume / --continue 时完全重建缓存（v2.1.69+）—— 高影响

**根本原因**：会话 JSONL 写入器在写入磁盘前剥离了 `deferred_tools_delta` 附件记录。
在 `--resume` 时这些记录已丢失 —— 因此 deferred tools 层没有先前的
公告历史，会从头重新公告所有工具。这使恢复对话中的每条消息位置都发生偏移，
彻底破坏了消息级别的缓存前缀。

**具体证据**（来自社区会话 JSONL 分析，含 14 个 skills 的会话）：

| 条目 | cache_read | cache_creation | 事件 |
|-------|-----------|----------------|-------|
| 102 | 84,164 | 174 | 正常轮次 |
| 103 | 0 | 87,176 | **Resume —— 完全重建** |
| 105 | 87,176 | 561 | 已恢复 |
| 166 | 115,989 | 221 | 正常轮次 |
| 167 | 0 | 118,523 | **Resume —— 完全重建** |

每次 resume = 87-118K token 被重建为 `cache_creation` 而非 `cache_read`。每个会话
3-4 次 resume = 30-40 万 token 的可避免成本。影响随 skills/deferred tools 的数量而扩大：
拥有 10 个以上 skills 的用户（框架配置中很常见）在每次 resume 时都会看到完全 0% 的缓存比。

**临时方案**：在修复发布前，避免使用 `--resume` 和 `--continue`。开启全新会话。
降级选项：`npm install -g @anthropic-ai/claude-code@2.1.68`（回归前的最后一个版本）。
Anthropic 正在内部追踪此问题（在源码遥测中引用为 `inc-4747`）。

**工程修复**：在写入会话 JSONL 时保留 `deferred_tools_delta` 和 `mcp_instructions_delta` 记录，
以便 resume 能够正确计算 delta，而非重新公告所有内容。

#### Bug 3 —— Attribution Header（低到中等影响，v2.1.69+）

**根本原因**：Claude Code 在每个 API 请求中将一个计费 header 注入为系统 prompt 的
**第一个块**。该 header 包含一个由你的第一条用户消息字符派生而来的 3 字符哈希，
使其在每个会话、每个 subagent 和每个旁路查询中都唯一。由于 Anthropic 的缓存是
基于前缀的，这个唯一的第一块会导致每次会话启动和 subagent 调用时，对约 12K token 的
系统 prompt 产生冷未命中。

**细微差别**（据原始逆向工程分析师 jmarianski 所述）：每会话的系统 prompt 冷未命中
在实践中影响"微乎其微"，因为系统 prompt 相对于整个会话上下文较小。
对于重度用户而言，resume bug（Bug 2）的可测量成本更大。

**实证测量**：应用临时方案后缓存命中率从 48% → 99.98% —— 但这反映的是与其他
缓存因素的综合效应；孤立的 Bug 3 影响可能更小。

**临时方案**（立即应用，风险低）：
```json
// ~/.claude/settings.json
{
  "env": {
    "CLAUDE_CODE_ATTRIBUTION_HEADER": "false"
  }
}
```
可接受的值：`"false"`、`"0"`、`"no"`、`"off"`。无需重启。

#### Bug 1 —— 哨兵字符串替换（独立二进制文件 v2.1.36+，边缘情况）

**根本原因**：Bun 的原生 HTTP 栈在序列化后替换请求体中的 `cch=00000` 占位符。
如果这个精确字符串出现在你的消息内容中（例如来自讨论此 bug 的 CLAUDE.md），
它可能在错误的位置被替换。

**临时方案**：不要在 CLAUDE.md 或配置文件中按字面粘贴 `cch=00000`。
注意：这仅影响独立二进制文件，不影响 npm/npx 安装。

#### 审计工具

运行 `/check-cache-bugs`（从 [examples/commands](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/examples/commands/check-cache-bugs.md) 目录安装）即可在约 20 秒内审计你的配置是否存在这全部三个 bug。

> **最佳实践**：在全新会话的最开始运行，或通过 `claude -p "$(cat .claude/commands/check-cache-bugs.md)"` 作为一次性命令运行，以避免用 `cch=` 字符串污染当前会话上下文（可能触发 Bug 1）。

#### 监控缓存健康状况

要验证你的会话是否健康，使用官方的 `ANTHROPIC_BASE_URL` 环境变量将流量路由通过一个透明的本地代理，并记录 API 响应中的 `cache_creation_input_tokens` / `cache_read_input_tokens`：

```json
// ~/.claude/settings.json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:8080"
  }
}
```

在 8080 端口运行一个透传代理，它读取但不修改请求/响应，从每个响应中解析 `usage` 对象。**健康的会话** 显示缓存读取比 > 80%；**受影响的会话** 显示 < 40%。

或者，直接检查 `~/.claude/projects/` 中的会话 JSONL 文件 —— 查看每轮的 `cache_creation_input_tokens` 和 `cache_read_input_tokens`。

用于监控的社区工具：
- [`cc-diag`](https://github.com/nicobailey/cc-diag) —— 基于 mitmproxy 的 Claude Code 流量分析
- [`claude-code-router`](https://github.com/pathintegral-institute/claude-code-router) —— 带日志记录的透明代理

社区补丁（同时应用 Bug 1 和 Bug 2 修复）：
- [`cc-cache-fix`](https://github.com/Rangizingo/cc-cache-fix) —— 社区开发的补丁 + 测试工具包

#### 官方回应

在 v2.1.88 中部分修复（tool schema 字节）。已确认 Bug 2 和 3 仍然活跃。

**追踪**：[Issue #40524](https://github.com/anthropics/claude-code/issues/40524)（自 2026 年 3 月起开放）

**相关问题**：[#40652](https://github.com/anthropics/claude-code/issues/40652)（cch= 计费哈希）· [#41663](https://github.com/anthropics/claude-code/issues/41663)（缓存 token 消耗）· [#41607](https://github.com/anthropics/claude-code/issues/41607)（重复的 compaction subagents）· [#41767](https://github.com/anthropics/claude-code/issues/41767)（v2.1.89 的 auto-compact 循环）· [#41750](https://github.com/anthropics/claude-code/issues/41750)（上下文管理每轮都触发）

---

### 1. GitHub Issue 在错误的仓库中被自动创建（2025 年 12 月至今）

**严重程度**：🔴 **严重 —— 安全/隐私风险**
**状态**：⚠️ 活跃（截至 2026 年 1 月 28 日）
**问题**：[#13797](https://github.com/anthropics/claude-code/issues/13797)
**首次报告**：2025 年 12 月 12 日
**受影响版本**：v2.0.65+

#### 问题

Claude Code **系统性地在公开的 `anthropics/claude-code` 仓库中创建 GitHub issue**，
而非用户的私有仓库，即使是在本地 git 仓库目录中工作时也是如此。

#### 影响

**高 —— 隐私/安全**：至少 **17 个以上确认案例** 中，用户意外地在公开仓库中暴露了敏感信息：

- 数据库 schema
- API 凭据和配置详情
- 基础设施架构
- 私有项目路线图
- 安全配置

#### 症状

- 创建的 issue 带有意外的 `--repo anthropics/claude-code` 标志
- 私有项目细节出现在公开的 anthropics/claude-code issues 中
- 在公开仓库中创建 issue 前没有确认提示
- 在本地 git 仓库中要求 Claude "创建一个 issue" 时发生

#### 意外创建的示例

近期确认的案例（2026 年 1 月）：
- [#20792](https://github.com/anthropics/claude-code/issues/20792)："Deleted - created in wrong repo"
- [#16483](https://github.com/anthropics/claude-code/issues/16483)、[#16476](https://github.com/anthropics/claude-code/issues/16476)："Claude OPENS ISSUES ON THE WRONG REPO"
- [#17899](https://github.com/anthropics/claude-code/issues/17899)："Claude Code suddenly decided to create issue in claude code repo"
- [#16464](https://github.com/anthropics/claude-code/issues/16464)："[Mistaken Post] Please delete"

完整列表：[搜索 "wrong repo" OR "delete this"](https://github.com/anthropics/claude-code/issues?q=is%3Aissue+%22wrong+repo%22+OR+%22delete+this%22)

#### 根本原因（假设）

Claude Code 可能混淆了：
- **关于 Claude Code 本身的合理反馈** → `anthropics/claude-code`（正确）
- **用户项目问题** → 当前仓库（应为默认）

该工具似乎将 `anthropics/claude-code` 硬编码或过度优先作为默认目标。

#### 临时方案

**🛡️ 通过 Claude Code 创建任何 GitHub issue 之前：**

1. **始终验证目标仓库**：
   ```bash
   # Check current repo
   git remote -v
   ```

2. **明确指定仓库**：
   ```bash
   gh issue create --repo YOUR_USERNAME/YOUR_REPO --title "..." --body "..."
   ```

3. 在执行前 **审查命令**：
   - 查找 `--repo anthropics/claude-code` 标志
   - 如果存在且不正确，中止并指定正确的仓库

4. 在 Claude 设置中对所有 `gh` 命令 **使用手动批准**

5. 在 bug 修复之前，**切勿在 issue 创建 prompt 中包含敏感信息**

#### 如果你受到影响

如果你意外创建了暴露敏感信息的 issue：

1. **立即联系 GitHub Support** 请求删除 issue（而非仅关闭）
2. **轮换任何已暴露的凭据**（API 密钥、密码、token）
3. 如涉及安全敏感信息，通过 [安全邮箱](mailto:security@anthropic.com) **向 Anthropic 报告**
4. **检查数据泄露**：监控已暴露信息的使用情况

#### 官方回应

截至 2026 年 1 月 28 日：**问题仍然开放**，无官方修复公告。

**追踪**：[Issue #13797](https://github.com/anthropics/claude-code/issues/13797)（自 2025 年 12 月 12 日起开放）

---

### 2. 过度的 Token 消耗（2026 年 1 月至今）

**严重程度**：🟠 **高 —— 成本影响**
**状态**：⚠️ 已报告（Anthropic 正在调查）
**问题**：[#16856](https://github.com/anthropics/claude-code/issues/16856)
**首次报告**：2026 年 1 月 8 日
**受影响版本**：v2.1.1+（已报告），可能影响更早版本

#### 问题

多名用户报告与之前版本相比 **token 消耗速度快 4 倍以上**，导致：
- 速率限制比正常情况快得多就被触及
- 相同的工作流消耗显著更多的 token
- 意外的成本增加

#### 症状

来自 Issue #16856：
> "Starting from today's morning with the updated to CC 2.1.1 - the usage is ridiculous. I am working on the same projects for months, same routines, same time. But today it hits 5h limits like 4+ times faster!"

常见报告：
- 每周限额在 1-2 天内耗尽（而正常为 5-7 天）
- 会话在 2-3 条消息后就达到 90% 上下文
- 相同操作的 token 消耗为 4-20 倍

#### 背景

**假日使用额度奖励到期**：2025 年 12 月 25-31 日，Anthropic 作为节日礼物将使用限额翻倍。当限额于 2026 年 1 月 1 日恢复正常时，用户感觉"容量缩减"。

然而，**报告在此时间点之后仍持续存在**，暗示存在潜在的底层问题。

#### Anthropic 回应

来自 [The Register](https://www.theregister.com/2026/01/05/claude_devs_usage_limits/)（2026 年 1 月 5 日）：
> "Anthropic stated it 'takes all such reports seriously but hasn't identified any flaw related to token usage' and indicated it had ruled out bugs in its inference stack."

**状态**：截至 2026 年 1 月 28 日，Anthropic **尚未正式确认为 bug**。

#### 相关问题

发现 20 个以上报告（2025 年 12 月 - 2026 年 1 月）：
- [#17687](https://github.com/anthropics/claude-code/issues/17687)："Unexpectedly high token consumption rate since January 2026"
- [#16073](https://github.com/anthropics/claude-code/issues/16073)："[Critical] Claude Code Quality Degradation - Ignoring Instructions, Excessive Token Usage"
- [#17252](https://github.com/anthropics/claude-code/issues/17252)："Excessive token consumption rate in session usage tracking"
- [#13536](https://github.com/anthropics/claude-code/issues/13536)："Excessive token usage on new session initialization"

[完整搜索](https://github.com/anthropics/claude-code/issues?q=is%3Aissue+excessive+token+created%3A2025-12-01..2026-01-28)

#### 临时方案

在 Anthropic 调查期间：

1. **主动监控 token 使用**：
   ```
   /context
   ```
   定期检查已使用 token 与容量的对比

2. **使用更短的会话**：
   - 在接近 50-60% 上下文时重启会话
   - 将复杂任务拆分为多个会话

3. **禁用 auto-compact**（可能有帮助）：
   ```bash
   claude config set autoCompaction false
   ```

4. 如不需要，**减少 MCP 工具**：
   - 审查 `~/.claude.json`（字段 `"mcpServers"`）
   - 禁用未使用的服务器

5. 对隔离的任务 **使用 subagents**：
   - Subagents 拥有独立的上下文窗口
   - 对复杂操作使用 Task 工具

6. **追踪你的使用模式**：
   - 对比版本升级前后
   - 记录异常峰值

#### 调查提示

如果遇到过度消耗：

1. 记下你的 **Claude Code 版本**：`claude --version`
2. **对比版本**：如有可用，用更早的稳定版本测试
3. **记录模式**：哪些操作触发了高使用量？
4. **附带数据报告**：在 issue 报告中包含版本、操作类型、token 计数

---

## ✅ 已解决的历史问题

### 三重 harness 事故：Effort、Thinking Tokens、Verbosity（2026 年 3-4 月）

**严重程度**：🔴 **高**
**状态**：✅ **已解决**（三个问题均于 2026 年 4 月 20 日解决）
**时间线**：2026 年 3 月 4 日 – 4 月 20 日

#### 问题

在为期六周的时间里，三项独立的 harness 与系统提示词改动降低了 Claude Code 的输出质量。这些都不是模型层面的回退；它们全部发生在 Claude Code 的 harness 层。直接使用 Anthropic API（不经过 Claude Code harness）则不受影响。

#### 事故 1：默认 Effort 从 High 降为 Medium（3 月 4 日，4 月 7 日回滚）

**触发原因**：在某些会话中，high effort 模式下的长延迟让 UI 看起来像是卡死了。
**改动**：Anthropic 将 Sonnet 4.6 和 Opus 4.6 的默认推理 effort 从 `high` 改为 `medium`。
**影响**：未手动设置 `/effort high` 的用户在不知情的情况下得到了 medium 质量的推理。产品内的指示器仍显示 "high"，使得这一回退被掩盖了一个多月。
**受影响**：Sonnet 4.6、Opus 4.6。
**解决方案**：4 月 7 日回滚。新默认值：Opus 4.7 为 xhigh，其余所有模型为 high。同时还交付了恰当的 UI 迭代（thinking 加载动画、更清晰的 `/effort` UX）。

#### 事故 2：闲置后每轮清除 Thinking Tokens（3 月 26 日，4 月 10 日修复）

**触发原因**：Anthropic 发布了一项改动，当会话闲置超过一小时后清除一次 thinking tokens（以降低恢复时的延迟与缓存成本）。
**Bug**：一处代码缺陷导致清除在该会话此后的每一轮都被触发，而不只是恢复时清除一次。
**影响**：会话变得健忘且重复，Claude 在恢复后的对话过程中逐步丢失上下文。
**受影响**：Sonnet 4.6、Opus 4.6。
**解决方案**：Bug 于 2026 年 4 月 10 日修复（v2.1.101）。据 Boris Cherny（CC 团队）所述，根本原因是：大型闲置会话导致完全的缓存未命中（900K+ tokens），在恢复时给 Pro 用户带来显著的 token 成本激增。

#### 事故 3：Verbosity 系统提示词指令（4 月 16 日，4 月 20 日回滚）

**触发原因**：Anthropic 新增了一条系统提示词指令以减少回复的冗长度。
**影响**：与当时生效的其他提示词改动叠加后，编码质量明显下降。
**受影响**：Sonnet 4.6、Opus 4.6、Opus 4.7。
**解决方案**：4 月 20 日回滚。暴露仅四天，是三起事故中解决最快的一起。

#### 社区影响

- Reddit、HN、X/Twitter 上广泛出现质量下降的报告（2026 年 3–4 月）
- Pro 与 Max 订阅用户出现退订
- Anthropic 员工（包括 Boris Cherny）最初在评论区回应，但未承认这些系统性问题
- HN 帖子在披露当天评论数达到 250+

#### Anthropic 的回应

**官方更新**：[An update on recent Claude Code quality reports](https://www.anthropic.com/engineering/april-23-postmortem)（2026 年 4 月 23 日）

帖子中的关键承诺：
- 为所有订阅用户重置使用限额（4 月 23 日）
- 更大比例的内部员工将使用与公开版完全一致的构建（而非功能测试构建）
- "Going forward" 一节承诺改进评测与发布实践

Boris Cherny 的关键引述（HN 评论）：
> "We agree, and will be spending the next few weeks increasing our investment in polish, quality, and reliability."

**解决方案**：三个问题均在 2026 年 4 月 7 日至 20 日之间解决。

---

### 模型质量下降（2025 年 8-9 月）

**严重程度**：🔴 **严重**
**状态**：✅ **已解决**（2025 年 9 月中旬）
**时间线**：2025 年 8 月 25 日 - 9 月初

#### 问题

用户报告 Claude Code 出现：
- 输出质量比先前版本更差
- 意外出现语法错误
- 意外插入字符（在英文回复中混入泰文/中文文本）
- 基本任务失败
- 错误的代码编辑

#### 根本原因

Anthropic 确认了**三个基础设施 bug**（而非模型退化）：

1. **流量错误路由**：约 30% 的 Claude Code 请求被路由到了错误的服务器类型 → 导致响应降级
2. **输出损坏**：8 月 25 日部署的一处错误配置导致 token 生成错误
3. **XLA:TPU 误编译**：一项性能优化触发了潜在的编译器 bug，影响了 token 的选择

#### 社区影响

- **大规模退订运动**（2025 年 8-9 月）
- 社区猜测：为降低成本而故意降低模型质量（量化）
- Reddit 情绪急剧转差

#### Anthropic 的回应

**官方事后复盘**：[A postmortem of three recent issues](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues)（2025 年 9 月 17 日）

关键引述：
> "We never reduce model quality due to demand, time of day, or server load. The problems our users reported were due to infrastructure bugs alone."

**解决方案**：所有 bug 于 2025 年 9 月中旬修复。

---

## 🔄 LLM 日常性能波动

**类型**：预期行为（不是 bug）
**严重程度**：🟡 **低 - 需知悉**
**状态**：LLM 推理固有特性，不针对任何特定版本

### 这是什么

即便使用完全相同的提示词和干净的上下文窗口，Claude 的输出质量也可能在不同会话之间出现明显波动。这与上下文窗口退化（发生在单个会话内，随着上下文被填满而出现）不同。这里说的是全新会话之间的波动。

用户有时会报告：回复变短、建议更保守，或对前一天还能正常完成的任务出现意外拒绝。这可能感觉像是模型被降级了，但事实并非如此。

### 根本原因

**概率性推理**：temperature 大于 0 意味着每次推理运行都是非确定性的。同一提示词运行两次会产生不同的 token 序列。这是语言模型工作方式的根本所在。

**MoE 路由波动**：Claude 采用 Mixture of Experts 架构。在每次前向传播中，路由机制会选择激活哪些专家权重。不同的运行会激活不同的组合，即使输入在语义上完全相同，也会产生不同的输出。

**基础设施波动**：在生产环境中，请求会命中负载水平、硬件代次和热状态各不相同的服务器。这些因素会影响推理过程中浮点运算的数值精度，从而造成细微但真实存在的输出差异。

**上下文敏感性**：即便执行了 `/clear`，会话之间的微小差异也会累积。系统提示词、工具列表和会话初始化都会对模型的首批输出产生轻微影响。

### 可观察的信号

| 信号 | 你看到的现象 | 含义 |
|--------|-------------|---------------|
| 回复长度 | 比平时更短、更不详细 | 路由命中了更保守的路径 |
| 拒绝 | 通常可行的边缘情况被拒绝 | 本次运行采用了不同的安全校准 |
| 代码风格 | 比预期更冗长或更简略 | 专家组合的激活方式不同 |
| 创造力 | 建议更保守、缺乏新意 | 不是能力损失，而是一次采样结果 |
| 冗长度 | 比平时更多的告诫与免责声明 | token 概率的正常波动 |

### 这不是什么

- **不是模型降级**：Anthropic 会有意地对模型进行版本管理并记录变更。日常波动发生在同一模型版本内部。
- **不是需要上报的 bug**：这一行为是预期的，并在 LLM 文献中有记载。它是概率性推理的固有特性。
- **不是永久性的**：下一个会话很可能表现不同。一次"糟糕"的运行并不代表持续性的改变。
- **不是上下文窗口退化**：那是单会话内由 token 累积引起的现象。这里说的是全新启动的会话之间的波动。

> 2025 年 8-9 月的事故（[见上文已解决问题](#model-quality-degradation-aug-sep-2025)）是例外：Anthropic 确认了确实存在导致系统性退化的基础设施 bug。真正的系统性退化很少见，且 Anthropic 会进行调查。正常的会话间波动则是另一回事。

### 缓解策略

**约束提示词**：更具体的提示词会缩小输出空间，使波动不那么明显。"写一个完成 X、Y、Z，返回类型 T，处理边缘情况 E 的函数" 会比 "给我写点处理 X 的东西" 产生更一致的输出。

**重要工作前清空上下文**：在高风险任务前执行 `/clear`。早前探索性工作累积的会话噪声，即使在同一会话内也可能让后续输出偏移。

**重新表述并重试**：如果某个输出与你的预期不符，试着用不同的措辞提出同一请求。第二种表述往往会经由不同的专家路径，产生更好的结果。

**对照一个已知良好的提示词**：如果你手上有一条来自先前会话、曾产出优秀输出的提示词，可将其作为参照。如果今天这条提示词持续地产出明显更差的输出，那就值得深入调查（如果可复现，可能还应提交一个 GitHub issue）。

**按任务类型校准预期**：确定性任务（正则、简单变换、定义明确的算法）的波动小于创造性或重判断的任务。前者可高度可靠地使用 Claude Code；后者则应在工作流中加入评审环节。

---

## 📊 问题统计（截至 2026 年 1 月 28 日）

| 指标 | 数量 | 来源 |
|--------|-------|--------|
| **开放 issue** | 5,702 | [GitHub API](https://github.com/anthropics/claude-code) |
| **标记为 "invalid" 的 issue** | 527 | GitHub Issues 搜索 |
| **"Wrong repo" issue（已确认）** | 17+ | 2026 年 1 月手动搜索 |
| **Token 消耗报告（12 月-1 月）** | 20+ | Issue 搜索 |
| **活跃发布** | 80+ | GitHub Releases |

---

## 🔍 如何追踪问题

### 查看开放的关键 issue

```bash
# Most reacted-to issues (community priority)
gh issue list --repo anthropics/claude-code --state open --sort reactions-+1 --limit 20

# Recent critical bugs
gh search issues --repo anthropics/claude-code "bug" "critical" --sort created --order desc --limit 10
```

### 监控特定主题

- **Token 消耗**：[搜索](https://github.com/anthropics/claude-code/issues?q=is%3Aissue+excessive+token)
- **错误仓库创建**：[搜索](https://github.com/anthropics/claude-code/issues?q=is%3Aissue+%22wrong+repo%22)
- **模型质量**：[搜索](https://github.com/anthropics/claude-code/issues?q=is%3Aissue+quality+degradation)

### 官方渠道

- **GitHub Issues**：https://github.com/anthropics/claude-code/issues
- **Anthropic Status**：https://status.anthropic.com/
- **Engineering Blog**：https://www.anthropic.com/engineering
- **Discord**：https://discord.gg/anthropic（仅限邀请，请查看官网）

---

## 📝 为本文档做贡献

本文档仅追踪**已核实、高影响的问题**。纳入标准：

- **已核实**：该问题在 GitHub 上存在且有多份报告，或有 Anthropic 官方确认
- **高影响**：影响安全、隐私、成本或核心功能
- **可操作**：有可用的变通方案或官方回应

如需建议更新：在 [claude-code-ultimate-guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/issues) 中提交 issue，并附上：
- GitHub issue 链接
- 影响的证据（多份报告、官方回应）
- 如有可用的变通方案

---

**免责声明**：本文档由社区维护，与 Anthropic 无任何关联。信息按现状提供。在做出决策前，请始终通过官方渠道核实当前状态。
