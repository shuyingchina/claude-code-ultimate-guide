# 模块 01：安装与配置

**用时**：15 分钟 | **难度**：⭐ 入门

## 目标

在你的系统上安装并运行 Claude Code。通过第一条命令验证它能正常工作。

---

## 你将学到

- 为你的平台安装 Claude Code（macOS / Linux / Windows）
- 理解基本的 prompt → 响应循环
- 运行你的第一条命令
- 使用帮助系统

---

## 安装

### macOS（推荐）

```bash
brew install anthropic/tap/claude-code
```

验证：
```bash
claude --version
```

### Linux

```bash
curl -sSL https://dl.claudecode.com/install.sh | bash
```

验证：
```bash
claude --version
```

### Windows

从 https://dl.claudecode.com/windows 下载安装程序，或使用：

```powershell
iex ((New-Object System.Net.WebClient).DownloadString('https://dl.claudecode.com/install.ps1'))
```

### Docker（任意平台）

```bash
docker run -it anthropic/claude-code:latest
```

---

## 首次运行

进入任意项目目录并启动 Claude：

```bash
cd ~/my-project
claude
```

你会看到：

```
Claude Code v2.x.x ready
Project: ~/my-project (git: main)
Context: 0% · Tokens available: 200,000

Type /help for commands or ask me anything
>
```

---

## 必备命令

| 命令 | 用途 |
|---------|---------|
| `/help` | 显示所有可用命令 |
| `/status` | 查看上下文用量和会话状态 |
| `/clear` | 重新开始（清空对话历史） |
| `Ctrl+C` | 取消当前操作 |
| `/exit` | 关闭 Claude Code |

---

## 你的前 5 分钟

### 练习 1：查看可用命令
```bash
/help
```

浏览命令列表。注意：
- **工作流**：`/plan`、`/rewind`、`/think`
- **导航**：`/goto`、`/read`
- **记忆**：启动时加载记忆
- **进阶**：`/model`、`/mode`

### 练习 2：查看会话状态
```bash
/status
```

你会看到：
- 上下文用量百分比
- 可用 token 数
- 当前项目
- Git 分支

### 练习 3：向 Claude 提问

```
What files are in my project?
```

Claude 会读取项目结构并作出响应。这就是核心循环：

```
Your prompt → Claude reads files → Claude suggests changes → You review → Apply
```

### 练习 4：审查建议的更改

如果 Claude 建议了代码更改，你会看到：
1. 更改的说明
2. 一个 `diff` 视图（哪些内容被添加/删除）
3. 接受或拒绝的提示

**规则**：在接受之前务必审查 diff。这能保护你免受意外更改的影响。

---

## 核心概念：循环

每一次交互都遵循这个模式：

```
┌─────────────┐
│ You ask     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Claude      │
│ reads files │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Claude      │
│ suggests    │
│ changes     │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ You review diff  │
│ and approve      │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Changes applied  │
│ to your files    │
└──────────────────┘
```

---

## 关键概念

### 会话

每次运行 `claude`，你都会开启一个新的**会话**。会话是你在使用 Claude Code 期间与 Claude 持续进行的一段对话。

- 会话默认**不会被保存**（退出时即结束）
- 会话一次只**作用于一个项目**
- 随着你提出更多问题，上下文会不断增长（最多约 200K tokens）

### 上下文

**上下文**是指 Claude 记住了多少对话内容。它以百分比（0-100%）形式显示。

- 0-50%：空间充裕，可自由使用
- 50-70%：有选择地使用，`/compact` 可选
- 70%+：运行 `/compact` 释放空间
- 90%+：你将被强制清理

### Git 感知

Claude Code 具备 **git 感知**能力。它会：
- 检测你当前所在的分支
- 显示未提交的更改
- 协助提交和审查
- 防止意外的破坏性更改

---

## 验证：满足以下条件即表示你已准备就绪……

✓ 你可以运行 `claude --version` 并看到已安装的版本号
✓ 你可以在项目中用 `claude` 启动 Claude
✓ 你理解了 prompt → response 循环
✓ 你能看到 `/status` 并理解它所展示的内容
✓ 你至少审阅过一次来自 Claude 的 diff

---

## 接下来做什么？

当你对本模块感到熟练后，进入 **Module 02: Core Loop**，了解：
- Claude 如何读取你的项目
- context 在底层是如何工作的
- 如何组织请求以获得更好的结果
- Plan Mode 和 thinking 模式

**进入下一模块所需时间**：可立即开始（除了运行过一次 Claude 之外无其他前置条件）

---

## 故障排查

### "claude: command not found"
你的安装未完成。尝试：
- **macOS**：再次运行 `brew install anthropic/tap/claude-code`
- **Linux**：重新运行安装脚本
- **Windows**：从 https://dl.claudecode.com/windows 下载安装程序

### "Project not found"
确保你处于一个包含 `package.json`、`.git` 或其他项目文件的目录中。Claude Code 在项目中工作效果最佳。

### "Permission denied"（macOS）
尝试：
```bash
chmod +x /usr/local/bin/claude
```

---

## 资源

- **官方文档**：https://code.claude.com/docs
- **FAQ**：参见 `guide/ultimate-guide.md` 附录 B
- **示例**：本指南中的 `examples/` 目录

---

**完成了 Module 01？** → 准备进入 Module 02: Core Loop
