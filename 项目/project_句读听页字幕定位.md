---
name: project-句读听页字幕定位
description: 2026-10-21 听页字幕「上下流转不平滑」的根因与定案：定位机制收敛成**单一可取消的请求**（animateTo ＋ 代次标记），坐标统一用**全局屏幕 Y**，焦点线不在视口内就**不定位**（不再追负坐标跳到边界），ListView 显式 `EdgeInsets.zero`（默认安全区 padding 会污染坐标），可见行只跟踪**已挂载行**。附：中文注音布局的**字重变化会改字格宽度⇒改行高⇒整列位移**（当前句变粗的隐藏代价）。
metadata:
  node_type: memory
  type: 项目
  created: 2026-10-21
  modified: 2026-10-21
type: project
updated: 2026-10-21
kind: fact
status: active
scope: 句读听页字幕定位
---

# 句读：听页字幕定位（2026-10-21）

## 用户报的现象（原话）

> 「听页字幕上下流转动画不平滑」

拆成三条：① 切句时**先跳一下再动**（像"卡"的一下）；② 偶尔**整列字幕瞬移**一段距离；
③ 快速连播时**动画互相打断**，字幕位置和正在读的那句对不上。

## 定位机制：原来有**四套**可能互相打架的机制

| 机制 | 原来的写法 | 毛病 |
| :--- | :--- | :--- |
| 平滑滚动 | `_alignRowIntoShape` → `animateTo(220ms)` | 与下面的硬跳并发 |
| 硬跳自校正 | `_settleOnScreenMiddle` → 260ms 后最多 4 轮 `jumpTo` | **动画播到一半被瞬移打断**（"卡卡的"） |
| 过期回调 | `addPostFrameCallback` + 延迟校正 | **无版本管理** ⇒ 快速连播时旧请求把列表拽回旧位置 |
| 估算跳转 | 常数 `_estimatedRowHeight = 175.0` | 课文行高 1~3 行不等 ⇒ 大跳转必偏 ⇒ 又要靠硬跳补 |

## 坐标：两套坐标系混用（独立于动画的第二处错）

- `_desiredRowTopInViewport()` 返回**视口局部 Y**（`screenHeight*0.28 - viewportTop`），
  而 `_computeVisibleIndex()` 拿行的**全局屏幕 Y** 去跟它比 ⇒ **坐标系混用**。
- 列表上方若有视频区，`viewportTop > screenHeight*0.28` ⇒ 焦点线算出来是**负数**
  ⇒ 目标永远达不到 ⇒ 只能 clamp 到边界 ⇒ **整列瞬移**。
- `ListView` 不显式设 `padding` 时会**自动套 MediaQuery 安全区 padding** ⇒ 坐标再偏一层。

## 定案（已落地，commit `a60a80e`）

1. **一个定位通道**：只有一条 `animateTo`（线性曲线，时长与距离成比例 160~420ms）；
   `jumpTo` 只在「明确要求立即定位」时用（`revealToken`/数据变化/模式切换）。
2. **代次标记** `_alignmentGeneration`：每次新请求 +1，旧请求的 post-frame 回调与
   动画完成回调一律作废 ⇒ 快速连播不会被旧请求拉回。
3. **坐标统一**：目标偏移一律用**全局屏幕坐标**算（`position.pixels + rowTopGlobal - focusScreenY`）。
4. **不可达就不定位**：`_focusIsReachable()` 判焦点线是否在视口内；不在就**不滚**，
   而不是追着负坐标跳到列表末尾。
5. **`ListView` 显式 `padding: EdgeInsets.zero`**（坐标由组件自己统一算）。
6. **可见行只扫已挂载行**（`_mountedRowIndices` 注册表），不再每帧遍历整篇课文做
   `findRenderObject()+localToGlobal()`。
7. **移除 `AnimatedDefaultTextStyle`**（文字度量逐帧插值会改行高）；`AnimatedContainer`
   只留背景色/强调线颜色过渡（几何恒定）。
8. **`initState` 也要对齐第 0 句**（原来只在 `currentIndex > 0` 时定位 ⇒ 首句入页位置不对）。

## ★ 一条被实测否掉的猜想（别再当根因）

曾以为「当前句字重 w400→w600 ⇒ 中文重新折行 ⇒ 行高变 ⇒ 整列位移」＝ "先跳一下"的主因。
**实测否掉**：注音布局按固定 `charSize` 排字格，测量出来的字宽只用于绘制，
⇒ 短句与**多行长句**切句时行高**完全不变**（已固化成回归测试）。
⇒ 真正的根因是上面那四套定位机制互相打架，不是字重。

## 回归网（不装真机就能判）

`test/widgets/subtitle_geometry_test.dart`（4 项）：
① 切句不改变任何一行高度；② 当前句对齐到屏幕 28% 焦点线；
③ 快速连切后停在最新一句（旧请求不得拉回）；④ 注音布局字重变化不改高度。

⚠️ `test/screens` 与 `test/widgets` 有 **24 项既有失败**（与本次改动无关，
用 `git stash` 同口径对照确认过）——别把既有烂账算到新改动头上。

## 真机验收（2026-10-21 16:20，小米 14 `bf6ef967`，装机后实测）

| 项 | 结果 |
| :--- | :--- |
| 听页字幕定位 | 切第 11 句 / 第 12 句连拍：**灰块始终钉在同一屏幕位置**，内容每次正好上移一行 ⇒ 定位连续、无瞬移、无跳顶 |
| 焦点线口径 | 听页视口 28%（= 改口径后）与读页视口 28% **同一把尺**，真机两边都对得上 |
| 读页记录 | 点圆形按钮 → 回显栏出现识别文本，**逐字上色**（读对的全绿、读错的字红） |
| 口令 | 按钮提示已是「说「**开始朗读**」开始」；logcat 里识别文本**第一个字就是「开始朗读」** ⇒ 新默认口令真机命中 |
| 流式链路 | `[LiveRead] pcm pushed=350` → `[LiveRead][worker] pcm=350 text="开始朗读长出两条后腿…"` ⇒ PCM→worker→文本流 整条链打通（上一轮因点击坐标不对从未验证过） |
| ASR 模型 | 三个模型真机在位（流式 zipformer-ctc、x-asr transducer、离线 zipformer-ctc-small） |

⚠️ 回授提醒：真机录音会**录进手机自己播的课文**（识别文本里出现当前句重复）⇒
`RecordConfig.echoCancel: false` + 页面自动播放 = 回授源，仍待处理。

## 送审渠道的坑（这一轮踩的，见能力总账与 skill CHANGELOG）

- 共享 Chrome 的**活动标签会被别的 Agent 抢走**；opencli 会话**一次只绑一个标签**，
  `tab new` 会抢绑定 ⇒ **两条浏览器通道必须串行**。
- `eval --tab <pageId>` 在 opencli v1.8.8 **是支持的**（能力总账原来那条「不认 --tab」是错的）。
- 镜像站**新会话**的 cid 带 `WEB:` 前缀 ⇒ `/backend-api/conversation/<cid>` 取不到；
  要等 URL 改写成**裸 uuid** 才能按 `create_time` 排序取回。
- 镜像站答案的**代码块只在 DOM 的 `<pre>` 里**，API 的 `content.parts` 文本里没有 ⇒
  取代码要从 DOM 捞。
