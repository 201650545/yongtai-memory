---
name: workflow-ai-wendabao-open
description: 用 opencli 最快打开 AI 问答宝（GPT 镜像站）并进到聊天框的流程——新标签页、不覆盖已开标签
metadata:
  node_type: memory
  type: 流程
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
  modified: 2026-09-04
---

# AI 问答宝（GPT 镜像站）最快打开流程

> 目标：从零到「能进聊天框」最短；**必须开新标签页，禁止覆盖 / 取消已经打开的标签页**。流程只读不破坏，成功即记。

## 前置

- opencli 连日常 Chrome（profile `n8hh7hyn`）。先 `opencli doctor` 确认 Extension connected。
- 只列现有标签，绝不动已开的（不 bind 乱切、不 close、不覆盖 route）。

## 步骤（照抄，别重探 DOM）

1. **开新标签页**（不覆盖已开标签）：
   ```
   opencli browser n8hh7hyn tab new "https://ai.wendabao-f.net/?utm_source=hidden-ncn"
   ```
   返回新 target id；原标签保持不动。

2. **确认已到新对话页**：
   ```
   opencli browser n8hh7hyn eval "() => JSON.stringify({u: location.href.slice(0,55), textarea: !!document.querySelector('textarea'), ce: document.querySelectorAll('[contenteditable]').length, cards: document.querySelectorAll('.n-card').length})"
   ```
   预期：`#/chat/` 新对话页、`textarea:false`、`ce:0`、`cards:8`（8 张账号卡）。

3. **读 8 张账号卡，找「活跃」**（受限不点）：
   ```
   opencli browser n8hh7hyn eval "() => { const cards=[...document.querySelectorAll('.n-card')].map((c,i)=>({i, id:c.id||'', txt:(c.innerText||'').replace(/\s+/g,' ').trim().slice(0,60)})); return JSON.stringify(cards); }"
   ```
   预期卡片文本形如 `Plus GPT-5 ㉔ 活跃`；挑「活跃」且非受限的。

4. **点活跃账号卡进聊天模式**（`.n-card` 或给 `__gN` id 赋值后 click）。进聊天后 textarea 出现在**独立镜像窗**（window.open 弹出），opencli 挂在入口页上不一定只见得到——需按 `feedback_gpt_mirror_account_switch` 与送审手册（`D:\Work\AI平台\docs\运行手册\GPT镜像站送审流程.md`）继续。

## 铁律

- **新标签页**：一律 `tab new`，绝不覆盖 / 取消已开标签。
- **发问闸门**：切到聊天框后，先确认顶部模型 pill = **Extended**，禁 Auto 再发问（关联 [[feedback_gpt_mirror_subagent_flow]]）。
- **不复探**：选择器 / localStorage / 流程照抄手册，别花 2–3 分钟重编。

## 固化一键脚本法（2026-09-04 实测，零→Extended ≤15s，最优选）

> 比逐段手点快 5–6 倍（74s→9.6s）。脚本在 `D:\Work\AI平台\docs\运行手册\scripts\`。两个脚本直接照抄，复探只会在跨实例时踩 hydration 坑。

```bash
opencli browser n8hh7hyn tab new "https://ai.wendabao-f.net/?utm_source=hidden-ncn"
sleep 2
opencli browser n8hh7hyn eval "$(cat 'D:/Work/AI平台/docs/运行手册/scripts/evalA_jump.js')"   # A：卡0 GPT-5→劫持window.open→跳 vip-XX
opencli browser n8hh7hyn eval "$(cat 'D:/Work/AI平台/docs/运行手册/scripts/evalB_ext.js')"    # B：全自动切 Extended 并验证
```

- **evalA_jump.js**：`window.open` 劫持存 `__openUrl`→点 `.n-card[0]` 第一个 GPT-5 span→`location.href=__openUrl` 秒跳。
- **evalB_ext.js**：单 async eval，内部 await 轮询（无固定 sleep）：等 host→**等 pill hydration**（占位 `Model`→`Auto`/`Extended`，占了 Model 就点必扑空，最大坑）→完整指针+原生 click 开菜单→`[role=menuitemradio]` 选 `Thinking• Extended`→等 pill=Extended 返回 `{ok:true}`。
- **新/旧对话同吃**：两者 composer 都是 `button.__composer-pill`，进旧对话(/c/…，contenteditable)后照跑 evalB 即可。
- **每次发送前**共用 evalB 复核（刷新/换对话回 Auto 就连跑 B）。

## 关联

- [[feedback_gpt_mirror_subagent_flow]] — 子 Agent 送审三条纪律 + Extended 切换法
- [[feedback_gpt_mirror_account_switch]] — 账号受限切活跃
- [[feedback_fork_forbidden]] — 本流程全员（含子 Agent）一律 fresh 上下文，禁止 fork
- 手册：`D:\Work\AI平台\docs\运行手册\GPT镜像站送审流程.md`（§三·五 固化一键脚本法）
- GitHub 同步：Obsidian 为主（`D:\记忆` 真源）→ `yongtai-memory` 镜像（脱敏后）