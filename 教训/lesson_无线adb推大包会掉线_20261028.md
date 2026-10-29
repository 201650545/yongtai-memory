---
name: lesson-无线adb推大包会掉线
description: 走无线 adb install 200MB+ 的 APK，会在数分钟后失败且错误信息为空，真实原因是无线连接掉线（device 变 offline），不是 MIUI 安装拦截；判据是失败时先看 adb devices
type: lesson
updated: 2026-10-28
kind: fact
status: active
scope: 晨读
---

# 无线 adb 推大包会掉线，不是安装被拦

## 现象（2026-10-28 实测）

`adb -s 192.168.100.100:44485 install -r app-debug.apk`（224,765,636 B）：

- 跑满 **8 分 22 秒**后失败；
- 错误输出是**空的**：`failed to install ...: `（冒号后面什么都没有）；
- 同一时刻 `adb devices` 里该设备状态从 `device` 变 **`offline`**。

## 根因

**不是** MIUI/HyperOS 的安装监控拦截（当时 `settings get global install_monitor` ＝ 0、
`adb_install_need_confirm` ＝ 0，两项都已是放行态），也**不是**包损坏。
是**无线调试通道在长时间大流量传输中掉线**，install 因此半途失去设备。

## 判断顺序（别搞反）

1. 失败后**第一动作**是 `adb devices -l` —— 看设备还在不在、是不是 `offline`；
2. 设备 offline ⇒ 通道问题，重连或改 USB，**不要**去翻 MIUI 那几个开关；
3. 设备仍是 `device` 且 install 报具体码（如 `INSTALL_FAILED_USER_RESTRICTED`）⇒ 这才去查系统拦截。

## 处置

- **>200MB 的 APK 一律走 USB**：同一份包换 USB 后 **7 秒**装完（实测）。
- 必须走无线时，接受"大包分次/更大超时"的代价，并在失败后先确认连接存活。

## 延伸（同批实测，可复用）

- **版本"最新"不能用 versionName 判断**：两台机器 versionName 都是 `0.9.3`，
  但一台装的是当天 12:00 的构件、另一台还停在 09:03 的旧构件。
  判据是 `dumpsys package <pkg> | grep lastUpdateTime` 与构建产物 sha1，不是版本号字符串。

## 关联

- 记忆：[[项目/project_晨读]]
- 同类坑：`全局变更广播.md` 第 10 条（MIUI 安装监控拦 `adb install` 的解法）——
  **本条的教训是"别把它当默认答案"**，两种失败长得像、根因不同。
