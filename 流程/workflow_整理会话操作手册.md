---
name: workflow-整理会话操作手册
description: 整理会话（settler）的操作手册：怎么读 _inbox 投递、判断归属、生成条目、重建索引与提交的固定流程。
type: workflow
updated: 2026-10-30
status: active
---

# 整理会话操作手册

> 版本 v1.0 · 2026-10-22 · 目标仓库 `D:\记忆`（母仓 `D:\Work`）
> 环境：Windows + **PowerShell 5.1（没有 pwsh，一律用 `powershell.exe`）** + Python（`python`，没有则 `py -3`）
> 手册里的命令可直接复制；尖括号 `<>` 是占位符，抄的时候换成真实名字。

## 一、这个手册解决什么

以前每次整理靠临场判断，现在把顺序固化成六步。照着做不需要判断，只做机械动作。

---

## 二、固定六步

### 步骤 1 · 体检（开工必跑，先于一切）

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\Work\_inbox\开工自检\preflight.ps1
```

- **成功判据**：最后一行打印"全 PASS"（后面可跟"（SKIP：…）"），进程退出码 `0`；简报落在 `D:\Work\_inbox\开工自检\简报_<时间戳>.md`。
- **失败怎么办**：有 FAIL 时退出码 `2`，输出形如"有 FAIL：编号引用断链"。**停下**，照简报"FAIL 明细"逐条修，修完重跑本步；**全 PASS 才准进第二步**。SKIP 不算失败（工具没做完 ≠ 坏了），不阻塞。
- 体检已含编号引用扫描（`scan_id_refs.py`，三态 ok/ambiguous/missing/unclear）。要单独看：`python "D:\Work\_inbox\引用扫描器\scan_id_refs.py"`（报告写到 `D:\Work\_inbox\引用扫描器\扫描结果.md`）。

### 步骤 2 · 清点（哪些任务目录待整理）

```powershell
python "D:\Work\_inbox\自动整理\tidy.py"
```

- **成功判据**：退出码 `0`，屏幕打印"目录总数：N  READY x / PAUSED y / STALE z"并列出 READY 清单；计划文件写到 `D:\Work\_inbox\自动整理\计划_<时间戳>.md`（这是本工具唯一写入点，`_inbox` 任务目录零改动）。
- **失败怎么办**：退出码 `2`＝参数错、`1`＝内部错误 → 停下看报错，原样重跑一次；仍失败就放弃本次整理，在交接里写明失败原因。
- **只处理 READY**：PAUSED（目录名含 `_work`，或文件命中 tmp/待 等草稿标记）本次一律不动；STALE（最新修改超过 7 天）不自动进计划，要整就人工点名后从步骤 3 起重走。

### 步骤 3 · 合规校验（不合规的不合并）

```powershell
python "D:\Work\_inbox\写入校验\validate_note.py" "D:\记忆\_inbox\<任务目录>"
```

逐个文件校验也行：`python "D:\Work\_inbox\写入校验\validate_note.py" "D:\记忆\_inbox\<任务目录>\<文件>.md"`

- **成功判据**：退出码 `0`，输出"共校验 N 个 / 通过 N 个 / 失败 0 个"。
- **失败怎么办**：退出码 `2`＝有不合格文件 → **不合格的那条不合并、不搬运**，退回写作者（附文件名、行号、缺哪个字段），其余合规的照常走步骤 4 起；退出码 `3`＝参数或路径错 → 停下改命令重跑。
- 口径：四字段 `kind` / `status` / `scope` / `requires`（定义见 `D:\记忆\通用规范\60-记忆条目字段规范.md`）；校验器要求 `status` ∈ active / superseded / archived / draft，`kind` 存在且非空，`scope` 空优于乱填，`requires` 只对 `kind: rule` 有意义。缺 scope/requires 可先跑 `python "D:\Work\_inbox\字段补齐\backfill_fields.py" --root "D:\记忆"` 看计划（默认 dry-run），确认无误再加 `--apply`。

### 步骤 4 · 发号（要新编号就用分配器）

```powershell
python "D:\Work\_inbox\编号分配器\id_alloc.py" alloc --type RULE --note "用途一句话"
```

类型只有五个：`RULE` / `IDEA` / `DEC` / `PIT` / `TERM`。台账 `D:\Work\_inbox\编号分配器\id_ledger.json`，退役号永不复用。

- **成功判据**：stdout 只打印一个编号（如 `RULE-016`），退出码 `0`。
- **失败怎么办**：退出码 `3`＝该前缀被黑名单 `occupied_prefixes.txt` 拦下（库内既有体系已占用）→ 换另一个类型重发，**不许改黑名单绕过**；退出码 `2`＝类型不认识或台账坏了；`1`＝台账读失败／抢锁失败（等 5 秒重试一次，仍失败就停下）。全部停下，不许手工编号顶上。
- 发完必须复查：

```powershell
python "D:\Work\_inbox\编号分配器\id_alloc.py" check
```

  **成功判据**：退出码 `0` 且输出"检查结果：没有重复号"。退出码 `2`＝有重复号／前缀冲突 → 按第四节处理，**不许合并成一个号**。
- 接管历史编号（首次接管旧库时用，默认 dry-run 只写报告）：`python "D:\Work\_inbox\编号分配器\import_legacy.py"`；确需写台账才加 `--apply`（会先备份 `id_ledger.json`）。

### 步骤 5 · 提交（唯一入口，逐路径单发）

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\小浣熊\mm-code\bin\obsidian-commit.ps1 -Repo "D:\记忆" -Paths "项目\某文件.md" -Message "整理：任务名 2026-10-22"
```

- 路径必须是**相对 `D:\记忆`** 的相对路径（绝对路径、越界路径、疑似 git 选项的路径，脚本直接拒绝）。
- **一次调用只传一个路径**：`powershell.exe -File` 方式下 `-Paths` 多值会被静默丢弃（实测）。多条路径就发多次调用，逐条核对返回码。
- **绝不能把多条路径塞成一个逗号串**（`-Paths "a.md,b.md"`）——那会提交 0 个文件却显示成功。
- 绝不使用 `git add -A`，绝不自己跑 `git commit` / `git push`。
- **成功判据**：每次调用退出码 `0`，且 `D:\小浣熊\mm-code\commit.log` 追加了本次记录。
- **失败怎么办**：退出码 `1`＝校验不过（路径不存在／越界／`-Paths` 为空／`-Message` 为空）→ 照 `commit.log` 的 ERROR 行改命令重来；退出码 `2`＝锁被占（另一个提交正在跑）→ 停下等它结束（锁超 10 分钟视为陈旧可强制接管），**不许改用 git 命令行绕过**；退出码 `0` 但提交 0 个文件（脚本记 nothing to commit）→ 停下核对路径，多半是路径写错或内容根本没变。
- 想先看将提交什么：同一条命令末尾加 `-DryRun`（只打印，不建锁、不写 git）。

### 步骤 6 · 归档 + 立即可查

**6a 搬运与清理**：把整理后的最终文件写进正式目录（`参考\` `项目\` `教训\` `反馈\` `流程\` `通用规范\`，按条目 `kind` 归位），提交成功后再清空对应的 `_inbox` 任务子目录：

```powershell
Remove-Item -LiteralPath "D:\记忆\_inbox\<任务目录>" -Recurse -Force
```

前置条件（缺一就不许删）：步骤 3 合规、步骤 4 号已发、步骤 5 提交成功判据全过。内容已内化就删原材料，不另建"原文归档"目录（依 `D:\记忆\通用规范\00-存档与内化.md`）。

**6b 立刻能查到**：

```powershell
python "D:\Work\_inbox\索引即时\index_one.py" --file "D:\记忆\项目\某文件.md" --apply
python "D:\Work\_inbox\索引即时\index_one.py" --verify "D:\记忆\项目\某文件.md"
```

- **成功判据**：第一条退出码 `0`（默认 dry-run，不加 `--apply` 只打印计划、不写库），第二条退出码 `0`（`3`＝不在索引里，`4`＝字段不完整）。
- **失败怎么办**：退出码 `2`＝停止条件命中 → 停下报告，不硬闯；`3` / `4` → 停下照报错补齐后重跑。
- 可选收尾（不影响上面六步）：`python "D:\Work\_inbox\夜巡\night_audit.py"`（7 项巡检，ERROR 退出码 `2`、只有 WARN 退出码 `1`）；`powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\小浣熊\mm-code\bin\cleanup.ps1`（默认 dry-run 只报告，真删加 `-Yes`）。

---

## 三、三条绝对不能做

1. **不许直接 `git add` / `git commit` / `git push`**。提交必须过 `obsidian-commit.ps1`：它抢独占锁 `D:\小浣熊\mm-code\.commit.lock` 保证单写者，绕过锁就会出现两个写者同时改同一批文件。
2. **不许自己编编号**。必须由 `id_alloc.py alloc` 发号：它用原子锁保证不撞号、退役号不复用；自己编的号不进台账，撞了没人知道，检索时会指向两处。
3. **不许自动合并内容**。`tidy.py` 只清点、只列清单，不合并；"哪条重复、哪条该并"必须由整理会话逐条看过再决定。自动合并会静默丢内容且不可回滚。

## 四、冲突怎么处理

| 情况 | 确定动作 |
| --- | --- |
| 两条笔记讲同一件事 | **不覆盖任何一条**。新建 `冲突-<主题>.md` 放 `D:\记忆\_inbox\`，正文写清双方出处（两个文件路径）与分歧点；两条原文都原样保留 |
| 编号撞了 | `python "D:\Work\_inbox\编号分配器\id_alloc.py" check` 报重复号（退出码 2）后按 `ambiguous` 处理：**不许合并成一个号**，不删任何一条；跑 `python "D:\Work\_inbox\编号分配器\import_legacy.py"` 重新判定该号是 active 还是 ambiguous（默认 dry-run），确认后加 `--apply` 写台账；按 `冲突-<主题>.md` 留证 |
| 校验不通过 | 不合并、不搬运，退回写作者；附文件名、行号、缺哪个字段，等改好再回步骤 3 |
| 提交失败 | 停下看 `obsidian-commit.ps1` 的输出与 `D:\小浣熊\mm-code\commit.log`，按第五步的失败分支处理；**不许改用 git 命令行绕过** |

## 五、每步的验收判据（可判定清单）

- 步骤 1：`preflight.ps1` 退出码 `0` 且输出"全 PASS"。
- 步骤 2：`tidy.py` 退出码 `0`，`计划_<时间戳>.md` 已生成，READY 清单已圈定；PAUSED 目录零改动。
- 步骤 3：对每个待合并文件 `validate_note.py` 退出码 `0`（不合规的已单列退回）。
- 步骤 4：`alloc` 退出码 `0`、stdout 恰好一个新编号；`check` 退出码 `0` 且输出"没有重复号"。
- 步骤 5：每次 `obsidian-commit.ps1` 调用退出码 `0`；**紧接该次调用**执行 `git -c core.quotePath=false show --name-only HEAD`，本批次文件行数 = 传入路径数（一次传一条时 = 1）。
- 步骤 6：`Test-Path "D:\记忆\_inbox\<任务目录>"` 返回 `False`（已清空/归档），正式目录里对应文件存在；`index_one.py --apply` 退出码 `0`，`--verify` 退出码 `0`，且用本地知识引擎检索该文件标题关键词能命中。

## 六、常见误操作与后果（真实事故）

1. **备份存成了"改后内容"** → 以为留了退路，真出事时回滚回来的还是改后的内容，回滚等于没做。备份必须是改之前的副本。
2. **备份目录丢了 `components\` 这一层** → 恢复出来的是错误目录结构，文件散在各处，看着像恢复成功其实全错位。恢复后先比对目录层级再采信。
3. **`-Paths` 传逗号串**（`-Paths "a.md,b.md"`）→ 实际提交 0 个文件，脚本还记 nothing to commit 退出 0，看着像成功，内容根本没进库。一次只传一个路径。
4. **两个 agent 并发改同一批文件** → 互相覆盖，git 里留下半截文件，还查不出谁改的。提交走 `obsidian-commit.ps1`（有锁）；同一批文件只让一个会话碰。
5. **把 `ambiguous` 全判成 FAIL** → 报警疲劳，真 FAIL 被淹没，真出事时没人看。`ambiguous` 是"疑似"，单独归一类人工看，不并进 FAIL。
6. **仓库里已有 `D-001`，与新发号器撞号** → 同一个号指两处，引用时不知道说的是哪个。`D-001` 属旧单字母体系，整理时看到 `D-xxx` 一律不新发、不合并；要发号只用整词前缀 `RULE/IDEA/DEC/PIT/TERM`，并把该前缀登记进 `occupied_prefixes.txt` 停用。
7. **以为 `_inbox` 里的文件会进 git** → `D:\记忆\_inbox` 已被 `.gitignore` 忽略，git 只收结论。文件必须先搬运到正式目录再提交。
8. **跳过步骤 5 直接删 `_inbox` 任务子目录** → 内容既没进库也没归档，净损失。删除只在步骤 5 验收通过后执行。