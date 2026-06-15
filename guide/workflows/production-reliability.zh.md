---
title: "Production Reliability Patterns"
description: "Escalation design, circuit breakers, structured error propagation, graceful degradation, human handoff, and source conflict resolution for Claude-powered systems"
tags: [workflow, reliability, production, escalation, circuit-breaker, error-handling]
---

# 生产环境可靠性模式

> **可信度**：Tier 2。这些模式源自生产环境部署。核心设计原则是稳定的；具体的阈值和字段名会因系统而异。

由 Claude 驱动的系统，其失败方式与传统软件不同。模型可能产生语法上有效但语义上错误的输出，可能在无法取得进展时拒绝继续，也可能在源数据不完整时产生部分结果。本指南涵盖了在生产环境中应对这些失败模式的可靠性模式。

---

## 目录

1. [升级设计](#escalation-design)
2. [熔断器模式](#circuit-breaker-pattern)
3. [结构化错误传播](#structured-error-propagation)
4. [部分结果与覆盖范围标注](#partial-results-and-coverage-annotations)
5. [结构化人工接管](#structured-human-handoff)
6. [来源冲突解决](#source-conflict-resolution)
7. [反模式](#anti-patterns)
8. [另请参阅](#see-also)

---

## 升级设计

最常见的可靠性错误，就是把 LLM 的置信度分数当作主要的升级信号。置信度分数并不是经过校准的概率：模型可能在事实上完全错误的同时输出一个很高的置信度值。生产环境中的升级应当由程序化信号驱动，而不是由数值化的置信度值驱动。

### 三种典型的升级触发条件

在一个设计良好的系统中，当且仅当三种条件之一被满足时，才会发生升级。

**1. 用户明确请求：** 客户明确要求转接人工。这一点没有商量余地，并且优先于所有其他信号，包括挫败感检测。"我要和人工对话"与愤怒语气是不同的信号，无论 AI 接下来本可以做什么，它都要求立即接管。

**2. 策略缺口：** 请求超出了系统定义的范围，无法由任何可用的工具或知识来处理。这不是模型失败；这是范围边界。正确的应对方式是带上下文的结构化升级，而不是不断道歉的循环。

**3. 无法取得进展：** 在经过定义数量的尝试或工具调用后，系统仍未产生有效结果。这是以程序化方式衡量的：重试预算耗尽、熔断器打开，或验证循环失败。

### 程序化升级信号

```python
from enum import Enum
from dataclasses import dataclass

class EscalationReason(Enum):
    EXPLICIT_REQUEST = "explicit_request"
    POLICY_GAP = "policy_gap"
    MAX_RETRIES_EXCEEDED = "max_retries_exceeded"
    CIRCUIT_BREAKER_OPEN = "circuit_breaker_open"
    MISSING_REQUIRED_TOOL = "missing_required_tool"

@dataclass
class EscalationSignal:
    should_escalate: bool
    reason: EscalationReason | None
    context: dict

def evaluate_escalation(
    user_message: str,
    attempt_count: int,
    policy_coverage: str,  # "covered" | "gap" | "out_of_scope"
    max_attempts: int = 3
) -> EscalationSignal:

    # Priority 1: explicit user request, check first, unconditionally
    if contains_explicit_escalation_request(user_message):
        return EscalationSignal(
            should_escalate=True,
            reason=EscalationReason.EXPLICIT_REQUEST,
            context={"trigger": "user_stated_intent"}
        )

    # Priority 2: policy gap
    if policy_coverage in ("gap", "out_of_scope"):
        return EscalationSignal(
            should_escalate=True,
            reason=EscalationReason.POLICY_GAP,
            context={"coverage": policy_coverage}
        )

    # Priority 3: inability to progress
    if attempt_count >= max_attempts:
        return EscalationSignal(
            should_escalate=True,
            reason=EscalationReason.MAX_RETRIES_EXCEEDED,
            context={"attempts": attempt_count, "max": max_attempts}
        )

    return EscalationSignal(should_escalate=False, reason=None, context={})

def contains_explicit_escalation_request(message: str) -> bool:
    explicit_phrases = [
        "speak to a human", "talk to a person", "real agent",
        "human agent", "transfer me", "escalate this",
        "supervisor", "manager"
    ]
    message_lower = message.lower()
    return any(phrase in message_lower for phrase in explicit_phrases)
```

### 挫败感 vs 明确升级请求

这是两个完全不同的信号，需要相反的应对方式。挫败感（愤怒语气、反复提问、"这毫无用处"）是一个信号，表明应当带着共情去回应，并尝试不同的方法。而明确的升级请求（"我要和真人对话"）则是一个信号，表明应当立即接管。

把两者混为一谈是一个常见错误，且会带来实际后果：在用户只是想要更好答案时却把沮丧的用户转给人工，或者在用户已经决定要人工坐席时却仍然更努力地继续尝试。

```python
def classify_user_signal(message: str) -> dict:
    # These patterns can coexist: check both independently
    frustration_markers = [
        "this is ridiculous", "not helpful", "keep asking",
        "not answering", "useless", "terrible", "waste"
    ]
    escalation_markers = [
        "speak to a human", "real person", "agent", "transfer",
        "supervisor", "escalate", "don't want ai"
    ]

    message_lower = message.lower()

    return {
        "frustrated": any(m in message_lower for m in frustration_markers),
        "wants_escalation": any(m in message_lower for m in escalation_markers)
    }

# Usage:
signals = classify_user_signal(user_message)

if signals["wants_escalation"]:
    initiate_human_handoff(context)   # immediate, unconditional
elif signals["frustrated"]:
    adjust_response_approach()        # more empathetic, different angle
```

### 基于规则、从结构化输出进行路由

只要有可能，就应当从结构化输出字段而非模型级置信度来推导升级决策。如果模型产生了一个带有 `policy_gap: true` 或 `requires_human_review: true` 的结构化结果，那么这些字段就是确定性的路由信号，无需任何置信度分数的解读。

```python
@dataclass
class AgentDecision:
    response_text: str
    policy_gap: bool
    requires_human_review: bool
    coverage_level: str  # "full" | "partial" | "none"
    missing_information: list[str]

def route_from_structured_output(decision: AgentDecision) -> str:
    if decision.policy_gap or decision.coverage_level == "none":
        return "escalate"
    if decision.requires_human_review or decision.coverage_level == "partial":
        return "queue_for_review"
    return "respond"
```

---

## 熔断器模式

熔断器可以防止一个失败的依赖（API、工具、外部服务）造成级联失败。如果没有它，每一个触及失败服务的 agent 调用都会挂起直至超时，从而消耗资源并使整个流水线降级。

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"        # normal operation
    OPEN = "open"            # failing, reject calls immediately
    HALF_OPEN = "half_open"  # testing recovery

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: float | None = None

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_recovery():
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise CircuitOpenError(
                    f"Circuit open since {self.last_failure_time:.0f}. "
                    f"Recovery in {self._time_until_recovery():.0f}s"
                )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception:
            self._on_failure()
            raise

    def _on_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.failure_count = 0

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _should_attempt_recovery(self) -> bool:
        if self.last_failure_time is None:
            return True
        return time.time() - self.last_failure_time >= self.recovery_timeout

    def _time_until_recovery(self) -> float:
        if self.last_failure_time is None:
            return 0.0
        return max(0.0, self.recovery_timeout - (time.time() - self.last_failure_time))

class CircuitOpenError(Exception):
    pass
```

### 批处理流水线中的逐文档隔离

在批处理流水线中，每个文档都应当拥有自己的错误边界。某一个文档的失败不应当中止剩余的批次。

```python
def process_document_batch(documents: list[str], processor) -> list[dict]:
    results = []
    circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30.0)

    for doc_id, document in enumerate(documents):
        try:
            result = circuit_breaker.call(processor, document)
            results.append({"doc_id": doc_id, "status": "success", "result": result})
        except CircuitOpenError as e:
            # Circuit open: skip remaining docs and surface the condition upstream
            results.append({"doc_id": doc_id, "status": "circuit_open", "error": str(e)})
            for remaining_id in range(doc_id + 1, len(documents)):
                results.append({
                    "doc_id": remaining_id,
                    "status": "skipped",
                    "reason": "circuit_open"
                })
            break
        except Exception as e:
            results.append({"doc_id": doc_id, "status": "error", "error": str(e)})

    return results
```

熔断器是在批次级别而非文档级别闭合的。当它打开时，你想知道的是底层服务不可用，而不是恰好有三个单独的文档接连失败。

---

## 结构化错误传播

在多智能体系统中，以通用异常字符串形式传递的错误会丢失恢复所需的上下文。结构化错误携带上游协调器（orchestrator）所需的信息，以决定是重试、改道还是上报。

```python
from dataclasses import dataclass

@dataclass
class StructuredAgentError:
    error_category: str           # "tool_failure" | "validation_error" | "policy_gap" | "timeout"
    is_retryable: bool
    failure_type: str             # specific subtype within the category
    attempted_query: str | None   # what was tried (useful for debugging)
    partial_results: dict | None  # any usable output produced before the failure
    alternative_approach: str | None  # suggestion for the orchestrator
    error_message: str
    attempt_count: int = 1

    def to_dict(self) -> dict:
        return {
            "error_category": self.error_category,
            "is_retryable": self.is_retryable,
            "failure_type": self.failure_type,
            "attempted_query": self.attempted_query,
            "has_partial_results": self.partial_results is not None,
            "alternative_approach": self.alternative_approach,
            "error_message": self.error_message,
            "attempt_count": self.attempt_count
        }

# Usage in a sub-agent:
def search_database(query: str) -> dict:
    try:
        return db.search(query)
    except DatabaseTimeoutError:
        raise StructuredAgentError(
            error_category="tool_failure",
            is_retryable=True,
            failure_type="database_timeout",
            attempted_query=query,
            partial_results=None,
            alternative_approach="retry with narrower query or use cached results",
            error_message="Database query timed out after 30s"
        )
    except NoResultsError:
        raise StructuredAgentError(
            error_category="tool_failure",
            is_retryable=False,
            failure_type="no_results",
            attempted_query=query,
            partial_results=None,
            alternative_approach="try broader search terms or escalate to human",
            error_message=f"No results found for query: {query}"
        )

# Orchestrator handling:
def orchestrate_with_recovery(agent_fn, query: str, max_retries: int = 2) -> dict:
    for attempt in range(max_retries + 1):
        try:
            return agent_fn(query)
        except StructuredAgentError as e:
            if not e.is_retryable or attempt == max_retries:
                return {
                    "status": "failed",
                    "error": e.to_dict(),
                    "partial_results": e.partial_results,
                    "requires_escalation": not e.is_retryable
                }
            # Retryable: apply the suggested alternative approach if present
            if e.alternative_approach:
                query = refine_query(query, e.alternative_approach)
```

关键字段是 `is_retryable`。一个无法判断该重试还是该上报的协调器，会默认对所有错误进行重试，这会在不可重试的错误上浪费预算，并错过处理瞬时错误的时机。

---

## 部分结果与覆盖度标注

当流水线无法完整完成一项任务时，返回带有明确覆盖度标注的部分结果，比什么都不返回更有用。消费方随后即可决定该部分结果是否可付诸行动，而无需了解失败环节的内部细节。

```python
from dataclasses import dataclass

@dataclass
class AnalysisResult:
    full_analysis: str | None
    section_results: dict[str, dict]  # section_id -> result
    coverage_summary: dict

def annotate_coverage(section_results: dict) -> dict:
    coverage_map = {}
    for section_id, result in section_results.items():
        if result.get("status") == "success" and result.get("confidence", 0) >= 0.8:
            coverage_map[section_id] = "well-supported"
        elif result.get("status") == "success":
            coverage_map[section_id] = "partially-supported"
        else:
            coverage_map[section_id] = "gap"

    counts = {"well-supported": 0, "partially-supported": 0, "gap": 0}
    for v in coverage_map.values():
        counts[v] += 1

    return {
        "sections": coverage_map,
        "counts": counts,
        "overall_coverage": counts["well-supported"] / len(coverage_map) if coverage_map else 0.0,
        "has_gaps": counts["gap"] > 0
    }
```

在响应中暴露覆盖度标注，以便下游消费方无需解析内部状态即可据此采取行动：

```
CONTRACT ANALYSIS SUMMARY

Section 1 (Payment Terms): well-supported (full analysis available)
Section 2 (Liability Clauses): partially-supported (analysis based on partial text; recommend manual review)
Section 3 (Termination Rights): gap (source text was unreadable; human review required)

Overall coverage: 67% (2 of 3 sections fully analyzed)
```

这一模式适用于任何可能产生不完整输出的流水线场景：文档抽取、多源研究、批量翻译，或部分条款缺乏支撑数据的合规性检查。

---

## 结构化的人工交接

当上报发生时，人工坐席收到的是一份结构化的载荷，而非原始的对话历史。目标是让人工坐席能在 30 秒内开始处理，而无需回溯阅读整段对话日志。

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class HandoffPayload:
    customer_id: str
    session_id: str
    escalation_reason: str        # from EscalationReason enum
    original_request: str         # verbatim first user message
    conversation_summary: str     # 3-5 sentence summary of what happened
    root_cause: str               # why the AI could not resolve this
    actions_taken: list[str]      # what was tried
    recommended_next_action: str  # specific suggestion for the human agent
    partial_results: dict | None  # any useful output produced
    urgency: str                  # "high" | "medium" | "low"
    created_at: str               # ISO 8601

def build_handoff(
    session: dict,
    escalation_signal: EscalationSignal,
    conversation_history: list[dict]
) -> HandoffPayload:
    return HandoffPayload(
        customer_id=session["customer_id"],
        session_id=session["session_id"],
        escalation_reason=escalation_signal.reason.value,
        original_request=conversation_history[0]["content"] if conversation_history else "",
        conversation_summary=summarize_conversation(conversation_history),
        root_cause=derive_root_cause(escalation_signal),
        actions_taken=extract_actions_taken(session),
        recommended_next_action=suggest_next_action(escalation_signal),
        partial_results=session.get("partial_results"),
        urgency="high" if escalation_signal.reason == EscalationReason.EXPLICIT_REQUEST else "medium",
        created_at=datetime.utcnow().isoformat()
    )
```

### 交接展示格式

人工坐席实际看到的内容，应当读起来像一份结构化的简报，而不是一堆数据转储：

```
ESCALATION BRIEF: Session a1b2c3d4
Reason: Customer requested human agent
Urgency: HIGH

ORIGINAL REQUEST
"I need to cancel my subscription and get a refund for last month's charge"

WHAT HAPPENED
The customer asked to cancel their subscription and requested a refund for the
charge processed on May 18. The AI confirmed account details and found the charge
($49.00) but hit a policy gap: refund approval for charges older than 7 days
requires manual authorization. Two escalation attempts were made; the customer
then explicitly requested a human agent.

ACTIONS TAKEN
- Account verified (customer_id: 88821)
- Charge located: $49.00 on 2026-05-18
- Subscription status: active

RECOMMENDED NEXT ACTION
Authorize refund for $49.00 (charge is 6 days old, within 7-day window) and
process cancellation. No additional verification needed.
```

`recommended_next_action` 字段是最有价值的部分。收到具体建议的人工坐席能更快地处理案件，也更不容易要求客户重复提供信息。

---

## 来源冲突解决

当多个来源相互矛盾时，解决策略取决于它们矛盾的原因。时间性差异（一个来源比另一个更新）需要采取与事实性冲突（关于同一时间段的来源在事实上相互矛盾）不同的处理方式。

```python
@dataclass
class Source:
    source_id: str
    content: str
    publication_date: str | None  # ISO 8601, mandatory for temporal disambiguation
    source_type: str              # "official" | "news" | "user_generated" | "internal"
    authority_score: float        # 0.0-1.0, domain-specific

def resolve_conflict(sources: list[Source], field: str) -> dict:
    values = [s for s in sources if get_field_value(s, field) is not None]

    if len(values) <= 1:
        return {"resolved": values[0] if values else None, "conflict": False}

    # Check for temporal difference first
    dated = [s for s in values if s.publication_date is not None]
    if len(dated) == len(values):
        sorted_by_date = sorted(dated, key=lambda s: s.publication_date, reverse=True)
        newest = sorted_by_date[0]
        second_newest = sorted_by_date[1] if len(sorted_by_date) > 1 else None

        if (second_newest is not None and
                get_field_value(newest, field) == get_field_value(second_newest, field)):
            # Two most recent sources agree: likely a correct update
            return {
                "resolved": newest,
                "conflict": False,
                "resolution_method": "temporal_precedence"
            }

    # Genuine factual conflict: do not resolve automatically
    return {
        "resolved": None,
        "conflict": True,
        "conflict_type": "factual",
        "conflicting_sources": [s.source_id for s in values],
        "requires_human_review": True
    }
```

始终在来源元数据中包含 `publication_date`。没有它，就无法进行时间性消歧，而看似事实性冲突的情况可能只是一个尚未淘汰的过时来源。

### 在输出中暴露冲突

当一个真正的冲突无法被自动解决时，应明确地将其暴露出来，而不是默默地选择某一个来源：

```
FIELD: regulatory_status

SOURCE A (internal-policy-doc, 2026-01-15): "Approved for EU markets"
SOURCE B (legal-review-2026, 2026-03-22): "Pending re-approval: EU regulatory update in progress"

CONFLICT TYPE: factual (same field, same jurisdiction, different values)
RESOLUTION: Cannot auto-resolve. Human review required before using this field.
```

这比返回一个没有来源标注的单一答案要好。一个看到自信答案却不知道它存在争议的消费者，无法就是否据此采取行动做出明智的判断。

---

## 反模式

**将置信度分数用作路由逻辑。** 来自 LLM 的置信度分数并不是经过校准的概率。应改用程序化信号：retry count、circuit state、结构化输出字段。

**将沮丧情绪与升级意图混为一谈。** 沮丧的用户通常想要一个更好的答案，而不是一个真人。说"我要找真人"的用户则总是想要真人。应将它们视为两个不同的信号，并给予不同的响应。

**在 agents 之间传递非结构化的异常。** 像 `"DatabaseError: connection refused"` 这样的字符串，无法告诉编排器应该重试还是升级。应使用带有 `is_retryable`、`error_category` 和 `alternative_approach` 的结构化错误类型。

**在存在部分结果时却什么都不返回。** 带有清晰覆盖率标注的部分结果，几乎总是比带有错误消息的空响应更有用。消费者可以决定如何处理"67% 覆盖率"；但他们无法从"分析失败"中决定任何事情。

**在来源元数据中省略 `publication_date`。** 没有日期，时间性冲突看起来就像事实性冲突。每一个被纳入管道的来源都应携带一个日期，哪怕只是一个近似值。

**将交接构建为对话转储。** 把对话的最后 20 轮粘贴进一张工单不是交接，而是工作转移。带有 `recommended_next_action` 的结构化交接载荷，才是区分一个优秀的升级系统与一个迟缓系统的关键所在。

---

## 参见

- [Agent Teams](agent-teams.md)：编排器/subagent 架构与工具路由
- [Event-Driven Agents](event-driven-agents.md)：基于触发器的自动化与重试循环
- [Task Management](task-management.md)：多步骤 agent 工作流的持久化状态
- [Plan-Driven Workflow](plan-driven.md)：在执行前进行规划阶段，以减少任务中途的失败
