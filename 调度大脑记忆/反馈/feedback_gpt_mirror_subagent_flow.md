---
name: feedback-gpt-mirror-subagent-flow
description: 委派 GPT 镜像站的子 Agent 三条硬纪律——流程写死不复探(快)、执行完不关标签/会话(复用)、发问前必选 Extended 禁 Auto(提问闸门)+ 实测模型切换法
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
  modified: 2026-09-04T14:08:11.347Z
---

委派 GPT 镜像站送审的任何子 Agent（或我亲自走流程），三条不能犯：

1. **流程必须写死、一次到位**：从打开账号池到注入发送，选择器 / localStorage 登录 / 完整指针事件序列一律照抄手册（`D:\Work\AI平台\docs\运行手册\GPT镜像站送审流程.md` 与 `resource-ops\docs\操作手册\01_镜像站GPT操作手册.md`），**不复探 DOM、不重编选择器**。从打开到提问应一分钟内进到聊天框并发送，绝不能花 2–3 分钟。
2. **执行完不许关掉标签/会话**：已完成绑定的 tab 与 opencli 会话保持不动，留着下一轮从聊天框继续输入；**不允许每个新任务各拉起新子 Agent 重跑全流程**，一个子 Agent 可串多个同上下文任务（遵守每任务 ≤3 轮、每窗口 ≤12 轮即可）。
3. **发问前提问闸门（优先级最高，反复踩的坑）**：**每次发问前**——无论是否刚切过——先确认顶部模型 pill 文本是 "Extended" 才能发；是 "Auto" 必须先切 Extended 再发。刷新 / 超级回 / 换窗口/历史页都会重置回 Auto，**没有例外、不靠"刚才切过"想当然**（手册 §四·五 第 4 条强闸）。Auto 提问纯属白烧一轮且答不对。

**实测模型切换法（2026-09-04 在 vip-23 验证，新对话+旧对话两条路径都通）：**
- **定位 pill**：`[...document.querySelectorAll('button')].find(b => b.querySelector('span') && b.textContent.trim()==='Auto')`——当前模型名 + 带 `<span>` 子元素。新对话(/，textarea)与旧对话(/c/…，contenteditable)都同样默认 Auto。
- **开菜单**：对 pill `dispatchEvent(new MouseEvent('pointerdown',{bubbles,cancelable,view:window,pointerId:1,pointerType:'mouse',button:0,detail:1,clientX,clientY}))` + 同样 `pointerup`，**之后再调 `pill.click()` 原生 click**——只发合成 pointer 事件开不了这个 Radix 菜单，必须补原生 `.click()` 才 expanded:true。
- **选 Extended**：菜单项文本含 `Thinking• Extended`，对它做同套 pointerdown+pointerup+原生 click。
- **确认**：等 ~2s，pill 文本变 `Extended` 即成。菜单另二项：`Auto` / `GPT-5.6 Luna`。
- **每次发送前**都必须上述确认（哪怕是刚切过）；换对话/刷新/回历史默认全回 Auto。

**Why：** 郭老师（2026-09-03）当场反馈两件事：子 Agent「从打开到提问整整花 2–3 分钟才找到搜索框输入发送」；且「每次执行完把老标签关了 → 每次拉起新子 Agent → 重复整条流程」；又（2026-09 初）反馈「子 Agent 设置总做不到，提问前没确保是 Extended(stand) 就以 Auto 去问」——架构题在 Auto 下答不到点子上，冤枉烧轮。

**How to apply：** 派 GPT 镜像站任务时先固化 opencli 会话 + 保活 tab；流程/选择器从手册照抄；**提示词里显式写入「发问闸门：确认 pill=Extended 再发，禁 Auto」**（子 Agent 是全新会话，读不到我的记忆，必须把这条写进派发词，并让它发问前先读手册 §四·五）；上一个 Agent 完成不 close tab；同主题后续直接复用该会话聊天框输入。关联 [[workflow-gpt-repo-sync]] [[feedback-gpt-rounds-discipline]] [[feedback-mirror-extend-for-architecture]] [[feedback-fork-forbidden]]