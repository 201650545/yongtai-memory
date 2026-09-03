---
name: seedream-5-paused
description: ark 账号 seedream-5.0 已账号级暂停（SetLimitExceeded），seedream-4.5 仍可用；Seedream 系列最小像素约束
metadata: 
  node_type: memory
  type: project
  originSessionId: e5ca6684-1e8b-4ac6-95bb-d10c88057836
  modified: 2026-09-01T15:29:39.273Z
---

2026-09-01 生图时发现：ark 上游对 `doubao-seedream-5-0-260128` 返回 429 `SetLimitExceeded`——账号已达该模型推理上限（安心体验模式：免费额度耗尽自动暂停）。控制台确认 Seedream-5.0-pro 与 5.0-lite 均显示「服务暂停」。**2026-09-01 用户拍板：搁置不管，不去做控制台恢复。** 替代路由见 [[image-gen-routes]]（agnes 主 + CF flux 补 + seedream-4.5 备用）。

**Why:** 影响后续所有 v2.x 立绘/背景生成任务（gen_gap_assets.py、gen_bg_per_realm.py 等都用 5.0）。

**How to apply:** 生成任务遇 429 先直连上游探测真实错误体（网关只透传状态码，channels.json 取 ark key）；恢复前新任务一律改用 seedream-4.5 或改走 [[project-ai-gateway]] 编排组询问。另：Seedream 5.0 有最小像素约束 ≥3,686,400px，2048×1152 会被 400 拒绝，用 2560×1440 或 2048×2048。
