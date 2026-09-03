---
name: codebuddy-model-policy
description: codebuddy 模型策略（2026-09-01 21:56 → 2026-09-02 修正）：默认 hy4-preview，额度用完切 GLM 5.3 flash，不切其他款
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 268c3880-5dca-437e-a181-26e2eebdff49
  modified: 2026-09-02T05:36:47.264Z
---

codebuddy 派发时**不显式传 `--model`**，让 codebuddy 服务端按额度自动决定：
1. hy4-preview 额度充足时 → 用 hy4-preview
2. hy4-preview 额度用完 → 自动切到 **GLM 5.3 flash**（不能切其他 GLM 款/不能切 deepseek-v4-flash/不能切其他模型）
3. 只有用户**显式指定**其他模型时（如 `--model deepseek-v4-flash`）才走用户指定

**Why:** 2026-09-01 21:56 郭老师原指令「hy4 用完切 deepseek-v4-flash 不切 glm-5.3」是约束**默认 fallback**，但 2026-09-02 codebuddy 升级后**显式支持** GLM 5.3 flash 作为 hy4 用完的官方兜底——修正后规则是：GLM 5.3 flash 是唯一允许的 fallback，**其他款（glm-5.3 Pro / 5.2 / 5.1 / 其他 GLM / deepseek-v4-flash 等）都不能切**。

**How to apply:**
1. workbuddy_cli.py：ALLOWED_MODELS 白名单含 `hy4-preview / glm-5.3-flash`（**仅这两款**）；其他模型在白名单里**只允许用户显式指定时**走（默认拒绝）
2. dispatch.py B-via=workbuddy **不传 `--model`**（让 codebuddy 服务端按额度自决）；只有 `--model` 用户显式传了才透传
3. 派发前必先 ping 验证当前模型：`workbuddy_cli.py "回复OK" --model glm-5.3-flash` 看返回是否正常（这是兜底模型健康检查）
4. 派发前必先验 7890 代理可达（[[feedback_codebuddy_proxy_precheck]]）

**修正历史**：
- 2026-09-01 16:25 原版：白名单仅 hy4/deepseek-v4-flash/minimax-m3，**拒绝 glm-5.3 任何形式**
- 2026-09-02 03:14 修正：GLM 5.3 flash 入白名单，作为 hy4 用完的官方兜底

相关：[[project_scheduler_role_matrix]] 派发矩阵 4 维；[[feedback_codebuddy_proxy_precheck]] 7890 代理前置
