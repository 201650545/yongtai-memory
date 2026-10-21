---
name: lesson_镜像站共享标签被抢占时用独立浏览器隔离
description: opencli 的 eval 只打活跃标签，多个会话共用同一个浏览器时互相抢标签会触发 detached_mid_command；解法是用 playwright 起独立 profile 的 Chrome + 内存中转账号池凭据，并按 create_time 排序 API 消息。
type: lesson
updated: 2026-10-21
kind: rule
status: active
---

# 镜像站共享标签争用 → 独立浏览器隔离（2026-10-21 实测）

## 现象

同一台机器上有两个会话都在用 `gpt-mirror-extended-review` 送审时，
opencli 的 `eval` **只打「活跃标签」**（v1.8.8 的 `eval` 不支持 `--tab` 定向），
对方把标签导航到根地址/账号池页，就会：

- 注入中途报 `detached_mid_command`（执行上下文被导航销毁）；
- 刚发出去的轮次被判成「没发出去」（DOM 的 `[data-message-author-role=user]` 计数
  在虚拟滚动下恒为 2—3，**不能**用来判发送成功与否）；
- 两个会话来回导航，谁也跑不完。

## 正解：另起一个独立浏览器实例

playwright 起**独立 profile** 的 Chrome（不碰用户那个窗口、不碰共享标签）：

1. 从**账号池页** localStorage 取 `panelAccountList` + `authToken`；
2. 用本机 `127.0.0.1` 的小 HTTP 服务在**内存里**中转（值不落盘、不回显、不过上下文，
   照 skill 的 secret_guard）；页内 `fetch` 到中转服务要带 CORS 头；
3. 独立浏览器里注入凭据 → 跑 `fast_jump.js` → 得到**自己的**镜像实例会话；
4. 之后全程不再碰共享标签（只在开局借 5 秒取凭据）。

⚠️ **独立浏览器必须 `locale='en-US'`**（还要带 `Accept-Language: en-US`）：
站点会按浏览器语言渲染界面，中文环境下 `jump_and_ready.js` 的
`pill==='High'` 恒失败（读到的是「高」），三闸过不去。

## backend-api 取回复的两个坑

- **mapping 不是时间序**：`/backend-api/conversation/<cid>` 返回的 mapping 按 node id 排，
  取「最后一条 assistant」会取到乱序的旧消息 ⇒ 必须按 `message.create_time` 排序。
- **cid 可能带 `WEB:` 前缀**：新会话 id 形如 `WEB:<uuid>` 时 API 收不了，
  要等页面 URL 改写成裸 uuid（或去掉前缀）再取。

## 完整实现

`D:\Work\English-Content-Factory\02_Projects\HN-ENGLISH-666\06_templates\_mirror_isolated.py`
（`bootstrap` / `run <a> <b> [轮次目录] [输出目录]`，含 base64 注入、三闸、DOM 兜底）

## 相关

- [[lesson_小红书发布_键盘事件与草稿存储]] —— 同一个浏览器桥上的另一个「标签归属」坑
