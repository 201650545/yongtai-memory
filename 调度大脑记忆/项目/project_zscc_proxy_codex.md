---
name: project-zscc-proxy-codex
description: Codex/ChatGPT 桌面端接入 DeepSeek V4 Flash 走本地 8787 翻译代理（上游可切换：zscc 中转 / DeepSeek 官方 API）
metadata: 
  node_type: memory
  type: project
  originSessionId: 0138a5b8-9f25-4369-a9dc-1d07f8519516
  modified: 2026-08-02T12:38:52.967Z
---

Codex(ChatGPT 桌面端) 的 `deepseek` 辅助 agent 通过本地代理访问 DeepSeek V4 Flash：

- 代理脚本：`C:\Users\郭永涛\Documents\New project\tools\zscc_responses_proxy.py`（Python，监听 127.0.0.1:8787，把 Codex 的 Responses API 翻译成 Chat Completions）。
- 上游地址由环境变量 `ZSCC_UPSTREAM_BASE` 控制。**2026-08-02 已切换到 DeepSeek 官方 API**：`ZSCC_UPSTREAM_BASE=https://api.deepseek.com/v1`（原来默认 `https://api.zscc.in/v1`，因中转额度用完弃用）。
- `DEEPSEEK_API_KEY` 用户环境变量 = DeepSeek 官方 key（`sk-564d...`，platform.deepseek.com 申请）。官方模型名是 `deepseek-v4-flash` / `deepseek-v4-pro`。
- 启动器：同目录 `start-zscc-proxy.cmd`（幂等，已在运行则跳过）、`start-zscc-proxy.vbs`（隐藏启动）；开机自启走 Startup 文件夹里的 `ZSCC-Proxy.lnk`。日志在 `New project\logs\zscc_proxy.log`。改环境变量后必须重启代理（杀进程 + 跑 .cmd）才生效。
- config.toml `[model_providers.deepseek-zscc]` → `http://127.0.0.1:8787/v1`，`wire_api = "responses"`；`model = "deepseek-v4-flash"`（provider 段名 `deepseek-zscc` 只是标签，当前实际指向官方 API）。
- 代理支持工具调用翻译（function_call / function_call_output ↔ tool_calls）、真实流式 SSE（所有事件带 `type` 字段）、usage 归一化（input_tokens/output_tokens）。流式非流式都验证过。
- **模型名映射坑**：Codex 桌面端已有对话线程会把模型名缓存进线程状态，切到官方 API 后旧线程仍发 `deepseek-v4-flash-cc`，官方 API 不认识 → HTTP 400 → response.failed。代理里 `MODEL_ALIASES` 统一把旧名映射到官方名（`deepseek-v4-flash-cc`→`deepseek-v4-flash`），改完要重启代理。改 config.toml 只影响新线程。
- **官方 DeepSeek 协议映射坑（2026-08-02 排障，400 的三种原因）**：① OpenAI `developer` 角色官方 API 不认，须映射成 `system`；② 并行工具调用（连续多个 function_call）必须合并成一条 assistant 消息含多个 tool_calls，否则报 "assistant message with tool_calls must be followed by tool messages"；③ Codex 单独的 `instructions` 字段要补成 system 消息（代理原忽略会丢系统提示）。排障方法：代理已加 `[req]` 请求摘要和 `[upstream-error]` 错误详情日志（含官方原始错误），看 `New project\logs\zscc_proxy.log`；能从应用日志 `~/.codex/logs_2.sqlite`（node:sqlite 查 logs 表）提取 Codex 实际发的完整请求体重放复现。

**Codex 配置坑（2026-07-31 排障总结，极易踩）：**
- `[windows] sandbox` 只接受 `"elevated"` 或 `"unelevated"`，写成 `"off"` 会导致 `Invalid configuration; using defaults`，整个配置被丢弃、应用卡加载。
- `model_catalog_json` 指向的 models.json 每条必须有 `shell_type` 等必需字段，缺了同样报错丢配置。**干脆别用 model_catalog_json**，让 Codex 用兜底元数据即可。
- 应用是 MSIX 商店版（`C:\Program Files\WindowsApps\OpenAI.Codex_...\ChatGPT.exe`，AUMID `OpenAI.Codex_2p2nqsd0c76g0!App`），运行时会改写 `~/.codex/config.toml`（会加回 `sandbox="elevated"`）。
- 重启应用：`Stop-Process` 全部 ChatGPT/codex 进程后，`Start-Process explorer.exe shell:AppsFolder\OpenAI.Codex_2p2nqsd0c76g0!App`。
- 当前可用配置：`model="deepseek-v4-flash"` + `model_provider="deepseek-zscc"` + `sandbox="unelevated"`（不含 model_catalog_json / MCP 段）。

相关：[[feedback-diagnosis]]
