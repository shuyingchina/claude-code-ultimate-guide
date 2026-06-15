---
title: "Agent Evaluation"
description: "Metrics, patterns, and tools for measuring custom agent effectiveness"
tags: [agents, testing, guide]
---

# Agent 评估

**快速导航**：[为什么要评估？](#why-evaluate-agents) · [需要追踪的指标](#metrics-to-track) · [实现](#implementation-patterns) · [示例](#example-agent-with-evaluation) · [工具](#tools--references)

---

## 为什么要评估 Agent？

当你在 `.claude/agents/` 中创建自定义 agents 时，你正在将专业化的专业知识编码进可复用的工作流。但你如何知道自己的 agents 是否真的有效？

**没有评估**，你就是在盲目地构建：
- ❌ 无法衡量 agent 的回复是随时间改善还是退化
- ❌ 无法客观地比较不同的 agent 配置
- ❌ 难以识别 agent 上下文/指令中哪些方面需要改进
- ❌ 没有数据来证明在 agent 开发上的投入是合理的

**有了评估**，你就能充满信心地迭代：
- ✅ 通过指标（响应时间、准确率、工具使用情况）量化 agent 质量
- ✅ 以可衡量的结果对不同 agent 配置进行 A/B 测试
- ✅ 识别成功与失败交互中的模式
- ✅ 建立持续改进的反馈循环

**核心原则**：Agents 即代码。和所有代码一样，它们需要测试、指标和可观测性。

---

## 需要追踪的指标

### 1. 回复质量指标

**衡量什么**：
- **任务完成率**：agent 是否达成了既定目标？
- **正确性**：agent 的输出在事实层面是否准确？
- **相关性**：回复是否切题并解决了实际问题？
- **幻觉率**：agent 编造信息的频率有多高？

**如何追踪**：
```bash
# Post-response hook: .claude/hooks/log-response-quality.sh
# Triggered after each agent response

# Log structure:
{
  "timestamp": "2026-02-10T14:32:00Z",
  "agent_id": "backend-architect",
  "task_completed": true,
  "correctness_score": 4.5,  # User rating 1-5
  "hallucinations": 0,
  "response_tokens": 1250
}
```

**实现提示**：使用用户反馈提示（点赞/点踩）或自动化检查（agent 生成代码后测试套件通过）。

---

### 2. 工具使用指标

**衡量什么**：
- **工具调用成功率**：执行无误的工具调用所占的百分比
- **工具选择准确率**：agent 是否为任务选择了正确的工具？
- **工具调用效率**：达成目标所需的最少调用次数（避免不必要的读取/搜索）
- **错误恢复**：agent 是否优雅地处理了工具失败？

**如何追踪**：
```bash
# Post-tool-use hook: .claude/hooks/log-tool-usage.sh
# Triggered after each tool call

# Log structure:
{
  "timestamp": "2026-02-10T14:32:05Z",
  "agent_id": "backend-architect",
  "tool_name": "Read",
  "tool_success": true,
  "tool_parameters": {"file_path": "src/auth.ts"},
  "execution_time_ms": 45
}
```

**实现提示**：使用 Claude Code hooks 系统（参见 `examples/hooks/`）自动记录工具调用。

---

### 3. 性能指标

**衡量什么**：
- **响应时间**：从用户提示到完整回复的总时长
- **Token 效率**：每个任务使用的输入/输出 tokens
- **上下文利用率**：使用了多少上下文窗口？
- **每任务成本**：整个交互的 API 成本

**如何追踪**：
```bash
# Session-end hook: .claude/hooks/log-performance.sh
# Triggered at end of session

# Log structure:
{
  "timestamp": "2026-02-10T14:35:00Z",
  "agent_id": "backend-architect",
  "session_duration_s": 180,
  "input_tokens": 3500,
  "output_tokens": 2800,
  "total_cost_usd": 0.15,
  "context_utilization": 0.42
}
```

**实现提示**：解析 Claude Code 会话日志或使用 MCP 可观测性工具。

---

### 4. 用户满意度指标

**衡量什么**：
- **显式反馈**：用户评分、评论、bug 报告
- **隐式信号**：用户是否采纳了 agent 的建议？他们是否重试了提示？
- **采用率**：相比其他选择，这个 agent 被使用的频率有多高？
- **留存率**：用户是否会回头使用这个 agent 处理类似任务？

**如何追踪**：
```bash
# Manual feedback collection
# After agent completes task, prompt user:
"Rate this agent's performance (1-5): _"

# Log:
{
  "timestamp": "2026-02-10T14:35:10Z",
  "agent_id": "backend-architect",
  "user_rating": 5,
  "user_comment": "Perfect analysis of auth flow",
  "would_use_again": true
}
```

**实现提示**：在 agent 模板中添加反馈提示，或使用会话后调查问卷。

---

## 实现模式

### 模式 1：日志 Hook 系统

**使用场景**：无需人工干预，自动追踪所有 agent 交互

**设置**：
```bash
# .claude/hooks/post-tool-use.sh
#!/bin/bash
# Triggered after every tool call

AGENT_ID=$(echo "$CLAUDE_AGENT_ID" | jq -r)
TOOL_NAME=$(echo "$CLAUDE_TOOL_NAME" | jq -r)
TOOL_SUCCESS=$(echo "$CLAUDE_TOOL_SUCCESS" | jq -r)

# Append to metrics log
echo "{\"timestamp\":\"$(date -Iseconds)\",\"agent\":\"$AGENT_ID\",\"tool\":\"$TOOL_NAME\",\"success\":$TOOL_SUCCESS}" \
  >> .claude/logs/agent-metrics.jsonl
```

**优点**：零人工开销、覆盖全面、时间序列数据
**缺点**：需要解析 Claude Code 环境变量（可能随版本变化）

---

### 模式 2：Agent 单元测试

**使用场景**：回归测试，确保 agent 的改进不会破坏现有能力

**设置**：
```bash
# tests/agents/backend-architect.test.sh
#!/bin/bash

# Test 1: Agent correctly identifies hexagonal architecture layers
echo "Test: Hexagonal architecture analysis"
RESULT=$(claude agent backend-architect "Analyze src/auth.ts for layer violations")
if echo "$RESULT" | grep -q "domain layer"; then
  echo "✅ PASS: Identified layers"
else
  echo "❌ FAIL: Did not identify layers"
  exit 1
fi

# Test 2: Agent recommends correct patterns
echo "Test: Pattern recommendations"
RESULT=$(claude agent backend-architect "Improve error handling in src/api.ts")
if echo "$RESULT" | grep -q "Result<T, E>"; then
  echo "✅ PASS: Recommended Result pattern"
else
  echo "❌ FAIL: Incorrect pattern"
  exit 1
fi
```

**优点**：自动化、能捕捉回归、可集成 CI/CD
**缺点**：需要维护，可能出现误报/漏报

---

### 模式 3：A/B 测试配置

**使用场景**：比较 agent 的两个版本，确定哪个表现更好

**设置**：
```yaml
# .claude/agents/backend-architect-v1.md (control)
name: backend-architect
version: 1.0
instructions: |
  You are a backend architect specializing in...
  [original instructions]

# .claude/agents/backend-architect-v2.md (experiment)
name: backend-architect-v2
version: 2.0
instructions: |
  You are a backend architect specializing in...
  [modified instructions with new pattern emphasis]
```

**评估**：
```bash
# Run same task with both agents, compare metrics
# Task: "Analyze src/auth.ts for security issues"

# Version 1 metrics:
# - Response time: 45s
# - Issues found: 3
# - User rating: 4/5

# Version 2 metrics:
# - Response time: 38s
# - Issues found: 5 (2 additional critical issues)
# - User rating: 5/5

# Conclusion: Version 2 is more thorough and faster → promote to production
```

**优点**：数据驱动的决策、可量化的改进
**缺点**：需要纪律性来开展受控实验

---

### 模式 4：反馈循环集成

**使用场景**：基于真实使用数据持续改进 agent

**设置**：
```bash
# After agent completes task
echo "How would you rate this response? (1-5, or 'skip'): "
read RATING

if [ "$RATING" != "skip" ]; then
  echo "Any specific feedback?: "
  read COMMENT

  # Log feedback
  echo "{\"timestamp\":\"$(date -Iseconds)\",\"agent\":\"$AGENT_ID\",\"rating\":$RATING,\"comment\":\"$COMMENT\"}" \
    >> .claude/logs/agent-feedback.jsonl
fi

# Weekly: Review feedback.jsonl, identify patterns
# Monthly: Update agent instructions based on aggregated feedback
```

**优点**：使 agent 与用户的实际需求对齐、识别边界情况
**缺点**：需要人工审阅反馈并据此采取行动

---

## 示例：带评估的 Agent

**完整模板可用**：[`examples/agents/analytics-with-eval/`](../../examples/agents/analytics-with-eval/) 包含完整的 agent 定义、hooks、分析脚本和报告模板。

### 配置：内置度量指标的分析 Agent

```yaml
# .claude/agents/analytics-agent.md
---
name: analytics-agent
description: SQL query generator with evaluation hooks
version: 1.0
tools:
  - Read
  - Write
  - Bash
hooks:
  post_response: .claude/hooks/log-analytics-metrics.sh
---

# Analytics Agent

You are an expert SQL analyst helping users query databases.

## Evaluation Criteria

After each query:
1. **Correctness**: Does query produce expected results?
2. **Performance**: Query execution time < 5s?
3. **Safety**: No destructive operations (DELETE, DROP, TRUNCATE)?
4. **Best practices**: Uses proper JOINs, indexes, parameterized queries?

## Instructions

[... agent instructions ...]
```

### 度量指标 Hook

```bash
# .claude/hooks/log-analytics-metrics.sh
#!/bin/bash
# Triggered after analytics-agent response

# Extract query from response (naive grep, improve with jq)
QUERY=$(echo "$CLAUDE_RESPONSE" | grep -oP 'SELECT.*?;')

if [ -n "$QUERY" ]; then
  # Test query (requires database connection)
  EXEC_TIME=$( (time psql -U user -d db -c "$QUERY") 2>&1 | grep real | awk '{print $2}')

  # Check for destructive operations
  if echo "$QUERY" | grep -iE 'DELETE|DROP|TRUNCATE'; then
    SAFETY="FAIL"
  else
    SAFETY="PASS"
  fi

  # Log metrics
  echo "{\"timestamp\":\"$(date -Iseconds)\",\"query\":\"$QUERY\",\"exec_time\":\"$EXEC_TIME\",\"safety\":\"$SAFETY\"}" \
    >> .claude/logs/analytics-metrics.jsonl
fi
```

### 分析

```bash
# Monthly review: Analyze metrics
jq -s 'group_by(.safety) | map({safety: .[0].safety, count: length})' \
  .claude/logs/analytics-metrics.jsonl

# Output:
# [
#   {"safety": "PASS", "count": 127},
#   {"safety": "FAIL", "count": 3}
# ]

# Action: Review 3 failed queries, update agent instructions to prevent future violations
```

---

## 工具与参考资料

### 开源评估框架

#### nao（分析 Agents）

**URL**：[github.com/getnao/nao](https://github.com/getnao/nao/)

**提供的功能**：
- 面向分析 agents 的内置评估框架
- 针对 agent 响应的单元测试能力
- 度量指标采集（响应质量、工具使用、性能）
- 反馈循环集成

**如何适配到 Claude Code**：
- **上下文构建器模式**：将 nao 的结构化上下文方法应用到 `.claude/agents/` 配置
- **评估 hooks**：将 nao 的评估框架转换为 Claude Code 的 hooks 系统
- **度量指标 schema**：把 nao 的度量指标 schema 用作你日志的模板

**状态**：生产就绪，积极维护，TypeScript + Python

---

### Claude Code 原生模式

**Hooks 系统**：使用 `.claude/hooks/` 实现自动化日志记录（参见 `examples/hooks/README.md`）

**Agents 目录**：使用 `.claude/agents/` 存放自定义 agent 定义（参见 `guide/ultimate-guide.md` 第 4 节）

**MCP 可观测性**：使用 MCP 服务器实现高级日志记录与度量指标聚合

---

## 最佳实践

### 从简单开始

**第 1 周**：添加基础日志 hook（仅记录工具调用）
**第 2 周**：添加用户反馈提示（手动评分）
**第 3 周**：搭建仪表盘以可视化度量指标
**第 4 周**：对 agent 配置运行第一次 A/B 测试

### 聚焦可操作的度量指标

不要追踪你不会据此采取行动的指标。优先考虑：
1. **任务完成率** → 优化 agent 指令
2. **工具调用错误** → 改进上下文或补充示例
3. **用户评分** → 识别令人困惑或无帮助的响应

### 尽可能自动化

手动评估无法规模化。可使用：
- 用 hooks 实现自动日志记录
- 用 CI/CD 集成进行 agent 单元测试
- 用脚本进行周期性度量指标聚合

### 构建反馈循环

度量指标若不付诸行动则毫无意义：
- 每周：审查度量指标，识别规律
- 每月：基于数据更新 agent 指令
- 每季度：必要时进行 agent 的大规模重构

---

## 相关章节

- **[Agents](#4-agents)**：创建自定义 agents
- **[Hooks](#7-hooks)**：使用事件 hooks 实现自动化
- **[可观测性](../ops/observability.md)**：日志记录与监控策略
- **[AI 生态系统](../ecosystem/ai-ecosystem.md#82-domain-specific-agent-frameworks)**：如 nao 之类的外部框架

---

**后续步骤**：
1. 为你最常用的 agent 添加日志 hook
2. 采集 1 周的度量指标
3. 基于数据分析并优化 agent

**模板**：参见 `examples/agents/analytics-with-eval/` 获取包含 hooks、脚本和报告模板的完整实现
