---
name: cherry-dsh-sync
description: Cherry Studio ↔ DSH ↔ API 网关模型关系 — 2026-08-25 起 DSH 只连本地网关 :3100（不再直连 7 provider）；zenmux 渠道接入；OpenRouter key 池；web_search 走 :3000 聚合
metadata: 
  node_type: memory
  type: project
  originSessionId: f278da07-fa93-4c68-a18a-ce5d52941e3a
  modified: 2026-09-01T10:28:44.191Z
---

# Cherry Studio ↔ DSH ↔ API 网关 模型同步（2026-08-25 架构变更）

**⚠️ 2026-08-26 web_search 已接 :3000 聚合搜索**——三件套：`/api/search_json` 端点 + `~/.dsh/search-stage/` 插件（源码；**改后必须 cp 到 `~/.dsh/profiles/web/node_modules/hub-web-search/index.js` 安装副本**）+ profile patch（insert hub-web-search 行、`web.searchProvider=hub`、tool-web 解禁+180s）。聚合单次 60-155s，超时预算三层都要 ≥180s：base bundle、**三个 agent 预设**（apps/cli/config/agent-presets/*/agent.cordis.yml，web 会话工具实例来自预设子树而非根树——根层 patch 够不到）、profile patch。曾因预设残留 60000 导致「探针全对但会话必 60s 超时」。引擎波动：元宝/豆包常页面超时属正常，kimi/千问稳。

**⚠️ 2026-08-25 二次演进：DSH 选择器 = 网关统一编排组自动同步**——`channels.py` 的 `set_unified_model`/`delete_unified_model` 已挂钩 `sync_dsh_models()`，编排一保存就把 `unified_models.json` 的组名（id）+ display（显示名）写进 `~/.dsh/settings.yaml` 的 local-gateway.models，DSH 热重载免重启；默认模型被删自动回落第一项；全删空不清空 DSH。**依赖网关解释器装 PyYAML**（workbuddy python 3.13.12 已装 6.0.3；换解释器/升级后要重装，否则静默不同步）。同日 web profile patch（`~/.dsh/profiles/web/cordis.patch.yml`）按 id 禁用 `llm-deepseek` 行 → 选择器不再混官方 DeepSeek 组；pi-ai 内置目录本就不注册路由。headless profile 未动。

**⚠️ 2026-08-25 用户拍板：DSH 不再维护直连 provider 清单**——settings.yaml 唯一 provider = `local-gateway`（http://127.0.0.1:3100/v1），agent-default-model 用户常切以盘上为准；备份 settings.yaml.bak-20260825。旧「7 provider/23 模型对齐」表作废（git/备份可查）。Cherry Studio 仍是用户侧模型启停的真源（新增厂商→读 sqlite user_provider/user_model→网关加自定义渠道）。

**🔑 网关鉴权后 DSH 必须带真 key（2026-08-25 起）**：:3100 已启用 API key 鉴权（api_state.json 的 api_key），settings.yaml 的 `Authorization: Bearer <真实网关密钥>` 不能再用占位值——**用户换 key 时 DSH 会全 401「莫名其妙用不了」**，把新值同步进 yaml 即恢复（热重载）。当前密钥以 api_state.json / 用户告知为准。

**zenmux 渠道（2026-08-25 接入，网关第 13 渠道）**：baseUrl https://zenmux.ai/api/v1（聚合器，全量 165 模型）；**必须走本机代理 http://127.0.0.1:7890 直连超时**（POST /api/channels 白名单已补 proxy 字段，直接改 channels.json 时也要记得带）；模型策展=用户 CS 启用的 4 个（deepseek-v4-flash-vision-exp-free / dots3-note-prev / ling-3.0-tiny / glm-4.7-flash-free），z-ai 免费模型上游常态 429 属上游拥挤。key 存 channels.json（源：CS sqlite api_keys，脚本读取不落日志）。

## 关键架构发现

**Cherry Studio 模型选择器**只读 `user_model` 表的 `is_enabled=1` 记录，不读 API 实时列表。CS 是用户侧模型清单真源（数据在 Data/cherrystudio.sqlite，非 config.json）。

## 7 Provider / 23 模型清单（2026-08-23 对齐后）

| Provider | 模型 |
|----------|------|
| **opencode-go** | `muse-spark-1.2-contributor`, `ox-alpha-free`（deepseek-v4-flash 已被用户在 CS 禁用并从 DSH 移除；网关 opencode 渠道保留 v4-flash/v4-pro 因直连可用） |
| **openrouter** | `cohere/north-mini-code:free`, `dots-studio/dots-3-note-preview:free`, `nvidia/nemotron-3.5-lightning:free`, `nvidia/nemotron-3-ultra-550b-a55b:free`(新), `openrouter/free`(新·自动路由), `stealth/ox-alpha`, `thinkingmachines/inkling-small:free`, `thinkingmachines/inkling:free`, `z-ai/glm-5.2:free` |
| **modelscope** | `ZhipuAI/GLM-5.2`, `deepseek-ai/DeepSeek-V4-Flash-0731`, `deepseek-ai/DeepSeek-V4-Pro-0813`, `moonshotai/Kimi-K3` |
| **sensetime (商汤)** | `deepseek-v4-flash`, `glm-5.2`, `sensenova-u1-fast` |
| **agnes** | `agnes-2.5-flash` |
| **zscc** | `claude-opus-4-8`, `claude-sonnet-5`, `gpt-5.6-sol`（kimi-k3-cc/deepseek-v4-flash-cc 已裁） |
| **xiaohongshu** | `dots3-note-prev` @ https://note3-prev-api.askdiandian.com/v1 |

## opencode-go 路由的坑

pi-ai 内置目录里没有 `muse-spark`/`ox-alpha-free`，且该 provider 目录混用多协议 → 必须显式写 `api: openai-completions` + `baseURL`，否则整段 llm-pi-ai 被拒收（选择器全空）。这两个免费模型上游不稳（地区封锁/间歇坏）；目录内模型直连正常。

## 网关 :3100 渠道现状（D:\项目\services\search_gateway\channels.py）

- **gemini 渠道已删**（2026-08-23 用户拍板）：Google 用自有 IP 情报判定代理出口为不支持地区，稳定 400 FAILED_PRECONDITION；公共 geo 库全说美国也没用，无法修复。
- **xiaohongshu 渠道已加**（agnes 之后、zscc 之前），key 从 ~/.dsh/.credentials.yaml 复制到 data/search_gateway/channels.json。
- **OpenRouter 多账号 key 池**：channels.json 新增 `key_pools.openrouter` 数组；`get_key()` 在「主key+池」间轮询；`chat_completion()` 遇 429 自动换下一把 key 重试一圈。4 账号分配（2026-08-24 齐）：**主号 fc5…982d 归 DSH+CS 专用**；网关=三号(…7003)升主 + 池[二号(…dbc5), 四号(…bc26)]，共 3 把轮换。
- **更早的网关旧主 key …6f28 已死**（401 User not found，账号被删），已移除。
- `z-ai/glm-5.2:free` 常态性上游 429（Z-AI 对免费层全局限流，与 key 无关）；`openrouter/free` 在网关侧不匹配 openrouter 渠道名（非 :free 后缀）会兜底到 zscc 应答，DSH 里则直连正常。

## DSH settings.yaml 对齐

`~/.dsh/settings.yaml` 的 local-gateway.models 现由网关编排自动同步（见顶段），手动改会被下次编排保存覆盖；要加非编排模型就建统一组。热重载生效（用户 UI 切默认模型会回写此文件，编辑前先读最新盘上状态）。

## DSH 插件副本陷阱（nitian-dsh-theme）

DSH web 端口 = **3080**（`http://127.0.0.1:3080`；nssm 服务 → node 子进程监听；8787 是 Codex 代理勿混）。DSH 服务跑 monorepo 源码（nssm: `node --import tsx/esm apps/cli/src/bin.ts web` @ `D:\DeepSeek\deepseek-harness`），但用户插件解析自**安装副本** `~/.dsh/profiles/web/node_modules/<pkg>`（真实拷贝非软链）：改源码 `~/.dsh/nitian-stage/` 无效，必须同步副本 + 重启 DeepSeekHarness 服务（bundle 内存缓存；浏览器还要带 cache-buster 强刷）。patch 层（cordis.patch.yml）改动则由 watchUserPatches 热应用、免重启。2026-08-25 修复过 lib/client.js 死代码 `if (i >= 15) { }`（subTier 内引用未定义 i → 整个客户端加载失败白屏）。

**挂载状态**：插件挂在 `cordis.patch.yml` 的 insert 块（id: nitian-dsh-theme-r2）。2026-08-29 曾因「疑似导致 composer 不渲染」剥离（无实证），2026-08-31 恢复挂载后 composer 正常、引擎 v2.3 全功能验证通过——再遇类似问题先实证排查勿盲摘。资产路由 200 但返回 index.html = SPA fallback 兜底，说明插件**没挂上**（/api/nitian/ping 是探针）。

**2026-08-31 v2.4 升级**：① 27 境全接分境界破境视频（BT_VID 映射表，四大关口 m/b/t/p 电影级，其余 bt_XX.mp4 5s 版，演出时长 minor 4300→5800ms）；② 修 eggtoast 彩蛋死代码（原代码查 .eggtoast 但 DOM 没这元素）；③ 心魔劫升级「心魔镜像」——enemies 目录为空，改用当前境界王林立绘 CSS 暗化（brightness .42 + 偏红 hue-rotate + mflick 闪烁）。

**2026-08-31 v2.5 资产缺口补齐**：① 印章 16~27 共 12 枚（Seedream 4.5，2048²；1024² 会 400 自动回退 2048²）；② 踏天桥 9 境立绘分化（era_19_qiao1~27_qiao9，Seedream 5.0，CH 映射新增 qiao1..qiao9）；③ 心魔敌人真立绘 4 张 `assets/enemies/fiend_{early,yuanying,kongjie,tatian}.png`（enemyOf 按纪元分档，镜像 fallback 保留；ALLOWED 新增 `/enemies/` 路由）。**坑**：collected 路由映射的是 `workers/collected`（不是 assets/collected），元婴背景 bg-01.jpg 一直存在未缺。生成脚本 `workers/gen_gap_assets.py` 可断点续跑。**2026-08-31 夜已重启+全链路验证通过**：enemies 路由 200、运行中 client.js 含 qiao1/enemyOf/fiend_。**坑 2（提权）**：UAC 提权重启会卡孤儿 consent.exe（父进程死、非提权杀不掉、还挡新提权）——先消掉卡住的 UAC 弹窗再触发；nssm 不在 PATH，重启必须用全路径 `C:\Users\郭永涛\.tools\nssm\nssm.exe`。**composer 修复（三个叠加 bug）**：① PAGE_CSS 里 `div[class*="_composerHero"]{display:none}` 误伤了空会话态的整个 composer 容器（新会话没输入框根因）→ 改为只藏内部 `>svg` 装饰；② 主题 shadow-DOM 的 `.empty` 王林立绘卡（z=2147400000）在 hero composer 出现时叠在输入框上 → empty-state 轮询加 hero-up+矩形相交检测，重叠即隐；③ opacity 带 CSS transition 时反复写入会卡死 CSSTransition（inline=0 但 computed=1）→ 轮询只在值变化时写 + 写前 `transition:none` + 隐藏时叠 `visibility:hidden`。教训：**对 `[class*="_xxx"]` 做全局隐藏前必须先实测该类挂在哪个容器上**（hero 类名同时是「装饰」和「整个输入框容器」的类名，只看名字猜会误伤）；**opacity 动画场景必须在值变化时才写，否则 CSSTransition 可能停在中间态**。

**2026-08-31 网关 SSE 帧修复**：DSH 发消息报 `Unexpected non-whitespace character after JSON at position 210 (line 2 column 1)`（PI_AI_ERROR）。根因：小红书/dots3 上游流式响应里部分事件只隔单 `\n`，pi-ai 按 `\n\n` 切分把两条 data: 行拼成一条消息 → JSON.parse 失败（210 = 第一条合法 JSON 的长度）。修在 `api_gateway.py` 的 `_SseReasoningStripper.feed()` —— 对每条完整 `data:` 行强制以 `\n\n` 收尾，事件重定界；网关原为手动孤儿进程（PID 50000，`python -u api_gateway.py`，工作目录即服务目录），计划任务 `SearchGateway` 已 Disabled，杀掉后重起；SSE 修复后实测 `fast` 34 事件全部双换行分隔、DSH 真实发消息成功无报错。教训：**JSON.parse 报 position=210 这类位置数字就是第一条合法 JSON 的长度 → 上游/网关把两条事件拼成一条了，查流分隔符**。详见 `D:\游戏\逆天主题\workers\汇报-资产缺口补齐.md` + [[error_lessons]]。

**YAML 缩进陷阱**：regex 替换 provider 块要用 `(\n\s*)` 捕获组引用前导空格，否则缩进翻倍。详见 [[error_lessons]]。

**2026-09-01 道藏设置面板错乱修复（v2.5.1）**：点「道藏」设置面板被压成 280px 窄条全竖排。根因是主题 PAGE_CSS 给 sidebarCol/detailsCol 的 `backdrop-filter:blur(18px)` **劫持了 fixed 后代的包含块**（设置面板 overlay position:fixed 不走 portal、直接挂在侧栏 footer 里，被锁进 280px 侧栏）。终稿：blur 移到 `::before(z:-1)` 伪元素（无后代不劫持），侧栏**只留 position:relative、不加任何 z-index/stacking context**——试错教训：isolation:isolate 会把面板封顶在侧栏原子组里被 centerCol 盖住，z-index:1 盖不过 composerSeat(z:7)/状态条(z:2)，**只有无 stacking context 才能让面板 z:1000 升出子树全局竞争（=DSH 原生行为）**。附带：模态开着时主题 HUD 自动隐（复用防卡死轮询写法）。验证：面板 800×727 居中、7 采样点全中面板内部、HUD 开隐关现、关闭后页面完好。教训：**fixed 弹层的祖先容器绝不能带 backdrop-filter/transform/isolate/任何 z-index，否则包含块劫持或层级封顶；毛玻璃要靠伪元素**。详见 `D:\游戏\逆天主题\workers\汇报-资产缺口补齐.md` + [[error_lessons]]。

## 同步脚本

`D:\项目\_tmp\cs_align_dsh.py`（CS→DSH 数据库方向）、`gw_add_or_pool.py`/`gw_check_all_or.py`（网关 key 校验与入池）、`gw_test_or.py`（网关轮换实测）。临时脚本统一放 `D:\项目\_tmp\`。
