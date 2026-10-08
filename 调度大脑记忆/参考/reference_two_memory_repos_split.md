---
name: reference-two-memory-repos-split
description: handbook v1.0 §6 定死两个 memory 仓的区别——yongtai-memory＝人的记忆/调度大脑长期上下文（真源 D:\记忆，GitHub 是脱敏镜像）；ai-hub-memory＝Agent 系统运行/协作记忆（STATE/DECISIONS/CHANGELOG），不是个人 PKM，不要为了"仓库少"强行合并；附元智能 home_template.md:23 的错处
metadata:
  node_type: memory
  type: 参考
  originSessionId: f969104b-ab73-4eac-a3ef-2a2649f10525
  modified: 2026-09-29
  关联批次: 2026-09-29 memory-work-inventory（口径A 713 份／口径B 653）
---

# 两个 memory 仓怎么区分（权威条款在 handbook）

**与 [[project_shared_memory]] 的分工**：那条讲 `ai-hub-memory` **怎么用**（分层协议、读写什么）；这条讲**两个仓怎么区分、哪个是权威**，以及查出的入口错账。

## 权威条款（handbook v1.1，2026-09-03 定稿 / 2026-10-08 升版；§5 已复核落地）

| 仓 | 是什么 | 真源 | GitHub 角色 |
|---|---|---|---|
| **`yongtai-memory`** | 人的记忆／调度大脑长期上下文 | **`D:\记忆`**（唯一可写 canonical） | 脱敏镜像，只读 |
| **`ai-hub-memory`** | Agent 系统运行／协作记忆（STATE / DECISIONS / CHANGELOG / coordination） | 本地工作树 | 协作面 |

**明确禁止**：「**不要为了"仓库少"强行合并**（数据类型不同）」。

**2026-10-08 已了结的旧待办（郭老师裁定：整合，不是二选一）**：本机原有两份可写克隆 `D:\ai-hub-memory` 与 `D:\项目\ai-hub-memory`（同一 remote）。处置＝`D:\项目\ai-hub-memory` 为唯一可写本体，未推送的 commit 已 rebase 并上、push 完成；`D:\ai-hub-memory` 改为 **junction 指向它**（旧目录内容已删，仅 3 个 `.pyc` 有差异）。`projects.yaml` 的 `caution` 已改为 `status_note` 记此结论。⚠️ 教训：**"选一份留一份"是错解**，同 remote 的双克隆正确解法是收口 + junction 防忘。

## 单写真源法则（handbook §0，全系统唯一同步法则）

> 不要追求"全系统只有一个真源"，要做到"**同一种数据只有一个可写真源，其余全部是镜像／投影／缓存／审计**"。

- 可写 = 允许人工编辑、是最终事实来源
- 镜像／投影／缓存 = 只读派生，**禁止反向写**
- 双向同步**原则上禁止**（单人系统不值得维护冲突解决机制）

发布方向固定单向：编辑 `D:\记忆` → commit → push → 镜像。飞书已退出记忆主链，只留 append-only 审计，**绝不飞书 → Obsidian 自动回写**。

## Owner Source 表（对象 → 唯一可写源，handbook §3）

| 对象 | 唯一可写源 |
|---|---|
| 项目文档 | 本地 Obsidian |
| Handbook | 本地 handbook 仓（`D:\Work\通用规范`） |
| 项目台账 projects.yaml | 本地项目仓 |
| **个人记忆** | **`D:\记忆`** |
| GitHub 镜像 / Pages JSON | 派生（只读） |
| 飞书原生运营表 | 飞书 |
| **Agent 运行状态** | **Agent memory 系统** |

⇒ 最后两行是分界：**关于"他"的记忆必须落 `D:\记忆`**；各 Agent 自己的运行状态留在各自的 memory 系统（Qoder auto-memory / Claude 内部 memory / WorkBuddy）。**别把 Agent 运行状态当个人记忆写进 `D:\记忆`，也别把个人记忆只留在 Agent 筒仓里**——后者正是他抱怨"换个 Agent 就要重讲一遍"的根因。

## 查出的入口错账（2026-09-29 实测，均未擅自改）

**1. `D:\Work\元智能\machine\home_template.md:23` 事实错误。**
原文：「持续记忆真源 = **D:\记忆**（跨 Agent／跨会话的状态、决策、协作记忆）。GitHub 运行仓 = ai-hub-memory。」
→ 把 `ai-hub-memory` 挂在了 `D:\记忆` 名下。实测 `D:\记忆` 的 origin 是 **`yongtai-memory`**（`git remote -v`）。按 handbook §6，两者是**不同数据类型、明令不得合并**的两个仓。
**为什么要紧**：外部 AI 读的正是这份模板（它的读取顺序口诀"先 WHERE 后 WHAT 再 FACT"）。照它去 clone `ai-hub-memory` 当记忆真源，会拿到协议完全不同的另一个仓。

**2. `ai-hub-memory` 有两份可写本地克隆**：`D:\ai-hub-memory` 与 `D:\项目\ai-hub-memory`，同一个 remote。元智能写前者（`runners\gpt-mirror-review.mjs:33` 的 `OUT_DIR`），本库 `project_shared_memory.md:11` 登记的是后者。
**为什么要紧**：两个工作副本对同一远端各自可写 = 违反 handbook §0 的单写法则。

**3. `D:\记忆\README.md:8` 悬空指针**：引用的 `D:\通用规范\50-知识管理三工具规范.md` 中，`D:\通用规范` **不存在**，真身在 `D:\Work\通用规范\`。见 [[reference_handbook_ssot]]。

## 关联（Work 原文锚点，勿复制正文）

| 内容 | 原文 | sha16 | 章节 |
|---|---|---|---|
| 单写真源法则 | `D:\Work\通用规范\50-知识管理三工具规范.md` | `7b0e69db6d30683d` | §0 |
| 三工具定位 + 禁止项 | 同上 | `7b0e69db6d30683d` | §1 |
| 单向发布闭环 + 坑A | 同上 | `7b0e69db6d30683d` | §2 |
| Owner Source 表 | 同上 | `7b0e69db6d30683d` | §3 |
| Memory 单写规则 | 同上 | `7b0e69db6d30683d` | §5 |
| **两个 memory 项目定死区别** | 同上 | `7b0e69db6d30683d` | **§6** |
| 本库自己的单写规则 | `D:\记忆\README.md` | — | §「单写真源规则」 |

sha16 由 `runners\memory-scan-work.mjs` 于 2026-09-29 批算出；错账由 `runners\memory-link-check.mjs` 同批复出。

关联条目：[[project_shared_memory]]、[[reference_handbook_ssot]]、[[feedback_handbook_security_redlines]]、[[feedback_memory_also_obsidian]]。
