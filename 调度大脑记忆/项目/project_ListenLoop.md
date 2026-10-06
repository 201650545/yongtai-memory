---
name: project-ListenLoop
description: ListenLoop（AI 精听训练器）＝面向严肃外语学习者的逐句精听＋抗遗忘学习系统。三处真源分开：文档 D:\Work\AI精听训练器、代码 D:\listenloop（Flutter）、发布仓 D:\Work\gh-sync\listenloop-project。它自带 Agent 快速通道（04_Agent机器索引）。联合点：模型面走网关 :3100，本地跑 sherpa-onnx/whisper 推理，曾把"网关部署到墙外云服务器"列为选项 E。**ASR 四档：端侧已于 2026-10-01 18:10/19:10 被另一 Agent 落地（未提交），PC 脚本与验收判据未做；权威工单在 `04_Agent机器索引_快速通道\TICKET-20261001-ASR四档切换.md`，本条目只是指针**。🔴 落地后暴露的真问题＝中文手机档 `paraformer-zh-small` **无 timestamp 头**（实测 0/29），引擎按总时长等距插值造时间戳、测试保的就是这个兜底 ⇒ 中文逐词时间是假的、分句只剩字数上限一条线索，**待郭老师拍**（详见 [[调度大脑记忆/教训/audit_两仓记录与实际冲突_20261001]] A1/A2/E1）
metadata:
  node_type: memory
  type: 项目
  created: 2026-09-30
  modified: 2026-10-01
---

# ListenLoop（AI 精听训练器）

**是什么**：README 自述——"面向严肃外语学习者的 **AI 智能管家驱动的影视级逐句精听与抗遗忘学习系统（Learning Runtime）**"。仓库按商业工程级知识管理组织，**双轨导航**：给人看的驾驶舱 ＋ 给 Agent 用的机器索引。

## 三处真源（分得很开，别只记一个）

| 用途 | 路径 |
|---|---|
| 文档／知识库真源 | `D:\Work\AI精听训练器\`（`00_项目驾驶舱_可视化中心`、`01_商业与战略规划`、`02_工程架构与系统设计`、`03_研发日志与历史归档`） |
| **代码真源** | `D:\listenloop\`（Flutter：`android/`、`.dart_tool`、`analysis_options.yaml`；内有 `HANDOFF-Milestone-1B.md`、`HANDOVER-20260921-listenloop.md`） |
| GitHub 发布仓 | `D:\Work\gh-sync\listenloop-project` ＋ 评审/调研仓 `D:\Work\gh-sync\listenloop-curated`（`github.com/201650545/listenloop-curated`，已公开） |

**⚠️ 目录名坑**：`D:\Work\gh-sync` 这个名字与内容不符——它实际是 ListenLoop 的发布台＋GPT 问诊工作台。改名要郭老师点头（有 9 处入向引用）。

## Agent 进门先读这两份（项目自己已经建好了）

- `D:\Work\AI精听训练器\04_Agent机器索引_快速通道\INDEX.md` —— 明写"本文件专供 AI / Agent 快速导航与状态对齐"，分「用户驾驶舱短链接」（汇报用）与「源码与契约短链接」（改码用）
- 同目录 `AGENT_MANIFEST.json`

⇒ 本项目**不需要郭老师再铺垫上下文**；别的 Agent 直接从这两份进。

## 联合点（它和别的project怎么连）

1. **模型面依赖 API 转发网关 `:3100`** —— 它是 api-gateway 那 9 个依赖方之一（见 [[调度大脑记忆/项目/project_relation_graph]]）。
2. **推理在本地**：`AI精听训练器\dist\_models\sherpa-onnx-whisper-*` 是本地 ASR 模型件，**不是云算力**；按 09-29 架构，重活本来就归本地 PC。
3. **上云路线已被写明但没做**：`02_工程架构与系统设计\04_AI伴学与Anki记忆卡优化设计.md:221` 的选项 **E. 网关部署到墙外云服务器**（原话评注："最省心，手机随时可用"）——部署位就是阿里 99 ECS，见 [[调度大脑记忆/参考/reference_云服务器底座与跨项目联合点]]。**⚠️ 这条只是文档里的候选方案，没有开工证据，别当已部署。**
5. **交接包挂着没接**：`D:\Work\gh-sync\HANDOFF-2026-09-29.md`（09-30 挂号，尚未被任何 Agent 读验接手）。

## ASR 八槽位升级（2026-10-05 郭老师最新裁定；PC 4 档 ＋ 手机 4 档）

**权威选型清单见 [[调度大脑记忆/参考/reference_本机本地模型清单]]**。
- **2026-10-05 升级实测定案**：郭老师裁定“电脑 4 个、手机 4 个（双端各自具备中/英高精与快速）”，全部 8 槽位已在 PC 实测通过。
- **✅ 彻底解决手机端时间戳卡点**：
  - 此前卡在第三方 `paraformer-zh-small` 无时间戳头；
  - 2026-10-05 实测解决方案：**中文手机快速档正式锁定 `sherpa-onnx-zipformer-ctc-small-zh-int8-2025-07-16`（60MB，RTF 0.0170，31/31 字级时间戳完全有效）**；
  - **中文手机高精档锁定 `sherpa-onnx-paraformer-zh-2023-09-14`（224MB 达摩院官方件，29/29 字级时间戳完整，高配机专用）**。
- **英文两档均已就绪**：PC 高精 `parakeet-0.6b` (460MB, WER 1.5%, 自带标点大小写)；手机与快速 `parakeet-110m` (99.5MB, WER 1.5%, 时间戳完整)。

## 关键词（拿去定位）

`ListenLoop` `AI精听训练器` `精听` `单句循环` `抗遗忘` `Learning Runtime` `sherpa-onnx` `whisper` `listenloop-curated` `gh-sync` `驾驶舱`

**How to apply:** 汇报进展给郭老师 → 用驾驶舱短链接；改代码 → 去 `D:\listenloop`。判"做到哪了"只认 `04_Agent机器索引_快速通道\INDEX.md`（2026-10-01 修：原少写 `_快速通道` 后缀＝死路径）与驾驶舱现值，**别引用本条记忆**（本项目推进快，记忆会先过时）。相关：[[调度大脑记忆/流程/workflow_work库冷启动接手序]]、[[调度大脑记忆/项目/project_ai_gateway]]
