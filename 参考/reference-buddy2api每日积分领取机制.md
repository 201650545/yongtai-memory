---
name: reference-buddy2api每日积分领取机制
description: buddy2api(:8787) 八个渠道「每日积分能不能领」的机制与实测结论：谁走 HTTP 签到、谁靠客户端、谁根本没有领取动作；含国际版 workbuddy「活动未开启(10001)」、千问办公「0 点自动到账」、小浣熊直调接口、Loomy 只能人工，以及 DPAPI 凭证误判与汇总假绿两个坑。
type: reference
updated: 2026-10-21
kind: reference
status: active
---

# buddy2api 每日积分领取：机制与实测结论（2026-10-21）

> 起因：郭老师问「buddy 网关每个渠道的积分是不是都能正常领取」。
> 答：8 个渠道里**能自动领的只有 3 个**，其余各有各的硬约束 —— 下面逐条给机制和证据。

## 一、结论总表（2026-10-21 实测，非推测）

| 渠道 | 能不能每天领 | 机制 | 证据 |
|---|---|---|---|
| **workbuddy 国内版**（郭老师） | ✅ 每天 +100，streak 20 天 | 网关 HTTP 签到 `POST /v2/billing/meter/daily-checkin` | `today_checked_in=true, today_credit=100` |
| **traework** | ✅ 每天 +100 | 同上 | `today_checked_in=true, today_credit=100` |
| **lobster** | ✅ +100（修好后首次成功，streak 4 天） | 网关 HTTP 签到（`/api/client-activities/.../actions/{actionId}`） | 「签到成功，+100」，余额 1443.23→1543.22 |
| **raccoon 商汤小浣熊** | ✅ 每天 +300 | **直调客户端那个接口**（原为「拉 GUI → 等 90s → 杀 12 进程」） | `POST https://xiaohuanxiong.com/api/web/desktop/v1/login/points/grant` → `{"code":0,"data":{"granted":false}}`（false=今天已领过） |
| **workbuddy 国际版 ×5** | ❌ **上游活动没开** | 接口**有**，但活动关着 | `{"code":10001,"msg":"签到活动未开启或已过期"}` |
| **qwenwork 千问办公** | ⚪ **不需要"领"** | 每日赠分**0 点自动到账**，客户端只弹通知 | 客户端文案「今日已获得 {{credits}} 免费积分 / 每日 0 点刷新」；上游 `account-context` 只有 user/plan/quota |
| **qoder 国际版** | ❌ 无此机制 | asar 里**没有**任何签到/每日赠送接口 | 扫 150MB app.asar，`checkin` 命中全是 `baseAssignIn` 之类误报 |
| **loomy 讯飞** | ❌ **只能人工** | 唯一领奖入口是 `recordValidTurn()`＝「在应用里真的聊天」 | 连续 4 天「启动也拿不到」，日额度由服务端按业务日自动重置（不靠启动） |
| workbuddy-intl | — | 0 个账号 | `accounts: 0` |

## 二、国际版 WorkBuddy：接口有，但上游活动没开

客户端 `D:\workbuddy internet\WorkBuddyAI\resources\app.asar` → `/main/account.js`：

- `POST /billing/meter/checkin-status` ← **注意不带 `/v2`**
- `POST /billing/meter/daily-checkin`
- 另有邀请码 `/activity/workbuddy/invitation/v2/my-code`

返回字段与国内版**完全一致**：`today_checked_in` / `streak_days` / `today_credit` /
`is_streak_day` / `next_streak_day` / `streak_bonus_days` / `streak_bonus_credit` / `checkin_dates`。

但实测两条路径都返回 **code 10001「签到活动未开启或已过期」**；状态接口 `active=false` 而
`daily_credit=100` 并存 ⇒ **机制存在、当前没开**。网关每天都在探（活动一开当天就能领到），
`checkin_supported=False` 的跳过是**对的**，不是漏领。

## 三、千问办公：赠分是"系统按点送"，不是"点一下领取"

客户端 `dailyCreditNotice`（中/英/繁三语同一套文案）：

- 「今日已获得 {{credits}} 免费积分」
- 「每日 0 点刷新，升级标准版会员每日可获得 200 积分 / 高级版 300 积分」
- 埋点：`daily_credit_notice_claim_result` / `_action_clk` / `_exp`

⇒ 动作在**服务端**（0 点刷新到账），客户端只负责弹窗 + 埋点。
上游 `account-context?include=user,plan,quota` 只有 user/plan/quota，**没有签到/每日任务字段**。
（另有一处 `creditsGrowthCard.checkinFailed`＝"签到失败"，那是**活动签到**，不是每日赠分。）

## 四、两个必须记住的坑

### 坑 1：裸读 SQLite 拿 token → 必然 401（DPAPI 加密）

`accounts` 表里存的是**加密串**（`enc:v1:dpapi:`），**只有 `database.list_accounts()` /
`db.get_account()` 会解密**。拿密文当 Bearer 打上游 ⇒ 401 ⇒ 很容易误判成
「这个渠道账号已经死了」。

**正确姿势**：用项目自己的代码，别自己拼 HTTP。

```python
import sys; sys.path.insert(0, r'D:\项目\ai-hub\buddy2api\src')
import database as db
from providers.qwenwork import QwenWorkProvider, _account_context
acc = db.list_accounts(provider='qwenwork')[0]          # ← 解密后的账号
snap = asyncio.run(QwenWorkProvider().fetch_quota(acc))  # → ok=True remaining=2100
raw  = asyncio.run(_account_context(acc))               # → HTTP 200，原始字段
```

### 坑 2：批量领取会把自己打出限流，而失败原因不落日志

连续探测国际版站点后跑 `checkin-all`，5 个账号里 3 个报失败且 **message 全空**；
随后**单账号逐个复测全部恢复「不适用」** ⇒ 批量串行打同一站点会被限流。
⇒ 探测要克制；message 为空时必须补状态码（已改 `daily_autoclaim.py`）。

## 五、脚本与位置

| 东西 | 位置 |
|---|---|
| 每日领取脚本 | `D:\项目\ai-hub\buddy2api\scripts\daily_autoclaim.py`（计划任务 `Buddy2API_DailyAutoClaim`，每天 01:25） |
| 日志 | `D:\项目\ai-hub\buddy2api\logs\daily_autoclaim.log` |
| 契约自检 | `D:\项目\ai-hub\buddy2api\scripts\check_switcher_sync.py`（2026-10-21 跑：**PASS 全通**） |
| 上游历史 | `D:\记忆\参考\reference_lobster每日签到修复_20261020.md`（lobster 那个 actions 字段结构的坑） |
| L1 草稿 | `D:\Work\元智能\10_AI自成长引擎\草稿区\L1_经验\L1_20261021_buddy2api加密凭证误判与领取假绿.md` |

### 汇总口径（2026-10-21 改，原先是假绿）

原来只有「N/N 项正常」两档，把**签到失败**、**不适用**、**跳过**、以及
Loomy 那种**根本没领到**全折叠成"正常" —— 10-20 那次网关签到组明确是
「领取 2 · 已领 0 · **失败 1**」，汇总照样写「3/3 项正常」。

现在分五档如实报：
`✅ 领到 · ⭕ 今日已领 · ⚠️ 没领到 · ❌ 失败 · ⏭ 跳过/不适用`；
「没领到」结构上就领不到（需人工动作），**不算失败、不再计入正常**；
退出码只有**真失败**才非 0。
