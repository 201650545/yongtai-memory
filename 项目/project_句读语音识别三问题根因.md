---
name: project-句读语音识别三问题根因
description: 2026-10-21 真机暴露的读页语音识别三个问题及其根因：① **多音字假阴性**（判定把"字"当成"唯一音节"：课文「长出」的「长」=zhǎng，ASR 吐「常」=cháng，zh/ch 不互认 ⇒ 判 substituted ⇒ 红字 ⇒ 游标不推进 ⇒ 整句卡死）；② **口令不常驻**（现在要点按钮才开麦，用户要的是进页就常驻监听、听到「开始朗读」自动开始）；③ **灵敏度太低**（RecordConfig 只有 autoGain/noiseSuppress，没设 AGC 目标电平、NS 强度、gain；且 echoCancel:false + 页面自动播放 ⇒ 录进手机自己的声音）。
metadata:
  node_type: memory
  type: 项目
  created: 2026-10-21
  modified: 2026-10-21
type: project
updated: 2026-10-21
kind: fact
status: active
scope: 句读语音识别三问题根因
---

# 句读：语音识别三问题（2026-10-21）

> 用户原话（真机反馈）：
> 「我读『长出两条后腿』，你竟然识别不了『长』……还有没有这方面的问题，关于多音字识别错误的问题。」
> 「朗读不是说了吗？是加一个识别口令，识别到开始朗读这个语音识别要常驻，听到我的口令之后它就自动开始。」
> 「需要好大好大的声音，而且靠它好近它才在识别……能不能把它识别声音的灵敏度加高一点呢？」

## ① 多音字假阴性（最要命：孩子读对了也被说读错）

**链条（已验证）**：

1. 课文侧音节 = `ChinesePinyin.format(课文句)`：先查词组表 `_phraseMap`（270 余条人工词组），
   查不到就查单字表 `_charMap`（400KB 生成表，**每字只有一个读音**；`'长': 'zhǎng'`）。
   词组表有「长高/长大/生长」「长长/长江/长袍/长短/细长」，**唯独没有「长出」**。
2. 识别侧：ASR 只吐**汉字**，再经**同一张表**转音节 ⇒ ASR 把「长」吐成「**常**」时，
   识别音节 = `cháng`，课文音节 = `zhǎng`。
3. 对齐在**去调音节**上比较：同声母 1.5 分（substituted）、其它 0.75 分；
   声母互认表只有 `zh↔z`、`ch↔c`、`sh↔s` ⇒ **zh 与 ch 不互认**
   ⇒ `zhǎng` vs `cháng` 判 substituted（红字）⇒ **游标不推进**（铁律：只有 matched 才推进）
   ⇒ **整句卡死**。

**根因一句话**：判定把「字」当成了「唯一的音节」。多音字 + 同音字 ⇒ 系统性假阴性。

**方向（不是补词组表）**：把「一个音节」升级成「**一个字的读音集合**」——
期望侧与识别侧都取集合，**交集非空即算读对**（同音字不罚）；多音字按上下文选期望读音、
判定时任一读音命中即可。轻声字（了/的/地/得/着/一/不）单独一档。
⚠️ 放宽后必须复查两条铁律：① 游标只在 matched 推进；② 整句全绿（matchedCount>=句长 && substitutedCount==0）才换句。

**已实测否掉的猜想**：不是「当前句变粗改折行」——注音布局按固定 charSize 排格，行高不变。

## ② 口令要常驻

现状：进读页 → **点圆形按钮才开麦** → 等口令「开始朗读」→ 命中才判读 → 判完停。
用户要：**常驻监听**，听到口令自动开始，判完回到「等口令」态（可连续多轮）。

要解决的子问题：常驻开麦的耗电/发热；静音时不做解码（能量门限/VAD 放哪一层）；
课文里出现「开始朗读」四字的**误触发**；Android 前台服务与权限；UI 上怎么表达"在听/已命中"。

现有件：`wake_phrase.dart`（归一化 + 严格/宽松 + `consume()`）、`live_reading_controller.dart`（阶段机）、
`read_along_recorder.dart`（开麦 + 16k PCM 旁路 `onPcm`）。

## ③ 灵敏度太低（必须大声 + 贴很近）

现有 `RecordConfig`（`read_along_recorder.dart`）：
`pcm16bits / sampleRate 48000 / numChannels 1 / autoGain true / noiseSuppress true / echoCancel false`
→ 之后 `PcmDecimator(48000→16000)`（低通+抽取）降到 16k，一路进 wav/端点检测，一路直推流式 ASR。

**没设**的参数（`record` 包支持）：`autoGainControlTargetDBFS`、`noiseSuppressLevel`、`gain`。
另外：`echoCancel:false` + 页面自动播放课文 ⇒ **回授**（真机已见识别文本里出现当前句重复）。

## 送审（本轮）

材料：`https://raw.githubusercontent.com/201650545/workspace-index/main/reviews/asr-polyphone-wakeup-sensitivity.md`
（39,975 字节，含背景、根因链条、约束、实现原文）
渠道：**ChatGPT 镜像版**（ChatGPT 6 Sol + High 思考 + 联网读链接）
与 **DeepSeek 官网 skill**（`deepseek-web-consult`，DeepThink + Search 均开）。
⚠️ 两条通道共用同一个 Chrome 活动标签 ⇒ **必须串行**（实测并行会互相踩）。
