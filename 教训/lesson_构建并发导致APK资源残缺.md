---
name: lesson-构建并发导致APK资源残缺
description: 两次 flutter build apk 并发抢同一 mergeDebugAssets 会产出只含 7 个 assets 的半残 APK；判据是 assets 条目≥29、含 FontManifest 与 5 个 ttf、总量≥120MB
type: lesson
updated: 2026-10-22
kind: rule
status: active
scope: 句读
---

# 构建并发导致 APK 资源残缺

**结论**：同一台机器上**两次 `flutter build apk` 并发**时，两路会抢同一个
`build/app/intermediates/assets/debug/mergeDebugAssets`，产出的 APK **只含 7 个 assets**
（缺全部字体、FontManifest、MaterialIcons、8 张主题图、词表、教材数据）。
装机后的表现是「很多内容没了 ＋ 字体切换零反应」——**不是代码错，是包残**。

**判据**（装机前必查，别靠肉眼）：

- APK 内 `assets/flutter_assets` 条目 **≥ 29**；
- 必须含 `FontManifest.json` 与 **5 个 ttf**（`SongTi / FangSong / Roboto-Regular / Roboto-Medium / Roboto-Bold`）；
- APK 总量 **≥ 120MB**（课包全量预置后 207MB 量级）。
- 门禁脚本：`D:\listenloop\tool\verify_apk_assets.py`。
- **同机同时只允许一个 build 在跑**；要并行就先确认没有第二个 build 进程。

**依据出处**：2026-10-22 句读构建事故（本轮实机复现与修复）；
合格样本实测：`build/app/outputs/flutter-apk/app-debug.apk` = assets 条目 29、ttf 6 个（含
`cupertino_icons` 的 `CupertinoIcons.ttf`）、含 `FontManifest.json`、207.3MB。
门禁脚本路径本轮 `Test-Path` **未命中**（文件尚未落地/改名），落地后须回填真实文件名。
