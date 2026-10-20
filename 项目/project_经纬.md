---
name: project-经纬
description: 经纬（Jingwei）＝DeepSeek Harness 的无限画布插件（@local/jingwei）。把一次真跑的 DAG 画在右栏，配左侧模型面板；执行器 v4 支持语义角色链（intake/produce/verify/merge/audit/output）。2026-10-20 状态 active：视觉语言升 v3（黑白为底 + 完成态绿单色相 + 模型面板入规），planner 断链真因已查明并换路由，重试链已加。真源 D:\Work\经纬\docs\00-项目总览.md。
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
