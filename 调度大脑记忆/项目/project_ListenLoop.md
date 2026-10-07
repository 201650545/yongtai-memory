---
name: project-ListenLoop
description: ListenLoop（AI 精听训练器）＝面向严肃外语学习者的逐句精听＋抗遗忘学习系统。三处真源分开：文档 D:\Work\AI精听训练器、代码 D:\listenloop（Flutter）、发布仓 D:\Work\gh-sync\listenloop-project。它自带 Agent 快速通道（04_Agent机器索引）。联合点：模型面走网关 :3100，本地跑 sherpa-onnx/whisper 推理，曾把"网关部署到墙外云服务器"列为选项 E。**ASR 四档：端侧已于 2026-10-01 18:10/19:10 被另一 Agent 落地（未提交），PC 脚本与验收判据未做；权威工单在 `04_Agent机器索引_快速通道\TICKET-20261001-ASR四档切换.md`，本条目只是指针**。🔴 落地后暴露的真问题＝中文手机档 `paraformer-zh-small` **无 timestamp 头**（实测 0/29），引擎按总时长等距插值造时间戳、测试保的就是这个兜底 ⇒ 中文逐词时间是假的、分句只剩字数上限一条线索，**待郭老师拍**（详见 [[调度大脑记忆/教训/audit_两仓记录与实际冲突_20261001]] A1/A2/E1）
metadata:
  node_type: memory
  type: 项目
  created: 2026-09-30
  modified: 2026-10-06
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

## ASR 定档（P-4 裁定，2026-10-07 最新口径；PC 4 档 ＋ 手机 2 档＝6 槽位/5 物理模型）

**权威选型清单见 [[调度大脑记忆/参考/reference_本机本地模型清单]]**。
- **形态**：PC 4 档（中/英高精＋快速）；手机**只做 2 档快速**（中/英快速）；英文快速 PC 与手机**共用同一个权重** ⇒ 全盘 5 个物理模型。
- **P-4 分工铁律**：PC 出 tokens 毫秒字戳、标点规整与初读/熟读双轴课包；手机端只负责丝滑播放与轻量跟读。
- **红线**：废多语言通才 Whisper；必须过时间戳探针（无字级时间戳一票否决）；手机端总权重 ~160MB。
- 手机中文快速实测锁定 `zipformer-ctc-small-zh-int8-2025-07-16`（60MB，31/31）；PC 中文快速 `zipformer-ctc-zh-int8-2025-07-03`(180MB，31/31）;PC 中文高精 `paraformer-zh-2023-09-14`(224MB，29/29）;PC 英文高精 `parakeet-tdt-0.6b`(460MB，48/48，WER 1.5%);英文快速 `parakeet_tdt_ctc_110m`(99.5MB，46/48? 实为 46/46)，PC 与手机共用。
- **⚠️ 代码同步（2026-10-07 已做）**：`AsrTier.zhSmall` 已从无时间戳的 `paraformer-zh-small` 切到 `zipformer_ctc` 小模型，引擎新增 `zipformer_ctc` 分支。

## 2026-10-06 最新进展（语文全景导图与教材级排版系统）

- **语文 1~9 年级思维导图导航落地**：彻底取代繁复下拉与跳转，书架页以思维导图直观铺开所选年级全部单元与课文篇目，支持双指缩放/平移，课文卡片直通精听，支持年级记忆持久化与“锁定我的年级”。
- **教材级拼音排版系统（自适应混合对齐）**：
  - 行行相间排版（拼音行与汉字行严格交替）；
  - **首创混合对齐**：长拼音/后鼻音（$\ge 4$ 字母）与汉字左边缘齐平对齐，短拼音（$< 4$ 字母）中轴垂直居中对齐；
  - 拼音字体跟随汉字设置联动（宋体 `SongTi` 原生字形支持），顶部声调预留安全区杜绝遮挡；
  - 连续长拼音防撞留白算法（6px 动态拉大至 11px）。
- **真机联调验证**：ADB 物理机 `bf6ef967` 全流程安装拉起通过。
- **角色交接**：当前阶段工程落地完成，转交规划型 Agent 进行全景 WBS、资源科学调配与多轨执行规划。

## 关键词（拿去定位）

`ListenLoop` `AI精听训练器` `精听` `单句循环` `抗遗忘` `Learning Runtime` `sherpa-onnx` `whisper` `listenloop-curated` `gh-sync` `驾驶舱` `思维导图` `自适应混合对齐`

**How to apply:** 汇报进展给郭老师 → 用驾驶舱短链接；改代码 → 去 `D:\listenloop`。判"做到哪了"只认 `04_Agent机器索引_快速通道\INDEX.md` 与驾驶舱现值，**别引用本条记忆**（本项目推进快，记忆会先过时）。相关：[[调度大脑记忆/流程/workflow_work库冷启动接手序]]、[[调度大脑记忆/项目/project_ai_gateway]]
