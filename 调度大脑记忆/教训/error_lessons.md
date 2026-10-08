---
name: error-lessons
description: 自动记录的 Bash/PowerShell 错误日志，Claude 应在执行类似操作前查阅
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2fd78737-0098-457f-9f20-e5e620ecec45
  modified: 2026-08-24T05:51:09.917Z
---

# 错误教训日志

此文件由 hook 自动追加，Claude 会在每次会话中参考以避免重复犯错。

---

## git-bash 内联 python -c 混合引号必炸（2026-08-23 两次踩坑）

**场景**：`python -c "..."` 里同时用单引号、双引号、正则（如 `re.search(r'X:\s*["\']?...')`）时，bash 的双引号包裹与 Python 字符串转义互相打架 → SyntaxError。

**修正**：凡是含引号/正则/多行的 Python，一律先 Write 成 `D:\项目\_tmp（已失效：目录已清空，内容为一次性脚本残留）\xxx.py` 再 `python 该文件`，不要内联。临时文件路径给 Windows 原生 Python 用时也要避免 `/tmp`（git-bash 虚拟路径 Windows python 看不见），统一用 `D:/项目/_tmp/`。

## runtime cli 重启不认手动/提权起的旧进程（2026-08-23）

**场景**：:3100 被 admin 权限的孤儿进程占着，`runtime/cli.py restart` 报「未在运行」另起新进程 → 双进程同听 :3100，请求仍落到旧代码进程。

**修正**：重启网关后必须 `netstat -ano | grep :3100` 核对只有一个 LISTENING；发现双进程先杀旧再验。提权进程普通 Stop-Process 拒绝访问 → 自写 ps1 + Start-Process -Verb RunAs 自提权（用户点 UAC）。

## YAML 块替换时前导空格翻倍（2026-08-23）

**场景**：用 Python regex 替换 YAML 文件中的 provider 配置块：
```python
pat = re.compile(re.escape(k) + r".*?(?=\n    \w[\w-]*:)", re.S)
t, n = pat.subn("    " + k + ":\n      ...", t)
```

**症状**：output 中 provider key 的缩进从 4 格变成 8 格（`        opencode-go:`）。

**原因**：match 从 `opencode-go:` 开始（不含前面的 `\n    `），但 replacement 以 `    opencode-go:` 开头。`\n    ` + `    opencode-go:` = 8 空格。

**修正**：用 `(\n\s*)` 捕获前导空格，replacement 用 `\g<1>` 引用：
```python
pat = re.compile(r"(\n\s*)" + re.escape(k) + r".*?(?=\n\s*\w[\w-]*:)", re.S)
t, n = pat.subn(r"\g<1>" + k + ":\n\g<1>  ...", t)
```

**验证**：`yaml.safe_load()` 通过即为正确。

## SSE 单换行分隔 → pi-ai JSON.parse 失败（2026-08-31）

**场景**：小红书/dots3 渠道（fast 组）流式响应里部分 SSE 事件只隔单个 `\n`，pi-ai 按 `\n\n` 切分把两条 data: 行拼成一个消息 → `JSON.parse` 报 "Unexpected non-whitespace character after JSON at position 210"。curl 直接打上游却正常（上游 OK，网关透传层坏）。

**根因**：网关 `api_gateway.py` 的 `_SseReasoningStripper.feed()`（reasoning 剥离层，所有流式响应必经）按行处理后用 `b"\n".join()` 重新拼装，原样保留了单 `\n` 分隔的不规范事件边界。

**修正**：feed() 改为对每条完整 `data:` 行强制以 `\n\n` 收尾（重定界），空行不透传。改完必须重启网关并用 awk/PowerShell 核对「无相邻 data 行」。同类排查口诀：**JSON.parse 位置数字 = 第一条合法 JSON 的长度 → 上游/网关把两条事件拼成一条了，查流分隔符**。

## CSS：backdrop-filter 劫持 fixed 包含块 + stacking context 封顶（2026-09-01）

**场景**：逆天主题给 DSH 侧栏 `sidebarCol` 加 `backdrop-filter:blur(18px)` 做毛玻璃 → 点「道藏」设置面板被压成 280px 窄条、全部文字竖排（面板 overlay 是 `position:fixed` 且不挂 portal，直接渲染在侧栏 footer 里）。

**根因（两层）**：① CSS 规范：带 `backdrop-filter/transform/filter/perspective/contain/will-change` 的元素成为所有 **fixed 后代的包含块** → 1600px 全视口面板被锁死在 280px 侧栏里。② 修复时若给该容器加 `isolation:isolate` 或任何 z-index 建 stacking context，内部弹层的 z:1000 会被封顶在容器层级里——isolate 会被 centerCol 相对子树盖住，z:1 盖不过 composerSeat(z:7)。

**修正（终稿模式）**：毛玻璃效果移到 `::before` 伪元素（`position:absolute;inset:0;z-index:-1`，伪元素无 DOM 后代，不劫持也不封顶）；宿主容器**只留 `position:relative`，绝不加 z-index 或 stacking context**，让内部 fixed+z:1000 升出子树参与全局竞争（= 原生行为）。

**排查口诀**：fixed 弹层「被压窄」先查祖先有没有 backdrop-filter/transform（包含块劫持）；「被盖住」先查祖先有没有 isolate/z-index/transform（stacking context 封顶）。二者都要求宿主容器保持"干净"。

## 镜像站三个流程性教训（2026-09-15，郭老师当面指正）

### 教训一：后台任务轮询镜像站 = 看不见的黑箱，必留残次品

**场景**：用 `run_in_background` 后台任务下载 10 张图，中途被 kill / 超时 → 留下 3 个**截断文件**（第02、03、08 张大小恰为 150000 / 300000 / 390000 字节，即 30000 的整数倍——**这是分块下载截断的判别特征**）。且后台任务看不到页面真实状态。

**修正**：**镜像站的回复一律用主会话前台监督**，状态检测 / 等待 / 下载全部逐步前台执行，每步立刻看返回值。禁止后台跑。

**落盘必校验**：`os.path.getsize()` 与 `total` 比对，不等即截断 → 自动重试。

### 教训二：镜像站页面不自动更新，必须每分钟刷新才有真实状态

**场景**：刚发送时读到 `imgs:0`，以为没出图；**刷新后 `imgs:33`**。页面 DOM 不会自动更新，模型在后台实际已完成。

**修正**：等待期间**每分钟刷新一次**再读状态。

**⚠️ 但刷新本身有坑**：直接 `location.reload()` 把活跃会话刷成了 `about:blank`，**丢失已发送的对话**（实测：10 张图只差 1 张时刷新，整个会话报废，第 09 张无法取回）。

**安全刷新法**：刷新前先记下当前 `vip-XX` 号；刷新后若 `host` 为空 → 会话已丢，需重走跳转。**更稳妥：非必要不刷新活跃会话，优先用 `tab new` 开新页读状态。**

### 教训三：绝不弹让用户确认下载地址的窗口

**场景**：下载图片时若走浏览器默认下载，会弹"另存为"对话框，要用户手动选路径。

**修正**：Agent 全程自己 `fetch → arrayBuffer → 分块取回 → 直接落盘预设目录`，**用户零操作**。

---

## 记忆写成"描述"而非"清单" → 关键步骤反复漏（2026-09-15，郭老师追问根因）

**场景**：镜像站「开 Extended」这一步**反复漏**，每次都要用户提醒。

**根因（三层）**：
1. **主因**：旧记忆写的是**观察描述**（"pill 选项已改名为 Thinking• Standard"），不是**动作指令**（"发送前必须点它并验证"）。描述需要主动推导出动作，清单直接执行——忙碌时推导极易丢失。
2. **次因**：记录埋在"踩坑日记"里，天然语境是"历史"而非"必须遵守"。而且项目日志会不断被新日志淹没。
3. **最隐蔽**：上次的成功记录本身就是漏了这一步的，照"上次怎么做的"惯性复现，错误被一起复现。

**修正原则（可复用）**：
- **规范必须写成强制执行清单**：①→⑥ 逐条走、每步验证通过才进下一步、标明"禁止凭惯性操作"。
- **最易漏的步骤用 `★★★` 显式标记**。
- **写出"失败怎么办"**（重试几次、仍失败就停下问用户）。
- **放在最高可见度位置**（文件顶部 / 独立技能），不要塞在项目日志里。
- **双写**：WorkBuddy 技能（`~/.workbuddy/skills/`）+ Obsidian 流程文档（`D:\记忆\调度大脑记忆\流程\`）。


---

## 教训四：刷新镜像站会**重置 Extended 模式**（2026-09-15 实测）

**场景**：按规则二刷新镜像站读状态后，模型回答为空、asst 计数为 0。

**根因**：`_ext10.py` 开启后 pill='Extended' → 执行 `_watch.py reload` → **pill 回落为 'Auto'**。刷新把模型选择重置了。本轮因"先发送、后刷新"，Extended 失效，模型空跑 2 分钟且一无所获。

**修正铁律（顺序不可颠倒）**：

```
刷新 → 重开 Extended → 验证 pill='Extended' → 注入 → 发送
```

**绝对禁止"先发送、后刷新"。**

## 教训五：镜像站的 asst 计数**不可信**（2026-09-15 实测）

**场景**：asst=0 时一度判定"模型没回答"，实际模型正在出图。

**根因**：镜像站不渲染 `data-message-author-role=assistant` 节点。

**可靠信号**：

| 信号 | 含义 |
|---|---|
| pill 文本含 Generating / Thinking | 正在生成（最可靠） |
| 图片 naturalWidth > 0（如 1672x941） | 已出图可下载 |
| img.src 含 estuary 但 naturalWidth=0 | 页面骨架资源，尚未出图 |
| data-message-author-role=user 计数 | 可靠：u=1 表示消息已入会话；不增长 = 消息根本没发出 |

## 教训六：落盘**禁止依赖序号自动命名后 mv 覆盖**（2026-09-15，导致封面丢失）

**场景**：下载脚本按"当前页面唯一图 = 第01张"命名，随后 mv 第01张.png 第09张.png，**把原有封面静默覆盖丢失**，需重新生成补回。

**修正**：

- 输出文件名**必须显式指定**，不依赖序号。
- 落盘前先 `os.path.exists()` 检查，**存在则报错换名，绝不静默覆盖**。
- 批量产物落盘后做一次**清单校验**（文件数 / PNG 头尾 / 字节数）。

## 教训七：镜像站取图的最稳路径 = 页面内 fetch → dataURL → 字符级分块（2026-09-15 验证）

**背景**：图片 URL 带 `&fn=&cd=&ts=&sig=`，**`&` 会被 cmd 解析炸掉**（'fn' is not recognized...），不能直接 curl。

**而且**：`eval` **不支持顶层 await**（报 `ReferenceError: await is not defined`）→ 不能写 `await fetch(...)`。

**正确两步法**：

1. JS 里用 `fetch(src).then(r=>r.blob()).then(...)` 转 FileReader 存入 `window.__IMG`，**立即 return "started"**（不阻塞）。
2. 等 15~20s 确认 `window.__IMG` 就绪（查 sz / len / head 是否为 `data:image/png;base64,iVBORw0KGgo`），再按 **CH=600000 字符**分块读回。

**关键纠正**：旧笔记写"按 30000 字节分块、CHUNK 必须 3 的倍数"，那是 `arrayBuffer→base64` 路径的约束。**dataURL 路径按字符分块无填充问题**（实测 1,160,890 字符 → 870,650 字节一次成功）。

**必须剥离 `data:` 前缀再解码**，否则报 `Incorrect padding`。

**校验**：PNG 头 `89504e470d0a1a0a`、尾 `49454e44ae426082`（无尾 = 截断）。
