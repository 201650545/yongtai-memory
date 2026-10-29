---
name: workflow_daily_essence_brief
description: 每日本质精选流水线——AIHOT 候选 → 自有网关免费模型提炼（≤3 条·本质+用途）→ 飞书汇报；清单落 runtime 不进记忆仓
type: workflow
updated: 2026-10-21
kind: rule
status: active
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
  3. 实时语音可控部署 → `:3100` 的 voice-asr/tts/chat/realtime 候选池 ＋ 晨读跟读拆分

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
- **再放宽一半**（2026-10-21 13:00，"展开之后的内容还可以再增加一半"）⇒ 本质 ≤**135**、用途 ≤**105**、
  信号 ≤**75** 字；实测展开后正文 **140–163 字**，仍在手机一屏内。
- ⚠️ **标题双重加粗**：模型可能自己写 `**标题**`，我若再包一层 ⇒ 渲染出 `**1. **标题****` 残留。
  ⇒ **先剥掉模型标题里的 `**`，加粗统一由 header 那层加**。

## 三·真手风琴（2026-10-21 13:20 落地）

**郭老师定**：「通常我这个信息是 3 条不一样的信息，根本就很少会有对照的情况出现……那我就直接来问 AI 了」⇒ **要真手风琴**（互斥展开）。

**为什么不能用 `collapsible_panel`**：它的展开/收起是**客户端本地行为、不回调服务端**
⇒ 服务端不知道"用户展开了哪一条"，做不出互斥。**只能让展开动作走 `button`（callback）**。

**实现（`buddy2api\scripts\card_accordion.py` ＋ `card_accordion_listener.py`）**
```
卡片：每条 = 一个标题 button（behaviors:[{type:"callback"}], value:{"idx":i}）
      ＋ 只有「当前展开那条」下面才有 本质/用途/出处/信号（服务端渲染）
用户点第 2 条
   → 飞书 card.action.trigger 回调（带 token：30 分钟有效、限用 2 次；带 action_value 与 card_content）
   → 监听器解析 idx ⇒ 重建整张卡片（只展开那一条，其余只留标题按钮）
   → POST /open-apis/interactive/v1/card/update  ⇒ 屏幕上永远只有一条内容
点已展开的那条 ⇒ 全部收起（toggle）
```
- **状态**：`20_自适应工作流引擎\runtime\card_accordion_state.json`（message_id → {date, open_idx, items}）
  —— 卡片里不存业务数据，只存原始条目，更新时据此重建。
- **发送端降级**：心跳文件 `card_accordion_listener.hb` 新鲜（<5 分钟）⇒ 发**手风琴卡片**；
  否则降级**本地折叠版**（点标题本地展开，不互斥但能用）⇒ 不会出现"点了没反应"。
- **卡片 JSON 必须用文件传参**（`--data @card_update.json`）：Windows 命令行上限 ~8191 字符。
- ⚠️ **硬前提（必须他本人在飞书开放平台点，脚本代劳不了）**：
  应用 `cli_aac444d793b85cc5` → **事件与回调 → 回调配置 → 订阅 `card.action.trigger`**（长连接方式）。
  官方文档明说**没有预检** ⇒ 没订阅就**静默收不到事件**（表现为"点标题没反应"）。
- 常驻：计划任务 `Buddy2API_CardAccordionListener`（登录即起）＋ `lark-cli event status` 看总线
  （`Bus: running` / `Active consumers: 1` / `DROPPED 0` 才是健康）。

### ★ 结局（2026-10-21 13:28）：**手风琴做通了，但他选了折叠面板**
- **手风琴实测 7/7 全成功**：他那 7 次点击（点第 1/2/3 条来回点）**每次都正确互斥**，
  0 失败、0 丢包；日志 `card_accordion_listener.log` 里逐条可查
  （`事件#2 点第2条 → updated:open=1` ⇒ 第 1 条自动收起）。
  ⇒ **结论：飞书上是能做出真手风琴的**（不必再怀疑技术路径）。
- **但郭老师体验后定案：用「本地折叠面板」**（`collapsible_panel`，纯文字标题行、点开即展）。
  ⇒ 他放弃的不是能力，是**交互形态**：按钮式标题不如纯文字标题行顺眼（他先前也说 emoji/按钮"太丑"），
  而且本地展开**零等待**，不用等服务端往返。
- **落地处置**：监听器已停、心跳已清、计划任务 `Buddy2API_CardAccordionListener` **已禁用**；
  每日流程改回 `build_daily_card.build_card()`（折叠面板版）。
  **手风琴代码保留在 `buddy2api\scripts\card_accordion*.py`（未启用、未删）**——
  他哪天想换回去，只要启用任务 ＋ 打开流程里的分支即可（一行开关）。

## 四、模型不可用怎么办（2026-10-21 13:35 郭老师问的三层保底）

郭老师问：「调用什么模型发的？如果那个模型不能用了怎么办？」——**这一问揪出了真隐患**：
旧备选链 3 个模型**全在 `workbuddy/` 一个渠道** ⇒ 同生共死；而失败时只写日志、不通知
⇒ 他会以为"今天没值得说的"，其实是我这边挂了（正是"该喊的时候没喊"）。

**现在的三层保底（已实测）**
1. **跨渠道备选链**（8 个模型，4 条渠道）：
   `workbuddy/minimax-m3.1-flash`（实测 4.2s）→ `traework/minimax-m3.1-flash` →
   `workbuddy/glm-5.3-flash` → `traework/glm-5.3-flash` → `loomy/GLM-5.3-Flash` →
   `raccoon/sn-glm-5-3-flash` → `workbuddy/deepseek-v4.1-flash` → `traework/deepseek-v4.1-flash`（慢，最后兜底）。
2. **零模型保底**：模型全挂 ⇒ 拉 AIHOT 上游自带的整理稿 `https://aihot.news/api/v1/agent/latest`
   （**上游服务端生成，不经过任何模型**）⇒ 解析出标题/摘要/推荐理由/原文链接/信源，
   仍能出一张卡（标注"本次为原始整理稿，未做用途映射"）。实测故障注入（模型全指向不存在的 id）→ 成功出 3 条。
3. **失败必须通知**：模型全挂且保底稿也失败、或飞书推送失败 ⇒ **主动发告警**给郭老师
   （走 user 身份 p2p，与卡片不同故障域），文案明说"今天没能发出"＋原因。

**另外抓到的真实不稳定**：上游 AIHOT **偶发 TLS 握手失败**
（`TLSV1_ALERT_PROTOCOL_VERSION`，实测热榜那次失败、items 那次成功）⇒
`aihot_hot_snapshot.http_get()` 加了 **curl 兜底**（Windows 自带 `curl.exe --compressed`，
上游文档也推荐这个组合），失败时自动重试一次；实测连抓 3 次全部正常。

## 五、"我不用你了，这流程就没用了？" —— 逐条拆开（2026-10-21 13:49 郭老师问）

**结论：运行环节 0 依赖任何 Agent 在线**；真正的单点不是"我"，是**Windows 的登录态**。

| 环节 | 宿主 | 需要 Agent 在线吗 |
| :-- | :-- | :-- |
| 01:20 触发 | Windows 计划任务 | 否 |
| 抓 AIHOT | python（curl 兜底） | 否 |
| 提炼 | **:8787 网关自己的免费模型**（网关是独立服务） | 否 |
| 推送 | lark-cli（node 独立进程） | 否 |
| 落盘 | 脚本自己写 | 否 |
| **改模板 / 调 prompt / 把好条目沉淀进记忆** | 需要某个 Agent | 需要，**但换谁都行**（脚本在 ai-hub 仓、机制在 `AGENTS.md`、结论在记忆仓、偏好档案在 `记忆仓\用户\`） |

**真实单点（比"我不在"实际得多）**：任务原本 `LogonType=Interactive` ⇒
**只在他已登录时才跑**。⇒ **锁屏不影响**（照跑）；**注销登录 / 重启后没登录** ⇒ 停，且**没人知道**。

**三条解法与取舍**
1. **S4U（不需登录即运行）** —— 实测**没成**：lark-cli 的 app secret 存在 **Windows DPAPI（用户密钥）**，
   S4U/SYSTEM 任务**解不开**；要绕过只有两条路：**任务计划存他的 Windows 密码**，或
   **把 app_secret 明文存成 SYSTEM 专用文件**。⇒ **两者都是凭据外置，属安全决策，得他点头**。
   （脚本已备好：`buddy2api\scripts\s4u_migrate_daily_tasks.ps1`，含探针＋失败不改原状的保护。）
2. **★ 零凭据风险的落地解（已做）**：两个每日任务**各加一个 AtLogOn 触发** ⇒
   **注销期间漏掉的，他一登录就自动补跑**；配合**幂等标记**
   （`aihot_daily_picks\aihot_daily_done_YYYY-MM-DD.txt`，**推送成功后才写**）
   ⇒ 当天已发过就秒退，不会重复打扰。实测幂等跳过正常。
3. **锁屏本来就不受影响** ⇒ 现实影响面比想象小。

⇒ 结论：**"我不用你了"不影响每日简报照发**；"你注销了"只会**延迟**（登录即补），不会丢。
真正需要"人/Agent 在线"的只有**改口味**与**把条目沉淀进记忆**这两件可选的优化。

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
