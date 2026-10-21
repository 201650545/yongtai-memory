---
name: project_buddy2api_switcher_sync
description: Buddy2API 网关(:8787) 与 WorkBuddy 账号切换器 的三重隐式耦合与契约自检机制——网关改数据层后切换器必须同步，否则数据静默没打通
type: project
updated: 2026-10-21
kind: fact
status: active
scope: buddy2api_switcher_sync
---

# Buddy2API ↔ WorkBuddy 账号切换器：契约与自检

## 一、问题是什么（2026-10-21 郭老师定）

原话：「这个网关我切换数据更新之后，不是还有一个 Workbuddy 账号切换器吗？
Workbuddy 账号切换器又没有同步更新，导致数据没有打通。」
另原话：「Buddy 还要再跟 AI 说一遍更新切换器，太麻烦了」

⇒ 要的不是「这次帮我改一下」，而是**以后不用再跟 AI 说一遍**。

## 二、根因：三重隐式耦合 + 静默吞异常

切换器 `D:\Tools\WorkBuddy-Account-Switcher`（pywebview + 单文件 `ui/index.html`）
与网关 `:8787`（`D:\项目\ai-hub\buddy2api`）之间靠三条**没写下来**的通道连着：
| # | 通道 | 具体依赖 |
| :-- | :-- | :-- |
| 1 | 直读网关 SQLite | `logs`（account_id / model / created_at / error_msg / status_code / total_tokens / credit / provider / duration_ms / prompt_tokens / completion_tokens）、`accounts`（id/name/uid/provider/domain/status/total_tokens/total_requests）、`account_resource_cache`（account_id/payload）、`account_checkin_cache`（account_id/checkin_date/payload）、`settings`（key/value，`key='selected_models'`） |
| 2 | 调网关 HTTP 端点 | `/admin/credit-summary`（channels/accounts/total_balance/updated_at）、`/admin/stats`、`/admin/accounts`、`/admin/models` |
| 3 | 读 DSH profile | `C:\Users\郭永涛\.dsh\profiles\desktop\cordis.patch.yml` 里 `providers.models` 的结构 |

**致命点**：切换器里这些读取**大量用 `except Exception: pass` 兜底**
（例：`switcher.py:582` 读 credit-summary 失败就静默跳过）。
⇒ 网关一改字段，切换器**不报错、不弹窗**，只是**静默显示 0 / 空列表** ⇒ 「数据没打通」，而人看不出来。

**另有一个隐性风险**：切换器**不在任何 git 仓库里** ⇒ 改了它没有历史、没法回滚、也没法让下一个 AI 知道改过什么。
（**已于 2026-10-21 00:32 解决**，见 §七）

## 三、落地的解法

### 3.1 契约自检脚本（真源在网关仓）

`D:\项目\ai-hub\buddy2api\scripts\check_switcher_sync.py`

- **从 `switcher.py` 原样抽取它实际执行的 19 条 SQL**，逐条打到活的网关上跑
  ⇒ 网关改了列名，这里直接 `OperationalError`，**不用维护第二份字段清单**（字段清单必腐烂）
- 校验 4 个 HTTP 端点的必备字段、5 张表的必备列、DSH profile 的 8787 provider 结构
- 对比网关渠道集合 vs 切换器的 `CHANNEL_TAG` / `CHANNEL_NAME` / `_QUOTA_CHANNELS` / `_SUBSCRIPTION_CHANNELS`
- 实跑切换器 5 个采集函数（`get_model_quota` / `get_model_params` / `get_channel_summary` /
  `get_model_capacity` / `get_today_quota`），抓「success=True 但列表为空」的静默失败
- **判据三档**（宁可误报也不漏报）：
  - **FAIL** 真断链（结构变了 / 数据漏算）——必须修
  - **WARN** 网关有但当前口径不显示（如 `CHANNEL_TAG` 少一个渠道 ⇒ 界面退化成前 3 字母，不崩）
  - **INFO** 设计过滤（如 `qoder` 没在 DSH 选模型 ⇒ 按设计不进渠道汇总）
- 退出码 0/1；`--log <path>` 追加落盘；`--notify` 时 FAIL 才**飞书私聊播报**（复用 `notify_capability.py`，不重造通道）

### 3.2 每日自动跑

- 计划任务 **`Buddy2API_SwitcherSyncCheck`**（每天 **03:07**，`pythonw.exe`，无窗口）
- 日志：`D:\项目\ai-hub\buddy2api\logs\switcher_sync_check.log`
- 注册在 `D:\Work\元智能\40_定时任务\registry.yaml`（owner: buddy2api）
- 登记进 `能力总账.md` §四 + `能力总账.json`

### 3.3 机制登记（让 AI 不用人交代）

- `C:\Users\郭永涛\AGENTS.md` **第 16 条**（指针行，正文在总账）
- `D:\Work\元智能\10_AI自成长引擎\技能库\能力总账.md` §四「网关 ↔ WorkBuddy 账号切换器 契约」

## 四、当前体检结论（2026-10-21 00:25）

**PASS 全通**——底层契约目前是通的：

- 4 个端点字段齐全 ｜ 5 张表列齐全 ｜ 切换器 19 条 SQL 全部在活库跑通
- 8 个网关渠道全部被 `CHANNEL_TAG`/`CHANNEL_NAME` 覆盖
- 采集函数：quota 17 条 / by_channel 24 条 / channel_summary 9 条 / params 24 条 / capacity 25 条
- INFO：`qoder` 未在 DSH 选模型 ⇒ 切换器按设计不列（不是断链）
- `workbuddy-intl`：网关侧 `unsupported=True`（无额度概念）⇒ 切换器不归类是**一致**，不是漏算

## 五、踩过的坑（改这个脚本时别再踩）

1. **带 `?` 占位的 SQL 必须补绑定值**，否则报的是 `Incorrect number of bindings supplied`，
   那不是字段缺失——是**误报**（第一版就栽在这，10 条假红）。
2. **别拿"网关有、切换器没有"直接当断链**：切换器只显示 DSH 选了的渠道，
   且网关自己 `unsupported` 的渠道本来就不算额度。判据要看**两侧口径是否一致**。
3. **DSH profile 的渠道集合要从 `- id: <provider>/` 抽**，不是从网关渠道表推——
   两者本就不该相等（`chatshare`/`webimage` 在 DSH 里选了但不在网关 credit-summary 里）。

## 六、遗留（未做，等郭老师点）

- 切换器里 `except Exception: pass` 的静默吞异常本身还没改（自检只是**外部探针**，不是根治）
- 旧目录备份 `D:\Tools\WorkBuddy-Account-Switcher.bak-20261021_0032` 还在（可回滚用），确认无误后可删

## 七、切换器并入 ai-hub 仓（2026-10-21 00:32）

- **真源**：现在在 `D:\项目\ai-hub\buddy2api\switcher\`（54 个文件，已提交 `6787b0b`）。
  `D:\Tools\WorkBuddy-Account-Switcher` 变成指向它的 **junction** —— **同一份文件，改哪边都一样**。
- **为什么用 junction 而不是直接搬走**：切换器内部有一堆硬编码自身路径
  （`tps_probe.py` 的 OUT、`_reload_switcher.bat`、`_restart_self.bat`、`启动账号切换器.bat`、
  `auto_ask_poll.py`、`free_model_probe.py`）⇒ 保留原路径当 junction，**这些路径一行没改仍然有效**。
- **凭据边界**：`profiles/*/workbuddy-desktop-ai.info` 是**加密登录态**（access/refresh token），
  `.gitignore` 已排除 `buddy2api/switcher/profiles/`；提交后核对过**提交内无 profiles 文件**。
  另排除 `tps_result.json`、`*.log`、`__pycache__/`、`ui/*.bak*`。
- **自检脚本跟着改**：`check_switcher_sync.py` 的 `SWITCHER_DIR` 指向**仓内真源**，junction 路径作 fallback。
- **迁移后复跑**：契约自检 **PASS 全通**，切换器从 junction 路径重启正常（PID 4700）。
- ⚠️ **旧目录是改名保留、不是删除**：`D:\Tools\WorkBuddy-Account-Switcher.bak-20261021_0032`
  —— **2026-10-21 07:42 已清空**：79 个文件全部移入回收站（其中 8 份 `ui/*.bak*` 历史版本
  已先保全到仓内 `ui/`），只剩 12 个**空目录壳**（回收站只收文件、拒收 workspace 外的目录级目标，
  未绕过）；空壳无害，可手动删除。

