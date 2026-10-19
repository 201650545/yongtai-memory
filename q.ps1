# q.ps1 — memory retrieval one-liner (wraps local-knowledge-engine query_evidence.py)
param([Parameter(ValueFromRemainingArguments=$true)]$Rest)
$py = "C:\Users\郭永涛\AppData\Local\Programs\Python\Python312\python.exe"
if (-not (Test-Path $py)) { $py = "python" }
& $py "D:\Work\元智能\10_AI自成长引擎\技能库\local-knowledge-engine\scripts\query_evidence.py" @Rest