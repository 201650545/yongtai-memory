---
name: feedback-model-policy
description: 郭老师的模型使用规矩：只用 :3100 已编排统一模型组；编排外模型先问；生图仅 agnes 免问；ark 暂停使用
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f278da07-fa93-4c68-a18a-ce5d52941e3a
  modified: 2026-08-26T11:22:30.319Z
type: feedback
updated: 2026-10-06
---

2026-08-26 郭老师明确（起因：cc 子代理默认模型路由到已失效的 modelscope 裸 ID `deepseek-ai/DeepSeek-V4-Flash-0731` 全部 400）：

1. **所有 AI 调用只用 ：3100 模型编排里确认的统一模型组**（当时 4 个，以 `GET /api/unified` 实时为准），不自己挑裸渠道模型名。
2. 要用编排之外的模型 → **先问他**；生图/生视频 → 先问，**唯一例外 agnes 渠道免问**。
3. **火山方舟(ark) 已于 2026-10-20 全部删除**（渠道、额度闸门条目、arkcli CLI、计划任务与全部残留文件）；**方舟的 40 个模型不再有"等通知开放"的状态** —— 是不再使用，不是暂缓。

**Why:** 他按性价比维护编排组；乱用未编排/失效模型会直接失败或烧不值当的额度。

**How to apply:** 任何 LLM 调用前先查 /api/unified 拿组名清单，payload.model 只填组名（fast/glm-5.2/deepseek-v4-flash/ox…）；子代理 spawn 前注意会话默认模型是否指向有效编排组。相关：[[project_ai_gateway]] [[feedback_judge_only_frontend]]
