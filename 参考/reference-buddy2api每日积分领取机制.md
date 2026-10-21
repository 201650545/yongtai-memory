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
| **workbuddy 渠道 · 国际站账号 ×5**<br>（provider=workbuddy, site=intl, 域名 `www.workbuddy.ai`）| ❌ **上游活动没开** | 接口**有**，但活动关着 | `{"code":10001,"msg":"签到活动未开启或已过期"}` |
| **qwenwork 千问办公** | ⚪ **不需要"领"** | 每日赠分**0 点自动到账**，客户端只弹通知 | 客户端文案「今日已获得 {{credits}} 免费积分 / 每日 0 点刷新」；上游 `account-context` 只有 user/plan/quota |
| **qoder 国际版** | ❌ 无此机制 | asar 里**没有**任何签到/每日赠送接口 | 扫 150MB app.asar，`checkin` 命中全是 `baseAssignIn` 之类误报 |
| **loomy 讯飞** | ❌ **只能人工** | 唯一领奖入口是 `recordValidTurn()`＝「在应用里真的聊天」 | 连续 4 天「启动也拿不到」，日额度由服务端按业务日自动重置（不靠启动） |
| workbuddy-intl | — | 0 个账号 | `accounts: 0` |

## 二、WorkBuddy 家族：三个名字，一件事（**别混**）

⚠️ 网关里 WorkBuddy 有**两个渠道 + 一个站点判据**，历史上 provider 混在一起
（`database.py:363` 注释原文：*「workbuddy-intl 复用 provider="workbuddy" + site="intl" 的链路，
日志里 provider 一律落成 workbuddy，只有 model 字段带 workbuddy-intl/ 前缀」*，
2026-10-18 才给 logs 加了 `site` 列把两站切开）：

| 名字 | 是什么 | 账号 | 签到 |
| :--- | :--- | :--- | :--- |
| `workbuddy`<br>（显示名 **"WorkBuddy / CodeBuddy"**）| **真 provider**，按账号域名自动分站点 | **6 个**：1 个 `codebuddy.cn`（郭老师，**中国站 cn**）+ 5 个 `www.workbuddy.ai`（**国际站 intl**，gmail）| 中国站那个有效（每天 +100，streak 20）；5 个国际站回 10001 |
| `workbuddy-intl`<br>（显示名 **"WorkBuddy 国际版"**）| **模型前缀/标签渠道**（`workbuddy-intl/<model>`），底层复用 workbuddy provider + `site=intl`；**自身 0 账号** | 0 | 每天显示「跳过(checkin_unsupported)」—— **这条与那 5 个账号无关** |
| `site` = cn / intl | 真正的站点判据：`account_site()` 按域名（`*.workbuddy.ai` → intl，其余 → cn）| — | 日志用 `logs.site` 区分 |

⇒ **写结论时的正确叫法**：
- 那 5 个账号一律叫「**workbuddy 渠道 · 国际站账号**」（provider=workbuddy, site=intl）；
- `workbuddy-intl` 一律叫「**workbuddy-intl 标签渠道（0 账号）**」；
- ❌ 不要把两者都叫"WorkBuddy 国际版"。

**接口有，但上游活动没开**（指上面那 5 个国际站账号）：

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

## 四、Loomy：「打开它就自动领」——账本上查无实据（2026-10-21 查证）

**扫了 4286 条 `/points/records` 流水，只有 3 条是加分**：

| 时间 | 类型 | 金额 |
|---|---|---|
| 2026-09-07 | 注册奖励 | +5000 |
| 2026-09-07 | 新手任务-发送第一条消息 | +500 |
| 2026-09-16 | 新手任务-生成 PPT | +1500 |

其余 4283 条全是 **debit「模型调用扣分」**（GLM-5.3-Flash）。**没有任何"每日发放"记录。**

三件事要分清：

| 看着像"每天自动领" | 真相 |
|---|---|
| 每天那 5000 | 是 `dailyBalance` **日额度**，服务端按业务日 0 点重置、**根本不落账本**；2026-10-10 跨日实测：**启动客户端之前**读出来就已经是 5000 ⇒ **与开不开客户端无关** |
| "打开就自动领" | 那是**新手任务**机制（打开并用一下就发 500/1500），9 月已领完，不会再有 |
| 真正要"动客户端"才有 | **宠物打工档位**（`/pet-work` tiers：tier_1=60 / tier_2=100 / tier_3=150 分）。规则：`minimumActiveDays: 7`、`sessionWeight 0.4 / depthWeight 0.6`、入口是 `recordValidTurn()`＝**真的得说够话**。当前 `lastGrant: null`、`rewardedTierIds: []`、`earnedPointsToday: 0` ⇒ **一次都没发过** |

**附带发现（比宠物分值钱）**：这 4283 条扣分全是 GLM-5.3-Flash ⇒ **这个 Loomy 号是被当模型 API 在用**，每天 5000 的额度被调用吃掉（10-21 当天 4146/5000 已被吃掉 83%）。
⚠️ 但 `:3100` 的 `model_routes.json` 里 **grep 不到 loomy**（0 次命中）⇒ 消耗不是本机网关发起的，
来源待查（Loomy 客户端自身，还是有人直连它的 API）。

**结论**：把 Loomy 的"启动客户端"从 `daily_autoclaim.py` 摘掉**没有损失任何积分** ——
连续 4 天开着也拿不到（那 4 天日志就是证据）。要拿档位分只能真聊天（7 个活跃日起步），
用 computer-use 模拟 = 刷活跃度，属另议。

## 五、两个必须记住的坑

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

## 六、脚本与位置

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
