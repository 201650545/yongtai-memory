---
name: reference_aihot_模型动态日报
description: AIHOT 模型类动态日报（新品发布面），每日定时任务覆盖刷新；每条标注方向与是否已接入本机网关。
type: reference
updated: 2026-11-04
---
# AIHOT 模型动态日报（每日）

> **同步时间**：2026-11-04 11:52:40（每日定时任务自动刷新落盘）
> **数据来源**：https://aihot.news/api/v1/items?mode=all&category=ai-models&window=24h
> **口径**：这是**新品/新发布面**（不是能力榜，也不是热度榜）——「AI 圈最近发布了什么模型」。
> **接入判定**：`✅ 已接入` = 该型号已在本机网关（:8787）模型清单里；`🆕 未接入` = 有型号但网关里没有，
> 值得评估接入；`· 不适用` = 这条是框架/工具/生态类，不是可接入的对话模型。

## 一、模型动态（过去 24h）

- **OpenRouter 上线隐身模型 Crouton Alpha** ｜· 不适用（非具体模型） ｜方向 其他
  - 🥷 新隐身模型：Crouton Alpha 一款高效推理模型，专为规模化处理你的智能体全天重复的工作而打造。 - 免费使用 - 1M token 上下文 - 文本、图像、音频和视频输入 - 不使用数据训练
- **OpenAI 称 GPT-6 Astra 在一周内从零设计出可与 Codex 对话的硬件设备** ｜· 不适用（非具体模型） ｜方向 其他
  - OpenAI 表示其硬件团队把 GPT-6 Astra 用作副业项目，在一周内从零设计出一款让用户与 Codex 编码智能体对话的设备，Astra 负责外壳设计、PCB 布局与元件选型布线、固件和用户界面。
- **Mistral Large 4 上线 Open Math OS，1.05T 开源权重、1M 上下文** ｜🆕 未发现目录匹配 ｜方向 代码 ｜型号 Large 4
  - Mistral AI 宣布 Mistral Large 4 加入 Open Math OS 模型阵容，拥有 1.05T 开源权重和 1M 上下文窗口，今天起面向获批团队开放。Open Math OS 是一个让数学家与 AI 智能体在共享项目上协作的研究工作区，仅基于开源模型构建，供社区检查和运行，并由社区掌控自己的数据。
- **Arena 预告腾讯混元 Hy4 即将上线并回顾 Hy4 preview 表现** ｜✅ 目录型号级命中（API 可调用性未核验） ｜方向 代码 ｜网关模型 `hy4-preview`
  - Arena 预告腾讯混元 Hy4 即将推出，届时将在 Arena 排行榜上公布其表现。其引用的数据显示，Hy4 preview 上月以开源模型身份位列 Agent Arena 第 2（总榜第 10），在 14.5K+ 真实智能体会话中净提升 +5.4%，仅落后 Kimi K3 (Max) 的 +6.6%；成本约 $0.26 per median task，比
- **Sarvam AI 发布决策模型 Sarvam Prism 并开放权重** ｜· 不适用（非具体模型） ｜方向 其他
  - Sarvam AI 发布基于 Sarvam 105B 的 System One 决策模型 Sarvam Prism，在自测的 25 个决策模型中以 71.8 分、44 ms 响应（B200 GPU）成为 100 ms 内得分最高的模型。
- **Mistral Large 4 以开放权重发布并附技术报告** ｜🆕 未发现目录匹配 ｜方向 代码 ｜型号 Large 4
  - Mistral 团队成员 Pierre Stock 宣布 ML4（Mistral Large 4）正式开放权重，称其在代码智能体与网络安全方向具备前沿能力，且比三周前的 Preview 版本更高效、更紧凑。技术报告讲述其研发过程：https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B/blob/mai
- **商汤发布 SenseNova 6.8 Flash，主打办公智能与动态设计** ｜🔶 目录家族级命中，变体待核 ｜方向 代码 ｜网关模型 `raccoon/sn-sensenova-6-8-flash`
  - 商汤推出 SenseNova 6.8 Flash，主打可靠工作流与精美设计。该模型具备长期记忆与主动交互的办公智能，可记住用户需求并持续推进任务，同时支持动画 PPT、动态海报、交互网站及可编辑 Blender 3D 项目。用户可在 SenseNova Token 计划中免费试用，每 5 小时获 1,500 次免费 API 请求。
- **商汤发布日日新 SenseNova 6.8 Flash 正式版，支持动态 PPT 与 Blender 3D 创作** ｜🔶 目录家族级命中，变体待核 ｜方向 其他 ｜网关模型 `raccoon/sn-sensenova-6-8-flash`
  - 商汤科技 11 月 2 日晚发布日日新 SenseNova 6.8 Flash 正式版，重点升级办公协作与设计生成能力，支持长期记忆、跨会话任务协作。

## 二、今日热议（热度面，交叉参考）

- MIT 称 GPT-6 Astra 可直接改写模型权重
- Google将引导学习引入Search和Classroom，K-12学生AI工具默认关闭
- 苹果 Apple 智能随 iOS 27.3 入华，接入阿里千问
- Anthropic 递交 S-1 拟以 ANT 登陆纳斯达克
- Anthropic 开源 FlashProve 可验证推理原型
- 马斯克承认Grok Bot成本高于收入并下调限额
- Claude Code 产品负责人 Cat Wu 宣布离开 Anthropic
- OpenAI 称 ChatGPT 搜索量达 Google 两成、周活 12 亿
- AMD发布三季度财报，预计2027年营收增长超80%
- OpenAI新设国家安全顾问，Driscoll出任

