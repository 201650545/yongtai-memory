---
name: lesson-数据职责别挂rAF-20261020
description: 把"首次加载真实数据"塞进 requestAnimationFrame ⇒ 页面隐藏（DSH 窗口被遮挡/最小化，document.hidden===true）时 rAF 永久不跑，画布永远显示内置 DEMO 假数据且不报错。2026-10-20 实证：经纬画布首屏显示「文案/设计/汇总」，而 graph.json 里是另外 4 个节点。修法＝数据加载直呼，rAF 只放摆版面的活并加 setTimeout 兜底
metadata:
  node_type: memory
  type: 教训
  created: 2026-10-20
  适用: 任何"首屏/首次加载/初始化"逻辑，尤其是插件面板、右栏 tab、懒挂载组件；以及任何把「数据请求」和「版面计算」写在同一段初始化里的代码
type: lesson
updated: 2026-10-20
---

# 教训：数据职责不能挂在动画帧上（rAF 是「可见才跑」）

## 一、症状

经纬画布（DSH 右栏 tab）打开后，画的是 `copy / design / merge`「文案 / 设计 / 汇总」，
而 `app/data/graph.json` 里明明是 `intake / art / output / merge` 另一套 4 个节点。

- **不报错**：console 干净，`window.onerror`、`unhandledrejection` 全空，`console.warn` 一条没有。
- **fetch 没发出去**：hook `window.fetch` 后切 tab 重挂载，记录里**只有 `jingwei/models`，没有 `jingwei/data/graph.json`**。
- **会「自己好」**：按 R 键（内部走 `reload`）或切走再切回来，节点就对了 —— 这个假象最容易把人带偏去查"偶发/时序/缓存"。

## 二、根因

`client.js` 的初始化是这么写的：

```js
rebuild(false);
requestAnimationFrame(() => {
  fit();          // 摆版面
  reload(false);  // ← 首次真实数据加载，被一起塞进了 rAF
});
```

而 **rAF 只在页面可见时才触发**。DSH 窗口被遮挡/最小化时：

```js
document.hidden === true      // 实测确认
document.visibilityState === 'hidden'
// 此时 requestAnimationFrame 的回调永远不会执行
```

⇒ `reload` 永不执行 ⇒ 画布停在初始值 `normalize(DEMO)`（内置三节点假数据）。
因为"画得出东西"，所以既不空屏也不报错，只是一个**错的东西**。

## 三、修法

**分开职责**：数据加载是数据职责，不该依赖动画帧。

```js
reload(false);                     // 直接调，不等帧

let fitted = false;                // fit 仍要等一帧（要实测节点高度）
const fitOnce = () => {
  if (fitted || destroyed) return;
  fitted = true;
  fit();
};
requestAnimationFrame(fitOnce);    // 可见时：下一帧
setTimeout(fitOnce, 300);          // 隐藏时兜底：rAF 不跑也能摆正
```

提交：经纬源仓 `f59d9df`，public 快照 `8f4fb9f`。

## 四、验证方式（怎么才算真验过）

1. `Page.reload` 后**不做任何额外动作**，首屏节点 id 必须直接是真实数据；
2. 在 `document.hidden === true`（窗口被遮挡）下复现，同样要正常；
3. 抓 fetch 记录，确认 `jingwei/data/graph.json` **确实被请求过**；
4. 回归 `node scripts/test_all.mjs`（103 断言）全绿。

## 五、可迁移的判断力

1. **rAF / setTimeout / requestIdleCallback 三者的触发条件不同**：
   rAF 要「可见」，rIC 要「空闲」，只有 setTimeout 基本无条件（后台标签也会被节流但会跑）。
   把「必须发生的事」交给 rAF，就是赌页面一直可见。
2. **「不报错的错」比崩溃更难查**。这次能定位靠的是三件事同时做：
   读源码找初始化路径 → hook fetch 看请求**有没有发** → 检查 `document.hidden`。
   只看 DOM 会以为是渲染问题（节点就是画错了嘛），只看 console 会以为什么都没发生。
3. **「重载一下就好了」是重要线索，不是噪音**。它指向"初始状态没被正确覆盖"，
   要顺着"初次挂载和后来触发的是不是同一条路径"去查，而不是去查缓存。
4. 同类陷阱：把「保存/上报」放进 rAF（隐藏时丢数据）、把「鉴权刷新」放进 rAF（隐藏时过期）。
