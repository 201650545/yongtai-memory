---
name: reference_两仓RAG运行事实_EmbedBackfill
description: 查证 2026-11-18：D:\记忆 与 D:\Work 两个仓的 RAG（语义向量检索）由计划任务 EmbedBackfill 每日 02:00 维护，实测两仓覆盖率均 100%（记忆 5158 块 / Work 100623 块），混合检索 hybrid_rrf 现场可用；该任务属检索基础设施，不可撤。另记 RAG 与「AA 榜单」两条链互不相干，别混为一谈。
type: reference
updated: 2026-11-18
status: active
---

# 两个仓的 RAG：跑什么、跑得怎么样、能不能撤（2026-11-18 查证）

## 一、结论

**两个仓都配了 RAG，每天在跑，而且状态良好。这是检索基础设施，不能撤。**

| 项 | 事实 |
|---|---|
| 计划任务 | `EmbedBackfill`，每日 **02:00**，`LastTaskResult = 0` |
| 入口 | `embed_backfill.ps1` → 顺带重建开工卡 → `embed_backfill.py` |
| 覆盖仓 | `VAULTS = [D:\记忆, D:\Work]`（正是他说的两个仓） |
| 底层引擎 | `技能库\local-knowledge-engine`（本地 ONNX embedder，无外部 API、不花钱） |
| 写哪 | 只写 `<vault>\.cache\` 与日志，**绝不改知识真源** |

## 二、实测覆盖率（2026-11-18 02:00）

```
记忆: before 1.0  sections 5160 → after 1.0  covered 5158/5158
Work: before 0.9964 sections 100548 → after 1.0 covered 100623/100623
```

两仓 **100% 覆盖**，状态文件 `ok: true`。

## 三、检索实测（现场验证，非推断）

`D:\记忆\q.cmd "开工卡 门禁"` → 命中 3 条，标注 `类型: hybrid_rrf`（中文词级 + 语义向量混合）。
`q.cmd "软链 resolve"` → 能跨库召回到 Work 侧的网关文档 —— 说明语义通道确实在工作，不只是关键词匹配。

## 四、它做了什么（一句话）

把两仓笔记切成 section → 给每块算语义指纹存本地 → 让 Agent 能「按意思找」而不只是「按字面找」。

这是他明确想要的：**帮 AI 快速找到重点、省资源、提效**。与「省 token、少读整本大文件」的 G-04 铁律同源。

## 五、⚠️ 别把两条链混为一谈

本轮排查纠正过一次误判：**RAG 与 AA 榜单没有任何依赖关系**。

| 链 | 状态 |
|---|---|
| RAG（EmbedBackfill） | ✅ 正常，100% 覆盖，要留 |
| AA 榜单（AALeaderboardRefresh） | ❌ 站点改版已坏 4 天，数据停在 11-14，可撤 |
| 免费模型发现 | `FreeCandidateRefresh` 依赖 AA 榜 → 同罪已撤；`OpenRouterFreeRefresh`/`ChannelFreeAudit` **自己抓站点、不依赖 AA 榜**，仍正常且供编排器当天使用 → 保留 |

## 六、相关

- 引擎用法与检索铁律：skill `local-knowledge-engine`
- 开工卡每日同批重建：[[参考/reference_开工卡与README入口约定的设定时间与更新链路]]
- 覆盖率门槛：`COVER_OK=0.99`、`COVER_ALERT=0.95`，低于 0.95 会写 `渠道警报.log`（不许静默）
