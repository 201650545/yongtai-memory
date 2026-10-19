# reference: 句读课程全流程工业化生产套件 Skill (listenloop-course-pipeline)

> 创建日期: 2026-10-16
> 真源路径: `D:\Work\元智能\10_AI自成长引擎\技能库\listenloop-course-pipeline\SKILL.md`
> 适用范围: 句读（ListenLoop）全生命周期自动化制课、课程包构建、组件化演进与全量验收

---

## 1. 架构定位
本 Skill 是句读课程开发的一键端到端总控套件（Skill Suite）。它确立了“**顶层总装流水线编排 + 内部 6 大独立原子组件解耦**”模式：
- 解决大杂烩 Skill 造成的上下文膨胀与规则混乱；
- 支持单组件独立演进与就地调试；
- 支持全流程一键流水线造包。

---

## 2. 6 大独立组件规划与数据契约

| 组件目录 | 职责与工具 | 输入源 | 核心产出物 | 验收断言 |
| :--- | :--- | :--- | :--- | :--- |
| `components/01_mindmap/` | 课程导图与目录层级 | 统编教材真源 | `lesson_tree.json` | `lessonId` 唯一全等 |
| `components/02_text_prepare/` | 官方原文与三表挂载 | 国家智慧教育平台教材 | `raw_text.txt` + `words.json` | 识字表/写字表/词语表数字严格吻合 |
| `components/03_segmentation/` | 双模态意群切分 | `raw_text.txt` | `segments.json` | 初读 4~8 留白禁假逗号；熟读 6~18 禁跨句 |
| `components/04_audio_slice/` | 名师原声音频切片 | B站白名单 UP 原声 | `clean_audio.wav` + `meta.json` | 纯净语音，1300ms gap 静音切片 |
| `components/05_asr_align/` | ASR 字级真实时间戳对齐 | 本地 Paraformer 引擎 | `timed_sentences.json` | 原生真戳禁均摊，单句时间戳完全闭合 |
| `components/06_animation_spec/`| 胶囊动效与跟读评测配置 | 前序产出物 | 标准 `.lllesson` 课包 | 满足播放器变色高亮与红绿双行判定 |

---

## 3. 自适应微调与双轨存档
- 遵循母仓总规：本地快照保留 **7 天**，夸克网盘归档保留 **30 天**；
- 单组件微调就地隔离，改前必须在 `.history/` 留存快照，避免局部调整污染全局。
