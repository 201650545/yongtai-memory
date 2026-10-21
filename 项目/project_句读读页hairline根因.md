---
name: project-句读读页hairline根因
description: 🟡 2026-10-21 定位并修复「读页只显示一句、其余大片空白」的根因：BoxDecoration 同时给了 borderRadius(10) 与 width:0 的 BorderSide（hairline）⇒ Flutter 规定 hairline 只能配零圆角 ⇒ paint() 阶段抛断言 ⇒ 那一行整行画不出来 ⇒ 只有当前句（width 2）能渲染。真机数据（69 句 chinese）全部正常，**不是数据问题**。修法：左边框宽度恒为 2dp 只换颜色；左内边距所有行一致避免整列横向跳。已配 paint smoke + golden 回归，并验证「改回旧写法测试立刻红」。
metadata:
  node_type: memory
  type: 项目
  created: 2026-10-21
  modified: 2026-10-21
type: project
updated: 2026-10-21
kind: fact
status: active
scope: 句读读页hairline根因
---

# 句读：读页「只显示一句」的根因（2026-10-21）

## 症状

读页只渲染出一句「看见荷叶上」，定位区却写「第 17 / 69 句」，其余大片空白。
同一课在听页显示正常（59 句有内容）。

## 排查路径（下次同类问题照走）

1. **先怀疑数据** ⇒ 用 adb 把真机课包拉下来看：
   `adb shell "run-as com.phrasing.phrasing cat app_flutter/lessons/<id>/chunks.json"`
   → 69 句 `chinese` **全部有内容**，平均 5.9 字。**数据没问题**。
2. 别停在「数据没问题」⇒ **写 widget test 复现**（用真机那份真实 69 句喂进去）
   → 立刻炸出 **9 个 paint 断言**。
3. 断言原文：`A hairline border like BorderSide(width: 0.0, style: BorderStyle.solid)
   can only be drawn when BorderRadius is zero or null.`

## 根因

`lib/widgets/lesson_reading_document.dart` 的句子容器：

```dart
decoration: BoxDecoration(
  borderRadius: BorderRadius.circular(10),
  border: Border(left: BorderSide(width: isCurrent ? 2 : 0, ...)),  // ← 0 是 hairline
)
```

Flutter 规定 **hairline 边框（width 0 + solid）只能配零圆角**。非当前句 width=0
⇒ 圆角非零 ⇒ **paint() 抛断言 ⇒ 那一行整行画不出来**。
当前句 width=2（正常边框）⇒ 能画 ⇒ 整页只剩那一句。

## 修法（已落地）

- 左边框**宽度恒为 2dp**，只换颜色（当前句强调色 / 其余透明）。
  绝不能写 `width: isCurrent ? 2 : 0`。
- 左内边距**所有行一致**（12dp）⇒ 当前句来临时整列文字不横向跳
  （这是听页踩过的「字幕抖动」坑的同款）。
- 同步修：定位区 / 句单高亮 / 课文灰块**统一到识别游标**
  （原先定位区报音频控制器句号、灰块跟识别游标，两个真源各说各话）。
- 听页灰色形状改回**跟随当前句**（原为钉在屏幕中线的固定聚光块），
  滚动定位改为把当前句对齐到视口上三分之一。

## 回归网（已建并验证）

- `test/widgets/reading_document_paint_test.dart` —— paint smoke ×3 + golden ×1
- `test/widgets/reading_document_real_data_test.dart` —— 整课多句渲染
- `test/widgets/reading_document_shots_test.dart` —— **三屏视觉基线**
  （head / middle / tail），不装真机也能一眼肉眼验收整篇是否渲染出来
- `test/dev/reading_preview_smoke_test.dart` —— Preview 入口能起来
- **已验证**：把代码改回 `width: isCurrent ? 2 : 0`，测试立刻红并精确指出 hairline 断言。

## 落点（2026-10-21）

- main：`8b38bf8`（根因+三件套）、`150e74f`（golden 真实字体）、`1ec38bc`（装机脚本+长图）、
  `105f8fd`（三屏基线）、`3268c29`（脚本自动发现）
- 同步仓 `origin/code-sync-20261020`：`6c290c8` / `80ef7e9` / `f3cd851` / `07a4419`（远端 17/17 文件已核）
- APK：`build/app/outputs/flutter-apk/app-debug.apk`（01:12 构建，282MB，含全部修复）
- 装机：`.\tool\verify-on-device.ps1 -Device <ip:port>`

## 踩过的测试坑

- ruby 排版是**逐字 `Text`** ⇒ `find.text('整句话')` 匹配不到，只能按单字找。
- `SliverList` **懒加载** ⇒ 滚到第 46 句时第 1 句早就不在树里，「首句不在树里」不是 bug。
  断言要写成「当前句附近的若干句都在」。
- `LessonReadingDocument` 有 `initialSentenceIndex` ⇒ 测试里要传，
  否则初始滚动停在第 0 句，目标句没被铺出来。
- `flutter_test` 默认 **Ahem 测试字体** ⇒ 中文全渲染成方块，golden 等于白做。
  要 `FontLoader` 加载 `assets/fonts/SongTi.ttf`（在 `flutter/services.dart`，不在 dart:ui）。
- `RenderRepaintBoundary.toImage()` 在 flutter_test 里**会卡住不返回**
  （844px 也卡）⇒ 离屏出图一律走 golden 机制。

