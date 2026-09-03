---
name: trae-model-lock
description: 用 TRAE SOLO 当子 Agent 时，模型只用 DeepSeek V4 Flash 正式版（当前打开对话的默认），不切其他模型
metadata: 
  node_type: memory
  type: feedback
  modified: 2026-08-30T08:15:23.696Z
  originSessionId: 8ee5c1ea-99c5-4cbe-bf2c-52824ee32254
---

**用 TRAE SOLO（opencli trae-solo send）时，模型固定用 DeepSeek V4 Flash 正式版**，即当前打开对话的默认模型。

**Why:** 用户 2026-08-30 明确：「你用它的模型只能用 DeepSeek V4 flash 正式版。这是你已经打开的对话中默认使用的模型」。

**How to apply:** `opencli trae-solo model` 只读确认当前模型，不要 switch 到别的模型；substring 匹配时若想验证，直接读当前即可。关联 [[trae-solo-opencli-control]] [[model-policy]]。
