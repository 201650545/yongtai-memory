---
name: mirror-chat-history-limit
description: ChatGPT 镜像版聊天记录保留最近 10 条即可，超了就删最旧的（Delete 真删）；列表顶部=最近、底部=最旧，从末尾往上删
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f059f218-e941-4b54-98ea-83c91434329e
  modified: 2026-09-04T14:32:11.860Z
---

用 ChatGPT 镜像版（AI问答宝/vip 实例）时，**聊天记录保留最近 10 条**；超了就从最旧的删起（列表顶部=最近、底部=最旧，**从末尾往上删**），删到剩 10 条最近为止。

**规则细节：**
- 删除方式 = **Delete 真删**（不可逆），不用 Archive。
- 只删**旧会话**，顶部最近的 10 条最看好保留。
- 批量用**脚本循环**一次删到位，不逐条手点（手点太慢）。
- 每条删除：精确定位该会话项的 `button[aria-label="Open conversation options for <title>"]`（**别用通用匹配，会抓成顶部那条**）→ 菜单 Delete → 确认框 Delete。

**Why:** 历史会话过长拖慢镜像站页面、混入旧上下文干扰当前问诊。2026-09-04 用户从「每 30 删一半」收紧为「保留最近 10 条、删最旧」。

**How to apply:** 在镜像站操作时留意会话列表条数，>10 就走脚本删末尾至剩 10。关联 [[feedback-gpt-mirror-account-switch]]、[[feedback-gpt-mirror-subagent-flow]]、手册 §四（账号与窗口纪律）。