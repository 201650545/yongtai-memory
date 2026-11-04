---
name: workflow_事件驱动中台契约与调度规范
description: 面向单机自动化任务舰队的轻量级事件中台契约规范：定义7个核心事件字段、指纹判重算法(sha256桶)、when表达式引擎与真实规则表样例。
type: workflow
updated: 2026-11-04
kind: rule
status: active
scope: 自动化/事件中台/计划任务/调度
---

# 事件驱动中台契约与调度规范（v0.1）

> **定位**：面向本地自动化任务舰队（计划任务、巡检、备份、抓取）的轻量级事件中台规范。
> **核心哲学**：不搞多机器复杂长轮询与重量级容器，采用“本地脚本写盘 + 助理开工读收件箱 + 规则表分流（挑人 vs 记流水）”。

---

## 一、七个核心事件字段

| 字段 | 类型 | 为什么要有 | 约束 |
|---|---|---|---|
| `id` | string | 事件唯一号（`evt-YYYYMMDD-HHMMSS-短指纹`）。写盘顺序、人工回指、日志排查核心索引。 | 必填 |
| `source` | string | 产生源（= 计划任务名或脚本名，必须与 `Get-ScheduledTask` 一字不差）。规则表靠它匹配。 | 必填 |
| `type` | string | 事件类别，点分层（如 `backup.daily.completed` / `patrol.drift.found`）。同一 source 可产出多种 type。 | 必填 |
| `object` | string | 作用对象（备份包名、笔记批次、巡检范围）。用于去重与“同一对象避免重复告警”。 | 必填 |
| `summary` | string | 一句话人话（≤40 字），**只给人看**，让助理会话不读完整 payload 即可快速决策。 | 必填 |
| `link` | string | 回溯物理链：日志文件、receipt JSON 或回执绝对路径（`file:///` 或盘符路径）。一步跳回现场。 | 必填 |
| `fingerprint` | string | 判重指纹（哈希计算）。同一件事被重复写入时用于幂等合并。 | 必填 |
| `time` | string | 事件发生时间（ISO-8601 带时区）。去重窗口、TTL 与每日汇总真源基准。 | 必填 |
| `payload` | object | 业务数据（退出码、体积、条数、失败项…）。规则与人均可读取，保持与脚本输出一致。 | 可选（建议带 exitCode） |

---

## 二、判重指纹算法（sha256 业务桶机制）

```python
fingerprint = sha256( f"{source}|{type}|{object}|{bucket}" )[0:16]
```

- **`bucket`（业务时间桶）**：避免精确到秒导致重跑无法去重：
  - **日任务**：`YYYY-MM-DD`
  - **周任务**：`YYYY-Www`
  - **即时告警**：`YYYY-MM-DDTHH`（1 小时桶）
- **判重流转**：
  1. 写入前检索在 `ttl` 去重窗口内的同 `fingerprint` 事件；
  2. **已存在**：不新建文件，累加已有事件的 `payload.seenCount += 1` 并刷新 `payload.lastSeenAt`；
  3. **不存在**：新建事件卡落盘。

---

## 三、`when` 规则表达式与调度引擎

条件表达式遵循极简子集，**可读性优先，杜绝复杂正则与动态函数**：
- **语法支持**：`==`、`!=`、`in [...]`、`>`、`<`、`and`、`or` 与小括号。
- **上下文取值**：`source`、`type` 直接取；业务指标一律走 `payload.xxx`（点路径）。
- **字符串与数组**：单引号 `'string'`，数组 `in ['itemA', 'itemB']`。

### 执行侧状态机
```python
for rule in rules:
    if eval_when(rule.when, event):
        if dedupe_hit(event.fingerprint, rule.dedupe.window):
            increment_seen_count(event.fingerprint)
        else:
            dispatch(to=rule.to, cwd=rule.cwd, skill=rule.skill, ttl=rule.ttl)
        break  # 命中首条即停（从上到下优先级）
```

---

## 四、本地架构对比（卡兹克方案 vs 本地现实版）

| 维 度 | 外部重型方案 | 本地单机现实版 | 收益与取舍 |
|---|---|---|---|
| **接单机制** | 中台常驻 + Agent 机器长轮询 50 秒 | **本地脚本直接写盘 + 会话开工扫目录** | 零网络端口暴露，无长轮询消耗 |
| **隔离沙箱** | 每任务启动新虚拟机，跑完销毁 | **同环境脚本按 `cwd` 切工作目录** | 均为本地白名单脚本，零启动延迟 |
| **基础设施** | 双 Mac mini + 云端中台 | **Windows 计划任务 + 结构化目录** | 零新增软件与服务，纯原生体系 |
| **路由去向** | 复杂多 Agent 路由池 | **`assistant_session`（挑人）/ `ledger`（记流水）** | 人机边界极简，注意力不被稀释 |
| **回溯机制** | 事件库跳转会话 ID | **`link` 直接关联日志/Receipt 绝对路径** | 文件不受会话清理影响，永久可溯 |

---

## 五、完整规则表参考配置（rules.json 样例）

```json
{
  "schemaVersion": "0.1",
  "toCatalog": {
    "assistant_session": "助理会话（挑人告警，必须由人处理）",
    "ledger": "流水账（自动归档，不打扰人）"
  },
  "rules": [
    {
      "id": "R1-Backup-Failure",
      "when": "source in ['Work_Backup_PackDaily', 'Work_Backup_PackWeekly'] and (payload.exitCode != 0 or payload.failedItems > 0 or payload.ok == false)",
      "to": "assistant_session",
      "cwd": "D:\\Work\\备份与安检\\备份",
      "skill": "backup_alert",
      "parallel": false,
      "dedupe": { "key": "fingerprint", "window": "12h" },
      "ttl": "30d",
      "note": "备份失败关乎数据安全，必须推送至会话；12h 窗口防刷屏。"
    },
    {
      "id": "R2-Backup-Success",
      "when": "source in ['Work_Backup_PackDaily', 'Work_Backup_PackWeekly'] and payload.exitCode == 0 and payload.failedItems == 0 and payload.ok == true",
      "to": "ledger",
      "cwd": "D:\\记忆\\轮次记录",
      "skill": null,
      "parallel": true,
      "dedupe": { "key": "fingerprint", "window": "1d" },
      "ttl": "7d",
      "note": "成功仅记流水，不占用注意力。"
    },
    {
      "id": "R3-AIHOT-New",
      "when": "source in ['AIHOTHotSnapshot', 'AIHOTDailyInsights'] and payload.exitCode == 0 and payload.newEntries > 0",
      "to": "assistant_session",
      "cwd": "D:\\Work\\元智能\\20_自适应工作流引擎",
      "skill": "aihot_digest",
      "parallel": false,
      "dedupe": { "key": "fingerprint", "window": "1d" },
      "ttl": "14d",
      "note": "抓取有新条目才汇总推人，同一天合并处理。"
    },
    {
      "id": "R4-Patrol-Drift",
      "when": "source == 'MetaIntelligence_Workflow_Patrol' and (payload.exitCode != 0 or payload.driftCount > 0 or payload.status != 'clean')",
      "to": "assistant_session",
      "cwd": "D:\\Work\\元智能",
      "skill": "patrol_triage",
      "parallel": false,
      "dedupe": { "key": "fingerprint", "window": "6h" },
      "ttl": "3d",
      "note": "巡检漂移异常立即推人，防止任务舰队暗中停摆。"
    }
  ],
  "defaults": {
    "parallel": false,
    "dedupe": { "key": "fingerprint", "window": "1d" },
    "ttl": "7d"
  }
}
```

---

## 六、典型事件数据实例（event.json 样例）

```json
{
  "id": "evt-20261104-010109-7b147371",
  "source": "Work_Backup_PackDaily",
  "type": "backup.daily.completed",
  "object": "pack-2026-11-04",
  "summary": "每日备份成功：2/2 上传，66.25MB，0 失败",
  "link": "D:\\Work\\备份与安检\\备份\\logs\\backup-receipt-2026-11-04-010109.json",
  "fingerprint": "7b147371a99bb837",
  "time": "2026-11-04T01:01:09+08:00",
  "payload": {
    "exitCode": 0,
    "ok": true,
    "weekly": false,
    "totalMb": 66.25,
    "uploaded": 2,
    "failedItems": 0,
    "archived": 2,
    "items": [
      { "tag": "A-记忆", "ok": true, "secs": 42.3, "mb": 66.2 },
      { "tag": "B-规范索引", "ok": true, "secs": 4.4, "mb": 0.05 }
    ],
    "seenCount": 1
  }
}
```
