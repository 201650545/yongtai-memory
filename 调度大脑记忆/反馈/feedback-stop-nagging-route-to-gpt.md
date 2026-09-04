---
name: feedback-stop-nagging-route-to-gpt
description: 不要反复向郭老师确认；决策/验证类默认自己办或问 GPT extend，只在「非常重大/破坏共享运行时」的事才停下来。做完就完结。
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
  modified: 2026-09-03T23:47:54.735Z
---

不要反复向郭老师发问。做完就完结，不要一件事喘不了气地确认来确认去。

**Why:** 2026-09-03 概念解释器收尾 + 网关 P0 批次时，我把「P0 行为验证」「monorepo 远程推不推」又抛回成问题，郭老师明确不满：「你不要反复地再向我确认什么事情了，除非非常重大的事情，不然你统一都去问 GPT extend。明明事情没做完，一直在这里问，问个啥呀？」——我的问题本身问错了对象也问太密。

**How to apply:**
- 有回报价值的小决策/验证方案/实现取舍 → 默认自己拍板，或走镜像版 GPT **extend** 商量（不要占用郭老师审核时间）。现有 [[feedback_decision_only_reporting]] / [[feedback_ask_user_only_urgent]] / [[workflow_gpt_repo_sync]] 同向。
- 只有「非常重大 / 破坏共享运行时」的动作才停手：例如 kill 正在被多工具共用的代理、改写 live 网关配置、force push、动共享基建。这类我按下不做，作为安全边界**陈述**一句，而不是当问题抛回去。
- 能离线/隔离验证的（stub、py_compile、子进程 harness）就自己做掉，不把验证方式的选择权交出去。
- 已做完的事直接收尾（标记、汇报），不反复确认；被问时只给需要决策的选项。