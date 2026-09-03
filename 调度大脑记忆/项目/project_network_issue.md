---
name: home-wifi-proxy-issue
description: 电脑连家里Wi-Fi无法使用Sparkle代理，根本原因是旧Wintun虚拟网卡驱动残留与新代理冲突，已修复
metadata: 
  node_type: memory
  type: project
  originSessionId: d2f46b38-1e99-48c4-bd86-24f96dd97893
  modified: 2026-08-31T09:10:05.431Z
---

## 问题描述（已修复）

电脑连家里 Wi-Fi 时，Sparkle 代理无法使用。手机连同一个 Wi-Fi 则代理正常，说明问题在电脑端，不在路由器/ISP。

## 根本原因

**旧的代理软件残留的 Wintun 虚拟网卡驱动与 Sparkle 冲突。**

故障链：
1. 之前安装过其他代理软件，装了 Wintun 虚拟网卡
2. 卸载代理后 Wintun 驱动残留
3. Wintun 和 Wi-Fi 网卡冲突 → 代理开启时网络断开
4. 同时 TUN 模式处于"半死状态"：设备存在、路由存在（以最高优先级劫持流量），但代理核心未正确处理 → 流量进了 TUN 出不去

## 修复过程

1. 卸载旧的 Wintun 虚拟网卡 — 消除冲突源
2. 重新安装 Sparkle — 使用新的 Meta Tunnel 驱动
3. TUN 模式恢复正常工作

## 教训

- 手机连同一个 WiFi 能用代理 → 问题在电脑端，不是网络层面
- 之前错误判断为运营商/路由器问题，浪费了时间
- 问题可能有多个叠加因素（驱动残留 + TUN 半死状态 + 路由劫持），不一定是单一原因

## 2026-08-31 第二次复发：WiFi 2322 Sparkle 全挂（已修复）

**现象**：连 2322 WiFi 时 Sparkle 订阅更新失败、代理连不上；手机同一 WiFi 同订阅正常；且「第一次连此 WiFi 时是好的，后来莫名其妙失效」。

**根因（IPv6 死链）**：mojie 订阅配置 `19aca179dec.yaml` 与全局 `mihomo.yaml` 都是 `ipv6: true`，节点域名 `m.cnmjin.net`/`t.cnmjcn.cyou` 后来加了 AAAA 记录（2400:8905::...），mihomo 优先连 IPv6 → 而节点 IPv6 是死的。IPv4（109.229.216.80/81、82.38.46.77）一直可达。这解释了「第一次能用（当时域名只有 A 记录）→ 后来失效（域名加了 AAAA）」的时间线，也解释了手机能用（手机端未开 IPv6）。

**修复**：两个文件共 4 处 `ipv6: true → false`（mihomo.yaml 顶层+dns段；19aca179dec.yaml 顶层+dns段，防订阅更新覆盖），自提权重启 Sparkle + Clash Core Service 后 google/baidu 全通。备份 `.bak_ipv6`。

**教训**：
- TCP 全失败 ≠ 网络封锁。必须用国内可达 DoH（doh.pub，注意 cloudflare-dns.com 本身被墙会 Connection reset）查权威 A+AAAA 记录：A 存在且可达 = 走 IPv4 就能通，问题在「为什么没用 IPv4」。
- 「以前能用后来失效」的 Mystery，优先怀疑**上游变了**（域名加 AAAA、证书、端口），不是本机坏了。
- Sparkle/Clash Core Service 都以管理员运行，普通 shell 的 Stop-Process 会静默失败；须自提权脚本（UAC 用户点「是」）。

## 系统信息（2026-04 首次）

- 系统：Windows 11 Home China 10.0.26200
- Wi-Fi 网卡：Realtek RTL8852BE WiFi 6 802.11ax
- 接口名：WLAN
- 代理软件：Sparkle（使用 Meta Tunnel 驱动）
- 旧驱动：Wintun（已卸载）
