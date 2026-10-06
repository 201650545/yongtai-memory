---
name: reference-本机本地模型清单
description: 郭老师这台 PC 的本地模型家底（2026-09-30 初版；2026-10-05 郭老师裁定升级为 PC 4 档 ＋ 手机 4 档 ＝ 8 槽位矩阵，全部实测落盘）。口径＝「ASR 中/英专用 × PC 高精/快速 ＋ 手机 高精/快速 ＝ 8 槽位」，多语言 whisper 出局；OCR 只留 PaddleOCR(PP-OCRv4)。含 8 槽位实测 RTF 与时间戳覆盖、调用姿势、硬件边界。
metadata:
  node_type: memory
  type: reference
  created: 2026-09-30
  modified: 2026-10-05
  实测方式: sherpa-onnx 1.13.8 隔离 venv 实跑＋8条标准测试波形＋字级毫秒时间戳探针
---

# 本机本地模型清单（2026-09-30 19:3x 重测；数字与本轮实测同批）

## 〇、口径（2026-10-05 郭老师裁定升级：PC 4 档 ＋ 手机 4 档 ＝ 8 槽位矩阵）

> **2026-10-05 郭老师定案**：「电脑上面有 4 个模型（专门的英文高精＋快速、中文高精＋快速），手机上面也有 4 个模型（英文高精＋快速、中文高精＋快速），一共 8 个模型槽位。」
> **设计原则**：电脑追求满血高精度与极速批量处理；手机追求端侧低内存、不发热与完整时间戳精听跟读。
> 同期有效规矩：「**不要多语言通才 whisper**」「**OCR 我只要一个（PaddleOCR）**」「**只留最有性价比的模型**」。

- **被问到“我机器上有什么模型／定了吗”**：第一句直接报**「已定：PC 4 档 ＋ 手机 4 档 共 8 槽位」**（见下表），绝不再各说各话、胡猜乱报。
- 选型已定与代码落地：模型均已落盘在 `D:\本地模型\` 并通过 2026-10-05 独立实测验证。

## 一、定档结果：8 个 ASR 档（2026-10-05 全部实测通过，sherpa-onnx 1.13.8 CPU 推理）

### 1. 电脑端（PC）4 档（大算力、高吞吐、出版级精修）

| 槽位 | 定档模型 | 权重体积 | 实测 RTF | 时间戳情况 | 核心优势与定位 |
|---|---|---|---|---|---|
| **PC · 中文高精** | `sherpa-onnx-paraformer-zh-2023-09-14`（达摩院官方件，int8 232MB） | 224 MB | **0.0257** | **29/29 字级完整** | 字级毫秒时间戳完备，课件对齐与精读主轴首选。<br>*(纯文本听写满血备选：`FireRedASR2-AED` 1.15GB，RTF 0.458，中英混读完美，无字戳)* |
| **PC · 中文快速** | `sherpa-onnx-zipformer-ctc-zh-int8-2025-07-03`（单文件） | 180 MB | **0.0324** | **31/31 字级完整** | 极速批量粗切、长音频段落快速定位 |
| **PC · 英文高精** | `sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8`（NVIDIA 0.6B） | 460 MB | **0.0557** | **48/48 Token 完整** | **WER 1.5%**，原生自带完整英文标点与大小写，长文精读天花板 |
| **PC · 英文快速** | `sherpa-onnx-nemo-parakeet_tdt_ctc_110m-en-36000-int8` | 99.5 MB | **0.0168** | **46/46 Token 完整** | 速度极快（1小时音频 1分钟出），批量英文快速粗转 |

### 2. 手机端（Mobile）4 档（省电、低发热、轻量端侧）

| 槽位 | 定档模型 | 权重体积 | 实测 RTF | 时间戳情况 | 核心优势与定位 |
|---|---|---|---|---|---|
| **手机 · 中文高精** | `sherpa-onnx-paraformer-zh-2023-09-14`（达摩院官方件） | 224 MB | **0.0257** | **29/29 字级完整** | 旗舰高配机离线精听专用，字字高亮毫秒对齐 |
| **手机 · 中文快速** | `sherpa-onnx-zipformer-ctc-small-zh-int8-2025-07-16` | **60 MB** | **0.0170** | **31/31 字级完整** | 超轻量、不发热，千元机跟读跟听秒出。<br>*(纯文字备选：`paraformer-zh-small` 74MB，RTF 0.0085，无字戳)* |
| **手机 · 英文高精** | `sherpa-onnx-nemo-parakeet_tdt_transducer_110m-en-36000-int8` | 110 MB | **0.0197** | **46/46 Token 完整** | Transducer 架构抗噪强，带时间戳，适合口语跟读与发音评测 |
| **手机 · 英文快速** | `sherpa-onnx-nemo-parakeet_tdt_ctc_110m-en-36000-int8`（单文件） | **99.5 MB** | **0.0168** | **46/46 Token 完整** | 极低内存占用、单权重、秒级流式响应 |

落点：`D:\本地模型\<模型名>\`（新模型唯一落点约定，已生效）。运行环境：`D:\本地模型\.venv-asr\`（隔离 venv，**sherpa-onnx 1.13.8**；不污染全局 Python）。

**时间戳实测数据见 §一 表后那一节，这里不重抄**（本仓刚因为"两处各写一份"吃过亏）。只留方法与教训：探针 `D:\临时文件夹\ts_probe.py` 可复跑（`rec.decode_stream(s)` 后读 `s.result.timestamps`，一个模型一个子进程）；**同族、同一个 `from_paraformer` API，换个导出包时间戳就从"有"变"没有"**——凡是要字/词级时间戳的用途（句轴、单句循环、字幕对齐、逐句精听），**选型必须把 `timestamps` 当一列实测**，只看转写文本与 RTF 会漏掉这条，而它能让整个功能失效。

调用姿势（踩过的坑，直接用）：
- Paraformer：`OfflineRecognizer.from_paraformer(paraformer=…\model.int8.onnx, tokens=…\tokens.txt, num_threads=8)`
- Parakeet 0.6B 必须 `from_transducer(..., model_type="nemo_transducer", modeling_unit="subword")`；不传 `model_type` 会报 `'vocab_size' does not exist in the metadata`
- Parakeet 110M CTC：`from_nemo_ctc(model=…, tokens=…)`
- **8kHz 素材可以直接喂，不用先重采样**（本清单此前写"两个 Parakeet 在 8k 都崩，81.8%／100% WER"是**我的打分脚本 bug**，已推翻：B 线 2026-09-30 21:07 批实测含 8k 的 WER 为 1.30%／2.60%／3.90%，与 NVIDIA 模型卡"μ-law 8k 仅劣化 4.1%"一致；sherpa 内部会自动建 8k→16k 重采样器，日志里那行 `Creating a resampler` 是正常提示不是报错）

### 一之一、四个定档的出身与上游发布日期（2026-10-01 核，他问"发布日期＋为什么不用之前的模型"时的现成答案）

| 槽 | 包名日期（k2-fsa 打包日） | **上游模型发布日期（2026-10-01 查上游 API，四个全部已核）** | 出身与许可 |
|---|---|---|---|
| 中文·PC | 2023-09-14（包内文件 mtime 2024-03-10） | **2023-08-18**（ModelScope API `CreatedTime=1692336138`；该仓最后更新 2024-09-25） | ModelScope `damo/speech_paraformer-large-vad-punc…vocab8404-onnx`（API 显示仓库 path 现已改名 `iic`），达摩院/FunASR 官方件；**Apache-2.0**（包内 README frontmatter 逐字 `license: apache-2.0` ＋ API `License: Apache License 2.0`）；Paraformer 架构论文 2022 |
| 中文·手机 | 2024-03-09（包内文件 mtime 2024-03-10） | **2024-01-11**（ModelScope API `CreatedTime=1704944027`） | ModelScope `crazyant/speech_paraformer…vocab8358-onnx` ⇒ ⚠️**第三方个人转传，不是 damo 官方**；API `License` 字段**为空**＋包内 README **无 license 行**＋包内无 LICENSE 文件 ⇒ **许可未声明**（本清单 §一 此前写 apache-2.0 是未核推定，已更正；要商用得先问上游） |
| 英文·PC | 包名无日期（目录 mtime 2025-08-16） | **2025-04-15**（HF API `createdAt=2025-04-15T19:31:12Z`）⚠️我 2026-09-30 报的"2025-05-01"是**错的**，以此为准 | HF `nvidia/parakeet-tdt-0.6b-v2`，NVIDIA 官方；**cc-by-4.0**（HF cardData 已核） |
| 英文·手机 | 2025-07-08（包内文件 mtime 同日） | **2024-09-17**（HF API `createdAt=2024-09-17T20:14:17Z`）⇒ 包比上游晚约 10 个月，那个日期是 k2-fsa 转 ONNX/int8 的时间 | HF `nvidia/parakeet-tdt_ctc-110m`，NVIDIA 官方；**cc-by-4.0**（已核）；架构论文 arXiv 2304.06795／2305.05084（HF tags 逐字） |

⇒ 这四行是"**包名日期≠模型代际**"最干净的实证：110m 包上写 2025-07-08，模型本体是 2024-09-17 的；反过来 paraformer-large 包上写 2023-09-14，上游 2023-08-18 就有了。查日期的办法（可复跑）：`curl -s https://huggingface.co/api/models/<owner>/<name>` 取 `createdAt`；`curl -s https://www.modelscope.cn/api/v1/models/<owner>/<name>` 取 `Data.CreatedTime`（epoch 秒）。

**whisper 各档发布时间**（OpenAI 官方 model card 原文，盘上 `D:\listenloop\models\large-v3-turbo.pt` 是最后一档）：2022-09 初代全系列（tiny/base/small/medium/large）→ 2022-12 large-v2 → 2023-11 large-v3 → **2024-09 large-v3-turbo**。架构是 2022 年的，此后 OpenAI 未出新版。

**"为什么不用之前的 whisper"＝同一批实测的三条**（不是推论）：① 体积 1/5～1/15（99.5MB vs 464MB／1460MB）；② 速度快 3～30 倍（RTF 0.03–0.10 vs 0.32–0.91）；③ 英文 WER 反而低一半以上（1.5% vs 3.0%／4.5%）。加上结构性两条：whisper 是**多语言通才**、一个模型扛中英，而四槽是**语种专用档**；且 whisper 停在 2024-09 不再更新。中文侧同理，paraformer RTF 0.02–0.04 vs whisper-small 0.94（约 25 倍）。

### 一之二、对照基线（同一批评测，说明为什么多语言 whisper 出局）

| 模型 | 类型 | 体积 | RTF | 英文 WER |
|---|---|---|---|---|
| parakeet-ctc-110m-en | 英文专用 | **99.5 MB** | **0.03** | **1.5%** |
| parakeet-tdt-0.6b-v2 | 英文专用 | 460 MB | 0.10 | **1.5%** |
| faster-whisper-medium | 多语言 | 1460 MB | 0.91 | 3.0% |
| faster-whisper-small | 多语言 | 464 MB | 0.32 | 4.5% |
| FireRedASR2-CTC zh_en | 双语 | 742 MB | 0.44 | 中英混说那条把英文打成 `YESDAY WAS…TOAY IS TDAY`（比 paraformer 差） |

⇒ **两个英文专用档都用 1/10～1/15 的体积、3～30 倍的速度，打出了比 whisper-medium（体积 1.5GB）更低的 WER。** 中文两档比 whisper-small 快 ~25 倍（RTF 0.02–0.04 vs 0.94）。

## 一之三、2026-09-30 深夜批：中文换代评估（六路，8 条音频 51.24s，含方言与中英混说）

样本＝`D:\本地模型\sherpa-onnx-paraformer-zh-2023-09-14\test_wavs\` 全部 8 条（含 `3-sichuan`／`4-tianjin`／`5-henan`／`6-zh-en`／`8k`）。8 线程，`num_threads=8`。
证据文件：`D:\临时文件夹\zhC_merged.json`（含逐条文本）、`zhC_full.log`、`parts\p*.json.log`。

| 模型 | 权重 | RTF | 1 小时音频 | 批次 | 备注 |
|---|---|---|---|---|---|
| paraformer-zh-small（手机现档） | 0.08 GB | **0.0101–0.0143** | **0.6–0.9 分钟** | 23:17／23:26 两批 | 8 条无明显错，全场最快 |
| SenseVoice-FunASR-Nano 2025-12-17（新，阿里 FunAudioLLM） | 0.25 GB | 0.0348 | 2.1 分钟 | 23:17 | 中英混说丢成 `yay was`；2.wav 读"深度**的**分析"（余路"深入的分析"） |
| paraformer-zh-2023（PC 现档） | 0.23 GB | 0.0390 | 2.3 分钟 | 23:17 | 四川话"好像很真**式**"❌（唯一真错） |
| FireRedASR2-CTC zh_en 2026-02-25（在机，App 正用） | 0.72 GB | 0.4324 | 25.9 分钟 | 23:17 | 中英混说崩成 `YESDAY WAS…TOAY IS TDAY` |
| **FireRedASR2-AED zh_en 2026-02-26（新，完整版本尊）** | 1.15 GB | **0.5780** | **34.7 分钟** | 23:43（受压批） | **准确度最高**：中英混说全对且自带大写、天津话"法律意识太**淡薄**了"（余路"单薄"）、河南话用"**它**"指管子（余路"他"） |
| FunASR-nano 2025-12-30（第三方社区导出） | 0.93 GB | **未跑出** | — | — | 见下 |

**三条可直接用的结论：**

1. **中文"PC 高精度档"用 paraformer-large 站不住**——两批独立复现：它比手机 small **慢 2.7–3.9 倍**，且在四川话那条读错一个字。§五.1 的怀疑已证实。
2. **要"最好的中文"就是 FireRedASR2-AED，代价是 34.7 分钟/小时音频（比手机档慢约 40 倍）**，权重 1.15GB（解压后 encoder 817MB＋decoder 417MB＝1.2GB）。40 分钟一节课要跑 23 分钟 ⇒ **只适合过夜批处理，不适合任何交互场景**。出身：k2-fsa 官方从 `FireRedTeam/FireRedASR2-AED` 转换。
3. **FunASR-nano 在本机跑不起来，原因不是内存**：sherpa-onnx 原生层 `funasr-nano-tokenizer.cc:1151 Cannot find tokenizer.json`，**路径归一为全正斜杠后仍报同一句**，文件确实在（`Qwen3-0.6B\tokenizer.json`，11.4MB）。疑为中文目录名 `本地模型` 未做 UTF-8→宽字符转换。**要测须先把整包复制到纯英文路径**。它是原生 `exit(-1)`：不留 Python traceback、`try/except` 抓不到、并把同进程里排在后面的模型一起带走 ⇒ **跑多模型务必一路一子进程**。出身也要挂 caveat：README 逐字写来自 `modelscope.cn/zengshuishui/FunASR-nano-onnx`、导出脚本作者 `github.com/Wasser1462`，**不是阿里官方打包**（内含 llm 600MB＝Qwen3-0.6B＋adaptor 238MB＋embedding 155MB）。

**RTF 的读数纪律**：上表数字来自三个时间窗（23:17–23:18／23:26／23:43），机器负载不同——同一个 paraformer-small 两批分别测得 0.0143 与 0.0101，**差 40%**。所以 RTF 只在同批内横向比可靠，跨批看量级；上表的**排序**在三批里稳定，那才是可用的部分。

调用姿势（新增三条，1.13.8 实测）：
- `from_fire_red_asr(encoder=…, decoder=…, tokens=…)`＝AED 完整版；`from_fire_red_asr_ctc(model=…, tokens=…)`＝CTC 阉割版（包内 README 逐字：`We export only the encoder and the CTC branch. The attention decoder is not used.`）
- `from_sense_voice(model=…, tokens=…, language="zh", use_itn=False)`；`from_funasr_nano(encoder_adaptor=…, llm=…, embedding=…, tokenizer=…)`；`from_qwen3_asr` 也存在（对应 `sherpa-onnx-qwen3-asr-0.6B-int8-2026-03-25`，838MB，**未下载未测**）
- **建流用 `rec.create_stream()`**，不是 `so.OfflineStream(rec.config)`（后者报 `No constructor defined`）

本轮新增占盘 4.2GB（`dlC\` 三个归档 1.8GB＋解压 AED 1.2GB／FunASR-nano 972MB／SenseVoice-nano 254MB），D 可用 122→**119GB**。

**2026-10-01 复验：上面这些一个都没清，全在盘上**——`dlB\` 实测 **917M**（4 个归档：parakeet-unified-en-0.6b／parakeet_tdt_transducer_110m／zipformer-ctc-small-zh-2025-07-16／zipformer-ctc-zh-2025-07-03）、`dlC\` 实测 **1.8G**（3 个归档＋3 份下载日志），解压出来的**被否掉的档**也都还在 `D:\本地模型\`：fire-red-asr2-zh_en-2026-02-26（AED）、funasr-nano-2025-12-30、sense-voice-funasr-nano-2025-12-17、两个 zipformer-ctc、parakeet-unified-en、parakeet_tdt_transducer_110m。**四槽定档后它们都不是候选**（§一之三 已判退步／撞多语言裁定／跑不起来），但**清/留仍等一个字**——按 §三 纪律删前逐成员 md5 孪生复验＋先问他。`punct-ct-transformer` 那份留着（中文标点补测＝未测缺口 §五.3 要用）。



## 二、OCR：只留一个

**唯一保留＝PaddleOCR 通路**：`paddleocr 2.10.0` + `paddlepaddle 2.6.2`(CPU)，实际加载的权重在 **`C:\Users\郭永涛\.paddleocr\whl\`（18 MB，PP-OCRv4 det＋rec＋cls）**。
- 实测：同一张 932×1644 票据图 **4.1s／页、34 行**（商户名、注册号、GST 税号等可读）；自造中英混排图 **亚秒级、2 行全对**。
- 必带环境变量 `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`（paddle 2.6.2 与新版 protobuf 冲突，见 [[调度大脑记忆/参考/reference_local_paddle_ocr]]）。

**⚠️ 本轮查清的一处旧账**：`C:\Users\郭永涛\.paddlex\official_models\` 里那 198MB（PP-OCRv6_medium det/rec、PP-OCRv5_mobile det/rec、doc_ori、textline_ori、UVDoc）**没有证据表明被 paddleocr 2.10 加载**：实跑不传任何 `model_dir`，权重整批落在 `~\.paddleocr\whl\` 的 PP-OCRv4（18MB，文件存在性已核），而 `.paddlex\official_models` 是 paddlex 3.x 的目录约定，本机装的是 2.10。本清单此前把它们写成"当前最新一代 PP-OCR 已装"，是把"下载过"当成"在用"，**已随本轮清理删除**（要再用得先装 paddlex 3.x 并显式指路径）。

## 三、本轮清理账（2026-09-30 19:2x–19:3x，删前逐条 md5 复验）

**C 盘回收 3.86 GB**：`~\.cache\whisper\{base,small,medium}.pt` 2057 MB（torch 格式，只被 `D:\listenloop\scratch\asr-export\export-onnx*.py` 按名字加载）＋ HF 缓存 `faster-whisper-base` 141 MB、`faster-whisper-medium` 1460 MB ＋ `.paddlex\official_models` 198 MB。
**D 盘回收 8 GB**（可用 120G→**128G**）：本轮下载的 5 个 `.tar.bz2` 归档 1075 MB（**逐成员 md5 全等于已解压目录**：4/4、5/5、18/18、19/19、14/14，不同 0）＋ 川话方言包 218 MB ＋ `Xiaomi-OCR-0` 1685 MB ＋ `.venv-xiaomi-ocr` 905 MB ＋ `ocr_xiaomi.py` 等探针件。
更早一轮（18:3x）：`listenloop\scratch\whisper-models\medium.pt` 1457 MB、`listenloop\dist\models\faster-whisper-small` 464 MB（均为逐字节孪生，孪生源删后复验仍在）、`AI精听训练器\dist\_models\` 两个 whisper 归档 310 MB。

**复装命令（万一要回滚）**：
`curl -LO https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/<包名>.tar.bz2`；
whisper 档回装 `pip install faster-whisper` 后按名加载即可自取缓存。

## 四、因被代码引用而**暂留**的三件历史件（不是选择，是欠账）

| 留下的是什么 | 体积 | 谁引用 | 摘除条件 |
|---|---|---|---|
| HF `faster-whisper-small`（多语言） | 464 MB | `D:\listenloop\tool\whisper_to_lesson.py:112 --whisper` 默认值＝`small`，`:25 WhisperModel(model_size)` | 该脚本改成"中文走 paraformer、英文走 parakeet"后可删 |
| `D:\listenloop\models\large-v3-turbo.pt`（多语言） | 1543 MB | `tool\create_your_name_lesson.py:36` 绝对路径 → `:207 whisper.load_model()` | ⚠️**2026-10-01 更正：这脚本能跑**，解释器是 `D:\listenloop\scratch\asr-env\`（openai-whisper 20250625＋torch 2.5.1+cpu＋onnxruntime 1.30.0），不是系统 Python。我一度只查系统 Python 就判它"死代码占着 1.6GB"并建议改脚本后删，**已当面撤回**。⇒ 删它要先有 §〇 那条 A/B 裁定（PC 侧还产不产 `.lllesson`），不是"改个引用"那么简单；`scratch/asr-env` 自身体积也在同一笔账里 |
| `sherpa-onnx-fire-red-asr2-ctc-zh_en-int8`（双语） | 742 MB | **App 在用**：`lib\creation\sherpa_onnx_asr_engine.dart:63`、`lib\preferences\app_preferences.dart:154`（`AsrTier.zhFireRedCtc`，目录名 `firered2-ctc-zh`） | 手机中文档换成 paraformer-zh-small（74MB，RTF 0.02）后可删 |

端侧现存旧档：`AsrTier.fast=whisper-base`、`precise=whisper-small`（`app_preferences.dart:165`）——与 4 档矩阵不一致，**要换成 paraformer-zh-small＋parakeet-110m-en**；`AI精听训练器\dist\_models\` 里的 `tiny.en`（244 MB，英文单语）同理。这几处都在别的项目仓里，**由对口项目的 Agent 落地，元智能侧只出证据**。

**2026-10-01 硬闸复验（`large-v3-turbo.pt`，1,617,941,637 字节）**：① 全仓真引用**只有** `tool/create_your_name_lesson.py:36`，其余命中全在 `scratch/asr-env/Lib/site-packages/`（whisper 包自己的模型表与 sha1 表）与 `scratch/transcribe_quwaipojia.py:14`（那是 HF 模型 id 字符串，不指本地文件）；② mtime **2026-09-19 23:30**；③ **全盘没有同尺寸孪生** ⇒ 删了**不能本地回滚**，只能按 whisper 包内那张 URL 表从 openaipublic CDN 重下 1.5GB。所以这 1.6GB 不满足"有孪生可回滚"的删除前提，**必须他点头才动**。

## 五、未测缺口（别把下表当成已证）

1. ~~中文 high 与 small 没拉开差距~~ → **已证实（2026-09-30 两批独立复现，见 §一之三）**：paraformer-large 比 small 慢 2.7–3.9 倍，且在四川话样本上多错一个字。**中文"PC 高精度档"要么换成 FireRedASR2-AED（准但 34.7 分钟/小时），要么直接取消这一档、两档合并成 paraformer-small 一档。** 仍缺的一步：在他的真实教材音频（≥20 条、带人工转写金标准）上复核——目前所有中文结论都建立在 8 条 AISHELL 风样本上，**没有真人参考文本，谁也给不出 CER 百分比**。
   **2026-10-01 处置**：四槽照旧定档，中文 PC 仍是 paraformer-zh-2023-09-14；上面那条"站不住"的实测我**只备案一次**（数据在 `D:\临时文件夹\zhC_merged.json`），他没裁就**保持现档、不再提**。FireRedASR2-AED 与"合并成一档"都属未采纳的备选，别当已定方案往下做。
1b. **FunASR-nano 未测**（原生 `exit(-1)`，疑因中文目录名；要测须先复制到纯英文路径）；**qwen3-asr-0.6B-int8-2026-03-25（838MB，全清单最新）未下载未测**，且它是多语言模型，撞 §〇 的"不要多语言"裁定 ⇒ 要测得先让他重划那条线（新代中文档 FireRedASR2／FunASR-nano／SenseVoice **全是双语或多语**，纯中文专用的新档在这份清单里不存在）。
2. **Parakeet 0.6B 相对 110M 的鲁棒性未测**：两条干净样本 WER 同为 1.5%，0.6B 的价值只剩"带标点与大小写"和"难音频更稳"（后者未证）。
3. **Paraformer 输出无标点**：整段转写要断句就得另接 `ct-punc` 标点模型（sherpa-onnx 支持，本机已下 `sherpa-onnx-punct-ct-transformer-zh-en-vocab272727-2024-04-12-int8`），**没测**。⚠️原先这条写的理由是"做课件需要标点"——他 2026-10-01 明说没要做课件，**理由作废但缺口仍在**：PC 侧转写产物到底要不要标点，取决于那个未定义的用途，别拿课件当依据。
4. 手机侧只做了体积／RTF 量级判断，**没在真机上跑过**。

## 六、硬件边界（选模型前先看）

- **无独显**（只有 `AMD Radeon` 集显，AdapterRAM 报 0.5GB）⇒ 全部 CPU 推理，**别推荐 CUDA 路线**。
- 内存 15.2 GB，但**实际可用只有 0.6–3.6 GB 且随他的 Agent 起落**（2026-09-30 23:0x–23:4x 实测：WorkBuddy 5 进程 2.1GB＋Qoder 5 进程 1.76GB＋ima.copilot 551MB＋chrome＋MsMpEng 常驻；本清单此前写"可用约 9.8 GB"是空闲时快照，**不能当选型前提**）。
  - 实测换算：加载 int8 权重约吃 **1.25 倍权重体积**的可用内存（0.72GB 权重 → 可用 3.75→2.84GB）。据此 AED(1.15GB) 需约 2.0GB、FunASR-nano(0.93GB) 需约 1.7GB、FireRed-CTC(0.72GB) 需约 1.4GB。
  - **提交余量（commit）常年有 20GB 左右**，所以大模型在物理内存不足时仍能加载成功，但会换页 ⇒ RTF 数字失真。**要么等一个空闲窗口再测，要么给数字挂"受压批次"标记**，两者都不许冒充干净基线。
- 实测 8 线程下小档峰值都很轻（0.6B int8 转 16.7s 音频用 1.6s）。
- 盘：**D 可用 128 GB**，C 可用 73 GB。
- 参照物：VLM 型 OCR 在这台机器上是"一页 100 秒"量级（本轮实测 3.0 tok/s），**管线型 OCR 是亚秒级**；同类边界适用于 ASR——大档不等于好用。

**How to apply:** 他问"我机器上有什么模型／能不能跑 X"→ 先答 §一 四档＋§二 一个 OCR；再按 §〇 口径判新候选（**多语言档一律出局**）；给建议必须带 §一 那种实测列，没测就写进 §五 具名缺口，不猜。相关：[[reference_云服务器底座与跨项目联合点]]、[[调度大脑记忆/参考/reference_local_paddle_ocr]]、[[project_ListenLoop]]
