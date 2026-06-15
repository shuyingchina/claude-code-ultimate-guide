---
title: "Enterprise AI Governance for Claude Code"
description: "Org-level governance for teams deploying Claude Code at scale: usage charters, MCP approval workflows, guardrail tiers, and compliance"
tags: [security, enterprise, governance, compliance]
---

# Claude Code 的企业级 AI 治理

> **目标读者**：在多个团队中部署 Claude Code 的技术负责人、工程经理和安全官。
>
> **范围**：组织级治理（策略、审批流程、分级、合规）。关于个人开发者的安全（注入防御、MCP 审查、CVE），参见 [security-hardening.md](./security-hardening.md)。关于 6 条不可妥协的生产规则，参见 [production-safety.md](./production-safety.md)。

---

## TL;DR

**治理缺口**：Claude Code 的安全文档涵盖了个人开发者应当怎么做。但它们没有涵盖当你的整个组织都在使用它时会发生什么 —— 50 名开发者、不同的风险画像、没有共享策略。

**本文涵盖的内容**：

| 章节 | 它为你提供什么 |
|---------|------------------|
| [本地 vs 共享](#1-local-vs-shared-the-governance-split) | 风险矩阵 + 决策框架 |
| [使用章程](#2-ai-usage-charter) | 精简模板，可直接套用 |
| [MCP 治理](#3-mcp-governance-workflow) | 审批流程 + YAML 注册表 |
| [护栏分级](#4-guardrail-tiers) | 4 个预配置分级，可复制粘贴的 settings.json |
| [规模化策略](#5-policy-enforcement-at-scale) | 推广、入职、CI/CD 关卡 |
| [审计与合规](#6-audit-compliance--governance-structure) | SOC2/ISO27001 审计员真正会问什么 |

---

## 1. 本地 vs 共享：治理的分界

企业级 AI 治理中最大的错误，是对所有场景套用同一套规则。本地使用和共享使用具有本质上不同的风险画像。

### 1.1 风险矩阵

| 维度 | 本地使用 | 共享使用 |
|-----------|-------------|--------------|
| **数据暴露** | 开发者自己的文件 | 客户数据、共享代码库、密钥 |
| **影响范围** | 一台机器 | 整个仓库、CI/CD、生产环境 |
| **责任归属** | 个人 | 团队 / 组织 |
| **可复现性** | 会话结束，历史消失 | 需要审计轨迹 |
| **合规范围** | 通常没有 | SOC2、ISO27001、HIPAA（如适用） |
| **配置漂移** | 个人偏好 | 团队一致性很重要 |

### 1.2 你能控制和不能控制的

**你可以控制**（通过提交到仓库的配置）：
- 哪些 MCP 服务器被批准（仓库中的 `settings.json`）
- Claude 能使用哪些工具（`permissions.deny`）
- CLAUDE.md 关于项目约定的内容
- 在工具使用前/后运行的 hook 脚本
- 校验 AI 生成代码的 CI/CD 关卡

**你无法直接控制**：
- 开发者拥有怎样的个人 `~/.claude/settings.json`
- 他们在个人 API 密钥上使用哪些模型
- 他们在你的仓库之外的个人项目中做什么
- 会话之间的 Memory / 会话内容

**实际含义**：把治理重点放在提交到你仓库、以及部署在共享环境中的内容上。个人开发工作流是开发者自己的责任。

### 1.3 决策框架：何时需要治理

并非所有事情都需要重度治理。按比例施加控制。

```
What are you governing?
│
├─ Personal dev workflow (local, throwaway code)
│   └─ Minimal: CLAUDE.md guidelines + basic hooks
│
├─ Team codebase (shared repo, not production)
│   └─ Standard: shared settings.json + MCP registry + PR gates
│
├─ Production system (customer-facing, real data)
│   └─ Strict: full tier config + approval workflow + audit log
│
└─ Regulated environment (HIPAA, SOC2, PCI, finance)
    └─ Regulated: all of above + compliance audit trail
```

---

## 2. AI 使用章程

使用章程回答一个根本问题："在本公司，我们被允许用 Claude Code 做什么？"没有它，每个团队都会给出不同的答案，从而造成不一致的风险暴露。

这是精简版。关于包含法律考量的完整章程，参见 [Whitepaper #11: Enterprise AI Governance](../../whitepapers/en/11-enterprise-ai-governance.qmd)（待发布）。

### 2.1 精简章程模板

将以下内容复制到你组织的 `docs/ai-usage-charter.md` 并加以调整：

```markdown
# AI Coding Tools Usage Charter

**Applies to**: Claude Code (and any AI coding assistant)
**Effective date**: [DATE]
**Owner**: Engineering Lead / CTO
**Review cadence**: Quarterly

---

## Approved Tools

| Tool | Scope | Data Classification |
|------|-------|---------------------|
| Claude Code (Pro/Team/Enterprise) | All dev work | Up to CONFIDENTIAL |
| Claude Code (personal accounts) | Personal dev only | PUBLIC/INTERNAL only |
| [Other approved tools] | [Scope] | [Classification] |

---

## Data Classification Rules

| Classification | Examples | Allowed with Claude Code? |
|----------------|----------|--------------------------|
| **PUBLIC** | Open source, public docs | Yes, no restrictions |
| **INTERNAL** | Internal tools, non-sensitive code | Yes, standard config |
| **CONFIDENTIAL** | Internal business secrets, non-regulated IP | Yes, Enterprise plan only |
| **RESTRICTED** | Customer PII, PCI card data, PHI, credentials | No — never in AI context without legal/compliance sign-off |

**Hard rule**: RESTRICTED data never enters an AI context window. Not in prompts, not in files Claude reads, not as examples. Configure `permissions.deny` to block access to restricted files.

---

## Approved Use Cases

- Code completion, review, refactoring
- Test generation
- Documentation drafting
- Debugging and root cause analysis
- Architecture analysis (internal systems only)
- CLI scripting and automation

---

## Prohibited Use Cases

- Processing payment card data (PCI scope)
- Generating code that handles raw PHI without security review
- Autonomous deployment to production without human approval
- Using personal AI accounts for CONFIDENTIAL or higher data
- Sharing customer data in prompts as examples

---

## Who Approves What

| Action | Approver |
|--------|---------|
| Add new MCP server to team config | Tech Lead + Security review |
| Enable Claude Code in new project | Team Lead |
| Use Enterprise features (Zero Trust, SSO) | IT/Security team |
| Exception to any charter rule | Engineering Director |

---

## Compliance Obligations

By using Claude Code on company systems, you agree to:
1. Follow this charter
2. Report suspected data exposure to security@[company] within 24h
3. Not circumvent governance controls (hooks, permission deny rules)
4. Participate in quarterly access reviews

---

**Charter violations**: Follow standard disciplinary process. First occurrence: coaching. Repeated or severe: escalation.
```

### 2.2 数据分级与 Claude Code 设置

将数据分级转化为实际配置：

```json
{
  "permissions": {
    "deny": [
      "Read(./**/*.pem)",
      "Read(./**/*.key)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(**/credentials*)",
      "Bash(cat .env*)",
      "Bash(printenv*)",
      "Bash(env)"
    ]
  }
}
```

```markdown
<!-- CLAUDE.md — data handling rules -->
## Data Handling

**NEVER** read, reference, or include in output:
- Files matching: .env, *.pem, *.key, credentials.*, secrets/
- Customer PII fields (fields named: email, phone, ssn, dob, card_*)
- Credentials or API keys (even masked/redacted examples)

If you encounter restricted data while reading a file, stop and inform the user.
Do not proceed until explicitly told to skip that content.
```

---

## 3. MCP 治理工作流

单个 MCP 的审查（5 分钟审计）已在 [security-hardening.md §1.1](./security-hardening.md#11-mcp-vetting-workflow) 中介绍。本节涵盖的是组织层面的工作流：新的 MCP 如何在团队中获得批准、部署和监控。

### 3.1 审批工作流

```
Developer wants new MCP
        │
        ▼
[1] Submit MCP Request
    - Name, source URL, version
    - Proposed use case
    - Data scope (what will it access?)
        │
        ▼
[2] Security Review (Tech Lead + optionally Security team)
    - 5-min MCP audit (see security-hardening.md)
    - Check: Stars >50, recent commits, no dangerous flags
    - Check: No CVEs (search NVD + GitHub security advisories)
    - Classify risk: LOW / MEDIUM / HIGH
        │
     ┌──┴──┐
   LOW   MED/HIGH
     │      │
     ▼      ▼
  Approve  Extended review
           (2-week trial in sandbox)
           + approval from Security team
        │
        ▼
[3] Add to Approved Registry
    - Pin exact version
    - Document approved scope
    - Set expiry date (6 months)
        │
        ▼
[4] Deploy via shared settings.json
    - Committed to repo
    - No local overrides for approved MCPs
        │
        ▼
[5] Monitor + Periodic Re-review
    - Check for security advisories every 30 days
    - Re-approve at version bumps (patch: auto, minor+: manual)
    - Quarterly full registry review
```

### 3.2 MCP 注册表格式

在团队共享配置仓库的 `.claude/mcp-registry.yaml` 中维护一个已批准的 MCP 注册表：

```yaml
# .claude/mcp-registry.yaml
# Approved MCP servers for [Organization Name]
# Last updated: 2026-03-10
# Reviewer: [Name, Role]

metadata:
  review_cycle: quarterly
  next_review: "2026-06-10"
  owner: "platform-team@company.com"

approved:
  - name: context7
    version: "1.2.3"
    source: "https://github.com/context7/mcp-server"
    approved_by: "john.doe@company.com"
    approved_date: "2026-01-15"
    expires: "2026-07-15"
    data_scope: PUBLIC
    risk: LOW
    rationale: "Read-only documentation lookup. No data egress."
    config:
      command: npx
      args: ["-y", "@context7/mcp-server@1.2.3"]

  - name: sequential-thinking
    version: "0.6.2"
    source: "https://github.com/modelcontextprotocol/servers"
    approved_by: "jane.smith@company.com"
    approved_date: "2026-01-15"
    expires: "2026-07-15"
    data_scope: INTERNAL
    risk: LOW
    rationale: "Local reasoning only. No network access."
    config:
      command: npx
      args: ["-y", "@modelcontextprotocol/server-sequential-thinking@0.6.2"]

  - name: internal-db-readonly
    version: "2.1.0"
    source: "internal"
    approved_by: "security@company.com"
    approved_date: "2026-02-01"
    expires: "2026-05-01"  # shorter expiry for higher risk
    data_scope: CONFIDENTIAL
    risk: MEDIUM
    rationale: "Read-only replica access. No PII tables in allowlist."
    restrictions:
      - "Read-only credentials only"
      - "No access to users, payments, or audit tables"
    config:
      command: npx
      args: ["-y", "@company/db-mcp@2.1.0"]

pending_review:
  - name: github-mcp
    requested_by: "dev@company.com"
    requested_date: "2026-03-05"
    use_case: "PR automation"
    status: under_review

denied:
  - name: browser-automation-mcp
    denied_date: "2026-02-10"
    reason: "Full browser access with no scope restriction. Risk too high."
```

### 3.3 通过 Hook 强制执行注册表

使用治理 hook 来验证只有已批准的 MCP 处于使用状态。下面的脚本是一个最小化的内联版本，你可以直接放入 `.claude/hooks/governance-check.sh`。如需包含额外检查（拒绝列表强制执行、危险允许列表检测）的更完整实现，参见 [`examples/hooks/bash/governance-enforcement-hook.sh`](../../examples/hooks/bash/governance-enforcement-hook.sh)。

```bash
#!/bin/bash
# .claude/hooks/governance-check.sh
# Event: SessionStart
# Validates active MCP config against approved registry

REGISTRY=".claude/mcp-registry.yaml"
SETTINGS="${HOME}/.claude.json"

if [[ ! -f "$REGISTRY" ]]; then
  exit 0  # No registry = no enforcement (opt-in governance)
fi

# Check for unapproved MCPs (requires yq and jq)
if command -v jq &>/dev/null && command -v yq &>/dev/null; then
  ACTIVE=$(jq -r '.mcpServers | keys[]' "$SETTINGS" 2>/dev/null)
  APPROVED=$(yq e '.approved[].name' "$REGISTRY" 2>/dev/null)

  for mcp in $ACTIVE; do
    if ! echo "$APPROVED" | grep -q "^${mcp}$"; then
      echo "GOVERNANCE WARNING: MCP '${mcp}' is not in approved registry."
      echo "Submit a request at: https://your-internal-wiki/mcp-requests"
      echo "Session continues — please remediate within 48 hours."
    fi
  done
fi

exit 0
```

**注意**：此 hook 只会警告，并不会阻断。在会话启动时阻断会造成过多摩擦。请改用周期性合规检查（参见 §5.3）。

---

## 4. 护栏分级

为四种常见场景预配置的护栏分级。将相应的分级复制到你项目的 `.claude/settings.json` 和 `CLAUDE.md` 中。

### 分级 1：入门级（Starter）

**适用场景**：小型团队（<5 人）、内部项目、无生产数据、合规要求较低。

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./**/*.key)",
      "Read(./**/*.pem)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": ["~/.claude/hooks/dangerous-actions-blocker.sh"]
      }
    ]
  }
}
```

```markdown
<!-- CLAUDE.md additions — Starter tier -->
## Security Basics
- Never read .env files or credential files
- Ask before running destructive commands (DROP, DELETE, rm -rf)
- Follow the codebase's existing patterns
```

**投入**：10 分钟即可完成设置。覆盖基础项。

### 分级 2：标准级（Standard）

**适用场景**：5–20 人团队、与生产环境相邻的代码、存在部分敏感数据、无硬性合规要求。

{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./**/*.key)",
      "Read(./**/*.pem)",
      "Read(./secrets/**)",
      "Bash(cat .env*)",
      "Bash(printenv*)",
      "Edit(docker-compose.yml)",
      "Edit(.github/workflows/**)",
      "Edit(terraform/**)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          "~/.claude/hooks/dangerous-actions-blocker.sh"
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [".claude/hooks/prompt-injection-detector.sh"]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": ["~/.claude/hooks/output-secrets-scanner.sh"]
      }
    ],
    "SessionStart": [
      ".claude/hooks/governance-check.sh"
    ]
  }
}
```

```markdown
<!-- CLAUDE.md additions — Standard tier -->

## 生产环境安全
- 基础设施文件（docker-compose、terraform、CI/CD）已锁定。
  修改前需先请求许可。
- 新增依赖需要 Tech Lead 批准。不要运行 npm install <pkg>。
- 数据库破坏性操作（DROP、DELETE、TRUNCATE）需要确认已备份。

## 代码审查门禁
- 所有涉及认证、支付或数据访问的 AI 生成代码，必须在 PR 描述中
  以 "AI-generated: review required" 注释标记。
```

**投入**：30–45 分钟搭建。覆盖大多数团队。

### Tier 3：Strict

**适用场景**：团队 20 人以上、生产关键系统、客户数据、非正式的合规预期。

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./.env.local)",
      "Read(./**/*.key)",
      "Read(./**/*.pem)",
      "Read(./secrets/**)",
      "Read(**/credentials*)",
      "Bash(cat .env*)",
      "Bash(printenv*)",
      "Bash(env)",
      "Bash(npm install *)",
      "Bash(pnpm add *)",
      "Bash(pip install *)",
      "Edit(docker-compose.yml)",
      "Edit(docker-compose.prod.yml)",
      "Edit(.github/workflows/**)",
      "Edit(terraform/**)",
      "Edit(kubernetes/**)",
      "Edit(prisma/schema.prisma)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          "~/.claude/hooks/dangerous-actions-blocker.sh",
          "~/.claude/hooks/velocity-governor.sh"
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [
          ".claude/hooks/prompt-injection-detector.sh",
          ".claude/hooks/unicode-injection-scanner.sh"
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": ["~/.claude/hooks/output-secrets-scanner.sh"]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [".claude/hooks/session-logger.sh"]
      }
    ],
    "SessionStart": [
      ".claude/hooks/governance-check.sh",
      "~/.claude/hooks/mcp-config-integrity.sh"
    ]
  }
}
```

```markdown
<!-- CLAUDE.md additions — Strict tier -->
## Security Posture: STRICT

You are operating in a strict security environment. Follow these rules without exception.

### Locked Files
These files cannot be modified without explicit permission in this conversation:
- docker-compose.yml, Dockerfile, .github/workflows/**, terraform/**, kubernetes/**
- prisma/schema.prisma (database schema)
- Any file in /src/auth/, /src/payments/, /src/crypto/

### Dependency Protocol
Before adding any dependency:
1. State the dependency name and purpose
2. List 2+ alternatives considered
3. Wait for explicit approval before running any install command

### Data Access Protocol
Before reading any file not in the project root:
1. State the file path and why you need it
2. Wait for approval if the path looks sensitive

### AI Attribution
All code blocks you generate must be prefixed with `// AI-generated` in PRs.
Tests generated by AI must include `// AI-generated test` comment.
```

**投入**：1–2 小时搭建。适用于大多数生产团队。

### Tier 4：Regulated

**适用场景**：金融、医疗、受监管行业。需要满足 HIPAA、SOC2、PCI、ISO27001 合规要求。

此层级在 Strict 之上叠加了合规专属的控制措施。

```json
{
  "permissions": {
    "deny": [
      "Read(./.env*)",
      "Read(./**/*.key)",
      "Read(./**/*.pem)",
      "Read(./secrets/**)",
      "Read(**/credentials*)",
      "Read(**/patient*)",
      "Read(**/phi*)",
      "Read(**/pii*)",
      "Read(**/card*)",
      "Read(**/ssn*)",
      "Bash(cat .env*)",
      "Bash(printenv*)",
      "Bash(env)",
      "Bash(npm install *)",
      "Bash(pnpm add *)",
      "Bash(pip install *)",
      "Bash(curl *)",
      "Bash(wget *)",
      "Edit(docker-compose*.yml)",
      "Edit(.github/workflows/**)",
      "Edit(terraform/**)",
      "Edit(kubernetes/**)",
      "Edit(prisma/schema.prisma)",
      "Edit(**/auth/**)",
      "Edit(**/crypto/**)",
      "Edit(**/encryption/**)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          "~/.claude/hooks/dangerous-actions-blocker.sh",
          "~/.claude/hooks/velocity-governor.sh"
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [
          ".claude/hooks/prompt-injection-detector.sh",
          ".claude/hooks/unicode-injection-scanner.sh"
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          "~/.claude/hooks/output-secrets-scanner.sh",
          ".claude/hooks/session-logger.sh"
        ]
      }
    ],
    "SessionStart": [
      ".claude/hooks/governance-check.sh",
      "~/.claude/hooks/mcp-config-integrity.sh"
    ]
  }
}
```

```markdown
<!-- CLAUDE.md additions — Regulated tier -->
## Compliance Mode: [HIPAA | SOC2 | PCI] — ACTIVE

You are operating under regulatory compliance requirements. These rules are non-negotiable.

### Prohibited Data
NEVER include in your output, suggestions, or examples:
- PHI (patient health information), PII (names, emails, phones in customer context)
- Card numbers, CVVs, bank accounts
- SSNs, tax IDs, government IDs
- Raw authentication tokens, session cookies, API keys

### Mandatory Review Gates
These changes require human approval BEFORE code is committed:
- Any change to authentication or authorization logic
- Any change to encryption or key management
- Any database migration
- Any new external API integration

### Audit Trail
Every session operating on regulated data must have:
- User ID noted at session start ("This session is for: [your-email]")
- Task description at session start ("Task: [brief description]")
- Checkpoint comment at natural breakpoints

### AI Attribution (Mandatory for Regulated)
All AI-generated code must include:
- `// AI-generated: [date] [model] [reviewer]` comment
- PR description must include AI disclosure section
```

**面向受监管环境的额外工具**：可以考虑使用 Entire CLI 来实现带审批门禁的完整会话审计追踪。详见 [AI Traceability §5.1](../ops/ai-traceability.md#51-entire-cli)，其中包含细节说明和一份 go/no-go 评估检查清单。

---

## 5. 规模化的策略执行

拥有策略与执行策略并不是一回事。本节介绍如何让治理在一个 10–100 人的开发团队中真正落地。

### 5.1 配置分发

**核心原则**：治理配置应存放在仓库中，而不是各个开发者的机器上。

```
your-org-config/                 ← separate "platform config" repo
├── .claude/
│   ├── settings.json            ← shared settings (tier-based)
│   ├── mcp-registry.yaml        ← approved MCPs
│   ├── hooks/
│   │   ├── governance-check.sh  ← MCP registry check
│   │   ├── session-logger.sh    ← audit trail
│   │   └── velocity-governor.sh ← rate limiting
│   └── agents/
│       └── security-reviewer.md ← shared agent for code review
├── templates/
│   ├── CLAUDE.md.starter        ← per-tier CLAUDE.md templates
│   ├── CLAUDE.md.standard
│   ├── CLAUDE.md.strict
│   └── CLAUDE.md.regulated
└── scripts/
    └── setup-project.sh         ← bootstraps new project with correct tier
```

**初始化一个新项目**：

```bash
#!/bin/bash
# scripts/setup-project.sh
# Usage: ./setup-project.sh [starter|standard|strict|regulated]

TIER=${1:-standard}
CONFIG_REPO="https://github.com/your-org/claude-code-config"

echo "Setting up Claude Code governance: $TIER tier"

# Create .claude directory
mkdir -p .claude/hooks

# Copy tier config
curl -s "$CONFIG_REPO/raw/main/templates/.claude/settings.${TIER}.json" \
  -o .claude/settings.json

# Copy CLAUDE.md template
curl -s "$CONFIG_REPO/raw/main/templates/CLAUDE.md.${TIER}" \
  -o CLAUDE.md

# Copy governance hooks
curl -s "$CONFIG_REPO/raw/main/hooks/governance-check.sh" \
  -o .claude/hooks/governance-check.sh
chmod +x .claude/hooks/governance-check.sh

echo "Done. Commit .claude/ and CLAUDE.md to your repo."
```

### 5.2 入职检查清单

加入使用 Claude Code 团队的新开发者应完成以下检查清单：

```markdown
## Claude Code Onboarding Checklist

### Setup (30 minutes)
- [ ] Install Claude Code: `npm i -g @anthropic-ai/claude-code`
- [ ] Configure global safety hooks: `./scripts/install-global-hooks.sh`
- [ ] Verify project config loads: `claude` then ask "What tier is this project?"
- [ ] Read the AI Usage Charter (link to your doc)
- [ ] Review approved MCP list: `.claude/mcp-registry.yaml`

### Security Basics
- [ ] Confirm `~/.claude/settings.json` has no `permissions.allow` overrides
  that bypass project's deny rules
- [ ] Confirm no personal MCP servers running that access production data
- [ ] Know how to report a data exposure: security@[company]

### First Week
- [ ] Complete one task with Claude Code (bug fix, small feature)
- [ ] Submit at least one PR with proper AI attribution section
- [ ] Flag any friction points to Tech Lead for config improvement

### Quarterly
- [ ] Participate in MCP registry review
- [ ] Review AI Usage Charter updates
- [ ] Confirm no personal config overrides in place
```

### 5.3 合规检查

自动化的周期性合规检查，用于检测配置漂移：

```bash
#!/bin/bash
# scripts/claude-governance-audit.sh
# Run weekly via CI/CD or cron

PASS=0
FAIL=0
WARN=0

check() {
  local name="$1"
  local result="$2"
  local severity="${3:-FAIL}"

  if [[ "$result" == "OK" ]]; then
    echo "  PASS: $name"
    ((PASS++))
  else
    echo "  $severity: $name — $result"
    [[ "$severity" == "FAIL" ]] && ((FAIL++)) || ((WARN++))
  fi
}

echo "=== Claude Code Governance Audit ==="
echo ""

# Check: settings.json present and committed
echo "1. Repository Config"
[[ -f ".claude/settings.json" ]] \
  && check "settings.json present" "OK" \
  || check "settings.json present" "Missing — team config not enforced" "FAIL"

git ls-files --error-unmatch .claude/settings.json &>/dev/null \
  && check "settings.json committed" "OK" \
  || check "settings.json committed" "Not tracked by git — won't apply to team" "WARN"

# Check: deny rules for secrets
echo ""
echo "2. Secret Protection"
if [[ -f ".claude/settings.json" ]]; then
  jq -e '.permissions.deny[]? | select(test("env|pem|key"))' \
    .claude/settings.json &>/dev/null \
    && check ".env protection rules" "OK" \
    || check ".env protection rules" "No deny rules for .env or key files" "FAIL"
fi

# Check: hooks installed and executable
echo ""
echo "3. Hook Stack"
for hook in ".claude/hooks/governance-check.sh"; do
  if [[ -f "$hook" ]]; then
    [[ -x "$hook" ]] \
      && check "$hook executable" "OK" \
      || check "$hook executable" "Not executable — run chmod +x $hook" "FAIL"
  else
    check "$hook present" "Missing" "WARN"
  fi
done

# Check: MCP registry present
echo ""
echo "4. MCP Governance"
[[ -f ".claude/mcp-registry.yaml" ]] \
  && check "MCP registry present" "OK" \
  || check "MCP registry present" "No registry — MCP usage ungoverned" "WARN"

# Check: CLAUDE.md present and committed
echo ""
echo "5. Documentation"
[[ -f "CLAUDE.md" ]] || [[ -f ".claude/CLAUDE.md" ]] \
  && check "CLAUDE.md present" "OK" \
  || check "CLAUDE.md present" "Missing — no project context for AI" "WARN"

echo ""
echo "=== Summary ==="
echo "  Passed:   $PASS"
echo "  Failed:   $FAIL (must fix)"
echo "  Warnings: $WARN (should fix)"
echo ""

[[ $FAIL -gt 0 ]] && exit 1 || exit 0
```

### 5.4 基于角色的护栏

不同开发者有不同的风险画像。应相应地定制 Claude Code 设置。

**做法：在 CLAUDE.md 中按经验/角色分级**

```markdown
<!-- CLAUDE.md — role-aware guidelines -->
## Developer Context

This is a [JUNIOR|SENIOR|LEAD] developer project context.

### If JUNIOR (< 1 year at company)
- Always confirm architecture decisions before implementing
- Do not modify database schemas, migrations, or auth code without pairing with a senior
- Every PR must have a human reviewer check the AI-generated sections explicitly
- Use /plan mode before implementing anything > 50 lines

### If SENIOR (1+ years at company)
- Standard review applies
- Can modify most files, but auth/payment/crypto still require lead review
- AI attribution in PRs required

### If LEAD/PRINCIPAL
- Full access, judgment-based restrictions
- Responsible for setting guardrail tier for their team projects
- Must conduct quarterly MCP registry review
```

**做法：每个环境使用不同的 settings.json**

在 CI/CD 中，于流水线启动时检查活动的 `settings.json` 路径，以强制使用正确的分级。Claude Code 会从项目根目录读取 `.claude/settings.json`——将你的严格分级配置提交到那里，这样无论开发者本地有什么，CI 始终都会采用它。

```bash
# In your CI pipeline setup step, verify the correct tier is committed
if ! grep -q '"Bash(curl \*)"' .claude/settings.json; then
  echo "ERROR: CI requires Regulated-tier settings.json (curl must be denied)"
  exit 1
fi
```

### 5.5 CI/CD 门禁

阻止不合规的 AI 使用进入生产环境：

```yaml
# .github/workflows/ai-governance.yml
name: AI Governance Check

on: [pull_request]

jobs:
  governance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check governance config present
        run: |
          if [[ ! -f ".claude/settings.json" ]]; then
            echo "::error::Missing .claude/settings.json — governance config required"
            exit 1
          fi

      - name: Check no credential access permissions
        run: |
          if jq -e '.permissions.allow[]? | select(test("env|pem|key|secret"))' \
            .claude/settings.json 2>/dev/null; then
            echo "::error::Dangerous permissions.allow detected — credentials may be exposed"
            exit 1
          fi

      - name: Run governance audit
        run: |
          chmod +x scripts/claude-governance-audit.sh
          ./scripts/claude-governance-audit.sh

      - name: Check AI attribution in PR description
        if: ${{ env.REQUIRE_AI_ATTRIBUTION == 'true' }}
        uses: actions/github-script@v7
        with:
          script: |
            const body = context.payload.pull_request.body || '';
            const hasAttribution = body.includes('AI') ||
                                   body.includes('Claude') ||
                                   body.includes('AI-generated');
            if (!hasAttribution) {
              core.warning('No AI attribution section found. Please disclose AI usage.');
            }
```

---

## 6. 审计、合规与治理结构

### 6.1 SOC2 和 ISO27001 审计员实际会问什么

审计员审查 AI 编码工具的使用情况时，通常会寻找以下控制措施的证据：

| 审计员的问题 | 他们想看到什么 | Claude Code 实现方式 |
|-----------------|----------------------|---------------------------|
| "你们有 AI 工具使用政策吗？" | 书面章程，已签署/已确认 | `docs/ai-usage-charter.md` + 入职检查清单 |
| "你们如何控制发送给 AI 供应商的数据？" | 数据分类 + 技术控制 | 对敏感文件使用 `permissions.deny` |
| "你们如何审查第三方 AI 组件？" | 审批流程 + 注册表 | MCP 注册表 + 审批流程 |
| "你们有 AI 操作的审计追踪吗？" | 工具调用、访问文件的日志 | 会话 JSONL 日志 + `compliance-audit-logger.sh` |
| "你们如何审查 AI 生成的代码？" | 带有 AI 披露的代码审查流程 | PR 模板 + 署名政策 |
| "发生事件时会怎样？" | 事件响应流程 | 现有 IR 流程 + AI 专项补充 |

**对于 SOC2 具体而言**：相关的信任服务标准是 CC6.1（逻辑访问控制）、CC6.3（访问移除）、CC7.1（监控）和 CC9.2（供应商风险）。你的 Claude Code 治理应映射到这些标准。

**对于 ISO27001 具体而言**：相关的附录 A 控制项包括 A.8.3（信息访问限制）、A.8.24（密码学的使用）、A.8.25（安全开发生命周期）和 A.5.23（云服务使用的信息安全）。

### 6.2 审计追踪设置

Claude Code 会话已经被记录到 `~/.claude/projects/<project>/*.jsonl`。挑战在于让它们：
1. 事后可访问（开发者离职时不会丢失）
2. 防篡改（无法被追溯修改）
3. 可供审计目的查询

**最小化审计追踪（无需额外工具）**：

```bash
#!/bin/bash
# .claude/hooks/compliance-audit-logger.sh
# Event: PostToolUse (all tools)
# Appends structured audit entries to a shared log

LOG_DIR="${COMPLIANCE_LOG_DIR:-/var/log/claude-audit}"
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d).jsonl"

mkdir -p "$LOG_DIR"

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool.name // "unknown"')
USER=$(whoami)
PROJECT=$(basename "$PWD")
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "{\"timestamp\":\"$TIMESTAMP\",\"user\":\"$USER\",\"project\":\"$PROJECT\",\"tool\":\"$TOOL\"}" \
  >> "$LOG_FILE"
```

**将日志传送到不可变存储**（推荐用于受监管环境）：

```bash
# Daily: sync session logs to immutable bucket
aws s3 sync ~/.claude/projects/ \
  s3://your-audit-bucket/claude-sessions/$(whoami)/ \
  --storage-class GLACIER_INSTANT_RETRIEVAL \
  --exclude "*.tmp"
```

**对于带有审批门控的完整合规审计追踪**，可考虑 Entire CLI——它捕获完整的会话上下文（提示、推理、工具调用、文件差异），并以加密方式与 git 提交链接。设置和评估标准请参见 [AI 可追溯性 §5.1](../ops/ai-traceability.md#51-entire-cli)。这只是众多选项中的一种工具；请根据你的具体合规需求进行评估。

### 6.3 AI 治理委员会（精简参考）

对于大规模管理 AI 风险的组织，一个轻量级的 AI 治理委员会能提供审计员所期望的问责结构。这是一种协调机制，而非瓶颈。

**最小化结构**（适用于 10–100 名开发者）：

| 角色 | 人员 | 职责 |
|------|--------|----------------|
| **治理负责人** | 工程经理或主管 | 政策更新、季度审查、升级处理 |
| **安全代表** | 安全工程师或 DevSecOps | MCP 风险审查、事件响应 |
| **开发代表** | 资深开发者轮值（任期 3 个月） | 开发者反馈、可用性平衡 |
| **合规代表** | 法务/合规（仅受监管时） | 章程、监管映射 |

**会议节奏**：每季度一次（30 分钟）。固定议程：
1. MCP 注册表审查——有什么需要添加、移除或标记的吗？
2. 事件审查——自上次会议以来有任何与 AI 相关的安全事件吗？
3. 政策更新——是否需要修改章程？
4. 指标——治理审计结果、合规检查状态

有关详细的 AI 治理委员会结构、RACI 矩阵和合规映射，请参见白皮书 #11：企业 AI 治理（FR/EN）。

### 6.4 合规监控

治理的可观测性层在 [observability.md](../ops/observability.md) 中介绍。针对合规具体而言，以下监控查询最为相关：

```bash
# Which files did Claude access in the last 30 days?
# macOS: date -v-30d; Linux: date -d '30 days ago'
if [[ "$OSTYPE" == "darwin"* ]]; then
  SINCE=$(date -v-30d +%Y-%m-%d)
else
  SINCE=$(date -d '30 days ago' +%Y-%m-%d)
fi

find ~/.claude/projects/ -name "*.jsonl" -newer "$SINCE" | \
  xargs jq -r 'select(.type == "assistant") |
    .message.content[]? |
    select(.type == "tool_use" and .name == "Read") |
    .input.file_path' 2>/dev/null | sort -u

# Any access to sensitive patterns?
# (Run after the above, pipe through grep)
grep -E '\.(env|pem|key)$|secrets/|credentials'

# Bash commands run by Claude this week
if [[ "$OSTYPE" == "darwin"* ]]; then
  SINCE_WEEK=$(date -v-7d +%Y-%m-%d)
else
  SINCE_WEEK=$(date -d '7 days ago' +%Y-%m-%d)
fi

find ~/.claude/projects/ -name "*.jsonl" -newer "$SINCE_WEEK" | \
  xargs jq -r 'select(.type == "assistant") |
    .message.content[]? |
    select(.type == "tool_use" and .name == "Bash") |
    .input.command' 2>/dev/null | sort
```

---

## 快速参考

### 层级选择

| 你的情况 | 层级 | 设置时间 |
|----------------|------|------------|
| 副业项目、个人使用 | Starter | 10 分钟 |
| 小团队、内部项目 | Starter | 10 分钟 |
| 5–20 人团队、任何生产代码 | Standard | 45 分钟 |
| 20 人以上团队、客户数据 | Strict | 2 小时 |
| 受监管行业（HIPAA/SOC2/PCI） | Regulated | 半天 |

### 治理成熟度等级

| 成熟度 | 你拥有什么 | 缺少什么 |
|----------|---------------|----------------|
| **临时性** | 每个开发者自行配置 | 一致性、问责制 |
| **基础** | 共享的 CLAUDE.md + settings.json | MCP 治理、审计追踪 |
| **受管理** | + MCP 注册表 + hooks | 合规报告 |
| **合规** | + 审计日志 + 章程 + 审查周期 | 无关键缺失 |
| **已审计** | + 外部验证 + 可追溯性 | — |

### 常见错误

| 错误 | 修复 |
|---------|-----|
| 治理仅存在于 `~/.claude`（个人） | 移至代码库中的 `.claude/` |
| `permissions.allow` 覆盖了团队的 `deny` | 每季度审查个人配置 |
| 没有 MCP 注册表 → 每个开发者添加不同的 MCP | 即使只有 3 个条目也要建立注册表 |
| CLAUDE.md 过长 → Claude 忽略规则 | 保持在 8KB 以内，优先考虑关键规则 |
| 审计员索要 AI 日志 → 什么都没保存 | 设置会话日志同步到 S3 |

---

## 另请参阅

- [安全加固](./security-hardening.md) — 开发者个人安全：MCP CVE、注入防御、5 分钟审计
- [生产安全规则](./production-safety.md) — 面向生产团队的 6 条不可妥协规则（端口、数据库安全、基础设施锁定）
- [数据隐私指南](./data-privacy.md) — Claude Code 向 Anthropic 发送哪些数据、保留政策
- [AI 可追溯性](../ops/ai-traceability.md) — 署名政策、Entire CLI、git-ai、合规框架
- [可观测性](../ops/observability.md) — 会话监控、成本追踪、活动审计查询
- [采用方法](../roles/adoption-approaches.md) — 团队推广模式、CLAUDE.md 策略
- [MCP 注册表模板](../../examples/scripts/mcp-registry-template.yaml) — 即用型注册表格式
- [治理 Hook](../../examples/hooks/bash/governance-enforcement-hook.sh) — 根据政策验证配置的 hook
- [AI 使用章程模板](../../examples/scripts/ai-usage-charter-template.md) — 可直接调整的章程模板

---

## 参考文献

- [Liminal AI 企业治理指南](https://www.liminal.ai/blog/enterprise-ai-governance-guide) — 实践落地
- [Databricks AI 治理框架](https://www.databricks.com/blog/practical-ai-governance-framework-enterprises) — 企业级框架
- [Augmentcode AI 代码治理](https://www.augmentcode.com/guides/ai-code-governance-framework-for-enterprise-dev-teams) — 针对开发团队
- [Partnership on AI — 2026 年六大治理优先事项](https://partnershiponai.org/resource/six-governance-priorities/) — 评估框架、问责制
- [欧盟 AI 法案](https://www.europarl.europa.eu/doceo/document/TA-9-2024-0138_EN.html) — 高风险 AI 系统的紧急停止开关要求
- [NIST AI RMF](https://airc.nist.gov/RMF/Overview) — 风险管理框架
- [SOC2 信任服务标准](https://www.aicpa.org/resources/article/soc-2-trust-services-criteria) — CC6.1、CC7.1、CC9.2

---

*版本 1.0.0 | 2026 年 3 月 | [Claude Code 终极指南](../README.md) 的一部分*
