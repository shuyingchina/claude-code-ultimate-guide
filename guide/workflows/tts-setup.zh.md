---
title: "TTS Setup Workflow - Agent Vibes Installation"
description: "Add text-to-speech narration to Claude Code on macOS"
tags: [workflow, tts, tutorial]
---

# TTS 配置工作流 - Agent Vibes 安装

**目标**：为 Claude Code 添加文本转语音的语音播报
**耗时**：18 分钟
**难度**：中级
**系统**：macOS（需要 Homebrew）

---

## 决策点：你是否应该安装 TTS？

使用下面的快速评估：

| 问题 | 回答 | 分值 |
|----------|--------|-------|
| 你是否要进行长时间的代码审查？ | 是 | +2 |
| 你是否在调试过程中同时处理多项任务？ | 是 | +2 |
| 你是否更喜欢音频通知？ | 是 | +1 |
| 你是否需要离线 TTS（不依赖云端）？ | 是 | +2 |
| 延迟是否至关重要（要求 <100ms）？ | 是 | -2 |
| 你是否在公共场所工作（不能播放音频）？ | 是 | -3 |
| 你是否更喜欢安静的工作环境？ | 是 | -2 |

**得分**：
- **≥3**：安装 TTS（很适合）
- **0-2**：可选（试用一下，可以卸载）
- **<0**：跳过 TTS（不太适合）

---

## 工作流概览

```
Phase 1: Prerequisites (5 min)
    ↓
Phase 2: Agent Vibes Install (5 min)
    ↓
Phase 3: Piper TTS + Voices (5 min)
    ↓
Phase 4: Test & Configure (3 min)
    ↓
Phase 5: Verify (1 min)
```

---

## 阶段 1：先决条件（5 分钟）

### 检查点 1.1：系统要求

```bash
# Verify macOS version
sw_vers
# Required: macOS 10.15+

# Verify Homebrew
brew --version
# If missing: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Verify Node.js
node --version
# Required: 16.0.0+
```

### 检查点 1.2：安装 Bash 5.x

```bash
# Install
brew install bash

# Verify
/opt/homebrew/bin/bash --version
# Expected: GNU bash, version 5.x

# ✅ Checkpoint: Bash 5.x installed
```

### 检查点 1.3：安装依赖

```bash
# Install audio tools
brew install sox ffmpeg util-linux espeak-ng

# Verify all installed
command -v sox && command -v ffmpeg && command -v espeak-ng && echo "✅ Dependencies OK"

# ✅ Checkpoint: Dependencies installed
```

**阶段 1 总耗时**：约 5 分钟

---

## 阶段 2：Agent Vibes 安装（5 分钟）

### 步骤 2.1：启动安装程序

```bash
# Navigate to your project
cd /path/to/your/claude-project

# Launch interactive installer
npx agentvibes install
```

**预期结果**：ASCII 横幅 + 4 页交互式安装程序

### 步骤 2.2：浏览各页面

**第 1/4 页 - Dependencies**：
- 检查：应当显示全部 ✓ 绿色对勾
- 操作：点击 "Next →"

**第 2/4 页 - Provider**：
- **选择**：`Piper TTS`（质量最佳，离线）
- 操作：点击 "Next →"

**第 3/4 页 - Voice**：
- **法语**：选择 `fr_FR-tom-medium`（男声，专业）
- **英语**：选择 `en_US-ryan-high`（质量最佳）
- 操作：点击 "Next →"

**第 4/4 页 - Settings**：
- **Reverb**：`Light`（推荐）
- **Background Music**：`Disabled`（避免分心）
- **Verbosity**：`Low`（更少废话）
- 操作：点击 "Start Installation"

### 检查点 2.3：验证安装

```bash
# Check installed files
ls .claude/hooks/play-tts.sh
ls .claude/commands/agent-vibes/
cat .claude/tts-provider.txt
# Expected: Files exist, provider shows "macos" or "piper"

# ✅ Checkpoint: Agent Vibes installed
```

**阶段 2 总耗时**：约 5 分钟

---

## 阶段 3：Piper TTS + 法语语音（5 分钟）

### 步骤 3.1：通过 pipx 安装 Piper

```bash
# Install Piper TTS
pipx install piper-tts

# Verify
piper --help
# Expected: Piper usage instructions

# ✅ Checkpoint: Piper installed
```

### 步骤 3.2：下载法语语音

```bash
# Create voice directory
mkdir -p ~/.claude/piper-voices
cd ~/.claude/piper-voices

# Download French male voice (recommended)
curl -L -o fr_FR-tom-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx"
curl -L -o fr_FR-tom-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium/fr_FR-tom-medium.onnx.json"

# Download French female voice (optional)
curl -L -o fr_FR-siwis-medium.onnx \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx"
curl -L -o fr_FR-siwis-medium.onnx.json \
  "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json"

# ✅ Checkpoint: Voices downloaded (~120MB)
```

**阶段 3 总耗时**：约 5 分钟

---

## 阶段 4：配置与测试（3 分钟）

### 步骤 4.1：配置 Provider 与 Voice

```bash
# Set Piper as provider
echo "piper" > .claude/tts-provider.txt

# Set French male voice
echo "fr_FR-tom-medium" > .claude/tts-voice.txt

# Verify configuration
cat .claude/tts-provider.txt  # Expected: piper
cat .claude/tts-voice.txt     # Expected: fr_FR-tom-medium

# ✅ Checkpoint: Configuration set
```

### 步骤 4.2：测试音频管道

```bash
# Test Piper directly
echo "Bonjour, je suis Claude et je parle français" | \
  piper -m ~/.claude/piper-voices/fr_FR-tom-medium.onnx \
  --output-file /tmp/test-fr.wav && afplay /tmp/test-fr.wav

# Test TTS hook
~/.claude/hooks/play-tts.sh "Ceci est un test audio"

# ✅ Checkpoint: Audio works
```

**预期结果**：你应当能听到法语男声。

**阶段 4 总耗时**：约 3 分钟

---

## 阶段 5：在 Claude Code 中验证（1 分钟）

### 步骤 5.1：启动并测试

```bash
# Start Claude Code
claude

# In Claude, run:
/agent-vibes:whoami
# Expected: Shows "piper" provider and "fr_FR-tom-medium" voice

# Test simple request
> "Dis-moi bonjour en français"
# Expected: Audio response in French male voice

# ✅ Checkpoint: TTS active in Claude Code
```

### 步骤 5.2：配置偏好设置

```bash
# Reduce verbosity (recommended)
/agent-vibes:verbosity low

# Hide 34 commands if cluttered
/agent-vibes:hide

# ✅ Checkpoint: Preferences set
```

**阶段 5 总耗时**：约 1 分钟

---

## 总耗时：约 18 分钟 ✅

---

## 安装后建议

### 针对你的工作流进行优化

**用于代码审查**：
```bash
/agent-vibes:verbosity low
/agent-vibes:effects off
```

**用于专注工作**：
```bash
/agent-vibes:mute  # Mute temporarily
# Work without audio
/agent-vibes:unmute  # Re-enable when done
```

**用于电池优化**：
```bash
# Switch to macOS Say (instant, no CPU burst)
/agent-vibes:provider switch macos
```

### 添加到 .gitignore

```bash
# Prevent committing large audio files
echo ".claude/audio/" >> .gitignore
echo ".claude/piper-voices/" >> .gitignore
echo "*.wav" >> .gitignore
echo "*.onnx" >> .gitignore
```

---

## 故障排查速查

| 问题 | 快速修复 |
|-------|-----------|
| 没有声音 | 检查 `cat .claude/tts-provider.txt` |
| 声音不对 | 运行 `/agent-vibes:switch fr_FR-tom-medium` |
| 过于啰嗦 | 运行 `/agent-vibes:verbosity low` |
| 命令杂乱 | 运行 `/agent-vibes:hide` |

**完整故障排查**：[Agent Vibes 故障排查](../../examples/integrations/agent-vibes/troubleshooting.md)

---

## 后续步骤

- **[语音目录](../../examples/integrations/agent-vibes/voice-catalog.md)** - 探索 15 种语音
- **[集成指南](../../examples/integrations/agent-vibes/README.md)** - 学习命令
- **[安装详情](../../examples/integrations/agent-vibes/installation.md)** - 深入了解

---

## 卸载说明

要彻底移除 Agent Vibes：

```bash
# Automated uninstall
npx agentvibes uninstall --yes

# Manual cleanup (if needed)
rm -rf .claude/hooks/*vibes*
rm -rf .claude/commands/agent-vibes/
rm -rf .claude/audio/
rm -rf ~/.claude/piper-voices/
pipx uninstall piper-tts
```

---

*工作流指南由 [Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide) 维护*
*最后更新：2026-01-22 | Agent Vibes v3.0.0*
