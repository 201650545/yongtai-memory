---
name: Home
type: entry
updated: 2026-10-19
description: 记忆仓的极简入口。只给 AI 读：先检索，索引自动生成。
---

# 记忆仓

> 这个库**只给 AI 读**，人不看。不要按目录翻找 —— 先检索。

- **系统地图**：[[概念解释器/SYSTEM_MAP]]
- **索引（自动生成，禁止手改）**：[[调度大脑记忆/索引]]
- **规则总入口**：[[通用规范/00-存档与内化]]

检索：

```powershell
python D:\Work\元智能\10_AI自成长引擎\技能库\local-knowledge-engine\scripts\query_evidence.py "关键词"
```

回写三步：查新（`git log` + 索引）→ 把结论写成条目（放 `调度大脑记忆/<type>/`，frontmatter 带 `type` 和 `updated`）→ 索引会自动重建，不用手动挂链。
