---
name: lesson-workbuddy国际版不读系统代理
description: WorkBuddy AI 国际版（Electron，D:\wbuddy 国际版）是**应用内建代理模式**、完全不看 Windows 系统代理注册表：代理状态只存在 ~\.workbuddy-ai\settings.json 的两个 vscode 风格顶层键 http.proxy / http.proxySupport。缺省即 persisted mode=none ⇒ Chromium session.setProxy direct + undici/axios 直连，把系统代理整个旁路掉，表现为「魔戒明明连着，WorkBuddy 却显示无代理、www.workbuddy.ai:443 超时」。正解＝手写 http.proxy=http://127.0.0.1:7890 + http.proxySupport=override 后重启（或设置页保存一次即时生效），用 main.log 的 applied persisted manual proxy / session.setProxy: explicit proxy / PROXY 127.0.0.1:7890 三条日志验收
metadata:
  node_type: memory
  type: 教训
  created: 2026-10-20
  证据来源: 应用自带日志 ~\.workbuddy-ai\logs\main.log（persisted mode=none → session.setProxy: mode=direct → getAxiosAgentsForUrl: DIRECT_TRUSTED reason=no-proxy）+ app.asar 源码（applyPersistedProxyToBootstrapEnv / inferProxyModeFromVscodeFields / ProxySettingsService.toVscodeFields）
type: lesson
updated: 2026-10-20
---

# WorkBuddy AI 国际版不读系统代理（2026-10-20）

## 一、现象与判据

- 魔戒（mihomo）正常运行，`127.0.0.1:7890` 走代理出口 IP 正常，`https://www.workbuddy.ai` 经代理 HTTP 200；
  但应用「网络诊断」显示**无代理**，且直连 `www.workbuddy.ai:443` TCP 超时。
- 应用自己日志已写明原因（`~\.workbuddy-ai\logs\main.log`，时间为 UTC）：
  - `[startup-proxy] persisted mode=none; leaving env as-is`
  - `[WorkBuddy] Chromium proxy will use direct mode (persisted none, no PAC)`
  - `[WorkBuddy] session.setProxy: mode=direct (persisted none)`
  - `[NetProxy] getAxiosAgentsForUrl: DIRECT_TRUSTED url=https://www.workbuddy.ai/v3/config reason=no-proxy`

## 二、根因（源码级）

应用是 Electron 应用，代理模式走**自己的 settings.json**，不看系统代理注册表：

| 模式 | `http.proxy` | `http.proxySupport` |
|---|---|---|
| none（默认，缺省即此） | `""` | `"off"` |
| system | `""` | `"on"` |
| manual | 代理 URL | `"override"` |

- 判定函数 `inferProxyModeFromVscodeFields`：两个键都缺 → `mode=none`。
- 启动路径 `applyPersistedProxyToBootstrapEnv`：none ⇒ 不注入 env，Chromium 直接 direct。
- mode-aware resolver（`createModeAwareProxyResolver`）：none ⇒ 全部请求返回 `DIRECT`。
- 「系统代理」模式不推荐：依赖 `productFeatures.SystemProxyDetection`，读不到产品配置时**默认关闭**。

## 三、正解

1. 往 `C:\Users\<用户>\.workbuddy-ai\settings.json` **顶层**写：
   `"http.proxy": "http://127.0.0.1:7890"`、`"http.proxySupport": "override"`；
2. **重启应用**（启动时读回落盘值并注入 `HTTP_PROXY/HTTPS_PROXY`）；
   或在「设置→代理」页选手动代理保存一次（`applyProxySettings` 即时生效，不用重启）；
3. 验收（`main.log`）：
   `[startup-proxy] applied persisted manual proxy (mode=manual, url=http://127.0.0.1:7890)`、
   `[WorkBuddy] session.setProxy: explicit proxy=127.0.0.1:7890`、
   `[NetProxy] undici global dispatcher: EnvHttpProxyAgent (proxy=127.0.0.1:7890, ...)`、
   `[MainProxy] resolveProxy ... rule="PROXY 127.0.0.1:7890"`、
   `getAxiosAgentsForUrl: HTTPS_AGENT`（不再是 `DIRECT_TRUSTED`）。

## 四、坑位（别再踩）

- 只开 Windows 系统代理 → 对本应用**零作用**；
- 只设用户级 `HTTP_PROXY/HTTPS_PROXY` 环境变量 → 只救 Node 侧（undici/axios），
  Chromium 仍 `session.setProxy: mode=direct`，半吊子；
- 不重启已运行进程 → 进程环境是启动时快照。

## 五、关键路径

- 安装：`D:\wbuddy 国际版\WorkBuddyAI\WorkBuddyAI.exe`（国际版，`--user-data-dir=~\.workbuddy-ai\app`）
- 配置：`~\.workbuddy-ai\settings.json`
- 日志：`~\.workbuddy-ai\logs\main.log`、`~\.workbuddy-ai\logs\network\latest.json`（网络诊断快照）
- 取证：`resources\app.asar` 内搜 `applyPersistedProxyToBootstrapEnv` / `inferProxyModeFromVscodeFields` / `ProxySettingsService`

## 六、关联

- 代理环境本体见 [[project_network_issue]]（mihomo / Sparkle / 出口与 IPv6 那些坑）。
- 经验条目草稿：`D:\Work\元智能\10_AI自成长引擎\草稿区\L1_经验\L1_20261020_WorkBuddy国际版不读系统代理必须手写settings_json.md`
