---
name: reference-gemini-via-adb-phone-channel
description: 用 adb 驱动小米 14 上的 Gemini APP（com.google.android.apps.bard）作为第三条 Gemini 通道，绕开 opencli 网页版的活跃标签抢占与代理卡顿；含已验证/未验证清单与操作要点（2026-10-16 建）
metadata:
  node_type: memory
  type: reference
  created: 2026-10-16
  modified: 2026-10-16
type: reference
updated: 2026-10-19
kind: reference
status: active
---

# 手机 ADB 驱动 Gemini 通道（第三条通道）

> **建立**：2026-10-16 ｜ 来源：郭老师提出「你自己调用 ADB 直接打开我的 Gemini APP，自己去提问」
> **定位**：Gemini 的第 3 条通道。前两条是①opencli 驱动 Gemini 网页版（`gemini-web-review` skill）、②郭老师手机提问后复制粘贴。
> **状态**：**2026-10-16 11:30 实测定论 —— APP 直驱路线因「中文输入不可用」搁置**；
> **替代路已探通：CDP 控手机 Kiwi 浏览器**（注入文本不需要输入法，中文可通）。
> 郭老师 2026-10-16 判定「**电脑上的 Gemini 稳定了，直接在电脑上用**」⇒ 本通道**降为备用**。

---

## 一、为什么值得专门记一条

网页版通道（opencli）这次连踩三个坑：活跃标签被抢、标签 id 回收复用、站点实例自行漂移（vip-20 → vip-21）。
**ADB 直驱手机 APP 完全绕开这三样**：不经过桌面浏览器、不占活跃标签、也不受桌面代理链路影响
（郭老师实测：桌面代理很卡时，手机上 Gemini 已经出了答案）。

## 二、环境事实（2026-10-16 实测）

| 项 | 值 |
| :--- | :--- |
| adb 路径 | `D:\android-sdk\platform-tools\adb.exe`（**不在 PATH**，必须写全路径） |
| adb 版本 | `1.0.41` / `37.0.1-15733141` |
| 设备 | 序列号 `bf6ef967`，`product:houji model:23127PN0CC` = **小米 14**（`adb devices` 显示 `device`，在线） |
| Gemini 包名 | `com.google.android.apps.bard` |
| Gemini 版本 | `1.0.971139365` |
| **当前档位** | **`Argon High`** —— 手机端已经是郭老师定的档位，无需再设 |
| 启动后前台 | `com.google.android.googlequicksearchbox/com.google.android.apps.search.assistant.surfaces.voice.robin.main.MainActivity` |

## 三、✅ 已验证 / ⬜ 未验证（**接手前必读，别把未验证当已具备**）

| 环节 | 状态 | 证据 |
| :--- | :---: | :--- |
| adb 可连手机 | ✅ | `adb devices -l` 返回 `bf6ef967 device` |
| 启动 Gemini APP | ✅ | `adb shell monkey -p com.google.android.apps.bard -c android.intent.category.LAUNCHER 1` → 前台切到 robin MainActivity |
| 读界面文本 | ✅ | `uiautomator dump` 产出 42,278 字节 XML；正则 `text="([^"]{2,})"` 取到可见文本 |
| 确认当前档位 | ✅ | dump 文本里出现 `Argon High` |
| **跳过引导页** | ✅ | 2026-10-16 实测：**两屏**。① `Look what you can do with Gemini 4` → 点 `Let's go`；② `Take big ideas all the way` → 点 `Try Gemini 4`。两屏点完才进 Chat（出现 `Chat`/`Task`/`Argon High`） |
| **输入问题并发送** | ❌ | 2026-10-16 实测：中文**走不通**（见下两行）。英文/ASCII 未单独测 |
| **轮询取回答** | ⬜ | 未试。预期反复 `uiautomator dump` 直到文本稳定；**长回答可能被截断**（uiautomator 只给可见文本，需要滚动） |
| 中文 `input text` | ❌ **崩** | 2026-10-16 实测 `adb shell input text "测试中文"` → **`java.lang.NullPointerException: Attempt to get length of null array`**，坐实高风险 |
| `cmd clipboard` 剪贴板 | ❌ **不存在** | 本机 Android **16**，`adb shell cmd clipboard` → **`No shell command implementation.`** |
| 机上是否有 ADBKeyboard | ❌ **没有** | `pm list packages` 无 adbkeyboard/clipper 类包；已装输入法为豆包/百度/微信/搜狗/讯飞/小米安全，**均无法被 ADB 直接驱动** |
| **CDP 控手机 Kiwi（替代路）** | ✅ **已探通** | 见下方「七、替代路」 |

## 四、操作要点

```powershell
$adb = 'D:\android-sdk\platform-tools\adb.exe'      # 全路径，不在 PATH

# 1) 设备在线？
& $adb devices -l

# 2) 启动 Gemini（monkey 比 am start 稳，不用记 Activity 全名）
& $adb shell monkey -p com.google.android.apps.bard -c android.intent.category.LAUNCHER 1

# 3) 取界面文本（比截图 OCR 可靠，直接拿 text 属性）
& $adb shell uiautomator dump /sdcard/ui_ab.xml
$xml = & $adb exec-out cat /sdcard/ui_ab.xml | Out-String
[regex]::Matches($xml, 'text="([^"]{2,})"') | ForEach-Object { $_.Groups[1].Value } | Select-Object -Unique

# 4) 截图（要看版面时）
& $adb exec-out screencap -p > shot.png
```

**坑**：
1. `adb shell "dumpsys ... | grep ..."` 会报 `Failed to write while dumping service activity: Broken pipe`
   —— **只是 stderr 噪音，结果本身有效**，不要据此判定失败。
2. **启动 APP 会顶掉郭老师手机当前的前台应用**（本次顶掉的是他自己的 `com.listenloop.listenloop`）。
   ⇒ 动他手机前先说一声；他正在用 ListenLoop 时更要谨慎。
3. `uiautomator dump` 只覆盖**当前可见**的节点 —— 长回答要配合滚动，否则会以为"它没答完"。

## 五、郭老师定的两条 Gemini 使用路径（2026-10-16）

1. **他在手机上提问 → 复制粘贴给我**（已用过一次：44 条页脚文案就是这么来的）
2. **我用 ADB 直驱他的 Gemini APP，自己提问、自己取回**

> 郭老师原话：「暂时不用 Gemini 吧。如果想要用 Gemini 也可以：1）我在手机上提问，然后复制发给你；2）或者你自己调用 ADB 直接打开我的 Gemini APP，自己去提问，然后把内容复制过来。」
> **⇒ 通道层面：不把 Gemini 作为默认依赖；要用就走上面两条，不走网页版。**

## 六、关联

- 通道①（网页版）：`D:\Work\元智能\10_AI自成长引擎\技能库\external-model-review\components\gemini-web-review\`
- 通道能力边界：[[reference_Gemini网页版能力与限制]]
- 同机既有手机工作流：`D:\小浣熊\_phone_cdp\`（`heal.ps1` 建隧道 + `cdp.mjs` 走 CDP 控手机 Chrome；
  走的是 `adb forward tcp:9222 localabstract:chrome_devtools_remote`，**控的是手机 Chrome，不是原生 APP** —— 与本条通道互补）
- 外脑路由：[[reference_外脑双通道任务路由表_GPT6Sol_vs_Gemini4Argon]]

---

## 七、替代路（2026-10-16 实测探通）：CDP 控手机浏览器

APP 直驱的死穴是**中文进不去**（无输入法入口）。而 `_phone_cdp` 那套走 **CDP 控手机浏览器**，
**注入文本靠 JS，完全不需要输入法** —— 中文这条路是通的。

```powershell
# 1) 建隧道（heal.ps1 会顺带反连 19825 / 19100）
powershell -ExecutionPolicy Bypass -File D:\小浣熊\_phone_cdp\heal.ps1
# 2) ★ 必须先启动 Kiwi，socket 才存在（不启动则 forward 建了也连不上）
& $adb shell monkey -p com.kiwibrowser.browser -c android.intent.category.LAUNCHER 1
Start-Sleep -Seconds 8          # 实测：起完才通，早了会 "连接被意外关闭"
# 3) 验证
Invoke-WebRequest http://127.0.0.1:9222/json/version     # 应返回 Android-Package: com.kiwibrowser.browser
& node D:\小浣熊\_phone_cdp\cdp.mjs list
```

| 项 | 实测值 |
| :--- | :--- |
| devtools socket 名 | **`chrome_devtools_remote`**（Kiwi 沿用 Chrome 的抽象 socket 名；`kiwi_devtools_remote` 等**均不存在**） |
| `/json/version` | `{"Android-Package":"com.kiwibrowser.browser","Browser":"Chrome/137.0.7337.0"}` |
| 时序坑 | **先起浏览器再连**；浏览器没起完时表现为 `SocketError: other side closed`（不是"没有 socket"） |
| 手机上其他 devtools socket | 仅有 `@webview_devtools_remote_<pid>`（WebView，非浏览器） |

**⚠️ 动手机前必说一声**：启动 APP / 浏览器会顶掉郭老师的前台应用（本次顶掉 `com.listenloop.listenloop`）。
**用完要还回去**：`& $adb shell monkey -p com.listenloop.listenloop -c android.intent.category.LAUNCHER 1`。

**定位**：本路虽已探通，但 2026-10-16 郭老师已确认**电脑网页版 Gemini 稳定可用**
（见 `gemini-web-review` skill），**优先走电脑版**；本条保留为备用。
