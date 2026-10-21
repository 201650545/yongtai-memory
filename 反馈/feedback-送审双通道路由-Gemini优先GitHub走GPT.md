---
name: feedback-送审双通道路由-Gemini优先GitHub走GPT
description: 外部强模型送审有两条通道（GPT 镜像站 / Gemini 4 网页版）；默认两边都问、Gemini 4 优先，只有要读 GitHub 公开仓库这类任务才单走 GPT。
type: feedback
updated: 2026-10-21
kind: fact
status: active
---

# 送审走双通道：默认两边都问，GitHub 类的单走 GPT

郭老师原话（2026-10-21）：

> 「现在，Gemini 4 和 ChatGPT 镜像版都可以用。其次，Gemini 4 的能力好像强于 GPT-6 sol high。
> 这样吧，你提问的时候可以两个都去提问，或者根据它们的特点，觉得这个问题谁适合回答就去问谁。
> 比如说，如果要问跟 GitHub 相关的内容，只能问 GPT，因为 Gemini 不能去读 GitHub 的公开仓库。」

## 落到执行上的规则

| 提问类型 | 走哪条 | 原因 |
|:--|:--|:--|
| 常规（文案 / 方案 / 代码 / 分析 / 排版建议） | **两边都问**（Gemini 4 优先，GPT 并行对照） | 用户实测 Gemini 4 ≥ GPT-6 Sol High；两边互为校验 |
| **要读公开 GitHub 仓库** | **只走 GPT 镜像站** | Gemini 网页版读不了 GitHub 公开仓库（`gemini-web-review/SKILL.md` 的 ❌ 边界） |
| 要在**镜像站实例**上验证/复现 | 只走 GPT | Gemini 不在镜像站环境里 |

## 工具

`技能库\external-model-review\components\dual-review\scripts\dual_review.py`

```bash
python dual_review.py <提问文件> <输出目录>              # 自动路由（关键词命中 ⇒ 单走 GPT）
python dual_review.py <提问文件> <输出目录> --only gpt   # 强制单走
```

输出 `gemini.md` / `gpt.md` / `_manifest.json`（记路由决定、两条通道的字符数与耗时，便于对照着挑）。

## 今晚的实测（2026-10-21 夜）

同一份「A4 教辅排版方案」的提问：
- **Gemini 4 网页版：一次跑通**，19,733 字符，≈4 分钟；
- **GPT 镜像站：试 12 次没取回**（实例抽风 no-pill / 流式截断只抓到 52 字 / 错抓上一轮答案 /
  凭据端口被残留进程占着）。

⇒ **交付时先用 Gemini**，镜像站当备份；两边都问时，manifest 里的字符数与耗时可用来初筛，
但**最终选哪份要人看内容**（用户判断 Gemini 更强，那就以 Gemini 为主、GPT 做对照补漏）。
