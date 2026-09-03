---
name: feedback-browser-element-nav
description: 浏览器自动化少用截图（我不是多模态），用 eval 取页面元素 rect/uid 定位再点击；出问题先问 opencli doctor；成功流程进记忆并持续提速
metadata: 
  node_type: memory
  type: feedback
  modified: 2026-09-03T16:54:18.820Z
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
---

郭老师（2026-09-03）明确规定浏览器自动化操作流程：

1. **减少用截图**（我不是多模态模型，截图慢且易认错/读不准），尽量**用页面元素识别来确定位置**：`eval` 拿元素 `getBoundingClientRect()` 的 x/y/宽高，或从 `state` 取 uid，再造真实 pointer/mouse/click 事件点击。
2. **出问题先问 `opencli doctor`** 诊断连通性/环境，别盲目重试。
3. **成功后把流程记进记忆**，并在不断执行中**持续优化流程提速提效**（呼应 [[feedback-optimize-repeat-tasks]]）。

**Why:** 郭老师观察到我老用截图找按钮点错位置（曾点错 Auto 芯片、找不到 extend 开关白白耗了 18+ 轮）；元素 rect 法更快更准。他明确要少截图、多定位元素。
**How to apply:** 在镜像版/任何 opencli 浏览器会话里：目标按钮 → `eval` 取其 closest('button') 的 rect → 派发真实事件(pointerdown/up,mousedown/up + click)或 opencli `click <uid>` → `state` 验证。模型选择器等下拉照此找 `role=menuitemradio` 项切。故障一律 `opencli doctor`。

**抓取镜像版回复的铁律（郭老师 2026-09-03 专门强调）**：**不要乱抓流式回复**——等模型**完全输出完**再抓全文。判定是否输出完：①发送箭头从正方形(■ 停止生成)变回三角形/纸飞机(▶ 发送)**或** ②轮询最后一条 `[data-message-author-role=assistant]` 的 innerText 长度，**连续 2 次不变即完成**。没输出完就抓会拿到半截（如曾抓成 2724 字但最终 5342 字）。关联 [[feedback-browser-session]]（一律 opencli）[[feedback-mirror-extend-for-architecture]]。