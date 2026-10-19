---
name: openrouter-free-list-no-ling31
description: OpenRouter 免费档只有带 :free 后缀的变体；ling-3.1-flash 是收费模型，已被 quota_guard 正确拦截
type: reference
updated: 2026-10-19
---

# OpenRouter 免费模型判定口径（2026-10-16 实测确认）

> 镜像自 Claude 内部记忆 `reference_openrouter_free_no_ling31.md`。本库为唯一可写真源。

**结论：OpenRouter 免费档只认带 `:free` 后缀的变体**（如 `google/gemma-4-31b-it:free`、`nvidia/nemotron-3-ultra-550b-a55b:free`）。**不带后缀的就是收费款**，即便渠道整体标 free。

## 具体案例：`inclusionai/ling-3.1-flash` 不是免费模型

- 审计文件 `D:\项目\ai-hub\search_gateway\data\openrouter_free_audit.json`（每日 01:38 由 `scripts/or_free_refresh.py` 生成，全目录 462 条费用审计）里，它明确落在**收费侧**（`charged_count`）：
  - prompt $0.075/M · completion $0.225/M · input_cache_read $0.015/M
  - 对比同门 `ling-3.0-flash`：prompt $0.021/M · completion $0.063/M —— **3.1 比 3.0 贵约 3.5 倍**
- 免费名单快照 `data/openrouter_free_models.json`（15 条）里**没有它**。

## ⚠️ 值得记住的假象：「能调通」≠「免费可用」

直接点名 `model=inclusionai/ling-3.1-flash` 经 `:3100` 调用**能返回 200** —— 因为它不在 `model_routes.json` 里，走了 legacy 默认链，**绕过了 quota_guard**。一旦登记成正式编排路由，guard 立刻按「OpenRouter 禁用一切付费模型」铁律拦下（`guard_not_allowlisted`）。

## 网关的两道相关闸门

- `services/quota_guard.py`：openrouter 配 `policy=allowlist` + `allow_source=openrouter_free_models.json`（快照白名单，mtime 热加载）。
- **郭老师 2026-09-22 铁律**：OpenRouter 禁用一切付费模型；主 key 付费档仅用于维持免费档每日 1000 次上限。
- openrouter `key_pools` 4 把 key：3 把免费（50 次/天）+ 1 把充值 $10（1000 次/天）≈ 1150 次/天，**只该用来跑真·免费模型**。

## 两头堵死

`inclusionai/ling-3.1-flash` 带 `:free` 后缀反而会被目录预过滤本地拒（`不在网关已知目录内`）；无后缀在正式路由下会被 guard 拦。**结论：这条模型在本网关拿不到免费通路。**

参见 [[reference_免费渠道调研_2026-09-22]]、[[reference_免费中转站与聚合代理工具池]]。
