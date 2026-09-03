---
name: trae-solo-opencli-control
description: opencli 可全自动控制 TRAE SOLO CN（CDP 9235）对话：open-task 打开任务、send 发消息等回复
metadata: 
  node_type: memory
  type: project
  modified: 2026-08-30T08:10:41.130Z
  originSessionId: 8ee5c1ea-99c5-4cbe-bf2c-52824ee32254
---

**opencli 已能全自动控制 TRAE SOLO CN 对话**（2026-08-30 扩展 trae-solo adapter 落地）：

- `opencli trae-solo open-task --project <任务名>`：从项目列表打开指定任务进聊天工作区（不指定则开第一个可见任务）。点击 `.task-list-row-wrapper`，等 `.chat-input-v2-input-box-editable` 出现即成功。
- `opencli trae-solo send "<prompt>" [--timeout N] [--raw]`：**自动注入输入框 → 点 `.chat-input-v2-send-button` → 轮询等回复完成 → 读 AI 回答返回**。自动打开第一个/匹配任务兜底。`--raw` 返回整轮文本。
- `opencli trae-solo eval "<js>"`：调试用，任意 JS 求值。
- 提取器：用户消息 `.turn__user-message`；AI 正文 `.turn__agent-message .agent-plan-item`；思考过程 `.core-expandable-section`。完成判定 = 正文连续稳定 2.5s + 输入框 contenteditable 恢复。
- 输入框是 Lexical 编辑器：`box.focus()` + selection 定位 + `document.execCommand('insertText', false, text)` 注入。
- 当前聊天模型 DeepSeek-V4-Flash 正式（:3100 网关免费模型），符合「测试用免费模型」规矩。
- 布局：项目列表（无输入框）↔ 聊天工作区；侧边栏任务列表与聊天主区可共存。

**How to apply:** 需要让 Trae 干活（写代码/分析/文档）时直接用 `opencli trae-solo open-task --project X` + `opencli trae-solo send "任务"`。关联 [[browser-session]]（opencli 机制）、[[feedback-on-demand-orchestration]]。
