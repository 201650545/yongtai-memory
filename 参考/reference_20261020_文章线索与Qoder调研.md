---
name: reference-20261020-文章线索与Qoder调研
description: 2026-10-20 郭老师微信收藏的 3 篇公众号 + 3 篇小红书摘要；含 Qoder「DeepSeek-V4.1-Flash-1017 免费到 10/24」的本地实测结论（BUDDY/qoder 渠道当前不可用）。会过时，引用前重查。
type: reference
updated: 2026-10-20
---

# 2026-10-20 文章线索与 Qoder 调研

> 郭老师原话：「内容有点杂，尤其是关于小红书的笔记……看完这些你就知道，其实我有一个编排：在记忆项目中应该有一个待办事项，用来存着一些问题，让它收集起来以后，等我有时间了再去处理。」
> 对应想法池：[[项目/project_想法池]] IDEA-020（逆向工程）／IDEA-021（轻量化剪辑）／IDEA-022（外部 Skill 统一转译）。

## 一、公众号（3 篇）

### 1. 3Blue1Brown：现在正是学习数学的最佳时机（量子位）
- 链接：https://mp.weixin.qq.com/s/3YqIHo3LkLrbpVST4LBieQ
- 格兰特·桑德森（Grant Sanderson）观点：AI 在数学证明上全面超过人类，**对数学本身的价值与经费几乎没影响**，甚至可能迎来最好的时代。
- 数学研究的 5 个部分：证明定理、提出猜想、构建理论、寻找应用、沟通交流；「好数学家证定理，伟大数学家提猜想，最伟大数学家写定义」。
- 数学的三种价值：应用（可能隔几十年才兑现，如虚数→量子力学）、个人能力（可迁移到计算机/金融/密码学）、以及定义「什么值得研究」。
- 当机器能批量生成证明，**证明就变成数学的「原始数据」**；AI 能解题不妨碍人通过解题变强（「机器比你更会举铁，但你仍然值得去健身」）。
- 教育真正瓶颈不是解释清楚，而是**人到底想不想学**；现在进入数学领域，有机会参与定义「什么样的数学工作值得被认可」。

### 2. 清华副校长彭刚：在清华，AI 如何重塑本科课程体系和培养模式（知识分子）
- 链接：https://mp.weixin.qq.com/s/lEpRoVNBucXl0TViObTriQ
- 主线：「三位一体」（价值塑造、能力培养、知识传授）从 2014 提出到 2018 升为教育理念，2023 获国家级教学成果特等奖。
- 2025 起从「AI 赋能」转向「AI 重塑」：不是加工具，而是**课程体系、教学方式、评价机制的系统性重构**。
- 数据：AI 赋能课程从 8 门试点扩到 **493 门**；AI 通识课约 **250 门**（占本科课程 7%）；**24 个学科知识引擎**，对外发布 10 个；学堂在线转型。
- 人机协同考试实验（理论力学重修班）：裸考同分的学生，人机协同表现差异大；**知道何时用/不用 AI 是关键**；未来考核要「安全车道 + 开放车道」双轨。
- 当答案不再稀缺，教师更像**健身教练**：设目标、给反馈、纠偏鼓励，陪学生跨过「门槛概念」（threshold concept）。
- 「一院一策」：保（AI 替代不了的核心训练）、增（AI 协作能力）、优（课程结构）、减（低阶重复任务）；书院制已 15 个书院，2026 级 57.4% 新生进书院。

### 3. VisionHOPE：第一个会自己改学习规则的视觉骨干开源（机器之心）
- 链接：https://mp.weixin.qq.com/s/PvvlnewqHgNkZmTWoK-u7Q
- 明略科技 + 中科院自动化所；**首个以「自修改学习系统」为核心的通用视觉骨干**：一次前向计算里边读图像边更新学习规则（步长、记忆保留、特征关联）。
- 基于嵌套学习（Nested Learning）与 HOPE 自指机制；自修改核心计算量随 Token 数**线性增长**。
- 成绩：ImageNet-1K 上 VisionHOPE-S（52.9M 参数）Top-1 **85.2%**，比 VMamba-B（89M）高 1.3 个点；B 版 85.6%。
- HF 每日论文榜第 2、GitHub 近 1000 stars；代码/算子/预训练权重 **MIT 开源**。
- 值得关注点：视觉骨干决定多模态上层能拿到什么；「怎么学」的规则也开始由数据动态决定。

## 二、小红书（3 篇）

### 4. 数字生命卡兹克：人，刷到请打开你的 Agent
- 链接：https://xhslink.cn/o/80fjMHPXhuR
- 介绍 **agentusecases.ai**：收集/分类网上分享的 Agent 实际案例（结果 + 提示词），可把案例直接发给自己的 Agent，让它找适合的 case。
- 背景：Personal AI 产品多（Dots、Grok Bot、Muse），但很多人装上不知道拿 Agent 做什么。
- 评论里有价值线索：有人用 Agent 赚 Amazon 100 刀抵扣、有人做「小猫 Agent」、有人收集提示词库但没流量。

### 5. 诚哥 AI 新世界：AI 学习神器 Skill，看懂复杂技术架构
- 链接：https://xhslink.cn/o/9dd7bFMTdpa
- 推荐 **Help Me Understand** 技能：一键拆解论文与 AI 底层架构，输出图文讲解，主打「看不懂的复杂技术」。
- 评论区大量「求分享/求 GitHub 名字」——说明这类「解释型 Skill」需求真实存在；与我们的「概念解释器/SYSTEM_MAP」思路同类，但更偏论文/架构图解。

### 6. Qoder 官方：DeepSeek-V4.1-Flash-1017 免费用到 1024
- 链接：https://xhslink.cn/o/79bCac5OOMo
- 1024 预热活动：**即日起至 10 月 24 日**，DeepSeek-V4.1-Flash-1017 限时免费，**系数 0.1x → 0x，不扣 Credits**。
- **国际版和 CN 版都同步支持**；个人版免费用户、付费用户都能用。
- 上下文窗口支持 **1M**，思考强度可拉到最大；1024 还有更大的活动（未剧透）。

## 三、Qoder 白嫖可行性（本地实测，2026-10-20 00:3x 与 00:5x 两轮）

**结论：还没做成，也没往 BUDDY 渠道里加。**

- 我们 buddy2api 的 `qoder` 渠道只接了**国际版**：`https://api2-v2.qoder.sh/model/v1`；CN 版（`lingma.aliyun.com`）**未实现**。
- 第一轮 6 个候选 ID 全部 `400 invalid_model_error`：`deepseek-v4.1-flash-1017` / `deepseek-v4.1-flash` / `dfmodel` / `deepseek-v4-flash-1017` / `dmodel-flash` / `deepseek-v4.1-flash-1024`。
- 第二轮又试 14 个变体（`deepseek-v4-flash`、`dfmodel-1017`、`dflash`、`d-flash`、`DeepSeek-V4.1-Flash`、`ds4.1f`、`v4.1-flash`、`dmodel`…）：
  - `dmodel` → 200，但 `usage.raw_usage.model` 回传 **`oem-deepseek-v4-pro`**（即 DeepSeek-V4-Pro，官方 0.5× 档，**不是**免费的 1017 Flash）。
  - `deepseek-v4-flash` → 404 `provider_error: All models failed`，details 里是 **`Model not exist.`**。
  - 其余变体仍全部 `400 invalid_model_error`。
- 换 `User-Agent`（QoderApp/0.4.5、0.5.0、0.5.2、1.0.0、2.0.0）重试 `deepseek-v4.1-flash-1017`，**全部 400**——不是客户端版本头在拦。
- 模型目录端点（`/model/v1/models`、`/api/v2/model/list` 等）均 404；`api.qoder.com` 的目录端点返回 token 不认。
- 判断：国际版 API 目前**没对现有 token 开放这个模型 ID**；要么等 Qoder 客户端升级后从新客户端里取真实 ID，要么该模型只在 Qoder 产品内（IDE/App）可用、不走这个反代端点。
- 没动配置的原因：拿不到可用 ID 就往 `constants.py` 里加，只会让 `/v1/models` 多一个必然 400 的名字——比不加更坏。
- 下一步（等条件具备再做）：
  1. 升级 Qoder 客户端 → 在应用里**确认模型选择器出现 DeepSeek-V4.1-Flash-1017** → 重新导入账号；
  2. 从新版客户端缓存/日志里取真实请求 ID，或再探一轮；
  3. 拿到 ID 后改 `buddy2api/src/providers/qoder/constants.py` 的 `STATIC_MODELS / ALIASES / MODEL_CAPACITY`（上下文按 1M 声明，网关侧按 600K 上限策略收）；
  4. 重启 8787 网关，`/v1/models` 出现后再看账号轮换器是否自动读到（它读网关模型目录）。
- 时效提醒：免费到 **10 月 24 日**；之后要么恢复 0.1x 系数，要么等下一轮活动。

## 关联

- [[项目/project_想法池]]（IDEA-020/021/022）
- buddy2api：`D:\项目\ai-hub\buddy2api\src\providers\qoder\`
- 账号轮换器：`D:\tools\WorkBuddy-Account-Switcher\`（`FREE_PROVIDERS` 含 qoder）
