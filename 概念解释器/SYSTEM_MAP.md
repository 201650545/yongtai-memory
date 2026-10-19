---
name: SYSTEM_MAP
type: explainer
updated: 2026-10-19
description: 整个工作空间当前真实的分层、仓边界、真源分工与已废弃对象。AI 只读这一页就够，不要再翻旧的 concepts 系列。
---

# SYSTEM_MAP · 工作空间当前真实结构（2026-10-19）

> 本页是旧的 `概念解释器/00~03`、`common-concepts`、`modules/*`、`projects/*` 的合并替代。
> 旧系列按 2026-09-03 的 Workspace 架构写，其中 AI平台/ai-platform 已于 2026-10-12 删除，
> 那些文档留在 git 历史里，**不再作为现行事实**。

## 一、两个 Vault

```
Workspace
├─ D:\Work         内容层：项目、产品、规范、脚本（各子项目自带 .git）
└─ D:\记忆         记忆层：可写的记忆真源（本库，有 remote，公开镜像）
```

`D:\Work\元智能` 是嵌在 Work 里的独立仓（控制平面：技能库/定时任务/巡检）；Work 根仓 `.gitignore` 已排除它。

## 二、四个仓的真实分工

| 仓 | 位置 | 管什么 | 不管什么 |
|---|---|---|---|
| 记忆仓（yongtai-memory） | `D:\记忆` | 结论、规范、项目卡、流程、教训、反馈、检索索引 | 不存项目正文副本；不是过程流水 |
| Work 根仓 | `D:\Work` | 项目事实与内容（按 `public-surface.json` 正向白名单） | 不存记忆结论；不存个人信息/产物 |
| 元智能 | `D:\Work\元智能` | 控制平面、技能库真源、40_定时任务、runners 巡检 | 不存业务内容 |
| Agent 记忆 | `D:\项目\ai-hub-memory` | 多 Agent 共享的 STATE/DECISIONS/CHANGELOG | 不替代本记忆仓的结论与规范 |

## 三、真源三分（互不越权）

- `项目清单/projects.yaml` —— **WHERE**：有哪些一级项目、去哪找。
- 本库各条目 —— **WHAT / DECISION**：它是什么、之前怎么定的、现在接着哪里做。
- 各项目 Owner 仓 —— **FACT**：它现在真实是什么（README → docs/00）。

一句话：**projects 定去哪；记忆定是什么、怎么定的；项目仓定现在真实是什么；通用规范定默认怎么做。**

## 四、三个不等号（仍然有效）

- **Vault ≠ Git 仓**：Vault 是浏览/知识工作空间，仓是版本与发布边界。
- **项目 ≠ 文件夹**：项目是责任与生命周期，文件夹只是物理承载。
- **数据源 ≠ 项目**：飞书 Base / JSON / API 可以服务项目，不因此成为一级项目。

## 五、进 `projects.yaml` 的判定（仍有效）

同时满足才进：① 一级责任单元；② 有独立 Git 仓/版本生命周期；③ 有稳定入口（README/project.yaml）；④ 外部 Agent 有合理场景直接路由进入。

机械判定：**能否作为一个独立 Git 仓被陌生 Agent 直接进入，并且进去后有一套自己的事实/规范/生命周期？**

## 六、已删除 / 已改名（别再去追）

| 对象 | 状态 |
|---|---|
| AI平台 / ai-platform | 2026-10-12 本地与远程仓彻底删除；相关 concepts 文档作废 |
| 项目学习、relativity-video、buoyancy-film | 2026-10-19 删除 |
| `_backups`、`_归档`、听诊/镜像旧备份 | 2026-10-19 删除（git 历史可查） |
| 课程思政教学竞赛 | 2026-10-19 改名 `教案与课件设计` |
| 工具之家 `D:\Work\工具` | 2026-10-19 改名 `D:\Work\备份与安检` |
| 飞书记忆主链 | 已废止；飞书只保留结构化数据用途（且当前未启用） |

## 七、AI 访问协议（唯一入口）

1. **找东西先检索**，不要全本读笔记：
   `python D:\Work\元智能\10_AI自成长引擎\技能库\local-knowledge-engine\scripts\query_evidence.py "关键词"`（加 `--work D:\Work` 联查内容层）。
2. 冷启动的确定性入口是**自动生成的索引**：`调度大脑记忆/索引.md`（**禁止手改**，由 `元智能\runners\build_memory_index.py --build` 生成）。
3. 每条记忆带 `type` + `updated`；type 词汇：`project/workflow/lesson/feedback/user/reference/rule/entry/memory/broadcast/explainer/routing`。
4. 写记忆前先读 `通用规范/00-存档与内化.md`：**7 天只管本地，git 只收结论**。
