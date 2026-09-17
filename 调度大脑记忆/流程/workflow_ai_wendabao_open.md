---
name: workflow-ai-wendabao-open
description: 用 opencli 打开/复用 AI 问答宝（GPT 镜像站）并进到聊天框的流程——**优先复用已有镜像站标签页，仅在没有时才新开**；含主会话监督、定时刷新、Extended 开关等强制规则
metadata:
  node_type: memory
  type: 流程
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
  modified: 2026-09-15
---

# AI 问答宝（GPT 镜像站）最快打开流程

> 目标：从零到「能进聊天框」最短；**必须开新标签页，禁止覆盖 / 取消已经打开的标签页**。流程只读不破坏，成功即记。

---

## ★★★ 三条强制规则（2026-09-15 郭老师新增，最高优先级）★★★

### 规则一：镜像站的回复一律用**主会话**监督，不用后台任务

**禁止**用后台 Bash 任务（`run_in_background`）去轮询镜像站状态。

**原因（实测教训）**：后台任务曾在下载 10 张图时中途被 kill / 超时，留下 3 个截断文件（文件大小恰为 30000 的整数倍即截断特征），且后台任务看不到页面真实状态。

**正确做法**：
- 状态检测、等待、下载**全部用主会话的前台调用**逐步执行。
- 每步立刻看返回值，异常马上处理，不要让任务在看不见的地方跑。

### 规则二：**每过一分钟必须刷新镜像站网页**，才能拿到真实状态

**核心事实**：镜像站页面**不会自动更新** DOM。刚发送时 `imgs=0`，模型其实在后台出图，只有**刷新后**才看得到真实结果（实测：刷新前 `imgs:0`，刷新后 `imgs:33`）。

**正确做法**：
- 等待出图期间，**每分钟刷新一次**页面再读状态。
- **⚠️ 刷新方式有坑（2026-09-15 实测教训）**：直接 `location.reload()` 会把活跃会话刷成 `about:blank`，**丢失已发送的对话**。
- **安全刷新法**：刷新后若发现 `host` 为空 / `about:blank`，说明会话丢了，需重新走跳转流程；**更稳的做法是只在确认页面已稳定时刷新，且刷新前记下当前 `vip-XX` 号，以便重开**。

### 规则二·补充坑（2026-09-15 实测新增）：**刷新会把 Extended 模式重置回 Auto** ★★★

**实测**：`_ext10.py` 开启后 `pill='Extended'` → 执行 `_watch.py reload` → `pill='Auto'`。

**因此正确顺序是铁律，不可颠倒**：

```
刷新 → 重开 Extended → 验证 pill='Extended' → 注入提示词 → 发送
```

**绝对禁止"先发送、后刷新"**。本轮就因发送后才刷新，导致 Extended 失效、模型空跑，白白等 2 分钟且一无所获。

### 判断"到底有没有在生成"——`asst` 计数**不可信** ★★★

**实测反例**：`asst=0` 时模型**其实正在出图**（`data-message-author-role=assistant` 在镜像站不渲染）。

**可靠信号表**：

| 信号 | 含义 |
|---|---|
| `pill` 文本含 `Generating` / `Thinking` | ✅ **正在生成**（最可靠） |
| 图片节点 `naturalWidth > 0`（如 `1672x941`） | ✅ 已渲染完成，可下载 |
| `img.src` 含 `estuary/content?id=file_` 且尺寸非 0 | 生成图 CDN 真身 |
| `img.src` 含 `estuary` 但 `naturalWidth=0` | ⏳ 页面骨架资源，尚未出图 |
| `data-message-author-role=user` 的计数 | ✅ **可靠**：`u=1` 表示消息已入会话；`u` 不增长 = 消息根本没发出去 |
| DOM 中 `main` 区含提示词原文 | ✅ 消息确已进入会话正文 |

### 规则三：**不要弹出让用户确认下载地址的窗口**

**禁止**任何需要用户手动选择保存位置、点击"确认下载"的交互。

**要求**：Agent 全程自己 `fetch → arrayBuffer → 分块取回 → 直接落盘到预设目录`，用户不需要做任何操作。

**落盘路径统一约定**：`<项目目录>\生成图\<用途名>\`

---

## 前置

- opencli 连日常 Chrome（profile `n8hh7hyn`）。先 `opencli doctor` 确认 Extension connected。
- 只列现有标签，绝不动已开的（不 bind 乱切、不 close、不覆盖 route）。

---

## ★★★ 规则零（最高优先级，2026-09-15 郭老师明确）：**复用原有标签页，不要反复新开** ★★★

**先 `tab list` 查有没有已在镜像站的标签页。**

```
opencli browser n8hh7hyn tab list
```

- **若已存在** `vip-XX.67673.live` 的标签页 → **直接 `tab select <那个 pageId>` 复用**，
  在原会话里继续对话。**禁止 `tab new`。**
- **仅当不存在时**，才 `tab new` 打开账号池页。

**为什么**：
1. 每个新标签页 = 一次新的 Chrome 渲染进程，**反复新开会让用户浏览器堆满页面**。
2. 会话历史断裂：原会话里已有上下文（如"生成封面图片"那次对话），新开则全部丢失。
3. 用户明确要求，违反即失败。

**⚠️ 历史误执行根因（必须记住）**：
旧记忆原文写的是「**开新标签页**（不覆盖已开标签）」——
本意是"**保护用户已打开的其他标签页，不要去覆盖/关闭它们**"，
但被误读成"**每轮开工都要 `tab new`**"，于是反复新开、把用户浏览器搞乱。

**正确理解**：
- ✅ 「不覆盖已开标签」= **不要动用户其他无关标签页**（不 close / 不乱切 / 不覆盖 route）
- ✅ 「复用」= **镜像站那个标签页要一直用同一个，在原会话里继续**
- ❌ 「每次都要 tab new」= **错误理解，禁止**

---

## ★★★ 标签页为什么会消失（2026-09-15 实测锁定，郭老师要求"固定它"）★★★

### ⚠️ 2026-09-18 实测更正（opencli v1.8.6）：`bind` 的 about:blank 故障**已修复**

**实测**：`bind` 返回真实 URL 与标题（`https://vip-14.67673.live/c/6aabe39b-...`／「㉔ 优化心理课设计」），
`tab list` 同步返回该页，**无 about:blank**，用户标签页未被关闭。会话历史（u=11 / a=12）完整保留。

**结论修正**：`bind` 是**接管用户已打开标签页的唯一官方途径**，不再是禁用命令。
主要风险变成「**绑错页**」（bind 绑定的是**当前激活**标签页；实测曾绑到 `127.0.0.1:3100` 网关页）。

| 场景 | 做法 |
|---|---|
| 接管用户已开的镜像站页 | 用户把该页切前台 → `bind` → 立刻 `tab list` 验证 URL |
| 绑错页 | 立即 `unbind`（不关闭用户页）→ 用户切页 → 重新 `bind` |
| 槽位空且用户无现成页 | `tab new` |

**bind 模式两条硬约束（v1.8.6 实测）**：
1. bind 后**页面自动锚定**，无需也无法再 `tab select`。
2. bind 下 `tab new`/`tab select`/`tab close` 全被拒：`bound_tab_mutation_blocked — requires an owned OpenCLI session` → 想改绑先 `unbind`。

**`tab list` 无法枚举 Chrome 全部标签页**：`op:'list'` 带 session／`all:true`／contextId 都只返回本 session 占用的 1 个页；
不带 session 报 `Browser session is required`。→ **找已开标签页只能靠 bind 前台页，不能靠枚举**。

**daemon HTTP**：`http://127.0.0.1:19825` 必须带头 `X-OpenCLI: 1`（否则 403）。端点仅 `/ping` `/status` `/logs` `/shutdown`，**无 /tabs**。

### 🚫 真凶：`bind` 命令 —— **历史故障，v1.8.6 已修复；绑错立即 unbind**

**实测后果**：执行 `bind` 后，session 槽位被绑到 **`about:blank`**，
`tab list` 显示 `page: D5110476...` + `url: about:blank`（**不再是镜像站**）。
此后**连用户手动打开的镜像站页也会被顶掉并关闭** → 表现为「刚打开就消失」。

**完整因果链**：

1. 执行 `bind` → session 槽位被绑到 `about:blank`。
2. 此后所有 `open` / `tab new` 都作用于该绑定槽位。
3. 用户手动打开镜像站 → opencli 把其槽位切过去 → session 释放时**连用户那个页一起被关闭**。

**症状识别**：

- `tab select <旧ID>` 报 **`stale page identity`** → 槽位已被污染。
- `tab list` 里出现 `about:blank` → **立即 `unbind` 抢救**。

### 决定性稳定性实验（证明无干扰时页面不会消失）

脚本 `_tab_stability.py`，锚定后每 20 秒探测，共 60 秒：

```
第 0 次：pageIds = ['D5110476...']  url = ...f.net/?...#/chat/...
第 1 次：pageIds = ['D5110476...']  → ✅ 存活
第 2 次：pageIds = ['D5110476...']  → ✅ 存活
第 3 次：pageIds = ['D5110476...']  → ✅ 存活
```

**结论：无干扰时页面稳定存活，pageId 与 URL 均不变。**
「消失」由 `bind` 污染引起，**不是** `tab new` 的租约回收（此前结论不完整，已更正）。

### 每个 session 只维护**一个页面槽位（slot）**

两次 `open` 返回的 pageId **完全相同**（都是 `D5110476AA36326FBFB1A61F3CCF433B`）。

→ `D5110476...` **不是"某个具体标签页"，而是 session 的复用槽位**。
→ 这解释了为什么"开新页"会顶掉旧页：**它们共用一个槽位。**

### 相关命令语义

| 命令 | 语义 | 建议 |
|---|---|---|
| `bind` | 把当前 Chrome 标签页绑定到 session | 🚫 **禁用**（会换成 about:blank） |
| `unbind` | 解绑 session，**不关闭用户标签页** | ✅ **抢救手段** |
| `tab select` | 选定槽位，之后可省略 `--tab` | ✅ 每次开工锚定 |
| `close` | 释放当前 session 的 tab lease | 一般不主动用 |

`opencli browser --help` 原文关键句：

> `<session>` is a required positional: pass the name of the browser session every subcommand should operate on.
> **Reuse the same name across calls to keep the tab/state alive**; pick a different name to isolate parallel browser work.

### ✅ 正确做法

1. **绝不执行 `bind`。**
2. 开工先 `tab list`：有镜像站页就 `tab select` 复用。
3. 若见到 `about:blank` 或报 `stale page identity` → **立刻 `unbind`**，再重新 `open`。
4. 保持 session 名 `n8hh7hyn` **始终不变**。

### 🌐 镜像站域名公告（2026-09-15 发现）

页面顶部公告条提示：

> **网址 aiwenda.chat 已停用，请前往 https://ai.wendabao.net 继续使用 AI 问答宝**

- 当前 `ai.wendabao-f.net` **仍可用**（账号已登录，会员有效期至 2026-10-29，卡片列表正常）。
- **新域名 `https://ai.wendabao.net`** 优先使用，旧域名随时可能失效。
- 账号池入口是否同步迁移待验证。

### 排查记录（可复用）

1. `tab list` 返 `[]` → 先别急着重开。
2. `opencli doctor` 若显示 **Daemon running / Extension connected / profile connected** → **不是连接问题**。
3. 枚举 `chrome.exe` 看主进程 `CreationDate`，判断浏览器是否重启过。
   **⚠️ `/Date(...)` 时间戳务必用 Python 换算，不要口算**（曾把 04:06 说成 17:26）。

---

## 步骤（照抄，别重探 DOM）

0. **先查并复用**（见上方规则零）：
   ```
   opencli browser n8hh7hyn tab list
   ```
   有 `vip-XX.67673.live` → 直接复用（bind 模式已自动锚定）进步骤 2。
   **返回 `[]` 但用户浏览器里开着镜像站页** → **不要 tab new**：请用户把该页切到前台，
   执行 `bind`，再 `tab list` 验证 URL 是目标页（v1.8.6 实测安全）。这是保住原会话历史的唯一方法。
   都没有 → 走步骤 1。

1. **开新标签页**（**仅在无现成镜像站标签页时**）：
   ```
   opencli browser n8hh7hyn tab new "https://ai.wendabao-f.net/?utm_source=hidden-ncn"
   ```
   返回新 target id；**原标签保持不动**（不 close、不覆盖）。

2. **★ 锚定标签页（2026-09-15 新增，必做）**：
   ```
   opencli browser n8hh7hyn tab select <pageId>
   ```
   **为什么必做**：标签页 ID 每次调用都会变，直接 `eval --tab <旧ID>` 必报
   `Target tab ... is not part of the current browser session`。
   锚定后可省略 `--tab`，后续所有命令自动作用于该页。

3. **确认已到新对话页**：
   ```
   opencli browser n8hh7hyn eval "() => JSON.stringify({u: location.href.slice(0,55), textarea: !!document.querySelector('textarea'), ce: document.querySelectorAll('[contenteditable]').length, cards: document.querySelectorAll('.n-card').length})"
   ```
   预期：`#/chat/` 新对话页、`textarea:false`、`ce:0`、`cards:8`（8 张账号卡）。

4. **读账号卡，找可用的**：
   ```
   opencli browser n8hh7hyn eval "() => { const cards=[...document.querySelectorAll('.n-card')].map((c,i)=>({i, id:c.id||'', txt:(c.innerText||'').replace(/\s+/g,' ').trim().slice(0,60)})); return JSON.stringify(cards); }"
   ```
   预期卡片文本形如 `Plus GPT-5 ㉔ 活跃`。
   **⚠️ 2026-09-15 实测更正**：卡片文案现为 `GPT-5 ⑭` 这类（带圈序号），**匹配规则用 `/GPT-5/`**，不要用"开始对话/立即对话"（会拿到空列表）。

5. **点账号卡进聊天模式**：劫持 `window.open` 存 `__openUrl` → 合成完整指针序列点击 → `location.href=__openUrl`。
   成功判据：`location.host` 变为 `vip-XX.67673.live`。

## 铁律

- **★ 复用优先**：先 `tab list`，有镜像站标签页就 `tab select` 复用，**不新开**（规则零）。
- **不动他人标签**：绝不 close / 覆盖 / 乱切用户其他已开标签页。
- **发问闸门**：切到聊天框后，先确认顶部模型 pill = **Extended / Thinking**，禁 Auto 再发问（关联 [[feedback_gpt_mirror_subagent_flow]]）。
- **不复探**：选择器 / localStorage / 流程照抄手册，别花 2–3 分钟重编。

## ★ Extended 模式切换（最容易漏的一步，2026-09-15 强化）

**为什么单列一节**：此处曾反复漏掉，根因是旧记忆写成了「描述性观察」（"pill 选项已改名为 Thinking• Standard"）而非「动作指令」。
**描述需要推导，清单直接执行。禁止凭"上次怎么做的"惯性操作。**

**执行时机**：**注入提示词之前必须执行**。不做可能用弱模型回答，直接影响出图质量。

```javascript
// 选择器
const pill = document.querySelector("button.__composer-pill");
// 菜单项：[role=menuitemradio]，匹配规则用 /Thinking/i
// 旧文案 "Thinking• Extended" 已改为 "Thinking• Standard"
// 选中后 pill 文本变为 "Thinking"（部分情况下显示 "Model"）
```

**关键约束**：
- **必须合成完整指针序列**：`pointerover → pointermove → pointerenter → pointerdown → pointerup → mousedown → mouseup → click`。仅 `.click()` 不生效。
- **⚠️ pill hydration 坑（最大坑）**：pill 有占位态 `Model` → 稳定态 `Auto`/`Extended`。
  **占了 `Model` 就点击必扑空**，必须先轮询等 pill 变成 `Auto`/`Thinking` 再操作。
- **验证**：pill 文本变为 `Thinking`（或 `Model`）。未变则重试，最多 3 次；仍失败**停下问用户**，不要硬发。

## 固化一键脚本法（2026-09-04 实测，零→Extended ≤15s，最优选）

> 比逐段手点快 5–6 倍（74s→9.6s）。脚本在 `D:\Work\AI平台\docs\运行手册\scripts\`。两个脚本直接照抄，复探只会在跨实例时踩 hydration 坑。

```bash
opencli browser n8hh7hyn tab new "https://ai.wendabao-f.net/?utm_source=hidden-ncn"
sleep 2
opencli browser n8hh7hyn tab select <pageId>                                                  # ★ 锚定
opencli browser n8hh7hyn eval "$(cat 'D:/Work/AI平台/docs/运行手册/scripts/evalA_jump.js')"   # A：卡0 GPT-5→劫持window.open→跳 vip-XX
opencli browser n8hh7hyn eval "$(cat 'D:/Work/AI平台/docs/运行手册/scripts/evalB_ext.js')"    # B：全自动切 Extended 并验证
```

- **evalA_jump.js**：`window.open` 劫持存 `__openUrl`→点 `.n-card[0]` 第一个 GPT-5 span→`location.href=__openUrl` 秒跳。
- **evalB_ext.js**：单 async eval，内部 await 轮询（无固定 sleep）：等 host→**等 pill hydration**（占位 `Model`→`Auto`/`Extended`，占了 Model 就点必扑空，最大坑）→完整指针+原生 click 开菜单→`[role=menuitemradio]` 选 `Thinking• Extended`→等 pill=Extended 返回 `{ok:true}`。
- **新/旧对话同吃**：两者 composer 都是 `button.__composer-pill`，进旧对话(/c/…，contenteditable)后照跑 evalB 即可。
- **每次发送前**共用 evalB 复核（刷新/换对话回 Auto 就连跑 B）。

## ★ 提示词注入与取图（2026-09-15 新增）

### 注入（长文必须分块）

| 方法 | 结论 |
|---|---|
| `fill "[contenteditable=true]"` | ❌ **不可靠**：814 字符只进 112（只填第一段） |
| base64 + `execCommand('insertText')` | ✅ 可靠，但**有命令行长度限制** |

- **命令行长度限制**：base64 后超过约 3000 字符会报 `The command line is too long.`（Windows cmd 上限）
- **解法：分片注入** —— 按 3000 字符分片存 `window.__P[i]`，最后 `join("")` 再解码注入。
- 中文还原必须用 `decodeURIComponent(escape(atob(b64)))`。
- 验证：返回 `{ok:true, want:N, got:M}`，M ≈ N（差值来自 Markdown 换行）。

### 取图（大图必须分块 + 重试）

- 图片 `src` 带 `&fn=&cd=&ts=&sig=` 等参数；**URL 里的 `&` 会被 cmd 解析炸掉**（`'fn' is not recognized`）
  → **URL 先 base64 编码，再在 JS 里解码**。
- 去重：同图有多尺寸副本，按 `id=([^&]+)` 取唯一值，并选 `naturalWidth×naturalHeight` 最大的那张。
- 大图取回：`fetch → arrayBuffer → window.__buf`，再**按 30000 字节分块**（CHUNK 必须是 3 的倍数，否则 base64 跨块填充错误 `Incorrect padding`）→ **逐段** b64decode 落盘。
- **必须校验完整性**：落盘后比对 `os.path.getsize()` 与 `total`，不等即截断，**自动重试最多 5 次**。
  （截断特征：文件大小恰为 30000 的整数倍）
- **图片模型常只出图不出文字**（`asstN=0`），属正常，图和文案需自行判读。

### 其他 cmd 转义坑

- **bash 里含单引号的 JS 会被 cmd 破坏** → **一律用 Python `subprocess.run(..., shell=False)`** 写临时文件再读成单行调用。
- `eval` **不支持 `--file`** → JS 必须压成单行（`tr -d '\n'`）作为位置参数传入。

### 可复用脚本清单

位置：`D:\Work\课程思政教学竞赛\6-上课要用的素材\课件和教具\opencli_scripts\`

| 脚本 | 作用 |
|---|---|
| `_jump11.js` | 账号池 → 镜像站跳转（匹配 `/GPT-5/` 卡片） |
| `_inject10b.py` | **分块注入**提示词（推荐） |
| `_probe10.py` | 探测 send 按钮 / 输入框长度 / 模式状态 |
| `_send10.py` | 点击发送 |
| `_watch.py` | **主会话状态监督 + 刷新**（`reload` / `status`） |
| `_dl10b.py` | **分块下载 + 完整性校验** |
| `_retry_one.py` | 单张重取（带 5 次重试） |

## 关联

- [[feedback_gpt_mirror_subagent_flow]] — 子 Agent 送审三条纪律 + Extended 切换法
- [[feedback_gpt_mirror_account_switch]] — 账号受限切活跃
- [[feedback_fork_forbidden]] — 本流程全员（含子 Agent）一律 fresh 上下文，禁止 fork
- 手册：`D:\Work\AI平台\docs\运行手册\GPT镜像站送审流程.md`（§三·五 固化一键脚本法）
- GitHub 同步：Obsidian 为主（`D:\记忆` 真源）→ `yongtai-memory` 镜像（脱敏后）
- 技能同步：`C:\Users\郭永涛\.workbuddy\skills\gpt-mirror-image\SKILL.md`（WorkBuddy 侧强制执行清单）
