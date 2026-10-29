---
name: project-晨读录音识别根因与流式改造
description: 🔴 2026-10-21 定位「读页录音识别根本做不到」的三层根因并完成改造：① 真机**一个 ASR 模型都没部署**（已推 3 个）；② 引擎传了 sherpa C++ 不认的 `modelType: 'zipformer_ctc'` ⇒ **text 变乱码**（真机实证 text="眼镛"），去掉即正常；③ 架构是「整课麦克风常开 + 每 800ms 离线重转写 7 秒」⇒ 慢、且录进大量回授。改造：真流式（OnlineRecognizer）+ 口令触发 + 逐字实时上色 + 句/全文两种模式 + 底部圆形录音按钮。
metadata:
  node_type: memory
  type: 项目
  created: 2026-10-21
  modified: 2026-10-21
type: project
updated: 2026-10-21
kind: fact
status: active
scope: 晨读录音识别根因与流式改造
---

# 晨读：录音识别（2026-10-21）

## 用户诉求（逐字）

> 「那个录音识别还是不可以啊，根本做不到。能不能做到像语音识别输入、法语音识别一样实时识别了」
>
> 「识别可以设计两种朗读模式，第一种模式呢，是以句为单位的每次只识别那一句吧……还有一种是全文的朗读识别，全文识别之后才进行处理」
>
> 「你对于朗读字幕展示动画的识别，能不能做成实时的？因为你现在有点卡。比如说，我是读完一句之后，你忽然就把那一句变成了红色，而不是根据我读的情况，一个字一个字地来识别并做这个动画」
>
> 「按钮整合：把开始识别和暂停识别浓缩为一个**圆形的录音按钮**，集合在底部中间的"听"和"读"上面」
>
> 「给这个按钮增加实时识别功能……录制一个口令（口令可由用户自定义，比如"开始朗读课文"）。当用户说出自定义口令，且系统准确识别到之后，才会触发正式测试」

## 三层根因（三板斧查出来的，别再走弯路）

### ① 真机**一个 ASR 模型都没有**（最致命）
`/sdcard/Android/data/com.phrasing.phrasing/files/models/asr/` 是**空目录**。
- 推了才有：`sherpa-onnx-zipformer-ctc-small-zh-int8-2025-07-16`（62MB，中文主力）
- 部署脚本 `scratch/push_models_to_phone.py` 里设备 ID **写死成 USB 时代的 `bf6ef967`** ⇒ 无线地址下推不进去。
- ⚠️ 拉手机上的二进制文件**必须用 `adb exec-out`** —— `adb shell` 走 pty 会改字节
  （实测 m4a 2373253 → 2381045 字节，文件损坏、`duration` 读出 4.7e11）。

### ② 引擎传了 sherpa 不认的 `modelType` ⇒ **text 乱码**
`lib/creation/sherpa_onnx_asr_engine.dart` 的 `zipformer_ctc` 分支传了
`modelType: 'zipformer_ctc'` —— **sherpa C++ 的合法 modelType 里没有这个值**
（合法的是 `zipformer2` / `zipformer` / `paraformer` / `nemo_ctc` / `whisper`…）。
后果：解码器走错分支 ⇒ 真机 `text="眼镛"`、`tokens="▁ƍĩ▁ƎŁŢ▁Ɛĸľ"`。
**同一模型 + 同一 tokens.txt，PC 端不传 modelType 时输出完整中文。**
⇒ 修法：**不传 modelType**（留空走 sherpa 默认的 CTC 路径）。
⚠️ 这个坑在**离线档**和**流式档**都存在，两边都要不传。

### ③ 架构是「整课麦克风常开 + 每 800ms 离线重转写 7 秒」
- 不是流式 ⇒ 不可能"边说边出字"；
- 每 800ms 把 7 秒音频**从头重转写一遍** ⇒ 慢、算力浪费；
- 麦克风一直开着 10 分钟 ⇒ 录进大量环境噪音 + **扬声器回授**（读页 `autoPlay: true` 会播课文，而 `RecordConfig.echoCancel: false`）⇒ 真机录音频谱实测：**过零率 2200Hz、谱峰 592/593/636Hz、1kHz 以上占 80%** ⇒ 那不是人声，模型当然识别不出。
- 对照实验：电脑放课文音频、手机录 ⇒ 频谱变成 100-300Hz 占 33%、过零率 1306Hz ⇒ **麦克风本身没问题**，是回授/环境音。

## 改造（2026-10-21 已落地）

| 层 | 文件 | 内容 |
| :--- | :--- | :--- |
| 引擎 | `lib/creation/streaming_asr_engine.dart` | **真流式**：`OnlineRecognizer` 常驻 isolate，PCM 块 `pushPcm`（fire-and-forget），识别文本走 `Stream<String>` 回来。⚠️ Dart 的 isolate **没有同步 RPC**（`RawReceivePort` 只有异步 handler）⇒ 只能"推+流回来"，不能"同步等结果" |
| 录音 | `lib/training/read_along_recorder.dart` | 加 **PCM 旁路** `onPcm` 回调（16k PCM 块直推流式引擎，不改 wav/端点检测原行为） |
| 对齐 | `lib/training/reading_alignment.dart` | `align()` 增加 **frontier**（识别覆盖到的 expected 下标）⇒ 流式下尾部「还没读到」判 **pending** 而不是 **missed**（否则满屏红字） |
| 会话 | `lib/training/continuous_reading_session.dart` | 加 `ReadingMode {sentence, fullText}`；`applyRecognition(..., live: true)` 走**流式**分支（基准 = **句首**而不是 committedCursor，否则累积文本会错位） |
| 口令 | `lib/training/wake_phrase.dart` | 口令检测：归一化（去标点/空白/全角）+ 严格/宽松（同音字）匹配 + `consume()` 切掉口令段 |
| 控制器 | `lib/training/live_reading_controller.dart` | 串起来：等口令 → 命中 → 切掉口令 → 逐字对齐 |
| UI | `lib/widgets/live_record_button.dart` | **圆形录音按钮**（开始/暂停合一 + 脉冲环 + 状态文案） |
| UI | `lib/screens/chinese_reading_screen.dart` | 圆形按钮悬浮在课文区底部中央；**去掉自动开麦**（改为手动点）；模式行（初读/熟读 + 逐句/全文） |
| 偏好 | `lib/preferences/app_preferences.dart` | `readWakePhrase`（口令可自定义）。**2026-10-21 用户定：默认口令改「开始朗读」**（原「开始朗读课文」四个字更短更好说），并加 `kReadWakePhrasePresetsZh/En` 预设表 |
| 设置 | `lib/screens/settings_screen.dart` | 「读页口令」区：**预设口令一键切换**（中文 4 个 / 英文 4 个 ＋「不用口令」＝留空＝点开直接判读）＋ 自定义输入框照旧 |

**口令为什么不用 sherpa 的 `KeywordSpotter`**：它要 transducer 模型 + 另配含关键词的词表，
用户每改一次口令就要重生成词表重推模型；用流式文本匹配则**零额外模型、任意自定义**。

## 逐句判定的正确逻辑（2026-10-21 用户两次纠正后才对）

郭老师原话：
> 「只要一开始录音，它就一直在识别那些句子……逐句识别的时候，应该是这一条句子读准了，再下一个句子呀，**全绿了才下一个**。」

三个必须同时满足的条件（少一个就会"一直跳"）：

1. **游标只在 `matched` 时推进** —— `substituted`（读成别的字）**不推进**。
   ⚠️ 老代码把 `substituted` 也算进"连续命中"⇒ 读错一个字，游标照样冲过句尾。
2. **换句只在整句全绿时**（`matchedCount >= 句长 && substitutedCount == 0`），
   而不是"连续命中到句尾"。
3. **换句后必须重置流式**（`_asr.reset()`）——
   流式吐的是**从开麦起（或上次 reset 起）的累积文本**，不重置的话，
   下一句的文本里还带着上一句 ⇒ 对齐整体错位。
   ⇒ 同时要记一个 `_textHasWake` 标志：reset 之前文本里**带着口令**要 consume，
   reset 之后是纯课文**不能再 consume**（否则把下一句头几个字切掉）。

## 测试（电脑上可跑，纯 Dart）

- `test/training/live_reading_feedback_test.dart`（13 个）—— 逐字推进 / 尾部 pending /
  批式仍判 missed / 红绿不闪 / 句与全文两种模式 / frontier /
  **没读完不跳句** / **全绿才跳句** / **有错字不跳句** / 第二句以第二句为基准
- `test/training/live_reading_controller_test.dart`（13 个）—— 口令归一化、严格命中、
  自定义口令、consume、阶段机、逐字上色、口令不污染课文

## 关键坑（都踩过）

- **Dart isolate 无同步 RPC** ⇒ 流式必须"推 + 文本流回来"，别写 `Future.sync`（不存在）。
- **`execCommand('insertText')` 在本 App 的 ProseMirror 输入框里静默失效** ⇒ 改用 `innerText` + `InputEvent`。
- **`#prompt-textarea` 是 contenteditable DIV**（不是 textarea）⇒ 设 `.value` 无效。
- **Windows 侧 sherpa dll 的 ORT 是 1.17.1**，流式 zipformer2-ctc 要 API 28 ⇒ PC 上跑 Dart 流式会崩；
  **PC 验证要用 Python 侧**（`scratch/asr-env`，ORT 1.30，能跑）⇒ `scratch/_stream_test2.py`。
- **流式模型清单**（GitHub releases 可达，modelscope/hf 需交互）：
  `sherpa-onnx-streaming-zipformer-ctc-zh-int8-2025-06-30`（中文 CTC，154MB）
  `sherpa-onnx-x-asr-480ms-streaming-zipformer-transducer-zh-en-punct-int8-2026-06-05`（带标点，169MB）
- `flutter analyze` 的 `info` 级提示（prefer_final_fields 等）不算错。
