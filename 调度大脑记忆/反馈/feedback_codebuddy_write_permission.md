---
name: codebuddy-write-permission
description: codebuddy CLI 必须显式传 --permission-mode bypassPermissions，否则写文件全部 permission denied
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
  modified: 2026-09-02T14:22:48.014Z
---

codebuddy CLI 默认拒绝所有写操作（Edit/Write/New-Item）。workbuddy_cli.py 必须传 `--permission-mode bypassPermissions` 给 codebuddy 子进程，否则 agent 写任何文件都会被拦下，只能给「调研结论+待授权后落地」汇报。

**Why:** 2026-09-02 派 harness 同步任务，codebuddy 首轮只能给调研结论——所有 `Bash`/`Write`/`Edit`/`New-Item`/`[IO.File]::WriteAllText` 全部 `permission denied`。修法=workbuddy_cli.py 加 `--permission-mode bypassPermissions` 到 codebuddy 命令行。

**How to apply:**
1. workbuddy_cli.py 启动 codebuddy 命令时必须含 `--permission-mode bypassPermissions`（已在 L54 加入）
2. 派发前必先 ping 验证 7890 代理可达（[[feedback_codebuddy_proxy_precheck]]）
3. 派发前必先验模型未 429（[[feedback_codebuddy_model_lock]]）：今天 2026-09-02 hy4 + GLM 5.3 flash 均 429，明日 13:46 重置

相关：[[feedback_codebuddy_model_lock]] 模型白名单；[[feedback_codebuddy_proxy_precheck]] 7890 代理前置