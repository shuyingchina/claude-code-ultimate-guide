---
title: "DevOps & SRE with Claude Code"
description: "FIRE framework for infrastructure diagnosis and DevOps workflows with Claude Code"
tags: [devops, guide, ci-cd, workflows]
---

# 使用 Claude Code 进行 DevOps 与 SRE

**阅读时长**：30 分钟
**技能级别**：中级（假定你已掌握 DevOps 基础）
**前置条件**：Claude Code 基础（主指南的[第 1-2 节](#getting-started)）

---

> **FIRE 框架**：一套使用 Claude Code 进行基础设施诊断的系统化方法。
>
> **F**irst Response（首次响应）→ **I**nvestigate（调查）→ **R**emediate（修复）→ **E**valuate（评估）

---

## 目录

1. [快速上手](#quick-start)
2. [模式：基础设施诊断](#pattern-infrastructure-diagnosis)
3. [模式：事故响应](#pattern-incident-response)
4. [模式：基础设施即代码](#pattern-infrastructure-as-code)
5. [防护栏与采用](#guardrails--adoption)
6. [快速参考](#quick-reference)

---

# 快速上手

**目标**：在 5 分钟内开始用 Claude Code 高效完成 DevOps 工作。

## 快速自检

| 情境 | 跳转至 |
|-----------|---------|
| 我现在正处于一次活跃的事故中 | [紧急：K8s 故障排查](#kubernetes-troubleshooting) |
| 第一次将 Claude 用于 DevOps | [教程：首次诊断](#your-first-infrastructure-diagnosis) |
| 想要自动化我的 runbook | [模式：事故响应](#pattern-incident-response) |
| 在为团队做评估 | [防护栏与采用](#guardrails--adoption) |
| 需要开箱即用的提示词 | [快速参考](#quick-reference) |

## FIRE 框架

使用 Claude 进行的每一次基础设施诊断都遵循以下模式：

```
F - First Response   → Give Claude the symptom + context
I - Investigate      → Claude analyzes logs, metrics, config
R - Remediate        → Claude proposes fix (with human approval)
E - Evaluate         → Postmortem, documentation, prevention
```

### 为什么是 FIRE？

| 阶段 | 人类角色 | Claude 角色 |
|-------|------------|-------------|
| **F**irst Response（首次响应） | 描述症状、提供上下文 | 分诊、确定检查优先级 |
| **I**nvestigate（调查） | 执行命令、粘贴输出 | 分析、关联、提出假设 |
| **R**emediate（修复） | **批准或拒绝** | 提出修复方案、说明影响 |
| **E**valuate（评估） | 复盘、分享知识 | 生成事后报告、文档 |

**关键**：Claude 提出方案，你来批准。这一点在以下场景中尤为重要：
- 破坏性操作（删除、缩容、重启）
- 生产环境
- 涉及安全敏感的变更

## 你的第一次基础设施诊断

### 示例：Pod CrashLoopBackOff

```bash
# Step 1: FIRST RESPONSE - Give context
claude "I have a pod in CrashLoopBackOff in the payment-service namespace.
Environment: production
Cluster: gke-prod-us-east1
Started: 10 minutes ago
What are the first 3 things I should check?"

# Step 2: INVESTIGATE - Run suggested commands and share output
kubectl describe pod payment-api-7d4b8c6f5-x2j9k -n payment-service
# Copy output and paste to Claude

# Step 3: REMEDIATE - Claude proposes, you approve
claude "Based on this describe output, what's the fix?
CONSTRAINT: Show me the exact command but don't execute anything."

# Step 4: EVALUATE - Document the incident
claude "Create a brief incident note for our wiki:
- What happened
- Root cause
- Fix applied
- Prevention recommendation"
```

### Claude 会返回什么（首次响应示例）

```markdown
## CrashLoopBackOff Triage (Priority Order)

1. **Check exit code and last logs**
   ```bash
   kubectl logs payment-api-7d4b8c6f5-x2j9k -n payment-service --previous
   ```
   Most common: OOM (exit 137), config errors (exit 1), dependency failures

2. **Check pod events and resource limits**
   ```bash
   kubectl describe pod payment-api-7d4b8c6f5-x2j9k -n payment-service
   ```
   Look for: OOMKilled, ImagePullBackOff, liveness probe failures

3. **Check recent deployment changes**
   ```bash
   kubectl rollout history deployment/payment-api -n payment-service
   ```
   If recent: consider rollback while investigating
```

---

# 模式：基础设施诊断

**目标**：对常见基础设施问题进行系统化故障排查。

## Kubernetes 故障排查

### K8s MCP Server 设置

为了让 K8s 上下文持久化，请安装 K8s MCP server：

```json
// ~/.claude.json (or .mcp.json)
{
  "mcpServers": {
    "kubernetes": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-kubernetes"]
    }
  }
}
```

**好处**：Claude 可以直接查询集群状态，减少复制粘贴的来回操作。

**不使用 MCP 时**：你需要手动将 kubectl 输出管道传给 Claude（同样有效）。

### 按症状分类的提示词

复制粘贴这些提示词，并替换 `<bracketed>` 中的值。

#### CrashLoopBackOff

```bash
kubectl describe pod <pod> -n <ns> | claude "Analyze this CrashLoopBackOff:
1. What's the exit code and what does it mean?
2. Check the last 5 restarts pattern (timing, consistent or escalating?)
3. Suggest 3 most likely root causes based on the events
4. Give me the exact commands to investigate each hypothesis"
```

**Claude 会识别出的常见原因**：
- Exit 137：OOMKilled（触及内存上限）
- Exit 1：应用错误（配置错误、缺少依赖）
- Exit 143：SIGTERM（优雅关闭超时）

#### OOMKilled

```bash
kubectl top pods -n <ns> && kubectl describe pod <pod> -n <ns> | claude "This pod was OOMKilled:
1. Compare requests vs limits vs actual usage
2. Is this a memory leak or under-provisioning?
3. If leak: what patterns in the container suggest investigation paths?
4. If under-provisioned: suggest optimal resource settings based on this data"
```

**针对内存泄漏的后续追问**：
```bash
claude "The pod has been restarting every 2 hours with OOMKilled.
Memory grows linearly from 200Mi to 512Mi limit before crash.
Language: Node.js 18
What are the top 3 things to check for memory leaks in this stack?"
```

#### ImagePullBackOff

```bash
kubectl describe pod <pod> -n <ns> | claude "ImagePullBackOff diagnosis:
1. Is this an auth issue, network issue, or wrong image name?
2. What's the exact error message telling us?
3. Give me commands to verify the image exists and credentials work"
```

#### Pending Pod（无法调度）

```bash
kubectl describe pod <pod> -n <ns> && kubectl describe nodes | claude "Pod stuck in Pending:
1. Is this resource constraints, node selectors, or affinity rules?
2. Which nodes were considered and why rejected?
3. What's the quickest fix vs proper solution?"
```

#### Service 无法访问

```bash
kubectl get svc,endpoints -n <ns> && kubectl describe svc <svc> -n <ns> | claude "Service not reachable:
1. Are there healthy endpoints?
2. Is the selector matching pods correctly?
3. Is it a network policy blocking traffic?
Give me diagnostic commands for each possibility"
```

### 案例研究：生产事故根因分析

**情境**：某电商平台，凌晨 3 点被告警唤醒，结账服务返回 503 错误。

**FIRE 实战**：

```bash
# F - First Response
claude "INCIDENT: checkout-service returning 503s, started 10 min ago.
Impact: 100% of checkout attempts failing.
Environment: AWS EKS production, us-east-1.
Recent changes: deployment 2 hours ago (new feature flag logic).
What's the fastest diagnostic path?"

# I - Investigate (Claude suggested checking pods first)
kubectl get pods -n checkout -l app=checkout-service
# Output: 3/5 pods in CrashLoopBackOff

kubectl logs checkout-service-xxx --previous | tail -50 | claude "Analyze crash logs"
# Claude identifies: panic: nil pointer dereference in feature flag code

# R - Remediate
claude "Root cause identified: nil pointer in feature flag logic from recent deploy.
Options:
A) Rollback to previous version
B) Hotfix the nil check
Which is faster and safer at 3 AM?"
# Claude recommends: Rollback (faster, proven state, fix properly tomorrow)

kubectl rollout undo deployment/checkout-service -n checkout
# Service restored in 2 minutes

# E - Evaluate (next day)
claude "Create postmortem from this incident:
Timeline: 3:02 AM alert, 3:15 AM root cause found, 3:17 AM rollback, 3:19 AM resolved
Root cause: Feature flag nil pointer from commit abc123
Impact: 15 minutes checkout downtime
Format: Blameless, focused on prevention"
```

**结果**：MTTR 为 15 分钟，事后报告清晰，并确定了相应的预防行动项。

## 日志分析与关联

### 多服务日志关联

```bash
# Collect logs from related services
kubectl logs -l app=api-gateway -n ingress --since=10m > gateway.log
kubectl logs -l app=auth-service -n auth --since=10m > auth.log
kubectl logs -l app=payment-service -n payment --since=10m > payment.log

# Analyze correlation
cat gateway.log auth.log payment.log | claude "Correlate these logs:
1. Find the request flow for failed transactions
2. Identify where the failure originates
3. Are there patterns in timing or specific endpoints?
4. Create a timeline of events"
```

### 日志模式检测

```bash
# Find anomalies in error patterns
grep -E "ERROR|WARN|Exception" app.log | claude "Analyze error patterns:
1. Cluster similar errors (group by type, not timestamp)
2. What's the most frequent vs most severe?
3. Which errors are correlated (same root cause)?
4. Prioritize investigation order"
```

### Prometheus/Grafana 查询协助

```bash
claude "I need a PromQL query to:
- Show p99 latency for the payment-service
- Group by endpoint
- Alert if > 500ms for 5 minutes
Include the alert rule YAML too"
```

## Claude 做不到什么（局限性）

了解局限性可以避免挫败感和不安全的依赖。

| 局限性 | 影响 | 应对方法 |
|------------|--------|------------|
| **无法获取实时集群状态** | 看不到当前 pod 状态 | 使用 K8s MCP 或粘贴 kubectl 输出 |
| **无法直接访问 API** | 无法调用 AWS/GCP API | 使用 MCP 服务器或共享 CLI 输出 |
| **上下文窗口限制** | 最多约 100K tokens | 聚焦相关日志，而非完整转储 |
| **无持久记忆** | 会话之间会遗忘 | 使用 CLAUDE.md 保存项目上下文 |
| **幻觉风险** | 可能建议无效的 flag | 运行前务必验证命令 |
| **无法获取实时指标** | 看不到当前图表 | 截图 Grafana 或粘贴指标值 |
| **无法访问密钥** | 无法读取 vault/secrets | 很好！永远不要把密钥分享给任何 LLM |

### 什么时候不该用 Claude

- **30 秒内必须做出的紧急决策**：你的肌肉记忆更快
- **高度机密的事件**：数据泄露调查（涉及法律影响）
- **简单、显而易见的修复**：如果你已经知道答案，直接动手就好
- **受合规限制的环境**：先确认是否允许使用 AI 工具
- **AI 专属的安全事件**：检测到 prompt injection、MCP 被攻陷、agent 正在外泄数据 → 参见 [Security Hardening — Response](../security/security-hardening.md#part-3-response-when-things-go-wrong) 了解专门的处置流程（kill switch 架构、隔离级别、事件时间线）

### Claude 擅长什么

- **复杂的根因分析**：多个相互作用的系统
- **文档生成**：事后复盘、运行手册、操作流程
- **学习新工具**：陌生的云服务、新的 k8s 特性
- **第二意见**：验证你的假设
- **批量操作**：为多个环境生成配置

---

# 模式：事件响应

**目标**：为事件管理提供结构化的工作流。

## 单人事件处理工作流

**现实**：凌晨 3 点，只有你一个人。这套工作流是为单人设计的。

### FIRE 实战：单人事件

#### F - 首次响应（30 秒）

```bash
claude "INCIDENT: [symptom - be specific]
Context: [service], [environment], [time started]
Recent changes: [deploys, infra changes, traffic spikes]
Current impact: [% users affected, revenue impact if known]
What are the 3 most critical things to check first?"
```

**示例**：
```bash
claude "INCIDENT: API returning 500 errors on /checkout endpoint
Context: checkout-service, production-us-east-1, started 5 min ago
Recent changes: deployed v2.3.4 at 2:45 AM, added new payment provider
Current impact: ~30% of checkout requests failing
What are the 3 most critical things to check first?"
```

#### I - 调查（2-5 分钟）

运行 Claude 建议的命令，分享输出：

```bash
# Claude suggested checking pod health first
kubectl get pods -n checkout | claude "Quick assessment of this pod list"

# Then checking recent logs
kubectl logs -l app=checkout --since=5m | head -100 | claude "Analyze for error patterns"

# Then checking the deployment diff
kubectl rollout history deployment/checkout-service -n checkout | claude "What changed in the last deployment?"
```

**专业提示**：留一个终端运行命令，另一个用于与 Claude 对话。

#### R - 修复（需经批准）

```bash
claude "Based on investigation:
- Root cause: [your understanding]
- Evidence: [key findings]

Propose remediation options:
1. Quick mitigation (restore service)
2. Proper fix (address root cause)

CONSTRAINT: I need to approve before any action. Show exact commands."
```

**批准关卡示例**：
```
Claude: "Recommended: Rollback to v2.3.3
Command: kubectl rollout undo deployment/checkout-service -n checkout
Risk: Low - previous version was stable for 2 weeks
Alternative: Scale down the new payment provider feature flag

Which approach do you want to take?"

You: "Proceed with rollback"
```

#### E - 评估（事件结束后，而非进行中）

```bash
claude "Create incident postmortem:

Timeline:
- 2:45 AM: Deployed v2.3.4
- 3:00 AM: First alerts fired
- 3:05 AM: Incident declared
- 3:12 AM: Root cause identified (nil pointer in new payment provider code)
- 3:15 AM: Rollback initiated
- 3:17 AM: Service restored

Format: Blameless, focus on systems not people
Include: Action items with owners"
```

## 事件期间的沟通

### 干系人更新生成器

```bash
claude "Generate incident update for stakeholders:

Incident: Checkout service degradation
Current status: Mitigated, monitoring
Impact: 15 minutes of 30% checkout failures
ETA to full resolution: 2 hours (proper fix in next deploy)

Audience: Non-technical executives
Tone: Professional, reassuring, factual
Length: 3 sentences max"
```

**输出示例**：
> 我们的结账服务经历了 15 分钟的中断，影响了约 30% 的交易，目前问题已解决。该问题由近期更新中的一个软件 bug 引起，已被迅速回滚。我们将在下一个计划维护窗口部署永久修复，预计不会对客户造成影响。

### 事件作战桥 Prompt

适用于实时事件频道：

```bash
claude "I'm managing an incident bridge. Help me:
1. Maintain a running timeline of events
2. Suggest next investigation steps when we hit dead ends
3. Draft comms updates every 15 minutes
4. Flag when I should escalate

Current status: [paste latest update]
What should I communicate to the bridge now?"
```

## 多 Agent 模式：事后分析

**何时使用多 agent**：不要在事件进行中使用。用于事后的全面分析。

```bash
# Agent 1: Timeline Reconstruction
claude "You are an incident timeline analyst.
From these logs and Slack messages, reconstruct a precise timeline:
[paste logs and comms]
Output: Timestamped events, who did what when"

# Agent 2: Root Cause Analysis
claude "You are a root cause analyst.
Given this timeline and system architecture, perform 5-whys analysis:
[paste timeline from Agent 1]
Output: Root cause chain, contributing factors"

# Agent 3: Prevention Recommendations
claude "You are an SRE process improvement specialist.
Given this root cause analysis:
[paste RCA from Agent 2]
Output: Prioritized prevention measures, effort estimates, ownership suggestions"
```

### 案例研究：OpsWorker.ai 的 MTTR 缩减

**背景**：SRE 团队管理 200+ 微服务，5 名值班工程师。

**使用 Claude 之前**：
- 平均 MTTR：45 分钟
- 事后复盘：经常延迟或被跳过
- 知识孤岛：每位工程师只熟悉不同的服务

**集成 Claude**：
1. 所有事件采用 FIRE 框架
2. Claude 在 1 小时内生成初版事后复盘草稿
3. 运行手册通过 Claude 辅助的故障排查得到增强

**3 个月后**：
- 平均 MTTR：18 分钟（缩减 60%）
- 事后复盘完成率：95% 在 24 小时内完成
- 知识共享：所有人都可访问 Claude 生成的运行手册

**关键洞见**：最大的收益不是速度——而是一致性和文档化。

---

# 模式：基础设施即代码

**目标**：利用 Claude 进行 Terraform、Ansible 和 GitOps 工作流。

## 在 Claude 中使用 Terraform

### 参考：Anton Babenko 的 Terraform Skill

适用于 Claude Code 的最全面的 Terraform skill：

**Repository**: [antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill)
**Author**: Anton Babenko（terraform-aws-modules 的作者，下载量超过 10 亿次）

```bash
# Install
cd ~/.claude/skills/
git clone https://github.com/antonbabenko/terraform-skill.git terraform
```

**它提供的内容**：
- 模块结构的最佳实践
- AWS、GCP、Azure 模式
- 状态管理指导
- CI/CD 集成模式

### 常见的 Terraform 提示词

#### 计划审查

```bash
terraform plan -out=plan.txt && cat plan.txt | claude "Review this Terraform plan:
1. Any dangerous changes? (data loss, downtime)
2. Are the changes what we expect?
3. Any missing changes we should add?
4. Cost implications if visible"
```

#### 模块生成

```bash
claude "Generate a Terraform module for:
- AWS ECS Fargate service
- With ALB and target group
- Auto-scaling based on CPU
- Secrets from SSM Parameter Store

Follow these conventions:
- Use for_each over count
- All resources tagged with var.tags
- Output the service URL and ARN"
```

#### 状态手术助手

```bash
claude "I need to move a resource to a different state file:
Current state: terraform-prod/terraform.tfstate
Resource: aws_s3_bucket.logs
Target state: terraform-shared/terraform.tfstate

What's the safest procedure? Include rollback steps."
```

### 漂移检测工作流

```bash
# Detect drift
terraform plan -detailed-exitcode 2>&1 | tee drift.txt

# Analyze with Claude
cat drift.txt | claude "Analyze this Terraform drift:
1. What changed outside of Terraform?
2. Is this drift expected (manual change) or concerning?
3. Should we import the changes or revert to Terraform state?
4. What's the safest remediation path?"
```

## 在 Claude 中使用 Ansible

### Playbook 审查

```bash
cat playbook.yml | claude "Review this Ansible playbook:
1. Idempotency issues?
2. Security concerns?
3. Error handling gaps?
4. Performance optimizations?"
```

### 角色生成

```bash
claude "Generate an Ansible role for:
- Installing and configuring Nginx
- SSL certificates via Let's Encrypt (certbot)
- Hardened configuration (disable server tokens, etc.)
- Log rotation

Follow best practices:
- Use handlers for service restarts
- Variables in defaults/main.yml
- Include molecule tests structure"
```

## 在 Claude 中使用 GitOps

### ArgoCD 应用审查

```bash
cat application.yaml | claude "Review this ArgoCD Application:
1. Sync policy appropriate for the environment?
2. Resource health checks defined?
3. Any sync wave ordering issues?
4. Namespace and project permissions correct?"
```

### Helm Values 生成

```bash
claude "Generate Helm values for deploying [application] to:
- Environment: staging
- Resources: Limited (cost-conscious)
- Replicas: 2
- Ingress: Internal only
- Secrets: From external-secrets operator

Base chart: [chart name]
Include comments explaining each value"
```

## 安全审查自动化

### 基础设施安全扫描

```bash
# Run tfsec or checkov, analyze results
tfsec . --format=json | claude "Analyze these security findings:
1. Prioritize by severity and exploitability
2. Which are false positives in our context?
3. For real issues: what's the fix?
4. Which can we ignore with a documented reason?"
```

### IAM 策略审查

```bash
cat iam-policy.json | claude "Review this IAM policy:
1. Does it follow least privilege?
2. Any overly permissive actions? (*, admin, etc.)
3. Resource constraints appropriate?
4. Suggest a more restrictive version that still works"
```

---

# 防护栏与团队采用

**目标**：安全地落地 Claude Code 并赢得团队认同。

## 成本意识

### Claude Code 成本

| 模型 | 输入（每 100 万 tokens） | 输出（每 100 万 tokens） |
|-------|-------------------|-------------------|
| Sonnet 4 | $3 | $15 |
| Opus 4 | $15 | $75 |

**典型的 DevOps 会话**：20K-50K tokens = $0.10-$0.50

**成本控制策略**：
1. 常规任务使用 Sonnet（默认）
2. 将 Opus 留给复杂的多系统分析
3. 当对话变长时，使用 `/compact` 来缩减上下文
4. 不要粘贴整个日志文件；先 grep 出相关的部分

### Claude 建议带来的基础设施成本

**注意**：Claude 看不到你的云账单。务必询问：

```bash
claude "Before I apply these changes, estimate:
1. Monthly cost impact (compute, storage, network)
2. Any resources that could scale unbounded?
3. Cost optimization alternatives?"
```

## 安全边界

### 切勿与 Claude 分享的内容

| 数据类型 | 原因 | 替代做法 |
|-----------|---------|-------------|
| API 密钥、令牌 | 可能被缓存/记录 | 使用占位符：`<API_KEY>` |
| 生产环境密钥 | 安全风险 | 描述密钥的类型，而非具体值 |
| 客户 PII | 隐私/合规 | 使用匿名化示例 |
| 专有算法 | 知识产权保护 | 描述行为，而非代码 |
| 含 PII 的事故详情 | 法律责任 | 分享前先脱敏 |

### 安全提示词模板

```bash
claude "Debug this authentication issue:
- Service: auth-service
- Error: 401 Unauthorized for valid tokens
- Environment: staging (not production)
- Token format: JWT with claims [user_id, org_id, exp]
- NOTE: I've redacted all actual token values

Here's the sanitized log:
[paste log with secrets replaced]"
```

### 生产环境的审批关卡

以下操作务必要求人工审批：

```yaml
# Example: Production change checklist
approval_required:
  - kubectl delete
  - kubectl scale (down)
  - terraform destroy
  - DROP TABLE / DELETE FROM
  - rm -rf (outside tmp directories)
  - Any production database write
  - Any IAM policy change
  - Any security group modification
```

## 团队推广清单

### 阶段 1：试点（1-2 名工程师，2 周）

- [ ] 为试点用户安装 Claude Code
- [ ] 创建包含通用上下文的团队 CLAUDE.md
- [ ] 记录前 5 个成功用例
- [ ] 确定一个需要标准化的工作流
- [ ] 跟踪节省的时间（前后对比）

### 阶段 2：扩展（团队，4 周）

- [ ] 在团队会议中分享试点经验
- [ ] 创建团队专属的 prompts 库
- [ ] 制定安全准则（哪些可以分享、哪些不可以）
- [ ] 搭建共享的 skills/commands 仓库
- [ ] 明确何时使用 Claude、何时不使用

### 阶段 3：优化（持续进行）

- [ ] 每月审查 prompt 库
- [ ] A/B 测试：针对类似事件，Claude 辅助方式 vs 传统方式
- [ ] 回馈社区（awesome-lists、本指南）
- [ ] 跟踪 MTTR、事后复盘完成率、文档质量

### 需要避免的采用误区

| 误区 | 为什么会发生 | 防范措施 |
|---------|---------------|------------|
| **过度依赖** | Claude 太好用了 | 强制安排学习时间，而不仅仅追求产出 |
| **盲目信任** | 命令通常都能用 | 运行前务必审查 |
| **上下文倾倒** | 期望 Claude 自己搞清楚 | 提供聚焦的上下文，而非所有内容 |
| **跳过验证** | 时间压力 | 将验证内建到工作流中 |
| **暗地使用** | 团队缺乏可见性 | 分享成果，让使用常态化 |

---

# 快速参考

## FIRE 框架摘要

```
┌─────────────────────────────────────────────────────────────┐
│ F - FIRST RESPONSE                                          │
│   "INCIDENT: [symptom]. Context: [service, env, time].      │
│    Recent changes: [what]. Impact: [who affected].          │
│    What are the 3 most critical things to check?"           │
├─────────────────────────────────────────────────────────────┤
│ I - INVESTIGATE                                             │
│   Run Claude's suggested commands                           │
│   Share output: "[output] | claude 'Analyze this'"          │
│   Iterate until root cause identified                       │
├─────────────────────────────────────────────────────────────┤
│ R - REMEDIATE                                               │
│   "Based on [findings], propose remediation.                │
│    CONSTRAINT: I need to approve before any action."        │
│   APPROVE → Execute │ REJECT → More investigation           │
├─────────────────────────────────────────────────────────────┤
│ E - EVALUATE                                                │
│   "Create postmortem: Timeline, root cause, prevention.     │
│    Format: Blameless, action items with owners."            │
└─────────────────────────────────────────────────────────────┘
```

## 按症状分类的 Prompts

### Kubernetes

| 症状 | Prompt |
|---------|--------|
| CrashLoopBackOff | `kubectl describe pod <pod> -n <ns> \| claude "Exit code meaning? 3 likely causes? Commands to investigate?"` |
| OOMKilled | `kubectl top pods && describe pod \| claude "Leak or under-provisioned? Optimal resources?"` |
| ImagePullBackOff | `kubectl describe pod \| claude "Auth, network, or wrong image? Verification commands?"` |
| Pending | `kubectl describe pod && describe nodes \| claude "Resource, selector, or affinity issue?"` |
| 服务不可达 | `kubectl get svc,endpoints \| claude "Healthy endpoints? Selector matching? Network policy?"` |

### 云 / 基础设施

| 症状 | Prompt |
|---------|--------|
| 高延迟 | `[metrics] \| claude "Bottleneck location? Is it compute, network, or dependency?"` |
| 磁盘已满 | `df -h && du -sh /* \| claude "What's consuming space? Safe to delete?"` |
| 连接被拒绝 | `netstat -tlnp \| claude "Service listening? Port correct? Firewall rules?"` |
| SSL 证书过期 | `openssl s_client -connect host:443 \| claude "Days until expiry? Renewal steps?"` |
| DNS 问题 | `dig +trace domain \| claude "Where does resolution fail?"` |

### Terraform

| 任务 | Prompt |
|------|--------|
| Plan 审查 | `terraform plan \| claude "Dangerous changes? Missing changes? Cost impact?"` |
| 漂移分析 | `terraform plan -detailed-exitcode \| claude "What drifted? Expected? Remediation?"` |
| 模块请求 | `claude "Generate Terraform module for [resource] with [requirements]"` |

## 面向 DevOps 的 MCP Servers

| Server | 用途 | 安装 |
|--------|---------|---------|
| Kubernetes | 直接访问集群 | `npx -y @anthropic/mcp-kubernetes` |
| AWS | 访问 AWS API | `npx -y @anthropic/mcp-aws` |
| GCP | 访问 GCP API | `npx -y @anthropic/mcp-gcp` |
| Prometheus | 直接查询指标 | 社区版：搜索 awesome-mcp-servers |
| Terraform | State/plan 分析 | 社区版：搜索 awesome-mcp-servers |

**配置位置**：`~/.claude.json`（字段 `"mcpServers"`）

```json
{
  "mcpServers": {
    "kubernetes": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-kubernetes"]
    }
  }
}
```

## 外部资源

### Awesome Lists

- **[awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)**（8.1k stars）：包含 SRE 在内的 agent 角色
- **[awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)**（4.6k stars）：包含基础设施相关的 skills

### 官方资源

- **[terraform-skill](https://github.com/antonbabenko/terraform-skill)**：由 Anton Babenko 制作的生产级 Terraform skill
- **[Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)**：官方文档

### 社区

- **Anthropic Discord**：#claude-code 频道
- **Reddit**：r/ClaudeAI
- **GitHub**：在 awesome-lists 上提交 issue 以请求新功能

---

## 另请参阅

- **[Agent 模板](../../examples/agents/devops-sre.md)**：面向 Claude 的 DevOps/SRE agent 角色
- **[CLAUDE.md 模板](../../examples/claude-md/devops-sre.md)**：面向 DevOps 团队的项目配置
- **[安全加固指南](../security/security-hardening.md)**：更多安全实践
- **[架构指南](../core/architecture.md)**：Claude Code 内部工作原理

---

*欢迎贡献！如果你有运行良好的 DevOps prompts，欢迎将它们添加到 awesome-lists，或向本指南提交 PR。*
