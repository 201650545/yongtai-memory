---
name: lesson-adb-中文输入与剪贴板坑
description: adb 中文 input text 会崩，Android 16 没有剪贴板命令且 Clipboard.getData 可能取不到；依赖剪贴板的交互必须有降级路径
type: lesson
updated: 2026-10-22
kind: rule
status: active
scope: 通用
---

已存在同主题条目：`参考/reference_手机ADB驱动Gemini通道.md:54-56`；本条为其补充/修正，请合并时替换。

# adb 中文输入与剪贴板坑

**结论**：adb 的**中文 input 会崩**
（`adb shell input text "测试中文"` → `java.lang.NullPointerException: Attempt to get length of null array`）；
**Android 16 没有剪贴板**（`adb shell cmd clipboard` → `No shell command implementation.`），
且 App 内 `Clipboard.getData` **可能取不到**。

**判据**：

- **依赖剪贴板的交互必须有降级路径**：手动粘贴框 / 可粘贴文本控件 / 文件导入，三者至少留一条。
- 不要把剪贴板当成**必选**通道（它还受系统隐私限制与后台限制影响）。
- 需要往手机送中文时：走 CDP 控浏览器、或用纯英文/ASCII 的 `input text`，或改走应用内自带的输入通道。

**依据出处**：`参考/reference_手机ADB驱动Gemini通道.md:54-56`
（2026-10-16 实测记录：中文 `input text` 崩、`cmd clipboard` 不存在、本机无 ADBKeyboard）。
