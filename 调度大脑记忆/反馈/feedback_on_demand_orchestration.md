---
name: on-demand-orchestration
description: 用户要「按需调度」而非定时汇报——自然说话，我当调度大脑路由到已打通工具
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 95cff9f0-c115-4770-a66a-5ed8ec23a5c2
  modified: 2026-08-13T06:41:38.680Z
---

郭老师的工作模型是**按需调度**：他自然说一句话（比如「查飞书资源表 + GitHub 对应项目」「搜个东西」），我当调度大脑，自己判断该打哪个已打通工具，去查、去连、去汇总、去解决。**不要**给他搭「定时任务 / 提醒 / 汇报」平台——这个方向他 2026-08-12 明确否掉了，我之前想岔了。

工具地图（已注册，首次用先验证鉴权）：
- opencli 外部 CLI：lark-cli=飞书、gh=GitHub、tg、wecom-cli=企业微信、wx=微信、notion、obsidian、longbridge 等
- opencli browser 控 AI 引擎：doubao-app / chatgpt-app / codex / cursor 等 adapter
- 统一网关(:3000, D:\游戏\ds_v4_cli，opencli 控 4 大搜索) 见 [[ai-gateway]]
- 编排器(:8791) 课件生成，见 [[english-teaching]] 相关

**Why:** 用户强调「人是会遗忘的」，想让 AI 记住工具地图并自主路由；同时明确不需要任何接收 AI 汇报/提醒的平台。
**How to apply:** 接到自然语言请求，先想「该打哪个已连接工具」并自动去查（飞书表→lark-cli、仓库→gh、搜索→网关多引擎、额度→台账），不要反问「去哪个窗口」、不要提议搭提醒/汇报平台。
