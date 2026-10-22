---
name: lesson-dsh桌面端认证cookie累积崩溃
description: 2026-10-22 DeepSeek Harness 桌面端启动即崩（desktop welcome: Web authentication failed）的真因＝认证 Cookie 按随机端口累积，Cookie 头超 16KB 被 Node 服务端拒收；清 dsh-auth-* Cookie 即恢复，与插件无关
metadata:
  node_type: memory
  type: 教训
  created: 2026-10-22
  证据链: crash-*-host.log 报错点 connectDesktopWelcome → app.asar 内 dsh-desktop-host 写死 --port 0 → client-connection 认证 Cookie 名绑定 host:port → 71 个 dsh-auth-* 累积使 Cookie 头达 16.1KB → Node maxHeaderSize 16KB 拒收
  对照实验: 注入 71 个真实尺寸 Cookie 复现崩溃；注入 70 个短 Cookie(≈1KB) 正常 → 阈值是字节数不是数量
  修复脚本: C:\Users\郭永涛\.dsh\tools\fix-dsh-auth.ps1
type: lesson
updated: 2026-10-22
kind: rule
status: active
---

# DeepSeek Harness 桌面端启动即崩：认证 Cookie 累积撑爆 16KB 请求头

**现象**：桌面端启动即崩，`logs\crash-*-host.log` 里是 `Error: desktop welcome: Web authentication failed`，
每 8~15 秒重复一次。点"禁用第三方插件"无效。

**真因链**：

1. 桌面端 Host 每次启动用**随机端口**（`app.asar` → `dsh-desktop-host/lib/index.js` 写死 `--port 0`）；
2. 认证 Cookie 名绑定 `host:port`（`dsh-auth-<sha256(authority)>`），而 Cookie **不区分端口**
   ⇒ 每启动一次，`127.0.0.1` 下多一个 `dsh-auth-*`；
3. Chromium 每次请求带上该 host 下**全部** Cookie ⇒ Cookie 头单调增长（每个约 230 字节）；
4. 累积到约 **16KB** 时超过 Node HTTP 服务端 `maxHeaderSize`（16KB）⇒ 服务端拒收该请求，
   桌面端拿不到 2xx ⇒ 报"Web authentication failed"。

**判据**（用来区分真因与假象）：

- 只带**单个**正确 Cookie 用 curl 请求 ⇒ 200（看起来完全正常）→ 这类"能跑通"的验证不足以定因；
- 必须复刻**带全量累积 Cookie 的浏览器侧请求**才复现；
- 对照实验：70 个短 Cookie（≈1KB）正常，71 个真实尺寸 Cookie（≈16.1KB）必崩
  ⇒ 阈值是**头部字节数**，不是 Cookie 个数。

**正解**：

- 清空 Electron Cookie 库里的 `dsh-auth-*`（保留其它 Cookie/会话/登录态）⇒ 立刻恢复；
  一键脚本：`C:\Users\郭永涛\.dsh\tools\fix-dsh-auth.ps1`。
- **不要**删整个 `~/.dsh/.credentials.yaml`（会连带清掉全部 API Key；本次密钥签名经逐条校验全部有效，与故障无关）。
- **不要**指望改 profile 的 `webServer.port` 固定端口：命令行 `--port 0` 优先级更高，
  实测端口仍随机；且应用有 "Desktop profile recovery" 会自动回滚被改坏的 patch 文件。

**插件的关系**：本次故障与插件无关（`cordis.patch.yml` 19 条配置全程完好）。
但"禁用第三方插件"确实把 `profiles\desktop\package.json` 的 `dsh.profile.bundles` 从 7 条砍到 2 条
（丢了 `@local/jingwei`、`@local/model-panel`、`dsh-experimental-auto-review`、
`dsh-experimental-agent-team-profile`、`dsh-experimental-inspector-profile`），
已于 2026-10-22 按 10/21 备份恢复。

**可复用套路**："Electron 应用认证失败"类问题 → crash log 定位函数 → 反查 asar 源码 →
分清 Node 侧与 Chromium 侧两条不同 HTTP 通道 → 用"注入合成合法 Cookie"做对照实验区分数量阈值与字节阈值。
