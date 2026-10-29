---
name: reference-贾维斯中控止损归档_20261022
description: 贾维斯中控项目止损归档结论（2026-10-22）：为什么停、已落地哪些、遗留资产与后续处置。
type: reference
updated: 2026-10-30
status: active
---

# 贾维斯中控 · 止损归档结论（2026-10-22）

> 写给未来的自己，不是给外人看的汇报。全部数字来自 2026-10-22 只读调查的 7 份报告，没有一处估算。
> **落位待裁决**：记忆库里已有正式条目 `D:\记忆\项目\project_贾维斯中控.md`（45 行）。本档是 `_inbox` 草稿，**未改动任何正式目录**；建议最终压成「止损归档」一节追加到那份正式条目末尾（见 §8）。是否追加由郭老师定。

## 1. 一句话结论

贾维斯中控（原 Codemote / Remote-Coding-Control）是「对手机说一句话，电脑替你办妥」的语音遥控电脑产品，**停在"设计已成形、代码侧冻结、远程通道按指令切断"这一步**：主产品代码在 `D:\Remote-Coding-Control`（不在文档库里），自 **2026-09-27** 起再无改动；文档库最后改到 **2026-10-20**（基础设施变更续记）；**2026-10-20 当天远程通道被"彻底断"（进程＋两个计划任务＋注册表 Run 项三处清零）**，至今未复活。

## 2. 现在磁盘上到底有什么（三层关系，最容易搞错的地方）

| 层 | 路径 | 是什么 | 此刻状态 |
|---|---|---|---|
| 文档层 | `D:\Work\贾维斯中控` | **只有文档**：34 篇自撰 .md（产品/架构/UX/工程/里程碑/进度/决策/研究/实验方案）＋ 一个微信通知自动化实验（**9 个手写源文件 / 1,605 行**＝7 个 .py ＋ 1 个 .html ＋ 1 个 .ps1） | 文档最后改动 2026-10-20；**代码 2026-09-27 后冻结**（25 天） |
| 代码层（真正的主产品） | `D:\Remote-Coding-Control` | companion 后端（FastAPI＋uvicorn，:8765）／mobile_app（Flutter）／web（PWA，`src/*.jsx` 含 VoiceControlSection.jsx） | **当前未运行**（计划任务 Disabled；8765 被无关进程占着） |
| 决策层 | `D:\项目\ai-hub\search_gateway` | Jev 网关：Windows 服务 `ai-gateway-3100`（nssm 托管，AppDirectory 指向该仓 `services`），监听 127.0.0.1:3100，`/v1/jev` 出结构化选择＋置信度 | **运行中**（Automatic＋Running，PID 3664） |

- **网关是决策层（上游），companion 是它的客户端**（`jev_router.py:4/:23` 指向 `:3100`）；微信实验也是它的客户端（`app.py:26`）。
- 三层里**只有网关在跑**。文档库里那 16 个"主产品构件"（Companion／Policy Engine／Capability Registry…）一个都不在那 4,477 个文件里——**那是设计库，不是代码库**。
- 微信通知自动化 2026-09-29 被裁定**并入而非归档**（`_搬迁说明_20260929.md`：「为什么是并入而不是归档」）。

## 3. 为什么跑不起来（按可执行性排，一行一条）

1. `启动_微信通知助手.ps1:3` 硬编码已删除的旧路径 `D:\Work\微信通知自动化`；因 `$ErrorActionPreference="Stop"`，脚本在 L8 拉起 python.exe 时**直接中止**，连开浏览器都执行不到。
2. `app.py:551` `WHISPER_DIR` 是同一批失效绝对路径 → 语音转文字降级（不阻塞启动，`preload()` 有 try/except 兜住）。
3. `app.py:65` 仍按**微信 3.x** 的窗口类 `WeChatMainWndForPC` 找窗口，本机微信是 **4.1.15.13**（`Weixin.exe`），4.0 之后控件树整体失效；替代的"截图＋视觉核对"**只写在方案文档里、尚未落进 `app.py`** → 主链路（搜索会话→核对→发送）跑不通，这是开发缺口不是环境缺口。
4. companion 的 **8765 被两个无关进程占着**（`python -m http.server 8765 --directory D:\Work\English-Content-Factory\...\03_Products`，PID 22896 / 23876，10-20 09:03 起）；计划任务 `\RemoteCodingControl` **= Disabled**（LastRun 2026-10-20 02:02:08，LastResult 0x41306）；全机无存活进程引用 `D:\Remote-Coding-Control` → **端口在，产品不在跑**。另有同源旧路径 `companion\app\config.py:19` 的 `WHISPER_MODEL_ROOT`。
5. **无 `requirements.txt` / `pyproject.toml`**（全库 0 命中）；依赖唯一真源是随库携带的 `.venv`（334,384,636 B ≈ **319 MB**，已被 `**/.venv/` gitignore）→ 换机/重建即失忆，**环境不可复现**。

## 4. 还有哪些东西真的能用（不吹，逐条说能拿去干什么）

1. **微信 4.0 截图核对＋键盘剪贴板流方案**（`方案_微信4.0截图核对键盘流_现行_20260930.md`）——4.0 时代唯一实测可用通路，启迪项目的现行做法已沿用。→ 拿去：任何"对微信桌面版做通知/自动化"的新活，**别再写 uiautomation 控件树**。
2. **companion 的执行器三件套**（`capabilities/`＋`policy.py`＋`artifacts.py`＋`jev_router.py`）——策略闸、产物归档、能力注册都是现成的；companion 依赖 6 项全在它自己的 `.venv`（CPython 3.13.2），开箱可读。→ 拿去：给任何"外部指令→本机执行"类项目套一层策略与产物留痕。
3. **Jev 网关接法**（`:3100/v1/jev`，key 从 `search_gateway\data\api_state.json` 读，`COMPANION_GATEWAY_KEY` 缺省回落）→ 拿去：需要"自然语言→结构化决策＋置信度"的项目直接复用，别再造路由层。
4. **零依赖单文件前端＋"干跑→逐条人工确认→再发送"纪律**（`ui/index.html` 278 行、无构建无 CDN；纪律写在 `app.py:5`）→ 拿去：任何会**向真人发不可撤销消息**的自动化，第一版就照抄这三段式。
5. **止损期的工作法**（3 轮外部评审＋"能否停手"当成一次正式评审来问＋交接单/决策档续记体例）→ 拿去：任何做了一半想收手的设计类项目。

## 5. 决策时间线（只保留真正拍过板的）

- **2026-09-29 · 服务器与商业化决策** → `07-Decisions\2026-09-29-服务器与商业化决策记录.md`：本机算力／阿里 99 ECS／腾讯轻量的分工；"云端算力购买话题关闭，现在不买任何服务器"（这份文件也是 §9 续记所在）。
- **2026-09-27 · 移除 AntigravityAdapter** → `D:\Remote-Coding-Control\companion\app\adapters\__init__.py:99`（提交 `1aba901`）：适配器文件删除、兜底改 claude_code；但 ADR-02 仍标"✅ 已采纳并实施"，文档没同步。
- **2026-10-20 · 基础设施变更（当面拍板）** → 同上决策档 §9「2026-10-20 续记」：powercfg 改从不睡眠、nssm 服务改 S4U＋看门狗 5 分钟循环、停用 `RemoteCodingControl`/`CodemoteFrpc`、删除注册表 `HKCU Run\RemoteCodingControlTunnel`；远程"彻底断"＝**清三处**（进程＋两个计划任务＋注册表）。

## 6. 教训（这节最值钱，5 条可迁移）

1. **文档先行没有"代码对照"，文档会系统性说谎。** 依据：文档地图 §5 列了 **18 条内部矛盾**（Session 状态三套、路由阈值两套、语音栈四套、Run 终态三套…），另有 **13 条 wikilink 断链**、3 篇 ADR（001/002/003）从未写出，显式版本号还停在 `0.1.0-M0`。
2. **密钥明文入库后，最小动作是先轮换再改写法；`.gitignore` 通配符笔误会把备份文件变成第二个密钥副本。** 依据：风险清单 §1.1——同一枚 JEV Bearer 出现在 **4 个已被 git 追踪的文件**（`app.py:27`、`app.py.bak-20260927:27`、方案文档 :12/:69）；根 `.gitignore` 写的是 `*.bak_*`（下划线），实际文件名是 `.bak-`（连字符），通配符失配。
3. **批量拷贝会毁掉 mtime，任何"按文件修改时间"做判据的机制（TTL／活跃度／过期清理）都会空转。** 依据：时间线 §4.2——抽样 100 个文件 **82 个落在同一天 2026-09-25**（`.venv` 的 4,389 个文件被统一刷成拷贝日）；同批记忆库盘点（`记忆-盘点.md` §6.7）显示 273 个 .md 中 252 个 mtime 同为一天，"以最后一次写入日期为基准"的 7 天 TTL 规则事实上处于空转状态。
4. **"端口在监听" ≠ "服务在跑"；判活要同时看监听者命令行＋计划任务状态＋进程路径三样。** 依据：冲突档 §3.2——8765 确实在 Listen，但持有者是别的项目的 `http.server`，主产品计划任务 Disabled、全机无进程引用其目录；文档地图正因只看端口，把"端口 Listen"误标成"服务在跑"。
5. **设计野心与落地量的比例失衡，是该收手的最强信号。** 依据：代码画像——手写代码 **1,605 行** vs 文档 2,346 行（**60% 内容是 Markdown**）；**7/9 个手写源文件仍硬编码搬迁前的旧路径**；3 个 `.bak-*` 与 2 个 0 字节日志已被 git 跟踪；`发送日志.jsonl` 从未被创建（这套实验很可能从未跑通过一次完整发送）。

## 7. 将来要复活：最小启动路径（抄报告，不自编）

**0. 先轮换 JEV 令牌**（风险清单 TOP10 #1/#2）：网关端 `127.0.0.1:3100` 重置该令牌 → `app.py:27`、`app.py.bak-20260927:27` 与方案文档 :12/:69 里的明文改为环境变量/占位 → 从 git 历史剔除。**轮换完成前不要启服务。**
1. 修 `启动_微信通知助手.ps1:3` → `$dir = "D:\Work\贾维斯中控\09-Experiments\微信通知自动化"`；也可跳过脚本直接走第 2 步。
2. `cd 'D:\Work\贾维斯中控\09-Experiments\微信通知自动化'` → `.\.venv\Scripts\python.exe app.py`（**必须用 venv 内解释器**，系统 Python 3.12 下依赖全缺）。
3. `Start-Process "http://127.0.0.1:8793"` 打开控制台。
4. （可选）修 `app.py:551` 的 `WHISPER_DIR` → 库内 `models\hf\...\snapshots\...` 真实路径。
5. 手动启动并登录微信客户端（`D:\Weixin\Weixin.exe`，4.1.15.13）。
6. 补唯一的真开发工作：按 `方案_微信4.0截图核对键盘流_现行_20260930.md` 实现微信 4.x 感知层，替换 `app.py:64-67` 的控件树取窗口。
7. companion 侧：腾出 8765（停掉 English-Content-Factory 那两个 http.server，**需人工裁决，本次未干预**）→ 把计划任务 `\RemoteCodingControl` 改回启用 → 修 `companion\app\config.py:19` 的 `WHISPER_MODEL_ROOT` 旧路径；companion 6 项依赖全在自己的 `.venv`，无需安装。
8. 固化依赖（一次性）：`.\.venv\Scripts\python.exe -m pip freeze > requirements.txt`。

## 8. 落位、检索与来源

- **检索**：grep `D:\记忆` 关键词 贾维斯／Codemicro／Codemote／语音遥控／微信通知／Remote-Coding-Control／RemoteCodingControl → **正文命中 14 个文件、79 处**；**标题只命中 1 个**：`D:\记忆\项目\project_贾维斯中控.md`。该正式条目已覆盖"是什么／文档真源／代码真源／三条联合点／自启三通道／已知坑"，**未覆盖**本次的止损归档、三层关系澄清、为何跑不起来、教训、复活路径。
- **建议**：把本档 §1–§7 压成「## 止损归档（2026-10-22）」一节，**追加**到 `D:\记忆\项目\project_贾维斯中控.md` 末尾；本档留在 `_inbox` 作原始草稿。等郭老师拍板。
- **路由**（memory-router skill 已加载）：`D:\项目\ai-hub-memory\MEMORY.json` 的 8 个项目（teaching／courseware／memory-system／english-teaching／english-learning／devel-tools／nitian-theme／ai-resources）与 `projects\` 实际目录（另有 gateway）**均无** 贾维斯中控／Codemote／语音遥控／Remote-Coding-Control 的别名或路径映射 → R1–R4 无法唯一确定 project_id，按 R7 **Fail Closed**：不写任何正式项目记忆线，只落本 vault 的 `_inbox` 暂存区。（未执行 `memory.py capture`，因其写入 `D:\项目\ai-hub-memory\inbox`，超出本次允许写入范围。）
- 本档来源：2026-10-22 只读调查，7 份原始报告在 `D:\Work\_inbox\vault-survey\`