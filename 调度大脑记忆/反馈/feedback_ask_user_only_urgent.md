---
name: feedback-ask-user-only-urgent
description: 除非极必要/极重要的问题才问郭老师；大部分问题直接去问 ChatGPT 镜像版（opencli chatgpt ask）解决，不占用他时间审核
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
  modified: 2026-09-03T16:28:28.870Z
---

绝大部分问题**不要问郭老师**，直接去问 **ChatGPT 镜像版**，我（Claude）和镜像版互相商量、互相配合解决就好。

只有一种情况才回问郭老师：**非常有必要、非常重要的决断**（涉及他不肯放手的核心选择）。

**Why:** 郭老师明确说「我没有那么多时间来审核」——他没空逐条复核我的琐碎问题；委托我给镜像版做日常咨询过滤。

**How to apply:**
- 日常/大部分问题 → `opencli chatgpt ask <prompt>`（或镜像标签页）问 GPT 镜像版，返回后我自己综合落地，不打扰郭老师。
- 架构/内容方案的第二个意见 → 走镜像版（配合 [[feedback_proactive_improvement]]）。
- 只有触及「真必要、真重要」的拍板（如隐私/公开/花真实额度/删数据等不可逆或大影响）才用 AskUserQuestion 问郭老师。
- 相关：[[project_cost_strategy]]（不买付费AI订阅，镜像版GPT-5.6够用）、[[feedback_gpt_rounds_discipline]]（镜像窗口轮次纪律）。