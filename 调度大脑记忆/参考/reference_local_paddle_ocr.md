# 本地 PaddleOCR 通路（扫描件 PDF 文本提取）

> type: reference | 创建：2026-09-08 | 来源：课程思政竞赛通知 17 页扫描件实测
> 场景：手头只有扫描版 PDF（无文本层），模型不能直接读图时，用本机 PaddleOCR 提取全文。

## 环境事实

- 安装位置：**系统 Python 3.12**（`C:\Users\郭永涛\AppData\Local\Programs\Python\Python312\`），包版本 `paddleocr 2.10.0` + `paddlepaddle 2.6.2`
- 隔离 venv（`~/.workbuddy/binaries/python/envs/default`）中另有备用 `rapidocr-onnxruntime`（2026-09-08 已装，含 onnxruntime）

## 标准用法（已验证）

1. PDF → PNG：pymupdf（`fitz`）逐页渲染，150 dpi（`Matrix(150/72)`）对 A4 公文足够清晰
2. PNG → 文本：PaddleOCR 逐页 `ocr(img, cls=True)`，按 y 序拼接 `item[1][0]`
3. **关键坑（必踩）**：paddle 2.6.2 与新版 protobuf 冲突，报 `TypeError: Descriptors cannot be created directly`。解法：运行时加环境变量 `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`（纯 Python 解析，17 页约 1–2 分钟，可接受；**不要**降级 protobuf，怕破坏其他包）
4. 中文路径下脚本运行正常；输出写 UTF-8 文本文件，逐页 flush 防中途失败丢结果

```bash
PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python \
  "C:/Users/郭永涛/AppData/Local/Programs/Python/Python312/python.exe" run_ocr.py
```

## 效果实测

- 郴州市课程思政竞赛通知（红头文件+表格）17 页全部识别成功，正文/表格文字准确，仅表格单元格顺序偶有错位、盖章区有杂字，人工校对成本低

## 决策规则

- 扫描件 PDF → **首选本机 PaddleOCR**（离线、免费、中文公文效果好）
- 备选：rapidocr（venv 内）、tencentcloud-ocr（需密钥，未配置）、网页找官方电子版（官方通知常无网页版，先搜一轮再 OCR）
- 正文 PDF（有文本层）直接 pdfplumber/pymupdf 提取，不走 OCR
