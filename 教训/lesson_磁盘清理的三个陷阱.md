---
name: lesson-磁盘清理的三个陷阱
description: 2026-10-20 全盘清理实战沉淀：①C 盘用户目录下 30 个目录是 junction 指向 D 盘，按路径算体积会严重高估 C 盘真实占用②Windows 回收站批量回收大目录会抛"This function is not supported on this system"，必须降级为逐文件回收③清空回收站只有 SHEmptyRecycleBin API 可靠，Clear-RecycleBin -DriveLetter 会报"cannot find the path specified"，Shell.Application 的 InvokeVerb 在非交互会话里根本不存在
type: lesson
updated: 2026-10-20
---

# 磁盘清理的三个陷阱

2026-10-20 郭老师要求"找 C 盘 D 盘垃圾、保持空间充足"，实操两小时沉淀。

## 陷阱一：C 盘目录是 junction，体积判断会骗人

`C:\Users\郭永涛` 下 **30 个目录是 junction**（指向 D 盘），`AppData\Local` 与 `AppData\Roaming` 下还有 **20 个**。

| 看到的路径 | 实际落点 |
|---|---|
| `.gradle` `.workbuddy` `.qoder` `.qoder-cn` `.cache` `.gemini` `.openclaw-autoclaw` `.codeartsdoer` `.trae` `.claude` `.bun` `.local` | `D:\C盘迁移\User\*` |
| `AppData\Local\Google` | `D:\AppData_Relocation\Google` |
| `AppData\Local\Doubao` | `D:\C盘迁移\Doubao\Doubao` |
| `AppData\Local\Pub` `uv` `node-gyp` | `D:\C盘迁移\Cache\*` |
| `AppData\Roaming\npm-cache` | `D:\C盘迁移\Cache\npm-cache` |
| `AppData\Roaming\npm` `Kingsoft` `Trae` `Trae CN` `Tencent` `Open Design` `rod` `Antigravity` | `D:\AppData_Move\*` |

**判据**：量一个用户目录前，先 `Get-Item $p -Force | % Target` 看是否 ReparsePoint。
**后果**：不判就删，会把 junction 本身删掉、C 盘路径变悬空链接、应用直接起不来。正确做法是**删 junction 指向的 D 盘真实目录**，删完再 `New-Item` 重建空目录，让 junction 不悬空。
**另一面**：清 C 盘路径其实释放的是 D 盘空间——报收益时必须按真实落点归盘，不然会告诉用户"C 盘多出 15G"而实际是 D 盘。

## 陷阱二：回收站批量回收大目录必失败

`Microsoft.VisualBasic.FileIO.FileSystem::DeleteDirectory(..., SendToRecycleBin)` 对**大目录整体**回收会抛
`"This function is not supported on this system"`，`AppData\Local\Temp` 则是 `"The system call level is not correct"`。

**不是长路径问题**——实测把 `D:\C盘迁移\User\.qoder\logs` 整体移到 `D:\_zz2`（仅为缩短路径的临时中转目录，收尾时已删除）缩短路径后，回收**依旧失败**；
而对其中**单个文件**调 `DeleteFile` 立刻成功。

**正确姿势（已验证）**：整树回收失败后，改成枚举全部文件**逐个 `DeleteFile` 进回收站**，再按路径长度倒序 `Remove-Item` 清空目录树。
本次 141542 个文件的 D 盘回收站就是靠这个清完的。

**代价**：逐文件回收很慢（实测约 130 文件/秒），141542 个文件耗时 ~18 分钟，必须放后台跑。

## 陷阱三：清空回收站只有一条路能走

| 方式 | 结果 |
|---|---|
| `Clear-RecycleBin -DriveLetter C,D -Force` | ❌ 抛 `The system cannot find the path specified` |
| `$sh.Namespace(10).InvokeVerb('delete')` | ❌ `System.__ComObject does not contain a method named 'InvokeVerb'`（非交互会话里没有 InvokeVerb） |
| `SHEmptyRecycleBin(NULL, NULL, SHERB_NOCONFIRMATION\|NOPROGRESSUI\|NOSOUND)` | ✅ 返回 0 |

`SHEmptyRecycleBin` 传 `NULL` 根路径会一次清空**所有盘**；随后再单独传 `C:\` `D:\` 会返回 `-2147418113`（DISP_E_EXCEPTION），
**这是正常的**——第一次已经清空了，不是失败。判断成败要看最终 `$Recycle.Bin` 的实际文件数，不要看返回码。

## 附带：其他有用判据

- 删大目录前先查**在跑的进程**（`Get-Process | ? ProcessName -match 'chrome|wps|qoder'`）。Chrome/WPS 正在运行时缓存文件被占用，只能跳过，等退出后再补清。
- `Get-ChildItem -Recurse` 在 D 盘（207G / 几十万文件）能跑 20 分钟不出结果，**必须换 `[System.IO.Directory]::EnumerateFiles($p,'*',[System.IO.SearchOption]::AllDirectories)`**，快一个数量级。
- 清完空目录壳要 `New-Item -ItemType Directory` 重建，否则 junction 悬空。
- 回收站**不占释放**——同卷搬进回收站不腾空间，**必须清空回收站**才真正还空间（本次 26.5G 进了回收站，清空后 C +11.6G / D +16.9G）。
- **`SHEmptyRecycleBin` 是同步阻塞调用**：清 15.2 万个文件耗时约 12 分钟（≈210 文件/秒）。
  **脚本进程退出 ≠ 清空完成**——实测脚本 02:33 就退出了，回收站还在继续降，判断成败必须以
  `$Recycle.Bin` 的实际文件数为准，不要看返回码、也不要只看进程是否还在。
- **回收速率参考**：整树回收 ≈130 文件/秒；永久清空 ≈210 文件/秒。**10 万级文件的目录一律要放后台跑**。
- **`node_modules` 是纯依赖缓存**，可当缓存清（`npm install` 可重建），而同目录下的 `src/`、`package.json`、
  文档必须保留——「清缓存」时按**子目录**切，不要整目录清，否则会连源码一起删。

**关联**：`D:\记忆\项目清单\projects.yaml` 无对应项目；本条为系统级运维教训，与项目无关。
