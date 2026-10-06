---
name: feedback-mirror-image-gen-slowworks-download
description: ChatGPT 镜像站 chat 生图「很慢但能出」——不是故障；出图后经「Download this image」按钮下载（Chrome 落 Downloads 为 .tmp，实为完整 PNG，复制改名即可）
metadata:
  node_type: memory
  type: feedback
  modified: 2026-09-12T11:15:00.000Z
  originSessionId: mirror-image-gen-curriculum-ideology
---

郭老师（2026-09-12）让经 ChatGPT 镜像站（AI问答宝/wendabao → vip-XX.67673.live，closeai.biz 代理）用 extend 注入海报提示词生图并下载。**更正我中途的错误判断**：我一度判定「镜像 chat 生图走不通/故障」，其实**只是极慢**（图片与文本都要数分钟才回流），最终出图成功。

**实测时间线（同一次排查）：**
- opencli v1.8.6 连通正常；healthy PLUS 账号 vip-48 / vip-09 均可登。
- vip-48 Extended 注入彩色海报提示词发送成功，等 7.5 分钟 + reload 仍 asst:0（当时误判为故障）。
- 换 vip-09（Auto 模式，其模型菜单打不开、切不了 Extended——属手册 §7.2 已知实例差异，Auto 兜底）重发彩色海报提示词，**约 5–8 分钟后出图**（生成 1 张，1055×1491，A4 比例）。
- 旁证：同账号发「1+1」纯文本，也要 1–2 分钟才回流「2」——说明镜像整体**延迟极高**，非故障。

**为何会误判：等待窗口取太短 + reload 后误读。** 该镜像 Extended/Auto 出图普遍 3–8 分钟；`data-message-author-role=assistant` 在生成完成前一直是 0，且没有 stop 按钮，容易误以为卡死。**判定完成要看是否出现图片元素**，不是看 assistant 轮数。

**出图后下载方法（已验证，重要）：**
1. 生成图在 DOM 里是 `<img src="https://vip-XX.67673.live/backend-api/estuary/content?id=file_...&sig=...&ts=...">`（1055×1491，alt="Generated image: …"）。同一张图会被 clone 成多个 `<img>`（同 src），取第一个即可。
2. **别用 curl 直连**：沙箱网络到镜像 host 不通（http=000）。要在浏览器里下。
3. 页面上有 `button[aria-label="Download this image"]`（在 `div.group\/imagegen-image` 内）。**点它**（完整 pointer 事件序列 + 原生 click）→ Chrome 把文件下到默认 Downloads，期间是 UUID 命名的 **`.tmp`**（如 `a61f5ee9-….tmp`）。
4. **`.tmp` 就是完整 PNG**（magic `89504e47`）——Chrome 因镜像的 Content-Disposition 未 finalize 改名。直接 `cp` 出来改名为目标名即可。用 Python 读 IHDR（bytes16:24）可校验宽高。

**Why:** 镜像 chat 后端延迟极高但可用；下载走页面按钮 + 从 Downloads 捞 `.tmp` 是最稳路径（curl 会被沙箱网络挡）。
**How to apply:** 再经该镜像生图：①Extended 切不动就 Auto 兜底（不强求）；②发送后耐心等 3–8 分钟，以「出现 estuary/content 的 <img>」为完成信号；③点击「Download this image」→ 去 `C:\Users\郭永涛\Downloads` 取最新 `.tmp` → 复制改名落目标目录。关联 [[feedback_mirror_as_generator_download]] [[feedback_mirror_extend_for_architecture]] [[feedback_mirror_send_speed]]。
