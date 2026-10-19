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

### 补充：国内版（CN）能不能也接进 BUDDY（2026-10-20 01:0x 实测）

- 本机同时装了国际版（`D:\Qoder`，0.4.1／缓存里已有 0.4.3 更新）和国内版（`C:\Users\郭永涛\AppData\Local\Programs\Qoder CN`，0.4.1）。
- 两个客户端的 auth 都能用同一套 DPAPI+AESGCM 解出来：国际版 `token=dt-…`（user 郭永涛）、CN 版 `token=dt-…`（user `aliyun-…`），token 有效期都到 **2026-10-28**。
- 从 CN 客户端 `qoder-worker-runtime.obf.mjs` 里挖出真实端点映射（`Ji?CN:intl`）：
  - 模型服务：CN = `gateway.qoder.com.cn`（对应国际版 `api2.qoder.sh`）
  - 模型对话路径：国际版 `/model/v1/chat/completions`；CN 实际走 **`/algo/api/v2/service/pro/sse/agent_chat_generation`**（SSE）
  - 另有 `openapi.qoder.com.cn` / `qoder.com.cn` 等。
- 用 CN token 实测：
  - `https://gateway.qoder.com.cn/algo/api/v2/service/pro/sse/agent_chat_generation` → HTTP 200，但 body 是 `{"code":"101","message":"Signature invalid"}`（403）⇒ **CN 网关要求请求签名**，不是简单 Bearer。
  - `https://gateway.qoder.com.cn/model/v1/chat/completions` → 503/404，说明 CN 不走这条路径。
- 结论：**CN 版暂时接不进 BUDDY**——缺的不是 token，而是请求签名算法（CN 客户端内部生成），要单独逆向；国际版仍按上文“ID 不被接受”卡住。
- 版本：CN 最新 0.4.8（本机 0.4.1），国际版最新 0.4.8（本机 0.4.1/0.4.3）；两版安装包可从 `https://download.qoder.com.cn/qoder-app/releases/0.4.8/` 取。

### 更新与更新后复测（2026-10-20 01:1x）

- 已把两个客户端都升到 **0.4.8**：国际版 `D:\Qoder`（原 0.4.1→0.4.8）、国内版 `D:\Qoder CN`（原 `%LocalAppData%\Programs\Qoder CN` 0.4.1→新装 0.4.8）。安装包 sha256 校验通过，静默安装 exit 0。
- 更新后重新解出国际版 token 再测：`deepseek-v4.1-flash-1017` / `deepseek-v4.1-flash` 仍 **400 invalid_model_error**；`dmodel` 仍回 `oem-deepseek-v4-pro`；`qwen-flash` 正常。
  ⇒ **不是客户端版本问题，是服务端对现有 token 没开放这个模型 ID**。
- 国内版仍是签名问题（`Signature invalid`），未接。
- 因此 BUDDY 里**没有**加国际版/国内版的 1017 模型；现有 qoder 渠道仍是 `qwen3.8-flash`（+ 映射 `dmodel`→V4-Pro）。

### 关键补充：国际版那个模型在客户端里叫 `dfmodel`（2026-10-20 01:2x）

- 郭老师确认：国际版模型选择器里显示 **「DeepSeek V4 flash」**，备注 **「DeepSeek V4.1 flash 1017」**。
- 从 Qoder 本地 `main.sqlite` 的 `chat_sessions.model` 列查到的真实 key 是 **`dfmodel`**（历史会话用过；另有 `qfmodel`、`qmodel_38max`）。动态文案 `dynamic-text/qoder.v1.json` 里 `model.dfmodel.label` = "DeepSeek-V4-Flash"，描述仍写 0731（缓存旧）。
- 但用我们账号 token 直连 `api2-v2.qoder.sh/model/v1/chat/completions`：`dfmodel` → **400 Unsupported model**；`deepseek-v4-flash` → 404 `Model not exist`；只有 `dmodel`（→ V4-Pro）和 `qwen-flash` 能通。
- 结论：客户端能看到的「DeepSeek V4.1 flash 1017」走的是客户端特有的一条路径（可能带客户端指纹/目录 token），我们用裸 token 复现不了，所以仍加不进 BUDDY。

### 千问办公（QwenWork）能不能加

- **BUDDY 里代码已经有了**：`providers/qwenwork/` 完整实现了 QwenWork / 千问办公协议（`gateway.qwenwork.cn`、`/algo/api/v2/service/pro/sse/agent_chat_generation`、RSA 签名、`qwork-auto/advanced/ultimate` 等模型）。
- 但本机**没装/没登录千问办公**：`%APPDATA%\QwenWorkCN` 不存在，也没有相关可执行文件；DB 里 providers 只有 lobster/loomy/qoder/raccoon/traework/workbuddy，**没有 qwenwork 账号**。
- 所以现在加不了；一旦装上并登录，用 provider 自带的 `store.discover()/import` 导入账号即可出现在渠道里，工作量约几分钟。

## 关联

- [[项目/project_想法池]]（IDEA-020/021/022）
- buddy2api：`D:\项目\ai-hub\buddy2api\src\providers\qoder\`
- 账号轮换器：`D:\tools\WorkBuddy-Account-Switcher\`（`FREE_PROVIDERS` 含 qoder）


### 抓包实证（2026-10-20 01:5x，mitmproxy，已恢复代理并删证书）

- 抓到 Qoder 模型目录响应（openapi.qoder.sh/api/v1/remote/environments 的 vailable_models）：
  - **dfmodel → displayName「DeepSeek-Flash」，description「Reasoning · Vision · New · 0x Credit」，priceFactor=0**（这就是郭老师看到的「DeepSeek V4 flash / V4.1 flash 1017」）
  - qfmodel → Qwen3.8-Flash，**0x Credit**；dmodel → V4-Pro，0.5x；qmodel_38max 0.2x
  - 说明：免费是**客户端权益**，模型 ID 就是 dfmodel。
- 抓到 job token 流程：POST https://openapi.qoder.sh/api/v1/me/jobToken → 返回 jt-…，有效期 24h。
- 但拿 job token + 仿客户端头（X-Qoder-Model / X-RequestSet-ID / X-Client-Timestamp / X-Machine-*）去打 pi2-v2.qoder.sh/model/v1/chat/completions：
  - dfmodel → 400 Unsupported model；qfmodel → 400；deepseek-v4-flash → 404 Model not exist；dmodel → 200（V4-Pro）
- 模型调用由 worker 进程**绕过系统代理直连**（HTTPDNS），抓不到实际请求；判断免费档只在客户端 agent 管线内可用，公共 API 不开放。
- 结论不变：**BUDDY 加不了 Qoder 这条**；想要 V4.1 Flash 白嫖，用已有免费渠道（loomy / raccoon / traework）。

### 千问办公（QwenWork）接入进度（2026-10-20 02:0x）

- 已装千问办公 1.3.2（D:\QwenWorkCN），郭老师登录成功。
- BUDDY 开 qwenwork 通道 + CB_GATEWAY_AUTO_IMPORT=1 后账号自动导入，/v1/models 出现 qwenwork/pro、qwenwork/flash、qwenwork/qwen3.8-max-preview。
- 但调用 500：providers.qwenwork.encode.EncodeError: attempted to take ownership of Rust value while it was borrowed。
- 原因：provider 按千问办公 **1.0.4** 协议写（官方 WASM prepareInferRequest），客户端已 1.3.2，WASM 接口变了。要升级 provider 的 encode 层才能用。

## 六、处置决定（2026-10-20 早）

- 郭老师决定：Qoder 的 1017 既然公共 API 用不了，**把 Qoder 从 BUDDY 选定模型中移除**。
- 已执行：`/admin/selected-models` 删除 `qoder` 渠道（原唯一暴露 `qoder/qwen3.8-flash`），接口返回 `dropped: ["qoder"]`；`/v1/models` 已无 `qoder/*`。
- provider 代码与账号保留（不删），日后官方开放 API 或模型 ID 可用时可直接重新加入 selected_models。

### 移除执行记录（2026-10-20 07:4x）

- `selected_models`：删除 `qoder` 渠道（原 `qoder/qwen3.8-flash`），接口返回 `dropped:["qoder"]`。
- `buddy2api/scripts/gateway_run.bat`：启动 provider 列表去掉 `qoder`（commit `ffd562c`）。
- 8787 网关重启后 `/v1/models` 已无 `qoder/*`（129 个模型，渠道：loomy/raccoon/traework/workbuddy/workbuddy-intl）。
- DSH profile 已用 `sync_dsh_profile.py` 重写（18 个模型），**需重启 DeepSeek Harness 才生效**；备份 `cordis.patch.yml.bak-20261020_074445`。
- 自检仍报 4 处漂移：`lobster/deepseek-flash`、`lobster/qwen3.8-omni-flash` 已选定但网关无此渠道（历史遗留，非本次操作引入）；要不要一并清理由郭老师定。
- qoder provider 代码与账号保留，日后可用时重新加回 selected_models 即可。

### Lobster（有道龙虾）处置（2026-10-20 07:4x）

- 渠道本身没坏：provider 代码齐全、账号 active（id=11）、上游额度查询 OK，剩余 **1343.37 积分**（标准订阅 0；新订阅活动 843.37，10-25 到期；新用户赠送 300，11-01 到期；每日登录 100+100）。
- `/v1/models` 里没有它，原因不是故障：`gateway_run.bat` 的 `CB_GATEWAY_PROVIDERS` 没列 `lobster`，启动时就没加载，于是选定模型里的 `lobster/*` 成了幽灵条目。
- 「额度消耗快」的实际口径：lobster 扣的是积分，deepseek-flash 默认 thinking=high 单次消耗偏高；活动积分 10-25 到期，所以体感快。
- 郭老师判断不好用，已从 `selected_models` 删除 `lobster`；DSH profile 重新同步后自检通过（0 漂移），备份 `cordis.patch.yml.bak-20261020_074701`。账号与 provider 保留，想恢复时把 `lobster` 加回启动列表与 selected_models 即可。

### Lobster 重新启用与调优（2026-10-20 07:5x）

- 郭老师定：Lobster 只用 `deepseek-flash` 一个模型，思考档默认调到 low。
- 实测：上游没有真正的 low 档——`low` 的 reasoning 长度与 `high` 相当，只有 `off` 真正为 0；因此把 DSH 的 `low/minimal` 映射到上游 `off`，默认档也设为 `off`（客户端不传档位时显式带上，避免上游默认 high）。
- 已改 `providers/lobster/constants.py` + `chat.py`；`gateway_run.bat` 重新启用 lobster；`selected_models` 只选 `lobster/deepseek-flash`；DSH profile 已同步、自检 0 漂移。commit `27f35d1`。
- 每日领取：之前没做。已把 LobsterAI 加入 `daily_autoclaim.py`（新 App 条目，启动客户端后用积分差值判断是否到账），计划任务 `Buddy2API_DailyAutoClaim` 每天 01:25 跑。commit `bcbf303` + `fix` 提交。
- 未验证项：LobsterAI 启动后是否确实触发每日登录奖励（明早任务跑完看日志 `daily_autoclaim.log` 里「积分 1343→1443」这类变化）。
