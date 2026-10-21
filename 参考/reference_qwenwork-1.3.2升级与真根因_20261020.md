---
name: reference-qwenwork-1.3.2升级与真根因
description: 千问办公（qwenwork）从 1.0.4 升到 1.3.2 的完整结论：旧诊断「WASM ABI 不兼容」是错的，真根因是我们的 WASM 字符串传递按字节数而非字符数分配；附 1.3.2 协议要点与解禁条件。
type: reference
updated: 2026-10-20
kind: reference
status: active
---

# 千问办公（qwenwork）升 1.3.2（2026-10-20）

起因：交接单里「千问办公 provider 升到 1.3.2」是仅剩的大件——
buddy2api 的 qwenwork provider 按 1.0.4 协议实现，客户端是 1.3.2，
调用报 `EncodeError: attempted to take ownership of Rust value while it was borrowed`
→ 接着 `prepareInferRequest` WASM trap。旧结论写的是「WASM ABI 不兼容」。

## 一、旧诊断是错的

1.0.4 与 1.3.2 的 `qoder_auth_wasm_bg.wasm` **SHA256 完全相同**
（`15dad38f…f04d3`，288929 字节；1.0.4 那份是当年从客户端拷进 `native/` 的）。
⇒ WASM 没换过，**ABI 谈不上不兼容**。

## 二、真根因：我们的 `_pass_str` 非 ASCII 分支写错了

官方 glue（`qoder_auth_wasm_bg.js`）的 `passStringToWasm0` 是**三步**：

```js
let i = n.length, s = e(i, 1) >>> 0;              // ① 按**字符数** malloc
for (; o < i; o++) { const c = n.charCodeAt(o); if (c > 127) break; a[s+o] = c; }
if (o !== i) {
  o !== 0 && (n = n.slice(o));
  s = r(s, i, i = o + n.length*3, 1) >>> 0;         // ② 扩容到 o+剩余字符数*3
  const c = cachedTextEncoder.encodeInto(n, a.subarray(s+o, s+i));  // ③ 写剩余 UTF-8
  o += c.written;
  s = r(s, i, o, 1) >>> 0;                           // ④ 收缩到实际字节数
}
```

我们原来的实现**按 UTF-8 字节数** malloc、realloc 的 `old_size` 也用字节数。
中文名（账号名「郭乐」：2 字符 / 6 字节）一进去，分配大小与 old_size 全错位
⇒ WASM 侧拿到错乱字符串 ⇒ Rust panic（`unreachable`）
⇒ 报成 `EncodeError: attempted to take ownership of Rust value while it was borrowed`。

**隔离实验**（`scripts/probe_qwenwork_132_isolate.py`，全本地零额度）：

| 入参 | 结果 |
|---|---|
| `{}` / 只有 uid+token | OK |
| 完整 userInfo（中文名） | **trap** |
| 完整 userInfo（ASCII 名） | OK |
| 完整 userInfo（中文名，但 `ensure_ascii=True`） | OK |
| 中文只在 uid | **trap** |

⇒ 内容一样、只差字节 ⇒ 铁证是**字节级**问题，不是 JSON 结构问题。
修法：`_pass_str` 逐行照抄 JS 那四步（`encode.py` 里已改，注释写明了为什么）。

## 三、1.3.2 协议要点（全部从 1.3.2 客户端 `app.asar` 逆向，脚本见 `scripts/probe_qwenwork_132_*.py`）

| 项 | 1.0.4（旧） | 1.3.2（新，客户端实际做法） |
|---|---|---|
| Cosy-Version | 冻死 `"1.1.32"` | **`electron.app.getVersion()` = "1.3.2"**（asar package.json 的 version） |
| 版本串 | 1.0.4-26090412 | 1.3.2-26101704 |
| chat query | `?FetchKeys=llm_model_result&AgentId=agent_common` | `?FetchKeys=llm_model_result`（**去掉 AgentId**） |
| userInfo | {uid, encrypt_user_info, key, organization_id} | {name, aid, uid, yx_uid, access_token, security_oauth_token, refresh_token, organization_id, organization_name, organization_tags, user_type, data_policy_agreed} **+ {encrypt_user_info, key}** |
| encrypt_user_info / key | **本地 RSA**（cosy.py） | **WASM 的 `generate_runtime_auth_fields(JSON)` 产生** |
| chat 编码 | `prepareInferRequest(endpoint, body, model_key, source)`（4 参） | **`prepareRequest(endpoint, path, method, "auth", body, extraHeaders?)`（6 参）** |
| 调用形如 | — | `prepare({endpoint: d.origin, path: e.path, method: e.method ?? "GET", body: JSON.stringify(body)})` |
| clientMetadata | brand 字符串 | clientMetadata 对象：{client_type:"6", business_product:"qoder_work", business_type:"agent", scene:"qwork"}（**内容没变，只是叫法变了**） |

新增的 WASM 导出 `generate_runtime_auth_fields` 签名（app.asar 内 JS 封装）：
`wasm.generate_runtime_auth_fields(ret, str_ptr, str_len)`，
返回 ret 处 `[ptr, len, err_ptr, err_flag]` 四个 i32，正常时 (ptr,len) 指向一段**待释放**字符串。

## 四、解禁 qwenwork 渠道

设计文档 `src/docs/design/multi-channel-v2.md` KD-11 写明：
「QwenWork 真请求 200 之前不得加入默认列表」。现已满足，于是：

- `scripts/gateway_daemon.py` 的 `CB_GATEWAY_PROVIDERS` 加入 `qwenwork`
  （不加的话网关一律 400 `unknown_channel`，且 `/v1/models` 不发布该渠道模型）；
- 加进 `selected_models`：`qwenwork/pro`、`qwenwork/flash`、`qwenwork/qwen3.8-max-preview`；
- DSH profile 同步（22 个模型，漂移自检一致）。

## 五、实测

- 本地纯算（零额度）：WASM 不 panic；URL = `…/agent_chat_generation?FetchKeys=llm_model_result&Encode=1`；
  头里有 `Authorization: Bearer COSY.…`、`Cosy-Version: 1.3.2`、`Cosy-Key`、`Cosy-User`、`Cosy-MachineId`。
- 真实请求 **1 条**：HTTP 200，服务端回 `pong`。
- 走 8787 网关：`qwenwork/pro` → `Pong! 🏓 Everything seems to be working.`

## 六、教训

**「版本不兼容」这类结论要先端正证据再下。** 这次两版 WASM 的哈希一模一样，
真正错的是我们自己手写的 WASM 宿主里的一行分配逻辑。
遇到 panic 先做**隔离实验**（改一个变量、跑一遍），再决定要不要升级协议。

## 关联

- 代码：`buddy2api\src\providers\qwenwork\{encode.py,constants.py,chat.py}`、`scripts\gateway_daemon.py`
- 探针：`buddy2api\scripts\probe_qwenwork_132_{callsite,glue_exports,biz,consts,exportmap,chatcall,prepare,encode_local,isolate,live}.py`
- 逆向源：`D:\QwenWorkCN\1.3.2-26101704\resources\app.asar`（用 mmap + 正则捞，265MB 不解压）
