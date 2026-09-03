---
name: feedback-admin-tasks-run-myself
description: 管理员操作（UAC/提权）由我自己执行触发，绝不叫用户跑命令；脚本需自带自提权逻辑
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 95cff9f0-c115-4770-a66a-5ed8ec23a5c2
  modified: 2026-08-15T13:31:12.537Z
---

管理员权限的操作（nssm 改服务、注册表、服务重启等）由我自己执行：用 PowerShell 工具直接跑脚本，脚本内部用 Start-Process -Verb RunAs 自提权，UAC 弹窗用户只需点「是」。

**Why:** 2026-08-15 郭老师明确发火：我能跑的任务不要叫他跑（"你是傻逼吧…你自己不会打开管理员权限的PowerShell"）。让用户手动开管理员 PowerShell 粘贴命令是错误做法。

**How to apply:** 需要提权的脚本写成「自提权」模式：开头检测 IsInRole(Administrator)，非管理员则 Start-Process -Verb RunAs 重启自己并等待结果文件；提权前明确告知用户「马上弹 UAC 点「是」」。相关：[[feedback-decision-only-reporting]]
