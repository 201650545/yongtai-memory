---
name: feedback-handbook-security-redlines
description: handbook 40-安全红线五条无例外——成品图/视频/压缩包永不进公开仓、密钥不入仓不入文档（出现即轮换）、个人记忆同步数据不入公开仓、推公开仓前必跑密钥扫描、飞书只承载结构化数据表；配套仓库约定＝一项目一仓、成品资产不进git
metadata:
  node_type: memory
  type: feedback
  originSessionId: f969104b-ab73-4eac-a3ef-2a2649f10525
  modified: 2026-09-29
  关联批次: 2026-09-29 memory-work-inventory（口径A 713 份／口径B 653）
---

# 安全红线（跨项目通用，无例外）

**这五条是 handbook 明写"无例外"的，任何项目、任何 Agent、任何紧急程度都不放行。**

1. **成品图／视频／压缩包永不进公开仓库**——`.gitignore` 扩展名黑名单兜底（png / jpg / mp4 / webm / zip / psd / log 等）
2. **密钥／API Key／JWT／登录凭据不入仓库、不入文档**；一旦出现**立即轮换**（不是删掉了事）
3. **个人记忆同步数据**（`memory-sync/` 等）**不入公开仓库**
4. **推公开仓前必须跑密钥扫描**（grep token / key / authorization / password / secret / eyJ…）
5. **飞书等外部平台只承载结构化数据表**；管理文档一律以项目 `docs/` 为准

## 配套仓库约定

一项目一仓；main 单分支；文档改动即 commit，按里程碑推送；**仓库内只有代码与文档**。

## 与"两个 vault"的呼应

Work vault 根目录**不要**做成一个大 git 仓（会陷入 nested repo / submodule / ignore 死循环）。合并 vault ≠ 合并 git repo——各项目仓保留各自 `.git`。

⇒ 所以给某个 Work 项目补 git 时，**只在该项目目录里 init，绝不在 `D:\Work` 根上 init**。

## 隐私红线（发布侧）

- 不要把整个 `.obsidian` 公布；忽略 `workspace.json`、`workspace-mobile.json`、缓存、插件运行数据、含机器路径的配置
- `D:\记忆` 分 `private/` 与 `publish/`；GitHub 上是"公开允许集中的**忠实镜像**"，**不是**所有私人记忆字节的镜像

⚠️ **实测现状**：`D:\记忆` 目前**没有** `private/` 与 `publish/` 分目录（handbook §7 坑D 与 §5 的"下一条演进建议"都点了这件事，尚未落地）。发布前必须人工判断哪些不能公开。

## 关联（Work 原文锚点，勿复制正文）

| 内容 | 原文 | sha16 | 章节 |
|---|---|---|---|
| 五条红线 | `D:\记忆\通用规范\40-安全红线.md` | `3e51ca953e22d456` | 全文（1–5） |
| 仓库管理约定 | `D:\记忆\通用规范\README.md` | `c88aef58cd69fb4c` | 「仓库管理」节 |
| 两个 vault + 坑B | `D:\记忆\通用规范\50-知识管理三工具规范.md` | `7b0e69db6d30683d` | §4 |
| 发布与隐私红线 坑C/坑D | 同上 | `7b0e69db6d30683d` | §7 |

sha16 由 `runners\memory-scan-work.mjs` 于 2026-09-29 批算出。

关联条目：[[reference_handbook_ssot]]、[[reference_two_memory_repos_split]]、[[feedback_memory_also_obsidian]]。
