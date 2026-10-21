---
name: reference-lobster-daily-checkin-fix-20261020
description: 有道龙虾（LobsterAI）每日 100 积分签到长期失败的根因与修复：上游 actions 是字符串数组而非对象数组，旧解析恒定取不到 actionId；同时证伪「启动客户端会触发登录奖励」。改的是 buddy2api 的 lobster provider。
type: reference
updated: 2026-10-20
kind: reference
status: active
---

# LobsterAI 每日签到修复（2026-10-20）

> 起因：郭老师问「积分每日领取有没有做」。查下来**从没真领到过**——累计只有 2 天 / 200 分，理论上早该是 100 分/天。

## 一、症状

- 计划任务 `Buddy2API_DailyAutoClaim`（每天 01:25）每天都跑，`LastTaskResult=0`。
- 日志里 lobster 那一行固定是：`lobster / 190****0185 -> 动作列表里没有 actionId`。
- 但汇总行写的是「每日自动领取结束：**3/3 项正常**」——失败被算成了正常。
- 积分长期停在 1343.23，跨天不动。

## 二、两个根因（叠加）

### 根因 A：字段结构猜错（决定性）

`src/providers/lobster/checkin.py` 按**对象**取 actionId：

```python
for item in actions:
    if isinstance(item, dict):
        aid = str(item.get("actionId") or item.get("id") or "")
```

而上游 `GET /api/client-activities/{activityCode}/context?configRevision=N` 实际返回：

```json
"actions": ["check_in"]
```

是**字符串数组**，字符串本身就是 actionId。⇒ 永远取不到 ⇒ 每天恒定失败。
（该字段结构是 2026-10-18 从客户端 app.asar 逆向时"看起来像"对象数组，猜错了。）

### 根因 B：成功判定是假绿

`daily_autoclaim.py` 把 `no_new_claim` 归进 `good` 集合，lobster 领取失败 → 状态落成 `no_new_claim` → 计入「正常」。
另外**失败信息在「网关签到」组内被淹没**，汇总行看不出哪个渠道真失败。

### 附带证伪：启动客户端**不会**触发登录奖励

2026-10-20 09:03 实测：启动 `LobsterAI.exe` 等 60s，积分 **1343.23 → 1343.23 不动**。
"每日登录奖励由客户端登录触发"这个假设是假的——奖励只走官方 HTTP 签到接口。

## 三、修法（commit `a93d81e`）

1. `checkin.py`：`actions` 同时兼容**字符串**与**对象**两种形态，字符串直接当 actionId。
2. `daily_autoclaim.py`：**移除**「启动 LobsterAI 客户端等积分」这条路径（实测拿不到，还每天白等 60s + 弹窗）；Lobster 改由网关 HTTP 签到一步完成。
3. 新增 `scripts/probe_lobster_checkin.py`（只读探针，打原始 JSON）与 `scripts/test_lobster_claim.py`（端到端实测）。

## 四、实测证据

| 项 | 结果 |
|---|---|
| 修复前累计 | 2 天 / 200 分，`claimedToday=false` |
| 修复后单次领取 | `1343.23 → 1443.23`（**+100.00**），`claimedDays 2 → 3` |
| 回读状态 | `claimedToday=true`，`claimedCredits=300.0`，`actions=[]`（已领后为空，与文档一致） |
| 网关 `POST /admin/accounts/checkin-all` | lobster → 「今日已领取（累计 3 天，本活动每次 100 积分）」，整体 `failed=0` |
| 网关重启 | 计划任务 `Buddy2API_Gateway` 停→起，新代码生效（pid 变 26292） |

## 五、边界与注意

- 每日奖励 **100 积分/天**，活动常驻（endAt 到 2126 年），`claimedToday=true` 时 `actions` 为空数组。
- 已领状态下 `claim()` 返回 `alreadyClaimed=True` 而非失败，属正常。
- 签到必须**重启 8787 网关**才生效（pythonw 常驻进程，模块级代码不热加载）。
- 网关本地鉴权只要求「回环 + 无 Origin」，脚本从 127.0.0.1 直连即可，无需 token。
- **仍未做**：Loomy 的打工分必须应用内真聊天才攒得出档位（脚本启动不产生），小浣熊靠启动后看账单判断是否已领——这两条是已知边界，不是 bug。

## 六、关联

- 代码：`D:\项目\ai-hub\buddy2api\src\providers\lobster\checkin.py`、`scripts\daily_autoclaim.py`
- 探针：`D:\项目\ai-hub\buddy2api\scripts\probe_lobster_checkin.py`、`scripts\test_lobster_claim.py`
- 网关：`D:\项目\ai-hub\buddy2api`（8787）；计划任务 `Buddy2API_DailyAutoClaim`（每天 01:25）
- 教训：`D:\记忆\教训\lesson_定时任务跑而不产出_占位符未替换.md`（同族：每天在跑但没产出）
- 相关项目页：`D:\记忆\项目\project_ai_hub.md`
