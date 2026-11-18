---
name: project-skill-library-thirdparty
description: 元智能技能库的第三方收藏分区：7 类口径、索引入口、baoyu-comic 归档
metadata:
  node_type: memory
  type: project
  modified: 2026-11-11
type: project
updated: 2026-11-11
kind: fact
status: active
scope: skill_library_thirdparty
---

第三方 skill 在元智能技能库里有了独立分区：`D:\Work\元智能\10_AI自成长引擎\技能库\_第三方收藏\`（2026-11-11 立）。
**规则**：技能本体留在宿主原地（`~\.agents\skills` 实体 + `.claude` / `.trae-cn` Junction），本区**只放说明、不搬本体**；与自研母仓分区。

**7 类（按用途，不按厂商，上限 7）**：`10-出图与绘本` `20-文档与办公` `30-前端与设计` `40-检索与调研` `50-浏览器与自动化` `60-平台与生态对接` `70-写作与内容`。
普查口径：只盘 `.agents/skills` 实体目录（DSH 单一真相根）；实体第三方 82 条 = 已分类 76 + 待归类 6（`apple` / `data-science` / `devops` / `domain` / `gaming` 缺 description；`chinese-textbook-segmentation` 疑自制待归位）。

**入口**：`_第三方收藏\README.md`（索引 MOC）｜`_第三方收藏\_分类口径.md`（判据/字段/删净三处）｜技能库 `README.md` §二 第 8 节。

**首个重点收藏 baoyu-comic**（`_第三方收藏\10-出图与绘本\baoyu-comic\说明.md`）：Gitee 镜像 `liyansong/baoyu-skills` commit `ed628c0`，Apache-2.0（非 MIT）；实体 `~\.agents\skills\baoyu-comic`，34 文件；**只当分镜/prompt 生成器**，默认 `npx bun` 出图链路本机不通；默认画对白气泡、柔光画风，与"图内零文字"冲突，每次需覆盖。试跑产物 `D:\comic\amy-room\`。

**已知欠账**：82 条里仅 baoyu-comic、anatomy 有实读许可证据，其余来源/许可标"未核实"；技能库 git 本轮未提交。

本轮记录：`D:\Work\项目索引\rounds\2026-11-11.md`
