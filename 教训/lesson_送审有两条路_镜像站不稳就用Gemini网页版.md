---
name: lesson_送审有两条路_镜像站不稳就用Gemini网页版
description: 外部强模型送审有两条通道：GPT 镜像站（gpt-mirror-extended-review）与 Gemini 4 网页版（gemini-web-review）；镜像站的取回链路不稳（实例抽风、流式截断、错抓上一轮），Gemini 网页版反而一次就跑通。
type: lesson
updated: 2026-10-21
kind: rule
status: active
---

# 送审要走双通道：镜像站不稳就换 Gemini 网页版（2026-10-21 实测）

## 场景

《核心 82 词深度词条》排版方案那一问，在 **GPT 镜像站**上试了 **12 次没取回**：
账号池派到不渲染 composer 的实例（vip-25 / vip-22 相继 no-pill）、
流式截断只抓到 52 字、抓回校验要求出现 `【word】` 标记（自由作答型提问没有）、
凭据中转端口被上轮残留进程占着、**错抓了上一轮的答案**（"最后一条 assistant" ≠ "这一轮的答案"）。

同一份提问，**Gemini 4 网页版一次跑通**：挂载 16s、注入 qlen 与预期一致、真回车发送、
`user-query` 恰好 +1、**19,733 字符的完整方案**落盘，全程约 4 分钟。

## 两条通道的要点

| | GPT 镜像站 | Gemini 4 网页版 |
|:--|:--|:--|
| 组件 | `gpt-mirror-extended-review` | `gemini-web-review` |
| 落点 | `vip-XX.67673.live`（实例会抽风） | `gemini.google.com/app` |
| 注入 | `#prompt-textarea`（contenteditable DIV） | Quill API（`send_quill.js`） |
| 发送 | 点 send 按钮 | **真回车** `keys Enter` |
| 必查 | 消息数 +1 且 composer 清空 | `qlen` 归 1 且 `<user-query>` +1 |
| 取回 | `backend-api/conversation/<cid>`（**要按 create_time 排**） | `message-content` 的 innerText |
| 坑 | 实例/端口/流式/错抓 | **页面必须 visible**（否则静默拒绝提交） |

## Gemini 驱动（本次新写，可直接用）

`D:\Work\English-Content-Factory\02_Projects\HN-ENGLISH-666\06_templates\_gemini_send.py <提问文件> <输出文件>`

要点：① `tab new` 开新标签（**必须活动标签**，否则 Gemini 静默拒收）→ 轮询到 `.ql-editor` 出现
→ 注入（Quill）→ `keys Enter` → 核对 `user-query` +1 → 轮询 `message-content` 到**长度稳定 ≥2 轮**再落盘。
⚠️ `set_thinking.js` 这次报 `no-mode-picker`（模式选择器的可编程路径仍不稳定），
但**不选模式也能正常出稿**（默认模型即可）。Gemini 网页版反复发请求有风控 ⇒ 一次一问。

## 结论

**同一件外部评审的事，准备两条通道**：镜像站那条今天从 12 次失败里挖出了不少可复用的坑
（API 要按 create_time 排、"最后一条"≠"这一轮"、随机端口避开残留、逐实例试闸），
但**交付时应该用更稳的那条**。以后要外部模型出方案/出文案，**先上 Gemini**，
镜像站当备份。
