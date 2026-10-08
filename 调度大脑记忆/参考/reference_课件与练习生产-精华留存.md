---
name: reference-课件与练习生产-精华留存
description: 2026-10-08 从已删除的 PUBLIC 仓 english-teaching-production 里按"只留两点"抽出的最小可用集（HTML 课件 ＋ DOCX 练习卷）：落点 D:\Work\课件与练习生产\，35 文件/1.83MB，含 2 份精简规范、12 个引擎与验证器（语法自检通过）、3 模板、2 份 exam_spec、3 档样例；原 1370 文件与学生个人信息随仓删除
metadata:
  node_type: memory
  type: 参考
  created: 2026-10-08
  Howtoapply: 他问"哪些 GitHub 仓可以整合优化"时的处置范式＝先查隐私、再问保留价值、抽精华后删仓
---

# 课件与练习生产（精华留存）

## 缘起

GitHub 13 仓盘点，`english-teaching-production`（10.2MB / 1370 文件 / 50 天未推送）被判为待整合。查出的**不是"闲置"问题，是隐私问题**：PUBLIC 仓顶层用 7 名学生真实姓名建目录，含 `学生档案.md`、`给家长的教学方案`、课件成品 HTML —— 而它自己的 `00_格式规范/00_全局约束与红线.md` R1 第一条就写着"绝对禁止出现个人姓名"，**规则在自己仓顶层被自己违反**；同时撞 handbook `40-安全红线` 第 3 条。

## 他的裁定（原话）

> "这个项目我想起来了。我觉得有用的就两点：1. 用 HTML 做课件。2. 如何生成规范的、我需要的练习文档。就这两点，其他没必要保留。"

## 处置

1. 抽精华 → `D:\Work\课件与练习生产\`（35 文件 / 1.83MB）：
   - `01_HTML课件规范.md`：单文件 HTML 全套硬约束（体积 ≥150KB、页数 40–45、page-id 契约、八环节预算、IndexedDB 采集、题目判定、风格包三轴正交、阅读 3+2 题型配额、**20 条硬门禁**、红线 R1–R7b）
   - `02_配套练习文档规范.md`：四部分 100 分/56 题结构、格式参数表、英文段落首行缩进 **1 字符**、制表位 1.5/6.5/11.5cm、简答 40 下划线/作文 60 下划线、选项随机化 `seed=课时号` 且相邻题答案字母不得相同、三档差异化表、八步生产流程
   - `引擎\`：`courseware_engine.py`(130KB)、`courseware_core.py`、`components.py`、`theme_colors.py`、`outline_renderer.py`、`docx_engine.py`、`build_practice_paper.py`（含 `randomize_all()`）、统一入口 `build_practice.py`、`verify_v2.py`、`verify_interaction_v1.py`、`verify_visual_v1.py`、`gen_l1_l13_v2.py` —— **`py_compile` 全部通过**
   - `模板\`：课件制作大纲/配套练习生成大纲/课程设计卡 ＋ `exam_spec_v2026_1.json`/`_2.json`
   - `样例\`：基础 210KB / 中等 119KB / 培优 322KB 三档 HTML
2. 删 GitHub 仓（`gh repo delete` 已执行、复查不存在）。
3. `projects.yaml` 两处更新：feishu-data-hub 与 english-teaching-production 改写为"已删除"沿革；`local_only` 新登记「课件与练习生产」。

## 顺带修掉的坑

- 原仓内部**规范自相矛盾**（页数 40–45 vs schema 25–30、体积 ≥150KB vs ≥100KB、交互点 ≥6 vs 3–6），提炼时按"更严/更新"裁决并写入规范第 15 节。
- 模板里的真实姓名示例（`许颖嘉/第05课时/…`）已替换为代号，符合其自身 R1。

## 三条可复用的判断

1. **公开仓先查隐私，再谈闲置**。学生姓名、家长方案、成绩数据这类东西在 PUBLIC 仓上，"要不要整合"是伪问题——先止血。
2. **"项目有用什么"要让他自己说，别替他判**。我第一反应是"归档还是删"，他直接给出保留价值（两点），避免了把 1370 文件整体搬进 Work。
3. **删仓前必须先把要留的抽出来并验证**（本轮用 `py_compile` 逐个自检 + 7/7 关键文件校验），再执行不可逆操作。

相关：[[调度大脑记忆/参考/reference_handbook_v11_收口]]、[[调度大脑记忆/参考/reference_two_memory_repos_split]]