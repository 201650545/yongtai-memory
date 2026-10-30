---
name: reference-IDEA021-GitHub二次调研_20261030
description: IDEA-021 视频剪辑器的 GitHub 二次调研结论（外部 AI 作答，未经本机独立核实）：硬结论、待核实仓库清单、ASR/合成/auto-reframe/队列四项选型、对"要不要自研"的判断与三步试跑路线。
type: reference
updated: 2026-10-30
status: active
---

# IDEA-021 · GitHub 二次调研结论（2026-10-30）

> **来源**：外部 AI 按 `docs\调研\20261030_IDEA021_GitHub二次调研搜索任务书.md` 作答。
> **⚠️ 可信度声明**：本机当时**无代理、无法访问 GitHub**，以下内容**未经本机独立核实**。已按三档标注：
> 🟢 硬结论（与 2026-10-21 旧调研交叉一致或属确定事实）｜🟡 高价值待核实（须进仓确认）｜🔴 可疑（仓名/数据形态异常）。

## 一、🟢 硬结论（可直接用于设计）

1. **FableCut**（`project.json` 即接口、MCP+REST 驱动、零 npm 依赖）两次独立调研指向同一结论 ⇒ 是"AI 可驱动剪辑"这条线最干净的参照物；本文给的 ★734 / MIT / 2026-10-18 仍活跃 与旧调研 ★736 一致。
2. **concat demuxer 在混合帧率下会音画漂移**（有生产案例：demuxer 产出 164s 视频对 171s 音频，结尾唇音超 4%）。⇒ 段数多、来源不一时应走 **concat filter（重编码）**，或先统一帧率/分辨率/采样率再 trim。
3. **ffmpeg 的 crop 没有主体检测**。auto-reframe 必须"先跑检测器再把坐标喂给 ffmpeg"（PySceneDetect→YOLO→ByteTrack→坐标）。
4. **moviepy 老化**（最近 release 距约 450 天），走 subprocess 调 ffmpeg，批量任务慢 10~100 倍 ⇒ 不作为首选。
5. **WebCodecs 可做浏览器内低清预览**，但最终导出应回原生 ffmpeg；Chromium 容器常驻内存会顶高峰值。
6. **kinocut 的 Video Receipt / quality gates 没被更通用规范取代**，仍是审计层最完整实现；它的 MCP 工具形态可与 FableCut 的 typed tools / 锁定保护互补。

## 二、🟡 高价值待核实（动手前必须进仓确认）

| 候选 | 说法 | 待核项 |
|---|---|---|
| **OneTake** | `leejersey/OneTake`，Python+FastAPI+faster-whisper+FFmpeg+SQLite；字级时间戳 <100ms；删文字即剪；支持 9:16/16:9；2026-01-21 后约 9 个月未更新 | 星数、许可证、是否支持 Windows、真实渲染内存 |
| **AI驯剪 / ai-xunjian** | 中文口播"剪气口＋剪重说＋响度归一＋逐字字幕"，命令行初剪、输出工程文件 | **仓名格式异常（见下）**、许可证、工程文件结构 |
| **Rescript** | 2026-07，Descript 的开源平替，改字幕文字视频同步剪 | 仓全名、许可证、成熟度 |
| **CapShorts** | 2026-09，本地优先、word-accurate captions、一键竖版 | 仓全名、星数、许可证 |
| dawn-cut | `kwakseongjae/dawn-cut`，文本剪辑+去静音，但重心是韩语 | 许可证；中文场景基本可排除 |

## 三、🔴 可疑项（勿直接采信）

- **`fxl1209739475-fxl/ai-xunjian`**：账号名形态像"用户名重复拼接"，不像真实 GitHub 账号；且星数、许可证全缺。⇒ **必须进仓确认存在性**，否则不得引用。
- 多处"未查到许可证"（OneTake、AI驯剪、dawn-cut、CapShorts）——**AGPL 风险未排除**，而 Work 仓准备公开，未经确认不得集成。

## 四、四项选型结论（🟡 需实测验证）

1. **ASR**：FunASR/SenseVoice 中文准确率与速度优于 Whisper（外部数据：错误率 7.81%/10.18% vs 20.02%，推理快 10~12 倍），**但只给句级时间戳**；WhisperX 词级时间戳成熟但中文准确率次之。
   ⇒ 两条现实路径：① 准确率优先＝FunASR 转写 + WhisperX/强制对齐细化到词级（管线长）；② 简洁优先＝直接用 WhisperX。**不建议拿句级时间戳做逐词剪辑。**
2. **合成层**：`ffmpeg-python`（生成可读 filter_complex）+ subprocess 兜底；需要帧级访问再上 PyAV。moviepy 不用。
3. **auto-reframe**：口播且人物不走动 ⇒ **固定偏移 + 人工选一帧 x 坐标**比任何跟踪都稳且省内存；人物会动才上 `auto-vertical-reframe` 的 YOLO+ByteTrack（注意 YOLO 会顶高内存）。
4. **作业队列**：`concurrent.futures.ProcessPoolExecutor` + subprocess + SQLite 记账即可，不引 Celery/Redis。**失败重试前必须删半截坏文件**，否则 concat 阶段会崩。

## 五、对"要不要自研"的判断

- **没有单一成品同时满足全部约束**（给 AI 用 + 250MB 峰值 + 只要 9:16/16:9 + 中文口播 + Windows 无 GPU）。FableCut 轻且 AI 友好但无中文精剪；OneTake/驯剪有精剪但不是"agent 改 JSON"架构且偏重；kinocut 是工具层不是剪辑器。
- **250MB 是硬筛选器**：OneTake 的 FastAPI+React+PyTorch、任何 Electron、带 YOLO 的跟踪管线都容易超。真正守得住的形态大概率是**无 GUI 的 Python 调度层 + subprocess ffmpeg + 可选本地浏览器低清预览**。
- **推荐路线（三步试跑，不自研完整剪辑器）**：
  1. 试 **AI驯剪初剪引擎**（先确认仓真实存在）——看"剪气口/剪重说/词级字幕"质量与内存占用；若工程文件可被程序消费，只加 `project.json` 适配层 + MCP 工具。
  2. 试 **FableCut MCP 接口层**——验证"agent 改 JSON → 热更 timeline → ffmpeg 导出"在 Windows 上跑通、峰值可控。
  3. 若 1+2 覆盖阶段 1 的 80% ⇒ **不自研剪辑器**，自研范围收窄到四块：**中文 ASR 对齐管线 / 口播精剪决策规则 / 双规格导出编排 / 轻量作业队列**。

## 六、本机视角补充（本条目自带判断，非外部回答）

1. **晨读产线已有句级切分、句轴、能量包络**——这是 AI 剪视频最难的一块（自动切点与字幕对齐）。无论走哪条路线，**先接这个资产，不要重造**。
2. 250MB 目标的现实口径：把"峰值"定义为**渲染进程内存**而非整机占用；Python 调度层 + ffmpeg 子进程是最优形态，任何常驻 Chromium/Node 服务都应拆成可选模块。
3. **先验证后写代码**：阶段 1 的四项（切分/拼接/字幕/双规格导出）用一条 ffmpeg 脚本链就能跑通，先证明链路与内存达标，再谈 GUI 与 MCP 层。

## 七、待核实清单（联网后逐条查，按此判定）

- [ ] `leejersey/OneTake` 是否存在？星数/许可证/最后提交/是否支持 Windows？
- [ ] `fxl1209739475-fxl/ai-xunjian` 是否存在？（**仓名形态可疑，优先查**）
- [ ] Rescript、CapShorts 的真实仓全名与许可证？
- [ ] FableCut 当前星数与最后提交，是否有 Windows 支持与中文 fork？
- [ ] FunASR vs Whisper 的中文错误率数据出处（是否为同一数据集、同一硬件）？
- [ ] 上述任一仓库若为 AGPL，是否仍考虑集成（Work 仓公开前的分发义务）？

**判定口径**：超过 6 个月未更新＝停更；许可证缺失＝不可集成；仓名查无此仓＝整条作废。
