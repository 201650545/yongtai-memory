---
name: reference-MiniMaxMPlan档位额度与并发口径
description: 郭老师的 MiniMax M Plan（订阅制）档位与额度真源口径：**官方没有"固定并发数"这个指标**，限流模型＝5 小时窗口 + 周窗口额度池 + RPM/TPM + 高峰动态限流；自查命令 `mmx quota show`；2026-10-20 实测当前档位 Explore（有效期至 2026-11-18），5 小时窗口与周窗口剩余均 99%。附非交互环境下 mmx 设备码登录的可用参数。
metadata:
  node_type: memory
  type: reference
  created: 2026-10-20
  modified: 2026-10-20
  实测方式: mmx-cli 1.0.28 OAuth 设备码登录 + 官方 /v1/token_plan/remains 接口实调
type: reference
updated: 2026-10-20
---

# MiniMax M Plan：档位、额度、并发口径（2026-10-20 实测）

## 一、结论先说：没有"固定并发数"

- 官方 M Plan **从不公布并发数**。唯一可用的套餐接口
  `GET https://api.minimaxi.com/v1/token_plan/remains`（等价 `/v1/coding_plan/remains`）
  返回体**只有额度窗口字段**（`start_time` / `end_time` / `current_interval_remaining_percent` /
  `current_weekly_remaining_percent` / `current_interval_usage_count` / `current_weekly_usage_count`），
  **无任何 concurrency 字段**；`/v1/token_plan/info`、`/v1/token_plan/plan`、`/v1/coding_plan/info`、
  `/v1/subscription/info` 实测全部 **404**。
- 官方限流模型 = **5 小时窗口 + 周窗口额度池 + RPM/TPM 速率限制 + 高峰动态限流**。
  官方文档原话只有"可以降低请求频率或**并发数**"（`docs/m-plan/usage-rules`），
  意思是并发会被**动态收放**（约 1 分钟恢复），而非按档位写死。官网 M Plan pricing 页与
  `m-plan/intro` / `faq` 全文搜"并发 / concurrent" **零命中**。
- 档位与额度倍数（`docs/m-plan/intro`）：Go ¥59/月（1×）、Explore ¥199/月（3×）、Build ¥599/月（12×）；
  国际版 $22/$55/$132，1×/3×/7.5×。三档都含 M3.1 Flash 文本模型。
- 时效：**到 2026-10-25 23:59（UTC+8）**，所有订阅用户在 MiniMax Code 内用 M3.1 Flash **不限量**；
  10/26 起恢复 5 小时 + 周窗口常态规则。

## 二、郭老师当前实际状态（2026-10-20 01:0x 实测，source: `mmx quota show`）

- 档位：**Explore**，有效期至 **2026-11-18**（来自 OAuth 返回的 `notification_message`）
- 5 小时窗口剩余 **99%**，周窗口剩余 **99%**，额度池名 `general`（文本/图像/音频共用一份）
- 调用链：`~/.minimax/config.yaml` → `minimaxModelSource: token_plan`，
  baseURL `https://agent.minimaxi.com/mavis/api/v1/llm/v1`（订阅通道，非按量 Key）

## 三、自查命令

```bash
npm install -g mmx-cli     # 官方指定安装方式
mmx auth login             # 需交互终端（浏览器设备码授权）
mmx quota show             # 打印档位/窗口水位
mmx auth status            # 认证状态
```

凭据落 `C:\Users\郭永涛\.mmx\config.json`（`{oauth:{access_token,refresh_token,expires_at,region,resource_url}, region}`）。

## 四、非交互（Agent/脚本）环境登录设备码流

`mmx auth login` 在无 TTY 时直接报 `--api-key is required in non-interactive mode.`，
需自行复刻设备码流（参数取自 `mmx-cli` 包内 `dist/mmx.mjs`）：

1. `POST https://account.minimaxi.com/oauth2/device/code`，表单
   `client_id=659cf4c1-615c-45f6-a5f6-4bf15eb476e5`、`scope=openid profile coding_plan`、
   `code_challenge=base64url(sha256(verifier))`、`code_challenge_method=S256`、`state=base64url(16B)`
2. 授权页 `https://platform.minimaxi.com/oauth-authorize?user_code=<user_code>&client=MiniMax+CLI`
3. `POST https://account.minimaxi.com/oauth2/token`，表单
   `grant_type=urn:ietf:params:oauth:grant-type:device_code`、`client_id`、`user_code`、`code_verifier`
4. 续期：`grant_type=refresh_token` + `refresh_token` + `client_id`

三个易踩的坑（详见 Work 侧 L1 经验条目）：
① 设备码响应的 `expired_in` 是**绝对毫秒时间戳**（官方 CLI 源码混用秒/毫秒，本身有 bug）；
② 响应**没有 `device_code` 字段**，只有 `user_code`；
③ 脚本 print 必须 `flush()`，否则轮询日志全被缓冲、看起来像卡死。
