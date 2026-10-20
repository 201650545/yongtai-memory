---
name: reference-生图渠道盘点与网页版伪API
description: 网关生图渠道全盘点（商汤/AGNES/即梦/豆包/元宝…，含免费与付费的边界）、buddy 渠道不能生图的结论，以及 opencli 驱动的「网页版生图伪 API」的实现与三个坑。
type: reference
updated: 2026-10-20
---

# 生图渠道盘点 + 网页版伪 API（2026-10-20）

起因：郭老师问「我的 API 转发网关里哪些渠道能生图？免费的有哪些？buddy 渠道支不支持生图？」
并定调：**ark/seedream 是付费的，删掉不用，只用即梦 CLI**；豆包/元宝网页版能生图，
若不能反带就用 **opencli 模拟人类操作**做成「伪 API」——跟 ChatGPT 镜像版一个套路。

## 一、结论速查（全部实测）

| 渠道 | 能不能生图 | 免费？ | 实测 |
|---|---|---|---|
| 商汤日日新 `sensenova-u1.5-fast` | ✅ | ✅ 免费 | 11~12s，4.5~6MB PNG |
| 商汤日日新 `sensenova-u1.5-lite` | ✅ | ✅ 免费 | 22.7s（慢一倍，别用） |
| AGNES `agnes-image-2.5/2.1/2.0-flash` | ✅ | ✅ 免费 | UA 必须 `curl/8.5.0`；**直连 TCP 超时，走 7890 代理才通** |
| ark `doubao-seedream-*` | ✅ 能 | ❌ **付费** | 已按指令**下线**（`api_gateway.py` 里删了分支，直接 400） |
| 即梦（网页版 / jimeng-free-api） | ✅ 能 | ✅ 免费积分 | 见第四节 |
| 豆包网页版 | ✅ 能 | ✅ 免费 | 伪 API 实测出图成功（171KB PNG） |
| 元宝网页版 | ✅ 能 | ✅ 免费 | 同豆包流程，未单独验证 |
| 千问 / Gemini / Grok / ChatGPT web | ✅ 能 | 免费但要登录态 | opencli 有原生 image 命令，未逐个验证 |
| **buddy（workbuddy）** | ❌ **不能** | — | 见第二节 |

## 二、buddy 渠道不能生图（三重证据）

1. `:3100` 里的 `buddy` 是**回环自定义渠道**，指向 `http://127.0.0.1:8787/v1`（= Buddy2API），
   只挂 `model=auto`，生图相关条目 **0**。
2. Buddy2API 自己**没有生图端点**：`POST /v1/images/generations` → **404**；
   `openapi.json` 35 条路由里 **0 条**含 image。
3. 8787 目录 33 个模型，**0 个**生图模型名。唯一带生图名的是 loomy 的
   `qwen-image-3.0-pro` / `Hy-Image-3.5-preview` / `doubao-seedream-5-lite`，
   但上游**全部 404**「该模型暂未开放」——是上游没开，不是调用姿势问题。

⇒ 要生图走 `:3100` 的 `image-gen`（商汤/AGNES/即梦/伪 API），**别走 buddy**。

## 二之二、还能「嫖」到哪些：用免费模型全表扫出来的 7 家（2026-10-20 实测结论）

扫描法：`search_gateway/data/channel_free_models.json`（每日 01:46 自动刷新的「免费模型全表」）
× `channels.json` 里**已配 key** 的渠道 → 脚本 `search_gateway/scripts/scan_free_image_channels.py`。

| 渠道 | 免费生图模型 | 实测结论 |
|---|---|---|
| **cloudflare** | `@cf/black-forest-labs/flux-1-schnell` | ✅ **可用**。Workers AI 免费层（每天 10,000 neurons），**实测 6.3s 出图**。接口形状特殊：`POST {base}/run/{model}` body `{prompt}` → `{result:{image: base64}}`（**没有 data 数组**，原样透传会让客户端拿不到图）；且 base_url 以 `/ai/v1` 结尾而 run 端点是 `/ai/run/`（没有 v1），拼错直接 400 |
| agnes | `agnes-image-2.5/2.1/2.0-flash` | ✅ 已接（需走 7890 代理） |
| nvidia | `flux_1-schnell` / `flux_1-dev` / `flux_1-kontext-dev` / `flux-3-image-klein` | ❌ 带点 `flux.1-schnell` 与带下划线两种写法都 **404** —— 这个 key 没该模型权限 |
| modelscope | `Qwen/Qwen-Image-Edit` | ⚠️ 提交返回 `task_id`（异步），但轮询 `/v1/tasks/{id}` 报 *task not found*，取结果端点未搞清，暂不接 |
| gemini | `gemini-2.5/3-pro/3.1-flash-image`、`nano-banana-2.1` | ⚠️ 走 **chat/completions**（modality=image），不是 images/generations，端点形状不同 |
| openrouter | `google/gemini-*-image`、`openai/gpt-5-image(-mini)`、`gpt-5.4-image-2` | ⚠️ 同上，走 chat；且这些在 OpenRouter 上**未必 0 价**（gpt-5-image 系列计费），别当免费用 |
| siliconflow | `Qwen/Qwen-Image`、`Z-Image(-Turbo)` | ⛔ 免费表把它当赠金，但**官方价目页标 ¥0.30/百万 Tokens（非 0 价）** ⇒ 有扣费风险，**不碰** |

**结论**：真正"白嫖"且**API 直连、不开浏览器、不会触发风控**的生图通道目前是
**商汤 ×2 + Cloudflare flux-1-schnell + AGNES**（都在 image-gen 链里），
网页版（豆包/元宝/即梦/千问/Gemini）作为慢兜底。

> 顺带修了个坑：`_handle_images` 外层原本 `except Exception` 把**任何**异常都报成
> 「请求体不是合法 JSON」，上游真实失败原因全被吞掉 ⇒ 改成带真因的报错。

## 三、网页版生图 —— 落成**正式 API 模型**「image」

> **最终形态（2026-10-20 晚，按郭老师要求两次调整）**：
> 生图不是网页按钮，而是 **模型列表里能选、像普通模型那样调**的东西。
>
> **设计：语义分层 + 能力表 + 点名（2026-10-20 13:20 郭老师问「怎么设计」）**
> 郭老师的原问：每个生图都作为一个模型？还是只要一个 image 由后台路由分发？
> 「这样好像不适合精细化控制吧」；「①做成模型？②还是通知 Agent 去调有深度的 API 选模型？」
> ⇒ **两个都要，但模型按「语义」命名，不按「厂商」命名**：
>
> 1. **语义模型**（进模型列表，给人用，4 个）：
>    - `webimage/image`「image」——通用/自动
>    - `webimage/image-fast`「image · 极速免费」——商汤/AGNES（秒级、不开浏览器、不烧积分）
>    - `webimage/image-hq`「image · 高质量」——即梦 5.0 Lite 等（积分制）
>    - `webimage/image-web`「image · 网页版免费」——豆包/元宝（免费但慢）
>    **命名**：主模型就叫 **image**（2026-10-20 郭老师原话「你字打错了就叫 image」——
>    之前我把它写成「猪吧image / zhuba-image」是自作聪明的玩笑，已全部改掉；
>    「猪吧image」「image-gen」「zhuba-image」仍作为**服务端别名**兼容，但不再出现在 id 里）。
>    **为什么不按厂商铺模型**：豆包慢、即梦烧积分、商汤最快……这些是**渠道知识**，
>    不该要求选模型的人（或 Agent）先知道；「要快/要好/要免费」才是真实需求。
> 2. **能力表**（给 Agent 查）：`GET /v1/web/images/capabilities`，
>    每个通道带 tier/cost/speed/browser/risk/note ⇒ Agent 先查表，
>    再决定用哪个语义模型、还是点名某通道拿精细控制。
> 3. **点名通道**（可调，但**不塞进模型下拉**，避免下拉被 10 个厂商条目淹没）：
>    `webimage/{sensenova-u1.5-fast,sensenova-u1.5-lite,agnes-image-2.5-flash,doubao,yuanbao,jimeng-5.0,qwen-image,gemini-image,grok-image,chatgpt-image}`
>
> **命名**：id 用 ASCII（`zhuba-image`），**显示名 = 猪吧image**；
> 同时接受中文别名 `猪吧image` / `猪吧` / 旧 id `image-gen`（模型 id 带中文会踩
> YAML/客户端校验的坑，所以别名走服务端解析，不进 id）。
>
> **调用**：`POST http://127.0.0.1:8787/v1/chat/completions`
> `{"model":"webimage/image","messages":[{"role":"user","content":"提示词"}]}`
> **返回**：标准 OpenAI chat completion，`content` =
> `[{type:text,…},{type:image_url,image_url:{url:"data:image/png;base64,…"}}]`
> ⇒ 任何 OpenAI 兼容客户端（DSH / Claude Code / OpenCode）都能直接显示图。
> 实测 10.3s，走商汤 u1.5-fast，base64 PNG。
> 已进 `selected_models` 与 DSH profile（26 个模型，漂移自检一致），**DSH 重启一次**生效。
>
> **链路**：`:8787`（有浏览器权限）先打 `:3100` 的**点名**快通道（商汤/AGNES，免费 11~22s），
> 都不成再走本地网页版（豆包/即梦/元宝，40~150s）。
> **回环防护**：`:8787 → :3100` 只用**点名**模型、不用 `image-gen` 别名；
> `:3100` 的 image-gen 链末尾 `imgpseudo` 指回 `:8787` 的 `/v1/web`（只跑网页版），两边各自单向。
>
> **坑**：`:3100` 的生图直点**只认不带「渠道/」前缀**的名字
> （`sensenova-u1.5-fast` ✅ / `sensetime/sensenova-u1.5-fast` ❌ 400「未支持的生图模型」）。
> 第一版快通道写成带前缀的 ⇒ 全被拒、直接掉进慢的网页版分支（差点又触发风控）。

**为什么不能把网页版生图塞进 :3100**：:3100 是 **LocalSystem** 身份跑的 NSSM 服务，
够不着用户交互会话里的 Chrome，而 opencli 的浏览器桥接（扩展 + 守护进程 19825）
**只存在于用户会话**。Buddy2API（:8787，计划任务 Buddy2API_Gateway / Interactive）
正好以当前用户身份常驻 ⇒ 网页版生图只能住在这一侧。

### 豆包/元宝的流程（无原生 image 命令）

`opencli browser default open <站点URL>`（**先把绑定标签切到该站点**）→
`opencli <site> new`（**开新对话**，在旧对话里直接 ask 不会触发生成）→
`opencli <site> ask "<画图提示词>"` → **只回一段意图预演文本**，图是**异步**生成的 →
每隔十几秒 `opencli <site> read -f json` → 适配器把图渲染成 `Image: <url>` 文本行 →
解析该行 → 下载 URL → base64。实测从提交到出图约 **40~150 秒**。

### 三个坑（都踩过）

1. **Windows 上 subprocess 跑不了 `.CMD`**：`opencli` 是 npm 生成的 `opencli.CMD`，
   Python 3.12 的 subprocess 先把程序名解析成 `.CMD` 再交给 `CreateProcess`，
   而 CreateProcess 不能直接执行 `.CMD` ⇒ `FileNotFoundError(WinError 2)`；
   `shutil.which` 却查得到，看着一切正常。
   修法：直接调 node 入口 `node <pkg>/dist/src/main.js`（npm shim 本质就是它），
   argv 由 Python 逐个传、不经 shell 解析；退路 `cmd.exe /c`（但长参数会被 cmd 再解析，长 JS 场景必须走 node）。
2. **即梦的适配器会「假超时」**：`opencli jimeng generate` 靠
   `img[src*="dreamina-sign"], img[src*="tb4s082cfz"]` 的**数量变化**判断出图，
   页面是懒加载画廊时数量不变 ⇒ 一直 `timeout`，**但图其实生成了**
   （页面历史里确实多出 3 张同提示词的图）。它的超时旋钮 `--timeout` 不存在，
   只有环境变量 `OPENCLI_BROWSER_COMMAND_TIMEOUT`；且 `opencli browser eval` 的
   CDP `Runtime.evaluate` 上限约 **115s**，所以要拆成「页内只提交 + 外部轮询」。
3. **即梦的生成按钮别点错**：真按钮是 32×32 圆形图标按钮
   （`button[data-generator-submit-available="true"]` / `.lv-btn-shape-circle`）；
   只按 `lv-btn-primary` 匹配会命中抽屉里的「复制链接」「立即抢购」⇒ 点错、页面当然不生成。

## 四、即梦 CLI（jimeng-free-api）—— 可靠解法，缺一个凭据

`D:\项目\ai-hub\jimeng-free-api` v1.2.8：**OpenAI 兼容**、端口 8000、
自建账号池 + 每日赠送积分自动领取（`credit_receive`）、积分不足自动降分辨率重试。

| 模型 | 单张积分 |
|---|---|
| `jimeng-image-3.1` / `3.0` | 1 |
| `jimeng-image-5.0-lite` | 3 |
| `jimeng-image-4.7` / `4.6` / `4.5` / `4.1` / `4.0` | 4 |
| `jimeng-image-5.0-pro` | 8 |

**卡点**：要即梦的 `sessionid`（httpOnly cookie，`document.cookie` 读不到，
Chrome 侧是 app-bound 加密，脚本解不了）。需要郭老师手动取一次：
F12 → Application → Cookies → `sessionid` → 复制值。
拿到后：`Authorization: Bearer <sessionid>`（多账号用英文逗号分隔，服务自动轮询）。

### 4.1 但网页版即梦也打通了（2026-10-20 晚，推荐先用这条）

不依赖 sessionid，走 `image-pseudo-api` 的 `jimeng-5.0`（browser-eval 驱动）。**关键三坑**：

1. **必须先把模型切到免费档**。账号「不羡仙 免费 永久 **积分 40**」的默认模型是
   **Seedream 5.0 Pro**（8~11 积分/张，疑似会员档）⇒ 点生成不生效，页面只弹
   「会员兑换/订阅管理」。历史里成功生成的 3 张恰好是 **5.0 Lite / 4.5 / 4.6**（免费档）。
   模型选择器是 `lv-select` 下拉（当前值在 `.lv-select-view-value`），面板**动态渲染**，
   第一次点开可能还没出选项 ⇒ 要重试并**回读校验**。
2. **出图检测不能靠 DOM 计数**。官方 `opencli jimeng generate` 靠
   `img[src*="dreamina-sign"], img[src*="tb4s082cfz"]` 的数量变化判断，
   懒加载画廊时数量不变 ⇒ 一直 `timeout`，**但图其实生成了**。
   改法：记录**主区**（排除右侧资产抽屉 x>1500）的结果图数量，提交后轮询增量。
3. **输入框有俩**：`div.tiptap.ProseMirror` 一个 912x76（旧的）一个 912x24（活动），
   叠在同一位置 ⇒ 写 `editors[0]`（官方适配器也写它，它确实能出图）。

实测：经 `:3100` 网关（`model=imgpseudo/jimeng-5.0`）出图成功，
主区结果图 19 → 23，命中 4 张，74.5s，输出 b64。

## 五、AGNES 那个 502 的修法（已落代码）

`api_gateway.py` 的 `_handle_images` 原来用**裸 `urllib.request.urlopen`**，
既不吃渠道配置的 proxy，也不走「直连不通自动回退代理」的自适应链路
⇒ AGNES（`apihub.agnes-ai.com` 直连 TCP 超时，走 7890 代理 200）恒定 502。
已改成 `channels._urlopen(req, timeout=300, channel_id=cid)`。

## 关联

- 伪 API（已撤独立服务）：`D:\项目\ai-hub\buddy2api\src\providers\webimage\{image_web.py,chat.py}`
- 登记脚本：`D:\项目\ai-hub\search_gateway\scripts\wire_imgpseudo_channel.py`
- 即梦服务：`D:\项目\ai-hub\jimeng-free-api`（API.md 有完整接口与积分说明）
- 计划任务：`ImagePseudoAPI`（开机自启，:8010）
