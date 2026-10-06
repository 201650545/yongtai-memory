---
name: reference-免费渠道调研-2026-09-22
description: 白嫖大模型/语音/ASR/视频渠道调研快照：已实抓核实的 + 待核实的清单，含接入优先级建议
metadata:
  node_type: memory
  type: reference
  created: 2026-09-22
---

# 免费 AI 渠道调研（2026-09-22 快照）

> 调研方式：内置 WebSearch/WebFetch 当日全挂（火山搜索渠道未激活），全部本机直连抓官网核实；标「待核实」的来自常识+旧资料，接入前须实测。

## 一、高价值新发现（建议接入）

| 渠道 | 内容 | 状态 |
|---|---|---|
| **Google AI Studio / Gemini API** | gemini-3.8-flash 等**免费层：输入输出全免**（限速制、不绑卡、数据用于训练） | ✅ **已接入**（2026-09-22 当日：key+渠道+free-balanced 编排，见 [[project-gemini-edge-tts]]（⚠️ 断链，目标不存在，2026-10-01 审计）） |
| **GitHub Models** | GitHub 账号免费调 GPT/DeepSeek/Llama/Phi 等目录模型（限速制） | ⏳ 页面 JS 渲染抓不到，需注册实测 |
| **阿里百炼** | 新用户各模型免费 token 包（qwen 系，90/180 天有效） | ⏳ 待核实明细 |
| **百度千帆** | ERNIE Lite/Speed 等永久免费档模型 | ⏳ 待核实 |
| **腾讯混元 lite / 讯飞 Spark Lite** | 官方宣称免费档 | ⏳ 待核实 |

## 二、语音方向（API 级真白嫖）

| 渠道 | 免费量 | 备注 |
|---|---|---|
| **Edge-TTS**（开源库） | **完全免费无限** | 微软 Edge 在线音色，中文音色质量好，TTS 链补席强候选 |
| Azure 语音免费层 F0 | TTS 50 万字符/月 + STT 5 小时/月 | 需 Azure 账号 |
| Google Cloud TTS/STT | TTS 400 万字符/月 + STT 60 分钟/月 | 需 GCP 账号 |
| ElevenLabs | 1 万字符/月 | 音质标杆，量小 |
| （已在用）groq whisper / mistral voxtral / 硅基 SenseVoice+Qwen3-ASR+XingChen / CosyVoice2 | — | 覆盖已足够 |

## 三、视频方向

- **API 级没有真白嫖**：已有方舟 Seedance（1.0-pro-fast 170 万 + 1.5-pro 200 万 token）+ agnes-video；硅基 Wan2.2 ¥2/条已裁决太贵。
- **Web 端每日赠送**（非 API，适合手动）：Kling / Hailuo / Vidu / PixVerse / 即梦每日登录积分。
- 开源自托管（Wan2.2/LTX-Video）需显卡，本机不现实。

## 四、结论与优先级

1. **Google Gemini 免费层** ✅ 已接入（2026-09-22）：flash-lite 500 RPD 进 free-balanced，3.8-flash 点名
2. **Edge-TTS** ✅ 已接入（2026-09-22）：voice-tts 第 2 席，免费无限
3. GitHub Models / 百炼 / 千帆作第二梯队，注册后逐个探针
4. 视频无新 API 白嫖，维持现状

## 五、小米 MiMo V2.6 系列（2026-09-22 晚补充调研）

- **官方平台 mimo.mi.com**：OpenAI/Anthropic 兼容网关，V2.6-Flash ¥1/M in ¥2/M out、V2.6-Pro ¥3/M ¥6/M（1M 上下文，100RPM/10M TPM）——**全付费无免费档**
- **白嫖途径**：①新客注册赠金 ②邀请有礼双方各 ¥10（均 40 天有效）③MiMo Claw ¥14.9/月**每天送 3h 免费时长** ④MiMo-V2.5-TTS 价格限时免费（多音色+音色克隆）⑤MiMo-X Pro/Flash Preview 邀测限时免费（需申请，状态待确认）
- OpenRouter 有 5 款 MiMo 全付费（flash $0.14/M 最便宜）；ModelScope/硅基无；无开源权重
- **桌面客户端已下载**：官网 CDN `XiaomiMiMo-latest-x64-setup.exe`（239.9MB）→ `D:\02-AI工具\小米MiMo客户端\`

## 六、web 转 API 可行性（2026-09-22 晚实测抓取）

| 站点 | 结论 | 证据 |
|---|---|---|
| **MiMo 网页**（aistudio.xiaomimimo.com） | ✅ 完全可行 | 发消息端点 `POST /fastchat/open-apis/bot/chat?xiaomichatbot_ph=<cookie>`，请求体 `{msgId, conversationId, query, modelConfig:{enableThinking, webSearchStatus, model:"mimo-v2.6-pro-ultraspeed-studio"}, multiMedias}`，cookie 鉴权，SSE 返回；Ultra/Chat 两种模式即不同 model 参数 |
| **千问网页**（chat.qwen.ai） | ✅ 可行 | 已登录（Qwen3.7-Plus 全系列可选），token 在 localStorage（JWT 209 字符），API 面 `/api/v2/*`；社区已有成熟转换方案 |

→ 待建任务：两个 web2api 适配器（OpenAI 格式 ↔ 站点私有格式），接入网关作免费渠道。MiMo 网页版 = 免费用 V2.6-Pro/UltraSpeed；千问网页 = 免费用 Qwen3.7-Plus 等全系列。

### web2api 开发情报包（2026-09-22 实抓，够直接开工）

**MiMo 适配器**
- 端点：`POST https://aistudio.xiaomimimo.com/fastchat/open-apis/bot/chat?xiaomichatbot_ph=<值>`
- 请求体：`{"msgId":"<uuid32>","conversationId":"<uuid>","query":"<用户文本>","isEditedQuery":false,"modelConfig":{"enableThinking":false,"webSearchStatus":"disabled","model":"mimo-v2.6-pro-ultraspeed-studio"},"multiMedias":[]}`（Ultra 模式；Chat 模式 model 名待抓）
- 响应：SSE——`event: message` + `data:{"type":"text","content":"<think>\0...\0收到"}`，内容用 `\u0000` 分隔，`<think>...</think>` 为推理段需剥离
- ⚠️ 鉴权坑：ph 值带字面引号（`"G0cjp/...=="`），且依赖 httpOnly 小米账号 cookie（document.cookie 不可见）→ 需 CDP Network.getAllCookies 或 DevTools 手动导出 Cookie 头；页面内 fetch 重放 401 已验证踩坑
- 实测一次回复消耗 promptTokens 2355（含 2176 缓存）

**千问适配器·实战补全（2026-09-22 晚，web2api 一期开发实测）**
- ⚠️ 站外直调死路：无浏览器指纹调 chat.qwen.ai → 阿里云 WAF JS 挑战页（HTTP 200 + aliyun_waf_aa HTML），非 4xx，极易误判成功
- ⚠️ 挂起陷阱：请求缺 `source:web`/`Version:0.2.91`/`X-Request-Id`/`X-Accel-Buffering:no`/`Accept` 头时服务端**不报错、fetch 永远 pending**（建会话/删会话/聊天全一样）；补齐自定义头才通
- 建会话：`POST /api/v2/chats/new` body `{"title":"x","chat":{}}` → `data.id`；不显式建会话直接发 chat_id → 200 `CHAT_NOT_FOUND`（页面 UI 是首条消息隐式建的，重放学不来）
- 删会话：`DELETE /api/v2/chats/<id>`（同样要全自定义头）——**适配器每次请求用完即删**，防网页版聊天记录爆炸
- SSE 格式：`data: {"choices":[{"delta":{"content":"...","phase":"answer"|"thinking","status":"typing"|"finished"}}],"usage":{...}}`；首行 response.created；phase 字段干净地区分思考段
- Bearer token = localStorage.token，页面上下文 fetch 其实靠 cookie 即可鉴权
- 落地：services/web2api.py :3102（浏览器桥，opencli eval 发起+轮询收割→OpenAI SSE 重放），网关 custom_channels `qwen-web`，点名 `qwen-web/qwen3.7-plus` 全链路 6.9s 实测通

**千问适配器**
- 端点：`POST https://chat.qwen.ai/api/v2/chat/completions?chat_id=<uuid>`
- 请求体：`{"stream":true,"version":"2.1","incremental_output":true,"chatId":"<uuid>","chat_mode":"normal","model":"qwen3.7-plus","messages":[{"role":"user","content":"...","chat_type":"t2t",...}],"feature_config":{...}}`
- 鉴权：Bearer token = localStorage.token（JWT，opencli eval 可取）
- SSE 增量输出（incremental_output:true），模型 id 形如 qwen3.7-plus

## 七、第二轮白嫖调研（腾讯云 17 家盘点，2026-03 发布，时效需逐个核）

| 渠道 | 内容 | 优先级 |
|---|---|---|
| **联通云 Coding Plan** | 0 元订阅 GLM5/Qwen3.5/MiniMax，Lite 1.8 万次/月（日 1200 次）Pro 9 万次/月，名额 12000 | ⭐ 高（量大管饱） |
| **Cerebras** | 每天 100 万 tokens 免费，推理速度极快 | ⭐ 高 |
| 百度千帆 | Lite/Speed 系每模型 100 万 tokens（3 个月） | 中 |
| 讯飞星辰 MaaS | GLM-5/Kimi-K2.5/MiniMax 免费活动（3 月 5 日截止，疑已过期） | 低（核时效） |
| 阿里云 Coding Plan | 有免费档（aliyun.com/benefit/scene/codingplan） | 中 |
| 欧派算力云 | 新用户 R1/V3 各 100 万 tokens（6 个月） | 低 |
| Modal | GLM-5 免费端点 | 中 |
| NVIDIA NIM / OpenRouter / Cloudflare / 魔搭 | 已在用 | — |

## 八、附带发现

- 内置 WebSearch 走的火山搜索渠道未激活（403 要求去 Ark 控制台开通）——需要郭老师在火山控制台激活或换搜索后端
- WebFetch 域名校验服务被网络墙掉——今后调研一律走本机直连抓取
