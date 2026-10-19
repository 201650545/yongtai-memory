---
name: image-gen-routes
description: 生图通路实测结论：商汤 u1.5-fast 主力（10~14s）、AGNES 备席、集梦 CLI 高清、Loomy 全线 404
metadata: 
  node_type: memory
  type: project
  originSessionId: e5ca6684-1e8b-4ac6-95bb-d10c88057836
  modified: 2026-09-01T15:27:03.640Z
type: project
updated: 2026-10-20
---

# 生图通路由实测

## 2026-10-20 复测（当前结论，优先于下文 9-01 版本）

四条渠道全量实跑，prompt 统一 `一只橘猫坐在窗台上，午后阳光，写实风格`：

| 渠道 | 模型 | 实测耗时 | 消耗 | 结论 |
|---|---|---|---|---|
| 商汤日日新 | `sensenova-u1.5-fast` | **10.1~14.0s**（5 轮中位 11.0s） | 入 1283~1531 tok + 出固定 4096 tok/张 | ✅ **主力**：快、稳（波动 ±1s）、线条一致性最好 |
| 商汤日日新 | `sensenova-u1.5-lite` | 20.2~26.1s | 入 ~1499 + 出 4096 | ⚠️ 慢一倍且 token 更多，无理由使用 |
| AGNES | `agnes-image-2.5-flash` | 16.5~22.0s（均值 18.5s） | 无 usage 字段，查不到 | ✅ 备席：质量好、无水印 |
| AGNES | `agnes-image-2.1-flash` / `-2.0-flash` | 16.9s / 24.8s | 同上 | ✅ 可用 |
| 集梦 CLI | `jimeng-5.0` / `-4.5` / `-4.6` | 40.0 / 39.3 / 53.6s | 固定 12 积分 = 4 张 2048×2048（3 分/张） | ✅ 质量最高，但是唯一有额度计费的 |
| 讯飞 Loomy（经 buddy2api:8787） | `doubao-seedream-5-lite`、`qwen-image-3.0-pro`、`Hy-Image-3.5-preview` | 0.3~40s（失败） | 0 | ❌ **全部 404** |

### Loomy 生图不可用（确定结论，不要重试）

三个生图模型出现在上游 `GET https://loomyad.xunfei.cn/api/v1/models` 目录里，
但无论经 buddy2api 转发还是**用解密后的 token 直连上游**，`/chat/completions` 一律返回：

```json
{"error":{"message":"该模型暂未开放，请切换其他模型","type":"not_found_error","code":404,
          "metadata":{"provider_name":"loomy"}}}
```

大小写敏感 ID（`Hy-Image-3.5-preview`）与带/不带 `loomy/` 前缀四种组合全试过，
均 404。上游 `/models` 是 OpenAI 兼容端点，但**没有任何 images 端点**，
`chat.py` 也只转发 `/chat/completions`。**这是上游侧未开放，不是调用姿势问题。**

### 商汤接口的四个坑

1. **`n` 只接受 1**：传 `n=2` 上游返回 502 `invalid n, should be in [1, 1]`。
2. **`response_format=url` 会丢 size**：上游自行按 2048×1536 出图，要控尺寸必须用默认 `b64_json`。
3. **尺寸都是字符串**：支持 `512x512` / `1024x1024` / `1024x1792` / `2048x2048`，
   2048 那张耗时 40.55s、产物 6.1MB。
4. **返回 PNG 无 alpha**，右下角带 `日日新 sensenova` 水印，必须后处理（见 [[project_workbuddy_account_switcher]] 的去水印流程）。

### AGNES 的坑

UA 必须是 `curl/8.5.0` 这类标准 UA；网关默认 UA 会触发上游误报 `invalid mode`。
余额端点全 404，无法核对额度，只能靠"持续 200 无扣费提示"判断可用。

### 路由现状（search_gateway `:3100`）

`data\model_routes.json` 的 `routes["image-gen"]` 成员：
`sensetime/sensenova-u1.5-fast` → `sensetime/sensenova-u1.5-lite` → `agnes/agnes-image-2.5-flash`。
**AGNES 和商汤两个渠道都已在 image 清单里，商汤占两席、AGNES 一席兜底，一个不缺。**
全表扫过，image 渠道只有这两家。调用需带 `Authorization: Bearer <data\api_state.json 的 api_key>`。

---

## 2026-09-01 版本（seedream-5.0 暂停后的历史结论，保留作对照）

2026-09-01 实测五条生图通路（seedream-5.0 账号级暂停后，用户拍板：搁置 5.0，agnes 主 + CF 补）：

| 通路 | 结论 |
|---|---|
| **agnes-image-2.1-flash**（apihub.agnes-ai.com，key 在 channels.json） | ✅ 主路：中文提示词理解好、质量高、约13s/张、1024²起 |
| **cloudflare flux-1-schnell**（Workers AI） | ✅ 补量：172.8 neurons/张，日额度 10000 neurons≈57张；**必须英文提示词**（中文画成书法字）；坑：channels.json 里 CF base_url 的 account id 被截断成 38 位，正确 32 位 hex 要取前 32；正确端点 `/client/v4/accounts/<id32>/ai/run/@cf/black-forest-labs/flux-1-schnell`，返回 result.image b64 |
| **doubao-seedream-4-5-251128**（ark 经 :3100） | ✅ 备用：免费额度内，尺寸≥3686400px（2560×1440 合规） |
| modelscope FLUX.1-schnell | ❌ 仅异步模式（头 X-ModelScope-Async-Mode: true），同步 40212 |
| siliconflow FLUX.1 | ❌ 403 Model disabled |

**Why:** [[project_seedream5_paused]] （原 `seedream-5-paused`）后所有生图任务需要替代路由；避免重复逐条试错。

**How to apply:** 生图脚本默认走 agnes（中文提示词）；批量补量用 CF flux（英文提示词翻译一轮）；4.5 留给需要 16:9 大图/仙逆官方画风的场景。CF account id 修正代码已在 [[project_ai_gateway]] channels.json 处理前先取前 32 位。产物规格：主题背景 2048×1152 JPEG q90（其他比例 PIL 裁切，top-biased 0.42）。

> **2026-10-20 修正**：上表"agnes 主路"的定位已被推翻——商汤 `u1.5-fast` 更快（10~14s）
> 且线条一致性明显更好，已成为主力。agnes 降为备席。

## 网关侧三个未修的小隐患

1. `data\channel_models.json` 的 `sensetime.selected` 只列了 `sensenova-u1.5-lite`，
   **缺 `sensenova-u1.5-fast`**。生图链路不读该文件，当前无影响，但属隐患。
2. `model_catalog.json` 为空（`models: {}`），别名目录里看不到 `image-gen`，
   只能在 `/v1/models` 的 routes 键看到。前端要展示生图入口得补 catalog。
3. quota 记账不解析 usage，图片 token 明细记为 0，账本上做不了生图成本统计。
