---
name: feedback-mirror-send-speed
description: 镜像站「注入+发送」别再重探滚动扫选择器——composer 是 #prompt-textarea(ProseMirror)，发送=点 [data-testid=send-button]（有文本才渲染）；多标签必先 tab select 钉死再操作；合成 Enter 不提交。2026-09-04 又卡一次被郭老师点名
metadata:
  node_type: memory
  type: feedback
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
  modified: 2026-09-04T15:52:53.516Z
---

**镜像站「注入问句 + 发送」必须照固化路径一次到位，绝不再重探滚扫。** 2026-09-04 我为了找发送按钮连续 4–5 轮窄 probe 卡死，被郭老师当场点名「又卡死？我说了速度要快……下次不要犯这种傻逼错误」。

**固化路径（照做，别想）**：
1. **composer 是新对话页的 `#prompt-textarea`**（ProseMirror `[contenteditable]`），**不是**那个 0×0 隐藏 `textarea`。注错那个=白注看不见。注入：`ce.focus(); ce.click(); document.execCommand('insertText',false,txt);` 再补一个 `InputEvent('input')`。
2. **发送 = 点 `[data-testid=send-button]`**。它**只在 composer 有文本后才渲染**——没文本时 DOM 里根本没有，别在那之前找，找到即点（完整指针序列+原生 click）。**合成/protocol Enter 不提交**，别指望 keys Enter。
3. **多标签先钉死，但别自称"定死"**：`tab new` 后 opencli 的 eval 默认目标会漂。先 `NEWID=$(opencli browser <s> tab new <url> … | grep -oE '[A-F0-9]{32}')` 再 `opencli browser <s> tab select $NEWID` 钉为会话默认。**但 tab select 只是尽力而为**：标签重排/多窗口会让 target id 失效，`tab list` 只吐当前活动页，**读某个会话的答案绝不能只信固定句柄**。要按**侧栏标题精确定位线程**：枚举 `a[href*='/c/']` 标题→点对应线程→等→读最后一条 `[data-message-author-role=assistant]`，交付前核对 `location.href` 的 `/c/<id>`+标题。同账号能开多个 vip 实例（vip-24/vip-48…），相近标题分属不同线程，别读了旧线程谎报"读到了"。
4. **找选择器只给猜 1 次宽探**：一个选择器没命中，就一次 dump 全部 `[data-testid]`+底部按钮+testids，判完就点；绝不 3 轮以上窄 probe 循环。
5. Extended 深答 1–15 分钟：`streaming:false` + 有答案才判定完成，别中途重发。

6. **给执行 Agent 的 eval 脚本统一传 IIFE 自执行 `(()=>{...})()`，不加 `--tab`**：裸箭头字面量 `() => {...}` 在部分 opencli 版本（如 v1.8.0）不自动调用、反报 `Unexpected token ')'`。要定向标签就用 `tab select <id>` 钉死再 eval。2026-09-04 外部 harness 用 v1.8.0 + `--tab` 复刻文档翻车，我本机 v1.8.6 四形态全过 → 判为版本契约差异，已把文档/存档脚本全改 IIFE 防任何 harness。

**Why：** 发送是最常卡的一环；重探 DOM + 标签漂移 + 误注隐藏 textarea + 合成 Enter 不提交 = 四个慢点叠一起。郭老师明确要速度，卡一次扣一分信任。

**How to apply：** 进镜像发问 = tab new→select 钉死→evalA 跳→evalB 切 Extended(ok:true)→注入 #prompt-textarea→点 send-button→background 守望 streaming:false。关联 [[feedback-gpt-mirror-subagent-flow]] [[workflow-ai-wendabao-open]] [[feedback-browser-element-nav]]

**预览/看板/成品构建，先问 GPT 再动手**：郭老师明确要求"预览的构建去问 GPT（镜像 Extended，架构优先进口）"——凡是给"能拍板"的预览（Obsidian 预览页、HTML 原型、界面骨架）前，先问 GPT 形态选型与复用/新建，别自己擅建静态 md 复制了事。2026-09-04 我没问就复制了一份预览 md，被抓。「架构优先用最先进模型把关；生成专属执行 Agent 只写命令+复核」也照此。