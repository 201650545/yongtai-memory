---
name: reference-linuxdo福利羊毛清单-20261020
description: 2026-10-20 扫 linux.do「福利羊毛」分区（30 条）整理的可用免费资源清单：免费 API 站、闲置订阅共享 key、学生优惠真相、基础设施类；附各资源的原帖链接与接入可行性判断。
type: reference
updated: 2026-10-20
kind: reference
status: active
---

# linux.do 福利羊毛清单（2026-10-20 16:00 扫，30 条最新）

> 分类页：`https://linux.do/c/welfare/36`（Lv1 = `/c/welfare/welfare-lv1/60`）
> 扫描方式：opencli browser 读列表 + 逐帖读首帖（脚本 `buddy2api/scripts/scan_linuxdo_welfare.py`）
> ⚠️ **共享 key / 订阅链接一律不抄进本仓**（本仓是公开镜像）——只记原帖链接。

## 一、能直接当 API 用的（对我们最有价值）

| 资源 | 内容 | 原帖 | 接入可行性 |
|---|---|---|---|
| **chatshare.tv** | 把 ChatGPT **plus/pro 免费席位**的 web 端反代成 API，**免注册、免费**，带聊天记录隔离 | /t/topic/3049759 | 站点活着（HTTP 200「公益试运营」），但 `/v1/models` 404 ⇒ API 路径要在网页里拿；★ 价值最高。**2026-10-20 16:40 实测**：主页显示 **Plus 席 24/120 空余、Pro 满员**，点「进入 Plus」→ `POST /identity` 领匿名身份 → 跳 **chat.chatshare.tv**（ChatGPT web 镜像，共享 Plus 账号池），**15 分钟无活动自动释放席位**。已做出 opencli「域名可切」覆盖版（`OPENCLI_CHATGPT_DOMAIN=chat.chatshare.tv`），但随后站点对我们 **connection reset** ⇒ **未接成渠道**（不稳的不进链）。默认仍是 chatgpt.com，**不破坏原 ChatGPT** |
| **river.ai** | 注册送 **$25 额度**；`api.river.ai/v1`；模型 `deepseek-ai/DeepSeek-V4.1-Flash`、`zai-org/GLM-5.3-Flash`、`DeepSeek-V4.1-Flash-1017` | /t/topic/3048324 | ★ OpenAI 兼容，**直连可达**（走 7890 代理反而不通，10061 拒绝）；`/v1/models` 返回标准 401「Missing or invalid Authorization header」⇒ **只差注册**。注册可能弹手机号验证（需免费接码平台），**要用户做** |
| **maimai 中转** | 基于 oc 反代，**免费给 ds-1017** 用 | /t/topic/3047482 | 有注册码；帖里说"额度准备更新" |
| **clinePass 闲置订阅** | 别人发的闲置额度（还剩 40%），模型前缀 `clinepass` | /t/topic/3049622 | 共享 key，稳定性看对方 |
| **StepFun / 阶跃星辰 pro 套餐** | 两条 base64 订阅链接，剩 95~98%，**当天到期** | /t/topic/3049317、/t/topic/3047553、/t/topic/3049180 | 过期即废，要用得马上 |
| **GLM Coding Plan 体验卡 ×5** | 7 天卡，支持 GLM-5.3 与 5.3-Flash | /t/topic/3049152 | 官方活动链接（bigmodel.cn），要注册 |
| **hub.linux.do #24493** | 国模免费 | /t/topic/3048351 | 站内 AI 平台 |
| **qoder 网页版** | 免费用 DeepSeek V4.1-Flash **到 10.24** | /t/topic/3047592、/t/topic/3048142 | 已用 opencli 驱动（要 `--remote-debugging-port=9237` 启动 Qoder） |
| **minimax 积分** | 有人问积分怎么用掉 | /t/topic/3047624 | 说明账号有积分待消耗 |
| **l0veyou / 生图公益站** | 见 `reference-外部公益站接入-l0veyou与生图公益站_20261020.md` | — | 已接入 3100 |

## 二、账号/优惠类（需要动手，有坑）

**Google AI 学生优惠（Gemini Pro/Plus）**——原帖复盘「已被反薅」，但规则很重要（/t/topic/3048172）：
- **美国高校学生**：可申请 **12 个月免费 Google AI Pro**；
- **非美区高校学生**：只有 **12 个月免费 Google AI Plus**；
- 两者都要 **SheerID 学生验证** + 匹配的 Google 账号与支付资料；
- ⚠️ **薅了 Plus 再取消订阅 ⇒ 优惠入口永久消失**（别取消）；
- ⚠️ 8.99 的 Pro 若页面**不显示续费到 2029** ⇒ 实际只有 1 个月，别订。
⇒ 结论：**美区 + 高校在美 ⇒ 一年免费 Pro**，比共享 key 强得多，值得单开账号搞。

其它生活类：移动 1~9 元话费券（/t/topic/3047552）、中银香港云闪付 5% 返现（/t/topic/3047940）、
粒上皇 10 元券（/t/topic/3047824）、微软 BING 领 B 站大会员（/t/topic/3048456）、
广东移动 0 元 10G 30 天（/t/topic/3049664）、武汉通 ApplePay 新卡免开卡费（/t/topic/3047612）、
4 个自建 CPA 48Team 标准席位 key（/t/topic/3047955，本次未渲染出来）。

## 三、基础设施类

Vmiss 便宜 VPS 放 tri（/t/topic/3048849）、200g 流量 11-20 到期（/t/topic/3048499）、
免费 Clash/V2Ray 节点订阅（/t/topic/3049721）、
insta 机器邀请可建 5 个 4H8G 容器（/t/topic/3048337）、
Linux Do Credit 怎么赚（帖里有人问）、LV中转 lvlv.lol（注册3元+留言2元+进群5元=10元额度，要发币）。

## 四、扫这类的纪律（别再犯）

- **低频**：1 个分类页 + N 个帖页，每页等 8s；撞 Cloudflare 挑战就多等（标题 "Just a moment..."，约 36s 自动过）。
- **别把别人的共享 key / 订阅链接抄进公开记忆仓**。
- **发现有用渠道先问郭老师要不要接**，别一口气全接（管理成本）。
- 探上游接口时**只读不生成**：GET /v1/models 之类不烧额度；真出图/出文才算消耗。

## 关联

- `reference-外部免费渠道-linuxtodo与公益站_20261020.md`（侦察过程与风控规律）
- `reference-外部公益站接入-l0veyou与生图公益站_20261020.md`（已接入的两个）
