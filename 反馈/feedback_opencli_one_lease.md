---
name: feedback-opencli-one-lease
description: "opencli browser session 只持一条 tab 租约,tab new/eval 会改写该租约并覆盖会话焦点——绝不能拿它会话来开\"给郭老师看的\"页面,会盖掉他在看的 GPT/工作标签;要独立 window/context"
metadata: 
  node_type: memory
  type: feedback
  modified: 2026-09-04T16:07:36.609Z
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
type: feedback
updated: 2026-10-12
kind: fact
status: active
---

**`opencli browser <s>` 一个 session 同一时刻只持一条 tab 租约。`tab new <url>` / `eval` 都写在这条租约上**:它只能看到/操作自己创建或绑定的那一条,列表(tab list)永远只吐这一条,"新开"其实是在这条租约上改导航。所以拿它会话来给郭老师"开页面",等于把他正看在的那条GPT/工作 tab 盖掉。2026-09-04 我连开问卷+镜像就连盖两次被点名。

**Why:** 郭老师只在日常 Chrome 里工作,GPT 镜像(vip)等线程在同一 Chrome。opencli 看不到/不能保住他那些 opencli 之外的 tab;我在同一 session 里 tab new → 直接改写会话来话焦点,他眼前就被换了页。{{feedback_gpt_mirror_subagent_flow}} 多标签纪律的经验在 opencli 是另一套语义,别照搬。

**How to apply:**
- **凡是"给郭老师看/让他操作"的页面(原型/问卷/预览),绝不用他工作 session(连接码,曾 `n8hh7hyn`,**2026-09-27 起 `d5vtd5bg`**)的 tab new 开**——那必然盖掉他在看的 tab。要开就用**独立 window / 独立 browser context / 独立的 session**,开在不会跟他浏览焦点打架的地方,或直接给他一个 http URL 自己去新窗口打开(他极简,给 URL 即可)。
- opencli 会话里的操作只限"我自己的中间物"。
- 若已在会话里盖了,承认并说明根因,不要反复 tab new 想修——只会滚雪球。
- 修旧:把合法预览物放指到 http 地址(如 127.0.0.1:8899/...),URL 给郭老师,不霸占他的 tab。

---

**✅ 2026-09-28 实测复验(换码后,结论不变·重要)**:换连接码 `d5vtd5bg` 后重跑一遍,**单租约语义完全复现**——
- 新建 session 时 `tab list` 返 `[]`(此时**未**接管任何用户页面,是唯一真正安全的状态);
- 执行 `browser d5vtd5bg tab new` → 返回 pageId `2AFABCAFA45951273763EF6C0517943D`,`url:null`;
- 再 `tab list` 只吐**这一条**,且 `active:true` → 焦点已被改写,郭老师眼前页面被盖(与 2026-09-04 判断一致)。

**本次教训(AI 侧)**:郭老师交代"不要抢别人的标签页,要打开新的标签"时,我误以为 `bind` 才抢、`tab new` 是安全替代,**实际两者都会改写同一条租约**。真正的"不抢"只有两条路:**给 URL 让他自己开**,或**独立 window/context**。以后凡涉及"给他看"的页面,先按本条判,不要凭字面理解自创做法。

---

## ✅ 2026-10-09 郭老师复述（口径不变，但这是他当场说的最后一句，优先按这句执行）

> **原话**：「我还在用镜像站，且**打开镜像站不能占用别人已经打开的标签，要自己打开新的标签**。」

**解读（这次别再自创）**：
- 前半句＝**镜像站仍在用**，所以 `20_自适应工作流引擎\contracts\gpt-mirror-extended-review.yaml` 这份契约**不退休**，红灯要修而不是删。
- 后半句＝**本条铁律继续生效**，且它同样约束**元智能的 P2 浏览器探针**：探针若要开浏览器测 `composer` / `reasoning_mode` / `answer_channel` / `opencli_session`，**必须开在独立 tab/独立 context，绝不能改写他日常 Chrome 里已开着的任何一条**。
- 由此得到一条操作判据：**凡是"读一次就够"的验证（巡检探针、状态核对），优先用只读 HTTP，不开浏览器**；确实必须开浏览器的，**只在独立 session，且用完不动他任何 tab**。