---
name: project-gateway-现状与展望
description: :3100 网关 2026-09-21~22 大建设战果总结（三档编排/语音三链/方舟额度警戒闸门/自动化矩阵）+ mermaid 可视化 + 未来前景路线
metadata:
  node_type: memory
  type: project
  created: 2026-09-22
---

# 网关项目现状与展望（2026-09-22 快照）

## 一、两天战果（9-21~22 大建设）

| 板块 | 战果 |
|---|---|
| 三档免费编排 | free-fast 4 / free-balanced 12 / free-heavy 2，全成员每日实测，能力底线 ≥qwen3.8-27b |
| 语音三链 | voice-asr（6 席全免费）/ voice-tts（mistral→CosyVoice2）/ voice-chat（zscc Qwen3-Omni 双席） |
| 能力端点 | /v1/audio/transcriptions + /v1/audio/speech + /v1/embeddings（硅基 Qwen3-Embedding-8B） |
| 方舟治理 | 免费额度 45 模型盘点入档 + 额度警戒闸门（白名单+≥250万门槛+20%警戒线）+ 每日 10:17 自动盘点 |
| 防扣费体系 | quota_guard 覆盖 ark/zscc/zenmux/openrouter + 8 渠道 deny_all；实测三种拒绝路径全生效 |
| 自动化矩阵 | ChannelDailyRefresh / ZenMuxFreeScan / ArkQuotaScan / BaiWelfareCheck 四任务 |
| 渠道纪律 | 12 渠道规则全部钦定落档；ark-coding 删除（不再续费）；bai 冷宫周探监 |
| 其他 | Sparkle 免重启补丁、Jev 决策模型激活、网关健康缓存性能修复 |

## 二、全景架构图

```mermaid
flowchart TB
    subgraph 调用方
        U[郭老师 / 前端 / 子Agent]
    end
    subgraph GW[:3100 api_gateway]
        AUTH[网关鉴权] --> RT{路由}
        RT -->|编排别名| POOL[members 保序回落链<br>free-fast/balanced/heavy/voice-*]
        RT -->|点名| RES[legacy 解析]
        RES --> QG{quota_guard 闸门<br>白名单+≥250万+20%线}
        POOL --> QG
        QG -->|放行| UP[上游渠道]
        QG -->|拦| BLK[502 无扣费失败]
        RT -->|audio/embeddings| VOICE[语音与向量专用通路]
    end
    subgraph 上游
        FREE[免费: groq/modelscope/agnes/CF/longcat/nvidia/硅基ASR]
        ZSCC[zscc 按量: V4.1-cc + Omni]
        ARK[方舟: Evolving 550万 + V4-Pro 250万]
        DENY[deny_all: 硅基chat/mistral chat/deepseek/zhipu/gmi/tokenrhythm/bai]
    end
    U --> GW
    QG --> FREE & ZSCC & ARK
    POOL -.-> FREE
```

## 三、防扣费防线图

```mermaid
flowchart LR
    A[任何请求] --> B[第1层 白名单制<br>未登记模型一律拒]
    B --> C[第2层 最低额度门槛<br>方舟总额度>=250万token]
    C --> D[第3层 20%警戒线<br>剩余<=20%自动停]
    D --> E[上游调用]
    F[ArkQuotaScan 每日10:17] -.->|回写剩余额度| D
    G[ChannelDailyRefresh 每日00:23] -.->|免费名单快照| B
    E -->|超额度| X[上游 402/403<br>429 熔断兜底]
```

## 四、自动化时间线

```mermaid
timeline
    title 网关自动化与治理时间线
    2026-08-26 : 渠道限流准入闸门 v2
    2026-09-21 : 三档免费模型线重建 : 12渠道规则钦定 : ChannelDailyRefresh+ZenMuxFreeScan : BaiWelfareCheck
    2026-09-22 : 语音三链+embeddings : 方舟45模型额度盘点 : quota_guard三层防线 : ArkQuotaScan 10:17 : ark-coding 删除
```

## 五、未来前景（路线候选，待郭老师拍板）

1. **Jev 决策层**（已激活待接）：意图路由自动选档 → 派发中心打分 → 对外「决策即服务」。毫秒级近零成本，注册送 $5 = 1.2 亿 token。
2. **语音助手闭环**：ASR（听）→ voice-chat（想，Omni）→ TTS（说）已在网关齐备，差一个前端入口（可挂在 ai-hub 前端或 dispatch 页）。
3. **RAG 语义检索**：embeddings 端点已就绪，可给 :3000 搜索网关加语义召回（Qwen3-Embedding-8B 4096 维，1.12s/次）。
4. **活动二红利**：方舟协作奖励计划（每日单模型 200 万免费 token）未领取，领取后 Evolving 日额上限可达 750 万/日——需要郭老师到控制台点「立即参与」。
5. **闸门智能化**：quota 记账可从「每日快照」升级为「网关侧 token 记账实时扣减」，彻底消除快照间隔窗口。
6. **nemotron-omni 免费语音对话**：openrouter/nvidia 有免费的 `nemotron-3-nano-omni-30b-a3b`，可加为 voice-chat 免费备席（待拍板）。

## 六、风险登记

- 方舟额度数据靠每日快照，间隔内极端用量可能越过 20% 线才被拦（下日 10:17 才发现）→ 见前景 5
- ArkQuotaScan 依赖 Chrome 开着且方舟控制台登录态；失败会写渠道警报但当天数据不更新
- Sparkle 自更新会冲掉 asar 补丁（更新不重启内核的补丁），冲掉后恢复重启行为
- zscc 按量计费是编排里唯一非免费成员（郭老师钦定），有监控义务

关联 [[workflow_调度大脑交接手册]] [[project_ai_gateway]]
