---
name: codebuddy-proxy-precheck
description: 派发 codebuddy 任务前必须先验 7890 代理可达性（2026-09-01 踩坑）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
  modified: 2026-09-01T16:21:22.467Z
---

codebuddy 任务派发前**必须前置测一次 7890 代理可达性**，不可达先不派或换执行位。

**Why:** 2026-09-01 派 codebuddy 改 OpenRouter 7 款落地，codebuddy 写文件阶段（不靠网络）成功了，但调用外部 copilot.tencent.com 时 7890 代理 ECONNREFUSED，导致 restart/实测/汇报阶段全挂——产生"半成功"需要调度大脑接管补完。

**How to apply:** 每次派 codebuddy 任务前先跑 `curl -m 3 -x http://127.0.0.1:7890 https://copilot.tencent.com` 看是否 200/可达。不可达时：
- 选项 A：不开代理也跑，让 codebuddy 自然 fallback
- 选项 B：换派给不靠腾讯通道的执行位（如 workbuddy_cli、cursor-cli、qoder_cli）
- 选项 C：调度大脑自己干（不推荐——执行者职责被调度大脑接管了）

相关：[[project_scheduler_role_matrix]] 派发矩阵 4 维；调度大脑只负责派发+审验，不替执行者改文件
