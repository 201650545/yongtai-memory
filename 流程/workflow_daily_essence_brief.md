---
name: workflow_daily_essence_brief
description: 每日本质精选流水线——AIHOT 候选 → 自有网关免费模型提炼（≤3 条·本质+用途）→ 飞书汇报；清单落 runtime 不进记忆仓
type: workflow
updated: 2026-10-21
---

# 每日本质精选（≤3 条 · 飞书汇报）

> 2026-10-21 郭老师定：「AI 根据我跟它对话日常积累的喜好，来帮我筛选每日简报中有哪些好的内容，
> **最多只选 3 点**跟我说。然后我来决定我们这个系统要不要更新，或者要加哪些创意点。」

## 一、三层分工（别混层）

| 层 | 干什么 | 产物落在哪 | 人看吗 |
| :-- | :-- | :-- | :-- |
| ① 候选层 | `aihot_hot_snapshot.py` 拉 AIHOT 今日动态（ai-models ＋ hot） | 冷 JSON ＋ 忆库日报 | **不看**（机器读的事实层） |
| ② **提炼层** | `extract_daily_insights.py`：用**他自己 :8787 网关的免费模型**，把 30+ 条压成 ≤3 条观点 | 飞书正文 ＋ runtime 清单 | **看**（这就是汇报） |
| ③ 决策层 | 他决定"系统要不要更新 / 加什么创意点" | 他同意的结论才由人写进记忆仓 | 他说了算 |

## 二、跑起来是什么样（2026-10-21 11:08 首跑实测）

- 候选 34 条 → 模型 `workbuddy/minimax-m3.1-flash` → **3 条，696 字**
- 飞书推送成功（**注意：是「郭樂's AI Assistant」这个 p2p 单聊，不是群**）
- 选出来的三条**都落到了他的系统**：
  1. 文档解析 → 记忆仓入库链路（带版面坐标的 Markdown/JSON，给 local-knowledge-engine 用）
  2. 可编辑图层设计模型 → 小红书图文产线（改标题/配色不必整张重做）
  3. 实时语音可控部署 → `:3100` 的 voice-asr/tts/chat/realtime 候选池 ＋ 句读跟读拆分

## 二·补 · 汇报形态的三个版本（2026-10-21 上午一路升级）

| 形态 | 怎么发 | 观感 | 结论 |
| :-- | :-- | :-- | :-- |
| ① 纯 text | `--text` | 一坨带 `**` 的原文 | ✗ 首版（且当时还只发得出第一行） |
| ② markdown→post | `--markdown` | 粗体/换行正常，**无标题栏** | △ 可用但不够 |
| ③ 精确 post | `--msg-type post --content <JSON>` | 标题栏＋颜色＋分割线 | ✓ 但 **lark-cli 会把 JSON 当 markdown 归一化**，真富文本没完全生效 |
| ④ **Card 2.0 卡片** | `--msg-type interactive --content <卡片JSON>` | 背景块＋折叠面板＋大标题焦点 | **✅ 现行**（11:37 已实发成功） |

**卡片按飞书规定走工作流产出**（`lark-im/references/card/lark-im-card-create.md`），
脚本在 `D:\项目\ai-hub\search_gateway\scripts\build_daily_card.py`：
Card 2.0｜header `blue`｜第 1 条做**唯一焦点**（title 字号）｜3 个带底色 `column_set`（blue-50 / grey-50）｜
「信号」放进 `collapsible_panel`｜**不含按钮**（按钮回调需服务端 `card.action.trigger`，本机无接收端）。

**踩过的三个坑（飞书侧）**
1. `note` tag **不被接受**：`ext=message_content has wrong tag:{note}` ⇒ 换成普通 text。
2. `config.summary.content` **必须是字符串**，给 map 会报 `expected string for content`。
3. **卡片只能 bot 身份发**（user 身份发不了，应用消息）⇒ 卡片走 **bot 私聊**通道。
   （`--content` 的 JSON 走 lark-cli 传参时**必须用 Python list 传**；在 PowerShell 里直接传会被吃掉双引号。）

**「手风琴」这件事的结论（2026-10-21 12:04）**
- **飞书 Card 2.0 没有 accordion 组件，也没有"多面板互斥展开"的机制** ⇒ **真手风琴做不了**。
  真互斥必须走 `card.action.trigger` 回调 ＋ **服务端更新卡片**（`update_multi`），而本机**没有飞书事件监听接收端**。
- **能做的"手风琴观感"（现行做法）**：
  **第 1 条展开（唯一焦点：blue-50 背景块 ＋ heading-2 大标题）＋ 第 2/3 条各成一个
  `collapsible_panel`（grey-50 底、默认收起、标题在 header 里）**。
  ⚠️ **不互斥**：展开第 2 条不会收起第 1 条（飞书没这机制）。
- **概念色块**：模型在提炼时用 `[[双中括号]]` 标出最关键的概念（每条≤2 个），
  渲染时转成 `<text_tag color='blue'>`。⚠️ **标题里的 `[[ ]]` 也要转**，否则露出裸标记。
- **字号只能用枚举**：`heading-0~4` / `normal` / `notation`；
  `config.style.text_size` 自定义 token 名**会静默失效**（郭老师反馈"所有字一样大"的根因）。

**卡片形态的最终约定（2026-10-21 12:10，郭老师三条要求）**
1. **全部条目都默认收起** ⇒ 首屏只看到 3 个**浓缩标题**（≤16 字，实测 9–15 字），
   点一下才展开内容。**不是"第 1 条展开"，是全部收起。**
2. **展开后一屏看完、不用滑** ⇒ prompt 里写死长度上限（本质 ≤60 字、用途 ≤50 字、信号 ≤40 字），
   实测展开后正文 **59–106 字**，手机一屏绰绰有余。
3. **每条必须有出处（谁发明的）** ⇒ prompt 明确「**出处 = 技术提出方/发布机构**（OpenAI、Meta、
   Coco Labs、面壁智能 OpenBMB…），**不是转发这条消息的账号**」；链接另附**可点的原文链接**。
   模型漏写时**按标题回填**候选的信源与链接（`parse_items(raw, candidates)`）。
   ⇒ 区分两件事：**发明方**（正文里的出处） ＋ **可追溯链接**（看原文）。
   实测 2026-10-21 12:58：链接自动选到了**官方来源**（`huggingface.co/SoMark/OXR`、
   `mistral.ai/news/voxtral-3/`）而不是 X 转发 ⇒ 可追溯性最好。

**2026-10-21 12:58 追加的两处微调（郭老师）**
- **去掉 emoji**（「太丑了，不好看」）⇒ `EMOJI = []`，标题只剩「1. 文档解析走向 Agent 友好」这种纯序号。
- **内容放宽一档**（"稍微详细一点"）⇒ 上限 本质 ≤60→**≤90** 字、用途 ≤50→**≤70** 字、信号 ≤40→**≤50** 字；
  实测展开后正文 **98–120 字**，手机一屏仍放得下。**标题仍 ≤16 字**（首屏只看到浓缩标题）。

## 三、关键设计（都是踩过或他定的）

1. **提炼模型用他自己的 `:8787`**，不用公共免费网关（`dsh-our-free-model` 那条**从未实测**，
   且会把 prompt 发到第三方上游 ⇒ 偏好档案不能去那儿）。
2. **模型备选顺序**：`workbuddy/minimax-m3.1-flash`（4.2s）→ `workbuddy/glm-5.3-flash` → `workbuddy/deepseek-v4.1-flash`。
   ⚠️ `traework/deepseek-v4.1-flash` **上游 ReadTimeout（90s 超时）**，不要放前面。
3. **prompt 里必须给三样东西**，缺一样就退化成流水：
   ① 他的**系统清单**（让"用途"有落点）② 他的**偏好档案**（让"筛选"有依据）③ 候选条目的标题＋摘要＋信源。
4. **允许挑 0~1 条**（prompt 里明写"宁可少，不要凑数"）。
5. **失败不推**（宁可不发也不发错）；异常写 `search_gateway\data\渠道警报.log`。
6. **每日清单落 `D:\Work\元智能\20_自适应工作流引擎\runtime\aihot_daily_picks\YYYY-MM-DD.md`**，
   **不进记忆仓**（会过时）；**只有他拍板采纳的结论**才由人写进记忆仓。
7. ⚠️ **飞书通道的老坑（2026-10-21 11:15 已修）**：`notify_capability.py` 原用 `shell=True` 传多行正文，
   **Windows 在第一个换行处截断 ⇒ 只发出标题、正文全丢，而返回码/message_id 看起来完全正常**。
   ⇒ 所有多行告警（能力体检／契约自检／本流水线）**此前一直在只显示标题**。
   修法：绕过 shell，直接 `node <npm>/node_modules/@larksuite/cli/scripts/run.js <args>`（list 传参）。
   验证：带 `--dry-run` 看请求体里 `\n` 是否齐全，**别只信返回码**。
   教训：`D:\记忆\教训\lesson_多行消息只发第一行_告警静默失效.md`。
8. **视觉增益用「精确 post JSON」（2026-10-21 11:20）**：`--markdown` 只是把 Markdown 转成 post
   （**无标题栏、单语言、样式受限**）⇒ 改用 `--msg-type post --content <JSON>` 自建富文本。
   **实测被接受**：`title` 标题栏 ＋ `text` 的 `style:["bold",颜色]`（grey/blue/orange 可用）＋ `hr` 分割线 ＋ emoji。
   **实测被拒**：`note` tag（`ext=message_content has wrong tag:{note}`）——飞书会直接报出是哪个 tag 错，
   而**被拒的消息不会到达郭老师** ⇒ 可以安全迭代收敛。
   还没用上、但飞书 post 支持的：`a` 链接、`at` @提及、`img` 内联图、`code_block` 代码块、
   `quote` 引用、`bullet`/`ordered` 列表、`collapsible` 折叠。
   **再往上一档 = `interactive` 卡片**（模块化布局、**按钮**、表单、下拉、**图表**、发后可更新、
   `card.action.trigger` 回调）——**按飞书规定必须先读 `card/lark-im-card-create.md` 工作流产出 JSON，不能手写**。
   它的价值在于：每条精选下面直接放「采纳／不采纳／想深聊」按钮 ⇒ **点一下就是决策**。

## 四、偏好档案在哪、怎么长

`D:\记忆\用户\user_偏好档案_AI资讯筛选.md`
—— 硬判据 5 条 ＋ 主题偏好 8 条 ＋ 负向 5 条 ＋ 待补充（冷启动缺口）。
**从日常对话增量积累**：他说出新的偏好就加一条（带出处），判据失效就删改，**不堆陈旧条目**。

## 五、相关

- 想法池 **IDEA-028**（需求本体，captured）
- `D:\记忆\用户\user_接收偏好_本质级文本.md`（输出模板 ①本质 ②用途 ③信号）
- `D:\记忆\教训\lesson_把采集当交付物等于交付流水.md`（反面教材）
- `AGENTS.md` 第 17 条（默认不主动汇报）、第 18 条（汇报质量门槛）
- 计划任务：`AIHOTDailyInsights`（01:20）｜候选层：`AIHOTHotSnapshot`（01:10）
