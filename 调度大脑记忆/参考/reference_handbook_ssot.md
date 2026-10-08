---
name: reference-handbook-ssot
description: D:\记忆\通用规范 是跨项目通用规范总库（handbook v1.0，SSOT）；规则优先级＝项目明确override＞项目自身规格＞handbook默认；引用必须钉版本号；三层职责＝workspace-index只索引/项目仓只写特有/handbook不存项目状态
metadata:
  node_type: memory
  type: 参考
  originSessionId: f969104b-ab73-4eac-a3ef-2a2649f10525
  modified: 2026-09-29
  关联批次: 2026-09-29 memory-work-inventory（口径A 713 份／口径B 653）
---

# 通用规范去哪查：handbook = 跨项目 SSOT

**位置**：`D:\记忆\通用规范`（有 git；10 份 .md；当前版本 **v1.0**）

⚠️ **不是 `D:\通用规范`**——那个路径不存在。`D:\记忆\README.md:8` 曾按 `D:\通用规范\50-知识管理三工具规范.md` 引用，是**悬空指针**（`memory-link-check.mjs` 2026-09-29 批已报出）。

## 规则优先级（背下来）

```
项目明确 override  >  项目自身规格  >  handbook 默认规范
```

**引用 handbook 必须写明版本号**（如「继承 handbook v1.0，例外如下」），否则规则演进会让旧项目语义漂移。

## 三层职责（多仓 SSOT）

| 层 | 管什么 | 不管什么 |
|---|---|---|
| workspace-index | 有哪些项目、去哪找 | **不保存任何正文副本** |
| 项目仓 | 这个项目现在真实是什么 | 事实 + 对 handbook 的例外 |
| handbook | 所有项目默认应该怎么做 | **不保存项目状态** |

⇒ **记忆库（本库）在这三层里扮演的是"目录"角色**：只放核心词 + 指回原文，不复制正文。这与 handbook 的分工一致，不是另立一套。

## 索引（六份规范各管一段）

| 文件 | 管什么 | sha16 |
|---|---|---|
| `README.md` | 总入口、优先级、三层职责、用法 | `c88aef58cd69fb4c` |
| `10-协作规范.md` | 人/Agent/外部模型分工、镜像站协作协议、执行纪律 | `8182d1b81fbd092c` |
| `20-出图与资产规范.md` | 出图规格、提示词锚点模板、命名与底图管理 | `6350e3381dd0ae23` |
| `30-台账格式.md` | 任务看板与资产清单的统一格式 | `92f757f970547776` |
| `40-安全红线.md` | 密钥/资产/隐私红线（无例外） | `3e51ca953e22d456` |
| `50-知识管理三工具规范.md` | Obsidian/GitHub/飞书 职责定界 + 单写真源法则 | `7b0e69db6d30683d` |
| `60-开发者与管理者角色.md` | 他个人的角色定位 + 持续学习地图 | `0e580a7aa86d6f8b` |
| `templates/` | 新项目开工骨架（README / project.yaml / 台账） | — |

sha16 由 `D:\Work\元智能\runners\memory-scan-work.mjs` 于 2026-09-29 批算出。

## 外部协作者（AI）的读取顺序

先读 workspace-index 定位项目 → 读项目 README 与 `docs/00` 总览 → 需要规范再查 handbook（**注意项目声明的版本号**）。
新项目开工：从 `templates/` 复制骨架，docs 头部声明「继承 handbook v1.0，例外如下」。

## 仓库管理约定

一项目一仓；main 单分支，文档改动即 commit，按里程碑推送；仓库内只有代码与文档，**成品资产一律不进 git**（见 [[feedback_handbook_security_redlines]]）。

⚠️ **实测现状与此约定不符**：15 个 Work 项目里只有 5 个有 git（AI平台／课程思政教学竞赛／跃己／逆天主题／通用规范），10 个无 git。无 git 的项目只能靠 sha256 当锚点，漂移只能复算发现。

关联条目：[[user_guo_three_identities]]、[[reference_two_memory_repos_split]]、[[workflow_collab_discipline_and_ledger]]。
