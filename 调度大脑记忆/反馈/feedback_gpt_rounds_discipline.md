---
name: feedback-gpt-rounds-discipline
description: 委派 GPT 镜像站时执行轮次纪律——一窗口最多 12 轮、每 3 轮必须彻底解决一个任务（GPT 反问也在此窗口内继续，不算新任务）
metadata:
  node_type: memory
  type: feedback
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
  modified: 2026-09-03T15:51:20.923Z
---

用户（2026-09-03）明确的 GPT 镜像站对话轮次纪律：

- **一个聊天窗口最多 12 轮对话**，不要无限续。
- **每 3 轮必须完成一个任务**：我带着一个任务/问题去问 GPT，就在这 3 轮内把它彻底解决；GPT 有时会反问或交流，那我就在同一窗口跟它对话继续，把它当成完成任务的一部分，而不是开新任务/新窗口。
- 每次委派带**单一、明确的任务**，3 轮内闭环（拿到结论/方案/答案）。

**Why:** 窗口拖太长 GPT 上下文臃肿、质量下降、成本高；用户整套流程是「一任务一窗口、3 轮内彻底解决」，之前委派 agent 反复重走流程/绕圈触怒过用户。
**How to apply:** 委派给镜像站的外部 agent 时，必须在 prompt 里写明「本次任务目标 + 3 轮内闭环，不另起窗口/任务」。同一任务的追问、GPT 反问都算在该任务这 3 轮窗口内。关联 [[workflow_gpt_repo_sync]] [[feedback_decision_only_reporting]]。