---
name: project-贾维斯中控
description: 贾维斯中控＝语音远程控制电脑（手机遥控器＋电脑执行体），原 Codemote／Remote-Coding-Control，2026-09-29 改中文名。当前阶段"重定义／M1 准备"。三条联合点：走网关 :3100/v1/jev 做意图路由、公网入口在阿里 99 ECS 的 frps、执行体是本地 PC。文档真源 D:\Work\贾维斯中控，代码真源 D:\Remote-Coding-Control
metadata:
  node_type: memory
  type: 项目
  created: 2026-09-30
  modified: 2026-09-30
---

# 贾维斯中控（手机语音遥控电脑）

**是什么**：对手机说一句话，电脑替你办妥。手机＝语音遥控器（识别＋确认＋收结果），电脑＝可被指挥的执行体（Jev 路由 → 能力执行器矩阵）。2026-09-27 产品重定义：从"编码遥控"改成"语音控制电脑"。

| | |
|---|---|
| 文档真源 | `D:\Work\贾维斯中控\`（入口 `00-INDEX.md`，驾驶舱式编号目录 01-Product…09-Experiments） |
| 代码真源 | `D:\Remote-Coding-Control`（**2026-09-29 更名只改了 Obsidian 侧，代码仓未改名**，别去找 `Remote-Coding-Control` 之外的名字） |
| 当前阶段 | 重定义 / **M1 准备**（M1＝状态查询执行器，跑通"非编码语音控制"闭环）；`00-INDEX.md` front-matter `status: doing`、`milestone: redefine`、`updated: 2026-09-27` |
| 安全分档 | L0 免确认 / L1 手机确认 / L2 禁止，正文在 `01-Product\04-产品重定义-语音遥控电脑` 第四节 |
| 架构件 | `02-Architecture\`：01 系统架构、02 Windows-Companion、03 Mobile-PWA、04 Agent-Adapter、05 Session、06 Network-Security |

## 三条跨项目联合点（别的 Agent 最该知道的）

1. **依赖 API 转发网关**：意图路由打 `:3100/v1/jev`（结构化 choice/score/noul ＋ 置信度）。2026-09-27 实测"手机指令 → 网关 → 决策"已跑通。⇒ **网关是它的上游**，也是全系统最大单点盲区，见 [[调度大脑记忆/项目/project_relation_graph]]。
2. **公网入口＝阿里 99 ECS 上的 frps**：家宽没公网，手机靠这台机器中转；本机侧是 frpc ＋ companion。⇒ 动远程控制链路就是动那台机器的转发，见 [[调度大脑记忆/参考/reference_云服务器底座与跨项目联合点]]。
3. **执行体重活在本地 PC**：不在云上。⇒ "云端算力不够"一般不是它的瓶颈。

## 关键词（拿去 Work/代码仓定位用）

`贾维斯中控` `Codemote` `Remote-Coding-Control` `companion` `frpc` `frps` `Mobile-PWA` `Jev 路由` `能力执行器矩阵` `L0/L1/L2` `M1 状态查询`

## 已知的坑与未决

- **companion 有僵死前科** → "PC 常驻化加固（自启＋看门狗）"是 09-29 挂着的待点头项，见 [[调度大脑记忆/参考/reference_云服务器底座与跨项目联合点]] §五。
- **自启是三条通道、对应三条互斥链路**（2026-10-02 实测核出，同日整改）：① 计划任务 `\RemoteCodingControl`（Logon，郭永涛/Interactive）＝本地 8765 后端，**手机 App 默认走这条**（`mobile_app/lib/core/app_context.dart:11` 写死 `192.168.2.73:8765`）；② 计划任务 `\CodemoteFrpc`＝公网备用，`123.57.84.97:7000` 收 → 回投本地 8765（`frpc.toml`，`loginFailExit=false` 自带重连）；③ `HKCU\...\Run\RemoteCodingControlTunnel`＝USB 备用（`adb reverse tcp:8765`，只在插数据线时有用）。**判活一律按端口 8765，别按进程名/命令行。** 09-30 那次改前状态：①② 都用 CUI 程序当动作＝开机必弹黑窗，且**他一关窗就把服务杀死**（两任务 `LastTaskResult=0xC000013A`）。10-02 已改：①动作换成 uv base 真 GUI `pythonw.exe`＋`service_launcher_direct.pyw`；②改 `BootTrigger`＋`SYSTEM/ServiceAccount`（⚠️ 从此 SYSTEM 持有，普通 shell 关不掉）；③改指 `companion/run_hidden.vbs`。四处子进程 spawn 补了 `CREATE_NO_WINDOW`。**代码改动全部未 commit（HEAD 仍是 `066ffee`），且"下次真开机不弹"未经真开机验证**；全部判据与踩坑见 [[调度大脑记忆/教训/lesson_弹窗判定看PE子系统不看名字]]。
- **飞书中转（`app/feishu_relay.py`，09-28 新加、未入库）此前每 5 秒崩一次重连**（两条 `node event consume` 长连接），10-02 整改后两条消费者存活 711 秒以上不再重启；**病因没被单独隔离出来**（同一时刻改了两件事：creationflags 与启动器），要归因得一次只回退一项。
- 产品定位仍在 redefine：`00-INDEX.md` 的 `updated` 是 2026-09-27，**判"现在做到哪"必须开驾驶舱文件，别引用记忆**。

**How to apply:** 接这个项目先读 `00-INDEX.md` ＋ `07-Decisions\`（决策档按日期命名，服务器那篇是 [[调度大脑记忆/参考/reference_云服务器底座与跨项目联合点]] 的真源）。改网关路由/端点前先看它是不是这条链的上游。相关：[[调度大脑记忆/项目/project_ai_gateway]]、[[调度大脑记忆/流程/workflow_work库冷启动接手序]]
