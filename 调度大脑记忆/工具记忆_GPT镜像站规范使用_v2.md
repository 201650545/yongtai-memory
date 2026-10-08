# 工具记忆：ChatGPT 镜像站规范使用与快速使用 v2

> 2026-09-27 整合稿。来源：GPT镜像站送审流程手册（D:\Work\AI平台\docs\runbooks\GPT镜像站送审流程.md）+ 2026-09-27 AI记忆卡三轮送审实测。
> 旧散篇 feedback 保留不动，本文为整合正稿；与手册冲突时以手册 + 本文较新者为准。

## 一、快速打开与标签规范

1. **只开新标签**：`opencli browser $S tab new <url>`，绝不点击/覆盖别人已打开的标签或链接。会话码用 `opencli profile list` 现取（当前 `d5vtd5bg`），daemon 报 stale 先 `opencli daemon restart`。
2. **eval 跟随活跃标签**：opencli 的 eval 永远打在当前活跃标签上——多 Agent 并行时这是抢占与串台的根源。每次注入/发送前必须回读 URL 与基准比对，不符即判被抢占。
3. **被抢占的红线**：不抢回。立即新开自己的标签重做，并把「跳转→切档→注入→发送」压缩为连续执行，最小化被抢窗口。
4. **会话一致性**：一个任务从哪个聊天窗口开始就留在哪（≤3 轮追问同窗口续，GPT 保上下文）。发现会话内出现**非己方消息（交叉污染）**→ 立即弃用该会话，新开对话发自包含版问题，绝不继续。
5. **备份链接**：进入会话页立即记下完整 `/c/<id>` 网址；更可靠的是发送后立刻 `fetch('/backend-api/conversation/<id>')` 归档全文（同源即可，不依赖标签存活）。标签被切走时先从侧边栏历史按标题找回 URL，避免重发浪费轮次。

## 二、模型选择：Extended 闸门（不可绕过）

1. **每次发送前**直接读 `button.__composer-pill` 文本，必须是 Extended（文案随上游漂移，只认现场 pill，不写死档位名）。
2. hydration 闸门：pill 显示占位值 "Model" 时不可点，轮询等到 Auto/Extended 再操作。
3. 切换方法：对 pill 合成完整指针序列（pointerover→…→mouseup）+ 原生 `.click()` 开 Radix 菜单，在 `[role=menuitemradio]` 里选含 "Extended" 的项，再同套事件点击；等 pill 文本变 Extended 才算成。刷新/换对话/回历史都会重置回 Auto，无例外。

## 三、注入与发送

1. **composer 判别（0×0 陷阱）**：注入前量几何尺寸——`getBoundingClientRect().width>10` 的才是真输入框。textarea 宽高 0×0 是隐形 fallback，真 composer 常是 contenteditable（新对话页也可能是可见 textarea，以实测尺寸为准）。
2. **注入**：一律 base64 + `atob` + TextDecoder 解码 + `execCommand('insertText')`（focus + selectAll 后替换写入）。native setter + input 事件 React 收不到，send-button 不会出现。长文本直接 fill 只进第一段，禁用。
3. **Windows 传参坑**：多行 JS 必须压单行（或经 Python 生成）；URL/JS 里的 `&` 会炸 cmd，用 `\u0026` 规避；复杂 JS 统一由 Python `subprocess(shell=False)` 生成单行脚本文件再执行。
4. **发送**：注入后等 ~600ms 让 React 刷新，`[data-testid=send-button]` 出现后完整指针序列 + click；若无该按钮，枚举 composer 区域按钮（aria-label/testid 匹配 send|submit 且非 voice/stop）。发送回执必须核对：userMsgs +1、stop 按钮出现、注入长度与 textarea/contenteditable 内容一致（防误发空消息）。
5. **daemon/CLI 版本不一致**（stale 报错）：先 `opencli daemon restart`，再 `profile list` 现取会话码。

## 四、结果取回与归档

1. **首选 backend-api**：完成后 `fetch('/backend-api/conversation/<id>',{headers:{accept:'application/json'}})` 拿全量 JSON（实测 116KB 级无损），解析 mapping 里 author.role=assistant 的 parts，按 create_time 排序拼接。DOM innerText 只做校验，不做主通道（虚拟滚动/被切走都会丢内容）。
2. 大文本分块取回：JSON.stringify 切片逐段取，**每段独立 json.loads 再拼接**；长文本走 `encodeURIComponent` 分段 + 本地 unquote。
3. 完成判定：stop 按钮消失 + 连续两次长度不再增长；Extended 思考 1–3 分钟起步、深度问题可达 15 分钟，`streaming:true len:0` 属正常。
4. **回复归属判定**：共享账号池下多 Agent 并发，必须按 user 消息精确特征（长度/开头文本）配对确认 assistant 回复归属，逐条核对再归档。
5. 全文先落盘归档（项目正库目录），再汇报摘要；汇报必须给全文绝对路径。

## 五、文档粘贴规范

1. 只贴**纯文本**（Markdown 源码可以）；富文本/HTML 不贴。
2. 超长文档不直接贴：拆成 ≤2 个长输出问题的多轮（单任务 ≤3 轮、每窗口 ≤24 轮），或走 GitHub 强读（见六）。
3. 注入用 base64 路径天然规避富文本问题；粘贴动作本身（人工）也建议从纯文本编辑器中转。

## 六、提问方法：GitHub 强读（2026-09-28 更新：公开仓 + 强读已验证 ✅）

- **政策演变**：09-27 初版为「私有仓+精选文档+送审前 push」；09-28 郭老师升级拍板——**小项目先公开，产品成熟后再转私有**。理由：GPT（镜像账号池）无法登录读取私有仓，公开后 GPT 网页浏览可直接强读，回复质量显著更高。
- **仓库**：`https://github.com/201650545/listenloop-curated`（现已公开，匿名可访问）。
- **范围（精选）**：ListenLoop Obsidian 正库（`D:\Work\AI精听训练器`）中的架构与设计类文档——README、00_项目驾驶舱_可视化中心、01_商业与战略规划、02_工程架构与系统设计全部；**不含**开发日志流水、03_归档目录、GPT 评审原文、任何密钥/凭证/个人隐私内容。
- **时机**：每次送审前 push 一次（`git -C "D:/Work/AI精听训练器/05_发布与问诊/listenloop-curated" add -A && commit && push`，走 `http.proxy=http://127.0.0.1:7890`），提示词精确列出文件路径清单要求 GPT 强读。
- **已验证（2026-09-28）**：GPT 可正常读取公开仓文档并准确复述内容（红线表格逐字匹配）——强读链路闭环。
- **红线**：密钥/凭证/个人隐私永不入仓；开发日志与评审原文暂不外发；产品成熟后整体转私有（届时需重新解决 GPT 读取授权）。
- **建仓与推送流程**：从 `D:\Work\AI精听训练器\` 同步精选文档到 `D:\Work\AI精听训练器\05_发布与问诊\listenloop-curated` → `git -C <仓> add -A && commit && push`（走既有代理）→ 提示词写「请先读 <repo>/<path> 后再…」。
- **红线**：密钥/凭证/个人隐私永不入仓；开发日志与评审原文（含 GPT 输出）暂不外发；建仓前把精选清单给郭老师过目一次。

### ✅ 已落地（2026-09-27 深夜，郭老师授权）

- **私有仓已建成**：`https://github.com/201650545/listenloop-curated`（private，经既有 git 凭据调 GitHub API 代建，无需 gh CLI）。
- **首次推送完成**：本地仓 `D:\Work\AI精听训练器\05_发布与问诊\listenloop-curated`（commit `ac2d269`），20 篇精选文档已推送至 main。
- **后续送审前 push 流程**：正库文档更新后 → 拷贝到本地仓 → `git -C "D:/Work/AI精听训练器/05_发布与问诊/listenloop-curated" add -A && git commit && git push`（走 7890 代理）。
- **安全红线（新增）**：git credential fill 的输出不得打印（PAT 会随工具输出暴露进会话记录）——凭据只允许在 Python 进程内存中读取使用；本次暴露的 token 建议在 GitHub 设置中轮换。

## 七、流程提速清单（实测有效）

1. 账号池 → 跳转 → 切档 → 注入 → 发送五步合并连续执行，被抢窗口最小化。
2. 发送后立即 backend-api 归档，省掉 DOM 轮询窗口与丢失风险。
3. Extended 等待期（1–3 分钟）不做无关操作占用桥接。
4. daemon stale / 会话码轮换 / 0×0 composer / `&` 炸 cmd / 多行 JS——五个高频坑全部有固定解法，遇错先对照本文而非重新探索。
