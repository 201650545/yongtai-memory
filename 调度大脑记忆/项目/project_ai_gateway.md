---
name: project-ai-gateway
description: 统一 AI 网关（D:\项目\ai-hub\search_gateway；:3000 搜索聚合 + :3100 API 转发，原 D:\游戏\ds_v4_cli 已迁移）——opencli 4 引擎 + LLM 渠道路由 + 统一模型组/光线拖拽编排/总开关/用量记账/派发中心二级页（GATEWAY_ID 陷阱）
metadata:
  node_type: memory
  type: project
  originSessionId: cc570cb5-bfc6-41c1-a63b-84533fa58583
  modified: 2026-10-08T00:00:00.000Z
---

# 统一 AI 网关（search_gateway）

> 本页为**概述 + 时间线索引**。全部操作级/踩坑级详情已归档至
> 👉 `项目/归档/project_ai_gateway_完整详细记录.md`（2026-09-08 起，本页只留结论，避免臃肿）。

## 这是什么

统一 AI 搜索聚合网关，运行于 `D:\项目\ai-hub\search_gateway\`（:3000 搜索 + :3100 转发），原 `D:\游戏\ds_v4_cli\` 已迁移为旧副本。仓库副本：`D:\Work\AI平台\apps\search-gateway`（:3000）+ `D:\Work\AI平台\apps\api-gateway`（:3100）。

- **:3000 搜索聚合**：`unified_gateway.py`，多引擎 opencli 浏览器检索 + `/v1/chat/completions` + `/api/search_json`，定位为 AI 的无头搜索工具。
- **:3100 API 转发**：`api_gateway.py`，OpenAI 兼容 LLM 渠道聚合转发，独立于 :3000，含路由编排/总开关/用量/限流/熔断/记账。
- 协同：`D:\项目\config\gateways.json`（3 网关注册）、`runtime.yaml`（服务拓扑真源）、中央平台 :8000。

## 关键不变量 / 易错点（必读）

- **路径**：运行体 = `D:\项目\ai-hub\search_gateway`（实测存在，2026-09 核实；此前多处误写 `D:\项目\services\search_gateway`，该路径不存在）；`apps/api-gateway` 是仓库自包含副本。两处 `api_page.html` 必须保持**同一内容**，改一边记得同步另一边。
- **GATEWAY_ID 陷阱**：`channels.GATEWAY_ID` 在 `import channels` 时**即冻结**；要某网关账本独立，必须在 import 前 `os.environ.setdefault("GATEWAY_ID","<id>")`，否则账全混进默认 `ds_v4_cli`。:3100 已设为 `api_gateway`，账本独立。
- **重启口径（2026-10-08 郭老师裁定改写，原「重启免 UAC」条款作废）**：`:3100` 由 nssm 服务 `ai-gateway-3100` 以 **LocalSystem** 持有 —— 这是郭老师**有意选的**（原话「就是我让它这样搞的，我不希望它一直弹那个弹窗，好烦，而且还开机自启动」），目的＝**不弹控制台窗 + 开机自启**。⇒ 改 **代码** 后重启统一走 **`nssm restart ai-gateway-3100`（需提权，UAC 弹一次）**；**改 `data/*.json` 配置不需要重启**（mtime 热加载，见 `/healthz` 的 `loaded_routes_sha256` 变化）。旧的「普通进程 Stop + 普通进程 Start」写法已作废。详见 [[调度大脑记忆/教训/lesson_gateway_restart_privilege_trap]] 第四节。
- **重启要杀全部同脚本进程**：`api_gateway.py` 若旧进程没死干净，新端点会 404 且旧端点照常，易误判「新代码没生效」。判断一律以 `netstat -ano | findstr :<端口>` LISTENING 为准。
- **四种状态勿混淆**：成员冷却（`_model_cooldown` 30s）≠ 渠道限流（`rate_limit.py` open/throttled/blocked，15/30/60/120/300s 退避）≠ 共享代理故障域熔断（`fault_domains.is_tripped`，DIRECT 不入域）。
- **主题落地方式**：一律走 `api_page.html` 的 `data-style` 新增风格（不另起主题系统）；不伪造、不假装「额度+延迟动态加权」。

## 时间线（近→远）

- **2026-10-08 · 实测核对 + 文档仓对齐（WorkBuddy 接手轮）**：`:3100` 活着（`/healthz` ok），**持有者 PID 6260，父 `nssm.exe`，服务 `ai-gateway-3100`（Auto）** —— 文档仓原记 PID 35192 已过时。实测：路由名 **16**（`/v1/models`）、渠道 **21**（`/api/channels`）、累计 calls 7941 / input 8.14 亿 tok / errors 0。编排席位数 free-flash **14** / free-high **8** / fast **8** / video-gen **1**（`data/model_routes.json`）。
  - **文档仓 `D:\Work\API转发网关` 改 4 处活文档**：`README.md`＋`SYSTEM_OVERVIEW.md` 目录树头 `D:\Work\api-gateway\`→`API转发网关`；`AGENTS.md` **`/api/channels/status` 是错的（实测 not found）→ 正确为 `/api/channels`**；`PROGRESS_TRACKER.md` PID→6260、M3 路径改名。带日期的历史件有意不改。
  - **口径修正（旧结论作废）**：09-30 记的「文档仓 `渠道编排规则.md` 停在 09-22 stale／双真源分叉」**已不成立** —— 该文件现仅存于运行体 `D:\项目\ai-hub\search_gateway\渠道编排规则.md`（40 KB，mtime 09-29 20:16），文档仓已无此文件。
  - **郭老师当场裁决并已执行（同日 11:5x，热加载零重启）**：① **删失效模型** —— `model_routes.json` 摘 4 枚：free-flash 的 `openrouter/qwen/qwen3.8-27b:free`、`openrouter/poolside/laguna-s-2.1:free`、`openrouter/stealth/space-bunny-alpha`；free-high 的 `openrouter/google/gemma-4-31b-it:free`；**另 `测试模型` 线的备份席也是同一枚已下架的 `stealth/space-bunny-alpha`，一并摘除** ⇒ 席位数 free-flash **14→11**、free-high **8→7**、测试模型 **3→2**。② **删方舟渠道** —— `channels.json` 摘 `keys.ark` ＋ `channel_enabled.ark=false`；`quota_guard.json` 加 `ark: deny_all`；`channel_notes.json`/`channel_expiry.json` 摘 ark 条目；**停用计划任务 `ArkQuotaScan`**。见证：`/api/channels` 已无 `ark`，`/healthz` 的 `loaded_routes_sha256` `048d9090…`→`c60969e8…`。
  - **退役口径（重要，勿再照旧改）**：本仓退役渠道的既有惯例是 **封存 + 隐藏 + 停用 + 摘 key**，`services/channels.py` 的代码桩**保留不删**（deepseek/zhipu/bai/gmi 同款）——删代码桩会撞 `channel_profiles.py` 的 `REDLINE_CHANNELS`↔`probe_free_channels.FORBIDDEN` 一致性断言。备份在 `data/_bak_20261008/`。
  - **持久性**：12:00 的 `or_free_refresh.py` 只追加**探活通过**的席位（`probe_ok` 真调四重前置），四枚失效模型探活必失败 ⇒ 不会自动回填。
  - **未决项（待郭老师拍板，本轮未动）**：② video-gen 单点哑线（他裁"暂时不管"）；③ 方舟额度警戒（已随渠道删除一并消失）；④ 僵尸路由名 `测试模型`/`测试模型1`（他说没看懂，待解释）；⑤ 重启权限死结（nssm 服务身份 vs「重启免 UAC」冲突，A/B/C 待裁）。
- **2026-09-30 · 联合点补登记（网关侧第一次认下自己的下游与底座）**：`:3100` 不只在本地——**阿里 99 ECS 上已有一份 `:3100` 在跑**（与 frps 中转、Uptime Kuma 同机，2026-09-29 决策档实证），本地那份才是运行体真源 `D:\项目\ai-hub\search_gateway`。被 9 个项目依赖这件事也进了 [[调度大脑记忆/项目/project_relation_graph]]。**跨项目联合点总表见 [[调度大脑记忆/参考/reference_云服务器底座与跨项目联合点]]**（改渠道/路由/端点前先查它，别砸到贾维斯中控与 ListenLoop）。
- **2026-09-30 · 真实用法下的"OR 一直失败"真因＝请求体 5.5MB（埋点当日抓到）**：`seat_fail_ms` 上线后头两条真实流量（12:50:27 / 12:52:12，`req_bytes≈5.57MB`）显示两个代理席各卡 **41s** `write operation timed out`（41＝20s×2，印证 urllib timeout 是单次 socket 操作上限），直连 `opencode/space-bunny-free` 兜住但要 26–142s。体量来自 Claude Code 每轮重发整段历史：活动会话 `~/.claude/projects/C--Users----/b6f0bd1b-….jsonl` **16.04MB/894 行**，`req_bytes` 随时间单调上涨。⇒ 判"渠道坏了"之前**先看 `req_bytes`**；每轮白烧 82s 才回落是结构问题，修法＝会话 `/compact` 或把直连席升首席／加体量闸（改 `测试模型` 三席顺序须郭老师点头，那是他 09-30 定的）。。**09-30 12:5x 郭老师裁：选前者（自己 /compact），网关不动，三席顺序保持原样。**
- **2026-09-30 · JEV 计费对清＋白嫖面定盘（12:2x 实测）**：
  ① **free-auto 用的就是他自己的 JEV**，走 `api_gateway.py:_jev_decide()` 直连 `https://api.typesafe.ai/v1/systemone`，key 在 `data/typesafe_key.txt`（**与 OpenRouter 无关；$5 赠金只买那一次分档判定**，正文由免费席出）。实测 `model=free-auto` → `/api/ops` 的 `jev.last_route={t:12:24:44, decision:{choice:fast, confidence:1.0}}`，HTTP 200/7.0s，落点 `cloudflare:@cf/qwen/qwen3.8-27b`。**`typesafe` 不在 `channels.keys` 里但这条线不是哑线**（独立 key 文件＋硬编码 URL），别照渠道表判它死。
  ② **OR 上那笔 `typesafe/jev-1.13` $0.000014（09-24）的出处＝每日巡检**：`data/probe_runs/2026-09-26/27` 三条台账写着 `channel=openrouter, model=typesafe/jev-1.13`，09-28 起探针改打 `channel=typesafe`，源头已断。`jev_reach` 探针回 **422＝活着**（`daily_channel_refresh.py:25,353` 故意发缺参请求；401/404/超时才算死），别当故障报。
  ③ **OR 付费门现在关着（进程内直查）**：`quota_guard.blocked('openrouter', …)` 对 `deepseek-v4-flash-vision-exp`/`anthropic/claude-sonnet-5`/**`typesafe/jev-1.13`** 全回 `guard_not_allowlisted`，只放 `:free` ⇒ 走 :3100 结构上不可能再产生 OR 扣费（日志里 29 条 OR 402 是配置生效前的旧账）。
  ④ **7890（mihomo）是本机单点**：openrouter/groq（`channels.py:76,92`）＋zenmux/gemini/opencode-zen（`channels.json`）5 席硬编码走 `127.0.0.1:7890`。代理没跑＝这 5 席一律 `WinError 10061 积极拒绝`（12:05 起就这样），**不关代码的事**。`fault_domains.promote_on_proxy_down()`（`fault_domains.py:104`，`promote_channels=[sensetime, cloudflare]`）会把直连席升链首救场，所以 `测试模型` 线（opencode-zen→openrouter→opencode 直连）代理全挂仍 100% 成功、`fast` 线 cloudflare 由第 8 位升到第 2 位。要看代理死没死：`Get-NetTCPConnection -LocalPort 7890 -State Listen` ＋ 注册表 `ProxyEnable`。
  ⑤ **日志页"没成功"≠真没成功**：严格字节窗口（10:13:42 起 396 条）OR **真成功 35 条**（10:15–12:02，全 `stealth/space-bunny-alpha`），最后一次成功后还有 38 行——他翻的是 12:05 之后的尾巴。**读 route_log 只能按字节偏移切窗口**（`ts` 无日期）。
  ⑥ 三动作落地：`api_page.html` 成功判据改为"落点席不在 failures 里"（热读免重启）；`quota_guard.json` 给 `opencode-zen` 补 allowlist 只放 `space-bunny-free`（热加载生效，付费席实测被拦）；埋点四字段**全部生效**：`seat_headers_ms/req_bytes/upstream_id` 先随 PID 19588 上线，12:4x 他点头后 `nssm restart ai-gateway-3100` 成功（PID 19588→22744），`seat_fail_ms` 12:51:38 实测到 `{"groq":1827}`（失败席也记耗时）＋同行 `seat_headers_ms={"cloudflare":1188}`、`upstream_id=id-1790743901115`。
- **2026-09-30 · OpenRouter「一直失败」查因＝网关自己误杀，已修并重启生效**：根因 `api_gateway.py:838-841` 把首字守卫 `GATEWAY_TTFT_TIMEOUT=3.0` 当成 **urlopen 的 socket 超时**传给 `channels.chat_completion(timeout=…)`，而该值覆盖"连接＋上传请求体＋等响应头"。Claude Code 量级请求体（150–300KB，openrouter 走本机 mihomo `127.0.0.1:7890`）实测光上传+等头就要 2.2–4.1s ⇒ 全部**非尾席**被判 timeout；链尾那席拿 `fault_domains.request_deadline_s=180` 所以看着稳。**改法**：拆两个超时——`ttft_limit` 只喂 `_peek_stream_decision`（它自己 `sock.settimeout`，行为不变），新增 `sock_limit=GATEWAY_UPSTREAM_TIMEOUT`（默认 20）喂 `chat_completion`。**隔离复现**（同席位 `stealth/space-bunny-alpha`，免费，max_tokens=8）：300KB @3.0s → TimeoutError；@30s → **200/4.09s**。
  - 失败账口径（`data/api_gateway/route_log.jsonl`，⚠️ `attempted` 是**过滤前的整条候选链**、`resolved_channel` 是**选席时写入**(:822) 都不等于真发过/真成功；ts 只有时分秒，按字符串切窗口会把昨天圈进来，要用字节偏移）：667 条 OR 失败条目＝HTTP 400 ×335(50%，legacy 广播把客户端裸名 `glm-5.3-flash-opencode` 直发 OR，OR 无此名必 400，结果仍落 zhipu/siliconflow)／上传读握手超时 ×187／quota-guard 预过滤 ×76＋测试硬闸 ×4（设计内）／**HTTP 402 ×23 全来自非免费席 `deepseek/deepseek-v4-flash-vision-exp`＝闸门漏拦**／429 ×12＋95% 提前切换 ×5（OR 免费池日限，3 把 key 当日都撞线）。
  - 生效见证：执行体换为 PID 7016（10:12:29，父 nssm.exe），healthz 200；改后严格窗口 10:13:42→11:22:20（224 条决策）内 **OR 真成功 27 条**（全为 `stealth/space-bunny-alpha`，占全部决策 12.1%）、OR 失败留痕 35 条（写超时 14／首字3s 9／空壳 7／guard 3）、**全链无落点 0 条**；同期改前 43 分钟窗口 OR 上传阶段超时是 38 条。真链路经 cc-switch `:15721` 四个 Claude Code 默认名全 200。
  - **进渠道侧对账（2026-09-30，opencli 连郭老师日常 Chrome 看 `openrouter.ai/logs`）三条硬事实**：① OR 侧 `Space Bunny Alpha (stealth)` 的 **TTFT 分布 0.87–3.6s**（prompt 38k–126k token，$0.00，19–90 tok/s）⇒ 网关 **3.0s 首字守卫低于上游真实 TTFT**，10:40(126k tok, 3.6s)、10:08(89k tok, 3.0s) 这类必被掐，窗口内 9 条"首字超过 3.0s"不是偶发。② OR 的 **Upstream Requests 视图全是 200/Attempts=1**——它把错误装在 **200 的 SSE 事件**里回，所以 OR 官网看不到任何"失败"，只有网关侧记成 `流式首包为空壳/错误事件`（OR 10:42 200/243ms ↔ 网关 10:42:38；OR 10:54 200/153ms ↔ 网关 10:54:08，逐分钟对上）。③ 网关 11:41:30 那条 OR write timeout 在 OR 侧**无对应行**＝**请求根本没出境**。
  - **机理纠正（重要，别再照旧结论修）**：`urllib`/socket 的 `timeout` 是**单次 socket 操作**上限，**不是整请求总时长**。实测 8 发 ×512KB 全 200、耗时 13.6–38.8s 却一次没 trip（且全落首席 opencode-zen）。⇒ `write operation timed out` 只在**对端完全停读**超过预算时出现，属**出海链路（mihomo 7890 或直连）真卡死**，**继续调大 `GATEWAY_UPSTREAM_TIMEOUT` 无益**（只会拖慢回落）；直连 curl 测 openrouter 也复现过 3 发里 1 发挂满 20s。
  - **两边数目对不上（未结，别当结论）**：网关严格窗口报 OR 成功 27 条，OR `/logs`（Default Workspace，1d）同期只有 ~13 行；疑该视图按 **workspace/账号作用域**过滤，而网关在 **4 把 key** 间轮换（`data/rate_limit_day.json` 当日记到 3 个不同 key 指纹）。逐条对齐需 **trace-id 配对埋点**。
  - 待裁定三条：① legacy 广播 400 要不要加目录预过滤；② 402 漏闸补闸门；③ `sock_limit=20` 与 key 池逐把重试相乘＝单席最差 80s（改前 12s），要不要收到 8s 或改共享总预算。**重启权限死结见 [[调度大脑记忆/教训/lesson_gateway_restart_privilege_trap]]——它和本页"重启免 UAC"那条正面冲突。**
  - 同轮改动（真源在他处，只留指针）：`data/model_routes.json` 三档免费线现名 **free-flash／free-high**（旧 free-fast/balanced/heavy 已退役，客户端仍发旧名＝**被 `catalog_routes.retired_alias()` 本地硬拒**，`api_gateway.py:666-676` 逐字「本地拒绝，未向任何渠道发请求」、`route_source="retired_alias"`、`attempted=[]`，该分支在 legacy 广播兜底之前触发 ⇒ **不会烧任何上游额度**；2026-10-01 审计修正，原文误写"走 legacy 广播"）；`/v1/models` 暴露 **16** 个路由名；`free-auto`/`auto` 是 **Jev 别名，不在列表里属正常**；cc-switch `gateway-3100` 的 `ANTHROPIC_MODEL=free-auto`、`CLAUDE_CODE_SUBAGENT_MODEL=free-flash`（原为付费线名与死席），Claude Code 读 `~/.claude/settings.json` 的 `*_MODEL`（客户端别名）→ `*_MODEL_NAME`（网关路由名）由 `:15721` 翻译。
- **2026-09-22 · 语音三链 + 方舟额度治理 + 防扣费体系**：voice-asr（groq whisper×2→mistral voxtral→硅基 3 免费款）/ voice-tts（mistral→CosyVoice2）/ voice-chat（zscc Qwen3-Omni 双席，郭老师批准）+ /v1/embeddings（硅基）。方舟 45 模型免费额度盘点入档；**额度警戒闸门 quota_guard 上线**（白名单制 + 方舟最低门槛 ≥250 万 token + 20% 警戒线；zscc/zenmux/openrouter 白名单、8 渠道 deny_all、ark-coding 删除不再续费）——实测点名付费模型三种路径全拦、无扣费失败。每日 ArkQuotaScan 10:17（opencli 抓方舟控制台→回写闸门→破线写渠道警报）。策略文章落 Obsidian：[[调度大脑记忆/流程/workflow_网关安全防扣费策略]]、[[调度大脑记忆/流程/workflow_网关渠道挑选与刷新策略]]、[[调度大脑记忆/流程/workflow_调度大脑交接手册]]、[[调度大脑记忆/项目/project_gateway_现状与展望]]。monorepo 1ffef93。

- **2026-09-21 · 三档免费模型线重建 + 渠道单模型规则**：free-fast/balanced/heavy 三档（members[] 保序回落链，别名直调）；郭老师逐渠道定规则并落成**唯一真源文档 `search_gateway\渠道编排规则.md`**（monorepo 已同步）：zscc 只用 deepseek-v4.1-flash-cc（-cc 后缀才可用，失效须提醒郭老师拍板）、modelscope 只用 DeepSeek-V4.1-Flash、groq 只用 compound(T1首跳 166tok/s 复合智能体+联网)+gpt-oss-120b(T2)（qwen3.8-27b 限流大户已剔）、zenmux 免费白嫖渠道激活（新 key + 每日 00:23 巡检 `ZenMuxFreeScan`，脚本 `scripts/zenmux_free_scan.py`）。能力硬底线=通用模型且 ≥qwen3.8-27b（本尊可过）；规则层级=「只用N个」硬约束优先。探针 revision=6。三档最终 4/12/2 员，热加载免重启。openrouter/cloudflare/xiaohongshu/agnes/longcat/nvidia 同日定稿；zhipu 踢出（账号无套餐，免费仅 glm-4.7-flash 限流凶）；bai 免费期结束（限免也扣credits）打入冷宫，周任务 BaiWelfareCheck 周一 09:17 探监、福利回归报警。每日 ChannelDailyRefresh 00:23 实测编排全量成员。
- **2026-09-08 · 主题体系完整落地（六套 data-style）**：4 主题总览见 `D:\Work\AI平台\apps\api-gateway\docs\主题体系.md`，各主题定义+预览图在 `docs\主题设置-*.md`（黑白建筑极简/云海天舟/星河枢机/月夜穹顶，「归一」已弃）。第六套 `data-style="mono"`（玄白·建筑极简）已在 `api_page.html` 落成并 byte 同步至运行体，浏览器 `http://localhost:3100/` → 🎨 选即见。
- **2026-08-31 · 派发中心二级页 + 删除 dashscope 渠道**。
- **2026-08-30 · 火山方舟 Coding Plan 接入**（49.9/月，单渠道 `ark-coding` 勿拆多；免 UAC 重启；剥离 reasoning_content；`deepseek-paid` 付费链）。
- **2026-08-30 · 待排查**：:3100 路由日志未见调用记录（已记录，任务做通后再查）。
- **2026-08-27 · 镜像站整体迁移**：`ai.wendabao-f.net` 新 UI，text_searcher 镜像设题适配器整体失效（阻塞）。
- **2026-08-27 · Claude Code 前缀模型 id 路由**（provider:model 通用解析）；health 60s 缓存落地；text_searcher 检索阶段修复。
- **2026-08-26 · 渠道限流准入闸门 v2**（rate_limit.py 原子 admission gate）；`/api/search_json` 回归修复。
- **2026-08-25 · 渠道管理自定义渠道/隐藏、光线芯片换模型、全网关皮肤层、网关鉴权（api_key）**。
- **2026-08-24·25 · 前端四套艺术风格主题 → liquid 液态玻璃 + 配色/高级感精修**（详情在归档）。
- **2026-08-24 · 统一模型组 + 光线编排、渠道模型选择三级页、model_overrides、首页三七分、四套风格主题起点**。
- **2026-08-21 · 前端 v3 大改版**（launcher 单屏、黑夜模式、渠道启停、接入信息页）；:3100 补入 runtime.yaml 管理。
- **2026-08-13 · 迁移**：网关迁至 `D:\项目\ai-hub\search_gateway\`，5 opencli 引擎（yuanbao/doubao/kimi/qianwen/metaai）。
- **2026-08-04 · 落地**：由郭老师交接文档驱动搭建，同日升级 v2 多渠道聚合站。

## 源文件

- 完整操作级/踩坑级详情、各轮实现细节 → `项目/归档/project_ai_gateway_完整详细记录.md`
- 主题设计文档/预览图 → `D:\Work\AI平台\apps\api-gateway\docs\`（主题体系.md、主题设置-*.md、预览图-*.png）
- 三拆配置 / 运行数据 → `D:\项目\ai-hub\search_gateway\data\model_catalog.json`、`model_routes.json`、`channel_registry.json`、`quota.json`、`api_state.json`
- 网关服务文档（Obsidian）→ `D:\Work\AI平台\docs\design\AI基础设施\服务\api_gateway.md`、`search_gateway.md`