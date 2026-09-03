---
name: feedback-subagent-gateway-burn
description: 子 Agent 本体是 Claude 不能换成别家模型；要真烧网关渠道额度（魔塔/官方/B.AI）→ 让子 Agent 当执行壳 POST :3100，日记才有记录
metadata: 
  node_type: memory
  type: feedback
  modified: 2026-09-03T16:39:07.900Z
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
---

郭老师（2026-09-03）指正：派子 Agent 跑任务，目的是**真实消耗网关里那些渠道的 API 额度**（魔塔每日过期/DeepSeek官方/B.AI 等），并从**网关用度日志**看到记录。他检查日志发现 fork 子 Agent 没有记录，追问是否子 Agent 用了我自己的模型。

**诚实结论（能就是能，不能就是不能）：**
- fork/general-purpose 子 Agent 是 Claude 进程派出的子进程，**其推理继承我的模型配置，无法把本体换成别家模型**——这是硬限制，如实承认，不假装。
- **能达到同样效果的路径**：让子 Agent 只当**执行壳**，把任务 POST 到网关 `:3100/v1/chat/completions`（model=deepseek-free，魔塔打头），由网关真调魔塔/DeepSeek官方/B.AI 的 API，拿到结果再落地。这样**网关 rate-ledger/用度日志有真实记录，额度真烧在那些平台**。

**Why:** 郭老师要的是"用那几个平台的 API 额度+看得见用度"，不是让 sub-agent 空转在我的算力上；日志无记录他会立刻发现并追问。
**How to apply:** 派执行类子 Agent 时，凡是要"烧网关渠道"的任务，让子 Agent 封装参数调 `:3100`（deepseek-free，路由魔塔优先）并把返回写盘落地，而不是子 Agent 自己推理完事；网关日志作为验收证据。关联 [[feedback-ask-user-only-urgent]] [[project-ai-gateway]]。