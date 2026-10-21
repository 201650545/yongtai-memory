---
name: reference-免费共享镜像站整体撤销与收口
description: 2026-10-20 郭老师定调「免费镜像站被薅光了，不要搞了」⇒ 把别人共享的免费渠道整体撤销（7 渠道 / 3 路由 / image-gen 回落链成员 / 14 条自定义别名），只留自己账号额度；含策略结论、可逆方式、脚本与备份坐标、热重载 401 的坑。后记补 River AI 接入（自己付费额度进 high 链）与「网关把模型名整体转小写致上游 404」的通用 bug。
type: reference
updated: 2026-10-20
kind: reference
status: active
---

# 免费共享 / 镜像站：整体撤销与收口（2026-10-20）

> 一句话：**别人的额度不算额度。** 免费共享站、公益站、镜像站一律不再纳入网关；
> 只留自己账号的渠道。撤销可逆，脚本仍在。

## 一、为什么撤（郭老师原话与判据）

郭老师 2026-10-20 指示：**「免费镜像站被薅光了，不要搞了」**。

支撑这个判断的三条事实（都是本轮之前实测到的，不是推测）：

1. **额度的所有权不是自己的**：48Team 共享席位的 4 个 5 小时窗口在撤销前**全部 100% 用满**；
   别人的池子说没就没、说关就关，自己没有任何处置权。
2. **占着自动回落链会拖慢主业务**：生图 `image-gen` 链里挂着公益站成员，
   上游一挂（`503 overloaded`）或余额一空（`403 Insufficient user quota`），
   **每次都先撞一遍死站再降级** ⇒ 生图端到端被拖长，且失败原因被掩盖成「生图不稳定」。
3. **被薅是常态而不是意外**：公益站的存活周期由站主和羊毛党决定，
   「今天能用」这件事本身不构成可用性保证。把它当基础设施用，等于给自己埋定时故障。

## 二、撤掉了什么

### 7 个渠道

| 渠道 id | 是什么 | 撤销前的实测状态 |
|---|---|---|
| `cpa` / `cpa-a1` / `cpa-a2` / `cpa-b1` / `cpa-b2` | 48Team 共享席位 relay（别人分享的 4 把席位 key） | 4 席 5h 窗口**全部 100%**，池子当天已被调用 3005 次 |
| `loveyy` | 生图公益站 | 余额 **$0**，`403 Insufficient user quota`，要领额度得先有兑换码 |
| `l0veyou` | 公益站（文本） | 上游**长期 `503 overloaded`**；生图对本账号分组 `403`（未开放） |

### 3 条路由

`cpa`（文本）、`cpa-image`（生图）、`l0veyou`（文本）——整条删除，不是停用。

### 生图自动回落链里的成员

把 `loveyy` / `gpt-image-2.5` 这一席从 `image-gen` 的 members 里**摘掉**。

撤销前的链（6 席）：

```
sensetime u1.5-fast → cloudflare flux-1-schnell → sensetime u1.5-lite
  → agnes image-2.5 → loveyy gpt-image-2.5（本轮摘掉）→ imgpseudo 豆包
```

摘掉后剩 5 席，全部是**自己账号**的额度。这是本轮唯一一处"改别人的链"，
判据是：**自动回落链只放自己可控的额度**，共享站再快也不进链。

### 14 条自定义模型别名

指向这些渠道的自定义别名一次性删除（`loveyy` ×2 / `l0veyou` ×2 / `cpa` ×10），
**`nvidia` 那条保留**——它不是共享站，是自有渠道。

## 三、保留了什么（撤销后的全部家底）

撤销后 `/v1/models` 只剩 **10 条**，`cpa` / `loveyy` / `l0veyou` **零残留**：

- 语音族 7 条：`voice-asr` / `voice-tts` / `voice-clone` / `voice-caption` / `voice-translate` / `voice-chat` / `voice-realtime`
- 生图：`image-gen`
- 文本：`flash`、`high`

渠道侧保留的全是**自己账号**的额度：商汤（日日新）/ Cloudflare Workers AI / AGNES /
豆包 / 元宝 / 即梦 / traework / workbuddy / qwenwork。

## 四、策略结论（长期有效，别再问"要不要接一个免费站"）

1. **免费共享站 / 公益站 / 镜像站不再纳入**网关。
   - 不因为「现在能用」「额度写着 unlimited」「模型名很猛」而动心。
   - 尤其不吃「4 席轮转 = 4 倍可用性」这类算术——那 4 倍是别人的余量，不是你的容量。
2. **只认自己账号的额度渠道**：商汤 / Cloudflare Workers AI / AGNES / 豆包 / 元宝 /
   即梦 / traework / workbuddy / qwenwork 这一类——账号在自己手上，额度规则可查、可续、可预期。
3. **自由额度共享站即使要留，也只能做「点名 / 路由」，绝不进自动回落链。**
   自动链是无人值守的路径，把别人的额度接进去 = 让主业务替别人的限流买单。
4. **风向变了要整体撤，不要一个个试**：本轮是「7 渠道 + 3 路由 + 链成员 + 14 别名」一次清干净，
   并按「渠道 / 路由 / 链成员 / 别名」四层分别校验零残留——只删渠道会留下幽灵模型条目。

## 五、可逆方式（想开随时一条命令接回来）

撤销是**数据层删除 + git 提交**，接线脚本一直留在仓库里，不是能力性删除：

- 接回共享席位：`wire_cpa_seats.py`
- 接回外部公益站：`wire_external_stations.py`
- 撤销/回滚的执行体：`drop_free_mirror_channels.py`

三个脚本的绝对路径与备份见下节。若要用备份整体回滚，把 `*.bak-dropfreemirror-20261020`
三个文件覆盖回原名，再热重载 3100 即可。

## 六、坐标：脚本、备份、key 在哪

| 项 | 位置 |
|---|---|
| 撤销脚本（已提交 git） | `D:\项目\ai-hub\search_gateway\scripts\drop_free_mirror_channels.py` |
| 接回共享席位 | `D:\项目\ai-hub\search_gateway\scripts\wire_cpa_seats.py` |
| 接回外部公益站 | `D:\项目\ai-hub\search_gateway\scripts\wire_external_stations.py` |
| 备份 · 渠道 | `D:\项目\ai-hub\search_gateway\data\channels.json.bak-dropfreemirror-20261020` |
| 备份 · 路由 | `D:\项目\ai-hub\search_gateway\data\model_routes.json.bak-dropfreemirror-20261020` |
| 备份 · 别名 | `D:\项目\ai-hub\search_gateway\data\model_overrides.json.bak-dropfreemirror-20261020` |
| 渠道与 key 的实际存放 | `D:\项目\ai-hub\search_gateway\data\channels.json`（`data/` 在 .gitignore 里） |
| 网关 master key 的存放 | `D:\项目\ai-hub\search_gateway\data\api_state.json` 的 `api_key` 字段 |

**本仓不记任何 key / token / cookie 值**（`D:\记忆` 是公开镜像）。要知道「key 存在哪个文件、
归哪个渠道」请看上表，值去那台机器上取。

## 七、热重载的坑：`POST /api/gateway/reload` 要 Bearer key

- 热重载接口是 **需要鉴权**的：`POST http://127.0.0.1:3100/api/gateway/reload` 必须带
  `Authorization: Bearer <api_state.json 的 api_key>`。
- 脚本里那段 `urllib` 请求**不带 key ⇒ 401**，看起来像「热重载失败」，其实是网关自己的鉴权拦的。
  ⇒ **手动带上 Authorization 头再发一次**，然后等 NSSM 把服务拉起来（约 3~6 秒），
  不要因为 401 就判定改配置没生效。
- 判定生效的硬证据是 `/v1/models` 的条目数（本轮从含共享站降到 10 条），不是「脚本打印了成功」。

## 八、撤销后的复验（只跑 1 次，别反复烧额度）

生图回落链改完复验 1 次：`image-gen` **10.4s 出图成功**，实际走 `agnes-image-2.5`，
返回 **url 形态**（`b64_json` 是空串）——**这是正常的**，AGNES 本来就只给 url，
消费方要能吃 url（b64 缺失时下载再转 base64）。详见 [[项目/project_image_gen_routes]]。

## 九、与其他条目的关系（口径以本条为准）

本条是**撤销结论**，优先于撤销前的接入记录。以下条目描述的是**撤销前的状态**，
其中的 `cpa*` / `loveyy` / `l0veyou` 渠道、路由、链成员、别名**现在都不存在了**，
当历史看，别照着接：

- [[参考/reference-CPA共享席位-4席轮转_20261020]]（共享席位接入，已撤）
- [[参考/reference-外部公益站接入-l0veyou与生图公益站_20261020]]（两个公益站接入，已撤）
- [[参考/reference-外部免费渠道-linuxtodo与公益站_20261020]]（侦察清单，渠道已撤）
- [[参考/reference-linuxdo福利羊毛清单-20261020]]（羊毛清单，渠道已撤）

**若别处仍把 `loveyy` 写在 `image-gen` 链里，那是撤销前口径**，以本条与
`D:\项目\ai-hub\search_gateway\data\model_routes.json` 的实际内容为准。

## 关联

- 生图链路现状：[[项目/project_image_gen_routes]]
- 成本与额度取向：[[项目/project_cost_strategy]]
- 撤销脚本：`D:\项目\ai-hub\search_gateway\scripts\drop_free_mirror_channels.py`
- 本轮流水：`轮次记录/2026-10-20.md`（免费共享站撤销段）
- River AI 接入（本轮随后完成，见下节）：自己的付费额度，已进 `high` 链

---

## 十、后记：River AI 接入与本轮暴露的通用 bug（2026-10-20 20:45）

撤销共享站之后，同一轮里补了一条**自己账号**的付费渠道 —— 这条正好是上面
「只留自己账号额度」策略的正面样本，两条一起读才完整。

### 10.1 River AI 是什么、怎么落的

- 站点 `console.river.ai`（控制台）／`api.river.ai/v1`（OpenAI 兼容），注册送 $25 试用额度。
- 由郭老师**本人注册**（邮箱 + 可能的手机验证，AI 做不完），key 由我用 opencli 在
  `console.river.ai/keys` 页自助建成（不甩给用户）。
- 落地形状：渠道 id `river`，**归 3100 管**（不是 8787 的 provider），已进 `high` 回落链第 3 位。
- 实测：`POST :3100/v1/chat/completions {"model":"high"}` → 5.3s 回 `pong`；
  点名 `{"model":"river/zai-org/GLM-5.3-Flash"}` → 5.7s 回 `pong`。
- 可用模型：`zai-org/GLM-5.3-Flash` 200；`deepseek-ai/DeepSeek-V4.1-Flash` **上游 503**（River 侧未就绪，非本地问题）。

### 10.2 踩到的通用 bug：网关会把模型名整体转小写

**现象**：同一个请求，直打 `api.river.ai` 200，经 3100 必 404 `model_not_found`。

**根因**：`search_gateway/services/channels.py` 的 `model_providers()` 第一步
`q = model_name.strip().lower()`，把整个模型名转小写后才交给 `_resolve_prefixed_model()`
剥渠道前缀 —— 剥出来的尾部已经是 `zai-org/glm-5.3-flash`，而 **River 的模型名大小写敏感**。

**影响面**：凡上游模型名带大写的渠道都会踩（River、NVIDIA NIM 等）。这类渠道以前
接得少，所以一直没暴露。

**修法**（commit `4818cb1`）：前缀比较用小写、**尾部原样保留**；
`model_providers()` 保留原始大小写的 `raw` 走前缀解析，`q` 只用于包含搜索。

**记住判据**：以后接任何「上游模型名带大写」的渠道，先点名打一发验证，
别等它被塞进回落链才发现。`a/b` 这种两层斜杠的模型 id 尤其要盯。

### 10.3 两个操作层的坑

1. **`chrome-error://chromewebdata/` 是中间态，不代表页面坏了**。
   `console.river.ai` 加载时会先跳 `auth.console.river.ai`，opencli 读 `location.href`
   拿到的是这个错误页 URL，**但页面其实正常渲染了**（截图一看就是 Sign up 表单）。
   别被 URL 骗，截图确认。
2. **`sync_dsh_profile.py` 会改默认模型**。它会把 `agent-default-model` 从
   `deepseek-official/deepseek-flash` 改成 `workbuddy-intl/deepseek-v4.1-flash`
   （因为前者不在 buddy2api 的 `selected_models` 里）。**每次跑完同步都要还原**，
   否则用户的默认模型被静默换掉。

### 10.4 归属原则（这条值得单独立住）

**river 这类渠道不进 8787 的 `selected_models`**。`selected_models` 管的是 8787 自己的
provider 池（workbuddy / qwenwork / loomy …），river 是 3100 侧的外部 API 渠道，
通过 `high` / `flash` 编排路由被调用。放错地方会造出**幽灵条目**：
8787 的 `/v1/models` 里查不到、DSH 里却有，选到就 404。
