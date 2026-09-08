---
name: cherry-dsh-sync
description: Cherry Studio ↔ DSH ↔ API 网关 模型同步 — 2026-08-25 起 DSH 只连本地网关 :3100（不再直连 7 provider）；统一编排组自动同步 DSH 选择器；网关鉴权后必须带真 key；zenmux 渠道；web_search 走 :3000 聚合
metadata: 
  node_type: memory
  type: project
  originSessionId: f278da07-fa93-4c68-a18a-ce5d52941e3a
  modified: 2026-09-08T00:00:00.000Z
---

# Cherry Studio ↔ DSH ↔ API 网关 模型同步

> 本页为**概述 + 关键不变量 + 时间线索引**。操作级/排障级详情已归档至
> 👉 `项目/归档/project_cherry_dsh_sync_完整详细记录.md`（2026-09-08 起，本页只留结论，避免臃肿）。

## 这是什么

DSH(Cherry) 模型来源由「直连 7 provider」改为「统一走后端网关 :3100 + :3000」，实现单点编排、模型选择器与 DSH 端自动同步。Cherry Studio(CS) 是用户侧模型清单的真源。

## 关键不变量 / 易错点（必读）

- **DSH 唯一 provider = `local-gateway`（http://127.0.0.1:3100/v1）**；不再维护直连 provider 清单（2026-08-25 用户拍板）。
- **网关鉴权后 DSH 必须带真 key**：settings.yaml 的 `Authorization: Bearer <真实网关密钥>` 不能是占位值；**用户换网关 key 时 DSH 会全 401「莫名其妙用不了」**，同步新值进 yaml 即恢复（热重载）。
- **web_search 走 :3000 聚合**（2026-08-26）：三件套 = `/api/search_json` 端点 + `~/.dsh/search-stage/` 插件源码（改后必须 cp 到安装副本 `~/.dsh/profiles/web/node_modules/hub-web-search/index.js`）+ profile patch；超时预算三层都要 ≥180s（base bundle、三个 agent 预设、profile）。
- **DSH 插件副本陷阱**：DSH web 端口 **3080**（nssm 服务 → node 子进程；8787 是 Codex 代理勿混）。用户插件解析自**安装副本**（真实拷贝非软链），改源码 `~/.dsh/nitian-stage/` 无效，必须同步副本 + 重启 DeepSeekHarness 服务（bundle 内存缓存 + 浏览器 cache-buster）。patch 层(cordis.patch.yml)改动热应用免重启。
- **统一编排组同步 DSH**：`channels.py` 的 `set/delete_unified_model` 挂钩 `sync_dsh_models()`，保存组就把 `unified_models.json` 组名写进 `~/.dsh/settings.yaml`，热重载免重启。**依赖网关解释器装 PyYAML**（换解释器/升级后要重装，否则静默不同步）。
- **opencode-go 路由坑**：`muse-spark`/`ox-alpha-free` 必须显式写 `api: openai-completions` + `baseURL`，否则整段 llm-pi-ai 被拒收（选择器全空）。
- **zenmux 渠道(第13渠道)**：必须走本机代理 `http://127.0.0.1:7890`，直连超时；z-ai 免费模型上游常态 429 属上游拥挤。
- **通用教训（详见归档 error_lessons）**：SSE `JSON.parse position=210` → 两条事件被拼成一条，查流分隔符 / 对 data: 行强制 `\n\n` 收尾；`[class*="_xxx"]` 全局隐藏前先实测挂哪个容器；fixed 弹层祖先容器不能带 backdrop-filter/transform/isolate/任何 z-index（毛玻璃靠 `::before(z:-1)` 伪元素）；YAML 块级替换用 `(\n\s*)` 捕获组引前导空格防缩进翻倍。
- **UAC 提权陷阱**：DSH/nssm 相关重启用全路径 `C:\Users\郭永涛\.tools\nssm\nssm.exe`（nssm 不在 PATH）；提权重启会卡孤儿 consent.exe。

## 时间线（近→远）

- **2026-09-01 · 道藏设置面板错乱修复 v2.5.1**：PAGE_CSS `backdrop-filter:blur(18px)` 劫持 fixed 后代包含块 → 面板 280px 窄条。终稿 blur 移 `::before(z:-1)` 伪元素、侧栏只留 position:relative、无 stacking context（否则被 composerSeat z:7 盖住）。
- **2026-08-31 · 逆天主题 v2.4/v2.5 + 资产缺口补齐**：27 境分境界破境视频（BT_VID 映射）、心魔镜像暗化、印章 12 枚/踏天桥 9 境立绘/心魔真立绘（Seedream 4.5/5.0）；composer 修复三叠加 bug（`_composerHero` 全局隐藏误伤、王林立绘 z-index、opacity transition 卡 CSSTransition）。
- **2026-08-31 · 网关 SSE 帧修复**：小红书/dots3 上游部分事件只隔单 `\n`，pi-ai 按 `\n\n` 切分把两条 data 拼一条 → JSON.parse 失败。修在 `api_gateway.py` 的 `_SseReasoningStripper.feed()`，对每条 data: 强制 `\n\n` 收尾。
- **2026-08-26 · web_search 接 :3000 聚合**（见上）。
- **2026-08-25 · 网关鉴权 + zenmux 接入 + DSH 二次演进**：DSH 选择器=网关统一编排组自动同步；网关启用 API key 鉴权（api_state.json 的 api_key）;zenmux 渠道接入（第 13 渠道）。
- **2026-08-23 · 渠道现状**：gemini 渠道已删（代理出口区域被 Google 判定不支持，无法修复）；xiaohongshu 渠道已加；OpenRouter 主 key + key_pools 轮询（4 账号），遇 429 自动换 key。
- **2026-08-25 前 · 旧架构**：7 provider/23 模型直连（已作废，git/备份可查）。

## 同步脚本

`D:\项目\_tmp\cs_align_dsh.py`（CS→DSH）、`gw_add_or_pool.py`/`gw_check_all_or.py`（网关 key 校验与入池）、`gw_test_or.py`（轮换实测）。临时脚本统一放 `D:\项目\_tmp\`。

## 源文件

- 完整操作级/排障级详情、7 Provider/23 模型清单、SSE 修复过程 → `项目/归档/project_cherry_dsh_sync_完整详细记录.md`
- 报告：`D:\游戏\逆天主题\workers\汇报-资产缺口补齐.md`
- 教训汇总：`[[error_lessons]]`