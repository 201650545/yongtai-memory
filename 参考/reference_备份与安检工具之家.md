---
name: reference-备份与安检工具之家
description: 跨项目工具之家（12-工具归属 v1.3，2026-10-19 郭老师定由 D:\Work\工具 改名）：备份＝G-02 双轨归档 Track B 执行体（每天 01:00 传夸克网盘＋7 天 TTL 本地清扫）＋安全＝全库密钥扫描；约定＝跨项目/全系统脚本放 D:\Work\备份与安检\<用途>\＋README
metadata:
  node_type: memory
  type: 参考
  created: 2026-10-19
  Howtoapply: 动备份/清扫脚本或计划任务前先读它的 README；新跨项目工具按 12-工具归属 v1.3 放这里，别塞业务项目
type: reference
updated: 2026-10-19
kind: reference
status: active
---

# 备份与安检 · 跨项目工具之家

> 文档仓 `D:\Work\备份与安检`（**2026-10-19 前名 `D:\Work\工具`**，郭老师定改名，命名对齐库内描述式风格；改前先查引用——计划任务 action 与脚本内部都硬编码路径）。
> 归属规范：`D:\记忆\通用规范\12-工具归属.md` **v1.3**（跨项目/全系统脚本 → `D:\Work\备份与安检\<用途>\`＋README；**禁止寄生业务项目**，任务名不得带业务前缀）。

## 里面有什么

| 子目录 | 是什么 | 谁在跑 |
|---|---|---|
| `备份\` | **G-02 双轨归档 Track B 执行体**：Work 库＋记忆仓打 zip 传夸克网盘（当日/归档 两层，上传前幂等去重）；`cleanup_archives.ps1` 每天随跑 **7 天 TTL 本地清扫**（轮次记录/巡检日志/自检日志/草稿区/备份暂存，DryRun 的 localDeleted 是"将删"不是已删） | `Work_Backup_PackDaily` 每天 01:00；`Work_Backup_PackWeekly` 周日 01:30（2026-10-15 补挂并跑通首轮） |
| `安全\` | `secret-scan-all.py` 全库密钥扫描（push/发布前安检） | 手动 |

## 关键事实（2026-10-19 实测）

- **链路活着**：当天日志 `ok=True`——上传 A-记忆 5.08MB＋B-规范索引 到夸克网盘、归档 4 个旧包、本地清扫 7 个超期文件。
- **改名同步面（2026-10-19 全部已改）**：两个计划任务 action（导出 XML 换路径、原设置保留）、4 个脚本内部 16 处硬编码（**保持无 BOM UTF-8**——任务跑 Windows PowerShell 5.1，BOM 丢了中文路径变乱码）、元智能 `40_定时任务\registry.yaml` 7 处、ops-task-fleet 契约、通用规范 3 文件、ECF PROJECT_SPEC、`.gitignore` logs 规则。
- **此前是黑户**：从未登记 vault_registry，2026-10-19 补登（Home 子库一览 rows=14）。
- ⚠️ **与 `_backups` 不是一回事**：`_backups`（2026-10-19 已删）是历次手术的**手工**改前快照堆，不在清扫脚本名单里；这里是**自动**备份机制。另：`D:\Work\飞书` 是活跃子项目（Lark 数据接入），与已删的 `_归档\飞书` 旧表说明书同名不同物。

相关：[[参考/reference_handbook_ssot]]
