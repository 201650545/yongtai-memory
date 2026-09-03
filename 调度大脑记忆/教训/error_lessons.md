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

**修正**：凡是含引号/正则/多行的 Python，一律先 Write 成 `D:\项目\_tmp\xxx.py` 再 `python 该文件`，不要内联。临时文件路径给 Windows 原生 Python 用时也要避免 `/tmp`（git-bash 虚拟路径 Windows python 看不见），统一用 `D:/项目/_tmp/`。

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
