---
name: lesson_ai_icon_to_vector
description: AI 生图当界面图标的完整可复用流程：位图不能直接上线，必须描轮廓矢量化；含骨架化失败、加粗顺序、textContent 抹图标三个坑
type: lesson
updated: 2026-10-20
---

# AI 生图 → 界面图标：可复用流程与三个坑

## 适用场景

用生图模型（商汤日日新 / AGNES / 集梦等）批量出 UI 图标，然后接进 Web 或桌面应用。
2026-10-20 在 WorkBuddy 账号切换器上跑通全流程（24 个图标，6 批四宫格 + 3 张补充）。

## 结论：五步流程

1. **四宫格批量出图**：一次让模型画 2×2 四个图标，比单张出图省 3/4 往返。
   prompt 必须锁死风格：`uniform icon set` / `identical visual weight` /
   `same thin even stroke` / `no fill, no gradient, no shadow, no 3D` /
   `no text, no letters, no numbers` / `plain pure white background`。
2. **去水印**：商汤每张图右下角有 `日日新 sensenova` 水印。
   水印是浅灰（亮度 ≥170），图标笔画是深炭（亮度 ~30），
   所以对水印区域做亮度阈值刷白即可，笔画毫发无伤。**不要裁切**，裁了会破坏居中对齐。
3. **切格 + alpha 化**：切 4 个 512×512，按 `alpha = 255 - 亮度` 转 RGBA，
   RGB 固定成主题色。这样白底自然透明，且线条边缘天然抗锯齿。
4. **矢量化（关键）**：`cv2.findContours(RETR_CCOMP)` 描轮廓 →
   `approxPolyDP` 简化 → 输出 `fill-rule="evenodd"` 的填充 path。
   洞（比如圆环内圈）靠 evenodd 自动挖掉。
5. **双主题**：同一个 alpha 蒙版换 RGB 出两套（亮主题深墨 `#1A1D20`、
   暗主题月白 `#E6E8EB`）；如果目标平台支持 SVG + `currentColor`，
   直接用 `fill: currentColor` 一套搞定，更省。

## 坑 1：位图不能直接当小图标用（必须先矢量化）

商汤出的图在 1024 画布上笔画约 6px。界面里图标显示尺寸是 13~14px，
缩放比 14/1024 ≈ 0.0137，笔画变成 **0.08px** —— 肉眼看就是没了。
即使拿 256px 的 PNG 去显示，笔画也只有 0.3px。

**判据**：只要目标显示尺寸 < 64px，就必须矢量化，不要试图用位图缩。

## 坑 2：矢量化必须描轮廓，不能骨架化

第一版用 Zhang-Suen 细化抽中心线再连折线，结果**24 个图标全部变成断续的点阵**。
原因是笔画只有 6px、抗锯齿边缘一细化就断，分支点也连不起来。

**正确做法**：描轮廓（`findContours`）输出填充路径，笔画宽度直接烘进形状里。
**错误做法**：骨架化 + 折线拟合。

## 坑 3：加粗必须在归一化之后做

第一版先加粗、再按"内容尺寸"反推目标笔宽，算出目标 53px 而画布只有 240px —— 荒谬值，
输出路径膨胀到 5 万字符且形状糊成一团。

**正确顺序**：
```
内容等比缩放到固定 240px 画布（占 86%，居中）
→ 目标笔宽 = 1.35/24 × 240 = 13.5px
→ 用 distanceTransform 估当前笔宽，差多少就 dilate/erode 多少
→ 描轮廓，坐标除以 10 得到 24 单位
```
正常输出每条 path 400~2800 字符。

## 坑 4：`textContent` 会抹掉图标

应用里凡是按钮文案由 JS 动态重置的地方（重启按钮的文字状态机 `🔄 重启 DSH` ↔
`⚠️ 确认重启？` ↔ `⏳ 重启中…`、全屏图标 `⛶` ↔ `🗗`、昼夜按钮 `🌙` ↔ `☀️`），
`btn.textContent = ...` 会把里面的 `<svg>` 一起清掉 —— **切一次状态图标就永久消失**。

**修法**：统一走 `btn.innerHTML = iconSvg(name) + 文本`，并抽一个
`setRestartBtnLabel(btn, text)` 之类的辅助函数集中处理。

## 验收方法

用 Playwright 渲染页面后跑一段统计：
```js
[...document.querySelectorAll('svg.ico')]        // 应等于预期数量
document.querySelectorAll('img.ico').length       // 应为 0
svgs.filter(s => !s.querySelector('path')?.getAttribute('d')).length  // 应为 0
```
再按 `data-theme` 分别截图，放大 3 倍肉眼确认 13px 下的清晰度。

## 相关

- [[project_workbuddy_account_switcher]] —— 本轮实际落地项目
- [[project_image_gen_routes]] —— 各生图渠道的速度与消耗实测
