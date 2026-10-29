---
name: reference-句读字幕与听页治理交接_20261027
description: 句读/Phrasing 项目 2026-10-25～10-27 三晚治理的交接总结：字幕深浅、音轴重对齐、音源合规、响度归一、听读页版式、产线机器闸六项已完成的改动与验收数；两台手机的课包对齐现状；以及服务器发布未通、欠账与待拍板清单。
type: reference
updated: 2026-10-29
status: active
kind: fact
---

# 句读字幕与听页治理 · 交接总结（2026-10-27）

> 本件是**交接件**，不是流水账。每条事实后面都带出处文件；核不出来的数字写「未取到」，不写印象。
> 真源根目录：`D:\dss-work4\logs\`；代码仓 `D:\listenloop`；技能库 `D:\Work\元智能\10_AI自成长引擎\技能库\phrasing-course-pipeline\`。
> 术语约定：首次出现的行话后面跟一句大白话（例：**句首预卷（pre-roll）＝切的时候提前留半秒到一秒，别把人家第一个字切掉**）。

---

## 0. 一句话现状

字幕「由浅到深」乱掉的根因已定位并修完；两台手机的课包已与本地发布源对齐（**实质混装 0**）；听读页版式按郭老师要求重排并已装包；产线规矩已落库并做成**机器闸**。**唯一卡点是服务器发布通道（SSH）不通 ⇒ 所有改动只在你手机与本地，线上仍是旧包。**

---

## 1. 下一位先看这三条事实

1. **APK 不含课包**：`pubspec.yaml` 的 `assets:` 段里**没有** `- assets/lessons/` ⇒ 课包是**发布源**（发布服务器），设备上的课要单独推 ⇒ **改完本地 ≠ 手机上生效**（今晚反复踩）。
   - 出处：`D:\listenloop\pubspec.yaml`（实测 grep：assets 段只有 `assets/fonts/`、`assets/data/`、`assets/theme/`、`assets/brand/`）；`D:\dss-work4\logs\apk_fix_20261026\fix_report.md` §1.3。
2. **手机曾大面积混装**：小米 14 一致 **25** / 混装 **153**（另有缺件 6、本地无对应 80，合计 264）；小米 10 Ultra 一致 **17** / 混装 **92**（缺件 0，合计 111）。根因＝判重拿**侧车清单里"声明"的 sha256**，而侧车在换包/推包时不更新 ⇒ 永远判"没变" ⇒ 旧课永不覆盖（已修，见 §3.5 / §3.6）。
   - 出处：`D:\dss-work4\logs\phone_consistency_20261026\consistency_report.md` §一；`…\device_95a8fd5_mi10ultra\consistency_report.md` §一；根因：`D:\dss-work4\logs\overwrite_sync_20261026\overwrite_report.md` §1.3。
3. **服务器仍是旧包** ⇒ **在 App 里点「同步 / 刷新课程库」会把设备上的新内容覆盖回旧版**（发布前禁止）。
   - 机制：新装的 App 带「**App 漂移即覆盖**」规则（设备侧课文件与导入指纹不符 ⇒ 自动用导入包覆盖），而服务器上现在还是旧包 ⇒ 旧包会把刚推上去的新内容盖回去。
   - 出处：`D:\dss-work4\logs\apk_build2_20261026\apk_report2.md`（🚨 提示段）；`D:\dss-work4\logs\apk_fix_20261026\fix_report.md` §④。

---

## 2. 设备现状

| 设备 | serial | 机型 / 代号 | 系统 | 课目录数 | APK 字节 / sha256 | 版本 | 课包对齐（最近一次全量复检） | 备注 |
|---|---|---|---|---|---|---|---|---|
| 小米 14 Ultra | `bf6ef967` | 23127PN0CC / `houji` | Android 16（SDK 36） | **264** | 164,011,430 B / `3f32a0b85397ed0d9665f06969f3a95a4217ecabfedff2238bd2941a800e1df6` | versionCode 4030 / versionName 0.9.3（**未升版**） | 复检 2026-10-27 01:05：一致 **179** / 混装 **1** / 缺件 **4** / 对不上 **80** ＝ 264；**实质混装 0** | 混装那 1 条是残留备份目录 `niuduzi-b-dual.bak_20261014_232420`（非业务课）；APK 装机时刻 2026-10-27 00:55:32 |
| 小米 10 Ultra | `95a8fd5` | M2007J1SC / `cas` | Android 13（SDK 33） | **113** | 164,011,430 B / `3f32a0b8…1df6`（同一包） | 4030 / 0.9.3（**未升版**） | 复检 2026-10-26 17:22（口径 2）：一致 **78** / 混装 **32** / 缺件 **0** / 对不上 **2** ＋ 备份目录 1 ＝ 113；**实质混装 0** | 屏幕 1080×2340 @440dpi ＝ **393×851 dp**（版式重排的验证对象）；32 条混装全是 C 类（仅音频重编码、时长相同）；APK 装机时刻 2026-10-26 16:33:57 |

- 出处：小米 14 行＝`D:\dss-work4\logs\resync_mi14_20261027\report.md` §①/§②/§④ ＋ `recheck.json`；小米 10 Ultra 行＝`D:\dss-work4\logs\device_switch_20261026\switch_report.md`（Android 13 / SDK 33）、`D:\dss-work4\logs\apk_fix_20261026\fix_report.md` §3.1（APK 三项数）、`D:\dss-work4\logs\final_push_ledger_20261026\final_report.md` §3.2（113 目录复检）、`D:\dss-work4\logs\listen_align_20261026\align_report.md`（393×851 dp）。
- 说明：**113 / 264 目录里各含 1 个 `.bak_` 备份目录**（见 §5.3），业务课分别 112 / 263 门。

**两机共同事实（不用再查）**

- 两台跑的是**同一个包**：164,011,430 B / `3f32a0b8…1df6`，versionCode 4030 / versionName 0.9.3，**全程未升版**（`pubspec.yaml` 仍是 `0.9.3+4030`）。
- 两台都只走 **USB**（小米 14 `transport_id:6`；小米 10 Ultra `transport_id:1`），**全程未用 `adb connect` 无线地址**。
- 两台的 App 都是 **debug 包** ⇒ 装包必须 `--debug`（见 §6.4）。
- 两台的学习数据（`listenloop.db`）在装包前后**字节数未变**（小米 10 Ultra 655,360 B ＋ journal 512 B）。
- 装机口径：**不卸载、不 `pm clear`、不删 databases**，只做 `install -r` 覆盖（`firstInstallTime` 不变）。

---

## 3. 已完成的改动

### 3.1 字幕深浅（UI 层把 -1 归一成 null）

- **做了什么**：模型层 `activeCharIndexAt` 在没有逐字戳时返回 **-1**（既有契约，不许改）；字级排版 `chinese_textbook_ruby_layout.dart:254-265` **只认 null** ⇒ -1 被当成"前沿 0" ⇒ 当前句整句落进未读档 0.35 ⇒ **每翻一句整句明暗反转**。修复在 **UI 层**归一：新增 `charDepthIndex(raw) => (raw == null || raw < 0) ? null : raw`，单句页 `sentence_display.dart:112-114`、流转页 `sentence_page_list.dart:1135-1141` 用同一把尺；词级光标只管位置（底色＋下划线），不再抢字色。**模型层一个字没动。**
- **验收数**：测试 **18/18 全绿**（monotonic 13 ＋ invariant 5）；三个回归文件 **30/30 全绿**；退回实验 **9 红 9 绿**；当前句墨色亮度 L **189.50 → 111.29**（Δ −78.21），左右两行 152.04 前后不变；逐像素差异 **4455** 个，包围盒只落在当前句那一行（x[56..503]、y[451..481]）。
- **评分**：**9.8 / 10**（独立第三方，合格线 8.0）
- **证据**：`D:\dss-work4\logs\subtitle_depth_fix\report.md`、`…\scorecard.md`、`…\green_both_after_restore.txt`、`…\preview\after_measure.txt`

### 3.2 音轴重对齐（离线 ASR 真戳，不均摊）

- **做了什么**：离线 ASR（sherpa-onnx ＋ 本地 zipformer CTC 模型，**0 次联网**）拿原生真戳 ＋ 拼音键二次校正，重写字级时间轴；字戳**只向后**吸附进静音、**绝不前移**；句首按"起音前 0.5~1s"预卷并钳制"不咬上一句尾音"；初读轨与熟读轨同步重算。
- **验收数**：
  - 《黄山奇石》：切点**晚于起音**的句子 **36/55 → 0/55**（最大差值 +5180ms → −60ms，余量 60~940ms、中位 380ms）。
  - 《寒号鸟》：「风」字动画比人声早 **+941ms → 0ms**（B 提前量中位 −121→0，最大 1679→0）。
  - 《语文园地五》（一上 `yuandi5_a1`）：**43/71 句（60.56%）晚于起音 → 0 句**；熟读 35 句无戳 → 37 句全有逐字戳；有人声无字幕 27 → 0。
  - 第一批 **8 门真人原声课**：落静音字数 **2187 → 0~126 字/条**（7 条 ≤8 字，`kuailexiaohe` 126 字）；切分门禁 **1 FAIL → 0 FAIL**；音频 `audio.m4a` **一个字节没动**（逐条 sha256 一致）。

  第二批 5 门课逐条验收（初读轨，A＝句首余量中位、B＝字戳提前量、E＝句轴覆盖率）：

  | 包 | A 余量中位（前→后） | B 提前量中位（前→后） | E 有人声无字幕字数（前→后） | 三硬阈值 |
  |---|---|---|---|---|
  | `hanhaoniao`（寒号鸟） | −141→**839** / −121→**1000** | −121→**0**（最大 1679→0） | 64→**0** | 部分达（熟读落静音 7.4%） |
  | `zuojingguantian`（坐井观天） | −61→**909** / −21→**1000** | −151→**0** | 10→**0** | **全达** |
  | `hulu`（我要的是葫芦） | −101→**859** / −100→**1000** | −21→**0** | 37→**0** | 未达（voiced 0.690 < 0.75） |
  | `yuandi5_a1`（语文园地五·一上） | −100→**1000** | −95→**0**（最大 3720→0） | 27→**0** | **全达** |
  | `yuandi5_shizi`（园地五 识字加油站） | −31→**1000** | 0→**0** | 7→**0** | **全达** |
  | `yuandi5_zici`（园地五 字词句运用） | −1→**1000** | −1→**0** | 21→**0** | **全达** |
  | `yuandi5_mingyan`（园地五 勤学名言） | −21→**57** / −21→**510** | 0→**0** | 9→**0** | 部分达（余量只有 57ms，见 §5.9） |
  | `huangshanqishi`（黄山奇石） | — | — | — | **只确认未改**（sha256 与 `075a4413…` 一致） |

  > 三硬阈值＝落静音 ≤5% ／ 静音点亮字 = 0 ／ voiced ≥ 0.75；`hulu` 是本批最差课。
- **评分**：**未取到**（本段无 `scorecard_*.md`）
- **证据**：`D:\dss-work4\logs\huangshan_fix_20261025\huangshan_report.md`、`…\realign_20261025\realign_report.md`、`…\realign_batch2_20261026\realign_batch2_report.md`、`…\quality_probe_20261025\probe_findings.md`（「风」941ms 的原始测法）
- 口径提醒：任务书里写的「苹果 8 条」这个说法在任何报告里都查不到（**未取到**）；按真源此处是「第一批 8 门真人原声课」。

### 3.3 音源合规（钦定两位 = 林鹿鸣 + SeaverThomsen）

- **做了什么**：把钦定 UP 主**定为两位**（热爱语文的林鹿鸣老师 ＋ SeaverThomsen），`song想有只猫`（mid 15610131）**移出白名单**；二上 60 条逐条定性判定（v2 表，只定性不改包）；活脚本 `D:\listenloop\tool\yuandi38_fetch_bili.py` 的白名单由三家收为两位；另把 8 条 TTS 音轨**回退成真人原声**（8 条全部对上"换版前"的 sha256/bytes）。
- **验收数**：二上 60 条＝钦定两位 6（真人 1 ＋ 合成 5）／非钦定 23／查不到出处 27／另有 4 条合成音无 bvid 无 owner；判定码 A=1 / C=23 / D=9 / E=3 / F=24。白名单只读验证：**林鹿鸣＝放行 / SeaverThomsen＝放行 / song想有只猫＝拒绝（PASS）**；活放行口**只剩 1 处**（`tool\` 里那个脚本），`pipeline\` 侧 grep **零命中**。全仓 `song想有只猫` 命中 16 处 / 8 个文件 → 已订正 2 / 事实引用 8 / 历史留痕 6 / 待拍板 0；文档侧 4 处 ＋ 脚本侧 1 处 ＝ **5 处全部处置**。
- **评分**：交付 1（TTS→真人回退）**8.80 / 10**；交付 2（60 条定性表 v2）**8.90 / 10**（两个交付均 ≥8.0，必改项 0 条）
- **证据**：`D:\dss-work4\logs\audio_source_audit\verdict\verdict_60.md`、`…\revert_tts_20261025\revert_report.md` ＋ `scorecard_assets.md`、`…\policy_tidy2_20261026\tidy2_report.md`

### 3.4 响度（归一到全库中位 −17.3 LUFS）

- **做了什么**：先只读体检全库 **259** 个包测 I（EBU R128 积分响度，ffmpeg `ebur128=peak=true`）；目标＝**全库中位**（259 条升序取第 130 个）＝ **−17.3 LUFS**；圈定四档（过轻 12／偏轻 16／偏响 39／过响 8 ＝ 75）→ 排除 5 → 处理 70 → **实改包 65**；滤镜只有 `volume=<gain>dB:precision=float` 一个，**同 codec / 同采样率 / 同声道**重编，真峰值压到 ≤ −1 dBFS（实操 −1.1），码率按需上调以保 **|r| ≥ 0.999**。
- **验收数**：**259/259 测到**（未取到 0 条）；65 条改包 → **53 条** I 落在目标 ±1 dB 内，**12 条**因真峰值受限未达标（逐条点名）；**|r| 最小 0.999238**；**时长一帧不差**（解码样本数之差 ≤ 1）；包体 87.9 MB → 180.8 MB（+93 MB，+106%）；未处理上游判定「正常」**178 条**与「样本不足」6 条（见 §5.6）。
- **评分**：**未取到**（本段无 `scorecard_*.md`）
- **证据**：`D:\dss-work4\logs\loudness_audit_20261026\loudness_report.md`、`…\loudness_normalize_20261026\normalize_report.md`

### 3.5 UI（听读页版式重排 ＋ 壁纸全局 ＋ 漂移即覆盖）

- **做了什么**：
  1. **听读页版式重排**（郭老师五条诉求全部落地）：① 课文标题居中 ② 计数件移到"上方组件的中间"（两个子页落点一致）③ 行号移到文字块正上方并居中 ④ 新增「**文本呈现形式**」两档（默认**居中**），统一驱动标题 / 计数件 / 行号 / 正文 ⑤ 徽标（合成音 / 音频待补）从标题行右侧挪到 meta 行右端 —— 不挪的话徽标会把标题挤偏约半个徽标宽（≈65dp），三者就不再同轴。
  2. **壁纸全局化**：自定义壁纸（含主题"背景图"档位）在听页 / 读页都生效，衬底 alpha **0.78**。
  3. **App 漂移即覆盖**：判重改用**设备侧实算 sha256**，不再信清单声明值；同时给 catalog 侧补 sha256。
  4. 目录改**手风琴**（任一时刻最多一个单元展开）；流转页标题栏钉顶、纯标题段不再渲染（报告记 110 课 / 114 段被跳过，时间轴 / 高亮 / 计数件未动；评分员复算为 111/115，差异因 `shuxingxing_b_dual` 在 23:45 被并行任务重打，非实现错误）、meta 行只剩总时长；一条与新设计互斥的旧断言改写成 6 条新判据。
- **验收数**：目标设备 = 小米 10 Ultra **393×851 dp**；golden 只更新指定的那 3 张；壁纸 3 张 golden sha256 前后完全一致 ＋ 受影响面测试 **34 文件 / 192 条全绿**；第二批 UI 相关测试 **174 条全绿**、`flutter analyze --no-pub lib test` **error = 0**。
- **评分**：`listen_layout_20261025\scorecard_ui.md` —— 交付 1 目录手风琴 **8.4**、交付 2 第二批 UI **9.0**、交付 3 APK 构建与装机 **9.0**，**三项合计 26.4 / 30**，均 ≥8.0 通过。**2026-10-26 的版式重排与壁纸全局化这两批没有评分卡 ⇒ 评分未取到。**
- **证据**：`D:\dss-work4\logs\listen_align_20261026\align_report.md`、`…\assert_fix_20261026\assert_fix_report.md`、`…\listen_layout_20261025\accordion_change.md`、`…\batch2_report.md`、`…\wallpaper_global_20261025\wallpaper_report.md`、`…\overwrite_sync_20261026\overwrite_report.md`

### 3.6 产线规矩与机器闸

- **做了什么**：
  1. **句首预卷铁律落库**：切分侧 `phrasing-lesson-segmentation` 新增**铁律 5**、制课侧 `phrasing-lesson-build` 新增**铁律七**（＋ 六道自查、混装对账）；5 个要点全部落成条款，grep 自查 **5/5**，`.history` 快照 sha256 与改前逐一相同。
  2. **新工具** `D:\listenloop\tool\verify_cut_lead.py`（只读课包自身 JSON，**不联网 / 不调 ASR / 不解码音频**）：切点晚于起音 ⇒ 硬失败；区间重叠/倒挂 ⇒ 硬失败；预卷余量 < 500ms ⇒ **只告警不判失败**（连续朗读时物理上给不足，宁可少给也不咬掉上一句的尾音）；假时间轴（`endMs-startMs < 实义字数×60ms`）⇒ 硬失败；包里没逐字戳 ⇒ 判「未取到」放行。
  3. **挂机器闸**：`pipeline\gatekeeper.py` 的**第 5 项**检查，卡口红灯 ⇒ 构建立即以**退出码 3** 失败，不进入入库/发布；原 1~4 项输出逐行一致。
  4. **台账全量重算**（`lessons_asset_manifest.json`，259 行）。
- **验收数**：工具目录模式跑 259 包 → **FAIL 117 / PASS 140 / 未取到 2**；好包 **3/3 退出码 0**（硬失败 0 句，黄石包余量中位 700ms / 最小 40ms / 最大 940ms）；坏包 8 个里 **7 个退出码 1**（命中 5~26 句）。台账：**总行 259，被改 74 行**、未改 185 行；差异 148 行 = 74 行 × 2 字段（`bytes`/`sha256`）；`diff_lines_outside_bytes_sha256 = 0`、`assert_rowset_equal = True`；孤儿行 / 孤儿包清单 ②③ 均 **0 条**。
- **评分**：**未取到**（本段无 `scorecard_*.md`）
- **证据**：`D:\dss-work4\logs\skill_rule_20261026\skill_rule_report.md`、`…\cut_lead_gate_20261026\gate_report.md`（＋ `run_verification.py`、`verification_results.json`）、`…\final_push_ledger_20261026\final_report.md` §2；技能库正文 `D:\Work\元智能\10_AI自成长引擎\技能库\phrasing-course-pipeline\components\phrasing-lesson-segmentation\SKILL.md`、`…\phrasing-lesson-build\SKILL.md`

---

## 4. 定下来的口径（**不要改**；改了要回写本文件）

| # | 口径 | 出处 |
|---|---|---|
| 1 | **钦定两位** ＝ 热爱语文的林鹿鸣老师 ＋ SeaverThomsen；`song想有只猫` 不在钦定之列 | `verdict_60.md` 口径段、`policy_tidy2_20261026\tidy2_report.md` |
| 2 | **句首预卷（pre-roll）0.5~1s 且绝不截断上一句字尾**（连续朗读时允许小到 60ms）⇒ 宁可预卷小，也不丢字 | `phrasing-lesson-segmentation\SKILL.md` 铁律 5、`phrasing-lesson-build\SKILL.md` 铁律七 |
| 3 | **字戳只向后吸附进静音（≤600ms），绝不前移** | `realign_batch2_20261026\realign_batch2_report.md` §2 |
| 4 | **响度目标＝全库中位 −17.3 LUFS**（259 条升序第 130 个），真峰值 ≤ −1 dBFS | `loudness_normalize_20261026\normalize_report.md` §2、§4 |
| 5 | **混装四类判定口径**：一致 / 混装 / 缺件 / 对不上；混装再分**实质**与非实质（仅格式 / 合并口径 / 仅音频重编码）；**四类合计必须 = 课目录数** | `resync_verify_20261026\verify_report.md` §2、`final_push_ledger_20261026\final_report.md` §3.2 |
| 6 | **App 漂移判据＝设备侧实算 sha256**（不信清单声明值） | `overwrite_sync_20261026\overwrite_report.md` §2.1 |

---

## 5. 未完成 / 待郭老师拍板

> **这一节全是没做完的，不许读成"已完成"。**

| # | 事项 | 卡在哪 | 需要谁点头 | 建议 |
|---|---|---|---|---|
| 1 | **服务器发布（SSH）不通** | SSH 通道断，`publish_update.ps1` 没执行 ⇒ 新包没上线，线上仍是旧包 | 郭老师开通道 / 给可达路径 | 先确认服务器可达再发布；**发布前 App 里一律不点「同步 / 刷新课程库」**（§1.3） |
| 2 | **设备侧 9 个残留文件**（小米 14：6 个旧 `audio.m4a` ＋ 3 个 `provenance.json`） | 旧 `audio.m4a` 未被引用（manifest 的 `audioFile` 已指向新的 `audio.mp3`），但不确认是否还有别处引用 | 郭老师点头才删 | 建议**先不动**，等服务器发布后随重推一并清 |
| 3 | **1 个 `.bak_` 残留目录**（`niuduzi-b-dual.bak_20261014_232420`） | 规矩是"不删 `.bak_`" | 郭老师 | 建议保留；代价是复检残留混装 1 条 |
| 4 | **80 门「手机有本地无」**（小米 14） | 手机侧有该 lessonId，本地 259 个包里没有对应包 | 郭老师定要不要补做本地包 | 先列出补做清单再动手 |
| 5 | **151 / 76 门「本地有手机无」**（小米 10 Ultra 151 / 小米 14 76） | 多数是**命名口径差**（设备侧 `g5a-*-dual` vs 本地包 lessonId `g5a-*-b-dual`），不是丢课 | 郭老师定要不要补推 | 先按 lessonId 对齐口径，不要按文件名硬配 |
| 6 | **178 条要不要也归一（响度）** | 审计判定「正常」的 178 条本轮没处理（只处理四档 75 条） | 郭老师 | **建议否** —— 已在目标带内，再动就多一代有损编码 |
| 7 | **C 类（仅音频重编码）要不要覆盖手机原版** | 门数口径差：`resync_verify`（2026-10-26 14:0x）记 **15 条**、`final_push_ledger`（17:22）记 **17 条**；两轮都是「时长相同、仅字节不同」 | 郭老师 | **建议否** —— 按工单一律不覆盖，保手机侧原版 |
| 8 | **3 条重做课的 2 项继承缺陷**（`yuandi5` 初读 **6 行 3 纯字** ／ `g3a`+`g4a` **fake_punct 8**） | 6 行按含标点是 4 字符（符合工单 4~8），按 gatekeeper"纯字"口径不达 4 字下限，**原包基线同样不合规**；`fake_punct` 是初读行尾有标点、熟读轨同句没有 —— 修它都要改文本 / 切分行结构 | 郭老师单独授权 | 建议：熟读轨补回句末标点（属"改文本"），先单课试点 |
| 9 | **「勤学名言」4 字任何钦定源都没念** | 钦定源全集枚举后**无**这条；老师念完"日积月累"有 **2.28 s 数字静音**（源 210.440–212.760 s，标题卡留白），原包 3 个假字戳正落在这段静音里。现做法：该行**不造字戳**（`charStarts: null`），App 走整句高亮 | 郭老师定**裁片策略** | 建议：要么维持现状（不造戳），要么另找一条真念到这 4 个字的钦定源（目前**未取到**），不许用非钦定源顶替 |
| 10 | **记忆库写入授权** | 本件只落 `_inbox`，**未写 `D:\记忆` 正文** | 郭老师 | 郭老师偏好：交付时要带术语解释 —— 本件已按此写 |

**拍板顺序建议（一次只推进一件，别一口气全做）**

1. **先解决 #1 服务器发布** —— 它一通，#2 / #4 / #5 三条欠账才好一起收；其余都可以先放着。
2. #2（残留文件）与 #3（`.bak_` 目录）**可以等 #1 之后一并清**，不必单独决策。
3. #4 / #5 是**口径问题不是能力问题**：先把两侧 lessonId 清单对齐成一张表，再决定推不推。
4. #6（178 条归一）**建议直接否**，不需要开会。
5. #7 / #8 / #9 都要**改内容**（音频 / 文本 / 裁片），属于"要郭老师点头"那一类，先出一页对比表再谈。

---

## 6. 给下一位的操作指引

### 6.1 铺包正确做法

- **整目录备份做一次**：`adb exec-out run-as com.phrasing.phrasing tar -cf - app_flutter/lessons > backup.tar`（本轮实测：541,048,832 B / tar 内 1699 文件 / sha256 `DB0496B189BD2B7BBA004FD03EEEB5D320A91551CA296102E179155D937FAFA8`）。**别逐课 tar**（见坑 1）。
- **manifest 合并规则＝`{**手机端, **本地包}`**：共享字段用本地新值覆盖、手机端独有字段保留；序列化 `ensure_ascii=False, indent=1`、**无尾换行**；`lesson.json` 写成与 `manifest.json` **同字节**。
- **C 类（仅音频重编码）不推**；**`cover.jpg` 一律不推**（设备侧原样保留）。
- **`.bak_` 目录不删**（只报不删）。
- **逐条写 progress 可续跑**：每推一条往 progress 文件追加一行（`status` / `stage` / 逐文件 sha256），中断后按文件续跑。

### 6.2 复检口径

四类（一致 / 混装 / 缺件 / 对不上）＋ 混装再拆**实质 / 非实质**（非实质三类：仅格式 / 合并口径 / 仅音频重编码）；**合计必须 = 课目录数**，对不上就说明采集有洞，先修采集再下结论。

### 6.3 台账重算

按 **lessonId**（**不是文件名**）配对；只改 `bytes` / `sha256` 两个字段；其余行**逐字节未动**；写完必须跑断言：**diff 行数 == 被改行数**（本轮 148 == 74 × 2）、`diff_lines_outside_bytes_sha256 = 0`、`assert_rowset_equal = True`、孤儿行/孤儿包清单均为 0。

### 6.4 装包正确做法

沿用 **versionCode 4030 / versionName 0.9.3**（**不升版**）；用 **`--debug`**（设备上跑的就是 debug 包，release 盖不住会撞 `INSTALL_FAILED_UPDATE_INCOMPATIBLE`）；加 **`--no-pub`**（本机无外网，装依赖会卡）。本轮实测：`flutter build apk --debug --no-pub --target-platform android-arm64` → 164,011,430 B / `3f32a0b8…`，`adb install -r` 6 秒 Success。

### 6.5 三个坑

- **坑 1**：`adb exec-out run-as … tar` **连续逐课调用会卡死**（设备端 tar 阻塞，而 `adb shell` 正常）⇒ **一次备份整目录，别逐课**。依据：本段改整目录一次后正常；另一条走逐课 tar 的 `mi14_push.py` 那路，`push_log.jsonl` 376 条里 **188 条 failed**（该"约 72 次"的具体阈值未在报告留证 ⇒ **未取到**）。
- **坑 2**：**推包时 App 必须在后台**（前台会用旧数据覆盖回去）⇒ **等郭老师自己退出，别 force-stop**（本轮全程 `ps -A` 只读复查，未 force-stop、未启动 App）。
- **坑 3**：**另一 DSH 会话可能同时推同一台设备** ⇒ 动手前先查 `Get-CimInstance Win32_Process | ? CommandLine -match 'push_mi14|mi14_push'`。依据：2026-10-27 00:56 另一会话起用旧流程 `mi14_push.py` 逐课 tar 推同一批目录，与本段脚本同时写同一批目录 / 同一 `push_log.jsonl` ⇒ 145 条非 ok；本段用字节级扫描判定实际状态并修复 48 门后逐文件 sha256 全部对齐。

### 6.6 铺包前后自检清单（照着念，缺一条就别往下走）

| # | 什么时候 | 查什么 | 通过标准 |
|---|---|---|---|
| 1 | 动手前 | `adb devices -l` | 只认当前那台；另一台**不碰** |
| 2 | 动手前 | `Get-CimInstance Win32_Process | ? CommandLine -match 'push_mi14\|mi14_push'` | **无输出**（没有别人在推同一台） |
| 3 | 动手前 | `adb shell ps -A | findstr phrasing` | App **不在前台**；在就等郭老师退出，**不 force-stop** |
| 4 | 备份后 | `tar -tf backup.tar` | **非空**、条目数对得上目录数 |
| 5 | 推完 | 逐文件 `run-as … sha256sum` | 与本地包**逐条相同**（`cover.jpg` 除外） |
| 6 | 推完 | 复检四类 | **合计 = 课目录数**，且**实质混装 = 0** |
| 7 | 收尾 | 设备侧临时目录 | `/data/local/tmp/llpush_*` **无残留** |
| 8 | 收尾 | `ls -1 app_flutter/lessons | Measure-Object` | 目录数与开工前**一致**（没多没少） |

---

## 7. 交付形态与纪律（写给下一位 Agent）

1. **交付物统一收进一个单文件离线 HTML 指挥台**：`D:\临时文件夹\指挥台_句读.html`（**13 页**，底稿 `D:\临时文件夹\指挥台_句读_底稿.json`，构建时间 2026-10-26 17:40）。同一工作域**永远更新同一个文件**，不新建。
   - **两步工作法**：第 1 步出**底稿 JSON**（只提取与计算），第 2 步渲染 HTML（只渲染，不算数据）。
   - **单文件硬约束**（本件实测）：`<style>` **1** 个、`<script>` **1** 个、`src=` **0**、`href=` **0**、`fetch(` **0**、`XMLHttpRequest` **0**；数据内联为常量，`file://` 双击可开；页内不写执行按钮（只允许 `window.print()`）。
   - 每页顶部一条**数据带**（本页数据时间｜来源｜口径），底部一行「本页无任何执行按钮；所有数字带口径；取不到写『未取到』」。
2. **产出前过评分闸**：先写评分细则（10 分制、合格线 **8.0**）→ 独立评分员（**没参与制作**）打分 → **<8.0 打回重做，上限 2 轮**。做事者 / 评分者 / 返工者**三个角色不得是同一个**。
3. **数字纪律**：每个数字带**口径与出处**；取不到一律写「**未取到**」，禁止编数；口径冲突要**列出来并标「待复核」**，不许挑一个当真相。
4. **写入纪律**：产物落 `D:\记忆\_inbox\<任务名>\`；**`D:\记忆` 正文永远只读**（本仓默认一个字都不许写）；不执行 git 写操作。
5. **节奏**：**一次只做一件事**，别为"先审计再动手"而慢；正文 / 清单 / 代码写进文件，不回贴主对话。
6. **涉及设备的三条红线**：**不许启动 / force-stop App**、**不许动音量**、**不许抢前台**；只做只读查询（`ps -A` / `dumpsys` / `stat` / `sha256sum`）。

---

## 8. 文件索引

**报告（改动主体）**
- `D:\dss-work4\logs\subtitle_depth_fix\report.md`（＋ `scorecard.md`）
- `D:\dss-work4\logs\huangshan_fix_20261025\huangshan_report.md`
- `D:\dss-work4\logs\realign_20261025\realign_report.md`
- `D:\dss-work4\logs\realign_batch2_20261026\realign_batch2_report.md`
- `D:\dss-work4\logs\audio_source_audit\verdict\verdict_60.md`
- `D:\dss-work4\logs\revert_tts_20261025\revert_report.md`（＋ `scorecard_assets.md`）
- `D:\dss-work4\logs\policy_tidy2_20261026\tidy2_report.md`
- `D:\dss-work4\logs\loudness_audit_20261026\loudness_report.md`
- `D:\dss-work4\logs\loudness_normalize_20261026\normalize_report.md`
- `D:\dss-work4\logs\listen_layout_20261025\accordion_change.md` ／ `batch2_report.md` ／ `scorecard_ui.md`
- `D:\dss-work4\logs\wallpaper_global_20261025\wallpaper_report.md`
- `D:\dss-work4\logs\listen_align_20261026\align_report.md` ／ `assert_fix_20261026\assert_fix_report.md`
- `D:\dss-work4\logs\overwrite_sync_20261026\overwrite_report.md`
- `D:\dss-work4\logs\cut_lead_gate_20261026\gate_report.md`
- `D:\dss-work4\logs\skill_rule_20261026\skill_rule_report.md`
- `D:\dss-work4\logs\resample_3lessons_20261026\resample_report.md`
- `D:\dss-work4\logs\apk_fix_20261026\fix_report.md` ／ `apk_build2_20261026\apk_report2.md`

**设备 / 铺包 / 一致性**
- `D:\dss-work4\logs\phone_consistency_20261026\consistency_report.md` ＋ `cross_device_note.md` ＋ `device_95a8fd5_mi10ultra\consistency_report.md`
- `D:\dss-work4\logs\device_switch_20261026\switch_report.md`
- `D:\dss-work4\logs\resync_all_20261026\resync_report.md`
- `D:\dss-work4\logs\resync_verify_20261026\verify_report.md`
- `D:\dss-work4\logs\final_push_ledger_20261026\final_report.md`
- `D:\dss-work4\logs\resync_mi14_20261027\report.md` ＋ `recheck.json` ＋ `push_log.jsonl`

**台账**
- 台账真源：`D:\listenloop\assets\lessons\lessons_asset_manifest.json`（259 行，本轮被改 74 行）
- 改前台账整份备份 ＋ 逐行对照：`D:\dss-work4\logs\final_push_ledger_20261026\lessons_asset_manifest.BEFORE.json`、`ledger_after.json`
- 响度待更新表：`D:\dss-work4\logs\loudness_normalize_20261026\ledger_pending.csv`；重做课待更新表：`D:\dss-work4\logs\resample_3lessons_20261026\ledger_pending.csv`

**证据（原始数据 / 备份 / 回退件）**
- `D:\dss-work4\logs\subtitle_depth_fix\green_*.txt`、`red_*.txt`、`regression_after_testfix.txt`、`preview\after_measure.txt`、`backup\`
- `D:\dss-work4\logs\loudness_normalize_20261026\backup\`（72 个包）＋ `backup_index.json`；回退脚本 `restore.py`
- `D:\dss-work4\logs\resample_3lessons_20261026\backup\`（3 包）＋ `restore_originals.ps1`
- `D:\dss-work4\logs\resync_mi14_20261027\phone_backup_all.tar`（整目录一次备份）、`phone_backup\`、`evidence\`
- `D:\dss-work4\logs\resync_all_20261026\backup\`（82 份逐课 tar）
- `D:\dss-work4\logs\cut_lead_gate_20261026\verification_results.json`、`gatekeeper.diff`、`build_course.diff`

**脚本**
- `D:\listenloop\tool\verify_cut_lead.py`（**新工具**：句首预卷机器闸）
- `D:\listenloop\pipeline\gatekeeper.py`（第 5 项检查）＋ `pipeline\build_course.py`
- `D:\listenloop\tool\yuandi38_fetch_bili.py`（白名单＝两位）
- `D:\dss-work4\logs\cut_lead_gate_20261026\run_verification.py`
- `D:\dss-work4\logs\resync_mi14_20261027\evidence\scripts\`（`mi14_push.py` / `push_mi14.py` / `finalize_mi14.py` / `recheck_mi14.py` / `mi14_classify.py` 等）
- `D:\dss-work4\logs\final_push_ledger_20261026\_s02_ledger.py`、`_push.py`、`_s12_recheck_final.py`
- `D:\dss-work4\logs\resample_3lessons_20261026\build_resample.py`、`install_verify.py`

**技能库（规矩真源）**
- `D:\Work\元智能\10_AI自成长引擎\技能库\phrasing-course-pipeline\components\phrasing-lesson-segmentation\SKILL.md`（铁律 5：句首预卷与音轴起点口径）
- `D:\Work\元智能\10_AI自成长引擎\技能库\phrasing-course-pipeline\components\phrasing-lesson-build\SKILL.md`（铁律七：句首预卷 0.5~1 秒 ＋ 六道自查 ＋ 混装对账）
- 同目录各有一份 `CHANGELOG.md`（本轮各追加一条）

**指挥台**
- `D:\临时文件夹\指挥台_句读.html`（13 页，209,684 B）
- `D:\临时文件夹\指挥台_句读_底稿.json`（260,961 B，第 1 步数据底稿）

**交接件（本件）**
- `D:\记忆\_inbox\句读\2026-10-27_句读字幕与听页治理_交接.md`

---

> **本件写于 2026-10-27 01:2x（Asia/Shanghai）。** 数字全部回真源核过；核不出来的写「未取到」。**服务器未发布、欠账未清、待拍板未决，都写在 §5，不许读成已完成。**
