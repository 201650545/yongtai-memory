---
name: lesson_弹窗判定看PE子系统不看名字
description: 🔴 判"会不会弹控制台窗"的唯一机械判据是 PE 子系统字节（2=GUI 不弹／3=CUI 必弹）＋子进程 creationflags，不是文件名、不是注释、不是 -WindowStyle Hidden。2026-10-02 贾维斯中控开机弹终端案：uv venv 的 `Scripts\pythonw.exe` 实测是 CUI(3) 的 45KB 转发存根，名字叫 pythonw 但照弹；同案含"关窗口＝杀服务"与"只换启动器会把一个常驻窗变成每 5 秒闪两个窗"两条连带教训
metadata:
  node_type: memory
  type: 教训
  created: 2026-10-02
  modified: 2026-10-02
---

# 判"会不会弹窗"看 PE 子系统字节，不看名字也不看注释

## 一句话

**`pythonw.exe` 这个名字不是证据。** 它如果是 venv/uv 生成的转发存根，PE 子系统就是 `CUI(3)`＝控制台程序，计划任务用交互登录令牌跑它＝开机必给一个黑窗。唯一的机械判据是读文件头那个字节，加上检查每一处 spawn 有没有 `CREATE_NO_WINDOW`。

## 本案（2026-10-02，贾维斯中控 / Remote-Coding-Control）

郭老师报"一开机那个 remote code 会弹终端窗口"，违反他 2026-09-24 定的红线 [[调度大脑记忆/反馈/feedback_no_popup_windows]]。查出**四条**自启通道，全部"本意隐藏、实际带控制台"：

| 通道 | 本意 | 实测 | 结果 |
|---|---|---|---|
| 计划任务 `\CodemoteFrpc` | 公网隧道 | 动作是裸 `frpc.exe`，**PE 子系统 CUI(3)**，`LogonType=Interactive`，`Hidden=False` | 开机一个**常驻**黑窗 |
| 计划任务 `\RemoteCodingControl` | "用 pythonw 所以无窗"（`register_task.ps1` 描述里就这么写） | `.venv\Scripts\pythonw.exe` ＝ uv 的 45,568 字节存根，**CUI(3)**；而 uv base 的真 `pythonw.exe` 是 **GUI(2)** | 同样弹 |
| `HKCU\...\Run` = `RemoteCodingControlTunnel` | `powershell -WindowStyle Hidden` | 控制台**先分配**、style **后应用** | 每次登录一闪 |
| `Startup\start_search_gateway_3000.bat`（另一个项目） | 注释写"no console - popup red line" | `.bat` 本体就是 cmd 控制台 | 同类缺陷 |

**判据字节**（可复制的读法）：`e_lfanew@0x3C` → `PE header + 24 + 68` 处的 WORD；2＝GUI，3＝CUI。**必须先拿对照样件验解析器**：`notepad`/`explorer`＝2、`cmd`/`ping`/`node`/`powershell`/`adb`/`frpc`＝3。我第一次读出的 `pythonw.exe＝CUI` 自己都怀疑是解析 bug，跑完对照才敢信。

## 三条连带教训（比"把窗关掉"本身更值钱）

1. **他关窗的动作就是在杀服务。** 两个任务的 `LastTaskResult` 都是 `0xC000013A`＝STATUS_CONTROL_C_EXIT＝**只有带控制台的进程才可能死在这个码上**（这条是决定性反证：真无窗程序不会这么死）。关掉 companion 的窗＝手机立刻"电脑未连接"；关掉 frpc 的窗＝出门链路断。**弹窗类故障别只当噪音，它常常是服务被打死的死因。**
2. **只换启动器不加 `CREATE_NO_WINDOW`，会把"一个常驻窗"放大成"每 5 秒闪两个窗"。** 因为原来那个 CUI 存根虽然恶心，却替子进程提供了继承控制台；换成真 GUI 的 pythonw 后父进程无控制台，`node`/`adb` 这些 CUI 子进程就各自分一个新窗口。**修这类问题必须父进程与所有子进程一起过一遍。**
3. **`capture_output=True` / `stdin/stdout/stderr=PIPE` 挡不住弹窗**（红线第 2 条的再确认）。`feishu_relay.py:262` 三条管道全给了，照弹。

## 修法（本机已落地，未 commit）

- 子进程一律 `creationflags=subprocess.CREATE_NO_WINDOW`：本案补了四处（`feishu_relay.py:272`、`claude_code_adapter.py:151`、`devops.py:157`、`tunnel.py:118`）。
- 计划任务的 Action 指向**真 GUI** 解释器：`\RemoteCodingControl` → uv base `pythonw.exe` + `service_launcher_direct.pyw`。
- 控制台程序（`frpc.exe` 这类）没法靠包装消窗 → **改任务的登录类型为无交互会话**：`\CodemoteFrpc` → `BootTrigger` + `SYSTEM/ServiceAccount/Highest`。⚠️ 副作用＝从此 SYSTEM 持有，普通 shell 关不掉，与 [[调度大脑记忆/教训/lesson_gateway_restart_privilege_trap]] 同型，改之前要认这个账。
- Run 键不能直接指控制台程序 → 指 `wscript.exe <一个 vbs>`，由 vbs 以窗口样式 0 拉起（wscript 本体是 GUI）。

## 验收纪律（这次踩到的测量坑）

- **"一闪"必须高频采样**：120–150 ms 采一次、取峰值减众数（众数＝他自己开着的终端稳态数）。低频采样会漏。
- **全局窗口计数会被自己的工具污染**：我第一次测出"基线 8 个终端窗"，那里面包括我自己 Bash 起的控制台。按 PID 归因又失败——Windows Terminal 托管时窗口属主是 WT 进程不是被启动的那个进程。**可用的设计是 A/B 交替多轮（旧写法/新写法各 3 轮）比增量**：本案 A 组 3/3 都 +1，B 组 3/3 都 +0。
- **别拿"端口没监听"倒推"从来没起来过"**：我据此下过一次错结论，被日志推翻（`service.log` 里 09:45:55 明明起了、还监听过）。判"起没起过"要看**带时间戳的服务日志**，判"现在活不活"才用端口。

## 状态（2026-10-02 落地后实测）

`\RemoteCodingControl` 动作解释器复验＝GUI(2)；`:8765` 在听；`\CodemoteFrpc` 改完 `State=Running`、frpc 1 个进程；两条 `node event consume` 存活 711 秒（此前每 5 秒重启一次）；Run 键＝`wscript.exe run_hidden.vbs`。**"下次真开机不弹"尚未由真开机验证**，本轮是在同机器上用等价上下文（无控制台父进程）证的。

**How to apply:** 审查任何 Windows 自动化（计划任务／Run 键／Startup／NSSM／看门狗）时，先读动作里那个 exe 的子系统字节，再顺着它的每条 spawn 找 `creationflags`；两条都过了才算"不弹窗"，注释和文件名都不算证据。相关：[[调度大脑记忆/反馈/feedback_no_popup_windows]]、[[调度大脑记忆/项目/project_贾维斯中控]]、[[调度大脑记忆/项目/project_ai_gateway]]
