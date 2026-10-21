---
name: 启迪家长通知 skill（qidi-parent-notify）
description: 给启迪培训机构家长催费 / 发课表通知 / 出出勤明细图时，用这个 skill：固定流程 + 出图脚本 + 示例图，不用每次重新想。数据只在本机飞书表，不进 git、不进记忆。
type: reference
created: 2026-10-19
updated: 2026-10-19
kind: reference
status: active
---

# 启迪 · 家长通知 skill（qidi-parent-notify）

> 真源：`D:\Work\元智能\10_AI自成长引擎\技能库\qidi-parent-notify\`
> 规范正文不复制：仍在 `D:\Work\启迪\00-项目规范\`，本 skill 只放执行索引与工具。

## 一句话

**催费 / 发课表不是每次重新想，是跑一条固定流水线。**
2026-10-19 前这套东西只有"规范 + 一堆一次性脚本"；现在收成一个 skill：任何 Agent 说
「催费 / 清理费用 / 课费通知 / 出勤明细 / 发课表 / 欠费名单」都能直接命中。

## skill 里有什么

| 件 | 作用 |
|---|---|
| `SKILL.md` | 流程 A 催费、流程 B 排课、红线、清理规则 |
| `scripts/gen_fee_notice.py` | 课费通知 SVG（套定稿句式：负数、不摆总额、🌹🌹🌹） |
| `scripts/gen_attendance_svg.py` | 出勤明细 SVG（只列通知同期；脚注三型） |
| `scripts/svg2png.py` | SVG → 2 倍 PNG（微信不预览 SVG，发送要双格式） |
| `examples/fee_notice.json` / `attendance.json` | 字段样例（全部虚构） |
| `assets/示例_课费通知.png` / `示例_出勤明细.png` | **要生成的就是这个样子** |

## 安全边界（2026-10-19 定）

- 家长姓名 / 电话 / 缴费明细只在本机飞书表与 `D:\Work\启迪`，**skill 与记忆都不写、不进 git**。
- `D:\Work\启迪` 已**整目录退出 git 跟踪**（`/启迪/` 进 .gitignore）；可复用部分只留在 skill。
- 出图产物 / 发送队列 / 排课通知 / 旧版存档 超 7 天由每日 01:00「存档清扫」自动删；
  **`03-通知定稿` 不删**（那是给家长的定稿母版，属文字真源）。
  ⚠️ 本地删了不等于 git 历史没了——所以启迪数据一开始就不进 git。

## 什么时候别用它

- 只问"启迪这个项目是什么" → 读 [[project_启迪]]；
- 要改规范 → 改 `D:\Work\启迪\00-项目规范\`（真源），skill 只跟随，不复制正文。
