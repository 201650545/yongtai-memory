---
name: reference_本地RAG与Agent记忆_2026前沿与本地方案短板
description: 2026-10-21 一手调研结论——Agent 记忆从"存"转向"管"（写入粒度/召回时机/遗忘与取代）；本机 local-knowledge-engine 这套 RAG 的评级与三处真短板（关系语义没在检索时执行、写后不可见、评测只有 40 条）；附 2026 前沿论文清单与明确不做的项
metadata:
  node_type: memory
  type: reference
  created: 2026-10-21
type: reference
updated: 2026-10-21
kind: reference
status: active
---

# 本地 RAG 与 Agent 记忆：2026 前沿 ＋ 本地方案的三个真短板

> 方案全文：`D:\Work\元智能\10_AI自成长引擎\docs\调研\20261021_本地知识库与Agent记忆_2026前沿综述与本地方案评审.md`
> 外部两路评审原文：`20261021_rag_review_gpt_out\round1.md`（结论段）、`20261021_rag_review_gpt2_out\round1.md`（追问全文）、`20261021_DeepSeek答_本地RAG方案评审.md`（全文）

## 一、本质（2026 的共识）

**"记忆"从"存"变成了"管"**——存的问题 2024 年就解决（向量库/摘要/向量检索）；真正拉开差距的是**生命周期**：什么时候写、什么粒度、何时召回、何时**忘**、旧事实被取代后**检索时怎么办**。

- **post-graph-rag**（arXiv 2608.24921，2026-08，一手核到）原话：*"a graph that only accumulates treats superseded and current facts alike"*。
  它的消融：**把每条关系的有效期带进合成阶段**，时间推理 **0.496 → 0.881**。
- **REM**（2610.27377）：记忆管三决策（存什么/何时召回/何时遗忘）；**"同一经验以摘要或轨迹注入，即使 oracle 检索也不如它"**。
  数字：match@1 68.7% vs 55.6%、解决率 27.6% vs 24.9%、成本低 17%。
- **RSPM / Let Them Sleep**（2610.25561）：定期"睡觉"＝聚类失败 → 蒸馏短规则 → **删原始 episode**；
  两个独立研究收敛到**重试循环少 ~93%、存储条目少 ~30%**，分数 +7.6~+11.9。
- **MemDerive**（2610.25373）：**派生状态上所有记忆系统都落后于朴素 BM25**；主因＝**没沿推导链把输入收集齐**；给足支撑事件时同一模型达 **96.01%**。
- **QEMem**（2610.22668）：**相关性 ≠ 充分性**；LoCoMo 91.43%。
- **TIDER**（2610.23598，NeurIPS 2026）：**时间感知双通道**；LifeBench +8.82%。
- **MaC / Memory as Code**（2610.27700）：记忆＝**可执行结构**；**declarative retrieval**＝把查询编译成检索程序；相对提升最高 15.91% 且省 token。
- **FEB-30**（2610.22209，amazon-science）：记忆系统正确分类记忆操作（create/update/reinforce/supersede）**只有 20% 的时间**。

## 二、他那套 RAG 的评级（两路独立评审共识）

检索质量 **B+**（40 条 Recall@5=1.000，但只读前 3 条，未测过期记忆/缺失证据/跨文件依赖/写后滞后）｜延迟 **A**（记忆库 44 ms）**B+**（Work 库 243 ms）｜可维护性 **A**｜成本 **A+**（全本地零额度）｜可扩展 **B+**（瓶颈在重建端）｜抗退化 **B−**。

**三处真短板（三方共识）**
1. **`status`/`superseded_by`/`requires`/`updated` 存在 frontmatter 里，检索时完全没用**——新旧事实同权召回。
2. **写后不可见**：刚写完的记忆，同一会话内检索不到（等 02:00 重建）。
3. **评测太薄**：证明不了"过期事实会不会被误召回""该弃答时会不会硬答"。

**另两条（GPT 提出、两路没说的）**
4. ★**"证据不足"必须是检索的合法输出**：RRF 返回 3 条 ≠ 3 条够用。检索要能表达三态——**充分／相关但不充分（说清还缺什么）／无**。
   现有 `unknown` 只作用在**条目层**，**检索层没有这个出口**（QEMem：相关性≠充分性；DeclineCraft：弃答率）。
5. ★**索引可见性要分三态**：**FTS 已更新／向量尚未更新／整条完全可检索**——把"写后可见"从玄学变成可测指标。

## 三、一周三件事（零依赖、零额度）

1. **关系/状态语义接到检索上**：SQL 默认排除 `superseded`（除非查历史）；**证据卡片带生效时间/被谁取代**（0.496→0.881 那一档）；`requires` 做**一跳**扩展（不展开多跳）；`updated` 做同分时序偏置；**"证据不足"成为合法输出**；形态是**轻量关系表**（依赖/取代/作用域三种），不是知识图谱。
2. **评测扩成对抗集**（**七类**：旧版本压过新版／无答案／跨文件依赖／时间约束／范围隔离／索引延迟／重排误判），**用库里已有条目反向出题，零模型额度**。
3. **一致性**：**保留 02:00 全库校验**（抗退化兜底）＋**另加写后增量**（git diff/mtime → 只重切变更文件，删除走 tombstone）＋ 会话级增量表让新条目当场可查 ＋ **可见性三态可观测**。

## 四、明确不做（省得白花时间）

❌ 不上图数据库（但**要做轻量关系表**）｜❌ 不上 ANN（38,090 块暴力扫描够快，ANN 的一致性风险不值）｜
❌ 不做多轮迭代检索（**DeclineCraft 2610.28340：迭代 RAG 会降低弃答率**，与"不知道就说不知道"相冲）｜
❌ 不全局加重排（先证明"顺序错"是主要损失）｜❌ 不换大模型／不引外部向量 API（会破坏"全本地零额度"的 A+）｜
❌ 不砍 02:00 全库校验（增量是**加**上去的，不是替掉它的）。

## 五、溯源状态（别当一手用）

- **一手核到（arXiv 官方摘要/页面）**：post-graph-rag、REM、RSPM、MemDerive、QEMem、MemCompile、TIDER、RAG-NIMBF、DeclineCraft、Biomedical RAG、FEB-30、HABIT-Bench、MemBubble、MFM、BEAM、PACE-Mem、Whose Credential、GLOBE、PrairieFire、MemLLM、FuseRAG、Cost of Context、Gen-vs-Dense、MEMORA、RAGit。
- **一手核到（GitHub/产品）**：`zilliztech/memsearch`（README 确认**默认已用 ONNX bge-m3**）、`satwiksps/steadlith`、`OmarElbachyr/ragit`、多个 `blackboard-mcp`。
- **转述未核到**：QARF（**arXiv 查无此篇**，疑为会议论文）、Zep DMR 94.8% vs MemGPT 93.4%、Bekko 384 维超 e5 全系、memsearch 的具体 R@5 0.653/0.783。
- ⚠️ 2026 这批多为**预印本未同行评审**；post-graph-rag 的 0.496→0.881 是**自家消融**。
