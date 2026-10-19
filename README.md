---
name: README
type: entry
updated: 2026-10-19
description: 记忆仓的机器契约：只给 AI 读，检索优先，索引生成，结论入 git。
---

# 记忆系统 · 机器契约

> **本库只给 AI 读。** 人不看这里的排版，别为人类阅读写长文、目录树或导航页。
> 找东西用检索引擎；冷启动看自动生成的索引；要写就写结论，过程不入库。

## 一、这个仓是什么

`D:\记忆` = **记忆的唯一可写真源**（git 有 remote，公开镜像 `yongtai-memory`）。
它存四类东西：跨项目规则、项目卡、流程与教训、路由表。
它**不存**项目正文副本、过程流水、抓取素材、个人信息。

## 二、目录职责

| 目录 | 放什么 | type |
|---|---|---|
| `通用规范/` | 跨项目默认规则（00-存档、40-安全红线…） | rule |
| `调度大脑记忆/项目/` | 每个项目的背景/决策/现状 | project |
| `调度大脑记忆/流程/` | 多步骤固定流程 | workflow |
| `调度大脑记忆/教训/` | 排错经验与踩坑 | lesson |
| `调度大脑记忆/反馈/` | 人的偏好、红线、纠正 | feedback |
| `调度大脑记忆/参考/` | 外部资源、工具、协议的指针 | reference |
| `调度大脑记忆/用户/` | 用户画像与协作准则 | user |
| `项目清单/projects.yaml` | WHERE：一级项目注册表 | routing |
| `概念解释器/SYSTEM_MAP.md` | 整个工作空间的当前真实结构（**唯一系统地图**） | explainer |
| `轮次记录/` | 按日过程流水（7 天，本地删） | round |

## 三、怎么读（唯一入口）

1. **先检索**：`query_evidence.py "关键词"`（跨 Work 加 `--work "D:\Work"`）。
2. **冷启动**：读 `调度大脑记忆/索引.md`（自动生成，**禁止手改**）。
3. **要细节**：用 `locate_anchor.py` 拿真实行号，再精准读那一段。

旧 `概念解释器/00~03`、`common-concepts`、`modules/*`、`projects/*` 已合并进 `SYSTEM_MAP.md`，原文在 git 历史里，**不再作为现行事实**。

## 四、怎么写

1. 每条记忆必须有 frontmatter：`name` + `description` + `type` + `updated`。
2. **只写结论与判据**，不写流水；过程进 `轮次记录/`，且 7 天后本地删除。
3. **单写真源**：同一事实只在一处写，别处放指针。
4. `type` 词汇固定：`project / workflow / lesson / feedback / user / reference / rule / entry / memory / broadcast / explainer / routing`。
5. 写完不用手动挂索引：02:00 的 `EmbedBackfill` 会自动重建索引。

## 五、生命周期

- **7 天只管本地磁盘，不管 git 历史**（见 `通用规范/00-存档与内化.md` §五）。
- **git 只收结论与规范**；过程产物、抓取素材、个人信息一开始就不进 git。
- 发布 = 本地更新后 `git push`；GitHub 上是核心内容的镜像，没有 7 天删除机制。

## 六、校验

- `元智能\runners\build_memory_index.py --check`：缺字段 / 重名 / 重复段落。
- 22:00 收尾自检 `session_close_lint.mjs` 的 `记忆schema` 项：异常即红。
