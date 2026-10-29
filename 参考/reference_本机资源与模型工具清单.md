---
name: reference_本机资源与模型工具清单
description: 做任何工具前先查这一份——本机 2026-10-29 实测可调用的模型入口（:3100 十条别名 / :8787 实测 201 模型·14 渠道 / 伪 API 生图）、可执行件（python3.12 包、node、git、gh、ffmpeg7.1+ffprobe、adb、opencli、lark-cli）、缺失项（moviepy/torch/soffice/pandoc 未装、adb 不在 PATH），以及复算命令
type: reference
updated: 2026-10-29
kind: fact
status: active
scope: 系统
---

# 本机资源与模型工具清单（IDEA-033）

> 用途：**做任何工具前先看"我手上有什么"**，别再造一遍已有的东西、也别假设不存在的能力。
> 口径：以下全部是 2026-10-29 本机实测（命令见末节，可复跑复算）；未核的项已标「未核」，不猜。

## 一、模型入口

### 1.1 主网关 `:3100`（唯一正规 LLM 通道）

- `base_url`：`http://127.0.0.1:3100`；鉴权 Bearer，key 在 `D:\项目\ai-hub\search_gateway\data\api_state.json` 的 `api_key`
- 规模（实测）：**routes 10 ｜ members 52 ｜ channels 36**
- 十条别名（每条=一条有序回落链）：

| 别名 | 用途 | 首成员 |
|---|---|---|
| `flash` | 通用（18 成员） | `longcat / LongCat-2.5-Preview` |
| `high` | 通用高智力（8 成员） | `modelscope / DeepSeek-V4.1-Flash` |
| `image-gen` | 图像生成（6 成员） | `agnes / agnes-image-2.5-flash` |
| `voice-asr` | 语音识别（6） | `groq / whisper-large-v3-turbo` |
| `voice-tts` | 语音合成（4） | `mimo / mimo-v2.5-tts` |
| `voice-clone` | 音色克隆（1） | `mimo / mimo-v2.5-tts-voiceclone` |
| `voice-chat` | 语音对话半双工（3） | `zscc / Qwen3-Omni-30B-A3B-Instruct` |
| `voice-realtime` | 全双工实时对话（3） | `gemini / gemini-3.8-live` |
| `voice-caption` | 音频描述/事件（2） | `siliconflow / Qwen3-Omni-30B-A3B-Captioner` |
| `voice-translate` | 语音翻译（1） | `groq / whisper-large-v3` |

- 免鉴权端点：`/healthz`、`/capabilities.json`（查现况不用 key）。

### 1.2 副网关 `:8787`（buddy2api，实测 201 个模型 / 14 个渠道）

- `http://127.0.0.1:8787/v1`，key 固定 `sk-buddy2api-local`；管理面在 `/admin/*`（accounts / channels / usage / logs）
- 渠道分布（2026-10-29 实测）：`workbuddy` 34、无前缀 34、`cline` 26、`workbuddy-intl` 20、`traework` 18、`webimage` 15、`loomy` 13、`officeace` 12、`raccoon` 9、`codearts` 8、`qoder`/`qodercn`/`qwenwork` 各 3、`chatshare`/`antling`/`lobster` 各 1
- 账号池：16 个账号（2026-10-29 把失效的 5 号置为 `inactive`；5 号 `workbuddy`、token 早已 invalid）
- 特殊价值：**第二条生图入口** —— `webimage/*`、`loomy/*`（网页版伪 API），别以为只有 :3100。
- **OfficeAce 渠道（2026-10-29 接通）**：走桌面客户端自带网关，不导入账号；凭据从 `D:\OfficeAce\data\storage.sqlite` + Windows 凭据管理器读（30 秒短缓存）。**会话 TTL 约 100 分钟且客户端关着不续期** ⇒ 断了的表现是 provider 报 `OfficeAceSessionExpired`，修法固定两步：① 打开 `D:\OfficeAce\OfficeAce.exe` 让它续期 ② 跑 `D:\项目\ai-hub\buddy2api\scripts\officeace_provision.py` 刷新落盘副本。**不用重启网关**（live 目录缓存 60 秒自愈）。上限：限流约 1 请求/秒、不支持图片、会话过期不假装成功。
- **前端「已接入渠道」的判定口径（2026-10-29 修）**：控制台原来按「名下有 active 账号」算已接入，凭据型渠道（无账号行）因此永远显示未接入。已在 `src\web\index.html` 加 `CREDLESS_PROVIDERS`（当前只 `officeace`），这类渠道改为「网关 enabled 且 loaded」即算已接入。该页每次请求实时读文件，**改完刷新浏览器即生效，不用重启网关**。
- 后端 `/admin/channels` 本身一直是 13 条（含 officeace，enabled+loaded），前端只显示 11 条是**展示逻辑**问题，不是接入失败。
- 现况明细以 `参考/reference_资源速查页.md` §4/§7 为准（那份是生成物，会自动刷新）。

## 二、本机可执行件（实测）

| 件 | 状态 | 备注 |
|---|---|---|
| Python | **3.12.10** | 主执行环境 |
| Node / npm | **24.11.1 / 11.6.2** | |
| git | **2.52.0** | |
| gh | **2.97.0** | 推 GitHub 走 gh 凭证，不用 SSH |
| `ffmpeg` | ✅ **7.1**（2026-10-29 装） | 稳定安装位 `D:\tools\ffmpeg\bin\ffmpeg.exe`，已加入用户 PATH；同目录 `ffprobe.exe`（6.1.1，取自带探测能力够用） |
| `ffprobe` | ✅ 6.1.1 | 同 `D:\tools\ffmpeg\bin`；与 ffmpeg 版本号不同属正常（来自不同发行包） |
| `adb` | ⚠️ **不在 PATH** | 真身 `D:\android-sdk\platform-tools\adb.exe` |
| `opencli` | ✅ 2.0.2 | 浏览器控制主通道（`browser open/eval/tab`，`--window background`） |
| `agent-browser` | ✅ 已装 | 需 Chrome 带 `--remote-debugging-port` 才能 `--auto-connect`；本机常跑 Chrome 无调试端口 ⇒ 默认走 opencli |
| `lark-cli` | ✅ | `D:\C盘迁移\User\.trae-cn\plugins\trae-remote-official\lark\1.0.5\bin\lark-cli.exe` |
| LibreOffice (`soffice`) | ❌ 未装 | 文档转 PDF 得另找路 |
| `pandoc` | ❌ 未装 | |

### Python 包（做课件/视频/文档最常查的）

- **有**：`faster_whisper`、`cv2`、`edge_tts`、`docx`(python-docx)、`openpyxl`、`pptx`(python-pptx)、`matplotlib`、`PIL`、`numpy`、`flask`、`pypdf`、`lxml`、`requests`、`soundfile`、`pydub`、`imageio_ffmpeg`
- **无**：`moviepy`、`torch`、`whisper`(openai-whisper)

⇒ 视频线可用组合：**ffmpeg(自带二进制) + cv2 + faster_whisper + edge_tts + soundfile/pydub**；涉及 torch 的重活（本地大模型推理）本机没有。

## 三、知识与检索

- 检索：`D:\记忆\q.cmd "关键词"`（跨库 `--work "D:\Work"`）→ 底层 `local-knowledge-engine`
- 索引库：`D:\记忆\.cache\knowledge.db`，**documents 270 ／ sections 4812**（2026-10-29 实测）
- 技能库：顶层技能 + 在役组件 + 归档 ≈ **58**（明细见 `能力总账.md` 与 `reference_资源速查页.md` §5）

## 四、已知短板（做东西前先认清）

1. ~~**ffmpeg 没有稳定安装**~~ → **2026-10-29 已修**：装到 `D:\tools\ffmpeg\bin` 并加入用户 PATH。**新开的终端/进程**才生效，旧会话要重开。`adb` 仍不在 PATH（真身在 `D:\android-sdk\platform-tools`），需要时显式用全路径或另加一次 PATH。
2. **无 torch** ⇒ 本地不做 GPU 推理；模型能力全部走网关转发。
3. **无 soffice/pandoc** ⇒ Office→PDF、格式转换要走打印或在线，别假设本机有。

## 五、复算命令（想更新这份清单就跑这几条）

```powershell
python -V; node -v; npm -v; git --version; gh --version
Get-Command ffmpeg,adb,opencli,agent-browser,lark-cli -ErrorAction SilentlyContinue
python -c "import importlib.util as u;mods=['faster_whisper','cv2','edge_tts','moviepy','docx','openpyxl','pptx','matplotlib','PIL','numpy','flask','torch','pypdf','imageio_ffmpeg'];print(', '.join(m+('OK' if u.find_spec(m) else 'NO') for m in mods))"
python -c "import sqlite3;c=sqlite3.connect(r'd:\记忆\.cache\knowledge.db');print([(t,c.execute(f'select count(*) from {t}').fetchone()[0]) for t in ['documents','sections']])"
```

## 六、未核项（诚实标注）

- 「子 Agent 9 档」：2026-10-27 口述里提到过，本轮**未核**，不在本清单断言。要核需查 `reference_本机本地模型清单.md` 与 DSH 条目。
