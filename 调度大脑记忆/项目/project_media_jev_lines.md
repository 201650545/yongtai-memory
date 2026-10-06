# 路由分类 + 媒体/Jev/语音线（project_media_jev_lines）

> 建立 2026-09-25。真源：`D:\项目\ai-hub\search_gateway\data\model_routes.json`（schema_version 2，mtime 热加载，改完即生效**无需重启**）
> 后端逻辑 `services/api_gateway.py`；规则文档 `search_gateway\渠道编排规则.md`；只读汇总 `GET /api/gateway-catalog`（需 Bearer 网关 key）
> **改代码才需重启**：提权 `nssm restart ai-gateway-3100`（nssm 在 `D:\Tools\nssm\nssm.exe`，不在 PATH）

## 一、路由一/二级分类（2026-09-25 郭老师指令）
每条路由带 `category`（一级）+ `sub`（二级中文名），共 14 条：

| 一级 category | 路由（二级 sub） |
|---|---|
| `llm` | free-fast 常规快线 / free-balanced 常规均衡线 / free-heavy 深度推理线 / paid-fast 付费快线 / jev 决策模型 |
| `voice` | voice-asr 识别 / voice-tts 合成 / voice-clone 音色克隆 / voice-translate 语音翻译 / voice-caption 音频描述事件 / voice-chat 语音对话（半双工） / voice-realtime 全双工实时对话 |
| `multimodal` | image-gen 图像生成 |
| `video` | video-gen 视频生成 |

向下兼容：`catalog_routes` 不读新字段，老调用别名全不变。

## 二、语音九大类 · 薅取进度
- **已装 7 类**：ASR 识别 / TTS 合成 / 音色克隆 / 语音翻译 / 音频描述事件（caption，2026-09-25 晚落地） / 半双工语音对话 / **全双工实时对话（realtime，2026-09-25 晚落地）**
- **待薅 2 类**：
  - 声纹分离 diarize —— 郭老师定：**注册 AssemblyAI**（需凭据）
  - 变声 VC / 歌声 —— 变声可由克隆替代；歌声候选 MiniMax Music / Suno（多为付费）

**diarize 已排雷**：siliconflow 免费 `XingChenASR-Diarize-V3.0` **只分段、不做说话人归属**——切分与人工构造的 1.2s 静音间隙完全吻合，但每段一律标 `speaker:"1"`（3 组音色 × 5 种参数全返回 `['1','1','1']`）。免费档不可用，必须走 AssemblyAI。

## 二·补、voice-caption 调用契约（2026-09-25 实测定稿，免注册）
`POST /v1/audio/captions`，两种入参：multipart（`file` + 可选 `prompt`）或 JSON（`audio` = 裸 base64 / `data:audio/...;base64,...`）。
响应归一化：`{provider, model, mode, caption, raw}`；首席 `mode:"caption"`（完整描述），备席 `mode:"transcribe+emotion"`。
- 首席 `Qwen/Qwen3-Omni-30B-A3B-Captioner`（付费 ¥2.8/M，实测 5.7s）：人数/性别/年龄/情绪语气/背景/非语音事件全描述
- 备席 `FunAudioLLM/SenseVoiceSmall`（免费兜底，35–37s）：只出文本 + 情绪 emoji（实测 `"...开会吧。😊"`）
- 定价取自硅基官方定价页 2026-09-25 实抓；复用已配 siliconflow，**省掉 Hume AI 注册**

## 二·补2、voice-realtime 调用契约（2026-09-25 实测定稿，免注册）
全双工实时语音，端点是 **WebSocket 升级**不是普通 POST：`GET /v1/realtime?key=<网关key>[&model=<上游模型名>]`（浏览器 WS 无法自定义请求头，故接受 `?key=`）。模块 `services/realtime_ws.py` + `api_gateway.py` `do_GET` 钩子。
**设计=透传而非翻译**：客户端直讲 Gemini Live `BidiGenerateContent` 协议，网关只做鉴权 / 选路（读 voice-realtime 链）/ 把**首个 setup 帧的 `model` 改写为路由成员真名**（客户端写 `voice-realtime` 即可）。不做协议翻译——实时语音的打断/turn 边界/音频分块跨层翻译必然有损。
响应头 `X-Realtime-Channel` / `X-Realtime-Model` 回带实际选中成员（排查"走了谁"看这俩，或查 route_log 的 `ws_frames`）。
- 成员：`gemini-3.8-live` → `gemini-2.5-flash-native-audio-latest`（两者吃裸 setup）→ `gemini-3.8-live-extended-thinking`（**必须客户端自带** `generationConfig.thinkingConfig.thinkingLevel`，low/high 实测均可；缺了上游 close 400「Thinking level must be specified for this model」，故压尾）
- 四例经网关实测全绿：正常往返（101→setupComplete→转写→24kHz PCM→turnComplete）/ `?model=` 点名备席 / 错 key 401 不升级 / 二进制 setup 帧注入生效
- 踩坑：①`responseModalities` 只收 `["AUDIO"]`，给 TEXT 或 AUDIO+TEXT 一律 close 400，要文字须开 `outputAudioTranscription` ②上游回帧是**二进制 0x2 不是文本 0x1**，只认 0x1 会静默丢光上游消息（表现为握手成功却永远等不到 setupComplete）③写上游须 `makefile("wb")` 不能给裸 socket ④收尾两侧都要 `shutdown`，否则每连接一线程挂死

## 三、voice-clone 调用契约（2026-09-25 实测定稿）
MiMo 克隆模型 `audio.voice` **不是音色 ID，而是参考音频的 DataURL**——无需平台预注册。

```jsonc
POST /v1/audio/speech
{"model":"voice-clone","input":"要说的文本",
 "ref_audio":"<裸 base64 或 data:audio/mpeg;base64,...>","ref_format":"mp3"}
// DataURL 也可直接放进 voice 字段
```

**缺参考音频返回 400，不静默回落预置音色**（防"以为克隆了、其实是预置声"）。

## 四、image-gen 生图线
- 调用：`POST /v1/images/generations` body `{"model":"image-gen","prompt":...}`，或聊天端点别名（prompt 从 messages 提取）
- 成员：sensetime/sensenova-u1.5-fast 首席（实测 9–14s）→ u1.5-lite → agnes/agnes-image-2.5-flash 备席（11.7s）
- 商汤生图：公测免费、`watermark=false` 免费去水印；标准 OpenAI `/images/generations` 形状

## 五、video-gen 视频线
- 调用：`POST /v1/videos` body `{"model":"video-gen","prompt":...}`，网关内部代轮询至 completed 返回顶层 url（超时则 202 + video_id 自查）
- 成员：agnes/agnes-video-2.5-flash 独席（$0/秒 限免中）
- **agnes 异步坑**：mode 合法值 = `"text"`（text2video / t2v 都是错的）；size 只收 `"720P"`；限流(429)报错会抢在参数校验前，**别把 rate_limit 误读成"格式正确"**；缺 n 报误导性 invalid mode 是假象；agnes 服务端按 UA 刁难 → channels.py agnes 已配 `"ua":"curl/8.5.0"`
- 响应：video_id → `GET https://apihub.agnes-ai.com/agnesapi?video_id=&model_name=` 轮询

## 六、jev 决策线
- 调用：`POST /v1/jev`（state + questions）
- 成员：typesafe/jev-latest 首席（$5 月赠金每月续、输出免费、1200RPM）→ openrouter/typesafe-jev-1.13 备席（`/api/alpha/decisions`）
- 生态：Kev-9B（HF jaredpalmer/kev-9b，开源 9B 决策模型）+ Laya（HF convaiinnovations）+ browser-use/jev-ultrafast 运行时；OpenRouter 常规模型表 / 硅基 / 魔塔均未上架决策模型
- **Kev-9B 自托管已否决**（2026-09-25 郭老师：「我不搞本地模型，我电脑干不了」）

## 七、音频链路踩坑（2026-09-25 修，改代码勿回退）
1. `/v1/audio/*` 与 `/v1/embeddings` **必须走 `channels._urlopen(..., channel_id=cid)`**，不能用裸 `urllib.urlopen` —— 否则绕过渠道代理，配了 `proxy` 的渠道（groq）会间歇 403。该 helper 自带"代理失败回退直连"。
2. ASR 转发 multipart 时，客户端没带 `model` 字段要**注入**（不能只做替换），否则 groq 400 `model is a required property`。
3. 链失败要**累积每个成员的失败原文**返回；只报"链全部失败"会让诊断全靠猜。
4. groq 按**文件名后缀**校验音频（`.bin` 被拒，须 `.mp3` 等白名单后缀）。
5. **硅基音频理解只认 `audio_url`**（`/chat/completions` 内容块），给 OpenAI 的 `input_audio` 报 400 code 20029「Only text and image_url are supported」。
6. **硅基 TTS 的 `voice` 须 `模型名:音色名`** 格式（如 `FunAudioLLM/CosyVoice2-0.5B:alex`、`fnlp/MOSS-TTSD-v0.5:anna`），裸音色名报 20047「Invalid voice」；支持 `response_format:"wav"` 出 RIFF WAV。
7. **Gemini Live 回帧是二进制 opcode 0x2 不是文本 0x1** —— 判别"是否文本帧"会**静默丢光上游全部消息**，表现为握手 101 成功却永远等不到 setupComplete。setup 注入也必须两种帧都认（否则客户端用二进制发 setup 时注入不生效）。
8. **`responseModalities` 只收 `["AUDIO"]`**；给 `["TEXT"]` 或 `["AUDIO","TEXT"]` 一律 close 400。要文字必须开 `outputAudioTranscription`，别改 modalities。
9. WS 桥两侧收尾都要 `shutdown`：任一方阻塞在读上时只有 shutdown 能立刻唤醒，否则"每连接一线程"会挂死；写上游的句柄须是 `makefile("wb")` 而非裸 socket（无 `.write`）。

## 八、文档勘误
`渠道编排规则.md` 旧注"mistral 必须走代理 7890"经核验**不成立**——mistral 渠道 `proxy` 为空，2026-09-25 实测 `api.mistral.ai` 直连 `/v1/models` 与 `/v1/audio/transcriptions`（voxtral-mini-latest）均稳定（ASR 3/3 成功，1.1–1.8s）。旧注已作废。

---
关联：[[project_ai_gateway]] [[project_nssm_wmi_cmdline]]（⚠️ 断链，目标不存在，2026-10-01 审计） [[feedback_no_popup_windows]] [[project_image_gen_routes]]
