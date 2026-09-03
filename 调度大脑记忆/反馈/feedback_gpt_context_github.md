---
name: gpt-context-via-github
description: 向 GPT 提问时把上下文上传 GitHub 让它强读，优化提示词数量；15s 监控、上轮完成再发下轮
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f059f218-e941-4b54-98ea-83c91434329e
  modified: 2026-08-30T06:59:54.962Z
---

向 GPT 镜像站提问的方法与注意点（2026-08-30 用户明确）：

**提问方法：**
1. **上传上下文**：把需要告诉 GPT 的上下文内容上传到 GitHub，并要求 GPT 强制读取 GitHub 项目中的上下文——它能根据系统真实特点给针对性建议。
2. **优化提示词**：上传的 GitHub 项目应包含核心内容，也可以把部分提示词放进去；减少聊天窗口中提示词的数量，响应更快速。

**注意点：**
1. **实时监控**：GPT 回答过程中最好每 15 秒监控一次生成状态。
2. **避免打断**：等它上一轮回复彻底完成之后再发下一轮问题，不然会打断它的回复。

**Why:** 聊天窗口提示词过长会让镜像站响应慢/易中断（实测续问空回复）；传 GitHub 让 GPT 读仓库比贴全文更准更快。

**How to apply:** 问 GPT 前先把相关代码/数据/提示词整理成仓库文档并 push（如 ai-hub 的 docs/），提示词只写"请读取 <repo/path> 后…"，监控用 15s 轮询，发下一轮前先确认 stop 按钮消失。关联 [[gpt-mirror-account-switch]]、[[mirror-chat-history-limit]]、[[workflow-gpt-repo-sync]]。
