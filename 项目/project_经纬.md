---
name: project-经纬
description: 经纬（Jingwei）＝DeepSeek Harness 的无限画布插件（@local/jingwei）。把一次真跑的 DAG 画在右栏，配左侧模型面板；执行器 v4 支持语义角色链（intake/produce/verify/merge/audit/output）。2026-10-20 状态 active：画布视觉语言升 v3.2（**纵向主轴 + DAG 拓扑分层**布局 + 三层节点结构 + 绿色唯一入口只给「执行完成」+ 反相签表达核查/交付结论 + 中央走线区绕行 + 预览安全加固），已按 GPT-6 Sol 第 3 轮裁决修正并实机验收通过；planner 断链真因已查明并换路由，重试链已加。真源 D:\Work\经纬\docs\00-项目总览.md。
metadata:
  node_type: memory
  type: 项目
  created: 2026-10-19
  modified: 2026-10-20
type: project
updated: 2026-10-20
---

# 经纬 · 无限画布插件

> **本条目只补记忆侧的状态与裁定，正文不复制**。项目真源：`D:\Work\经纬\docs\00-项目总览.md`。

## 一句话

DSH 右栏里是一张无限画布：一次真跑的 DAG 画成可拖、可平移、可缩放的节点图，按语义角色分列；左边挂着模型面板，显示有哪些模型、来自哪个渠道、还剩多少额度。

## 三条原则（仍然钉死）

1. **图是唯一视图真相**：数据真源是 `artifacts/<runId>/` 与会话日志，画布只读 manifest。
2. **单点调度**：真跑只有主 AI 能发起，插件不自己调模型。
3. **视图只读**：画布不直接改运行状态。

## 现状（2026-10-20 上午，接手基线）

- `project.yaml` → `status: active`；插件已装（profile `desktop`，symlink 到 `plugin/jingwei`）
- **执行器 v4**（`orchestrator-v4.js`）：`runTask / runPlan / runSubgraph / publishRun / archiveRun` 五链齐备；语义角色 `intake/produce/verify/merge/audit/output`；`toGraph()` 按角色分列（x = column×240）
- 跑通记录：runId `20261020-070900-f7b7`（5 节点语义链全 done）、`20261020-015649-e9b7`（四路分组 + 发布包）
- 文档 `docs/00~06` 已于 2026-10-20 全面追平 10-20 的真实代码（此前停在 10-19，落后一个昼夜）

## 形态裁定：v2 黑白 → v3 黑白为底 + 完成态绿（重要）

- **2026-10-19 深夜**郭老师否掉 v1 dashboard，定「纯黑白、任何色相即回退」（D-16~D-18）
- **2026-10-20**代码先越线（引入绿色、发光、模型面板常驻浮层），规范没升版 → 郭老师裁定**改规范承认实现**，不回头删代码
- **v3 视觉语言**（`docs/03` v3、`AGENTS.md` §三.1）：黑白为底 + **只允许完成态绿 `rgb(80,255,150)` 且只表达「已完成」**；done 态允许发光；模型面板是**唯一常驻浮层**；失败态仍不用红；圆角 ≤4px，唯一例外是模型面板圆形悬浮按钮
- 配套记录：决策 `docs/05` D-26（视觉升版）、D-27（先修 planner）

## 关键教训（2026-10-20 取证得出，容易再踩）

1. **planner 断链不是代码 bug**。`planner-last.json` 的 error 空输出，经会话日志取证（`scripts/jingwei_diag_planner.mjs` 解 `session.*.jsonl.zstd`）查明：10-20 **01:45~01:53 全机模型调用整层挂**（`502 所有渠道均不可用` / `CERTIFICATE_VERIFY_FAILED` / `TRANSPORT`）。planner 恰好挂在依赖外网聚合渠道的 `local-gateway`(:3100) 上，worker 走的 `buddy2api`(:8787) 没受影响。**已把 planner 主路由换成 `buddy2api/workbuddy/deepseek-v4.1-flash`（实测 2.2s 稳定出 JSON），`local-gateway/high` 降为兜底，并加重试链 + 诊断落盘。**
2. **「编排器不同角色走不同路由」时，先问这条路由依不依赖外网**。挂在会随外网波动整层挂的聚合网关上 = 一有波动就断链。
3. **守卫字段必须和它守护的对象同生共死**。`orchestrator-epoch.json` 的 runId 与 `graph.json` 不一致时，旧图的**每一次写入都被 `saveGraph` 静默丢弃**（评审、打回重跑全写不进去且不报错）——规划失败会污染 epoch，现已改为失败即回滚。**这是「闭环打回重跑从未跑通」的最可能根因。**
4. **Host 侧改动不随安装热更新**：`index.js` / `orchestrator-v4.js` 改动**必须重启 DSH**；`client.js` 也一样（bundle 缓存）。判断新版是否生效，看**进程启动时间 vs 源文件修改时间**，但「大概率」不算证据，仍以页面目视为准。

## 模型可用性是波动的（2026-10-20 实测）

10-19 探测里 `lobster/loomy/qoder/raccoon/traework` 整批 25s 超时，**10-20 同一批几乎全部可用**（0.7~6.3s）。所以模型面板必须显示**实时**状态，不能拿旧探测表当结论；速度/智力标签由 `scripts/probe_models.mjs` 随时刷新 `app/data/model-probe.json`。

面板的智力分真源：记忆库 `参考/reference_全维度AI模型智力评分与推荐调度总则.md` §二（LMSYS Elo / GPQA），**只搬真源数字、真源没有的不标**。

## 产品分工（2026-10-20 GPT-6 Sol 评审拍板，重要）

> **经纬的画布负责回答「AI 做到了哪一步」，成果页负责回答「这些东西现在能不能拿来用」。这两个问题必须分开。**

- 画布的绿**只代表「执行完成」**（`status === 'done'`），**不扩展成「质量合格」**；绿只能挂在**状态类**上，不能挂在**角色类**上（`verify`/`output` 之前把绿写死在角色样式里，导致非 done 也发绿）。
- 质量结论走**正交的 `review` 字段**（`pass`/`fail`/`unknown`，取核查产物首行）+ 运行级 `graph.delivery`（`ready`/`blocked`/`failed`）。
- **判断型节点（merge / audit / output）不因上游 failed 而被阻断**——它们的职责恰恰是看到 FAIL 给出返工结论；一起拦掉，整条链会在第一个 FAIL 处断掉。
- 端点感靠**形状**（intake 左白线 / output 右白线），不靠色相。
- **不做「自动弹出预览面板」**，改成 output 节点内一次性提示 + 预览面板顶部「在浏览器打开」按钮。理由：自动弹会打断正在看画布的人，而画布的全局视图正是它的价值。
- 成果页要**自包含单文件**：图片在**生成阶段**用 base64 内嵌（`plugin/jingwei/pack-html.js`），不能引用外部文件。
- 预览 iframe 的 sandbox 用 `allow-scripts` 而**不是空值**：空 sandbox 会把成果页里所有 JS 禁掉；不给 `allow-same-origin` 才既能用交互又读不到父页面。

## 里程碑：两次"第一次"（2026-10-20）

**① 「一句话 → 自动拆图」第一次真跑通**（10:30，runId `20261020-103036-f469`）。
planner 用 `buddy2api/workbuddy/deepseek-v4.1-flash`（`stopReason=completed`）把一句《观潮》学习资料需求拆成 8 节点语义链。
**根因（取证）**：之前不是代码坏，是 **01:45~01:53 全机模型调用整层挂**（`502 所有渠道均不可用` / `CERTIFICATE_VERIFY_FAILED` / `TRANSPORT`），
而 planner 恰好挂在依赖外网聚合渠道的 `local-gateway` 上。**planner 与 worker 都在那条线上，只换 planner 是不够的**——修完两个才真的通。

**② D4 完整语义链（12 节点）第一次全通**（12:08，runId `20261020-115406-e5bc`）：**12/12 done、零 failed**。
`intake → 4×produce → 4×verify → merge → audit → output`；`delivery` 正确汇总为 `blocked`（4 个 verify + audit 判 FAIL）；
**判断型节点（merge/audit/output）全部照常跑完，没被上游 FAIL 拦住**。

**成果页该由 AI 产，不该人工手写**（关键认知）：
D4 的 output 产物质量远超人工样板——一句话点明「不可交付」+ 三条具体原因 + 逐项状态表（路径/类型/尺寸/✅⚠️❌）+
连「薄雾 báo（应 bó）」「霎＝妾（应 妻）」这种错别字都抓到了，还要求三处同步改。
**人手工写的成果页样例被判定「不能用，质量差」，而 AI 产的那份是可用级** ⇒ 成果页的正确做法是**让 output 节点产出自包含 HTML**（内嵌 PNG），不是人去写。

**并行写状态会互相覆盖**（今天踩的第 N 个坑）：
并行节点各自 `读 graph.json → 改 → 写回`，后写的覆盖先写的 ⇒ **画布上节点显示 `idle`，而产物其实正在写**，看起来像"卡住了"。
DSH 侧 agent 独立复现了三次，GPT-6 评审也点了这条。**修法：模块级 `withGraphLock()` 把所有读-改-写排成串行。**
这类 bug 不报错不崩溃，只是**状态显示不可信**，比崩溃更难查。

**「重新组装子计划」时，语义字段必须一起带过去**（今天最后一个坑）：
`runSubgraph()` 从已有图拼 `planNodes` 时只抄了 id/title/kind/deps/prompt/artifact，**漏了 `role`** ⇒
`sanitizePlan()` 按结构把 verify 补成 produce ⇒ `runNode()` 里 `node.role === 'verify'` 不成立 ⇒
**核查结论永远不写回**（review 一直 pending）。**这类 bug 的共同特征：不崩溃，只是静默地把语义降级**（verify 变 produce）。

**闭环打回重跑的正确语义**（今天实测三轮才对）：
范围 = **目标节点 + 它的直接上游 produce + 全部下游**。
- 只含「自己+下游」⇒ 核查员读的还是旧产物，**打回等于白打**；
- 只往上追公共根（intake）⇒ 等于整轮重来、还会作废无关分支。
- 重跑子图的 `deps` **要保留原样**：未重跑的上游仍然提供产物，只是不再执行它们。

**planner 自由拆图实测（2026-10-20 13:10，入口落地后的第一轮）**：
自然语言任务「把四年级上册《观潮》做成一套家庭学习资料：辅导笔记 + 3:4 讲义图 + 课堂提问卡 + 字词表」
→ planner 一次拆出 **12 节点**：intake → 4×(produce→verify) → merge → audit → output，
标题分别是「生产：家长辅导笔记」「校验：辅导笔记」「汇总：四件套合稿与修订」「输出：自包含 HTML 成果页」。
**它自己定了目录约定**：`sources/`（口径与规格）`copy/`（文本产物）`images/`（图）—— 比写死的固定剧本更整齐。
**做图那路会做视觉自检迭代**（写 HTML → 跑出 PNG → `read_image` 读回看 → 改 → 再跑），单节点耗时可达 6~9 分钟，属正常而非卡死。

## 协作模式（2026-10-20 郭老师授权 · 重要）

> 原话：「你去跟 ChatGPT 镜像版 GPT-6 HIGH 合作，不用来问我了，我只要跟你说我喜不喜欢。」

**含义**：
- **技术决策不用问郭老师** —— 架构、拆解、实现顺序、改哪个文件、要不要重跑、怎么验证，我自己判断并推进
- **郭老师的角色是"审美与结果裁决"** —— 他说喜不喜欢、要不要这个方向
- **协作链路是「我 ↔ GPT-6 High」** —— 经纬的视觉与设计难题，优先走镜像站让 GPT-6 参与（它的审美/设计/思维更强），
  我负责拆需求、喂材料、验产物、落代码、维护契约
- **不需要他参与中间环节** —— 不用为了"要不要做"停下来等回复

**因此**：
- 能自主推进的活就别问，做完汇报（含"我做了什么判断、为什么"）
- 需要他做**物理动作**（开 DSH 会话、给 GitHub 凭证、目视验收）时才找他，且一次问清
- 涉及**方向性取舍**（如"加不加风格控制节点"）可以给建议并说明理由，但不要停下来等批准；先按最佳判断做，做完说明

## 需求做成 skill：分界线在哪（2026-10-20 下午，郭老师提的）

> 郭老师的原话：「其实不用给 planner 写太多的提示词，可以把一些需求做成 skill，让它自己去调用 skill。」

**这条直觉是对的，已落地。** 但必须分清两类，否则会出错：

| 内容 | 放哪 | 为什么 |
|---|---|---|
| 可复用流程与规范（怎么跑经纬、成果页怎么写、风格预设） | **skill** | 主 agent 会自动发现并加载；独立迭代、随仓走 |
| 产品不变量（六种角色结构、必须逐路核查、output 必须 HTML、verify 首行 PASS/FAIL） | **planner 提示词** | **经纬的子 agent 读不到 skill** —— 它们的 prompt 由编排器生成，不带 skill 上下文 |

**已建的两个项目级 skill**（DSH 发现优先级 100：`<projectRoot>/.dsh/skills`）：
- `jingwei-runner` —— 怎么跑经纬（探端口、拿带 `session-` 前缀的 sessionId、两个动作、
  四个字段语义、打回范围＝依赖图决定、7 个坑）
- `jingwei-output-style` —— 成果页规范（五块结构、HTML 骨架、颜色语义、诚实标注、读者适配、5 种风格预设）

**关键闭环**：编排器**读同一个 skill 文件并注入 output 节点的 prompt** ⇒
主 agent 与 output 子 agent 遵守同一份真源，两边永远一致。

**「风格控制」的正确落点（不是新节点）**：
- `dispatch` / `run-plan` 新增可选 `style` 参数 → 存进 `graph.style` → 注入 output 节点
- 预设：家长向 / 学生向 / 专业向 / 极简 / 可打印，可组合
- 迭代：**打回 intake 节点 = 全链按新风格重做**（`rerunScope` 天然支持）
- 实测（4 节点快计划，style=「家长向 + 可打印」）：4/4 done、零 failed，成果页 12,418 B、
  外链 0、五块结构齐全、含诚实标注，**且配色真的按 style 走**（`--bg:#fff` 白底黑字）。

**为什么不做「风格控制节点」**：它自己也是 planner 拆的 ⇒ 风格还是 AI 定的，
**你要的"控制"没兑现**，却多了一跳、多一个要打回的对象、图上多一个节点。
风格是**需求**（人给），不是**结构**（AI 拆）。

## 入口：经纬怎么被"一句话"触发（2026-10-20 13:10 落地并实测）

**此前只有"我会跑经纬"**（我走 HTTP 直接调），郭老师自己不会触发 —— 这是产品真正的缺口。
**解法：写一份给 DSH agent 看的操作手册**（`D:\Work\经纬\docs\08-操作手册.md`），并在经纬 `AGENTS.md` 加「〇」节指向它。
**实测通过（2026-10-20 13:10）**：DSH agent 自主完成「读手册 → 探端口(55483) → 确认 sessionId 形态 → POST dispatch → HTTP 202」，全程无人工介入。

手册里沉淀的关键事实（**别再踩**）：
- **sessionId 必须带 `session-` 前缀**（`session-<uuid>`），只用裸 uuid 会 409 `session is not live`；
  磁盘目录名是裸 uuid、但 `agents.get()` 认的是带前缀的 —— **两个形态不一样，别混**。
- **DSH web 端口每次重启都变**，别写死，要从 `--expose-internals` 的 host 进程反查。
- **节点路由固定用 `buddy2api/workbuddy/deepseek-v4.1-flash`**（本地凭据网关、零倍率、1.3s）；
  **`local-gateway/high` 依赖外网聚合渠道，今天整层挂过两次**（01:45、10:31），会把整链一次拖死。
- `status`（执行）/ `review`（核查）/ `humanReview`（人工）/ `graph.delivery`（能否交付）**四个字段语义别读错**：
  **done 只代表执行完成，不代表质量合格。**

## 能力突破：planner 首次成功 + 自动化通道（2026-10-20 上午）

**① 「一句话 → 自动拆图」第一次真跑通**（runId `20261020-103736-ae6b`）。
planner 用 `buddy2api/workbuddy/deepseek-v4.1-flash`（`stopReason=completed`）把一句《观潮》学习资料需求拆成 8 节点语义链：
`intake → 2×produce → 2×verify → merge → audit → output`。产物实测：讲义图 PNG **1200×1600（精确 3:4）**、
辅导笔记是带结构梳理表和「静—动—静」教学抓手的真教研内容（还诚实标注了「段落边界以孩子课本为准」防编造）。
**这条链是这个项目存在的理由，现在它有实证了。**

**② 修掉了「只修一半的故障域」**（2026-10-20 10:31 整链 502 暴露）：
planner 换到 `buddy2api` 后成功，worker 却**仍在 `local-gateway/high`** 上 → 9 个节点全 502。
**教训：修路由稳定性要把链上所有角色一起看；改完要看图里每个节点实际的 `provider/model`，别只看代码默认值。**

**③ 三处静默结构 bug**（一次 planner 复现全炸出，图看着完全正常）：
判据只认 `kind==='merge'` 而 planner 只给 `role` → 多补一个「汇总」；output 节点被标成 merge（提示词 role 枚举里没有 output）；
`MAX_NODES` 检查排在补节点之前 → 补出来的节点绕过上限（且 `MAX_NODES=8` 装不下 D4 的 12 节点）。
**已加回归测试 `scripts/test_sanitize_plan.mjs`，拿 planner 真实输出当断言（9/9）。**

**④ 新的自动化通道：CDP 直连 DSH**（`scripts/dsh_cdp.mjs` + `dsh_restart_with_cdp.ps1`）。
DSH 是 Electron，加 `--remote-debugging-port` 后可用 CDP 直连 renderer，于是
`send`（自己发消息）/ `read`（读回复）/ `eval`（读画布 DOM）/ `screenshot`（自己截图验收画布）都变成脚本命令。
**意义：经纬的 dispatch 需要「活着的 DSH 会话」，以前每跑一次都要人手动开会话发一句；现在不必了。**
同款打法在 opencli 里对 Codex/Antigravity 已成熟（`opencli list` 可见那批 CDP 适配器）。

## 边界（不做）

不做通用 DAG 编辑器（节点创建/连线编辑/属性面板）／不做实验报告界面／不做多模型调度后端／不做公网服务。

## 下一步（2026-10-20 排定）

1. **复现 planner**：DSH 里开一个活会话 → `scripts/jingwei_repro_planner.ps1 -SessionId <id>`（`dispatch` 必须是活会话，DSH 重启后停在首页会 409）
2. 目视验收画布 v3（分列布局 / 完成态绿与发光 / verify 状态条 / output 节点 / 合并双阶段动画）
3. 跑 D4 完整语义计划（4 路并行）
4. 闭环实测（打回某一路 → 只重跑该路 + 下游 → 重新合并 → 发布 → 归档）

## 关联

- 宿主：DeepSeek Harness（profile `desktop`）
- 插件：`@local/jingwei`（Host 路由 `/jingwei/**` + Client 右栏 tab）
- 模型来路：客户端凭据网关（`:8787`，buddy2api 零倍率，主力）、API转发网关（`:3100`，外网聚合，**易整层挂，只作兜底**）
- 项目登记：`D:\记忆\项目清单\projects.yaml` → `local_only` 段「经纬（Jingwei）」
- vault 登记：`D:\Work\元智能\machine\vault_registry.yaml` → 经纬

## 2026-10-20 状态更新 · 画布 v3.2 第 1~2 段（+ GPT 第 3 轮复核）

- **版式**：节点＝角色标签 / 标题 / 状态行 / 分隔线 / 结论签 / 来源行；绿色只出现在「12×2px 短线 + 执行完成文字」，
  核查未过 / 人工退回 / 交付受阻用白底黑字反相签；intake＝委托卡，output＝作品封签。
- **布局（关键变更）**：从「按语义角色分列、x = column × 240」改为 **纵向主轴 + DAG 拓扑分层**
  （主轴 x=240；双列中心距 252、净间距 36；上下净间距 72；尺寸取 DOM 实测）。
  ⚠️ 前者是**旧代码的实现**，不是 GPT-6 Sol 的原意 —— 抄规范时抄错了，已纠偏。
- **坐标唯一真源**：`client.js` 的 `layoutMissing()`；编排器 `toGraph()` 不再输出 x/y。
- **两条 GPT 点名的硬约束**：`dagRank`（逻辑层级）≠ `visualRow`（视觉行）；
  **单元是布局策略不是 DAG 数据结构** —— 共享核查 / 多父核查不得硬挂到某个生产者上。
- **旧坐标迁移**：`view.json` 记 `layoutVersion`；加载后检测节点真实矩形重叠；
  冲突时给不阻断提示条 `[保留当前布局] [按新版式重排]`（可撤销），不擅自平移缩放旧坐标。
- **回归**：`node scripts/test_all.mjs` → 65 断言全绿（新增 布局 15 + 渲染语义 23）。
- **留档**：`D:\Work\经纬\docs\09-gpt6-第3轮裁决.md`（提问 + 裁决原文）。
- **待办**：v3.2 第 3 段（连线：跨波次长边绕行、单一坐标系、边状态判据）、第 4 段（预览页适配）；
  郭老师目视验收；`jingwei-public` 推送仍缺 GitHub 凭证。

## 交接档指针（换会话接手先看）

- **交接单**：D:\Work\经纬\docs\11-交接单-2026-10-20.md
  （我的角色与授权边界 / 开局三读 / 关键路径地图 / 当前状态 / 命令速查 / 铁律 / 未决事项）
- **事故记录**：D:\Work\经纬\docs\10-事故记录-2026-10-20.md（两次 DSH 崩溃取证）
- **GPT 第 3 轮裁决**：D:\Work\经纬\docs\09-gpt6-第3轮裁决.md（提问与裁决原文）

## 2026-10-20 晚间更新 · v3.2 第 3~4 段 + 两次 DSH 崩溃根治

- **第 3 段 连线**：跨波次长边走**中央走线区**（`x = AXIS ± 18`），车道错位不汇合；
  边状态判据改为「上游完成 **且** 下游已开始或结束」；连线**不再传绿**。
- **第 4 段 预览**：`.md` 走 markdown 渲染（以前落 text 分支）；未知类型安全回退；
  **链接协议白名单**（`javascript:`/`data:` 不再能进 href —— 预览页与插件同源）。
- **⚠️ 改插件源码必须原子写入**：DSH 带 HMR，磁盘一改就自动重新导入 ⇒
  「分多次编辑」的中间态会被抢先加载。已两次因此出事（19:00 黑屏、19:09 DSH 崩在启动画面）。
  ⇒ 一律走 `scripts/atomic_patch.py`；回归里有 `test_client_lint.mjs` 静态守卫兜底
  （TDZ + 重复声明，用 git 里的真事故版本反向验证过）。
  ⇒ **DSH 崩了先读** `%APPDATA%\@deepseek-ai\dsh-desktop\logs\crash-*.log`（带渲染进程 console 原文）。
- **实机验收通过**：右栏经纬 tab 正常渲染；「重排版面」后纵向主轴生效（节点中心 x 全 240）。
- 回归 **103 断言全绿**；留档 `docs/09-gpt6-第3轮裁决.md`、`docs/10-事故记录-2026-10-20.md`。

## 2026-10-20 19:25 交接单复核（三处修正）

- **交接单** `D:\Work\经纬\docs\11-交接单-2026-10-20.md` 八节结构复核完毕，路径逐条 `Test-Path` 通过。
- **修正 1**：`client.js` 实为 **2930 行**（原写 2898），`orchestrator-v4.js` 869 行。
- **修正 2**：提交轨迹补最新一笔 `c241988`（加交接单）；并注明 **`D:\Work` 是多项目共仓**，
  别的项目（AI精听训练器 / English-Content-Factory）有未提交改动 ⇒ **禁止 `git add -A`，只 add `经纬/`**。
- **修正 3（重要，新发现）**：`D:\小浣熊\jingwei-public` 的本地副本是 **v3.0 旧版**
  （`client.js` 2151 行，无 `dagRank`/`visualRow`/`LAYOUT_VERSION`/「重排版面」；源是 2930 行），
  且 7 个文件有未提交改动。**直接 push 会把 v3.0 发出去**——
  正确顺序：先从 `D:\Work\经纬` 同步 v3.2 → 再提交 → 最后推。
  另：GitHub SSH 认证实测 `Permission denied (publickey)`，本机 `~/.ssh/id_ed25519` 在但 GitHub 侧没认这把钥匙。
- **收尾状态**：DSH 崩溃日志最新仍停在 19:09:14（此后 16 分钟零崩溃），8 个 `DeepSeek Harness` 进程正常，
  `:3100` / `:8787` 均 LISTEN，经纬工作区干净，103 断言全绿。
