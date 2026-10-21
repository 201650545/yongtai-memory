---
name: workflow_external_model_review_public_link
description: 用公开 GitHub raw 链接让外部强模型（ChatGPT 镜像站 GPT-6 Sol）自己读材料再评审，同窗口续问做「相互讨论」——已实测跑通两轮
type: workflow
updated: 2026-10-21
---

# 外部强模型协作：公开链接指路 ＋ 同窗口相互讨论

> 2026-10-21 郭老师定：「你把公开仓库的链接发给 ChatGPT，强制让它去读；
> 把提示词塞进公开链接中，让它强制去读某个文件里的提示词，然后跟它相互讨论。」

## 一、为什么是这条路

- 长材料塞进输入框迟早失败（实测 110K 字符静默失败、5K 分块会被共享标签抢占打断）。
- 镜像站里的 ChatGPT **没有我的 GitHub 授权** ⇒ **仓库必须公开**（私有仓等于没推）。
- 官方 skill 已把它固化成脚本：`external-model-review\components\gpt-mirror-extended-review\scripts\publish_prompt.py`
  （`--file/--repo/--path/--branch/--note`，输出 raw URL；**会检测仓库私有性并中止**）。

## 二、已跑通的完整流程（2026-10-21 实测两轮）

1. **写材料**：把背景、方案全文、**真实数据样本**、要它答的问题清单写成一个 md
   （**它只能读文件，给原则不给数据它就会空谈**）。
2. **发布到公开仓**：`publish_prompt.py --file <md> --repo 201650545/workspace-index --path reviews/<name>.md`
   ⇒ raw URL `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>`；
   **必须再无授权 GET 一次验可读**（`Invoke-WebRequest` 期望 HTTP 200）。
3. **输入框只留指路**：「请阅读 <raw URL> 的全文（它包含…），然后按第 N 节逐条回答」。
4. **走 skill 的三闸**：`Chat` 标签 / 模型 `6`（=ChatGPT 6 Sol）/ 档位 `High`；不过就拒绝发送。
5. **取回复**：`wait_and_fetch.py <目标md>`（2.5s 心跳；长答案要刷新后重读，DOM 兜底标 `[SUCCESS·DOM]`）。
6. **第二轮同窗口续问**：把「核实结果 ＋ 已做的修复 ＋ 真实字段 ＋ 新的追问」写成第二份材料发布，
   再在**同一 `/c/…` 会话页**用 `send_turn.py` 续问（它保留全部历史上下文，GPT 不用重新交代背景）。
   ⇒ 轮数纪律：**每任务 ≤3 轮，每聊天框 ≤24 轮**。

## 三、这一轮踩到的坑（都属于 skill 文档里已有的，我跳过规范才踩的）

| 坑 | 症状 | 正解 |
| :-- | :-- | :-- |
| 跳过 P1 探针直接开浏览器 | 拿到的卡是 **Free 账号**（`郭老师 / Free` ＋ `Rejoin Plus`）⇒ 页面上**根本没有模型 pill 和档位滑杆**，三闸无从谈起 | 先跑 `probes\probe_gpt_mirror.ps1`，读 `runtime\gpt-mirror.drift.json` 的 `summary`；`warn>0` ⇒ 停下报人 |
| 卡号自选 | 用了 vip-25/vip-31（不在契约候选集内） | 契约 `card_id_discovery` 走 **explicit_list**（vip-23/vip-49/vip-11）；池页 HTML 路径已永久失效（SPA 壳） |
| 长 JS 整段送 | `Runtime.evaluate timed out after 115s` ⇒ 三闸永远假失败 | base64 切 **≤2000 字符/段** 推进 `window.__llB64`，最后页内 `eval(atob(join('')))` |
| 存档网址写错位置 | 备份在 skill 目录 ⇒ 真源 `D:\Work\元智能\20_自适应工作流引擎\runtime\gpt_mirror_active_url.txt` 仍是旧会话 ⇒ 首轮被切去已失效的卡 | 存档真源只有 `20_自适应工作流引擎\runtime\` 那一个 |
| 首轮被误判"页面漂移" | 首轮本来就在根地址（发出后才进 `/c/`）⇒ 被切回几天前的旧会话 | 已修 `send_turn.py`：只有「当前是**别的** `/c/` 会话」才算漂移（CHG-14） |

## 四、怎么判断"它真的读了"

- 它会**引用文件里的具体内容**（如点名 `qwenwork/flash` 这个矛盾、复述表格里的样例）⇒ 读了；
- 它会**主动说"我尝试读取 X 但工具不支持该 content-type，读不到"** ⇒ 读不到时不编；
- ⚠️ 它也可能**把材料里的字段语义搞错**（例如把我生成的日报里的"网关模型"字段当成别的含义）
  ⇒ **凡它提出的"矛盾"，都要回本地核实再回应**，别直接认领、也别直接反驳。

## 五、这一轮的实际收获

外部评审**抓到了我实现里的真 bug**（短 tail 子串误配 + set 无序导致结果不可复现），
并把方案的**排期从"一期出完整席级表"收窄成"一期只做①层型号归一化清单"**。
⇒ 价值不在于"外部模型更聪明"，而在于**它读的是落盘文件、给的是可逐条核对的结论**。

细节见 `D:\记忆\项目\project_aihot_slot_radar.md`。
