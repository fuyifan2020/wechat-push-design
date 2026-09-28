# 微信公众号移动端规范速查

## 尺寸体系

| 项目 | 数值 | 说明 |
|------|------|------|
| 设计宽度 | 750px | 对应 iPhone @2x，正文安全区约 686px（两侧各 32px 边距） |
| 预览视口 | 375px（CSS px） | 开发预览时模拟此宽度 |
| 长图导出宽度 | ≥1500px | devicePixelRatio=2 时 750×2；3x 时 2250px |
| 正文字号 | 30–32px（@2x） | 约等于 15–16px @1x，移动端可读下限 |
| 标题字号 | 40–56px（@2x） | 与正文拉开 1.5–2 倍对比 |
| 注释字号 | ≥24px（@2x） | 不低于 12px @1x |

## HTML / CSS 硬性规则

- **单文件**：所有 CSS 写在 `<style>` 内，不引用外部样式表。
- **禁用外部 JS**：微信编辑器/WebView 会剥离 `<script>`；推送图文本质是静态内容，不需要 JS。
- **禁用元素**：`<iframe>`、`<form>`、`<video>` 外链（微信环境不可靠）、`position: fixed`（长图截图会错位、微信内表现异常）。
- **布局**：块级流式布局为主；flex 可用；避免复杂 grid（旧版 WebView 兼容性问题），需要时用 flex 替代。
- **单位**：整体按 750px 设计稿写 px；容器用 `max-width: 750px; margin: 0 auto;`。
- **背景**：整页背景色设在 `body` 上，避免截图时出现白边。

## 字体

```css
font-family: -apple-system, BlinkMacSystemFont, "PingFang SC",
  "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
```

- 不依赖 webfont（微信环境加载不可靠且拖慢渲染）。
- 数字/英文装饰性大字可用 `Georgia, "Times New Roman", serif` 制造衬线对比。

## 图片策略（按优先级）

1. **装饰图形** → 内联 SVG 或 CSS 渐变/形状，零外链、最稳定、可任意缩放不失真。
2. **用户提供的图片** → 本地相对路径引用；导出长图前确认文件存在。
3. **照片/氛围图** → 免版权图库 https 直链：
   - Unsplash: `https://images.unsplash.com/photo-<id>?w=1200&q=80`
   - Pexels: `https://images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg?w=1200`
   - 引用前用 FetchURL 或浏览器验证链接可访问；失败则改用 SVG/CSS 设计替代。

## 导出前检查清单

- [ ] 375px 视口下无横向滚动条
- [ ] 无 `<script>`、无外链 CSS/JS、无 iframe、无 position:fixed
- [ ] 所有图片加载成功（截图前在浏览器逐段检查）
- [ ] 文字与背景对比度充足（正文 ≥ 4.5:1）
- [ ] 页面底部有完整收尾（落款/二维码位/版权行），长图不突兀截断
