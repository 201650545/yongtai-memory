---
name: project-deepseek-harness-opencli
description: 用户给的后备执行方法——当子 Agent 本体无法换别家模型时，用 Open CLI 控制 DeepSeek Harness 烧额度（改模型/一任务一窗口/可开10窗口）
metadata: 
  node_type: memory
  type: project
  modified: 2026-09-03T16:40:18.400Z
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
---

郭老师（2026-09-03，深夜放权）给的后备执行方法：**当调度大脑的 fork 子 Agent 实现不了"让别的平台的模型真跑"时，改用 Open CLI 调用 DeepSeek Harness 来控制它。**

**具体操作：**
1. 更改 Harness 的模型配置，让它选定特定模型。
2. **每个任务新开一个独立对话/独立聊天窗口**，让它在独立窗口执行。
3. 任务做完，通过 Open CLI 就能看到结果。
4. 可并发开**10 个窗口**给 Harness 同时干活。

**Why:** 用户的真实目的是让子 Agent 的活**用上网关里那几个渠道的模型额度**（魔塔/DeepSeek官方/B.AI）而非跑在我的算力上，且要从日志/窗口看到真执行。fork 子 Agent 本体是 Claude 换不了模型，这是替代通道（呼应 [[feedback-subagent-gateway-burn]]）。
**How to apply:** 当需要"独立对话窗口 + 指定模型 + 烧 DeepSeek 额度"的执行任务时，用 opencli 控制 DeepSeek Harness；每个任务一个独立窗口，跑完 opencli 读结果。可与镜像版（AI问答宝，extend 模式）分工：镜像版负责架构/设计把关，Harness 负责执行/烧额度。关联 [[project-trae-solo-control]]（同为 opencli 控制的对话式 agent）[[feedback-mirror-extend-for-architecture]]。