---
name: workflow-gpt-repo-sync
description: 向 ChatGPT 提问前必做三步：让它先读 GitHub 仓库了解结构、有更改先 push 到 english-teaching-production、补齐上下文
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 72205e30-501c-4c38-91a5-20cf27cb4d60
  modified: 2026-09-03T17:19:21.757Z
---

教师拍板（2026-08-06）的 GPT 对话流程：每次向 ChatGPT 发包前必做三步——
1. **让 GPT 先看 GitHub 仓库**：问题包开头写明「请先读 `201650545/english-teaching-production`，重点看 00_格式规范/05_索引说明.md、更新记录.md、00_总规划/README_索引.md」。
2. **有更改就更新仓库**：规范/工具/命令/交付记录变更落盘后，同步到 `english-teaching-production` 并 push，再问 GPT。手动 push（教师已决定不配 Actions 自动同步）。staging 仓库在 `C:\Users\郭永涛\AppData\Local\Temp\eng-teaching-up`。**不入库**：`_*.py`/`fix_*`/`check_*` 临时脚本、zip、06_归档。
3. **补充上下文**：问题包必须带本次要解决什么、涉及文件路径、已知限制/红线、期望输出格式、最近一次仓库更新日期。

**Why:** GPT 读不了本地 D:\英语教学，GitHub 仓库是它了解项目结构的唯一通道；仓库过时 = GPT 基于旧结构回答 = 方案作废。
**How to apply:** 每次写 GPT 问题包时先核对仓库是否最新（本地 commit 与 origin/main 一致）；有未 push 变更先 push 再写包。仓库当前状态：2026-08-06 commit `7b2add5`（129 文件，含全部最新命令/交付记录/问题包）。规范文件：`D:\英语教学\00_总规划\GPT对话流程规范_20260806.md`。关联 [[workflow_human_ai_research]] [[project_english_teaching_specs]]。

**GitHub 直读技巧（2026-08-26 教师补充）**：ai-hub 项目（网关）问 GPT 时同样走此流程——核心代码已在 `201650545/ai-hub`（分支 refactor/monorepo-20260812）。提示词必须**精确列出要读的文件路径清单**（如 `services/search_gateway/rate_limit.py` + 一句「这个文件是什么」），不要只给仓库根或单个文档链接——指定路径它读得快、上下文全。push 需代理：`git -c http.proxy=http://127.0.0.1:7890 push`。

**镜像站直连（2026-08-08 教师告知）**：以后问 GPT **无需教师中转复制**——直接用 Open CLI（命令行打开浏览器）访问镜像网站，在输入框中输入问题、等待回复即可。镜像站 URL：`https://vip-49.67673.live/c/6a74a480-4a94-83ea-80ef-79f314872354`。用法：用浏览器/命令行打开该 URL → 在对话框输入问题包内容 → 等待 GPT 回复 → 读取回复。三步流程（先读仓库/push/补上下文）仍有效，只是**输入和取回复由我直接完成**，不再靠教师粘贴。关联 [[workflow_human_ai_research]]。

**镜像站实操细节（2026-08-08 收口实测打通；2026-08-25 大更新；2026-09-03 wendabao 账号池流程补全）**：
- **对话轮数规则（教师 2026-08-25 明确，必须遵守）**：同一对话**不超过 40 轮就不要新开对话**——继续在当前历史对话里问（GPT 保有上下文，质量更高）；**每个任务须在 3 轮问答内完成**（GPT 反问或需追问就继续问，但总轮数 ≤3）。
- **⚠️ 2026-09-03 起入口变更（vip-09 直连已失效）**：`vip-09.67673.live` 现强制重定向到 `ai.wendabao-f.net`（AI问答宝账号池导航站），不再是直接 chat 界面。**wendabao 账号池完整流程（实测打通）**：
  1. 打开 `https://ai.wendabao-f.net/?utm_source=hidden-ncn#/chat/<id>`（或 vip-09 跳转过来），页面显示引擎卡片（问答宝宝/ChatGPT/Claude/DeepSeek/Gemini/Grok）+ Plus 账号卡片列表（GPT-5 ㊽⑫⑬…，绿色圆点=活跃）
  2. **必须遵守共享标签页纪律**：`tab new` 新建自己的标签页操作，绝不占用别人的
  3. **点 Plus 账号卡片的 GPT-5 span 文字**（不是 Plus 徽章按钮——那个只刷新账号池列表）：`.n-card span` 里 innerText 以 "GPT-5" 开头的第一个
  4. **关键坑**：点击触发 `window.open('https://vip-XX.67673.live/api/v2/plus-login?account=...&jwt=...')`——**Chrome 弹窗拦截会吃掉它**，当前标签变 about:blank
  5. **破法**：先劫持 `window.open = function(u){ window.__openUrl = u; return null; }`，再点 span，然后本标签 `location.href = window.__openUrl` 跳转（绕过拦截）
  6. 到达 `vip-XX.67673.live` 真镜像界面：textarea（placeholder "Ask anything"）+ ProseMirror contenteditable 并存；按下面注入规则操作
- **React 菜单/按钮点击（关键坑）**：opencli 的 CDP click 和 JS element.click() 都**点不开**模型下拉菜单——必须用 JS 派发**完整指针事件序列**：pointerdown→mousedown→pointerup→mouseup→click（带 clientX/Y 坐标，getBoundingClientRect 取中心）。模型按钮=文本恰好 "Auto" 的 button；菜单项 "Thinking• Extended" 同法点击；点完按钮文本变 "Extended" = 生效。页面刷新后模式会重置回 Auto，每次都要重切。
- **切换 Extended·新 UI（2026-09-01 vip 实测，vip-48 也适用）**：pill 变为 `button.__composer-pill`（文本 Auto）。**opencli 原生 click 与键盘 ArrowDown 都开不了 Radix 菜单**；必须 eval 合成**完整指针序列**（pointerover→pointermove→pointerdown→mousedown→pointerup→mouseup→click，带 pointerId/pointerType）打在 pill 中心。菜单项：`[role=menuitemradio]` 的 "Auto" / "Thinking• Extended" / "GPT-5.6 Luna"。选完 pill 显示 "Extended"。
- **注入提问（关键坑）**：**新对话页** composer 是 textarea（placeholder "Ask anything"）→ 用原生 value setter + input 事件；**历史对话页** composer 是 contenteditable div（那个 textarea 是 0×0 的 `wcDTda_fallbackTextarea`，注进去不显示！）→ 必须 focus + `execCommand('insertText')`（先 selectAll 清旧内容）。中文用 base64+atob+TextDecoder 解码后注入。**2026-09-03 vip-48 实测**：`opencli browser <s> fill "[contenteditable=true]" "<text>"`（CDP 设值）对 ProseMirror 一次成功（filled:true，941 字符全进），比 eval 注入简单——优先 fill。发送=[data-testid=send-button] 同样用完整事件序列；流式中=[data-testid=stop-button] 存在；回答=[data-message-author-role=assistant] 最后一条。
- **深度问题至少等 15 分钟**（Extended 思考 1-3 分钟后才出字，streaming:true len:0 属正常）。教师强调搜索要给足提示词、选思考模型+Extended。
- **提速原则（2026-09-03 教师拍板，固定流程）**：这个点击流程「明明很简单」——固定 4 步：①开池先扫**绿色活跃**账号卡、受限直接跳过别点（找可用账号最慢，先扫再点是头号加速）；②点 `innerText 首 "GPT-5"` 的第一个 `.n-card span`（非 Plus 徽章），先劫持 `window.open` 存 `__openUrl` 再点、再 `location.href=__openUrl` 破弹窗拦截秒跳；③扫聊天记录——同主题聊过就复用原窗口（保上下文），全新主题立马新开 tab；④切 Extended=pill `button.__composer-pill` 只能 eval 合成完整指针序列点开、`[role=menuitemradio]` 选 "Thinking• Extended"、pill 变 Extended 才生效。**提速最大杠杆=选择器一次固化写死不复探 + 菜单一律合成指针序列（原生 click/键盘开不了 Radix）**。完整固定流程与选择器速查表已落**Obsidian 知识库**：`D:\Work\AI平台\docs\运行手册\GPT镜像站送审流程.md`（ai-platform 仓；2026-09-03 Obsidian 五库→两库整合后挂载点移入 Work，原 `D:\AI平台` 已并入）。关联 link 见该文档。
