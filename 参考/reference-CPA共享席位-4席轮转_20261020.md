---
name: reference-CPA共享席位-4席轮转
description: linux.do 楼主分享的 48Team 共享席位 relay（cpa-relay，82 模型含 9 个生图），4 个独立席位各有 5 小时滚动窗口与撞墙重置卡；接进 :3100 的做法与实测状态。
type: reference
updated: 2026-10-20
kind: reference
status: active
---

# CPA relay：4 个共享席位，82 个模型，含 9 个生图（2026-10-20）

来源：linux.do/t/topic/3047955 —— 楼主「都是自己的手工号，不打算续费了也不想卖号…所以直接分享出来」。

## 一、是什么

- base：`https://cpa-relay.ming212duo.workers.dev/v1`（OpenAI 兼容；**直连 7890 代理**才通）
- **4 把 key 写在帖子里（base64 编码，帖里说「Base64解码一下」）**，
  解出来分别是 `sk-teamA1-…` / `sk-teamA2-…` / `sk-teamB1-…` / `sk-teamB2-…`
  ⇒ **key 本身不写进本仓**（公开镜像），存在 `search_gateway/data/channels.json`。
- **82 个模型**，含顶级文本与**9 个生图**：
  - 生图：`gpt-image-2.5` / `gpt-image-2.5-flare` / `gpt-image-2.5-sunburst` /
    `gpt-image-2` / `gpt-image-1.5` / `grok-imagine-image` / `grok-imagine-image-2.0` /
    `grok-imagine-image-quality` / `gemini-3.1-flash-image`
  - 文本：`gpt-6-astra` / `gpt-6.1` / `gpt-6-sol` / `gpt-6-luna` / `gpt-5.6-terra` /
    `claude-opus-4-6-thinking` / `claude-sonnet-4-6` / `grok-4.20-0309-reasoning` /
    `gemini-3.8-flash-high` / `kimi-k3` / `qwen3.8-max` / `minimax-m3` / `muse-spark-1.3-contributor` …
  - 还有视频（grok-imagine-video 系）、TTS（grok-tts、grok-voice-tts-1.0）
- 配套 GitHub：`212duo/cpa-plugin-carpool`（CLIProxyAPI 拼车管家插件）

## 二、4 个席位 = 4 份独立额度（关键）

每个席位有**自己独立的** 5 小时滚动窗口 + 周窗口，互不影响；所以
**4 席轮转 ≈ 单席的 4 倍可用性**。查询与重置：

```
GET https://cpa-relay.ming212duo.workers.dev/api/status?key=<key>
→ {seat_name, provider, upstream_usage.rate_limit.primary_window{used_percent,
   reset_after_seconds, reset_at}, secondary_window{...}, credits_available,
   local_calls, input_tokens, ...}
```
网页版 portal：`https://cpa-relay.ming212duo.workers.dev/portal`（输入 key 查席位 + **一键核销重置卡**）。
「撞墙重置卡」= 写码撞 429 时可立刻消耗一张官方重置卡复活（每席 0~2 张，credits_available=0 就是没有）。

**2026-10-20 16:20 实测状态**：4 席的 5h 窗口**全部 100% 用满**，约 4 小时后陆续复位；
周窗口都只用了 16%；池子当天已被调用 **3005 次**（438/655/1057/855）⇒ 掉得很快，别当主通道。

## 三、接进 :3100 的做法（已落地）

- 4 个自定义渠道：`cpa-a1` / `cpa-a2` / `cpa-b1` / `cpa-b2`，各写一把 key
  （脚本 `search_gateway/scripts/wire_cpa_seats.py`）。
- 两条**编排路由**，members 就是回落链（某席冷却自动换下一席）：
  - `cpa` → 4 席 × `gpt-6-luna`（文本）
  - `cpa-image` → 4 席 × `gpt-image-2.5-flare`（生图）
- **api_gateway.py 的 `_handle_images` 已泛化**：任何**编排路由名**都能当生图模型调
  （原来只认 `image-gen` 一个别名）。
- ⚠️ 共享席位消耗快 ⇒ **不插进 image-gen 的自动回落链**（那留给稳定的商汤/Cloudflare/AGNES），
  只做点名/路由，避免自动去烧别人的额度。

## 四、坑

- 帖子里 4 把 key 是 **base64**，直接正则 `sk-` 抓不到；
- 席位名与 key 前缀**不是一一顺延**（A1/A2 交错），按 key 前缀命名才不乱；
- 席位状态只有 `GET /api/status?key=` 才查得到（表格/门户都只显示打码 key）；
- 席位冷却时上游报 **`auth_unavailable: carpool: your dedicated seat (X) is currently in cooldown`**，
  不是 429 —— 看到这条就是"这个席位在冷却，等窗口复位或用重置卡"。

## 关联

- `reference-外部公益站接入-l0veyou与生图公益站_20261020.md`（另外两个已接的公益站）
- `reference-linuxdo福利羊毛清单-20261020.md`（全部羊毛清单）
- 脚本：`search_gateway/scripts/wire_cpa_seats.py`
