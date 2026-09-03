---
name: feedback-report-receive-rule
description: 子 Agent 交付汇报后调度大脑必须立即回写 STATE/CHANGELOG，不要等下一次会话
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
  modified: 2026-09-03T06:52:53.659Z
---

子 Agent（TRAE/codebuddy/逆天执行位）交付汇报文件到 workers/ 或类似路径后，**调度大脑必须在当日（或下次主动调度时）回写**对应项目 STATE/CHANGELOG 的"已完成(最近)"段，**不要等下一次会话才补**——郭老师会问"漏项"，9-1 交付的汇报 9-3 才发现没回写就是反例。

**Why:** 9-3 郭老师拍桌"v2.8 汇报我没读没回写"。汇报文件存在但 STATE 没同步 = 调度大脑漏项，子 Agent 的 commit 不等于 STATE 闭环。漏读超过 1 天 = 漏项。

**How to apply:**
1. 派任务时在交接文档固定要求"汇报路径 + 4 项格式"，并在调度大脑自己的 TODO 里加一项"读汇报+回写"
2. 看到 git log 子 Agent 有 commit 但 STATE "已完成(最近)" 没对应条目 → 主动读 commit 的汇报文件 + 补 S-XXXXXXXX
3. 跨项目汇报要记到正确项目（不能凭项目名猜归属，9-3 v2.8 实际是 nitian-theme 不是 ai-resources）
4. 4 项对照（模块×验收项 / 变更清单 / 验证 / 已知偏差）是 [[handoff-require-brief-report]] 必选模板
5. 漏项反思进 STATE"已完成(最近)"段末尾，避免再犯

相关：[[handoff-require-brief-report]]、[[feedback-decision-only-reporting]]。
