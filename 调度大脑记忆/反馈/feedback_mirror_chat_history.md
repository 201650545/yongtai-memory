---
name: mirror-chat-history-limit
description: ChatGPT 镜像版聊天历史 ≤30 条，每到 30 删一半（非删 10 条）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f059f218-e941-4b54-98ea-83c91434329e
  modified: 2026-08-30T06:58:10.290Z
---

用 ChatGPT 镜像版（AI问答宝/vip 实例）时，**最近的聊天历史记录不能超过 30 条；每达到 30 条就删除一半**（保留最近 15 条）。此前规则是「每 30 删 10」，2026-08-30 用户改为「每 30 删一半」。

**Why:** 历史会话过长会拖慢镜像站页面、混入旧上下文干扰当前问诊；用户明确要求收紧清理力度。

**How to apply:** 在镜像站操作过程中留意会话列表条数，≥30 时清理一半（删除最旧的一半，保留最近 15 条）。关联 [[gpt-mirror-account-switch]]、TOOLS.md §4 会话纪律（每任务 ≤3 轮、每窗口 ≤12 轮）。
