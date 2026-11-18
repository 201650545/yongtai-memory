---
name: lesson_魔搭魔粒守护三处失效修复
description: 2026-11-18 修复 ModelScope 每日魔粒守护（3 个月零成功）：opencli 2.x 三处 API 变更（doctor 输出转 JSON、browser session 改 --session 选项、eval 返回值多包一层 {ok,data}）＋魔搭接口改名 magic_cube→magicubes。修后计划任务退出码 0，250 魔粒到账（每日登录 200＋阿里云绑定 50），巡检转绿。附魔粒真实接口与字段。
type: lesson
updated: 2026-11-18
kind: fact
status: active
---

# 魔搭魔粒守护：三处 API 失效一次修完（2026-11-18）

## 结论

任务从 **2026-08-13 之后连续 3 个月零成功**（每日日志都是 `granted:{}, balance:null`），原因是 **opencli 升级到 2.x 后三处调用方式全变**，加上**魔搭接口改名**。四处全修后，退出码 **0**，250 魔粒到账。

## 四处失效点与修法

| # | 失效点 | 旧写法 | 新写法 |
|---|---|---|---|
| 1 | `opencli doctor` 输出格式 | 文本，判据 `/Daemon: running/` | **JSON** `{"ok":true,"data":{"daemonRunning":true,"extensionConnected":true}}` |
| 2 | `browser` 的 session 传参 | `browser msdaily <cmd>`（位置参数） | `browser <cmd> --session msdaily`（**选项**，放最后） |
| 3 | `eval` 返回值 | 直接用页面返回串 | 多包一层 `{"ok":true,"data":"<页面字符串>"}`，需先剥壳再 `JSON.parse` |
| 4 | 魔搭余额/流水接口 | `/openapi/v1/magic_cube/balance` | **`/openapi/v1/magicubes/balance`**（复数，无下划线） |

## 魔搭魔粒真实接口（2026-11-18 实测）

```
GET https://www.modelscope.cn/openapi/v1/magicubes/balance
 → {"success":true,"data":{"total_balance":240,"available_balance":240,
                           "frozen_amount":0,"is_disabled":false}}

GET https://www.modelscope.cn/openapi/v1/magicubes/transactions?page=1&page_size=60
 → {"success":true,"data":{"page":1,"page_size":50,"records":[
     {"gmt_created":"2026-11-18","type":"EARN","rule_key":"aliyun_bindlogin",
      "title":"绑定阿里云账号","category":"每日发放","total_amount":50,...}]}}
```

- **余额字段只有** `total_balance` / `available_balance` / `frozen_amount` / `is_disabled`。
  旧代码读的 `nearest_expiry_amount`、`nearest_expiry_at`、`user_level` **已不存在**，会打印 `undefined` —— 已改为「有则打印、无则跳过」。
- 入口页：`https://www.modelscope.cn/my/overview`（魔粒按钮 `aria-label="Magic Cube"`，页面上不出现「魔粒」二字，只能靠 aria-label 或接口找）。
- **别再去 `artificialanalysis` 找魔粒**——那是另一套东西。

## 诊断方法（可复用）

1. **先看历史日志的体积变化**：`logs/YYYY-MM-DD.json` 一直是同一字节数（本例 284→216 字节）= 每天同一份失败模板，说明很久没真跑通过。
2. **抓页面真实请求**，不要猜接口名：
   ```js
   performance.getEntriesByType('resource').map(r=>r.name)
     .filter(u=>/magic|cube|credit|point/i.test(u))
   ```
   本例据此一秒钟找到 `magicubes`（而手工试了 8 个 `magic_cube` 变体全是 404）。
3. **opencli eval 的坑**：必须传**表达式**，裸 `fetch(...).then(...)` 会失败；用 `(async()=>{...})()` IIFE 包起来。
4. `.cmd` 包装器 + `shell:true` 会破坏含引号/中文的 JS 参数；**改用 `node <opencli>/dist/src/main.js` 直调**绕开。

## 验证输出（2026-11-18 21:10）

```
[21:10:27] 桥接正常（daemon + 扩展在线）
[21:10:47] 每日魔粒已全部到账
[21:10:48] 完成，退出码 0
计划任务 LastTaskResult = 0
巡检：red 10 → 9，asserted_green 15 → 16（task_modelscope_daily_guard 转绿）
```

日报：每日登录 200 + 阿里云绑定日奖 50 = **250 魔粒**；余额 240。

## 相关

- 项目：`D:\项目\modelscope-daily\`（`运行.ps1` 入口、`魔粒守护.js` 主体、`config.json` 接口配置）
- 备份：`魔粒守护.js.bak-doctor-20261118`、`config.json.bak-20261118`
- opencli 版本：CLI 2.0.2（有 2.0.3 可用）、扩展 1.0.26（有 1.0.27 可用）
