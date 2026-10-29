---
name: reference_资源速查页
description: 本机资源与工具速查（生成物，勿手改）——网关 :3100 入口与鉴权、10 条路由与成员、生图可复制请求、DSH 模型条目数、58 个技能逐条一句话、不可用渠道清单、记忆检索库规模；由 build_capability_catalog.py 生成，配置变更后重跑即可刷新
type: reference
kind: reference
status: active
scope: 全局（所有 Agent、全部项目）
requires: 无（资料类条目，不设前提）
updated: 2026-10-25
---

# 资源速查页（生成物 · 请勿手改）

> 生成时间：2026-10-25 00:59:16　生成器：`build_capability_catalog.py`
> 本页由脚本从真源抽取，**配置变了就重跑**，不要手改。手写版 `资源与工具总目录.md` 已过期，以本页为准。

## 0 · 源文件快照

| 源 | 修改时间 | sha256(前8) | 状态 |
| --- | --- | --- | --- |
| `D:\项目\ai-hub\search_gateway\data\model_routes.json` | 2026-10-24 01:54 | `1ca2850f` | ✅ |
| `D:\项目\ai-hub\search_gateway\data\gateway_capabilities.json` | 2026-10-23 01:24 | `792c47a8` | ✅ |
| `C:\Users\郭永涛\.dsh\profiles\desktop\cordis.patch.yml` | 2026-10-25 00:58 | `8c5a0ee5` | ✅ |
| `D:\Work\元智能\10_AI自成长引擎\技能库\能力总账.json` | 2026-10-24 08:45 | `cf518f29` | ✅ |

## 1 · 网关入口与鉴权

- base_url：`http://127.0.0.1:3100`
- 鉴权：`bearer`，头 `Authorization`，key 在 `data/api_state.json` 的 `api_key` 字段
- 免鉴权端点：调 /v1/* 需带 master key；/healthz 与 /capabilities.json 免鉴权
- 规模：routes 10 ｜ members 52 ｜ channels 36 ｜ 已过期 2

**怎么调（真源原样）**
```
{'purpose': '列模型', 'curl': 'curl -s -H "Authorization: Bearer $KEY" http://127.0.0.1:3100/v1/models'}
```
```
{'purpose': '对话', 'curl': 'curl -s -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" -d \'{"model":"<alias>","messages":[{"role":"user","content":"hi"}]}\' http://127.0.0.1:3100/v1/chat/completions'}
```

## 2 · 网关路由（别名 = 一条有序成员链）

| 别名 | 类别 | 成员 | 首成员 | fallback(配置) |
| --- | --- | --- | --- | --- |
| `flash` | 通用 | 18 | `longcat / LongCat-2.5-Preview` | 关 |
| `high` | 通用 | 8 | `modelscope / deepseek-ai/DeepSeek-V4.1-Flash` | 关 |
| `image-gen` | multimodal/图像生成 | 6 | `agnes / agnes-image-2.5-flash` | 关 |
| `voice-asr` | voice/识别 ASR | 6 | `groq / whisper-large-v3-turbo` | 关 |
| `voice-caption` | voice/音频描述/事件 | 2 | `siliconflow / Qwen/Qwen3-Omni-30B-A3B-Captioner` | 关 |
| `voice-chat` | voice/语音对话（半双工） | 3 | `zscc / Qwen/Qwen3-Omni-30B-A3B-Instruct` | 关 |
| `voice-clone` | voice/音色克隆 | 1 | `mimo / mimo-v2.5-tts-voiceclone` | 关 |
| `voice-realtime` | voice/全双工实时对话 | 3 | `gemini / gemini-3.8-live` | 关 |
| `voice-translate` | voice/语音翻译 | 1 | `groq / whisper-large-v3` | 关 |
| `voice-tts` | voice/合成 TTS | 4 | `mimo / mimo-v2.5-tts` | 关 |

> `fallback(配置)` 只管 `/v1/chat/completions`；**生图与语音 handler 自己在代码里遍历整条 chain**，真实回落看响应头 `X-Fallback-Count`。`首成员` ＝ 链上第一位。

## 3 · 生图（可直接复制）

```powershell
$k = (Get-Content 'D:\项目\ai-hub\search_gateway\data\api_state.json' -Raw | ConvertFrom-Json).api_key
$body = '{"model":"image-gen","prompt":"一只戴眼镜的橘猫","size":"1024x1024"}'
$r = Invoke-RestMethod -Uri 'http://127.0.0.1:3100/v1/images/generations' -Method Post `
  -Headers @{Authorization="Bearer $k"} -ContentType 'application/json' -Body $body
# 取图：$r.data[0].b64_json 写 .png；或 $r.data[0].url 下载（AGNES 只给 url）
```

现行链（6 席，保序回落）：

1. `agnes / agnes-image-2.5-flash`
2. `agnes / agnes-image-2.1-flash`
3. `cloudflare / @cf/black-forest-labs/flux-1-schnell`
4. `imgpseudo / doubao-image`
5. `sensetime / sensenova-u1.5-fast`
6. `sensetime / sensenova-u1.5-lite`

> 真源 note（可能含历史席位，现行链以上面列表为准）：生图专用链（2026-10-20 19:43 郭老师裁定：肯定选 AGNES，无水印）：AGNES agnes-image-2.5-flash -> AGNES agnes-image-2.1-flash -> Cloudflare flux-1-schnell -> 生图公益站 gpt-image-2.5 -> 豆包/即梦网页版伪 API -> 商汤 u1.5-fast -> 商汤 u1.5-lite（**商汤「日日新」带 logo 水印，降为末席兜底**）。**ark/seedream 是付费通路，已下线。**

生图还有第二个入口：`http://127.0.0.1:8787/v1/models` 里的 `webimage/*` 与 `loomy/*`（`Bearer sk-buddy2api-local`，网页版伪 API）。两边都列，别以为只有 3100。

## 4 · DSH 模型入口

| provider | 入口 | 模型数 | 状态 |
| --- | --- | --- | --- |
| `local-gateway` | `http://127.0.0.1:3100/v1` | 2 | ✅ |
| `buddy2api` | `http://127.0.0.1:8787/v1` | 28 | ✅ |
| `minimax-code` | `http://127.0.0.1:3211` | 2 | ✅ |
| `step` | `https://api.stepfun.ai/step_plan/v1` | 1 | ⚠️ 未设 `STEP_API_KEY` |

- profile 内 `- id:` 合计 **33** —— 这是「已配条目数」，不是「可用模型总数」。
- 默认模型：`buddy2api / workbuddy/deepseek-v4.1-flash`（内置适配器，不在上面表里）
- 语音 / 生图 / 多模态不进 DSH 选择器，必须直接打端点。

## 5 · 技能（全部列出，逐条带一句话）

- 根目录：`D:\Work\元智能\10_AI自成长引擎\技能库`
- 结构：`<技能>\SKILL.md`；母仓 `\<母仓>\components\<组件>\SKILL.md`
- 计数：顶层 16 + 在役组件 21 + 归档 21 = **58**（剔 `.history`；归档在 `_收存_宿主自产`，默认不加载）
- 能力总账 standalone：**12** 条（不在母仓下的独立技能）
- ⚠️ 账上有、盘上无：pagesift-crawler

### 5.1 顶层技能

| 技能（目录） | 干什么 |
| --- | --- |
| `anatomy` | Build crafted, highly detailed, interactive isometric SVG figures that explain… |
| `computer-use` | 本机桌面控制（computer use）—— 让 Agent 能"看见"这台电脑的屏幕并动手操作：看屏幕（控件结构 + 截图 + OCR）、点鼠标、打字、按… |
| `dsh-our-free-model` | DSH 免费大模型插件（dsh-our-free-model）收录记录：免登录/免注册/免 API Key，直连 Kimi K3（2.8T）与 DeepSe… |
| `engineering-traps` | 本机工程实战踩坑沉淀册（母仓）。6 个 L3 原子组件，每条都是从真实排障里提炼的硬核防护：Shell/PowerShell 传参截断、Node 管道丢输出… |
| `external-model-review` | 外部强模型送审母仓（Skill Suite）。3 个原子组件：GPT 镜像站送审（AI 问答宝账号池 / Chat 标签 + ChatGPT 6 Sol +… |
| `gateway-channel-catalog-inventory` | 对多渠道 LLM 网关做全渠道模型目录拉取、评分筛选线匹配与免费档清单输出的稳定流程。覆盖：实时与配置混合来源标注、key 文件 BOM 修正、聚合渠道付费… |
| `local-knowledge-engine` | 本地知识证据引擎与断流检索规范。用于在查询知识库（如 D:\记忆、D:\Work、通用规范、项目文档）时进行本地增量索引、毫秒级证据抽取、混合检索（中文词级… |
| `memory-router` | 多 Agent 多项目共享记忆路由协议。任何 Agent 在读写 ai-hub-memory 记忆前必须加载本 Skill，按 R1-R9 确定项目作用域并… |
| `obsidian-canvas-board` | 用户语境下的“可视化看板/可画”特指 Obsidian Canvas (.canvas) 原生画布文件 |
| `opencli-browser-stable-roundtrip` | 在共享浏览器里用 opencli 通道把消息稳定送到对端会话（GPT 镜像站等）并完整取回长回复的操作规程。覆盖：只操作自己新建的标签页、注入前 eval … |
| `ops-task-fleet-watch` | 本机定时任务舰队巡检 —— 只读核对「我方运维计划任务」还在不在、有没有被停用、退出码对不对、有没有过期没跑。当要回答"某个自动化是不是已经悄悄停摆了""这… |
| `phrasing-course-pipeline` | 句读/Phrasing 课程全流程生产母仓（Skill Suite）。母目录下 7 个原子组件各守一环，母仓本文件只做路由与编排：篇目核对→字词导图→双模态… |
| `phrasing-lesson-plan-coauthor` | 与用户（在职二年级语文教师）逐层共创统编二上语文教案的工作流。核心是「按文体定主线」+ 从课程思政《不会的时候》移植的三条纪律 + 字词先锁环节后写。触发词… |
| `qidi-parent-notify` | 启迪培训机构家长通知的执行规范（催费 / 课费核对 / 出勤明细图 / 排课通知 / 欠费清单）。当用户说「催费」「清理费用」「课费通知」「家长通知」「出勤… |
| `rename-sync-tool` | 批量改名/改路径的同步流水线——改目录（git mv）→ 白名单内容替换 → Junction 重指向 → 旧名残留扫描 → 新路径逐条可达性校验 → fr… |
| `xhs-ops` | 小红书全链路运营母仓（Skill Suite）。3 个原子组件：点赞每日管线（A取消旧赞/B新笔记v3分析/C旧信息联网复核）、图文笔记完整发布流程（图片标… |

### 5.2 母仓组件

**engineering-traps**（6）

| 组件 | 干什么 |
| --- | --- |
| `lark-cli-home-redirect-not-configured` | Loomy shell 的 HOME/APPDATA 重定向会让 lark-cli 读不到用户配置，调用前须临时切换 |
| `node-exit-drops-piped-stdout` | Node 脚本在 process.exit 前用 console.log 写管道会整段丢输出，绿灯读数因此说谎 |
| `powershell-json-arg-space-truncation-field-id` | PowerShell 5.1 向原生 CLI 传 JSON 时字段名含空格会截断参数，应改用字段 ID 作键 |
| `snapshot-membership-loop-drops-new-inputs` | 批处理环按"上一轮索引快照的成员集"遍历，会静默丢掉刚新增的条目——环看着在跑，实际越跑越旧 |
| `split-parallel-walk-for-mass-fs-scan` | 百万级目录遍历要切成子树并行跑并逐段报进度，串行全扫会长时间无出账、无法区分卡死与慢 |
| `zero-hit-census-is-scanner-failure-not-absence` | 枚举/扫描类脚本的零命中必须判为"自己失效"，Windows 上 shell out 会命中 WSL bash 把失效伪装成"不存在" |

**external-model-review**（5）

| 组件 | 干什么 |
| --- | --- |
| `deepseek-web-consult` ⛔ | **【2026-10-25 起暂停】郭老师 DeepSeek 账号被封 3 天（至 2026-10-28 前后），该通道一律别开；要联网改走 gpt-mirror-extended-review / gemini-web-review / doubao-yuanbao-web-consult** 原描述：用官方 chat.deepseek.com 网页版直接提问并取回完整回答；也能按「多选批量删除」清聊天记录。原生 fill 输入、原生 Enter 发送、3… |
| `doubao-yuanbao-web-consult` | 用官方 www.doubao.com / yuanbao.tencent.com 网页版直接提问并取回干净正文。豆包可一键把档位从「快速」切到「专家」，元宝… |
| `dual-review` | 一份提问同时问两个外部强模型（Gemini 4 优先、GPT 镜像站并行对照），或按题型自动路由到更合适的那一个。通用知识/架构/产品判断默认双问再交叉比对… |
| `gemini-web-review` | 用浏览器能力驱动本机已登录的 Gemini 网页版（AI Ultra），把材料**直接贴进正文**送审、要第二意见。实现见 技能库\naming.yaml … |
| `gpt-mirror-extended-review` | 通过 AI 问答宝账号池 / GPT 镜像站（wendabao → vip-XX.67673.live）以**默认 ChatGPT 6 Sol + 顶档 H… |

**phrasing-course-pipeline**（7）

| 组件 | 干什么 |
| --- | --- |
| `phrasing-dist-audit` | 句读/ListenLoop dist 课包批量三查执行器（只读、幂等）。第1查初读/熟读双口径（卡口 gatekeeper.py §1–§4 + 规范 19… |
| `phrasing-lesson-build` | 从「教材原文 ＋ B站名师原声」造出句读（ListenLoop）的 .lllesson 双模课包（听读＋视听）。含音源优先级裁定（林鹿鸣＞SeaverTho… |
| `phrasing-lesson-package-audit` | 句读/ListenLoop 课程包审核、挂接校验与制课验收 SOP。五条真源铁律（教材原文为文本唯一真源 / ASR 只出时间轴 / lessonId 以包… |
| `phrasing-lesson-segmentation` | 课文朗读与听读切分规范 Skill（语文低幼双模态意群切分与精听时间轴统合规范）。用于将课文原文与 ASR 原生时间戳精细切分为“初读（短呼吸节拍）”与“熟… |
| `phrasing-text-split` | 句读课文初读/熟读怎么切行：初读4~7字短切、见逗号就切、副词介词前也切。含郭老师《犟龟》106句验收用例、二上6篇合规证据、与旧12字顶/卡口阈值的冲突登… |
| `phrasing-textbook-catalog-sync` | 统编版语文教材篇目核对与同步 SOP。教材篇目核对铁律（教师为唯一真源 / 先查替换时间表 / 只碰标题层）+ 五步同步流程 + 双验证门禁，防止照抄旧版目… |
| `phrasing-textbook-words-mindmap` | 把统编版语文课本的「会认字 / 会写字 / 词语」按课文挂到句读（ListenLoop）APP「课文思维导图」的三级节点上。真源是**人民教育出版社课本附录… |

**xhs-ops**（3）

| 组件 | 干什么 |
| --- | --- |
| `multi-store-sync-delete` | 多数据源同步真删 SOP——dry-run 校验、分批删云端行、删本地文件与 JSON 键、双向孤儿终检。Use when 批量删除多端同步的笔记/记录或清… |
| `xhs-like-daily` | 小红书点赞每日管线（A取消旧赞/B新笔记v3分析/C旧信息时效复核）的执行与补跑手册。Use when 用户要求跑或补跑点赞任务、取消旧点赞、分析新点赞笔记… |
| `xhs-note-publish` | 小红书图文笔记的完整发布流程（图片/标题/正文/话题/原创声明/文件附件/发布）。需要「在已登录的小红书页面完成发布流程（含附件与原创声明）」这一浏览器能力… |

### 5.4 停用中（1）

| 技能 | 状态 | 说明 |
| --- | --- | --- |
| `deepseek-web-consult` | ⛔ 2026-10-25 起暂停 | 郭老师 DeepSeek 账号被封 3 天（至 2026-10-28 前后），该通道一律别开；要联网改走 gpt-mirror-extended-review / gemini-web-review / doubao-yuanbao-web-consult |

### 5.3 归档（21，默认不加载）

`agent-role-handover-doc`、`anatomy_伪版备份_20261016`、`android-subtitle-remake`、`asr-subtitle-proper-noun-fix`、`channel-probe-typing`、`clash-direct-rule-fix`、`disk-relocation-decay-check`、`execution-report-audit`、`feishu-base-batch-record-migration`、`flutter-llm-quiz-judgement`、`flutter-preference-toggle`、`gateway-channel-catalog-inventory`、`gateway-free-seat-sync`、`gateway-route-line-restructure`、`health-probe-false-negative-debug`、`long-build-timeout-diagnosis`、`model-rank-recalibration`、`npm-global-upgrade-redirected-shell`、`opencli-browser-stable-roundtrip`、`project-task-handover-doc`、`termux-fdroid-boot-autostart`

- 口径：只统计上述技能库；DSH 插件自带的技能不在此计数。用之前先 `skill` 加载同名技能。

## 6 · MCP

- 台账登记：computer-use、api-gateway-media
- `computer_use` 已被用户明令禁用（2026-10-22），不许调用、不许建议恢复。

## 7 · 不可用 / 已下线（别去试）

| 类型 | 对象 | 说明 |
| --- | --- | --- |
| 渠道过期 | `gmi` | 2026-09-06 |
| 渠道过期 | `xiaohongshu` | 2026-09-30 |
| 渠道 disabled | `ark` | - |
| 渠道 disabled | `bai` | - |
| 渠道 disabled | `cmkk` | - |
| 渠道 disabled | `stepfun` | - |
| 模型下线 | `seedream*` / `seededit*` | 付费通路，调用直接 400 |
| 工具禁用 | `computer_use`（MCP） | 用户明令禁用 |
| 命令不可用 | `arkcli` | 不在 PATH |

## 8 · 目录

| 根 | 子目录（不含隐藏） | 含隐藏 | 有效（非 . / _ 前缀） |
| --- | --- | --- | --- |
| `D:\Work` | 17 | 21 | 15 |
| `D:\项目` | 24 | 26 | 23 |
| `D:\记忆` | 11 | 15 | 9 |

## 9 · 记忆检索库

- `D:\记忆\.cache\knowledge.db`：50.0 MB · documents 268 · sections 4731
- 查法：`D:\记忆\q.cmd "词"`（跨库加 `--work "D:\Work"`）；精读用 `…\local-knowledge-engine\scripts\locate_anchor.py` 拿行号后再读 ≤50 行。
- `索引.md` 自述条目：299
- ⚠️ 差 31 条（索引与库不同步，重建后核对）

## 10 · 产物落点与提交

- 执行会话产物只写 `D:\记忆\_inbox\<任务名>\` 或 `D:\Work\_inbox\<任务名>\`；不直写正式目录。
- 入库只走单写者：`D:\小浣熊\mm-code\bin\obsidian-commit.ps1 -Repo "D:\记忆" -Paths "相对路径" -Message "…" -DryRun`（一次一条路径）。
- 网关自检：`GET http://127.0.0.1:3100/healthz`（免鉴权）、`GET /v1/models`（需 master key）。

## 11 · 本次体检

- ⚠️ 账实不符：能力总账有、盘上无 → pagesift-crawler
- ⚠️ 索引漂移：索引.md 299 vs 库 268（差 31）

## 12 · 视频能力（2026-10-28 补，防止 Agent 搜不到）

- **AI 自动剪辑引擎**：`D:\Work\元智能\10_AI自成长引擎\草稿区\L3_Skill\video-assembler\`（896 文件，SKILL.md）
- **宣传片项目**：`D:\Work\AI视频项目\`（561 文件）
- **项目入口页**：`D:\记忆\项目\project_AI视频项目.md`
- **底料**：ffmpeg 7.1 **不在 PATH**，用 `imageio_ffmpeg.get_ffmpeg_exe()`；`faster_whisper`(字幕) + `edge_tts`(配音) + `cv2/PIL`(画面) 均已装
- **成片路径注意**：`D:\Work\_inbox\宣传片_句读60秒\v2_动效\final_v3\` 已不存在（10-24 删除）
