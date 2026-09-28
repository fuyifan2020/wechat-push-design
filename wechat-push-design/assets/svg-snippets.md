# 可复用 SVG / CSS 装饰片段库

所有片段均为内联代码，直接嵌入 HTML 使用。颜色用 `currentColor` 或替换 `{{PRIMARY}}` 为主色 hex。

## 1. 大号半透明章节序号

```html
<span style="font-family: Georgia, serif; font-size: 120px; font-weight: 700;
  color: {{PRIMARY}}; opacity: .12; line-height: 1; display: block;">01</span>
```

## 2. 小号英文标签（eyebrow）

```html
<span style="display: inline-block; font-size: 20px; letter-spacing: 6px;
  text-transform: uppercase; color: {{PRIMARY}}; font-weight: 600;">CHAPTER ONE</span>
```

## 3. 细线分隔符（居中菱形）

```html
<div style="display: flex; align-items: center; justify-content: center; gap: 16px; margin: 80px auto;">
  <span style="width: 80px; height: 1px; background: {{PRIMARY}}; opacity: .4;"></span>
  <span style="width: 8px; height: 8px; background: {{PRIMARY}}; transform: rotate(45deg);"></span>
  <span style="width: 80px; height: 1px; background: {{PRIMARY}}; opacity: .4;"></span>
</div>
```

## 4. 波浪分隔线（SVG）

```html
<svg viewBox="0 0 750 40" width="100%" height="40" preserveAspectRatio="none" style="display: block;">
  <path d="M0,20 C125,40 250,0 375,20 C500,40 625,0 750,20"
        fill="none" stroke="{{PRIMARY}}" stroke-width="2" opacity="0.3"/>
</svg>
```

## 5. 装饰渐变圆（背景点缀，绝对定位在 section 内）

```html
<div style="position: absolute; top: -60px; right: -80px; width: 280px; height: 280px;
  border-radius: 50%; background: radial-gradient(circle, {{PRIMARY}} 0%, transparent 70%);
  opacity: .15; pointer-events: none;"></div>
```
（父容器需 `position: relative; overflow: hidden;`）

## 6. 引言装饰（大引号）

```html
<blockquote style="position: relative; padding: 40px 48px; margin: 0;">
  <span style="position: absolute; top: 0; left: 0; font-family: Georgia, serif;
    font-size: 100px; color: {{PRIMARY}}; opacity: .2; line-height: 1;">&ldquo;</span>
  <p style="font-size: 34px; line-height: 1.8; font-weight: 500; margin: 0;">引言文字</p>
</blockquote>
```

## 7. 标签胶囊

```html
<span style="display: inline-block; padding: 10px 28px; border: 1px solid {{PRIMARY}};
  border-radius: 999px; font-size: 24px; color: {{PRIMARY}}; letter-spacing: 2px;">标签文字</span>
```

## 8. 几何线条纹理背景（SVG，section 顶部）

```html
<svg viewBox="0 0 750 120" width="100%" height="120" style="display: block;">
  <line x1="0" y1="60" x2="750" y2="60" stroke="{{PRIMARY}}" stroke-width="1" opacity="0.15"/>
  <circle cx="375" cy="60" r="6" fill="{{PRIMARY}}"/>
  <circle cx="375" cy="60" r="14" fill="none" stroke="{{PRIMARY}}" stroke-width="1" opacity="0.5"/>
</svg>
```

## 9. 渐变文字标题

```html
<h2 style="font-size: 52px; font-weight: 800; line-height: 1.3; margin: 0;
  background: linear-gradient(135deg, {{PRIMARY}}, {{SECONDARY}});
  -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;">标题文字</h2>
```

## 10. 竖排装饰文字（东方风格）

```html
<span style="writing-mode: vertical-rl; letter-spacing: 12px; font-size: 28px;
  color: {{PRIMARY}}; opacity: .6; font-family: 'Songti SC', 'SimSun', serif;">竖排文字</span>
```

## 11. 图片统一处理样式

```html
<img src="..." alt="..." style="width: 100%; display: block; border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0,0,0,.08);">
```

## 12. 数据大数字

```html
<div style="text-align: center;">
  <span style="font-family: Georgia, serif; font-size: 96px; font-weight: 700;
    color: {{PRIMARY}}; line-height: 1;">98<span style="font-size: 48px;">%</span></span>
  <p style="font-size: 26px; opacity: .55; margin-top: 12px; letter-spacing: 2px;">数据说明文字</p>
</div>
```
