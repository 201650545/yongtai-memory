---
name: project_workbuddy_account_switcher
description: WorkBuddy 账号切换器（D:\tools\WorkBuddy-Account-Switcher）——pywebview 单文件 SPA，管理多账号登录态切换与额度看板；2026-10-20 完成商汤生图→矢量图标换肤
type: project
updated: 2026-10-20
kind: fact
status: active
scope: workbuddy_account_switcher
---

# WorkBuddy 账号切换器

## 是什么

`D:\tools\WorkBuddy-Account-Switcher`，pywebview + 单文件 `ui/index.html` 的桌面小工具。
用途：本机多个 WorkBuddy 账号的登录态切换、额度/容量看板、渠道用量统计。

- 启动：`pythonw.exe switcher.py`（Python 在 `D:\Python312\cpython-3.12.10-windows-x86_64-none\`）
- UI 全在 `ui/index.html`（约 4050 行），双主题靠 `html[data-theme]`，颜色一律走 CSS 变量
- 后端 `switcher.py` 负责登录态加解密（`wb_atrest.py`，AES-256-GCM + 机器 protectorKey）
- 数据源：buddy2api 网关 `127.0.0.1:8787`（**必须用 `scripts\gateway_daemon.py` 启动**，
  直接 `pythonw server.py` 会静默丢掉 `lobster` 渠道）

## 2026-10-20 · 图标换肤（本轮主要改动）

**背景**：此前图标是 AI 生成的 PNG，描边纯白 `#FFF`，白昼模式下等于隐形（用户反馈"看不清"）。
10-19 曾临时改成手写内联 SVG 应急；10-20 用商汤日日新重新出图并矢量化为最终方案。

**链路**：商汤 `sensenova-u1.5-fast`（经 API 转发网关 `:3100`，`image-gen` 别名链）
→ 6 批四宫格 + 3 张补充图 → 去水印 → 切格 → alpha 化 → 矢量化 → 写入 `ICONS` 对象。

**产出**：`ui/index.html` 的 `ICONS` 现为 **28 个**图标（原 20 个），全部是
`24×24 viewBox` + `fill: currentColor` 的**填充路径**（`fill-rule="evenodd"`），
颜色跟随文字色，双主题自动适配，任意缩放清晰。

新增 8 个：`expand` / `shrink`（全屏切换）、`power`（重启）、`sun`（白昼）、
`moon`（黑夜）、`web` / `plus` / `archive`（原先用 emoji 📥➕🚀 的按钮）。

同时把按钮里的 emoji 全部替换为图标：`🔄 刷新`、`📥 归档当前登录态`、`➕ 录入新账号`、
`🚀 打开 WorkBuddy`、`🔄 重启 DSH`、`⟳ 重启本工具`、`⛶/🗗 全屏`、`🌙/☀️ 昼夜`。

## 关键判据（复用价值高）

1. **位图不能直接当 13px 图标用**：商汤出的图在 1024 画布上笔画约 6px，
   缩到界面 13~14px 后笔画不足 0.3px，等于消失。必须先矢量化。
2. **矢量化必须描轮廓、不能骨架化**：骨架化（Zhang-Suen 细化）会把 6px 笔画打成断续的点，
   还原度归零（实测 24 个图标全废）。正确做法是 `cv2.findContours` 描轮廓
   → `approxPolyDP` 简化 → 输出 `fill-rule="evenodd"` 的填充路径。
3. **加粗要在归一化之后做**：先按内容尺寸算目标笔宽会算出超过画布的荒谬值（实测算出 53px/240px 画布）。
   正确顺序是"缩放到固定 240px 画布 → 再按 `1.35/24×240` 算目标笔宽 → dilate/erode 到位"。
4. **`textContent` 会抹掉图标**：凡是按钮文案由 JS 重置的地方（重启按钮的文字状态机、
   全屏图标、昼夜按钮），必须改用 `innerHTML = iconSvg(name) + 文本`，
   否则切一次状态图标就没了。

## 生图渠道实测（同日，源数据见 [[project_image_gen_routes]]）

| 渠道 | 模型 | 速度 | 结论 |
|---|---|---|---|
| 商汤日日新 | `sensenova-u1.5-fast` | 10~14s | ✅ 本轮实际使用，质量与一致性最好 |
| 商汤日日新 | `sensenova-u1.5-lite` | 20~26s | 慢一倍、token 更多，不推荐 |
| AGNES | `agnes-image-2.5-flash` | 16~22s | ✅ 可用，UA 必须 `curl/8.5.0` |
| 集梦 CLI | `jimeng-4.5/4.6/5.0` | 39~54s | ✅ 每日免费 40 积分，12 分/4 张 2048² |
| 讯飞 Loomy（经 buddy2api） | `doubao-seedream-5-lite` 等 3 个 | — | ❌ 上游 404「该模型暂未开放」，直连同样 404 |

## 脚本资产

全部在 `D:\小浣熊\_imgtest\`：
`gen_icons_sensenova.py`（生图）、`post_icons_sensenova.py`（去水印+切格+alpha）、
`vectorize_filled.py`（矢量化核心）、`apply_icons2.py`（写入 index.html）、
`gen_extra_icons.py` / `gen_sun.py`（补充图标）、`shot_app.py`（Playwright 截图验证）。

改动前备份：`ui/index.html.bak-icons-sensenova-*` / `.bak-icons2-*`。

## 待办 / 未定项

- `assets/icon.png` + `assets/icon.ico`（托盘与窗口图标）仍是旧样式，未与新图标统一
- 生图路由网关侧三个小隐患（详见 [[project_image_gen_routes]]）：`channel_models.json`
  的 `sensetime.selected` 缺 `sensenova-u1.5-fast`、`model_catalog.json` 为空、
  quota 记账丢图片 token 明细
