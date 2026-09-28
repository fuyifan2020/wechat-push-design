---
name: wechat-push-design
description: 制作微信公众号移动端图文推送 / 长图海报。当用户要求设计微信推送、公众号文章排版、长图、图文海报、mobile article design、WeChat article / push design 时使用。完整工作流：素材盘点 → 设计规划确认 → 设计语言确认 → HTML 实现 → 预览迭代 → 高清长图导出。
---

# 微信公众号推送设计工作流

本 skill 用于将用户提供的文案、图片、模板制作成具有高端设计感的微信公众号移动端推送（HTML），并最终导出高清长图。

## 核心原则

1. **五阶段硬性门禁**：每个阶段必须获得用户明确确认后才能进入下一阶段，绝不跳步。
2. **先设计后实现**：没有确认的设计语言，不写一行 HTML。
3. **微信合规**：产出必须符合 `references/wechat-spec.md` 的移动端规范。
4. **高设计感**：遵循 `references/design-guidelines.md` 的设计手法。

## 阶段一：素材盘点与设计规划

收到用户的文案、图片、模板后：

1. **盘点清单**：列出已收到的所有素材（文案段落、图片数量与内容、参考模板），说明每份素材的用途判断。
2. **输出设计规划**，包括：
   - 内容结构大纲（开头钩子 → 正文分段 → 结尾行动号召）
   - 视觉风格提案（1 句话调性描述 + 适用理由）
   - 素材使用计划（每张图放在哪里、装饰元素如何补足）
3. **主动指出问题**：
   - 缺失的材料（如缺封面图、缺品牌色、文案某段过长/过短）
   - 建议修改的部分（如文案节奏、图片质量、信息层级）
4. 用 AskUserQuestion 或直接提问，**等待用户确认或补充后才进入阶段二**。

## 阶段二：设计语言确认

给出 1–2 套具体的设计语言方案，每套包含：

- 主色 / 辅色 / 强调色（hex 值）
- 中英文字体栈与字重层级（标题/正文/注释）
- 留白与节奏规范（段间距、呼吸感）
- 装饰语言（几何/渐变/线条/噪点等，参考 `assets/svg-snippets.md`）

用户选定或调整后才进入阶段三。详细话术见 `references/workflow-details.md`。

## 阶段三：HTML 实现

按 `references/wechat-spec.md` 编写**单文件 HTML**：

- 以 `templates/base.html` 为骨架起点。
- 750px 设计宽度，CSS 全部内联，无外部 JS，无 iframe。
- 装饰图形优先内联 SVG / CSS 渐变；照片类可引用免版权图库（Unsplash / Pexels 的 https 直链）或用户提供的本地图片。
- 复用 `assets/svg-snippets.md` 中的装饰片段，避免重复造轮子。
- 输出到当前工作目录下的推送专属文件夹（如 `output/<主题名>/index.html`）。

## 阶段四：预览确认

1. 浏览器 MCP 不接受 `file://` URL——先用本地静态服务器托管：
   `python -m http.server <端口> --directory <推送文件夹>`（后台运行），然后打开 `http://127.0.0.1:<端口>/index.html`。
2. 用 `tab.set_device_mode` 设置 responsive 设备：宽 750px，高约 800px，scaleMode=fixed，scale=1（自动获得 deviceScaleFactor=2）。
3. 用 `page.visual.snapshot` 分段截图展示给用户（首屏 + 关键段落）。
4. 收集修改意见，迭代 HTML，**直到用户明确说「可以 / 确认 / 导出」**。

## 阶段五：长图导出（已验证的可行流程）

1. **测内容高度**：把视口高度设得明显偏大（如 4000），`page.visual.snapshot` 后从返回图上目测内容底部位置的比例，换算出内容实际高度 H（CSS px）。再将视口高度精确设为 H + 少量余量（约 30px），重新截图确认内容完整且无大段空白。
2. **分带裁切**：`page.visual.snapshot` 返回降采样图和 `snapshotId`；用 `page.visual.crop` 按返回图像素坐标分带裁切，每条带输出为**原始分辨率 PNG**。
   - 注意：单条带输出高度有上限（约 2000px），超限会被整体缩放导致宽度不一致、无法拼接。**每条带的显示高度 ≤ 800px 最安全**（750 宽 × DPR2 时输出宽固定为 1500px）。
   - 快照缓存约 60 秒过期；若报 SNAPSHOT_EXPIRED，重新 snapshot 再裁切。
   - `page.visual.snapshot` 偶发 PAGE_NOT_READY，直接重试一次即可。
3. **拼接**：裁切结果会保存为本地 PNG 附件（结果中给出绝对路径）。用 skill 自带的零依赖脚本纵向拼接：
   `python scripts/stitch_png.py output/<主题名>/long-image.png <band1.png> <band2.png> ...`
4. **验证**：成品宽度应为 1500px（2x）。用 ReadMediaFile 的 region 参数抽查带与带的接缝处文字是否清晰、无错位。
5. 交付长图文件路径，并附上 HTML 源文件路径。

## 失败处理

- desktop_browser MCP 不可用 → 告知用户，并询问是否改用其他截图方式（不擅自安装依赖）。
- 外部图库图片加载失败 → 替换为本地 SVG/CSS 占位设计，并告知用户。
- 用户跳过某个确认环节 → 礼貌提醒该环节的价值，但尊重用户决定并记录跳过的环节。
