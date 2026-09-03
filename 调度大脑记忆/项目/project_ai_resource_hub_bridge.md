---
name: ai-resource-hub-bridge
description: ai-resource-hub 公开数据桥加固完成（10 条 GPT 建议全落地）；真实 BASE_TOKEN 已在 git 历史，接受现状不清理
metadata: 
  node_type: memory
  type: project
  originSessionId: 95cff9f0-c115-4770-a66a-5ed8ec23a5c2
  modified: 2026-08-11T15:38:38.487Z
---

ai-resource-hub（github.com/201650545/ai-resource-hub）公开数据桥 exporter 于 2026-08-11 完成 GPT Extended 审查后全部 10 条加固并实测通过：scanner 不打敏感值、视图 fail-closed、删反推字段、语义 validator（count/主键/引用/字段集/枚举/值形状/数量突变>30% 阻断）、build_id 变更才部署、Secret job/Pages job 拆分、HTTP retry+错误日志清洗、失败通知 job、classification 声明+硬校验（未分类字段默认拒绝导出）。

**已决策：** 真实飞书 BASE_TOKEN 硬编码在 feishu/ 脚本（build_v03.py 等 7 个）+ 2 份 docs，且已在公开仓库 git 历史。评估为**接受现状**——base token 是半敏感标识（需配 app_secret 才可读写），单独泄露仅能看到 Base 存在；不轮换、不重写历史。后续 AI 看到硬编码 token 不要再提议清理。BRIDGE_ALERT_WEBHOOK 未配置（notify 静默跳过，需要时再配）。

**Why:** 避免未来 AI 因历史遗留的硬编码 token 重复提议破坏性清理（filter-repo/轮换），浪费时间且有风险。

**How to apply:** 涉及 ai-resource-hub 时，直接沿用现状；新增公开字段须走「飞书建字段 → whitelist+classifications 声明 → mock+validate 验证 → push」流程。关联 [[reference-feishu-app-qclaw]] [[project-ai-gateway]]。
