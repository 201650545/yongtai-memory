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
**How to apply:** 写记忆时（尤其 feedback/project 型）同时要考虑落到 Obsidian 侧的记忆项目（模块位置待用户拍板）；Claude 内部记忆仍是被基础调度引用的运行层，Obsidian 记忆 = 人读镜像我同步。关联 [[shared-memory-repo]] [[feedback-chinese-naming]]。

**✅ 2026-09-03 已拍板并落地**：Obsidian 记忆项目 = `D:\记忆`（原本是你飞书记忆系统三件套的家），现补成 vault（.obsidian/ + Home.md），新增 `调度大脑记忆/` 层 = Claude 内部 50 条记忆的镜像（反馈/项目/参考/流程/教训 + 索引），本地 git 已初始化并提交。**GitHub 同步：暂不推，保持本地**（记忆含飞书 base_token 等敏感引用，公开推送有泄露风险，用户选本地即可）。Claude 更新内部记忆时同步镜像到这里。