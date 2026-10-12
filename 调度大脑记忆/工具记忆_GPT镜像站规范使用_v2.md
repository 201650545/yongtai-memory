# 工具记忆：ChatGPT 镜像站规范使用与快速使用 v2

> 2026-09-27 整合稿。来源：GPT镜像站送审流程手册（D:\Work\元智能\20_自适应工作流引擎\docs\runbooks\GPT镜像站送审流程.md）+ 2026-09-27 AI记忆卡三轮送审实测。
> 旧散篇 feedback 保留不动，本文为整合正稿；与手册冲突时以手册 + 本文较新者为准。
>
> **⭐ 2026-10-11 关键更正（目标改回 Chat）**：实测 **`Work` 标签不可用**（据郭老师＝接 Codex、本账号无权限）—— Work + `GPT-6 Astra` + `Max` 下，连「1+1」「你好」都被 OpenAI 式安全拒绝挡回（`This content can't be shown for safety reasons`），切回 `Chat` 同题正常。**郭老师 2026-10-11 裁定：改回 `Chat` 标签 + 顶档 `High`，且默认模型必须用 `ChatGPT 6 Sol`**；2026-10-10 的「一律走 Work」裁定**作废**。**§二 已按此整节重写**；契约同步到 **v5**（`D:\Work\元智能\20_自适应工作流引擎\contracts\gpt-mirror-extended-review.yaml`）；skill 同步（`D:\Work\元智能\10_AI自成长引擎\技能库\gpt-mirror-extended-review\SKILL.md`）。
> **⭐ 2026-10-10 站点改版（背景）**：镜像站换 **新版 ChatGPT UI**，旧档位文案 `Auto / Thinking• Extended / GPT-5.6 Luna` **一个字都不剩**。模型档位改为 **顶部 `Chat | Work` 标签 + pill 内 "Power" 滑杆**，默认 `Instant`。
> **★★ 2026-10-11 模型纪律（郭老师明令）**：**默认必须用 `ChatGPT 6 Sol` + 顶档 `High`** —— 镜像站 Chat 里 `ChatGPT 6 Sol` 显示为 **`6`** 且**默认即选中**，**保持不动、不许改成 `GPT-5.6 Sol` / `GPT-5.5`**。`mode_gate` 已升**三闸**（Chat / 模型 `6` / pill `High`）。见 §二。
> **⚡ 2026-10-11 跳转加速（新增 §一·五）**：旧流程（`open` 池页 → 点卡片 → `sleep 6` → 切档）**≈40s+** ⇒ 优化后 **复用 tab ≤8s / 热启动 ≤20s / 冷启动 ≤28s**；新增脚本 `fast_jump.js`（池页读 localStorage 跳转）与 `jump_and_ready.js`（一条 eval 完成等就绪+切档+断言）。

## 一、快速打开与标签规范

1. **`eval` 默认打「活跃标签」，多标签必须 `--tab <pageId>` 定向**：`tab new <url>` 会返回 `{page:"<id>"}`，之后所有 `eval/wait/click` 都带 `--tab <id>` 才不会串台。⚠️ **2026-10-11 修正**：早先记的「`tab new` 建的标签不被跟踪」**不准确** —— 标签建出来了，只是不带 `--tab` 的 eval 打到了活跃标签。⇒ **想不打扰郭老师，就 `tab new` 开自己的标签 + 全程 `--tab` 定向**（实测可行）。⛔ 导航别用 `open`（等 network-idle ⇒ 18–21s 白等）。会话码用 `opencli profile list` 现取（当前 `d5vtd5bg`），daemon 报 stale 先 `opencli daemon restart`。**绝不点击/覆盖别人已打开的标签或链接。**
2. **eval 跟随活跃标签**：opencli 的 eval 永远打在当前活跃标签上——多 Agent 并行时这是抢占与串台的根源。每次注入/发送前必须回读 URL 与基准比对，不符即判被抢占。
3. **被抢占的红线**：不抢回。立即新开自己的标签重做，并把「跳转→切档→注入→发送」压缩为连续执行，最小化被抢窗口。
4. **会话一致性**：一个任务从哪个聊天窗口开始就留在哪（≤3 轮追问同窗口续，GPT 保上下文）。发现会话内出现**非己方消息（交叉污染）**→ 立即弃用该会话，新开对话发自包含版问题，绝不继续。
5. **★ 记住网址（最省时间的一招）**：**第一次**进入镜像后**立刻把镜像网址抄下来存档**（`D:\Work\元智能\20_自适应工作流引擎\runtime\gpt_mirror_active_url.txt`）；**第二次、第三次直接导航它**，跳过账号池与取号。进入会话页再记下完整 `/c/<id>` 网址；更可靠的是发送后立刻 `fetch('/backend-api/conversation/<id>')` 归档全文（同源即可，不依赖标签存活）。标签被切走时先从侧边栏历史按标题找回 URL，避免重发浪费轮次。
6. **★ 轮数纪律（2026-09-18 郭老师定，2026-10-11 复核确认）**：**每次任务 ≤3 轮**、**每个聊天框 ≤24 轮**（GPT 反问算同窗口；达到 24 轮 = **先要总结 → 带总结新开**，不是直接新开）。⚠️ 2026-10-11 已删掉旧「同一对话 ≤40 轮」——它与 24 冲突、且手册 §9.3（唯一真源）全篇无 40。**24 轮不是免死金牌**——GPT 一旦遗忘 / 混淆 / 答非所问，不等满轮次，立即走同一条路。契约闸门 `turn_budget` 是唯一真源。

## 一·五、跳转加速（硬性要求 · 2026-10-11 实测）

> **实测对比**：旧流程（`open` 池页 → 点卡片 → `sleep 6` → 切档）**≈40s+**；优化后 **复用 tab ≤8s / 热启动 ≤20s / 冷启动 ≤28s**（2026-10-11 实测：**4.5s / 18.8s / 22.7s**）。

**先记住两条根因**
1. **`opencli` 每次调用有 ~3.5s 纯 node 启动 + 1–6s 桥往返**（实测 `opencli --version` 单独就 3.53s）⇒ **调用次数是最大杠杆**，能一条 eval 干完的绝不拆两条。
2. **`open` 命令等 network-idle**，而镜像站 / 账号池都是长轮询 SPA ⇒ **永远不 idle**，实测 **18–21s** 才返回（纯白等）。

**六条硬性要求**
| # | 要求 | 反例（禁止） |
|---|---|---|
| R1 | **复用优先**：`state` 显示已在 `67673.live` 就直接切档 | 每次都重跑账号池 |
| R2 | **导航一律 `eval "location.href=..."`** | ⛔ `opencli browser $S open <url>`（18–21s） |
| R3 | **禁固定 `sleep`**，用页内自旋等元素 / `wait selector` | ⛔ `sleep 6` / `sleep 10` |
| R4 | **合并 eval**：等就绪 + 切档 + 断言写进同一条 | 拆成 wait + gate + verify 三条 |
| R5 | **优先直连缓存的镜像 URL**，跳过池页 | 会话还活着也绕池页 |
| R6 | **池页取号读 `localStorage`**，不点 DOM | ⛔ 等卡片渲染 + 点 span + 劫持 `window.open` |

**标准调用序列（照抄）**
```bash
S=$(opencli profile list | grep -oE '[a-z0-9]{8} default' | awk '{print $1}')
SK="D:/Work/元智能/10_AI自成长引擎/技能库/gpt-mirror-extended-review/scripts"
# ① 热路径：直连缓存的镜像 URL
opencli browser $S eval "location.href='<缓存的 https://vip-XX.67673.live/>';'go'"
R=$(opencli browser $S eval "eval(decodeURIComponent(escape(atob('$(base64 -w0 < $SK/jump_and_ready.js)'))))")
# ② 冷路径（仅当 R 报 still-on-pool / no-pill 才走）
if echo "$R" | grep -qE 'still-on-pool|no-pill'; then
  opencli browser $S eval "location.href='https://ai.wendabao-f.net/?utm_source=hidden-ncn';'go'"
  opencli browser $S eval "eval(decodeURIComponent(escape(atob('$(base64 -w0 < $SK/fast_jump.js)'))))"
  R=$(opencli browser $S eval "eval(decodeURIComponent(escape(atob('$(base64 -w0 < $SK/jump_and_ready.js)'))))")
fi
echo "$R"   # 必须 ok:true 才可发问
```
- **缓存**：每次成功进入镜像后把当前 URL 写 `D:\Work\元智能\20_自适应工作流引擎\runtime\gpt_mirror_active_url.txt`；下次先直连它。
- ⚠️ `fast_jump.js` 会读 `authToken`（**敏感值**）—— 只在该 eval 内使用，**不落盘、不入仓、不回显**。
- 两个脚本落点：`…\技能库\gpt-mirror-extended-review\scripts\`（`fast_jump.js` / `jump_and_ready.js`）。

## 二、模型选择：三闸门 —— ①留在 `Chat` 标签 ②**模型 = `ChatGPT 6 Sol`** ③顶档 `High`（2026-10-11）

> **★★ 郭老师 2026-10-11 明令：默认必须用 `ChatGPT 6 Sol` + `High`。** 镜像站 Chat 里 `ChatGPT 6 Sol` 显示为 **`6`**（「Select model」高级视图里的默认选中项，`aria-checked=true`）—— **保持不动，不许改成 `GPT-5.6 Sol` / `GPT-5.5`**。
> ⚠️ 同日背景：**`Work` 标签不可用**（接 Codex、本账号无权限）—— Work + `GPT-6 Astra` + `Max` 下连「1+1」「你好」都被 OpenAI 式安全拒绝挡回（`This content can't be shown for safety reasons`），切回 `Chat` 同题正常；2026-10-10 的「一律走 Work」裁定作废。

1. **闸门 A · 必须在 `Chat` 标签**：顶部中央 `Chat | Work` 是一组 `button[role=radio]`，`Chat` 的 `data-state` 必须是 `on`（**默认就是 Chat，不用切**；若在 Work 上，点回 Chat）。
   - ⚠️ 该开关**只在首页新对话页有**；进入某个对话（`/c/…`）后消失（实测 `radios: []`）。
   - `Chat`：3 档（`Instant` / `Medium` / `High`）。← **现行目标，顶档 `High`**。
   - `Work`：5 档（Light..Max）。❌ **不可用，别切**。
2. **闸门 B · 模型必须是 `ChatGPT 6 Sol`（★ 郭老师明令）**：
   - Chat 点 pill →「Select model」高级视图里，`[role=menuitemradio]` 清单 = `6` / `GPT-5.6 Sol` / `GPT-5.5 Leaving on October 14`。
   - **`6` 就是 `ChatGPT 6 Sol`，且默认即选中**（`aria-checked=true`）⇒ **什么都不用做，保持默认**。
   - ❌ **不许**改成 `GPT-5.6 Sol` / `GPT-5.5`。
3. **闸门 C · pill 闭态必须是 `High`**：
   - pill = `button.__composer-pill`。**Chat 标签下关闭态文本 = 档位名**（`Instant` / `Medium` / `High`）；展开态文本会变成 `Thinking effort`——**别把展开态文本当档位读**。
   - hydration 坑仍在：pill 未就绪时点它必扑空，先轮询到可操作文案再动手。
4. **切档三步（实测跑通）**：
   1. 合成完整指针序列 + 原生 `.click()` 点 pill → 开 `[role=menu]`（`data-testid=composer-intelligence-picker-content`）。
   2. 聚焦 `[role=menuitem][aria-label="Power"]` 内的 **`[role=slider]`**，连发 `ArrowRight` 直到 `aria-valuenow == aria-valuemax`（**Chat 为 `0..2`，顶 = `2` = `High`**）。
   3. **关菜单**：⚠️ 合成 pointerdown / `keys Escape` / 原生 `click` **都关不掉** → 必须 **document 级 pointerdown**（见 §三.3 第 4 条）。
5. 刷新 / 换对话 / 回历史都会重置回 **`Chat` + `Instant`**（模型仍是默认 `6`），无例外——**每次发送前重走三闸**。
6. 一键脚本：`D:\Work\元智能\10_AI自成长引擎\技能库\gpt-mirror-extended-review\scripts\jump_and_ready.js`（确认 Chat + 校验模型 `6` + 推滑杆到顶 + 关菜单 + 断言 `High`，返回 `ok`）。

## 三、注入与发送

1. **composer 判别（0×0 陷阱）**：注入前量几何尺寸——`getBoundingClientRect().width>10` 的才是真输入框。textarea 宽高 0×0 是隐形 fallback，真 composer 常是 contenteditable（新对话页也可能是可见 textarea，以实测尺寸为准）。
2. **注入**：一律 base64 + `atob` + TextDecoder 解码 + `execCommand('insertText')`（focus + selectAll 后替换写入）。native setter + input 事件 React 收不到，send-button 不会出现。长文本直接 fill 只进第一段，禁用。
3. **Windows 传参坑（四坑）**：多行 JS 必须压单行（或经 Python 生成）；URL/JS 里的 `&` 会炸 cmd，用 `\u0026` 规避；**JS 里的 `<` / `>` 也会被 cmd 当重定向**（`for(let i=0;i<n;i++)` 直接报 `SyntaxError: Unexpected end of input`）；复杂 JS 统一由 Python `subprocess(shell=False)` 生成单行脚本文件再执行。
   - ⭐ **2026-10-10 实测最稳解法**：整段 JS 先 base64，再 `opencli browser <S> eval "eval(decodeURIComponent(escape(atob('<b64>'))))"` 传入——一次性规避 `<` `>` `&` 换行四个坑，比 `tr -d '\n'` 更省事。
   - ⚠️ **2026-10-11 补坑（UTF-8）**：`eval(atob(b64))` 把字节按 **Latin-1** 解，**脚本里的中文字符串字面量会全变乱码**（实测 `'dry-run：未做任何删除'` → `'dry-runï¼æªå...'`）→ **一律用 `decodeURIComponent(escape(atob(b64)))`**（它不含 `<` `>`，可安全内联）。ASCII-only 的脚本侥幸不出错，但别赌。
4. **发送**：注入后等 ~600ms 让 React 刷新，`[data-testid=send-button]` 出现后完整指针序列 + click；若无该按钮，枚举 composer 区域按钮（aria-label/testid 匹配 send|submit 且非 voice/stop）。发送回执必须核对：userMsgs +1、stop 按钮出现、注入长度与 textarea/contenteditable 内容一致（防误发空消息）。
5. **daemon/CLI 版本不一致**（stale 报错）：先 `opencli daemon restart`，再 `profile list` 现取会话码。

## 四、结果取回与归档

1. **首选 backend-api**：完成后 `fetch('/backend-api/conversation/<id>',{headers:{accept:'application/json'}})` 拿全量 JSON（实测 116KB 级无损），解析 mapping 里 author.role=assistant 的 parts，按 create_time 排序拼接。DOM innerText 只做校验，不做主通道（虚拟滚动/被切走都会丢内容）。
2. 大文本分块取回：JSON.stringify 切片逐段取，**每段独立 json.loads 再拼接**；长文本走 `encodeURIComponent` 分段 + 本地 unquote。
3. 完成判定：stop 按钮消失 + 连续两次长度不再增长；**顶档 `High` 下思考时间视问题而定（2026-10-11 实测两个无害问题分别约 32s / 18s 完成）**，`streaming:true len:0` 属正常。
4. **回复归属判定**：共享账号池下多 Agent 并发，必须按 user 消息精确特征（长度/开头文本）配对确认 assistant 回复归属，逐条核对再归档。
5. 全文先落盘归档（项目正库目录），再汇报摘要；汇报必须给全文绝对路径。

## 五、文档粘贴规范

1. 只贴**纯文本**（Markdown 源码可以）；富文本/HTML 不贴。
2. 超长文档不直接贴：拆成 ≤2 个长输出问题的多轮（单任务 ≤3 轮、每窗口 ≤24 轮），或走 GitHub 强读（见六）。
3. 注入用 base64 路径天然规避富文本问题；粘贴动作本身（人工）也建议从纯文本编辑器中转。

## 六、提问方法：GitHub 强读（2026-09-28 更新：公开仓 + 强读已验证 ✅）

- **政策演变**：09-27 初版为「私有仓+精选文档+送审前 push」；09-28 郭老师升级拍板——**小项目先公开，产品成熟后再转私有**。理由：GPT（镜像账号池）无法登录读取私有仓，公开后 GPT 网页浏览可直接强读，回复质量显著更高。
- **仓库**：`https://github.com/201650545/listenloop-curated`（现已公开，匿名可访问）。
- **范围（精选）**：ListenLoop Obsidian 正库（`D:\Work\AI精听训练器`）中的架构与设计类文档——README、00_项目驾驶舱_可视化中心、01_商业与战略规划、02_工程架构与系统设计全部；**不含**开发日志流水、03_归档目录、GPT 评审原文、任何密钥/凭证/个人隐私内容。
- **时机**：每次送审前 push 一次（`git -C "D:/Work/AI精听训练器/05_发布与问诊/listenloop-curated" add -A && commit && push`，走 `http.proxy=http://127.0.0.1:7890`），提示词精确列出文件路径清单要求 GPT 强读。
- **已验证（2026-09-28）**：GPT 可正常读取公开仓文档并准确复述内容（红线表格逐字匹配）——强读链路闭环。
- **红线**：密钥/凭证/个人隐私永不入仓；开发日志与评审原文暂不外发；产品成熟后整体转私有（届时需重新解决 GPT 读取授权）。
- **建仓与推送流程**：从 `D:\Work\AI精听训练器\` 同步精选文档到 `D:\Work\AI精听训练器\05_发布与问诊\listenloop-curated` → `git -C <仓> add -A && commit && push`（走既有代理）→ 提示词写「请先读 <repo>/<path> 后再…」。
- **红线**：密钥/凭证/个人隐私永不入仓；开发日志与评审原文（含 GPT 输出）暂不外发；建仓前把精选清单给郭老师过目一次。

### ✅ 已落地（2026-09-27 深夜，郭老师授权）

- **私有仓已建成**：`https://github.com/201650545/listenloop-curated`（private，经既有 git 凭据调 GitHub API 代建，无需 gh CLI）。
- **首次推送完成**：本地仓 `D:\Work\AI精听训练器\05_发布与问诊\listenloop-curated`（commit `ac2d269`），20 篇精选文档已推送至 main。
- **后续送审前 push 流程**：正库文档更新后 → 拷贝到本地仓 → `git -C "D:/Work/AI精听训练器/05_发布与问诊/listenloop-curated" add -A && git commit && git push`（走 7890 代理）。
- **安全红线（新增）**：git credential fill 的输出不得打印（PAT 会随工具输出暴露进会话记录）——凭据只允许在 Python 进程内存中读取使用；本次暴露的 token 建议在 GitHub 设置中轮换。

## 七、流程提速清单（实测有效）

1. 账号池 → 跳转 → 切档 → 注入 → 发送五步合并连续执行，被抢窗口最小化。
2. 发送后立即 backend-api 归档，省掉 DOM 轮询窗口与丢失风险。
3. 最深档等待期（1–3 分钟）不做无关操作占用桥接。
4. daemon stale / 会话码轮换 / 0×0 composer / `&` 炸 cmd / `<` `>` 炸 cmd / 多行 JS——六个高频坑全部有固定解法，遇错先对照本文而非重新探索。

## 八、额度机制与账号分配（2026-10-10 实测）

> 完整版见 `D:\Work\元智能\20_自适应工作流引擎\docs\runbooks\GPT镜像站Work模式模型与额度指南.md`

1. **三层额度**：①**平台层** = 问答宝会员制、不按次计费，会员有效期至 **2026-10-29**（`userInfo.balance=0`、`hasPurchased=true`、`isValid=true`）；②**账号层** = 每个镜像账号各带一份 OpenAI feature limits；③**档位层** = 滑杆恒定提示 `Consumes usage limits faster`，**档位越高、烧账号额度越快**（5 档都显示这句，是滑杆整体说明，不是分档提示）。
2. **查额度（只读，一行）**：在**账号池页**（`ai.wendabao-f.net`，不是 vip-XX 镜像页）执行
   `JSON.parse(localStorage.getItem('panelAccountList')).map(a=>({id:a.carID,badge:a.badge,limits:(a.metadata&&a.metadata.limits_progress||[]).map(x=>x.feature_name+'='+x.remaining)}))`
   —— 建议挂成"派活前的只读探针"，别等失败才发现额度空了。
3. **badge = 底层 ChatGPT 档位**：`PLUS` → 侧栏显示 `郭老师 / Plus`；**`PROLITE` → 侧栏显示 `郭老师 / Pro`**。
   - **PLUS（13 张）**：`deep_research` 20–25、`file_upload` 0–80、`paste_text_to_file` 76–80、`image_gen` 120
   - **PROLITE（4 张：vip-31/27/32/30）**：`deep_research` 107–122（≈5×）、`image_gen` 1000（≈8×），**但没有 `file_upload` / `paste_text_to_file` 两项**（"不限"还是"不支持"未验证）
4. **分配口诀**：**重活 / 深研 / 生图 → PROLITE；上传文件 / 粘贴长文 → PLUS**；派账号前先跑 §八.2 那行查询，别派到 `file_upload=0` 的账号（vip-24 实测为 0）。
5. **省额度**：别无脑拉满档（平台明确提示越高效越费额度）；只有真需要深推理时才拉到 `High`；同主题复用同一窗口，别重复交代背景。
6. **边界**：`metadata.model_limits` 实测为**空数组** ⇒ 看不到"某模型还能发多少条"；"哪个模型擅长什么"**官方无任何说明，一律不写、不许编**。
