---
name: deepseek-web-consult-changelog-2026-10-21-long-material
description: 2026-10-21 用 DeepSeek 官网送审「读页语音识别三问题」的实战沉淀：材料走公开仓 raw URL；**两条浏览器通道必须串行**（共享 Chrome 活动标签 + opencli 会话一次只绑一个标签）；答案的**代码块只在 DOM 的 <pre> 里**；新会话 cid 带 WEB: 前缀取不到、要看 URL 改写成裸 uuid；流式会静默断开 ⇒ 刷新重取。
metadata:
  node_type: memory
  type: 参考
  created: 2026-10-21
  modified: 2026-10-21
type: reference
updated: 2026-10-21
---

# DeepSeek 官网送审 · 2026-10-21 实战沉淀

> 这次问的是「晨读」读页语音识别的三个问题（多音字假阴性 / 口令常驻 / 录音灵敏度）。
> 材料：<https://raw.githubusercontent.com/201650545/workspace-index/main/reviews/asr-polyphone-wakeup-sensitivity.md>（39,975 字节）
> 回答落盘：`D:\Work\元智能\20_自适应工作流引擎\runtime\asr_fix\ds_answer.md`（16,828 字节）
> 与 ChatGPT 镜像版的交叉比对结论见 `D:\记忆\项目\project_晨读语音识别三问题根因.md`。

## 一、怎么问（实测有效）

```bash
python scripts/ds_doctor.py            # 闸门：host/login/composer/idle/render
python scripts/ds_ask.py "<提问>" --new-chat -o answer.md --json \
       --search on --deepthink on --tab <pageId>
```
- **DeepThink / Search 默认就是开的**（doctor 的 `toggles` 项会打印），不用特意去点。
- **材料太长 ⇒ 发到公开仓、只给 raw URL**：DeepSeek 能读公网 URL（不依赖 Search 开关）。

## 二、坑（都是这次踩出来的）

| 坑 | 现象 | 正解 |
| :--- | :--- | :--- |
| **两条浏览器通道不能并行** | DeepSeek 与 ChatGPT 镜像站**共用同一个 Chrome 活动标签**，且 opencli **会话一次只绑一个标签**（`tab new` 会抢绑定）⇒ 并行发问会互相踩，两边都拿不到答案 | **串行**：先 DeepSeek，答完再 ChatGPT |
| **答案的代码块不在 API 文本里** | `content.parts` 的文本里没有代码块 | 代码块在页面的 `<pre>` 里 ⇒ 取代码要捞 DOM |
| **新会话的 cid 带 `WEB:` 前缀** | `/backend-api/conversation/WEB:xxx` → 400；去掉前缀 → 404 | **等 URL 自己改写成裸 uuid** 再按 `create_time` 排序取 |
| **流式会静默断开** | 页面停在残缺内容上，等多久都不出正文 | 每 5 分钟 `location.reload()` 再取；刷新后要重新 select + nudge |
| **页签可能已被别的 Agent 导航走** | `--tab` 报「not part of the current browser session」 | 重新跑 `ds_doctor.py` 拿新 pageId |

## 三、这次它给出的判断（与 ChatGPT 镜像版交叉比对）

- 多音字主因：**ASR 解码阶段选错读音**（对齐器只是忠实判成 substituted）；
  它给的对齐器改法（异读候选集 + 句子级重打分）与 ChatGPT 的「汉字主对齐」**互补**。
- 口令常驻：阶段机改成「常驻 listening + `_judging` 布尔」＋ **三级门控**
  （能量门 → VAD → KWS/ASR 唤醒门）＋ 误触发防护（300ms 内仍有语音 / 1.5s 冷却）。
- 灵敏度：**先关 autoGain / noiseSuppress**，加固定增益＋软限幅，回授用**半双工**而不是硬开 AEC。
- ⚠️ 它有一处判断**错了**：说 RMS 门限会把音频挡在 ASR 门外 ⇒ 真机代码里
  `onPcm` 在 `tracker.feed` **之前**无条件推流 ⇒ 门限只管端点检测（ChatGPT 那边判对了）。
- ⚠️ 它的抗混叠怀疑也不成立：我们早就是 33 阶加窗 sinc FIR（送审材料没贴到那段）。
