---
name: feedback-chinese-naming
description: 所有项目/子项目的人看层命名一律用中文；GitHub slug 平台限制不能中文走英文/pinyin；代码目录保留英文路径但在中文文档注中文名
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
  modified: 2026-09-03T15:39:32.605Z
---

用户（非英语母语者）明确要求：**所有项目一律用中文命名，包括子项目（文件、文件夹）；所有仓库项目命名都改为中文**。起因是中英混名（如 `resource-ops` + `00_中央平台` 并存、`docs/设计`、仓库 slug 纯英文）让他混乱难懂。

**Why:** 读起来费劲、记忆成本高；他看得懂中文、看不懂随意英文 slug。
**How to apply:**（2026-09-03 拍板 =「知识库层全中文（推荐）」档）
- **人看的层（笔记/文档/运行手册/看板/项目显示名）→ 全中文师名**。新建或重命名知识库/文档文件一律中文。
- **GitHub 仓库名受平台限制只能是 ASCII slug，做不了纯中文**。现实解 = 本地目录/Obsidian 全中文，GitHub slug 用英文或 **pinyin**（如 ai-platform→aipingtai）作 URL 把手；中文名登记在文档里（如 projects.yaml）。
- **代码目录/被 CI/import 引用的路径（resource-ops/integrations/agent/config/tests/docs/）保留英文路径**——它们是给机器跑的，不是给人看的；但在中文文档里注明中文名方便对照。
- 不主动把「代码目录也改中文」（除非用户再拍板，那档高风险会 break CI/Pages/import，需专门排期+回归）。

关联 [[feedback_decision_only_reporting]] [[project_scheduler_role_matrix]] [[project_ai_gateway]]。