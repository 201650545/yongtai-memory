---
name: handoff-require-brief-report
description: 交接任务给外部执行 AI 时，须要求其完成后写一份简短汇报
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 72205e30-501c-4c38-91a5-20cf27cb4d60
  modified: 2026-08-04T14:15:44.661Z
---

每次把任务交接给另一个 AI（可读本地文档的执行 Agent）时，交接/开工说明文档末尾的「验收输出」节必须固定要求：**完成后回报一份简短汇报**——模块×验收项 PASS/FAIL 表、变更文件清单、验证结果、已知偏差。例：《B类收口交接_给执行Agent_20260804.md》的执行方即产出《最终交付清单》。

**Why:** 郭老师明确要求（2026-08-04）。中继核对与归档都需要执行方自述，不能只交文件不交汇报。

**How to apply:** 写交接文档时，「验收输出」节模板写：完成后回报：① 模块×验收项 PASS/FAIL 表 ② 变更文件清单 ③ 验证结果 ④ 已知偏差。相关：[[workflow-human-ai-research]]、[[reference_skill_tech_cofounder]]。
