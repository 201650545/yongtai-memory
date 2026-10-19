---
name: reference-extbrain-dual-channel-task-routing
description: 外脑双通道（ChatGPT 镜像 GPT-6 Sol / Gemini 网页版 4 Argon）按三大榜单实测数据做的「任务类型 → 首选模型 → 是否并行双跑 → 档位」路由表，含双跑判定硬规则、档位等价表与并行落地的工程约束（2026-10-15 建）
metadata:
  node_type: memory
  type: reference
  created: 2026-10-15
  modified: 2026-10-15
type: reference
updated: 2026-10-19
---

# 外脑双通道任务路由表 · GPT-6 Sol vs Gemini 4 Argon

> **建立**：2026-10-15 ｜ 依据：LMArena(arena.ai) / AIHOT / AA 三榜实测取数
> **上位真源**：[[reference_全维度AI模型智力评分与推荐调度总则]]（本表是其 Gemini 与 GPT 席位的**外脑细分补充**，不推翻其任何总则）
> **消费方**：`gpt-mirror-extended-review` skill ｜ `gemini-web-review` skill
> **状态**：**方案稿，待郭老师拍板**（**9 个拍板点**见 §八，其中 P9 是"榜单 vs SSOT 对撞"，最先需要裁定；未拍板前不改任何路由真源与生产配置）

---

## 一、一句话结论

**两个通道不是"谁强用谁"，而是分工明确的两把不同的刀：**

- **要"人读着舒服 / 写得好看 / 交付件严谨 / 开放式困难判断" → Gemini 4 Argon**（LMArena **文本综合、文本编程、困难提示三项全部第 1**；AIHOT 专业办公第 1；同价位）
- **要"读我们的仓库 / 有标准答案的硬推理 / 长文精准召回 / 前端成品" → GPT-6 Sol**（AA-LCR 长文反超 6.9 分、Code Arena **HTML 模板第 1**；且**只有它能读 GitHub**）

**⇒ 结论：默认单跑 + 按任务分派；只有"结论要写进产品、且两榜分庭抗礼"的少数场合才双跑。双跑的瓶颈不是钱，是本机两条通道抢同一个 opencli 活跃标签（见 §7）。**

---

## 二、取数结果与可信度（先说数据是怎么来的）

| 榜单 | 取数状态 | 覆盖 | 数据时点 |
| :--- | :--- | :--- | :--- |
| **LMArena**（arena.ai） | ⚠️ **直连 403**（主路径与 `/leaderboard/text`、`/leaderboard/coding` **全部 Cloudflare IP 级拦截**；旧域名 `lmarena.ai` fetch failed）→ 全部走第三方镜像取回 | **5 个子榜**：Text Arena 综合 ／ Text Arena›**Coding** ／ **Hard Prompts 困难模式** ／ Code Arena›**WebDev** ／ Code Arena›**HTML 模板** ＋ Agent Arena（仅名次） | 主镜像 **10-08**，第二镜像 **10-13** |
| **AIHOT**（aihot.news） | ✅ 直连 200，7 个 URL 全通 | 综合 + 编程/科研/专业办公/知识问答 4 分类 + 35 项分项 | 页面自标 **10/15 20:06 更新** |
| **AA**（artificialanalysis.ai） | ✅ 本地每日快照（`reference_AA全球模型每日量化快照`） | 智力指数 + TPS + TTFT + 价格 | 系统 **2026-10-15 01:00** 同步 |
| 学术基准 SWE-bench / GPQA / MMLU-Pro | ❌ **本表未取到可比值**：总则表里有 GPT-6(Chat High) 的 62.5%/74.8%，但**没有 Argon**，且该行命名与现在的模型谱系已对不上 → 不足以支撑双模型比较，改用 AIHOT 分项（CyberBench / SciCode / Terminal-Bench / FrontierMath 等）替代 | — | — |

**LMArena 的镜像来源（多族独立，数值互证）**

| 镜像 | URL | 快照 | 提供 |
| :--- | :--- | :--- | :--- |
| **AITNT 对话模型榜** | https://www.aitntnews.com/arena/ ／ `/arena/code/` | **2026-10-08** | 20+ 子榜，含浮点分、**CI、票数**（最完整，本表主源） |
| 猫目 maomu | https://maomu.com/rank/models/arena-text ／ `/coding` | 2026-10-13 | 自述源自 Arena 官方公开数据集（CC BY 4.0） |
| llmrun.dev | https://llmrun.dev/benchmark/lmarena-text ／ `lmarena-webdev` | 至 2026-10 | 自述 Source = arena.ai |
| DataLearnerAI（旁证） | https://www.datalearner.com/leaderboards/external/text-generation | 2026-09-30 | 更旧，仅作参照 |
| BDM / AI Agent Store（旁证） | https://www.blogdumoderateur.com/meilleurs-modeles-piloter-agents-ia-octobre-2026/ | 2026-10-15 | 只给名次，无 Elo |

**四条交叉验证（说明数据可信）**：
1. GPT-6 Sol 的 Text Elo：AIHOT 报 **1458.3** ／ llmrun 报 **1455.9** ／ SWEN.AI 报 **1458** —— **三源吻合**。
2. Argon 的 Text Elo **1525**：AITNT(10-08)、猫目(10-13)、llmrun(1525.4)、DataLearnerAI、SWEN.AI —— **五源完全一致**。
3. GPT-6.1 Sol 的 Text Elo **1484 ± 9**：AITNT（4.5K 票）与 AI Agent Store 复述的 Arena 官方数字**一致**。
4. WebDev 三项：llmrun 1755.4 / 1688.2 / 1677.8 与 AITNT(10-08) 1755 / 1688 / 1678、猫目(10-13) 1760 / 1686 / 1678 —— **三源一致**。

**⚠️ 三条必须带上的口径警告**

1. **`Text Arena › Coding` 与 `Code Arena › WebDev` 是两个不同的榜，不可混用** —— 同一个 Argon 在两者是 **1562 vs 1678（差 116 Elo）**。本表**分列示，不合并**。
2. **同一指标跨快照会漂移**：GPT-6.1 Sol 的 WebDev 在 10-01 为 1759/#3 → 10-08 为 1755/#4 → 10-13 为 1760/#4。**引用必须带快照日期与榜单名。**
3. **档位不对等**：榜单上 Gemini 只有 **`4 Argon High`** 一档，而 GPT 侧多为 **`Max`**（比镜像站可达的最高档还高一级）。**本表所有"Argon 领先"的结论，都是 Argon 用更低档位赢下来的。**

---

## 三、三模型能力对照矩阵（本表的决策依据）

### 3.1 三榜横向对照

| 维度 | 榜单 | **Gemini 4 Argon (High)** | GPT-6.1 Sol | GPT-6 Sol |
| :--- | :--- | ---: | ---: | ---: |
| 人类盲选 · **文本综合** | LMArena Text | **🥇 #1 / 1525** | #21 / 1484 (Max) | #67 / 1456 (Max) |
| 人类盲选 · **文本榜内编程** | LMArena Text›Coding | **🥇 #1 / 1562** | #8 / 1545 (Max) | #37 / 1519 (Max) |
| 人类盲选 · **困难提示** | LMArena Hard Prompts | **🥇 #1 / 1551** | #20 / 1507 (Max) | 未取到（表被截断，不填） |
| 人类盲选 · **前端成品 WebDev** | LMArena Code Arena | #9 / 1678 | **#4 / 1755 (Max)** | #8 / 1688 (Max) |
| 人类盲选 · **HTML 模板** | LMArena Code Arena | #15 / 1642 | **🥇 #1 / 1797 (Max)** | #6 / 1686 (Max) |
| Agent 综合（**仅名次**） | BDM 转述 Agent Arena | #4 | **#2** | #7 |
| 综合智力指数 | AA | **52.6** | 51.8(Max)／50.2(**High**)／47.8(Med) | 未进 AA 前 25 |
| 综合（7 机构加权） | AIHOT | **73.0 / #2** | 68.9 / #8 | 65.6 / #12 |
| 编程 | AIHOT | **70.8 / #4** | 66.3 / #11 | 66.4 / #10 |
| 科研推理 | AIHOT | 74.3 / #4 | **75.5 / #3** | 69.0 / #11 |
| 专业办公 | AIHOT | **75.3 / #1** | 65.8 / #14 | 62.9 / #20 |
| 知识问答 | AIHOT | **73.3 / #4** | 72.0 / #7 | 64.2 / #16 |
| 长文精准召回 | AIHOT · AA-LCR | 55.1 | 60.8 | **62.0** |
| 事实问答 | AIHOT · SimpleQA | **88.8** | 85.9 | 70.4 |
| 上下文 | AA | 1.0M | 1.0M | 1.0M |
| 单价（输入/输出） | AA | $2 / $10 | $2 / $10 | — |
| 首字延迟 | AA | 未给 | **56.7s (High)** / 7.6s (Med) | — |
| 输出速度 | AA | 未给 | 56.4 tok/s (High) | — |

### 3.2 ★ 三个真实冲突（必须写进选型，不能藏）

**冲突一：编程到底谁强？—— 不是"两榜打架"，是"两种编程"。**

| 编程相关榜 | Argon | GPT-6.1 Sol | 谁赢 |
| :--- | ---: | ---: | :--- |
| AIHOT 编程（7 机构加权，含 CyberBench / SciCode 底层项） | **70.8 / #4** | 66.3 / #11 | **Argon** |
| LMArena **Text Arena›Coding**（人类盲选，通用编程） | **1562 / #1** | 1545 / #8 | **Argon** |
| LMArena **Hard Prompts**（人类盲选，困难提示） | **1551 / #1** | 1507 / #20 | **Argon** |
| LMArena **Code Arena›WebDev**（人类盲选，前端成品） | 1678 / #9 | **1755 / #4** | **GPT** |
| LMArena **Code Arena›HTML 模板** | 1642 / #15 | **1797 / #1** | **GPT（大胜）** |

**⇒ 五个编程相关榜里 Argon 赢三个、GPT 赢两个，且分界非常干净：**

- **通用编程 / 困难问题 / 底层算法 / 安全补丁 / 科学计算 → Argon**（AIHOT 分项 CyberBench Patch **62.9 对 52.6**、SciCode **64.9 对 54.7**，高整整一个档）
- **WebDev / HTML 模板 / 界面成品 → GPT-6.1 Sol**（HTML 子榜 **1797 第 1**，领先 Argon **155 Elo**；WebDev 领先 77 Elo）
- **⇒ 对本项目最有用的一条**：我们做**排版样张 HTML→PDF、看板页面**这类"前端成品"，人类盲选明确投给 **GPT**；而写**数据清洗脚本 / 正则 / 算法**，盲选与加权都投给 **Argon**。

**冲突二：Argon「专业办公第 1」却在长文召回上明显偏弱。**
- AIHOT 专业办公：Argon **75.3 第 1**（领先 GPT-6 Sol 12.4 分）
- AIHOT 分项 AA-LCR（长文精准检索）：Argon **55.1**，比 GPT-6.1 Sol 低 5.7、比 GPT-6 Sol 低 6.9

**⇒ 细分读法**：**"要产出高质量专业交付件"（写、组织、交付）→ Argon**；**"要从一大坨材料里准确定位到那一条"（长文召回）→ GPT 系**。两者不是一回事。

**冲突三：困难推理谁强？—— "有标准答案的科研题"和"开放式困难提问"也不是一回事。**

| 困难推理相关榜 | Argon | GPT-6.1 Sol | 谁赢 |
| :--- | ---: | ---: | :--- |
| AIHOT 科研推理（学术/科研类，有标准答案） | 74.3 / #4 | **75.5 / #3** | **GPT** |
| LMArena **Hard Prompts**（人类盲选的困难提问） | **1551 / #1** | 1507 / **#20** | **Argon（差 44 Elo、名次 1 对 20）** |

**⇒ 细分读法**：**有标准答案的科研 / 数学 / 学术题 → GPT-6.1 Sol**；**没有标准答案、靠人判断好坏的困难问题（方案权衡、架构取舍、疑难诊断）→ Argon**。
**本项目大量的"帮我判断这个方案行不行""这个排版问题到底出在哪"正属于后者 —— 按榜单该给 Argon，而不是习惯性丢给 GPT 镜像。**

### 3.3 ⚠️ 覆盖不齐，禁止直接比综合分

| 模型 | AIHOT 评测覆盖 | 已有成绩 | 缺什么 |
| :--- | ---: | ---: | :--- |
| Gemini 4 Argon | **82%** | 28 项 | LiveBench 编程综合／推理与数学／数据分析／语言与指令、Terminal-Bench Science·AA、τ³-Banking、**MLCR-AA** |
| GPT-6.1 Sol | **100%** | 35 项 | 仅缺 Vibe Code Bench 1–100 |
| GPT-6 Sol | **100%** | 34 项 | Vibe Code Bench 1–100、AA-Analyst Agent |

**⇒ Argon 的 73.0 是缺 7 项算出来的，GPT-6.1 Sol 的 68.9 是满覆盖算出来的。二者不可等价并列**（这与 `model-rank-recalibration` skill 的纪律同源：刻度/覆盖不同不得同表直接比）。
**可执行做法**：只比**双方都有成绩的项**；需要严格可比时，从 AIHOT 模型详情页取共同项重算。

---

## 四、★ 路由表（任务类型 → 首选模型 → 是否并行双跑 → 档位）

> 档位写法：GPT 侧为镜像站 `Chat` 标签三档 `Instant(0)/Medium(1)/High(2)`；Gemini 侧为 `Thinking level` `Low/Medium/High`。

| # | 任务类型 | 判定依据（榜单证据） | 首选模型 | 并行双跑 | 档位 |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1** | **读外部仓库 / 整包材料后评审**（贴 GitHub 链接式） | **硬能力差异**：ChatGPT 镜像实测读过 8 份 md + 5 张图；**Gemini 网页版实测读不了公开仓**（只回「无法访问外部链接」） | **GPT-6 Sol** | ❌ **否**（Argon 无此通路，跑必空转） | **High** |
| **2** | **顶层方案推演 / 产品定义 / 重大技术选型** | ⚠️ **SSOT 与榜单对撞**：AIHOT 综合差 4.1（灰色区）、AA 差 2.4 → 接近；**但按任务属性它属"开放式困难判断"，Hard Prompts 榜一边倒向 Argon（#1 vs #20）**；而**总则 SSOT 明令外脑顶层架构仲裁走 GPT-6 High** | **双跑**（冲突下的稳妥解）<br>先 GPT 后 Argon，**隔离提问** | ✅ **是**（**例外行**，不以分差判定） | **双 High** |
| **3** | **科研推理 / 数学 / 算法难题**（**有标准答案**） | AIHOT 科研推理：GPT-6.1 Sol **75.5 第 3** > Argon 74.3 第 4（仅差 1.2） | **GPT-6.1 Sol**（若 `6` 确认为 6.1，见 P1） | ⭕ 可选（只在高价值时） | **High** |
| **3b** | **开放式困难判断**（**无标准答案**：方案权衡、架构取舍、疑难诊断） | LMArena **Hard Prompts**：Argon **🥇#1 / 1551** vs GPT-6.1 Sol 1507 **#20**（差 44 Elo） | **Gemini 4 Argon** | ❌ 否 | **High** |
| **4** | **写作 / 文案 / 表达重写 / 文风打磨** | LMArena Text **断层第 1**：1525.4 vs 1483.7（领先 41.7 Elo，且 Argon 用的是 High 档） | **Gemini 4 Argon** | ❌ 否（一方压倒，双跑是浪费） | **High**（长文）／**Medium**（短稿） |
| **5** | **专业交付件 / 长公文 / 结构化严谨文档** | AIHOT 专业办公 **75.3 第 1**，领先 GPT-6 Sol 12.4 分 | **Gemini 4 Argon** | ❌ 否 | **High** |
| **6a** | **大材料事实定位 / 长文精准召回**（能贴文本） | AA-LCR：GPT-6 Sol 62.0 > GPT-6.1 Sol 60.8 > Argon 55.1；但**优先级更低**：本地 1M+ 上下文模型更便宜 | **不走外脑**（网关 `free-heavy`：MiMo 2.6 Pro / HY4 Preview） | ❌ 否 | — |
| **6b** | 同上，但材料只能靠**链接/仓库**给 | 同 #1 硬能力差异 | **GPT-6 Sol** | ❌ 否 | **High** |
| **7** | **事实核对 / 单点问答 / 短句改写 / 格式转换** | 不需要推理链；低档位即可，顶格是烧额度 | **就近通道**（哪个通道已开着就用哪个） | ❌ 否 | **低档**：GPT `Instant` ／ Argon `Low` |
| **8a** | **前端成品 / HTML 模板 / WebDev 界面**（若需外脑） | LMArena Code Arena：GPT-6.1 Sol **HTML 🥇#1 / 1797**、WebDev **#4 / 1755**；Argon 仅 #15 / #9 | **默认不走外脑**（本地 HTML/CSS 直做）→ 需外脑时 **GPT-6.1 Sol** | ❌ 否 | **High** |
| **8b** | **通用编程 / 脚本 / 正则 / 底层算法**（若需外脑） | Argon 双赢：AIHOT 编程 **70.8** ／ LMArena Text›Coding **🥇#1 / 1562** | **默认不走外脑**（网关 Gemini 3.8 Flash / GLM 5.3）→ 需外脑时 **Gemini 4 Argon** | ❌ 否 | **High** |
| **9** | **生图** | 只有 GPT 镜像有通路（PROLITE 卡 `image_gen` 额度约 8×） | **GPT 镜像**（PROLITE 账号） | ❌ 否 | 生图无推理档位 |
| **10** | **中文教研 / 考纲对齐 / 释义把关** | SSOT 总则已定席位：Qwen 3.8 Max（中文权威与学术考纲终审） | **不走外脑**（Qwen 3.8 Max） | ❌ 否 | — |
| **11** | **数据清洗 / 批处理 / 时间戳校验** | SSOT 已定席位：DeepSeek V4.1 Flash（高吞吐数据工程） | **不走外脑**（DeepSeek V4.1 Flash） | ❌ 否 | — |
| **12** | **独立第二意见 / 对抗性找错**（要"另一个脑子"而非"更好的答案"） | 价值来自**独立性**，不来自分数 | **双跑**，**必须先跑完 A、再问 B，且不把 A 的结论透露给 B** | ✅ **是** | **双 High** |
| **13** | **中文长文研读 + 结构化提炼**（材料可贴） | AIHOT 知识问答 73.3 vs 72.0（差 1.3）＋ Text 盲选 Argon 领先 | **Gemini 4 Argon** | ⭕ 可选 | **Medium**（常规）／**High**（要找错） |

---

## 五、双跑判定硬规则（不许逐案拍脑袋）

**同时满足以下 4 条 → 双跑；任一条不满足 → 单跑：**

1. **结论要进产品 / 进规范 / 对外发布**（能人工秒判的琐事不值得双跑）
2. **该维度上两边真的接近** —— 口径化：AIHOT 类百分制 **分差 ≤ 3**；Elo 类 **分差 ≤ 20**
   - **3–5 分 / 20–40 Elo 属灰色区**：高价值任务双跑，其余单跑
   - **≥ 5 分 / ≥ 40 Elo → 一侧压倒**，跑另一侧纯属浪费（**唯一例外见 #2**：那一行的冲突来自"榜单 vs SSOT"，不以分差判定）
3. **两侧都真能拿到材料**（任一侧有硬能力缺失 → 直接单跑，如 #1）
4. **额度允许**（GPT 侧是租号池 17 卡、有轮次与配额上限；Argon 是自家 AI Ultra 额度）

**污染隔离铁律（双跑的灵魂）**：
> 双跑的价值是"两个独立的判断"，不是"两个判断的平均"。
> **禁止**把 A 的结论、A 的措辞、A 的框架以任何形式透露给 B —— 那样 B 只会附和，双跑退化成单跑 + 一次昂贵的复读。
> 正确顺序：**A 独立作答 → 收完落盘 → B 独立作答 → 收完落盘 → 人（或第三方）做差异比对。**

---

## 六、档位等价表与额度口径

| 强度 | GPT 镜像 · `Chat` 标签 | Gemini 网页版 · `Thinking level` | 典型耗时（GPT 侧实测） |
| :--- | :--- | :--- | :--- |
| 低（不推理，直接答） | `Instant`（滑杆 0） | `Low` | 秒级 |
| 中（一定推演） | `Medium`（滑杆 1） | `Medium` | 10 秒 – 1 分钟 |
| 高（长链推理 + 自校验） | `High`（滑杆 2） | `High` | 1 – 5 分钟 |

- **两边都是"模型不动、只调档"**（已固化进两侧 skill）——这是统一策略：简单问题降档提速，**不降模型**。
- **⚠️ Argon 的档位代价无法量化**：AA 只给了 `Argon (High)` 一档，没有 Low/Medium 的智力指数。**GPT 侧可量化**：`High` 50.2 → `Medium` 47.8（**掉 2.4 分**），但首字延迟从 **56.7s 降到 7.6s（快 7.5 倍）**。⇒ **要快就降档，这个交换在 GPT 侧是有数据支撑的；Argon 侧只能凭体感。**
- **额度纪律**（两侧既有约束，原样继承，本表不作废）：GPT 侧 `Chat` 标签唯一可用、顶档默认 High、`Work` 标签禁用（接 Codex 无权限）、单窗口 ≤24 轮、**同一会话只能发一次**、卡住即刷新；PROLITE 卡（重活/超长推演/生图 + deep_research 5×）vs PLUS 卡（`file_upload` / `paste_text_to_file`）。Gemini 侧：SPA 需等挂载 40–60s、**发送只能点一次**。

---

## 七、★ 并行双跑的工程约束（不解决这条，"双跑"落不了地）

**现状**：两条通道**用的是同一个 opencli 会话**（`d5vtd5bg`），而该版本 opencli 的 **`eval` 跟随浏览器活跃标签**（v1.8.8 **不支持** `eval --tab`，定向要用 `tab select <pageId>`）。

**⇒ 后果：两个通道在同一会话内并发跑，会互相抢活跃标签** —— A 的回复查询会打在 B 的页面上，表现为读到空值、`no-composer`、或 CDP `Runtime.evaluate timed out`（镜像站 skill 已记录过被抢占导致长循环全崩的实例）。

**可执行的三种做法（按推荐度）：**

| 做法 | 说明 | 推荐度 |
| :--- | :--- | :---: |
| **① 串行错峰**（默认） | A 发问 → A 收完落盘 → `tab select` 切 B 发问 → B 收完落盘。总耗时 = 两者之和，但零风险 | ⭐⭐⭐ **默认用它** |
| **② 双 opencli 会话/profile** | 给一条通道独立会话，物理隔离活跃标签。**未实测**，需先验证 Gemini 侧登录态能否在新会话复用 | ⭐⭐ 值得一试 |
| **③ 真假并发** | 同会话内两页同时生成，收的时候串行读 | ⛔ **不推荐**，抢标签风险最高 |

**外加两条不可违反的通道纪律**（来自两侧 skill，双跑时更易踩）：
- 镜像站：**禁止后台任务轮询**、**禁止 fork 子 Agent**、必须**主会话前台监督**（黑箱轮询必留残次品）
- 两侧：**发送只能点一次**（指针序列不放 `'click'`，激活只留最后一句 `.click()`）—— 双跑时最容易"两边各点两次"

---

## 八、★ 拍板点与待核实（未拍板前不动任何路由真源）

| # | 拍板点 / 待核实 | 为什么重要 | 建议 |
| :---: | :--- | :--- | :--- |
| **P1** | **镜像站 Chat 里的 `6` 到底是 `GPT-6 Sol` 还是 `GPT-6.1 Sol`？** | 两者是**榜单上两个不同模型**：GPT-6 Sol 综合 **65.6**（09-22 上线）／GPT-6.1 Sol 综合 **68.9**（09-29 上线），**差 3.3 分**；而镜像站 Work 标签的历史模型清单里**两者同时存在**（`GPT-6.1 Sol` / `GPT-6 Astra` / `GPT-6 Sol` / `GPT-6 Luna`…），说明站方是能区分的。Chat 高级视图实测只看到 `6` / `GPT-5.6 Sol` / `GPT-5.5`，`6` 是单字符，**文案上无法判定** | **下次开镜像站时抓 `6` 的 aria-label / 副标题 / 详情文案落盘核实**；核实前本表 #3 的"科研第 3"结论**不得**直接挂到 `6` 上 |
| **P2** | **是否把 `Gemini 4 Argon` 补进 SSOT 总则的 Gemini 席位？** | 总则（10-11 定调）里 Gemini 席位**只写了 `Gemini 3.8 Flash`**，**没有 4 Argon**；而 4 Argon 现在是 LMArena Text **第 1**、AIHOT 综合 **第 2**、专业办公 **第 1**。总则已滞后 4 天 | 建议**新增** Argon 为"外脑第二通道"席位（不删 3.8 Flash，它仍是网关 `free-balanced` 的工程主力）；改动属 SSOT 变更，**等拍板** |
| **P3** | **双跑频次上限（额度预算）** | Argon 吃自家 AI Ultra 会员额度，GPT 吃租号池（会员至 **2026-10-29**、17 卡、单窗口 ≤24 轮）。双跑 = 两边各烧一轮 | 建议：**默认单跑；双跑只限"结论要进产品"的场合**，且事先说清这一轮要花两边额度 |
| **P4** | **Argon 评测覆盖只有 82%，是否接受它排第 2？** | 它缺 7 项，其中包含**编程综合、推理与数学、数据分析**——恰好是它可能不稳的区 | 建议：**接受名次，但比较时只用共同项**；对外引用分数时注明覆盖 |
| **P5** | **`reference_Gemini网页版能力与限制.md` 与 `gemini-web-review/SKILL.md` 内部自相矛盾** | 后者 §三 已写"三档思考 2026-10-15 实测打通"（给了 `set_thinking.js`），但 §六「待验证」里**还挂着**"★ 三档思考的控件路径（最优先）：没找到可编程入口"——**该待办未回勾**。照 §六 读会白重做一遍 | 建议：**改 §六 回勾**（纯文档修正，不改行为），我方可代改 |
| **P6** | **总则里的 LMSYS/学术基准行是否重取？** | 总则那行是 `GPT-6 (Chat High)`：Coding Elo ~1595 / Hard Prompts ~1430 / SWE-bench 62.5% / GPQA 74.8%，**既不含 Argon，命名也对不上现在的谱系**（且 arena.ai 直连已 403，得走镜像） | 建议：**下次顺手重取**；本表已用 AIHOT 分项替代，不阻塞 |
| **P7** | **arena.ai 长期走哪个镜像？** | arena.ai 主路径与子路径**全被 Cloudflare IP 级 403 拦死**，旧域名 `lmarena.ai` fetch failed —— 本表 LMArena 维度来自 **AITNT(10-08) + 猫目(10-13) + llmrun** 三族镜像，且数值互证（Argon 1525 **五源一致**） | 建议：**定 AITNT 为主镜像**（有 CI 与票数，20+ 子榜最完整），猫目做第二源；**引用一律带快照日期 + 榜单名**（§二口径警告 2） |
| **P8** | **本表落在哪、要不要在项目侧留指针？** | SSOT 规则：子项目**禁止私设模型筛选规则，只保留指针** | 建议：**留在记忆库 参考/**（已落此），English-Content-Factory 侧只在看板留一行指针，**不复制本表内容** |
| **P9** | **★ 顶层架构推演的席位该给谁？（榜单 vs SSOT 对撞）** | 按榜单：这属于"开放式困难判断"，**Hard Prompts 榜 Argon #1 / 1551，GPT-6.1 Sol 仅 #20 / 1507**（差 44 Elo、名次 1 对 20）→ 应走 Argon。按 SSOT：总则**明令**外脑顶层架构仲裁是 GPT-6 High 的独占席位。**两者直接冲突** | 本表**暂定双跑**（§四 #2）。**是否把该席位改判 Argon 单跑，属 SSOT 变更，必须郭老师裁定**；裁定前维持"GPT 为主 + 双跑" |

---

## 九、数据来源与时点

| 来源 | URL | 时点 | 备注 |
| :--- | :--- | :--- | :--- |
| **LMArena 主镜像 · AITNT** | https://www.aitntnews.com/arena/ ／ `/arena/code/` ／ `/arena/code/html/` | **2026-10-08** | 含浮点分 + CI + 票数，本表 LMArena 主源 |
| **LMArena 第二镜像 · 猫目** | https://maomu.com/rank/models/arena-text ／ `/coding` | 2026-10-13 | 源自 Arena 官方 CC BY 4.0 数据集 |
| LMArena 第三镜像 · llmrun | https://llmrun.dev/benchmark/lmarena-text ／ `lmarena-webdev` | 至 2026-10 | 自述 Source = arena.ai |
| LMArena 旁证 | DataLearnerAI（09-30）／ BDM（10-15，仅名次）／ SWEN.AI ／ AI Agent Store | 09-30 ~ 10-15 | 数值一致或只给名次 |
| AIHOT 综合榜 | https://aihot.news/leaderboard | 10/15 20:06 | 直连可用 |
| AIHOT 分类榜 | `/leaderboard/category/{coding,reasoning,professional,knowledge}` | 10/15 20:06 | 4 榜全部 200 |
| AIHOT 模型详情 | `/leaderboard/{gemini-4-argon,gpt-6-1-sol,gpt-6-sol}` | 10/15 20:06 | 35 项分项来源 |
| AA 量化快照 | https://artificialanalysis.ai/leaderboards/models | 2026-10-15 01:00 | 本地快照文件 |
| ❌ arena.ai 直连（含子路径） | https://arena.ai/leaderboard ／ `/text` ／ `/coding` | — | **全部 HTTP 403 Cloudflare IP 级拦截** |
| ❌ lmarena.ai（旧域名） | https://lmarena.ai/leaderboard ／ `/text` | — | **fetch failed**（网络层，非 403） |
| ❌ 其他失败源 | anotherwrapper（403）／ HuggingFace `lmarena-ai/leaderboard-dataset` viewer（两次网络失败）／ swfte.com（**2026-05 旧快照，未含目标模型 —— 列出以防误用**） | — | — |

---

## 十、关联

- 上位总则：[[reference_全维度AI模型智力评分与推荐调度总则]]
- AA 快照：[[reference_AA全球模型每日量化快照]]
- Gemini 通道能力边界：[[reference_Gemini网页版能力与限制]]
- 通道 skill：`D:\Work\元智能\10_AI自成长引擎\技能库\gpt-mirror-extended-review\` ｜ `...\gemini-web-review\`
- 方法纪律同源 skill：`...\_收存_宿主自产\model-rank-recalibration\SKILL.md`（刻度/覆盖变更须重校准，不得沿用旧阈值、不得混表比较）
- 项目侧（只留指针，不复制本表）：`English-Content-Factory\02_Projects\HN-ENGLISH-666\00_项目主控与看板\接手单_培优版主线.md` 遗留待办 #5
