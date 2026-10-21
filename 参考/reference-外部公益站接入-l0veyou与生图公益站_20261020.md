---
name: reference-外部公益站接入-l0veyou与生图公益站
description: 2026-10-20 从 linux.do 找到并接入的两个外部公益站（l0veyou 文本可用/生图不开放；生图公益站 key 有效但余额 0 需兑换），附「自己拿 key」的两条技术路径与安全约定。
type: reference
updated: 2026-10-20
kind: reference
status: active
---

# 外部公益站接入（2026-10-20 下午）

配套：`reference-外部免费渠道-linuxtodo与公益站_20261020.md`（侦察过程与风控规律）、
`AGENTS.md` §12（拿 key 自己来，不要甩给用户）。

## 一、l0veyou.com（linux.do/t/topic/2910500，981 回复）

| 项 | 结论 |
|---|---|
| 接口 | `https://l0veyou.com/v1`，**OpenAI 兼容**；直连超时，**走 7890 代理**才通 |
| key | 已在 :3100 注册为自定义渠道 `l0veyou`（free 组）——**key 本身不写进记忆仓（公开仓库），存在 `search_gateway/data/channels.json`** |
| 文本模型 | `muse-spark-1.3`（100 万上下文、不限额度）、`deepseek/deepseek-v4.1-flash` |
| **生图** | ❌ **本账号所有分组都不开放**：`403 {"error":{"message":"Image generation is not enabled for this group"}}`（`gpt-image-2-5-flare` / `gpt-image-2-5-full` 都试过）。站上有生图模型，但**要付费组** |
| 实测 | 路由通、鉴权过，请求确实到了上游；上游当时 **503 overloaded**，3100 的「限流保护（95% 提前切换）」自动降级跳过 ⇒ 这是上游容量问题，不是接线问题 |
| 接入方式 | :3100 新增路由 `l0veyou`（members: muse-spark-1.3 → deepseek/deepseek-v4.1-flash）。**它是 3100 的渠道，不要加进 8787 的 selected_models**（DSH 指向 8787，加了会变幽灵条目） |

## 二、生图公益站 ai.loveyy.qzz.io（公益站列表贴里专列一条）

| 项 | 结论 |
|---|---|
| 接口 | `https://ai.loveyy.qzz.io/v1`（**不带 `/ldc`**——带 /ldc 只会返回前端 HTML），New API 平台，OpenAI 兼容 |
| key | 已在 :3100 注册为自定义渠道 `loveyy`（default 组、额度 Unlimited）——**key 存在 channels.json，不进记忆仓** |
| 模型 | `gpt-image-2.5`、`gpt-image-2.5-sunburst`（`/v1/models` 实测返回这两个） |
| **卡点** | **账号余额 $0** ⇒ `403 {"error":{"message":"Insufficient user quota, remaining quota: $0.000000"}}`。路由完全通，只差额度 |
| 领额度 | Wallet 页（`/console/topup` → `/wallet`）有「**HAVE A CODE? Redeem**」兑换码输入框，支付方式含「Linux Do Credit（LDC）」 |
| 接入方式 | 已挂进 :3100 的 `image-gen` 链（AGNES 之后、网页版伪 API 之前） |

## 三、「自己拿 key」的两条技术路径（AGENTS.md §12 的落地）

1. **从「Use API Key / Use Key」弹窗里抠**：New API 系站点的该弹窗会给出 **Codex CLI / OpenCode 的配置片段**，
   里面是**完整 key**（表格里显示的是打码的 `sk-472...6ec0`）。
   l0veyou 就是这么拿到的：`opencli browser default eval` 读 `pre/code/textarea` 里的 `sk-` 串。
2. **从站点自己的 API 取 body**：`opencli browser default network --detail "<key>"` 拿完整响应。
   生图公益站的 key 就是这么拿的：`POST /api/token/1808/key` → `{"data":{"key":"20Qg…"}}`（key id 在 URL 里）。
   —— 表格里的打码是**前端做的**，接口返回的是完整的。

**建 key 的表单坑**：按钮名可能不是「Create」而是「**Save changes**」（生图公益站就是），
且弹窗里的按钮要用 `document.querySelector('[role=dialog]')` **限定在弹窗内**找，
否则会点到弹窗后面那个同名触发器（我就先点了触发器，白跑一趟）。

**自定义 key**：l0veyou 的建 key 弹窗有「Custom Key」开关，打开后可以自己指定 key
（限字母数字下划线连字符、≥16 位）——比从打码里抠更省事。

## 四、别把 key 写进会被提交的地方

- `search_gateway/data/` 整个目录**在 .gitignore 里**（`git ls-files search_gateway/data/` = 0 个文件），
  所以 `channels.json` 里的 key 不会进仓库 ✅
- 记忆仓 `D:\记忆` 是**公开镜像**（推 yongtai-memory）⇒ **key 一律不进记忆仓**，
  记忆里只写「key 存在哪个文件、哪个渠道、什么权限」。

## 关联

- 注册脚本：`search_gateway/scripts/wire_external_stations.py`
- 拿 key 侦察脚本：`buddy2api/scripts/find_linuxdo_redeem_code.py`、`read_linuxdo_topics.py`
