---
name: deepseek-harness-basics
description: DeepSeek Harness（DSH）基本情况全景——模块构成/设计理念/操作逻辑/自定义切入点，2026-09-04 源码盘点产物
metadata:
  node_type: memory
  type: project
  modified: 2026-09-04T10:00:00.000Z
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
---

# DeepSeek Harness（DSH）基本情况

> 开源的 AI Agent 宿主/运行时。定制项目 `D:\Work\dsh-personal-host`（源码盘点在 `00-inventory/`，本篇是给人读的精简认知版）。

## 一、它有什么（模块构成）

**两个入口**：`apps/cli`（终端）、`apps/web`（浏览器，:3080，vite）。

**packages 按职责分层**（`packages/<域>/<包>`）：

| 层 | 关键包 | 干什么 |
|---|---|---|
| 前端 UI | `client/ui-*`（theme/model-selection/settings-models/slots） | Web 组件与扩展点 |
| Host 服务 | `host/webserver`、`frontend-static`、`plugin-inventory` | 后端路由/静态/插件发现 |
| 核心 | `core/agent-loop`、`core/tools`、`core/agent-default-model` | Agent 主循环、工具注册、默认模型 |
| 模型 | `llm/llm`（类型基座）、`llm-pi-ai`、`llm-deepseek` | provider / adapter / 消息类型 |
| 子 Agent | `subagent/subagent` + spawn/fork/acp/codex 多实现 | 派发 child agent |
| 启动插件 | `boot/app-boot`、`bundle/base`、`bundle/web-app` | profile 发现 / patch 组合 |
| 上下文 | `context/*`、`attachment/*`、`compaction/*` | 文件/图片/会话上下文 |
| 执行 | `code-runtime/*`、`subprocess/*`、`sandbox/*` | 代码执行/子进程 |

**对定制最重要的两个包**：
- `llm-pi-ai` —— 本地网关 provider 的宿主（settings 里的 `local-gateway` 就是它注册的）。
- `core/agent-loop` —— `AgentLoop`（inject: agents/sessions/llm/tools/systemPrompt），主循环本体。

## 二、有什么设计

**1. cordis 插件体系**：**Service + 依赖注入（inject）+ patch layer 组合**，但准确表述是 **declarative dependency + scoped effects + reversible activation**（不只是 DI）。插件 `apply(ctx)` 靠 `ctx.<service>` 取依赖；**生命周期由 Fiber/effect 托管**（不是"无生命周期"）——`ctx` 注册的事件/工具会随插件卸载自动撤销，外部资源须放进 `ctx.effect(() => disposer)` 清理。插件三种形态（函数 / 对象 / `Service` 子类）都是正式契约。（GPT 校准：我原写"非 init/dispose"低估了生命周期。）

**2. 分层扩展原则（红线）**：官方 6 级定制层，越靠后越失控：
```
settings（属于某能力自己的用户配置）
→ 第三方 bundle / plugin
→ profile cordis.patch.yml
→ $DSH_HOME/cordis.patch.yml   ← 全局补丁层（此前漏）
→ 临时 --patch                 ← 启动参数临时补丁（此前漏）
→ fork upstream                ← 最后手段，等同改源码
```
我原简化的"设置 > 插件 > patch > 改源码"不错但漏了 `$DSH_HOME` 全局级和 `--patch` 临时级。**DSH 仍是 Developer Preview，API 会破坏性变化**。

**3. profile 机制**：`~/.dsh/profiles/web/` 是用户态，靠 `package.json` 的 `dsh.profile.bundles`（有序 bundle 列表）+ 自己的 `cordis.patch.yml`（用户 patch 层，热重载）组合起来。

**4. 单一 provider + 编排组**：模型不直连上游，统一走 `local-gateway`（:3100）→ 8 个「编排组」（fast / deepseek-free / glm-5.3-flash / deepseek-opencode 等）→ 网关层渠道链 fallback。

**5. 子 Agent 已内置**：`SubagentRuntime` + 多 provider（spawn/fork/acp/codex）+ `tool-subagent`（把「派子 agent」本身做成一个 tool 暴露给模型）。**不是从零造，是在它之上做编排。**

**6. 多模态消息**：图片在会话里是 `ImageBlock`（只存 attachment 引用），adapter 转 base64 发上游；能力门在 `llm-pi-ai/adapter.ts`：模型 `input` 不含 `image` 就拒。

## 三、操作逻辑

**启动链**：profile 发现 → bundles patch 依序 apply → 用户 patch → cordis loader 生成 entry list → Service 注入 → 插件 apply。

**改东西三档生效**（GPT 校准后，我原版把"热重载"写太绝对）：
- 改 `cordis.patch.yml`（profile patch）→ **仅当 profile 开启了 live reload 才热重载**，非无条件。
- 改 `settings.yaml`（模型编排/默认模型）→ **取决于具体插件是否监听**，不是所有 settings 都热生效。
- 改「安装副本 node_modules 里的 Host 插件本体」→ **要 restart**；但**「必清 bundle cache」不对**——Client 端看构建/HMR，不是一律清缓存。

**模型解析链路**：`agent-default-model`（settings：provider+model）→ `llm` Service → provider 路由（`llm-pi-ai` 的 local-gateway）→ :3100 网关 → 渠道链。

**一句话区分**：patch 只作用于「插件模块层」，不作用「settings 层」——adapter 运行时读 settings，patch 改不动它。

## 四、自定义从哪切入（4 个正道 + 1 个禁区）

| 切入面 | 落点 | 改源码? |
|---|---|---|
| **模型编排**（GLM 5.3 flash 成默认、图片通） | 全局 provider/model 放 `settings.yaml`；**单次 Agent/子 Agent 选模走 Agent options**（别把"每次换模"塞进全局 settings） | 否 |
| **工具链**（加自己的 tool） | 插件 `inject:['tools']` → `ctx.tools.register(definition)`（基本对） | 否，纯插件 |
| **UI 主题/资产**（专属界面） | **优先 client plugin + slots**（`dsh.client` + `exports["./client"]` + client `apply(ctx)` + slots）；大改布局用 UI plugin/slot，纯 CSS 只够调主题 | 否，client plugin |
| **子 Agent 编排**（派活给多模态子 agent） | **依赖 `subagents` 服务**（`subagents.start("spawn", …)`），不直接贴 `SubagentRuntime` | 否，编排层 |

**第3个关键遗漏 = Web Client 正式扩展面**：`dsh.client` + `exports["./client"]` + client `apply(ctx)` + `slots`——这是官方 client 插件正式契约（先前只当我们「前端注入 client.js」一笔带过，实为官方一等扩展点）。

**禁区**：直接改官方源码（`D:\DeepSeek\deepseek-harness`）。**现状已违规**：28 处未提交改动（模型置顶/隐藏 ~700 行、pi-ai 暂停、盘符选择器、超时 180s 等）正支撑运行中的服务，已定 `00-inventory/customization-migration.md` 迁出清单，逐步搬回正道。

## 关联

- 定制项目唯一事实源：`D:\Work\dsh-personal-host`（README/盘点文档）。
- 网关侧模型组真源：[[project_cherry_dsh_sync]]。
- 后备执行通道：[[project_deepseek_harness_opencli]]。
- 需求定位：接管 Claude 短板（界面/交互/视觉），第一步验收=能派多模态子 agent。