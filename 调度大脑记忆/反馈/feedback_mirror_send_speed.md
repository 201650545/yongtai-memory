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

---

## ★★★ 郭老师 2026-09-15 新增三条强制规则 ★★★

### 规则一：镜像站的回复**一律用主会话监督**，禁止后台任务

**原话**：「每次你用来检测镜像站的后台任务都跟蠢猪一样，镜像站的回复你以后都用主会话去监督」

**实测教训**：后台任务（`run_in_background`）下载 10 张图，中途被 kill/超时 → 留下 **3 个截断文件**（第02、03、08 张大小恰为 150000/300000/390000 字节 = **30000 的整数倍，这是分块下载截断的判别特征**）。且后台跑看不到页面真实状态。

**执行要求**：
- 状态检测、等待、下载**全部用主会话前台调用**，逐步执行、每步立刻看返回值。
- 落盘后**必须校验完整性**：`os.path.getsize()` 与 `total` 比对，不等即截断 → **自动重试最多 5 次**。

### 规则二：**每过一分钟刷新镜像站网页**，才能拿到真实状态

**原话**：「每过一分钟刷新镜像站网页，才能更新到真正的状态」

**核心事实**：镜像站页面**不会自动更新 DOM**。实测：刷新前 `imgs:0`，刷新后 `imgs:33`（模型其实早已在后台完成）。

**执行要求**：等待期间每分钟刷新一次再读状态。

**⚠️ 但刷新有坑（我踩了）**：直接 `location.reload()` 把活跃会话刷成了 `about:blank`，**丢失整个已发送的对话**（10 张图只差 1 张时刷新，会话报废，第 09 张取不回）。
- **安全刷新法**：刷新前先记下当前 `vip-XX` 号，以便重开；刷新后若 `host` 为空/`about:blank` → 会话已丢，需重走跳转流程。
- **更稳妥**：非必要不刷新活跃会话，优先用 `tab new` 开新页读状态。

### 规则三：**绝不弹出让用户确认下载地址的窗口**

**原话**：「自己想办法下载所需文件，不要弹出要用用户确定下载地址的文件窗口，避免让用户执行多余操作」

**执行要求**：Agent 全程自己 `fetch → arrayBuffer → 分块取回 → 直接落盘到预设目录`，**用户零操作**。
落盘路径统一：`<项目目录>\生成图\<用途名>\`。

### 双写要求（郭老师明确）

**这些记忆不仅要在 WorkBuddy 中记载，更要写入 Obsidian 记忆仓库。**
- WorkBuddy 侧：`C:\Users\郭永涛\.workbuddy\skills\gpt-mirror-image\SKILL.md`（强制执行清单）
- Obsidian 侧：`D:\记忆\调度大脑记忆\流程\workflow_ai_wendabao_open.md` + 本文件