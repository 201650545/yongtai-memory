---
name: browser-session-rule
description: 用户反复强调：OpenClaw/CDP 打开的浏览器应是他已打开在用的 Chrome（十几个标签页，登录永涛账号），不是全新实例
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 95cff9f0-c115-4770-a66a-5ed8ec23a5c2
  modified: 2026-08-11T14:24:28.021Z
---

用户要求：用浏览器（OpenClaw/CDP）操作时，打开的应是他**已打开在用的 Chrome**（十几个标签页，登录账号 永涛 / yongtaog767@gmail.com），不是新开的干净实例。

**Why:** 用户不想重复登录；已有会话（飞书/其他）应直接用。

**How to apply:** 连接浏览器后先 `mcp__cdp__list_pages` 核对——若只有少量页面/显示登录页，说明当前连到的是 chrome-devtools-mcp 默认的独立 profile，而非用户主 Chrome（主 Chrome 默认无 --remote-debugging-port，无法直接附加）。此时如实告知用户当前看不到其会话，用最小动作补齐（如扫一次飞书二维码）。不要反复把他已登录会话当不存在、也不要硬编造会话存在。

**正确工具（用户 2026-08-11 反复强调，记死）：浏览器操作一律用 Open CLI（opencli），不要用 chrome-devtools-mcp！**
- opencli Browser Bridge 通过扩展连接用户**日常在用的 Chrome**（daemon:19825，profile `n8hh7hyn default`）。`opencli doctor` 可诊断连通性。
- 用法：`opencli browser <会话名> <命令>`（bind/state/tab list/open/click/type/fill/eval/screenshot 等）；`--profile <name>` 指定 profile。会话首次用 `opencli browser <新会话名> open <url>` 建立。
- 网关项目已用它驱动 4 大 AI 搜索（D:\游戏\ds_v4_cli，setup_engines.py 绑会话）。AI 引擎实测经验见 [[project-ai-gateway]]。
- chrome-devtools-mcp 只能控制它自己 `--remote-debugging-pipe` 启动的隔离实例，**物理上无法附加到已在运行的 Chrome**——用户已明确不满，别再用它当默认浏览器工具。

**技术事实（2026-08-11 实测，供参考）：**
- 用户主 Chrome 的 Default profile **拒绝绑定** `--remote-debugging-port`（换端口/flag/杀光进程都试过），全新空 profile 能绑。属 Chrome 136+ 对主 profile 的安全保护。
- 把用户 profile 的 Local State/Cookies 拷进隔离 profile → 只能拿到**登录态**，扩展和其他网站登录记录带不过去。此路不通，走 opencli。
