---
name: feedback-memory-also-obsidian
description: 记忆不只存 Claude 内部，还须落到用户的 Obsidian 建一个跟 GitHub（ai-hub-memory）同等待遇的记忆项目，人可读可查
metadata:
  node_type: memory
  type: feedback
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
  modified: 2026-09-03T15:59:34.839Z
---

用户（2026-09-03）指示：**记忆不能只落实在 Claude 自己的记忆里（`~/.claude/projects/<cwd>/memory/`），还必须在用户的 Obsidian 里有一个「跟 GitHub 一样」的记忆项目**——即像 ai-hub-memory 那样独立存在、人能开 Obsidian 看/查、能同步到 GitHub，而不是埋在小练习不可见的内部文件里。

**Why:** Claude 内部记忆用户看不到，用户希望记忆是一份他自己也能打开 Obsidian 读、能随仓库同步走的人读资产；GitHub 已有 ai-hub-memory 同款待遇，Obsidian 端要对等。
**How to apply:** 写记忆时（尤其 feedback/project 型）同时要考虑落到 Obsidian 侧的记忆项目（模块位置待用户拍板）；Claude 内部记忆仍是被基础调度引用的运行层，Obsidian 记忆 = 人读镜像我同步。关联 [[shared-memory-repo]]（⚠️ 断链，目标不存在，2026-10-01 审计） [[feedback_chinese_naming]]。

**✅ 2026-09-03 已拍板并落地**：Obsidian 记忆项目 = `D:\记忆`（原本是你飞书记忆系统三件套的家），现补成 vault（.obsidian/ + Home.md），新增 `调度大脑记忆/` 层 = Claude 内部 50 条记忆的镜像（反馈/项目/参考/流程/教训 + 索引），本地 git 已初始化并提交。**GitHub 同步：暂不推，保持本地**（记忆含飞书 base_token 等敏感引用，公开推送有泄露风险，用户选本地即可）。Claude 更新内部记忆时同步镜像到这里。

---

## ★ 记忆分层框架：「宪法 vs 地方法律」（郭老师 2026-09-15 提出）

**郭老师原话**：「这些除了是记忆，还有在 Obsidian 的 work 项目中的宿舍比赛也要记录。等于说，这两个方面都要记录，**记忆是全局性规范，就像一部法律在任何地方都通用。而在项目中要有详细的项目规范，就像地方法律一样，那么记忆就是宪法**。」

### 采纳后的准确模型（含对原比喻的一处修正）

郭老师的**上下位/宽窄**描述方向正确，但两者真实关系是 **「分工」而非「派生」**：

| | 记忆库（宪法） | 项目规范（地方法） |
|---|---|---|
| 位置 | WorkBuddy `~/.workbuddy/MEMORY.md` ＋ 项目 `.workbuddy/memory/` | Obsidian `调度大脑记忆/项目/project_*.md` |
| 管什么 | **我怎么做事**（行为准则 / 流程纪律） | **这件事怎么做**（领域规则 / 成果标准） |
| 例子 | "郭老师的灵感式提问必须当场落库" | "封面文字四层：190px/46px/38px/32px" |
| 换项目是否有效 | ✅ 有效 | ❌ 无效（换课、换比赛就不适用） |
| 谁执行 | AI | AI ＋ 郭老师共同约定 |

**为什么不是"派生"关系**：项目规范里**绝大多数内容在宪法中没有任何对应条款**——
例如"封面文字四层字号"是**独立产生的领域知识**，不是任何行为准则的下位细则。
**更准确的比喻**：像「**宪法**」与「**技术标准**」——宪法不会派生出一份建筑规范，但两者都必须有。

### 强制双写规则（升级版）

**任何一条规范，判断归属后写入对应位置，两边不可互相替代：**

| 该规范的性质 | 写入位置 |
|---|---|
| 跨项目行为准则（怎么跟郭老师配合、怎么做事的纪律） | ① WorkBuddy 用户级 `~/.workbuddy/MEMORY.md`（宪法） |
| 本项目领域规则（字号/色值/结构/赛事规定） | ② Obsidian `项目/project_<项目名>.md`（地方法）**＋** WorkBuddy 项目 `MEMORY.md` |
| 本次执行细节（做了啥、发现啥） | ③ WorkBuddy 项目 `.workbuddy/memory/YYYY-MM-DD.md`（日志） |

**自查**：每轮结束用 `grep` 关键词在三处计数，**任一为 0 即为漏写**。

### 已发生的事故（2026-09-15）
本轮确立 6 条制作规范后，我只写了 WorkBuddy 三处，**漏了 Obsidian 项目文件**，
直到郭老师追问「Obsidian 的 work 项目中的宿舍比赛也要记录」才发现。
**此后 project 型内容必须先落 Obsidian，再回写 WorkBuddy。**
