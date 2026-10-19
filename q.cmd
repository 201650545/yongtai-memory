@echo off
rem q.cmd: one-line memory retrieval wrapper (calls q.ps1)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0q.ps1" %*