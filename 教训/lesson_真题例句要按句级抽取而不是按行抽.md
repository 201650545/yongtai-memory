---
name: lesson_真题例句要按句级抽取而不是按行抽
description: 从真题 segments.json 抽「可做教材例句」的句子，按行抽会得到大量选项行/通知清单/邮件碎片（实测 120 条里 62 条不合格）；必须先按句切再过硬门。
type: lesson
updated: 2026-10-21
kind: rule
status: active
---

# 真题例句：按行抽会出垃圾，要按句抽（2026-10-21 实测）

## 现象

湖南中考 688 词册的「层5 真题例句」第一版用**行级**过滤（长度 45—170、无中文、非选项行），
从 `03_data\题型切分\segments.json` 抽出 120 条当例句。人工过一遍：

**62/120 条不合格**，涉及 51/82 个词 —— 典型垃圾：

- 选项行：`C. Basketball is a great way to improve physical health.`
- 通知清单（多句拼贴）：`⑤However, none of these benefits come for free. Training AI also uses a lot of energy...`
- 邮件落款：`Help at the old people's home. Dance or sing well. Free in September. E-mail Anna at hnzk@gfimail.com.`

这些一旦印进教辅，学生看到的是「题册碎片」而不是例句。

## 正解：先按句切，再过硬门

改法（`_assemble_core82.py` v4）：

1. **按句切**：先去掉行首的选项标记（`A.`/`B.`/`C.`、带圈序号、题号、项目符号），
   再用 `re.split(r'(?<=[.!?])\s+', line)` 拆成句子；
2. **逐句过硬门**：句内**不许有中文**（硬门，不是比例）、不许有 `[计][美][英][方]` 类标注、
   不许有 `@`/网址/填空 `___`/勾叉、必须大写开头、必须有句末标点、
   词数 6—26、句长 30—160；
3. **还要有谓语**：`has_finite_verb()`（助动词/情态动词表，或词表里的 -ed/-s 形）
   ⇒ 把「不定式短语」类残句（`The chance to connect with good people a lot.`）挡掉；
4. **词表兜底**：句中所有**小写**词都要认得（母表 ∪ 课标 3185 ∪ 高中 6008，
   含复数/变形），专有名词大写放行；
5. **顺手修 PDF 掉空格**：`abreak → a break`、`settinggoals → setting goals`
   （按词表做两段切分复原）。

实测：候选 995 句 → 覆盖 **81/82** 词、**0 条缺陷**。

## 附带教训

- `"词".isalpha()` 是 True、`"词典".islower()` 也是 True ⇒ 任何「首词是小写英文」的过滤
  都会把中文行匹配上，必须用 `re.fullmatch(r"[a-z][a-z'-']*", tok)`。
- 母表里存的是 HTML 实体（`can&#x27;t help doing`），**渲染前要先 unescape 再 escape**，
  否则卡片上会原样印出 `can&#124;t help doing`。

## 相关

- 实现：`D:\Work\English-Content-Factory\02_Projects\HN-ENGLISH-666\06_templates\_assemble_core82.py`
- 体检脚本：`..\06_templates\_analyze_examples.py`（缺陷统计 + 抽样）
