---
name: lesson-gateway-restart-privilege-trap
description: :3100 现由 nssm 服务以 LocalSystem 持有，普通权限 shell 既杀不掉也 restart 不了（Access denied）；项目 stop 脚本会静默失败却照样写 .api3100_stop 哑雷。与库内既有「重启免 UAC」条款正面冲突，2026-09-30 待郭老师裁定走哪条
metadata:
  node_type: memory
  type: 教训
  created: 2026-09-30
---

# 网关重启的权限死结（2026-09-30 实测）

## 一、事实

- 服务 `ai-gateway-3100`：`BINARY_PATH_NAME = D:\Tools\nssm\nssm.exe`，`SERVICE_START_NAME = LocalSystem`。
- ⇒ 它的 python 子进程是 **SYSTEM 进程**。实测：非管理员 shell 下
  - `nssm restart ai-gateway-3100` → 无输出/不生效（服务控制被拒）
  - `taskkill /PID <py> /F` → `Access is denied`
  - 项目自带 `services\stop_api_gateway_3100.ps1` → 打印"stopped successfully"但**进程没死**（`Stop-Process -ErrorAction SilentlyContinue` 把拒绝访问吞了）
- 更坏的：该脚本第 28 行**无论杀没杀掉都会写 `.api3100_stop`**。这个标志会让 `start_api_gateway_3100.ps1` 直接 `return`（"stop flag present - skip auto start"）＝**下次谁点启动会被静默跳过**。本轮已手动删除该标志。

## 二、与库内既有条款冲突（必须点名）

[[调度大脑记忆/项目/project_ai_gateway]] 的关键不变量写着：

> **重启免 UAC**：网关必须普通权限运行。禁止 `Start-Process -Verb RunAs` 启动 python（会变提权进程 → 下次杀它 Access denied → 恶性循环）。重启 = 普通进程 Stop + 普通进程 Start。

本轮为了让补丁生效，走的是 `Start-Process -Verb RunAs nssm.exe restart`（提权）——**正是那条警告的恶性循环形态**：执行体换成了 PID 7016（10:12:29，父进程 nssm.exe，SYSTEM 会话）。补丁因此才生效，但下一任用文档 prescribed 的普通权限 stop 照样杀不动。

规范与现实已经分叉：**只要端口被 LocalSystem 服务子进程持有，"普通权限 Stop＋普通 Start"就不可能成立**。（`project_ai_gateway.md` 那条假设的是"普通用户拉起的 python 进程"。）

## 三、待裁定（回一个字即可）

| 选项 | 动作 | 后果 |
|---|---|---|
| **A 认服务为真源** | 作废"免 UAC"条款；重启统一 `nssm restart`＋**必须提权**；stop/start ps1 改成调 nssm | 每次重启弹一次 UAC；文档与本条改写 |
| **B 认普通进程为真源**（原设计意图） | `nssm stop` ＋ `nssm set ai-gateway-3100 Start SERVICE_DEMAND_START`（或 remove），再由 `start_api_gateway_3100.ps1` 普通权限拉起 | 之后重启真免 UAC；代价：开机不自启，需靠看门狗计划任务或人工拉起 |
| **C 先不动** | 保留现状（服务持端口），本轮结论仅登记 | 下一任还会在这道墙上耗时间 |

现状未决项：A/B 都涉及共享状态（9 个项目依赖 :3100），**没点头我不再动服务配置**。

## 四、郭老师裁定（2026-10-08，口述）：**走 A —— 认服务为真源**

> 原话：「就是我让它这样搞的，我不希望它一直弹那个弹窗，好烦，而且还开机自启动。」

**判读**：服务化（nssm / LocalSystem / 开机自启）**是他有意选的**，目的就两条 —— **① 不弹控制台窗口 ② 开机自启**。所以：

- **不是待修缺陷**，是设计取舍。选项 B（改回普通进程）**明确作废** —— 它会丢掉开机自启。
- **「重启免 UAC」条款作废**：那条假设"普通用户拉起的 python 进程"，与服务化现状正面冲突，已从 `project_ai_gateway.md` 改写。
- **重启口径（新）**：改代码后重启统一走 **`nssm restart ai-gateway-3100`，需要提权**（UAC 弹一次）。
- **日常不受影响**：`data/*.json` 全部走 mtime 热加载，**改配置不需要重启**。这道墙只在"要改 `.py` 代码"时才咬人。
- 服务实况（2026-10-08 复测）：`ai-gateway-3100` 与 `web2api-3102` 均 `state=Running / start=Auto / acct=LocalSystem` ⇒ 无窗 + 自启，达标。

## 五、顺带实测：真正还在弹窗的是 `:8787`（不是 `:3100`）

- `:3100`/`:3102` 走 nssm 服务 ⇒ **无窗**，符合他的红线。
- 但 `:8787`（客户端凭据网关 / `D:\tools\Buddy2API`）由计划任务 `Buddy2API_Gateway` 拉起，动作是 **`gateway_run.bat`**（.bat 里 `pythonw server.py` 是**前台阻塞**），任务设置 `Hidden=False` + `LogonType=Interactive` ⇒ **登录时会弹一个 cmd 窗口，且窗口会一直挂着**（bat 不退出）。
- 证据：该任务 `LastRunTime=2026-10-08 07:20:49`，**`LastResult=3221225786`＝`0xC000013A`（STATUS_CONTROL_C_EXIT，关窗被杀）** ⇒ 说明窗口确实出现过、且被手动关掉；pythonw 随后成为孤儿进程存活（父进程为空）。
- 与红线 `feedback_no_popup_windows`（🔴 禁止一切可见控制台弹窗）冲突。**修法候选**：把任务动作换成隐藏启动（VBS `WScript.Shell.Run(..., 0, False)` 包一层），或改任务为"不管用户是否登录都运行"——但后者跑在 session 0，**可能读不到用户已登录客户端的私有登录态**（这正是 :8787 的命根子），故优先前者。**未动，待郭老师点头**（属「客户端凭据网关」项目，非本项目）。
