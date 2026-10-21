---
name: reference-Tabbit本地模型回环反带
description: Tabbit Browser 内置 Local Agent 的模型 API 反带成果：本地回环（127.0.0.1:<port>/v1，OpenAI Responses 协议）、token 在 Tabbit 进程环境变量 TABBIT_LOCAL_AGENT_LOOPBACK_TOKEN、Codex 风格 model_providers.tabbit-local 配置模板、云端四步协议（challenges/exchange/models/responses）、启动门槛链（账号 token→installation key→challenge/exchange→catalog→default model，且是实验特性开关），以及 buddy2api 侧 provider tabbit 的落地状态（代码就绪、默认未启用、等实测）。
type: reference
updated: 2026-10-21
---

# Tabbit Local Agent：模型 API 反带（2026-10-21）

> **2026-10-21 18:3x 结局：郭老师决定不做，并让我把 Tabbit 浏览器卸载了**
> （原话：「那算了，不搞他了吧，额度又不多，难度又很大」）。
> ⇒ 浏览器已卸载（官方卸载器 + 清 AppData/计划任务/注册表）；
> ⇒ buddy2api 侧的 `providers/tabbit/` 与 `scripts/tabbit_selftest.py` **已一并删除**
> （浏览器没了 ⇒ 该渠道永远跑不起来，留着是死代码）；能力总账里的登记也已撤销。
> **本文件留作"方法与机制"留档**：如果哪天重装 Tabbit，下面 §二/§三/§四·补 的反带结论
> 能直接省掉两小时考古（协议四步、开关 pref 名、门槛链都写在这儿了）。
> ⚠️ 本文件里的"buddy2api 侧落地代码"一节已作废（代码已删）。

> 起因：郭老师装了 Tabbit，问"这个程序里的 API 可以反带出来吗" ⇒ 反带成了，
> 并在 buddy2api 里落成第 9 个渠道的代码（**默认未启用**，等实测）。

## 一、Tabbit 是什么（别和网页版搞混）

| 部件 | 位置 | 干什么 |
|---|---|---|
| 浏览器 | （浏览器 exe，**已卸载·路径已不存在**）（Chromium 内核，1.17.16.0） | 带原生侧栏的 AI 浏览器 |
| **TabbitDance**（本地代理运行时） | `…\Application\1.17.16.0\TabbitDance\`（自带 89MB `node.exe`） | 跑 **DSH（DeepSeek Harness）**；`agent-provider-claude.mjs` / `-codex.mjs` / `-cursor.mjs` / `-workbuddy.mjs` ⇒ **它的模型后端是你本地的 Claude Code / Codex / Cursor / WorkBuddy** |
| CLI | （Tabbit LocalAgent 的 CLI，**已卸载·路径已不存在**） | 官方只读诊断 + Playwright 驱动（`create` / `nodejs` / `tabs` / `diagnose` / `finish`） |
| 本地 runtime 服务 | 命名管道 `\\.\pipe\tabbit-public-<hash>-<gen>`（token 在 `…\User Data\LocalAgent\endpoint.json`） | 浏览器 ↔ 本地 agent 的控制面（**不是模型 API**） |
| 网页端 | `https://web.tabbit.com/`（落地页）、`https://www.tabbit.com/`（官网/会员权益/妙招广场/学生专区） | 营销站；**登录态与浏览器原生面板是不同会话** |

⚠️ profile 里的三个扩展是 **AutoGLM / Microsoft Power Automate / 薅羊毛**，**都不是 Tabbit 的面板** ⇒
Local Agent 面板在**浏览器原生 UI**里，Playwright 够不着（只能看网页内容）。

## 二、反带到的四件核心（来源：`Tabbit.dll` 里的 `codex_local_agent_gateway.cc` 字符串）

1. **上游 = 本地回环**：`http://127.0.0.1:%d/v1`（端口运行时挑）
   ⇒ **不必复现云端签名**（浏览器自己签云端），只跟本地说话。
2. **协议 = OpenAI Responses**（`wire_api="responses"`）⇒ 不是 chat/completions
   （所以在二进制里搜 `/v1/chat/completions` 是 0 命中，别当成没有 API）。
3. **认证 = 进程环境变量**：`TABBIT_LOCAL_AGENT_LOOPBACK_TOKEN`；
   Tabbit 给 agent 写的配置里 `auth={command="cmd.exe", args=["/d","/c","echo %TABBIT_LOCAL_AGENT_LOOPBACK_TOKEN%"], timeout_ms=5000}`；
   `requires_openai_auth=false`。
4. **配置模板（Codex/DSH 风格）**：
   ```toml
   model_providers.tabbit-local = { name="Tabbit Local", base_url=<回环>,
       wire_api="responses", requires_openai_auth=false, supports_websockets=false,
       auth={command="cmd.exe", args=["/d","/c","echo %TABBIT_LOCAL_AGENT_LOOPBACK_TOKEN%"], timeout_ms=5000} }
   shell_environment_policy = { inherit="core", exclude=["TABBIT_LOCAL_AGENT_LOOPBACK_TOKEN"] }
   ```

## 三、云端协议（备用路，设备绑定，难度高）

`https://web.tabbit.com/api/v1/local-agent-runtime/`：

| 步骤 | 方法/路径 | 关键字段 |
|---|---|---|
| ① 挑战 | `POST .../challenges` | `challengeId` / `audience` / `exchangeVersion` / `applicationProof` / `methods`(`installation-pop-v1`, `local-mock-v1`) |
| ② 换 token | `POST .../exchange` | `publicKeySpki` / `device-key-bound-v1` / `local-development-only` / `evidence` / `deviceKey` |
| ③ 模型目录 | `GET .../models` | `If-None-Match` → `ETag` / `X-Tabbit-Applied-Catalog-Revision` |
| ④ 推理 | `POST .../responses` | `text/event-stream`（SSE）+ `Idempotency-Key` + `X-Client-Request-Id`（小写 UUID）+ `X-Tabbit-Catalog-Revision/Etag` |

无凭据直打会得到 `400 protocol_contract_violation`（"请求字段不符合 local agent gateway 契约"）⇒ 端点活着，缺的是合规签名请求。

## 四、启动门槛链（**缺一不可**，缺哪个都起不来）

```
LoadCacheAndStartServer → StartLoopbackServer
  ① "Failed to fetch the Tabbit account token"   ← 需要 Tabbit 账号登录（web 端会话）
  ② "Cannot load Local Agent installation key"    ← 本地设备密钥
  ③ /challenges → ④ /exchange → ⑤ /models(ETag)
  ⑥ "Local Agent Gateway has no verified model catalog"
     "Tabbit Local Agent has no models published by the Local Agent Gateway"
     "Local Agent has no effective default model"  ← 目录里得有一个可用模型
另外：Local Agent 是**实验特性**（"valid Local Agent experimental feature"）
```

**2026-10-21 实测状态**：Tabbit 10 个进程在跑，但 **0 个 TCP 监听**、磁盘上没有 Profile-private
`config.toml`、Tabbit 进程环境里**没有** `TABBIT_LOCAL_AGENT_LOOPBACK_TOKEN` ⇒ 回环没起来。
原因：`web.tabbit.com/login` 明确显示**「登录状态已失效」**（账号 `190****0185`）——
**网页端会话 ≠ 浏览器原生面板的登录态**，两套。

## 四·补：那个"实验特性开关"到底是什么（2026-10-21 晚追加）

**不是 UI 开关，是一组 Chromium pref**（在 `Tabbit.dll` 的 pref 注册表里，和
`tab_operations.*`、`vertical_tabs.*` 排在一起）：

```
tabbit.local_agent.enabled            ← 就是它
tabbit.local_agent.permission_mode / permission_profile / model / reasoning_effort
tabbit.local_agent.working_directory / collaboration_mode / service_tier / personality
tabbit.local_agent.projects
tabbit.local_agent.config_defaults_version / config_default_entries
tabbit.local_agent.installation_id / installation_wrapped_key   ← 首次启用时浏览器自动生成，别手填
```

- DLL 里那句 **"Invalid Local Agent experimental feature"** 是**报错文案**（不是开关名），
  说明"实验特性"是这个设置对象里的一个字段。
- ⚠️ `Local State` 的 `browser.enabled_labs_experiments` = **null** ⇒ **与 chrome://flags 无关**。
- 2026-10-21 实测：改之前 `Default\Preferences` 的 `tabbit` 段是**空的**（这些 pref 一个都没写过），
  说明 Local Agent **从未被启用过**。
- **开启方法（已实测，pref 能保住）**：
  1. **先完全退出** Tabbit 浏览器（Chromium 退出时会把内存里的 pref 写回，覆盖手改值）
  2. 改 `…\User Data\Default\Preferences`：把 `tabbit.local_agent.enabled` 置 `true`
     （备份留在同目录 `Preferences.bak-tabbit`）
  3. 再启动浏览器 → 实测 `enabled=True` 保住了
- **但开了还不够**：Local Agent 仍然没起（0 监听、无 `config.toml`、TabbitDance node 的 env 里
  没有 `TABBIT_LOCAL_AGENT_LOOPBACK_TOKEN`）⇒ **卡在账号**：
  - 网页端 `web.tabbit.com/login` 显示「**登录状态已失效**」（账号 `190****0185`），
    点「恢复登录」只跳回落地页（**它要唤起桌面端确认**，网页端自己不做），
    抓到的唯一请求是 RUM 埋点 `rumt-zh.com/speed`。
  - ⚠️ **网页端会话 ≠ 浏览器原生面板的登录态**（两套）。`Preferences` 里
    `web.tabbit.com` 的 `site_engagement.visits=12`、`pointsAddedToday=15` ⇒ 网页端他确实用过。
  - 恢复登录的唯一入口在**客户端原生 UI**（Playwright 够不着；他的
    `chrome://settings/aiFeatures` 标签页属于他自己会话，`tabbit-cli claim` 报 CLAIM_FAILED）。

## 五、buddy2api 侧落地的代码（2026-10-21 写，**18:3x 已全部删除**）

当日写过一版 provider（`constants.py` / `runtime.py` / `chat.py` / `store.py` / `__init__.py` ＋ 自检脚本），
注册进 `providers/__init__.py` 的 `_LOADED` ＋ `providers/protocol.py` 的 `KNOWN_CHANNEL_IDS`。
**2026-10-21 18:3x 郭老师定「不搞了」并让我卸载浏览器 ⇒ 这批代码已一并删除**
（浏览器没了 ⇒ 该渠道永远跑不起来，留着是死代码），能力总账里的登记也已撤销。
**本节只留设计记录；将来重建时按 §二/§三/§四·补 的结论即可复现。**

设计要点（供重建）：

- **回环解析**：借道 `tabbit-cli nodejs`（跑在 TabbitDance 的 node 进程里 ⇒ 环境变量天然继承）读 env；
  拿不到 base_url 就去 `User Data` 里找它写的 `config.toml`；都没有 ⇒ 明确报未就绪。
- **协议翻译**：chat.completions ⇄ **Responses**（messages→input、system→instructions、SSE→chunk）。
- **伪账号**：在 `accounts` 表维护一个本地伪账号（token 走库里加密通道落库）。
- **自检**：解析回环 → GET /v1/models → 真打一次 /v1/responses；没就绪就退出码 1 并说明要做什么。
- **默认不进 `DEFAULT_PROVIDER_IDS`**（上游未就绪 ⇒ 挂上去就是 503 假绿）。

## 六、结局（2026-10-21 18:3x）

郭老师定「那算了，不搞他了吧，额度又不多，难度又很大」→ 浏览器已卸载（官方卸载器 ＋ 清 AppData 396MB ＋
更新计划任务 ＋ 注册表）＋ 这批代码删除 ＋ 能力总账登记撤销。**本文件留作方法留档**（重装 Tabbit 时能省两小时考古）。

## 七、顺带发现（额度入口）

`www.tabbit.com/membership`（会员权益，落地页写"体验版 注册即可"）、`skills.tabbit.com/plaza/skills`（妙招广场）、
`go.tabbit.com/student-skills`（学生专区）、`web.tabbit.com/ukm` `/uma`（**API 路径，网页上是 404**）。
