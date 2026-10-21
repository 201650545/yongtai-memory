---
name: feedback-向外求先问镜像站与DeepSeek官网
description: 郭老师定：找信息/跑数据/做工作/要图片风格/找灵感，一律先想用 ChatGPT 镜像站 skill 与 DeepSeek 官网 skill，别自己闷头做
metadata:
  type: feedback
  updated: 2026-10-21

type: feedback
updated: 2026-10-21
kind: fact
status: active
---

# 向外求，先问镜像站与 DeepSeek 官网

## 他的原话（2026-10-21 16:5x）

> 「无论是找信息、跑数据、做工作，还是想要什么图片风格、找灵感，什么都可以去用 ChatGPT 镜像版的 skill，以及 DeepSeek 官网搜索那个 skill。」

## 这条为什么重要

他的原话里藏着一个**能力盲区**：不是"我不知道有这个工具"，而是**"我以为得自己干"**。

本次实例：做「核心 82 词深度词条册」封面时，我**自己手搓 SVG 扁平矢量插画**，
被他一句「这个国内版这个风格做得也太丑了吧」打回。
而 `gpt-mirror-extended-review` 的 SKILL.md 里**明写着**「需要用镜像站 chat 生图（图像模型可直接渲染中文）」——
**能力一直在库里，我只是没想起来用**。改成走 AGNES 生图通道出真水彩插画后，他直接说「这个教材本很好看」。

⇒ 印证第 11 条的判断：**「搜得到」≠「想得起来」**。手搓 ≠ 能力不存在。

## 落到动作上

| 场景 | 先用 |
| :--- | :--- |
| 找信息 / 查资料 / 读公开链接 | `deepseek-web-consult`（`ds_ask.py` / `ds_read_links.py`） |
| 深度送审 / 生图 / 长文 / 视觉灵感 | `gpt-mirror-extended-review`（`mirror_isolated.py`） |
| GitHub 公开仓库 / 代码 / 星标 | **只能**问镜像站（Gemini 读不了公开仓库） |
| 通用知识 / 架构 / 产品判断 | `dual-review` 双问再交叉比对 |
| 想要某种图片风格 | **镜像站能出图**，先送审要风格参考，别自己猜 |

## 边界

- 与第 6 条**不冲突**：`web_search` 按次计费、硬禁；镜像站与 DeepSeek 官网是另一条已授权通路。
- 与第 10 条**不冲突**：本条讲"用通道产出交付物"；第 10 条禁"为了验证模型好坏而批量发请求"（1~3 次上限）。
- 两个 skill 都属 `D:\Work\元智能\10_AI自成长引擎\技能库\external-model-review\components\` 组件族。

## 机制正文在哪

**单写真源 = `C:\Users\郭永涛\AGENTS.md` 第 11.1 条**（2026-10-21 新增）。
本文件只留原话与实例，细则不复制。
