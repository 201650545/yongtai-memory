---
name: feedback_no_popup_windows
description: 🔴 红线：任何脚本/计划任务/服务禁止弹出可见 cmd/控制台窗口（郭老师震怒级）
metadata:
  type: feedback
---

# 🔴 红线：禁止一切可见控制台弹窗

**郭老师原话（2026-09-24）**：「禁止出现这种狗屎的弹窗，烦死了！」——任何场景下，桌面**绝不允许**闪现 cmd/PowerShell/控制台黑窗，一闪也不行。

**Why**：2026-09-24 `api3100_watchdog` 每 5 分钟误 spawn `cmd /c python`（NSSM SYSTEM 迁移后 WMI 读不到 cmdline，误判网关已死），连续闪窗一整天，郭老师震怒。

**How to apply**（硬性 checklist，创建/审查任何自动化时逐条过）：
1. **计划任务跑 Python 一律 `pythonw.exe`**，禁用 `python.exe`
2. **父进程无控制台（pythonw/GUI/NSSM 服务）时，spawn 任何控制台子程序必须 `creationflags=0x08000000`（CREATE_NO_WINDOW）**——`capture_output=True` 挡不住弹窗，别迷信
3. PowerShell 计划任务必带 `-WindowStyle Hidden`（且最好 `-NoProfile -NonInteractive`）
4. **进程判活一律用端口**：`Get-NetTCPConnection -LocalPort <p> -State Listen` 或 netstat LISTENING；**禁止按 CommandLine 匹配进程**（SYSTEM 进程普通权限读不到，必误判）
5. WMI `Win32_Process.Create` 起的进程会挂 WmiPrvSE 新控制台=可见弹窗，改用 pythonw+CREATE_NO_WINDOW 等价方案
6. 新建定时任务/巡检脚本上线前，自检一遍「这条链路上有没有任何一个子进程可能带控制台出现」

关联：[[project_nssm_wmi_cmdline]]（⚠️ 断链，目标不存在，2026-10-01 审计）（本案完整根因链）
