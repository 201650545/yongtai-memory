# Gemini 网页版：可驱动性、能力边界与实测结论

> 建立：2026-10-15（DeepSeek 窗口实测）｜ 分类：参考 · 外部资源指针
> 一句话：**Gemini 网页版能被 opencli 驱动，但读不了公开 GitHub 仓库**（与 ChatGPT 镜像站能力不同）。

---

## 一、为什么记这篇

郭老师 2026-10-15 提出：ChatGPT-6 镜像站能读我们的 GitHub 公开仓并给出高质量回答，
**Gemini 网页版（AI Ultra 会员）文字能力也强，是否也能这么用？**
本篇记录**实测结论**，避免下一个人重复试错，也避免把"未验证"当成"已具备"。

---

## 二、✅ 已实测：可驱动性（本机环境）

| 项 | 实测结果 |
| :--- | :--- |
| 访问地址 | `https://gemini.google.com/app` |
| 驱动方式 | `opencli browser <session> tab new <url>` + `eval` |
| 使用的会话档 | `d5vtd5bg`（本机默认 Chrome，桌面） |
| 登录状态 | **已登录**（直接可用，无需重新授权） |
| 账号档位 | 页面底部显示 **Google AI Ultra** |
| ⚠️ 加载特性 | **SPA 需约 40–60 秒才挂载完**。刚打开时 `document.body` 里几乎没有节点（曾出现 `divs:35 / btns:0`），**必须等到 `btns>0` 且输入框出现**再操作 |
| 输入框 | Quill 编辑器：`rich-textarea > .ql-editor[contenteditable="true"]` |
| 回复节点 | `model-response`（外层）→ `message-content`（正文）→ `div.markdown` |
| 生成中判定 | 出现 `button[aria-label*="Stop"]` / 状态条显示 "Searching the web" |

**发送脚本**：`D:\小浣熊\_gemini_send.js`（插入文本 + 单次点击发送）

> 🔴 **发送必须只点一次**。指针序列只到 `mouseup`，**不要在序列里放 `'click'`**，激活只由最后那一句 `btn.click()` 负责。
> 这条与 ChatGPT 镜像站的 `send_turn.py` 是同一个坑（见 skill `gpt-mirror-extended-review` 的 CHANGELOG CHG-9）：
> 序列里含 `'click'` + 再调 `.click()` = **点两次** = 消息发两条 = 平台判定重复提交。

---

## 三、❌ 已实测：读不了公开 GitHub 仓库

**测试方法**（2026-10-15）：在输入框里贴上公开仓链接，要求它回答仓库里的一个具体事实，
并约定「读不到就直说无法访问，不要猜」：

> 请读取这个公开 GitHub 仓库 … https://github.com/201650545/english-content-factory
> 问题：这个仓库里规定的「每页填充率硬性门槛」是多少？
> 如果无法访问，请直接回答「无法访问外部链接」，不要猜测答案。

**实测结果**：Gemini 页面出现 **"Searching the web"**（它确实尝试了联网检索），
但最终回答只有一句：**「无法访问外部链接」**（8 字）。

**结论**：**Gemini 网页版不能像 ChatGPT 镜像站那样，靠贴一个 GitHub 链接就读取仓库内容。**

---

## 四、⭕ 尚未验证的替代路径（谁要试谁补记）

| 路径 | 状态 | 备注 |
| :--- | :--- | :--- |
| 把仓库内容**直接贴进正文** | 未验证 | 一定可行但受上下文长度限制，且费人 |
| **附件上传**（把 .md 打包上传） | 未验证 | Gemini 支持上传文件，值得一试 |
| **Deep Research** 模式 | 未验证 | 该模式具备联网研究能力，**最可能读通** |
| 让它自己 `web_search` 找仓库 | 已验证不可靠 | 本次就是这样失败的 |
| 走 API（而非网页版） | 未纳入 | 需要 API Key，与"用会员网页版"的初衷不同 |

---

## 五、与 ChatGPT 镜像站的对比（选型用）

| 能力 | ChatGPT 镜像站（wendabao → vip-XX） | Gemini 网页版（AI Ultra） |
| :--- | :---: | :---: |
| opencli 可驱动 | ✅ | ✅（SPA 慢，需等 40–60s） |
| 读公开 GitHub 仓库 | ✅ **实测通过**（读过 8 份 md + 5 张图，还抓出文档不一致） | ❌ **实测失败** |
| 读图片内容 | ✅ | 未测 |
| 档位控制 | 三闸：Chat + 模型 `6` + pill `High` | 模型选择器（页面显示 `Argon Medium` 等） |
| 已知坑 | 双发按钮（已修）、中断需刷新 | 加载慢；发送同样只能点一次 |

**结论**：需要"让外部模型读我们的仓库再评审"这类用途 → **仍走 ChatGPT 镜像站**；
Gemini 适合当作**纯文本能力补充**（把材料直接贴进去问），或后续验证 Deep Research 路径。

---

## 六、相关文件

- 发送脚本：`D:\小浣熊\_gemini_send.js`
- 对照 skill：`D:\Work\元智能\10_AI自成长引擎\技能库\gpt-mirror-extended-review\`
- 被用作测试对象的公开仓：`https://github.com/201650545/english-content-factory`
