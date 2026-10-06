---
name: workflow-调度大脑交接手册
description: 新 Agent 接手 ai-resource-hub 调度大脑的第一动作、关键路径地图、每日例行、命令速查（保证任何人/任何 Agent 都能快速接手）
metadata:
  node_type: memory
  type: workflow
  created: 2026-09-22
---

# 调度大脑交接手册

> 目标：任何 Agent 接手都能 10 分钟内进入状态。身份 = ai-resource-hub 调度大脑（唯一窗口，郭老师只在这窗口聊）。

## 一、开局三读（第一动作，顺序执行）

1. `D:\项目\ai-hub\search_gateway\渠道编排规则.md` —— 渠道规则**唯一真源**（郭老师逐条钦定）
2. `D:\项目\ai-hub-memory\projects\ai-resources\STATE.md` + `CHANGELOG.md` 尾部 20 条 —— 项目状态与最近流水
3. 本 Obsidian 库 `索引.md` + `项目/project_ai_gateway.md` 时间线 —— 长线脉络

## 二、关键路径地图

| 资产 | 路径 |
|---|---|
| 网关 :3100（API 转发） | `D:\项目\ai-hub\search_gateway`（重启：`services\start_api_gateway_3100.ps1`，**普通权限禁 UAC**） |
| 渠道编排（三档+语音链） | `data\model_routes.json`（mtime 热加载，改完即生效） |
| 额度警戒闸门 | `services\quota_guard.py` + `data\quota_guard.json`（无 BOM！） |
| 每日自动化脚本 | `scripts\daily_channel_refresh.py` / `zenmux_free_scan.py` / `ark_quota_scan.py` / `bai_welfare_check.py` |
| 警报出口 | `data\渠道警报.log`（zscc 失效/方舟破线/巡检失败都写这里） |
| monorepo（代码唯一家） | `D:\Work\AI平台\apps\search-gateway\services`（改完代码同步+commit+push） |
| 共享记忆仓库 | `D:\项目\ai-hub-memory\projects\ai-resources\`（STATE/DECISIONS/CHANGELOG） |
| 本 Obsidian 库 | `D:\记忆\调度大脑记忆\`（git 管理，改完挂 [[调度大脑记忆/索引]]） |
| 网关 key | `data\api_state.json` 的 api_key 字段（不进对话不入 git） |
| Jev 决策模型 key | `data\typesafe_key.txt`（POST api.typesafe.ai/v1/systemone） |

## 三、每日例行（自动化已接管，人只看警报）

- 00:23 ChannelDailyRefresh：编排全量成员实测 + zenmux/openrouter 免费名单巡检
- 10:17 ArkQuotaScan：方舟额度盘点→回写警戒闸门（需 Chrome 开着且方舟控制台登录态）
- 周一 09:17 BaiWelfareCheck：bai 探监
- **Agent 开工时**先瞄一眼 `data\渠道警报.log`，有新警报按 [[workflow_网关渠道挑选与刷新策略]] 处置

## 四、命令速查

```bash
# 网关存活
netstat -ano | findstr :3100          # 以 LISTENING 为准
# 三档/语音链真调（别名直调）
curl -X POST http://127.0.0.1:3100/v1/chat/completions -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" -d '{"model":"free-fast","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'
# 别名清单 / 闸门看板 / 路由日志
curl http://127.0.0.1:3100/v1/models -H "Authorization: Bearer $KEY"
curl http://127.0.0.1:3100/api/quota-guard
curl http://127.0.0.1:3100/api/route-log -H "Authorization: Bearer $KEY"
# 探针（免费渠道真调实测，付费禁测）
python services/probe_free_channels.py --only=<渠道>
```

## 五、铁律清单（全程有效）

- 付费禁测：deepseek / opencode / tokenrhythm / ark-coding（已删）；zscc 禁压测
- **zscc V4.1-cc 失效必须当日提醒郭老师拍板，禁止自行换模型**
- 密钥永不外泄（不进 git/记忆/Obsidian/对话）；data/ 整体 gitignore
- 管理员操作自己跑（UAC 郭老师点「是」）；网关重启禁 UAC
- 别反复问：小决策自己办，只有重大/破坏共享运行时才停手
- 做完即完结：任务闭环 + 档案四写（规则文档/CHANGELOG/Obsidian/内部记忆）
- 人可读层中文命名；结尾转发块约 50 字含真源路径（[[workflow_转发与汇报策略]]）
- 代码改动同步 monorepo 并 push（git add 指定文件后 commit **不带 pathspec**——`git commit -- <path>` 会把工作区全量带上的坑，见 CHANGELOG 9-21）

## 六、未决事项（接手先看）

- Jev 决策层三步走计划（`Jev决策层接入计划.md`）：意图路由/派发打分/决策即服务，待郭老师点哪步先做
- Sparkle asar 免重启补丁：自更新会冲掉，需重打（备份 app.asar.bak_b4hotreload_20260921）
- ChatGPT 镜像自动提问通道当日不稳（选择器/流程见 workflow_ai_wendabao_open）
- 硅基聊天大模型不入编排（9-22 裁决）； CosyVoice2/赠金名单已接语音与 embedding

关联 [[project_gateway_现状与展望]] [[workflow_网关安全防扣费策略]]
