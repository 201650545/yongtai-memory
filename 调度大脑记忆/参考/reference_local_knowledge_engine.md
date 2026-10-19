---
name: 本地知识检索引擎（local-knowledge-engine）
description: 想知道「某个东西在哪、之前怎么定的、有没有相关文档」时，先用它检索证据，不要全本读笔记、不要全盘漫游。省上下文 token、省代理流量，毫秒级返回 3 条带行号的证据。
type: reference
updated: 2026-10-19
---

# 本地知识检索引擎 —— 找资料先查它，别全本读笔记

## 一句话

**在 `D:\记忆` 和 `D:\Work` 里找东西时，先跑它，再决定读哪篇。**
它不搬内容，只告诉你「东西在哪一行的哪一段」，返回 3 条 200–350 字的证据卡片。
（2026-10-17 郭老师定；2026-10-19 统一入口）

## 它解决什么问题

原来的痛点不是"搜得慢"，是**不知道东西在哪**：

- 只能靠 `glob` + `grep` 一层层试，或者把整本笔记塞进上下文；
- 客户端每轮把历史全量上行重传，**代理流量每天被吃掉几 G**；
- 塞进去的几百行里，真正有用的往往只有一句。

现在的效果：全库 223 万 token → **243 ms 返回 3 条、约 700 token 的证据**。

## 怎么用（三条命令）

引擎目录 `D:\Work\元智能\10_AI自成长引擎\技能库\local-knowledge-engine\scripts\`：

```powershell
# 1) 查证据（最常用）
python query_evidence.py "关键词" --vault "D:\记忆"
python query_evidence.py "关键词" --vault "D:\记忆" --work "D:\Work"   # 跨库联合查
python query_evidence.py "关键词" --format json                        # 机器可读
python query_evidence.py "关键词" --no-semantic                        # 缺 numpy 时

# 2) 查某篇文档某章节的真实行号（禁止硬编码行号）
python locate_anchor.py "文件路径" "章节名"

# 3) 索引与向量每天 02:00 自动更新（计划任务 EmbedBackfill），一般不用手动跑
#    改完笔记想立刻生效时才手动跑；**--embed 才会补向量，不加只建索引**
python indexer.py --vault "D:\记忆" --embed
python indexer.py --vault "D:\Work" --embed
```

## 别人可能怎么问它（别名与口语）

**它是同一个东西**，下面这些说法都指向本条目 —— 检索时命中任意一条都算找对了：

- 工具名：`local-knowledge-engine` / `query_evidence.py` / `locate_anchor.py` / `indexer.py`
- 中文叫法：本地检索引擎、本地检索工具、知识检索引擎、知识检索工具、证据检索、断流检索、本地知识库检索
- 技术术语：RAG（检索增强生成）、Agentic RAG、混合检索、语义检索、向量检索、FTS5、召回
- 要解决的事：找资料、找文档、查笔记、搜笔记、某个东西在哪、之前怎么定的、省 token、省上下文、省代理流量
- 反义提醒：它**不是**联网搜索（联网那个是 `ai-search-pool`）

## 什么时候必须用它

- 「某个概念 / 规范 / 决策**在哪**」「**之前是怎么定的**」「有没有相关文档」
- 要读某篇文档，但**不确定该读哪篇**
- 任何"应该翻一下笔记"的时刻

## 什么时候不用它

- **已经知道确切路径** → 直接读，别绕
- **要通读全文**（写总结、做审查）→ 那就读全文
- **刚改完的笔记还没到 02:00** → 先跑 `indexer.py --embed`，否则它看不见新内容（向量同理）

## 什么形态存在（四个零件）

| 零件 | 位置 | 说明 |
|---|---|---|
| 代码 | `技能库\local-knowledge-engine\scripts\` | `indexer.py` / `query_evidence.py` / `locate_anchor.py` / `embedder.py` |
| 说明 | 同目录 `SKILL.md` | **正文在 SKILL.md，本文件只做指针** |
| 索引数据 | `<vault>\.cache\knowledge.db` + `knowledge.vectors.npy` | 已 gitignore，**永不进知识树、不进 Obsidian** |
| 入口指针 | `AGENTS.md` 三处 | 本文件是第 4 处，专管"它是什么" |

## 关键事实（引用前必读）

- **检索方式**：FTS5 中文词级（jieba）＋ trigram ＋ 本地语义向量（`multilingual-e5-small` ONNX，384 维），
  用 RRF（k=60）融合，再叠可解释加权（文件名 ×1.60 / 目录 ×1.45 / 标题 ×1.25 / .md ×1.30）。
- **别名扩展**（2026-10-19）：查询前读引擎根的 `aliases.json`，命中口语触发词就拼上规范用词
  （「机器换人/接手」→「冷启动 接手序 交接手册」），再对「文件名/标题命中扩展词」的条目 ×2.2 重排。
  起因：口语「机器换人接手项目先看哪份」原本搜不到 `workflow_work库冷启动接手序`；加表后它排第 1。
  `--no-expand` 可关闭。
- **一句话入口**：`D:\记忆\q.cmd "关键词"` 是一行封装；用户说「读 Obsidian 的仓库」时按 `D:\记忆\README.md` 走。
- **它只做 RAG 的前半段**：只检索，不做"总结生成"。后半段交给 Agent 自己读原文 —— 在 Agent 场景里这更可靠。
- **实测性能**（40 条评测集）：记忆库 p50 44 ms、Work 库 p50 243 ms；混合检索 Recall@5 = **1.000**（两个库）。
- **索引规模**（2026-10-19 23:15 实测）：记忆库 192 文件 / 2,962 块；Work 库 1,043 文件 / 38,090 块；两库向量覆盖率均 100%。
- **被排除的目录**：`runtime` `models` `node_modules` `.cache` `_staging` `b_answers` 等机器产物；
  **`logs` `99_Archive` `会话记录导出` 仍然索引**（那些是有价值的叙述性内容）。
- **索引与向量每天 02:00 自动更新**（计划任务 `EmbedBackfill`，2026-10-19 上线）：
  跑 `10_AI自成长引擎\scripts\embed_backfill.py`，对两个 vault 做「增量重建索引 + 只补缺向量的块」，
  覆盖率 <95% 写 `D:\项目\ai-hub\search_gateway\data\渠道警报.log`。
  为什么必须有这一步：`indexer.py` 原先的 `__main__` **不传 embedder**，光跑它向量永远补不上，
  新笔记在语义通道里是瞎的（曾出现索引 18:27 重建、向量停在 01:32）。现在 `indexer.py` 已加 `--embed` 开关。
  手动立刻生效：`python indexer.py --vault "D:\记忆" --embed`（**不加 `--embed` 不编码向量**）。

- **调用埋点**：每次检索追加一行 `10_AI自成长引擎\logs\knowledge-query.jsonl`
  （时间 / 查询词 / 库 / mode / 命中数 / 检索耗时 / 模型启动耗时 / 前 5 路径 / cwd / argv），写日志失败静默。
  要看真实使用率就数这个文件按 `cwd` 分组，**别再解压几百个会话文件倒推**（2026-10-19 教训）。

## 它不是什么

- 不是搜索引擎：不联网，只查本地两个 vault。
- 不是知识图谱：不做实体关系推理。
- 不是自动记忆：它不会自己更新，也不会跨会话记住你问过什么。

## 关联

- 完整用法与排序规则：`D:\Work\元智能\10_AI自成长引擎\技能库\local-knowledge-engine\SKILL.md`
- 全局强制条款：`C:\Users\郭永涛\AGENTS.md` §7（严禁全本漫游）
- 首次广播：[[全局变更广播]]
- 姊妹工具：[[调度大脑记忆/参考/reference_skill_ai_search_pool]]（那个是**联网**搜索，这个是**本地**检索）
