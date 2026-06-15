# 模块 07：进阶模式

**时长**：2-3 小时 | **复杂度**：⭐⭐⭐ 进阶

## 目标

编排多 agent 工作流。构建协调多个专用 agent 的复杂自动化。

---

## 你将学到

- 多 agent 架构模式
- 编排策略
- 错误处理与恢复
- 生产级自动化
- 团队工作流
- 真实场景

---

## 多 Agent 系统

**多 agent 系统**是指多个专用 agent 协同完成一个目标。

### 示例：代码发布工作流

与其让单个 Claude 处理所有事情：

```
You: "Release version 3.5.0"
    ↓
    ├─→ [Version Agent] Updates VERSION file
    │
    ├─→ [Changelog Agent] Creates release notes
    │
    ├─→ [Test Agent] Runs full test suite
    │
    ├─→ [Security Agent] Security audit
    │
    ├─→ [Docs Agent] Updates documentation
    │
    └─→ [Release Agent] Tags, builds, publishes

Result: Complete, tested, documented release
```

每个 agent 在其专长任务上都很迅速。

---

## 编排模式

### 模式 1：顺序式（流水线）

agent 一个接一个地运行。agent N 的输出成为 agent N+1 的输入。

```
Input
  ↓
[Agent 1: Parse Requirements] → Output: structured requirements
  ↓
[Agent 2: Design Schema] → Output: database schema
  ↓
[Agent 3: Generate Code] → Output: code skeleton
  ↓
[Agent 4: Write Tests] → Output: test suite
  ↓
Final Result
```

**适用场景**：每一步都依赖于上一步的工作流。

**示例**：
```bash
/agent requirements-parser
Parse the feature request into specifications

# Later, once we have specifications:
/agent database-designer
Design the schema based on these specs

# Once schema is approved:
/agent code-generator
Generate models based on the schema
```

### 模式 2：并行式（Fork-Join）

多个 agent 同时工作，结果汇总合并。

```
         Input
           ↓
    ┌──────┼──────┐
    ↓      ↓      ↓
 [Unit   [Int.  [Sec.
  Tests] Tests] Audit]
    ↓      ↓      ↓
    └──────┼──────┘
           ↓
      Combine Results
           ↓
      Final Report
```

**适用场景**：相互独立的检查或任务。

**示例**：
```
Request: "Review my code changes"

Parallel tasks:
- Code quality agent reviews
- Security agent scans
- Test coverage agent checks
- Performance agent analyzes

(All run at the same time)

Results combined into one report
```

### 模式 3：条件式（If-Then）

根据条件路由到不同的 agent。

```
Input: "Fix the bug"
  ↓
[Analyzer: Is it security?]
  ├─ YES → [Security Agent]
  ├─ PERFORMANCE → [Performance Agent]
  └─ LOGIC → [Logic Agent]
  ↓
Result
```

**示例**：
```bash
/agent bug-classifier
Categorize this bug: security, performance, or logic

# Based on response:
# If security:
/agent security-patcher
Fix the security vulnerability

# If performance:
/agent perf-optimizer
Optimize this code
```

---

## 构建发布工作流

### 场景

你想自动化发布流程。目前你需要：
1. 更新 VERSION 文件
2. 更新 CHANGELOG
3. 运行测试
4. 运行安全扫描
5. 创建 git tag
6. 推送到 origin
7. 部署到 staging

### 解决方案：多 Agent 工作流

**第 1 步：创建 agent**（每个专注于一项任务）

`.claude/agents/version-manager.md`：
```markdown
---
name: version-manager
description: Manages version files and tags
capabilities:
  - read_files
  - write_files
  - NO: push
---

# Version Manager

## Purpose
Update VERSION files and create git tags

## Tasks
- Bump version (patch, minor, major)
- Update VERSION file
- Update version in package.json, pyproject.toml, etc
- Create annotated git tags
```

`.claude/agents/changelog-generator.md`：
```markdown
---
name: changelog-generator
description: Generates release notes
---

# Changelog Generator

## Purpose
Create readable release notes from commits

## Output Format
- Version header
- Breaking changes (if any)
- New features
- Bug fixes
- Deprecations
```

`.claude/agents/test-validator.md`:
```markdown
---
name: test-validator
description: Runs full test suite
---

# Test Validator

## Purpose
Execute all tests and verify coverage

## Minimum Requirements
- All tests pass
- Coverage >80%
- No flaky tests
```

`.claude/agents/release-publisher.md`:
```markdown
---
name: release-publisher
description: Publishes and deploys
---

# Release Publisher

## Purpose
Tag and push to origin

## Steps
1. Create git tag
2. Push to origin
3. Trigger CI/CD pipeline
4. Monitor deployment
```

**第 2 步：创建发布工作流命令**

`.claude/commands/release-workflow.md`:
```markdown
# /release-workflow

Orchestrate a complete release process.

Usage:
```
/release-workflow patch|minor|major
```

## Process

1. Validate release readiness
2. Update version (version-manager agent)
3. Generate changelog (changelog-generator agent)
4. Run tests (test-validator agent)
5. Security scan (security-auditor agent)
6. Publish and deploy (release-publisher agent)

## Requirements
- All tests passing
- No outstanding security issues
- Changelog updated
```

**第 3 步：使用该工作流**

```bash
/release-workflow patch
```

随后 Claude 会：
1. 调用 version-manager → 更新 VERSION
2. 调用 changelog-generator → 生成发布说明
3. 调用 test-validator → 验证测试通过
4. 调用 security-auditor → 扫描漏洞
5. 调用 release-publisher → 创建标签并推送
6. 你审查后，再逐步批准每一步

---

## 多 Agent 系统中的错误处理

### 模式：优雅降级

如果某个 agent 失败，其他 agent 继续运行：

```
[Test Agent] ❌ FAILED: 3 test failures
  ↓
[Security Agent] ✅ PASSED: No vulnerabilities
  ↓
[Docs Agent] ✅ PASSED: Docs updated
  ↓
[Aggregate Results]
  ⚠️  Release blocked (tests failed)
  ✅ Security passed
  ✅ Docs ready
  [Instructions to fix tests first]
```

### 模式：失败重试

针对瞬时性故障（网络、超时）：

```bash
#!/bin/bash
# In a hook or skill

max_retries=3
retry=0

while [ $retry -lt $max_retries ]; do
  if /agent test-validator run-tests; then
    echo "✅ Tests passed"
    exit 0
  fi
  
  retry=$((retry + 1))
  if [ $retry -lt $max_retries ]; then
    echo "⚠️  Retry $retry/$max_retries"
    sleep 5
  fi
done

echo "❌ Tests failed after $max_retries attempts"
exit 1
```

### 模式：出错回滚

如果出现问题，撤销更改：

```bash
#!/bin/bash
# Rollback helper

ORIGINAL_VERSION=$(git rev-parse HEAD:VERSION)
ORIGINAL_TAG=$(git describe --tags --abbrev=0)

cleanup_and_exit() {
  echo "Rolling back..."
  git reset --hard HEAD~1
  git tag -d "$NEW_TAG"
  echo "VERSION restored to: $ORIGINAL_VERSION"
  exit 1
}

# Run release steps
if ! /agent version-manager bump-version patch; then
  cleanup_and_exit
fi

if ! /agent test-validator validate-all; then
  cleanup_and_exit
fi

# If we get here, release succeeded
exit 0
```

---

## 生产环境模式

### 模式 1：分阶段发布

逐步发布到不同的环境：

```
/release major
  ↓
[Dev] Deploy and test
  ✅ Verified
  ↓
[Staging] Deploy and test
  ✅ Verified
  ↓
[Prod] Deploy with monitoring
  ✅ Monitoring green
  ↓
Release Complete
```

### 模式 2：审批门禁

在通过审查前阻止推进：

```bash
# In .claude/hooks/pre-prod-deploy.sh

echo "🚨 PRODUCTION DEPLOY"
echo "Changes: $CHANGES"
echo "Tests: PASSING"
echo "Security: PASSING"
echo ""
read -p "Type 'I approve' to deploy to production: " approval

if [ "$approval" != "I approve" ]; then
  echo "❌ Deploy cancelled"
  exit 1
fi

exit 0
```

### 模式 3：监控与回滚

部署后，验证健康状态：

```bash
#!/bin/bash
# Post-deploy hook

sleep 10  # Let services start

# Health checks
if ! curl -f https://api.example.com/health; then
  echo "❌ Health check failed"
  echo "Rolling back..."
  git revert -n HEAD
  git commit -m "Rollback: deployment health check failed"
  exit 1
fi

echo "✅ Deployment successful and healthy"
exit 0
```

---

## 练习：构建你的第一个多 agent 工作流

### 场景

你有一个数据科学项目。发布清单：
1. 更新模型版本
2. 运行验证测试
3. 生成性能报告
4. 更新文档
5. 创建发布标签

### 第 1 步：创建 agents

创建 `.claude/agents/`，包含：
- `model-versioner.md` - 更新 VERSION、模型元数据
- `validator.md` - 运行验证测试
- `report-generator.md` - 创建性能指标
- `doc-updater.md` - 更新 README、API 文档
- `release-tagger.md` - 创建 git 标签

### 第 2 步：创建编排命令

`.claude/commands/ml-release.md`：
```markdown
# /ml-release

Release a new model version.

Usage:
```
/ml-release [major|minor|patch]
```

## Workflow
1. Version agent bumps version
2. Validator runs test suite
3. Report agent generates metrics
4. Doc agent updates documentation
5. Tagger creates release tag
```

### 第 3 步：测试它

```bash
/ml-release patch
```

观察 agents 如何协调完成整个发布过程。

---

## 高级系统的最佳实践

### 应该做

✅ 将 agents 设计为**可组合的**（输出能衔接到下一个 agent）

✅ **记录一切**（有助于调试故障）

✅ **先在小改动上**测试工作流

✅ **记录编排流程**（让他人也能理解）

✅ 为高风险操作内置**审批关卡**

✅ **自动化后持续监控**（验证是否成功）

### 不应该做

❌ 串联过多 agents（超过 7 个就很难调试）

❌ 让 agents **相互依赖**（优先选择松耦合）

❌ 跳过**错误处理**（事情总会出错）

❌ 在未先测试工作流的情况下**部署自动化发布**

❌ 假设 agents **总会达成一致**（要构建冲突解决机制）

---

## 验证：如果你能做到以下几点，就说明你已准备就绪……

✓ 你能解释多 agent 编排模式

✓ 你已创建了至少 2-3 个相互协作的 agents

✓ 你理解错误处理策略

✓ 你知道如何设计带审批关卡的工作流

✓ 你能为自己的项目构建发布自动化

---

## 接下来呢？

你已经完成了 7 个模块的学习路径！现在你已经掌握：

- ✅ 安装与配置
- ✅ 核心循环与上下文
- ✅ 记忆与配置
- ✅ Agent 专精化
- ✅ Skills 与知识
- ✅ Hooks 与自动化
- ✅ 高级编排

### 后续步骤

**选项 A：深入某个领域**
- 深入安全：`guide/security/`
- 深入 DevOps：`guide/ops/`
- 深入架构：`guide/core/architecture.md`

**选项 B：动手构建**
- 为你的项目创建一个多 agent 工作流
- 实现本路径中的某个练习
- 构建一个插件包并与团队分享

**选项 C：从示例中学习**
- 查看 `examples/agents/` 中的生产级 agents
- 研究 `examples/plugins/` 中的插件包
- 探索 `guide/core/skill-design-patterns.md` 中的 skills

**选项 D：自我评估**
- 进行 `/self-assessment comprehensive` 以找出差距
- 获取个性化建议
- 为薄弱环节制定学习计划

---

**完成了模块 07？** → 你已经是 Claude Code 高级用户了！🚀

到 `guide/ultimate-guide.md` 探索完整指南以深入学习，或把你学到的内容教给他人。
