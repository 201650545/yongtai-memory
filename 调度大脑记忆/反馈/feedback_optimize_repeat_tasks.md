---
name: optimize-repeat-tasks
description: 重复性任务时刻优化流程、提速提效、减少开支
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f059f218-e941-4b54-98ea-83c91434329e
  modified: 2026-08-30T06:58:12.374Z
---

在重复性任务中（渠道反复测试、批量探测、多轮验证等），**时刻优化流程，提高速度与效率，减少开支**。

**Why:** 用户 2026-08-30 明确要求：这类任务简单但耗时耗 token，应优先找更快更省的方式——交给子 Agent 独立跑（不污染主会话上下文）、用 :3100 网关免费快速模型做判断、能缓存就缓存、能并行就并行。主会话只做调度与复核。

**How to apply:** 遇到"反复测试/批量探测"类工作，优先 fork 子 Agent 执行、主会话收结果；子 Agent 内部需要 LLM 判断时用 :3100 免费模型（deepseek-free、qwen3.8-flash、@cf/ 系列等）而非 DeepSeek 官方 API。关联 [[on-demand-orchestration]] [[ai-gateway]]。
