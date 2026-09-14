---
name: reference-presentation-system-spec
description: Presentation System 演示文稿生产系统设计规范——内容与输出格式分离，先结构化 Spec 再渲染成 HTML/PPTX/PDF/图片
metadata:
  node_type: memory
  type: reference
  modified: 2026-09-15T00:05:00.000Z
---

# Presentation System｜演示文稿生产系统设计规范 v1.0

> 由郭老师提供（2026-09-15）。**适用面：任何演示文稿类任务（课件、汇报、路演、报告）。**
> 一句话定义：**一套将结构化内容，通过统一的页面原型和视觉设计系统，快速渲染成 HTML、PPTX、PDF 和图片的演示文稿生产体系。**

---

## 1. 核心思想

传统方式：内容 → 直接进 PPT → 一页页手工设计 → 反复改。
本系统：内容 → **结构化 Presentation Spec** → Presentation System → HTML / PPTX / PDF / Images。

**核心原则：内容与最终输出格式分离。HTML、PPT、PDF 都只是不同的 Renderer。**

## 2. 四层架构

```
Layer 1 Content System   内容系统（讲什么）
Layer 2 Slide System     页面结构系统（怎么排）
Layer 3 Design System    视觉设计系统（长什么样）
Layer 4 Renderer         输出渲染系统（出成什么格式）
```

## 3-4. Layer 1 · Content System / Presentation Outline

此阶段**不考虑** PPT、HTML、字体、颜色、动画；只考虑核心观点、内容逻辑、叙事顺序、页面目的、信息层级。
每个项目必须先建立完整大纲（例：01 封面 / 02 背景 / 03 问题 / 04 为什么重要 / 05 核心观点 / 06 理论 / 07 方案 / 08 过程 / 09 案例 / 10 数据 / 11 价值 / 12 展望 / 13 结束）。

## 5. 每一页必须回答一个问题

- **One Slide, One Message.** 禁止一页同时表达 5 个核心观点。
- 标题必须是**观点**，不是名词。
  - ✗ "项目介绍"
  - ✓ "传统教学方式难以让理论真正进入学生的真实生活。"

## 6. Slide Content Model

```json
{
  "slide": 6,
  "type": "comparison",
  "title": "传统课堂与沉浸式课堂的差异",
  "message": "沉浸式体验能够明显增强学生的参与感。",
  "content": {},
  "visual_intent": "contrast"
}
```
字段：slide（编号）/ type（页面类型）/ title（标题）/ message（唯一核心观点）/ content（内容）/ visual_intent（视觉目的）。

## 7. Presentation Spec

所有页面内容统一存入 `presentation.json` 或 `presentation.yaml`。

```json
{
  "project": { "title": "项目名称", "theme": "modern-red", "aspect_ratio": "16:9" },
  "slides": [
    { "slide": 1, "type": "cover", "title": "项目标题", "subtitle": "副标题" },
    { "slide": 2, "type": "big_statement",
      "title": "真正的问题并不是学生没有学习，而是理论与现实之间存在距离。",
      "message": "建立问题意识" }
  ]
}
```

## 8-9. Layer 2 · Slide System 与标准页面原型库

不要每做一页都重新设计；提前建立 **Slide Archetype Library（页面原型库）**。建议至少 15 种：

1. **Cover** — 封面：主标题 / 副标题 / 项目团队信息 / Hero Visual
2. **Big Statement** — 一句核心观点：大字号核心句 / 少量辅助说明 / 视觉留白（适合转场、核心判断、价值主张）
3. **Context / Background** — 背景：标题 / 背景说明 / 1 个主要视觉 / 2~3 个关键信息
4. **Problem** — 问题：问题标题 / 现状 / 矛盾点 / 问题结果
5. **Three Cards** — 三张并列卡（三大问题、三个能力、三个原则、三个成果）
6. **Comparison** — 前后/左右对比，**必须一眼看懂**
7. **Process** — 过程：Step1→2→3→4 或 01→02→03→04
8. **Timeline** — 时间线（发展、历史、实施计划、Roadmap）
9. **Architecture** — 体系/框架/结构（核心目标 → 模块 A/B/C）
10. **Data / KPI** — 核心数字，一页只放少量真正重要的数据
11. **Chart** — 图表**用来表达结论**，不是展示所有数据；标题应直接写结论（✗"学生反馈数据" ✓"改革后学生主动参与率提升了 37%。"）
12. **Case Study** — 案例：背景 / 问题 / 措施 / 结果
13. **Quote** — 引用一句话 + 人物/来源
14. **Image Story** — 大面积照片 + 少量文字 + 一句核心观点
15. **Closing** — 结束：最终观点 / 感谢 / 团队信息

## 10. 页面原型的意义

30 页 ≠ 设计 30 个页面；而是**建 10~15 个原型，30 页内容分别调用这些原型**。这样才能快速生成、保持统一、快速修改、多项目复用。

## 11-22. Layer 3 · Design System

规定：Color / Typography / Spacing / Grid / Card / Border / Image / Icon / Chart / Animation。

- **Color**：禁止逐页随意选色，必须建立统一变量（Background Primary/Secondary、Text Primary/Secondary、Accent Primary/Secondary）；不同项目通过 Theme 更换。
- **Typography**：必须规定 Display / H1 / H2 / Body / Caption / Number 六级。HTML 例：`--font-display:72px; --font-h1:48px; --font-h2:30px; --font-body:22px; --font-caption:16px;`。**PPT 必须尽量遵循相同比例。**
- **Spacing**：统一 8 / 16 / 24 / 32 / 48 / 64 / 96，避免 17px、23px、31px 这种随手值。
- **Grid**：默认 16:9，推荐 12 栏栅格，左右上下安全区统一（如四边各 6%）。
- **Card**：圆角/边框/阴影/Padding 统一，不要每页不同卡片风格。
- **Icon**：一套演示只用**一种** Icon 风格（Outline / Filled / Minimal line / 3D），禁止混用线性、卡通、拟物。
- **Image**：图片风格必须统一（摄影/插画/3D/AI、色调、光线、人物风格、背景、构图、镜头感）。用 AI 生图必须**先建立统一的 Image Style Prompt**，所有图在这个风格上变化。
- **AI 生图职责**：**不承担**正文、长标题、精确数字、表格、数据图、页码；**主要承担** Hero Visual、Concept Art、场景、人物、背景、3D Visual、抽象概念图。**原则：AI 负责视觉，HTML/PPT 负责信息。**
- **Chart**：简单、直接、有结论、少装饰、强调关键数据；禁止无意义 3D 图表、过多颜色、默认 Excel 风格、一页十几组数据。
- **Animation**：可用 CSS / GSAP / SVG / Canvas / Three.js，但**动画用于表达信息，不是炫技**。推荐 Fade / Slide / Scale / Number Count / Chart Draw / Progress Reveal。

## 22-23. Theme System 与思政比赛建议 Theme

建立可切换 Theme Pack：`themes/` 下 minimal-white / dark-tech / **modern-red** / consulting / editorial / luxury / education / corporate —— 每个 Theme 定义 colors / fonts / spacing / cards / charts / images / animations。

**思政比赛建议单独建立 `modern-red`**：不是传统"大红色 PPT"，而是**现代、克制、庄重、有文化感**；建议深红 / 暗红 / 米白 / 深灰 / 少量金色。
视觉上避免：满屏红色、过多党政模板式装饰、过多金色立体字、复杂边框。
重点应是：**内容可信、结构清晰、视觉庄重。**

## 24-27. Layer 4 · Renderer System

- **HTML Renderer（主要生产方式）**：Presentation JSON + Theme + Slide Components → HTML。优势：AI 易编辑、CSS 统一、改得快、支持动画、支持数据、可截图、可浏览器展示。
- **PPT Renderer（正式可编辑交付格式）**：必须生成**真正文本框 / 真正 Shape / 真正图片 / 真正图表**，**不是整页截图塞进 PowerPoint**。
- **Image Renderer**：用于最终不可编辑展示、PDF、社交平台、图片报告、快速预览；可由 HTML 自动截图。

## 28. 三条生产线

```
Presentation Spec
   ├── HTML  → 主生产线
   ├── PPTX  → 客户交付线
   └── Images→ 视觉输出线
```

## 29. 推荐工作流程（12 步）

1. 理解项目（Audience / Purpose / Context / Duration / Output / Style）
2. 建立 Storyline（先写**一句核心观点**，再设计叙事）
3. 建立 Outline（列出所有页面）
4. 定义每页 Message（每页只有一个核心信息）
5. 选择 Slide Archetype
6. 确定 Theme
7. 制作视觉参考（AI 只生成 Cover / Content / Data / Quote / Case Study 等**少量代表页**，**不要直接生成全部 30 页**）
8. 确认 Design System（颜色/字体/间距/图片/图表/动画）
9. **HTML 优先实现**（Agent 读 Spec → 选 Slide Component → 应用 Theme → 生成 HTML）
10. 截图 QA（逐页查 Overflow / Alignment / Contrast / Font Size / Whitespace / Visual Hierarchy / Consistency）
11. 迭代修改（**优先改 Design Token，而不是逐页修补**）
12. 输出其他格式（HTML / PPTX / PDF / PNG）

## 30. Agent 工作原则（六条，强制）

1. **不要一收到材料就直接开始设计页面**。先：理解内容 → 建立故事线 → 建立大纲。
2. **不要一页一页随机设计**，必须使用 Slide Archetype。
3. **不要每页重新定义颜色、字体、间距**，必须遵循 Design System。
4. 全局性问题**优先改 Theme / Token / Component**，不要逐页修改。
5. AI 生图只负责适合图片表达的内容，文字和数据由 Renderer 负责。
6. 任何页面必须回答：**"观众看完这一页，只记住什么？"** 不能回答就必须重构。

## 31-32. 页面质量检查与整套 QA

- **Content**：是否只有一个核心观点？标题是否表达观点？是否文字过多？**是否可删 30%？**
- **Layout**：层级是否明显？视线知道先看哪里？有无多余元素？留白够不够？
- **Visual**：图片是否真正支持观点？风格是否一致？颜色是否统一？
- **Data**：数据是否准确？是否突出结论？能否更简单？
- **整套 QA**：第一页到最后一页是否像同一个作品？Storyline 是否连贯？有无重复页？有无突然变化的视觉风格？字号/颜色/图片/图表/动画是否统一？

## 33-34. 推荐目录结构 与 项目/系统分离

```
Projects/            （具体项目：思政比赛、ListenLoop、课程设计）
  └── 00-Project-Overview.md / 01-Source-Materials/ / 02-Research/
      03-Storyline/ / 04-Presentation/(presentation.md/.json/slide-notes.md)
      05-Assets/(images,charts,icons) / 06-Output/(html,ppt,pdf,images)

Systems/             （长期复用方法论：Presentation System / Research System /
                      Writing System / Image Generation System）
  └── Presentation-System/（Design-Spec / Slide-Archetypes / Themes / Agent-Prompt）
```

**非常重要**：Systems 存方法论，Projects 存具体项目。Agent 应"读 System + 读 Project → 执行任务"，而不是每个项目都重新教一次。

## 35. 推荐 Agent 执行入口（可直接复制的指令模板）

> 请先读取 `Systems/Presentation-System/Presentation-System-Design-Spec.md`，然后读取当前项目 `Projects/思政比赛/`，严格按照 Presentation System 规范执行。
> **第一阶段只输出**：1. Presentation Storyline　2. 页面大纲　3. 每页 Key Message　4. 每页 Slide Archetype。
> **不要立即制作 HTML 或 PPT**，等结构确认后再进入视觉设计。

## 36-38. 核心原则总结

Presentation System 的核心不是"做漂亮 PPT"，而是**把演示文稿变成结构化、模块化、可重复生成的内容产品**：

```
Content + Slide System + Design System + Theme = Presentation
```
Renderer 决定 HTML / PPTX / PDF / Images，**而不是决定内容本身**。

以后不要问"这一页 PPT 怎么做？"，优先问：
**"这一页是什么类型？""它唯一想表达什么？""该调用哪个 Slide Archetype？""当前 Theme 要怎样表现它？"**
这四个问题定下来，HTML、PPT、PDF 都只是后面的生成问题。
