---
name: image-gen-routes
description: seedream-5.0 暂停后的生图通路实测结论（2026-09-01）：agnes 主 + cloudflare flux 补 + seedream-4.5 备用
metadata: 
  node_type: memory
  type: project
  originSessionId: e5ca6684-1e8b-4ac6-95bb-d10c88057836
  modified: 2026-09-01T15:27:03.640Z
---

2026-09-01 实测五条生图通路（seedream-5.0 账号级暂停后，用户拍板：搁置 5.0，agnes 主 + CF 补）：

| 通路 | 结论 |
|---|---|
| **agnes-image-2.1-flash**（apihub.agnes-ai.com，key 在 channels.json） | ✅ 主路：中文提示词理解好、质量高、约13s/张、1024²起 |
| **cloudflare flux-1-schnell**（Workers AI） | ✅ 补量：172.8 neurons/张，日额度 10000 neurons≈57张；**必须英文提示词**（中文画成书法字）；坑：channels.json 里 CF base_url 的 account id 被截断成 38 位，正确 32 位 hex 要取前 32；正确端点 `/client/v4/accounts/<id32>/ai/run/@cf/black-forest-labs/flux-1-schnell`，返回 result.image b64 |
| **doubao-seedream-4-5-251128**（ark 经 :3100） | ✅ 备用：免费额度内，尺寸≥3686400px（2560×1440 合规） |
| modelscope FLUX.1-schnell | ❌ 仅异步模式（头 X-ModelScope-Async-Mode: true），同步 40212 |
| siliconflow FLUX.1 | ❌ 403 Model disabled |

**Why:** [[seedream-5-paused]] 后所有生图任务需要替代路由；避免重复逐条试错。

**How to apply:** 生图脚本默认走 agnes（中文提示词）；批量补量用 CF flux（英文提示词翻译一轮）；4.5 留给需要 16:9 大图/仙逆官方画风的场景。CF account id 修正代码已在 [[project-ai-gateway]] channels.json 处理前先取前 32 位。产物规格：主题背景 2048×1152 JPEG q90（其他比例 PIL 裁切，top-biased 0.42）。
