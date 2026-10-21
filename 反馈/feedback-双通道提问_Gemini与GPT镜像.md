---
name: feedback-双通道提问_Gemini与GPT镜像
description: 🟠 郭老师 2026-10-21 08:5x 定：**高价值问题默认双通道提问** —— Gemini 4（`gemini -p`）＋ ChatGPT 镜像版（`mirror_isolated.py` 独立浏览器送审），交叉比对。**分工：GitHub 公开仓库/代码/星标类只能问 GPT**（Gemini 读不了公开仓库）；通用知识、架构、产品判断、长文综述优先问 Gemini 4。执行含义：①高难问题两边都问，再比对共识与分歧 ②按题目特点选通道 ③对强模型**描述需求、把决定权交给它**（不下死命令、不写死输出格式）④GPT 镜像版纪律照旧：默认 6 Sol ＋ High 档、一会话发一条等它答完、每 5 分钟刷新、不占用户标签页。
metadata:
  node_type: memory
  type: 反馈
  created: 2026-10-21
  modified: 2026-10-21
type: feedback
updated: 2026-10-21
kind: fact
status: active
---

# 双通道提问：Gemini 4 ＋ ChatGPT 镜像版

## 他的原话（逐字）

> 「现在，Gemini 4 和 ChatGPT 镜像版都可以用。其次，Gemini 4 的能力好像强于 GPT-6 sol high。
> 这样吧，你提问的时候可以两个都去提问，或者根据它们的特点，觉得这个问题谁适合回答就去问谁。
> 比如说，**如果要问跟 GitHub 相关的内容，只能问 GPT，因为 Gemini 不能去读 GitHub 的公开仓库**。」

## 执行口径

| 情况 | 走哪条通道 |
|:---|:---|
| GitHub 公开仓库、代码、星标、PR | **只能 GPT 镜像**（Gemini 读不了公开仓库） |
| 通用知识、架构推演、产品判断、长文综述 | **优先 Gemini 4** |
| 高价值 / 有争议 / 要交叉验证 | **两边都问**，比对共识与分歧（分歧要如实说"两家不一致"） |

## 通道入口（2026-10-21 实查）

| 通道 | 命令 | 备注 |
|:---|:---|:---|
| GPT 镜像版 | `python skills\...\gpt-mirror-extended-review\scripts\mirror_isolated.py run <a> <b> <轮次目录> <输出目录>` | 独立 profile 的 Chrome，**不占用户标签页**；P1 探针 `probes\probe_gpt_mirror.ps1` 必跑；默认 `6 Sol` ＋ `High` |
| Gemini | `gemini --prompt "<问题>"` | npm 全局 `@google/gemini-cli`；本机 `GOOGLE_API_KEY` 已配；**PowerShell 里多行提示词必须加引号**（否则被拆成位置参数 ⇒ 报 "Cannot use both a positional prompt and the --prompt flag"） |
| 本机网关 | `http://127.0.0.1:3100` | key 自取 `search_gateway\data\api_state.json`；模型表 `data\model_routes.json` |

## 边界

- 这条**不改变**镜像版 skill 自身的纪律（三闸、发一条等它答完、5 分钟刷新、失败不抢回）。
- 不改变"一次只做一件事"（第 13 条）：双问是**同一个问题**问两家，不是两件活。
- 机制单写源：`C:\Users\郭永涛\AGENTS.md` 第 16 条。
