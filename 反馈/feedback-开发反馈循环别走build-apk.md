---
name: feedback-开发反馈循环别走build-apk
description: 🔴 郭老师 2026-10-21 定：改 UI 反馈循环必须压到 10~30 秒——**不要每改一点就 flutter build apk + 装机 + 手点导航**（那要 180~240 秒，一个下午推进不了几件事）。他原话「一定要把这个软件分成层级，拆成几个小部分，最后再组装起来变成这个 APP。不要每次改一个小部分，都要把它重新组装起来再跑，太蠢了」。经 GPT 镜像站（ChatGPT 6 Sol）评审后落地为三条通道：真机 hot reload（1~5 秒）/ 独立 Preview 入口（1~5 秒）/ 局部 widget test + golden（3~15 秒）。执行含义：① 改 UI 优先 hot reload 或 Preview 入口，不 build apk；② paint 断言类 bug 用局部 widget test 自动抓，不靠肉眼；③ 提交前才跑全量测试，日常只跑受影响范围。
metadata:
  node_type: memory
  type: 反馈
  created: 2026-10-21
  modified: 2026-10-21
type: feedback
updated: 2026-10-21
kind: fact
status: active
---

# 开发反馈循环：别走 build apk

## 他的原话（逐字）

> 「现在改东西真的是越来越慢了，我觉得我们这个开发逻辑绝对是有问题的。」
>
> 「一定要把这个软件分成层级，拆成几个小部分，最后再组装起来变成这个 APP。不要每次改一个小部分，都要把它重新组装起来再跑，太蠢了！这种操作速度又慢，搞好久才有新的进展。」（2026-10-21 00:00 前后）

## 真实症结（GPT 镜像站评审结论，与他的直觉有出入）

他以为是「代码没分层」。评审的结论是：**不是分层问题，是把「构建发布包」当成了日常开发调试**。

30 多个模块的规模还没到必须拆 package 的程度。**先建三条通道**，再谈拆包。

## 落地（2026-10-21 已建）

| 通道 | 手段 | 耗时 |
| :--- | :--- | :--- |
| A 真机 hot reload | `flutter run -d <id>` 后按 `r`；`R` = 重启（改了 initState/main 才用） | 1~5 秒 |
| B 独立 Preview 入口 | `lib/dev/reading_preview.dart`，不起 sqflite/ASR/音频 | 1~5 秒 |
| C 局部测试 + golden | `test/widgets/reading_document_paint_test.dart` | 3~15 秒 |

配套：`tool/test-changed.ps1`（按目录裁剪测试范围）、`docs/开发反馈循环手册.md`（完整手册）。

## 执行含义（下次照做）

- 改 UI ⇒ hot reload / Preview，**不 build apk**。
- 改 paint/布局 ⇒ 先写局部 widget test（`takeException()` 抓 paint 断言），不靠真机肉眼。
- 提交前 ⇒ `.\tool\test-changed.ps1`；里程碑前才 `flutter test` 全量。
- 只有改原生/pubspec/assets 才需要重新 `flutter run`；只有发布才 `flutter build apk`。
- **给新组件建 Preview 入口**是最高性价比的一件事（半天成本，此后每个组件都省几分钟）。
- 判定「这块 UI 是否够独立」的**唯一标准**：能不能用固定输入在 `testWidgets()` 里直接构造它。

## 边界

- 这是**开发效率**规则，不是产品规则。
- 涉及设备/账号/推送/原生 SDK 的改动仍需真机验证 —— hot reload 不覆盖。
- 评审全文：`D:\Work\元智能\20_自适应工作流引擎\runtime\gpt_flutter_devloop_answer.md`（2026-10-21 GPT 镜像站会话「㉒ Flutter 开发反馈优化」）。
