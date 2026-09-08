---
name: project-ai-gateway
description: 统一 AI 网关（D:\项目\ai-hub\search_gateway；:3000 搜索聚合 + :3100 API 转发，原 D:\游戏\ds_v4_cli 已迁移）——opencli 4 引擎 + LLM 渠道路由 + 统一模型组/光线拖拽编排/总开关/用量记账/派发中心二级页（GATEWAY_ID 陷阱）
metadata:
  node_type: memory
  type: project
  originSessionId: cc570cb5-bfc6-41c1-a63b-84533fa58583
  modified: 2026-09-08T00:00:00.000Z
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
- **重启免 UAC**：网关必须普通权限运行。禁止 `Start-Process -Verb RunAs` 启动 python（会变提权进程 → 下次杀它 Access denied → 恶性循环）。重启 = 普通进程 Stop + 普通进程 Start。
- **重启要杀全部同脚本进程**：`api_gateway.py` 若旧进程没死干净，新端点会 404 且旧端点照常，易误判「新代码没生效」。判断一律以 `netstat -ano | findstr :<端口>` LISTENING 为准。
- **四种状态勿混淆**：成员冷却（`_model_cooldown` 30s）≠ 渠道限流（`rate_limit.py` open/throttled/blocked，15/30/60/120/300s 退避）≠ 共享代理故障域熔断（`fault_domains.is_tripped`，DIRECT 不入域）。
- **主题落地方式**：一律走 `api_page.html` 的 `data-style` 新增风格（不另起主题系统）；不伪造、不假装「额度+延迟动态加权」。

## 时间线（近→远）

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