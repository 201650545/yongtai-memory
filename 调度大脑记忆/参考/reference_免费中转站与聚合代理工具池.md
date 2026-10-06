---
name: reference-免费中转站与聚合代理工具池
description: 白嫖额度三条路线：①国产客户端积分转API(agent2api+loomy2api)②国际工具聚合(CLIProxyAPI/openrelay)③第三方公益中转站候选池(未经审计、含prompt泄露风险)。含OpenRouter在自家网关「登记过但从未跑通」的待办。附各站额度特征与实测来源。
metadata:
  node_type: memory
  type: 参考
  modified: 2026-10-01
---

# 免费额度三路线 · 工具池与候选站

> 建立：2026-10-01。用途：把「不花钱用大模型额度」这件事的三条路线与工具钉在一处，供随时查。**入库即长期待更新，非一次性快照。**

## 〇、总览：三条路线互不重叠

| 路线 | 覆盖 | 工具 | 安全性质 |
|---|---|---|---|
| **① 国产客户端积分** | 小浣熊／Loomy／Qoder／CatPaw | `agent2api` + `loomy2api` | 厂商自家积分，**无第三方中转** |
| **② 国际工具聚合** | Claude Code/Desktop、Copilot、Kiro、Windsurf、Gemini CLI、Codex | `CLIProxyAPI` / `openrelay` | 用你自己已订阅的额度，**凭据不出本机** |
| **③ 第三方公益中转站** | 各类免费模型 | ⛔ **别人运营的公共站** | 🔴 **未经审计，prompt 会流经对方** |

⚠️ 郭老师 2026-10-01 定标：**优先 ①②（走自有额度，隐私边界清楚）**，③只当「待验证候选池」，不入日常主链。

---

## 一、路线① 国产客户端积分转 API

**机制**：厂商客户端已登录 → 读本机登录态 → 转 OpenAI 兼容 API。**算力与积分仍是厂商的**，只换消费口。

| 工具 | 语言 | Star | 覆盖 |
|---|---|---|---|
| **`aimod-cc/agent2api`** | Rust | 190 | 小浣熊(`raccoon/`)＋Qoder(`qoder/`)＋CatPaw＋WorkBuddy |
| **`wangliangdong/loomy2api`** | Python | 7 | 仅 Loomy（多账号配额感知负载均衡） |

🔴 **Buddy2api 是弯路**（2026-10-01 源码核实）：`providers/` 只有 `qclaw`/`qwenwork`/`traework`/`workbuddy`，**不含小浣熊/Loomy/Qoder**；而郭老师不接 WorkBuddy ⇒ **装了也白装**。
⚠️ **小浣熊只能手动填凭证**：agent2api README 明写「小浣熊网页登录与导入本机桌面端登录态**不可用**」⇒「一键扫本机登录文件」对这一家不成立，别设计成全自动。
⚠️ **实际需跑两个网关**（agent2api :8788 ＋ loomy2api :8789），不是一个。

---

## 二、路线② 国际工具聚合代理

| 工具 | 核实结果 |
|---|---|
| **`router-for-me/CLIProxyAPI`** | ✅ Go，**★53689**，更新 2026-10-01。转 OpenAI/Gemini/Claude/Codex/Grok 兼容接口，覆盖 Antigravity／Codex／Claude Code／Grok／Muse／Davin |
| **`romgX/openrelay`** | ✅ TypeScript，★2306，**MIT**，更新 2026-09-19。接 **11 家本地配额**（Claude Desktop／Claude Code／Kiro／Windsurf／Antigravity／OpenCode／VS Code Copilot／OpenAI Codex／Gemini CLI／Rovo Dev／QClaw）＋ **45 个直连 API**（Groq／Gemini／DeepSeek／Mistral／OpenRouter／Ollama 等） |

**凭据安全**：openrelay README 第 165 行——「应用 token/cookie 从你的机器读取，只用于连接原供应商。通过 OpenRelay 添加的 API Key 存储在本机 `~/.openrelay/` 配置中」⇒ **落盘，不是纯内存**。（网传「凭据只在内存处理」的说法不实。）

🔴 **CLIProxyAPI README 塞满赞助商中转站广告**（PackyCode／AICodeMirror／APIKEY.FUN／FennoAI／Cubence／Aiberm／PatewayAI／OpenLux）——**全是商业付费中转**，郭老师长期记忆 `project_cost_strategy` 已定**不买付费 AI 订阅**。⚠️ **只取其免费额度聚合能力，别被 README 带偏**。

---

## 三、路线③ 第三方公益中转站候选池 🔴

> **性质：别人运营的公共站，非自建、服务器代码不可审计。**
> 郭老师 2026-10-01 拍板：入库为**候选池**，非已批准通道。**接入前须自己拍板。**

### 3.1 两个情报来源（已核实）

| 来源 | 核实 |
|---|---|
| **`kirito8/free-newapi`** | ✅ GitHub，MIT，★39，创建 2026-09-04 / 更新 2026-10-01。**是导航站不提供服务**，收录免费/公益中转与额度清单 |
| **`blog.200205.net/blog/ai/free-ai`** | 第三方博客，收录 12 个站（见下表） |

### 3.2 候选站清单（来自博客，2026-10-01 收录，**未测试**）

| 站点 | 免费额度 | 备注 |
|---|---|---|
| AgentRouter `agentrouter.org` | 签到 25/日，邀请 150 | — |
| AnyRouter `anyrouter.top` | 签到 25/日，邀请 50 | 老牌，**仅 CC 可用** |
| 哈吉米AI `api.gemai.cc` | 邀请码 100，签到 5~9/日 | 价格高但过程稳定 |
| Conduit（TG 机器人） | 注册 500 | Gpt 速度快 |
| SeekAI `seekai.cc` | 邀请码 200，签到 20/日 | — |
| JustDoWork `api.justwoker.icu` | 邀请码 200，签到 5~9/日 | — |
| **TokenRouter** `tokenrouter.com` | 号称真正无限免费（kimi v3／deepseek v4 pro 等） | ⚠️ **博客明确警示：长上下文会「文字混乱」，不建议接 agent** |
| **FreeBuff** `freebuff.com` | DeepSeek V4 Flash 约 3 小时/日 | ⚠️ 近期香港不可用，需美国节点 |
| OrcaRouter `orcarouter.ai` | 免费模型少 | 速度非常快 |
| Nvidia `build.nvidia.com` | 少量模型（智谱） | 官方站，相对可信 |
| 免密钥 IP 站 ×2 | 不用 key | ⛔ **博客自己标注「这些 AI 都不建议使用」** |

### 3.3 🔴 风险（博客自述 + 本库判据）

- 博客原话：「**公益中转站的安全性无法保证，请注意数据或隐私安全**」，并引用先知社区《API 中转站投毒的攻击链深入分析》。
- **核心风险**：中转站运营方**能看到全部 prompt 与 API Key**；多数靠「签到送余额＋邀请返利」运营，**有拉新动机**。接入=把代码、上下文、文件内容流向第三方。
- 与 `D:\Work\通用规范\40-安全红线.md` 第 2 条（密钥/凭据不入文档）精神相悖——**需郭老师逐站拍板后方可接入**。
- ⚠️ **本清单未做任何实测**（未注册、未调用）。数字与限制均为博客转述，**引用前须自行验证**。

---

## 四、🔴 待办：OpenRouter 在自家网关「登记过但从未跑通」

2026-10-01 实测 `D:\项目\ai-hub\search_gateway\`：

| 文件 | 结果 |
## 四、✅ OpenRouter：网关内**已深度集成**（2026-10-01 复核，前一版本节结论有误已纠正）

⚠️ **本节曾误记「登记过但从未跑通」，已作废。** 错因：只查了 `channels.json` 就下结论，漏了 `model_routes.json`（路由真源）与整套 OpenRouter 专用设施。**郭老师当场纠正「API转发网关中的注册渠道不是有吗」——教训：判「某渠道有没有接」必须扫全 `data/`，不能只看一个文件。**

**实测真相：OpenRouter 是网关的活跃深度集成渠道，有一整套专用设施，且巡检到当日。**

| 文件 | 实测内容 |
|---|---|
| `data/openrouter_free_models.json` | **2026-10-01 12:00:03 自动巡检**。判定规则：*pricing 递归摊平后全部数值字段为 0 才算免费*（含 `overrides` 阶梯价／`audio`／`image`／`web_search`／`input_cache_read/write`）；再剔除 `DENY_PREFIXES` 钦定伪免费。结果 `count: 17` / `catalog_total: 462` |
| `data/openrouter_free_audit.json` | 全目录费用审计（**不参与放行判定**）：462 个中 **442 个收费**，逐个列明哪些字段收费 |
| `denied_pseudo_free`（已剔除） | `thinkingmachines/inkling-small:free`、`thinkingmachines/inkling:free`、`openrouter/free` |
| `data/probe_budget_openrouter.json` | 探针预算 |
| `data/model_routes.json`（15 处）／`data/orchestration_state.json`（12 处）／`data/quota_guard.json`／`data/model_pricing.json`／`data/gateway_resources.json`／`data/promos.json`／`data/rate_limit_day.json`／`data/daily_probe_state.json` | 路由真源、编排状态、限额、防扣费、促销、日巡检**全线接入** |
| `data/channel_registry.json` | `channels/openrouter` = `enabled:true, registered, quota:free`（该文件只记粗粒度状态，`health:unknown`／`last_success:null` **不代表未接通**，别据此下结论） |

**已识别的真免费模型（17 个，2026-10-01 实测）**：`stealth/space-bunny-alpha`(ctx 1M)、`inclusionai/ling-3.0-flash-sante:free`(262144)、`qwen/qwen3.8-27b:free`(262144)、`nvidia/nemotron-3-*`、`google/gemma-4-*`、`cohere/north-mini-code:free`、`poolside/laguna-*`、`dots-studio/dots-3-note-preview:free`、`google/lyria-3-*-preview` 等，详见 `data/openrouter_free_models.json`。

🔴 **别用粗筛替代它的判定**：手工 `pricing.prompt=="0" and pricing.completion=="0"` 会多捞出 3 个**已被它拉黑的伪免费**，且会漏掉递归摊平才准的 overrides/audio/web_search 类伪免费。**引用免费名单一律读 `data/openrouter_free_models.json`，不要现拉现算。**
⚠️ 名单每日 12:00 自动刷新，引用须带 `checked_at` 日期。

⚠️ **改网关前必读**：`:3100` 由 NSSM/LocalSystem 持有（记忆 `lesson_gateway_restart_privilege_trap`：stop 脚本会打印成功却静默失败并照样写停止标记）；`quota_guard` 有三层防扣费防线。**先备份 `channels.json`，改完不要立即重启**。

---

## 五、纪律（接任何新源前必过）

1. 🔴 **禁一切可见弹窗**（`feedback_no_popup_windows`）——后台一律 pythonw／`-WindowStyle Hidden`／`CREATE_NO_WINDOW(0x08000000)`；**判活走端口不走 CommandLine**。
2. 🔴 **凭据（cookie/token/key/base_token）不入记忆库、不入公开仓**（`40-安全红线` 第 2 条）。本条目已刻意不含任何真实凭据值。
3. 🔴 **任务中途不切模型**——切换会重读上下文、烧大量 tokens。
4. ⚠️ **Qoder 排队伪装成超时**：排队时第三方 Agent 显示「无响应」而非「排队中」，易误判成 API 挂了（平台问题非软件问题）。
5. ⚠️ **切换成本**：Buddy2API/loomy2api 等是独立网关，别与应用共用端口（建议 8788／8789）。

**关联**：[[project_three_tier_free_models]]（⚠️ 断链，目标不存在，2026-10-01 审计）、[[reference_zenmux_free_models]]（⚠️ 断链，目标不存在，2026-10-01 审计）、[[reference_本机本地模型清单]]、[[feedback_model_policy]]、[[project_cost_strategy]]、[[feedback_task_completion]]、[[lesson_gateway_restart_privilege_trap]]、[[project_贾维斯中控]]

**锚点**：网关运行体 `D:\项目\ai-hub\search_gateway\`；实测交接单 `D:\Work\项目索引\rounds\交接_工具项目与DSH截断修复_给执行Agent_20261001.md`