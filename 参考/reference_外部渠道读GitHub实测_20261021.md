---
name: 2026-10-21-外部渠道读GitHub实测
description: 2026-10-21 实测：GPT 镜像站（vip-24 / Chat / 模型6 / High）与 DeepSeek 官网都能真实读 GitHub 公开仓并原文贴出库内提示词；含大文件超限、ds_ask.py 30 秒刷新打断、opencli 原生输入需先 tab select、PowerShell 5.1 多行带引号参数被截断四个坑。
type: memory
updated: 2026-10-21
kind: fact
status: active
source:
  - D:\main\_inbox\chan-test\gpt-mirror.md
  - D:\main\_inbox\chan-test\deepseek-web-consult.md
destination_note: D:\记忆\参考\reference-deepseek-web-送审实战沉淀-20261021.md
---

# 外部渠道读 GitHub 公开仓 · 2026-10-21 实测沉淀

> 投递任务：chan-test（外部渠道读 GitHub 实测）。
> 来源原始记录：`D:\main\_inbox\chan-test\gpt-mirror.md`、`D:\main\_inbox\chan-test\deepseek-web-consult.md`。
> 去向：本条是**已存在笔记的追加段**，请整理会话并入既有条目，不要新建重复条目。

## 一、结论（两条通道都实测通过）

- **GPT 镜像站**：vip-24 账号（Plus）、`Chat` 标签、模型 `6`（ChatGPT 6 Sol）、顶档 `High`，**一次成功**读 `github.com/f/awesome-chatgpt-prompts`，原文贴出 "Act as a Linux Terminal" 提示词，非编造（assistant 正文 459 字，`stop=false` 确认生成结束）。
- **DeepSeek 官网**（chat.deepseek.com）：**三次尝试**后完全成功，同样原文贴出同一提示词；已用 `Invoke-WebRequest` 取 raw `prompts.csv` / `PROMPTS.md` 逐字核对，出处为 PROMPTS.md 的 Linux Terminal 小节（第 12–18 行）。
- ⇒ **修正旧口径**：不再只有镜像站能读公开仓，**DeepSeek 官网也能读**（Gemini 网页版仍然读不了，❌ 不变）。

## 二、四个坑

1. **大文件超 GitHub 展示上限**：`prompts.csv` 达 7.6MB，超出 GitHub 网页展示上限；只发仓库主页，模型会直接说"读不到"。**必须指向具体 .md 分节文件**才读得到。长提示词入库要**一题一文件**，别堆成单个大表。
2. **DeepSeek 侧 `ds_ask.py` 的 30 秒刷新会打断联网阅读**：脚本内置"输出停 30 秒就原生 open 刷新页面重取"，模型还在联网阅读时页面被刷掉，一次读取直接作废。**去掉该刷新、等待放宽到 ~220s** 后稳定。
3. **opencli 原生输入前必须先 `tab select <pageId>`**：否则报 `Native input requires a visible browser page`；每次原生输入前都要重新 select。文本里的**双引号要写 `\"`**，否则被 opencli 吞掉。
4. **PowerShell 5.1 传带引号的多行参数会被截断**：实测在 `"Act` 处断掉。改用 `$env:` 变量（如 `$env:DSQ`）+ `python -c` 调 `ds_ask.ask()` 传题。

## 三、补充可复用细节

- **两条浏览器通道不能并行**：DeepSeek 与 GPT 镜像站共用同一个 Chrome 活动标签，opencli 会话一次只绑一个标签（`tab new` 会抢绑定）⇒ 并行发问互相踩。**串行**：先 DeepSeek，答完再 ChatGPT。
- **DeepSeek 取答前必须让标签可见**：`activate_window` + `tab select`，`visibilityState=hidden` 时消息节点恒为 0。
- **GPT 镜像站取答判据**：轮询到 `n=1` / 长度稳定 / `stop=false`，连续两次长度不变才算完；发送走 `fill '#prompt-textarea'` → Enter，URL 跳 `/c/WEB:<uuid>`。
- **合规**：未登录、未改任何文件；DeepSeek 侧开 4 标签（含 1 次体检）/ 关 4 / 剩 0。

## 四、请整理会话合并去向（勿新建重复条目）

已有笔记命中，**本文件是该笔记的追加段**，请并入：

1. `D:\记忆\参考\reference-deepseek-web-送审实战沉淀-20261021.md` — 并入坑 2（30 秒刷新去掉 / 220s）、坑 4（PowerShell 5.1 传参）、坑 3（tab select）、可见性坑，以及"DeepSeek 能读 GitHub 公开仓"的新事实。
2. `D:\记忆\参考\reference_Gemini网页版能力与限制.md` — 能力对照表补一行：**DeepSeek 官网 = ✅ 实测通过**（Gemini 仍 ❌）。
3. `D:\记忆\反馈\feedback-向外求先问镜像站与DeepSeek官网.md` 与 `D:\记忆\反馈\feedback-送审双通道路由-Gemini优先GitHub走GPT.md` — 路由表"GitHub 公开仓库 只能问镜像站"需改为"**镜像站 或 DeepSeek 官网**（Gemini 不行）"。
4. `D:\记忆\README.md` 第 35 行"GitHub 公开仓库只能问镜像站"同上口径需修订。
