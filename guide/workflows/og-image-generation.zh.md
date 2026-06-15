# 使用 Astro 动态生成 OG 图片

在构建时自动生成社交预览图片，而不是维护陈旧的静态 PNG。每一次在 Twitter/X、LinkedIn 或 Slack 上的分享都会展示准确、最新的统计数据。

## 为什么值得这么做

静态 OG 图片会过时。当你新增第 200 个模板或达到 1k GitHub stars 的那一天，你的社交预览却仍然显示旧数字。动态生成只需配置一次，便能永远保持准确。

下面的方案使用 Satori（Vercel）将类 React 的树渲染为 SVG，再用 resvg 转换为 PNG。它在 Astro 中于构建时运行——零运行时开销，无需外部服务。

## 技术栈

| 包 | 作用 |
|---------|------|
| `satori` | 将类 JSX 对象树渲染为 SVG |
| `@resvg/resvg-js` | 将 SVG 转换为 PNG（Rust 编写，速度快） |
| `@fontsource/inter` | 本地字体文件（需要 woff1 格式） |

## 配置

```bash
pnpm add satori @resvg/resvg-js @fontsource/inter
```

在 `src/pages/og-image.png.ts` 创建该文件。Astro 会自动将其托管在 `/og-image.png`。

在你的布局中引用它：

```html
<meta property="og:image" content="/og-image.png" />
<meta name="twitter:image" content="/og-image.png" />
```

参见开箱即用的模板：[`examples/scripts/og-image-astro.ts`](../../examples/scripts/og-image-astro.ts)

## 实现模式

```typescript
import type { APIRoute } from 'astro'
import satori from 'satori'
import { Resvg } from '@resvg/resvg-js'
import { readFileSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))

export const GET: APIRoute = () => {
  const fontData = readFileSync(
    resolve(__dirname, '../../node_modules/@fontsource/inter/files/inter-latin-400-normal.woff')
  ).buffer as ArrayBuffer

  const svg = satori(
    { type: 'div', props: { style: { /* ... */ }, children: [ /* ... */ ] } },
    { width: 1200, height: 630, fonts: [{ name: 'Inter', data: fontData }] }
  )

  const png = new Resvg(svg, { fitTo: { mode: 'width', value: 1200 } }).render().asPng()

  return new Response(png.buffer as ArrayBuffer, {
    headers: { 'Content-Type': 'image/png' },
  })
}
```

## 从内容动态获取统计数据

在构建时统计你的内容文件数量，而不是硬编码：

```typescript
function countQuestions(): number {
  const dir = resolve(__dirname, '../content/questions')
  let total = 0
  for (const cat of readdirSync(dir, { withFileTypes: true })) {
    if (cat.isDirectory()) {
      total += readdirSync(resolve(dir, cat.name))
        .filter(f => f.endsWith('.md')).length
    }
  }
  return total
}
```

可以自动统计的数据：
- 内容目录中的 Markdown 文件（问题、文章、文档）
- 数据文件中的 YAML 条目
- 大型文档的行数

应保持硬编码（手动更新）的数据：
- GitHub stars（动态变化，使用 `1.1k+` 这类保守标签）
- 来自其他仓库的模板
- 性能基准测试

## 注意事项

### 字体格式很重要

Satori 要求 **woff1** 或 **TTF**。使用 woff2 或会重定向到 HTML 的远程 CDN URL 时，它会静默失败或抛出错误。

```typescript
// 正确——来自 @fontsource 的本地 woff1
readFileSync('node_modules/@fontsource/inter/files/inter-latin-400-normal.woff')

// 失败——resvg 不支持 woff2
readFileSync('node_modules/@fontsource/inter/files/inter-latin-400-normal.woff2')

// 失败——CDN 可能返回 HTML（重定向、登录墙）
await fetch('https://fonts.gstatic.com/s/inter/...')
```

### 静态文件会遮蔽 API 路由

Astro 开发服务器会**先于** API 路由托管 `public/` 中的静态文件。如果你有一个 `public/og-image.png`，它将始终被托管，而不是你的动态端点。

**删除它：**
```bash
rm public/og-image.png
```

同时检查项目根目录和 `dist/`——那里的文件也可能遮蔽该路由。用 `curl -I http://localhost:4321/og-image.png` 进行诊断：如果响应中带有 `Last-Modified` 头，说明你访问的是静态文件，而非 API 路由。

### 浏览器缓存

删除静态文件后，执行强制刷新（`Cmd+Shift+R`）或在全新的隐身窗口中测试。浏览器可能已经激进地缓存了旧的 PNG。

### `satori` 在较新版本中是同步的

某些版本的 satori 返回 `Promise<string>`，另一些则返回 `string`。如果你得到的 PNG 是 `[object Promise]`，请加上 `await`：

```typescript
const svg = await satori(tree, options)
```

## 测试

**本地预览**——直接在浏览器中访问：
```
http://localhost:4321/og-image.png
```

**社交预览模拟**——将你的生产环境 URL 粘贴到：
- [opengraph.xyz](https://www.opengraph.xyz) —— 通用 OG 调试器
- LinkedIn Post Inspector（`linkedin.com/post-inspector/`）—— 为 LinkedIn 强制刷新缓存
- Twitter Card Validator（`cards-dev.twitter.com/validator`）

**CI 检查**——如果你想捕获回归问题，可以添加一个构建步骤，检查生成的 PNG 文件大小是否超过某个阈值：

```bash
# In CI after pnpm build
SIZE=$(wc -c < dist/og-image.png)
if [ "$SIZE" -lt 10000 ]; then
  echo "og-image.png looks too small ($SIZE bytes) — generation may have failed"
  exit 1
fi
```

## 变体

### 个人品牌（无统计网格）

```typescript
children: [
  { type: 'span', props: { style: { fontSize: '48px', color: '#c0522a' }, children: 'FB.' } },
  { type: 'span', props: { style: { fontSize: '80px', fontWeight: 800, color: '#f5f5f5' }, children: 'Your Name' } },
  { type: 'span', props: { style: { fontSize: '24px', color: '#8b949e' }, children: 'Your tagline here' } },
]
```

### 项目列表徽章

```typescript
['project-a.com', 'project-b.com', 'project-c.com'].map(label => ({
  type: 'div',
  props: {
    style: { background: '#161b22', border: '1px solid #30363d', borderRadius: '8px', padding: '8px 16px' },
    children: [{ type: 'span', props: { style: { color: '#c0522a' }, children: label } }],
  },
}))
```

### 终端风格徽章（适用于 CLI 工具）

```typescript
{
  type: 'div',
  props: {
    style: { background: '#21262d', border: '1px solid #30363d', borderRadius: '20px', padding: '6px 16px', color: '#3fb950', fontFamily: 'monospace' },
    children: '>_ your-cli-tool',
  },
}
```

## 保持统计数据同步

维护单一可信源。当你更新 OG 图片中的统计数据时，在同一次提交中将它们在所有地方一并更新（落地页徽章、README 等）。

对于拥有多个落地页的项目，创建一个 slash command `/update-stats-image-landings`，它会遍历每个仓库并提示你逐项核验每个统计数据。这能防止各站点之间出现数据漂移。
