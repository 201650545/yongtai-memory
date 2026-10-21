---
name: reference-外部免费渠道-linuxtodo与公益站
description: 2026-10-20 在 linux.do（福利羊毛/资源荟萃）实测到的外部免费渠道清单与生图 API 站，以及 linux.do 的 Cloudflare 风控规律与正确访问姿势。
type: reference
updated: 2026-10-20
kind: reference
status: active
---

# 外部免费渠道（linux.do 实地侦察，2026-10-20 14:00~14:30）

起因：郭老师问「内部渠道就这几个了，去外面看看，Linux.do 这个站点你去读帖子，会不会有风控」。

## 一、linux.do 的风控规律（实测，不是猜）

| 现象 | 真相 | 怎么办 |
|---|---|---|
| 页面标题 **"Just a moment..."**、body 为空 | **Cloudflare Turnstile** 挑战页 | **约 36 秒自动通过**，不用人工点。等着就行 |
| `opencli linux-do search` 报 **"Response is not valid JSON"** | 挑战没过时 Discourse 返回 **HTML**，适配器按 JSON 解析就炸 | **重试一次**（挑战过后就正常） |
| 报 **"Pre-navigation to https://linux.do failed: Navigation rejected."** | 适配器要做的预导航被扩展拒了 | 先 `opencli browser default open https://linux.do/`，再调适配器 |
| 适配器命令 | `linux-do {search,feed,categories,tags,login}`（都走你的 cookie）。**没有读帖命令** —— 读帖用通用浏览器：`browser default open <topicURL>` → 等渲染 → `browser default eval` 抓 `#post-1 .cooked` | 分类页 id：`福利羊毛 = /c/welfare/36`（Lv1 = /c/welfare/welfare-lv1/60） |

⇒ **有风控但可控**：走你已登录的 Chrome（cookie 模式）、低频、每次只开 1~2 个页面即可。别高频刷。

## 二、找到的外部渠道（按可用性排序）

### 1. l0veyou.com 公益站（linux.do/t/topic/2910500，981 回复）★最对口
- **gpt-image2 生图：免费、不限次数、永久 0 ldc**（走企业付费 API 渠道）
- **muse-spark-1.3 文本 API：100 万上下文、不限额度**；deepseek-v4.1-flash 免费三天
- 接 **LINUX DO Connect** 登录，站内右上角 api 建 key
- 实测：`https://l0veyou.com/v1/models` → **401「API key is required」** ⇒ OpenAI 兼容、只差 key
- 注：直连超时，**走 7890 代理**才通

### 2. 生图公益站 `https://ai.loveyy.qzz.io/v1`（公益站列表贴里专列一条）
- 只有一个模型 **gpt-image-2.5**，可注册
- 实测 `/v1/models` → 401 Invalid token（New API 平台，OpenAI 兼容）✅
- ⚠️ **API 前缀不带 `/ldc`**（带 /ldc 只会返回前端 HTML）
- 帖里注明已接 AI 审核、不允许 nsfw

### 3. qoder 网页版：**免费用 DeepSeek V4.1-Flash 到 10.24**
- 本机 Qoder 已装（`D:\Qoder\Qoder.exe`）
- ⚠️ opencli 的 qoder 适配器要求 Qoder **带 `--remote-debugging-port=9237 --remote-allow-origins=*` 启动**
  （win32 不支持自动拉起；报错原文「Qoder is not reachable on CDP port 9237」）
- 实测：带参数拉起后 opencli 能连、`qoder history/read` 正常；`qoder ask` 能把问题发出去（34s），
  但**回复没等到**（论坛里也说 qoder 免费 ds-flash 要排队、慢）
- ⇒ 可当**网页版免费文本模型**接（与 traework/workbuddy 同类），但慢

### 4. 其它
- **hub.linux.do #24493** 国模免费（站内 AI 开发平台）
- **LV中转 lvlv.lol**：新开站，注册3元 + 开业帖留言2元 + 进群5元 = 10 元额度（**要发币，不是纯白嫖**）
- **公益站列表贴**（linux.do/t/topic/2714504，20 来个站）+ 列表站 **https://ldoh.105117.xyz/**
  名单（部分）：Any Router、Ark API(windhub.cc)、『烁』、黑与白、42 API、WONG、薄荷(x666.me)、
  dudu、CoeeApi、PrismAI、zifeiyu、Hlool、小鸡毛(ark717.com)、随时跑路、胖猫、773、
  Fengwind API、咕咕嘎嘎…　类型多为「签到 / 邀请码 / LDC购买注册码」
- **已炸**：api.lhyb.dpdns.org、api2.lhyb.dpdns.org → SSL EOF
- **AIHelper**（github.com/chgblog/AIHelper）：开源桌面工具，提示词注入 + 网页脚本注入免费用各家网页版，
  新增**批量生图**（CSV 提示词 + 录制回放）——适合做批量出图工作流

## 三、还没通的（可继续挖）

- modelscope `Qwen/Qwen-Image-Edit`：提交返回 task_id，但 `/v1/tasks/{id}` 报 task not found，**取结果端点未搞清**
- gemini / openrouter 的生图模型：走 **chat/completions**（modality=image），不是 images/generations
- l0veyou / 生图公益站的 key：**需要用户去注册**（LINUX DO Connect 登录 → 建 key）

## 关联

- 侦察脚本：`buddy2api\scripts\read_linuxdo_topics.py`（读帖）、`search_gateway\scripts\scan_free_image_channels.py`（扫免费生图渠道）
- 内部侧对应：`buddy2api\src\providers\webimage\`（网页版伪 API）、`reference_生图渠道盘点与网页版伪API_20261020.md`
