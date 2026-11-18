---
name: workflow_删除计划任务必须同步清理注册表
description: 本机删除/停用计划任务不是 Unregister 一步完事——元智能有两处活注册表（40_定时任务/registry.yaml 与 20_自适应工作流引擎/contracts/ops-task-fleet.yaml）会按任务名做探针，任务没了会天天报 CONDITION_RED / level=break，把巡检拖成 FAIL。固定五步：备份→删任务→清两处注册→跑巡检验证→确认 red 数下降。2026-11-18 实证：删三个任务后 red 14→12。
type: workflow
updated: 2026-11-18
kind: fact
status: active
---

# 删除/停用计划任务：五步固定动作

## 为什么要这条

2026-11-18 踩过：删了 `FreeCandidateRefresh`、`GatewaySpeedTestDaily` 后只做了 `Unregister-ScheduledTask`，结果巡检日志天天报：

```
🔴 ops-task-fleet｜CONDITION_RED｜task_freecandidaterefresh
   level=break｜expected=存在且启用…｜actual=未找到
```

**任务删掉了，但它还挂在两处注册表里被探针盯**，于是「删干净」变成了「新增一条永久红灯」——比不删还糟。

## 五步（顺序不可乱）

### 1. 备份
```powershell
$bakDir = 'D:\临时文件夹\<任务名>_删除备份_<日期>'
New-Item -ItemType Directory -Path $bakDir -Force
Export-ScheduledTask -TaskName '<任务名>' | Out-File "$bakDir\任务定义.xml" -Encoding UTF8
Copy-Item 'D:\Work\元智能\40_定时任务\registry.yaml' "$bakDir\registry.yaml.bak"
Copy-Item 'D:\Work\元智能\20_自适应工作流引擎\contracts\ops-task-fleet.yaml' "$bakDir\ops-task-fleet.yaml.bak"
```

### 2. 删任务
```powershell
Unregister-ScheduledTask -TaskName '<任务名>' -Confirm:$false
```
只想停不想删则用 `Disable-ScheduledTask`；但**注意** `allow_disabled: false` 的条目停用照样报红，也必须清注册。

### 3. 清两处注册（关键，最易漏）

| 文件 | 登记形态 | 条目长什么样 |
|---|---|---|
| `D:\Work\元智能\40_定时任务\registry.yaml` | `- name: <任务名>` 在 `tasks:` 列表下 | 带 `at:` / `cadence:` / `executor:` / `probe: scheduled_task` |
| `D:\Work\元智能\20_自适应工作流引擎\contracts\ops-task-fleet.yaml` | `task_<任务名全小写>:` 在契约下 | 带 `probe: scheduled_task` / `task_name:` / `artifact_assertions:` |

条目结束边界＝下一个同级 key 之前（含前导空行）。删完**必须**做 YAML 合法性验证：
```powershell
python -c "import yaml; yaml.safe_load(open(r'<路径>',encoding='utf-8')); print('OK')"
```

### 4. 跑巡检验证
```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\Work\元智能\runners\patrol-daily.ps1'
```
**只看最后一次巡检段**（日志是累加的，历史段里仍会有已删任务名，别误判）：
```powershell
$content = Get-Content $log -Encoding UTF8
$lastStart = 0
for($i=0;$i -lt $content.Count;$i++){ if($content[$i] -match '巡检开始'){ $lastStart = $i } }
$content[$lastStart..($content.Count-1)]
```

### 5. 确认 red 数下降
看 `GATE|PATROL|` 行的 `red=` / `condition_red=` 有没有变小。没变小说明还有别的问题，不是这次删除的锅。

## 实证记录（2026-11-18）

删了三个：`GatewaySpeedTestDaily`（测速）、`FreeCandidateRefresh`（免费候选，已坏）、`AutoSeatOrchestrate`（编排器，18 天 HALT 自我锁死）。

- 前两个只删任务 → 巡检报 `task_freecandidaterefresh: 未找到`、`task_gatewayspeedtestdaily: break`
- 补齐两处注册后 → **最后一次巡检不再出现任何已删任务**，`red 14→12`、`condition_red 13→11`

## ⚠️ 别被误导的两点

1. **`capability-*.json` / `heartbeat-status.json` / `ops-task-fleet.runtime.json` 里的同名记录不用改** —— 那些是历史运行快照，不是活配置。判据：文件里带日期戳的是历史，带 `probe:`/`executor:` 的是活配置。
2. **日志里出现的已删任务名是正常的** —— 巡检日志累加写，历史段不会自己消失。只核最后一次。

## 🔴 漏检陷阱：任务名带下划线/数字后缀时搜不到（2026-11-18 实踩）

`Work_DailyReport_0800` 删除时，我搜 `DailyReport|daily_report` 报「无残留」，删完跑巡检却仍然红：

```
🔴 task_work_dailyreport_0800：actual=未找到｜任务计划程序里找不到名为「Work_DailyReport_0800」的任务
```

**原因**：`Select-String -Pattern 'xxx' -SimpleMatch` 在 PowerShell 里对含下划线的模式会漏匹配（`-SimpleMatch` 与 `-Pattern` 组合行为不一致）。

**正确做法：用逐行正则扫，不要依赖 Select-String + SimpleMatch：**
```powershell
$c = Get-Content 'D:\Work\元智能\40_定时任务\registry.yaml' -Encoding UTF8
for($i=0;$i -lt $c.Count;$i++){
  if($c[$i] -match '<任务名或其小写形式>'){ 'L{0}: {1}' -f ($i+1), $c[$i] }
}
```

**并且必须搜四种形态**：原名 `Work_DailyReport_0800`、小写 `work_dailyreport_0800`（fleet 契约惯用）、去后缀 `Work_DailyReport`、全小写去后缀 `work_dailyreport`。

**另一种漏检**：删了条目后**注释里还留着任务名**（如 `# 例外：GatewaySpeedTestDaily 用 ...`）。注释不影响探针，但会误导后来的人以为任务还在——顺手改成「原 X 条目已于 YYYY-MM-DD 删除」。

## 最终验证标准（必做）

跑 `patrol-daily.ps1` 后，取**最后一段**巡检，确认：
- `已删任务名` 在段内 **0 次命中**
- `GATE|PATROL|` 行的 `red=` **数值下降**

2026-11-18 实绩：删 4 个任务（`GatewaySpeedTestDaily` / `FreeCandidateRefresh` / `AutoSeatOrchestrate` / `Work_DailyReport_0800`），`red 14 → 11`、`condition_red 13 → 10`，4 个任务名全部不再出现。

## 相关

- 巡检本体：`D:\Work\元智能\runners\patrol-daily.ps1`
- 任务舰队巡检 skill：`ops-task-fleet-watch`
- 撤任务前的四步（查影响面）：[[反馈/feedback-讲黑箱系统时一次只讲一个讲透]] §C
