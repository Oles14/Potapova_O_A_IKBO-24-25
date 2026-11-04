
@echo off
cd /d "%~dp0.."
py src/main.py --vfs scripts/vfs_multi.json --script scripts/stage3_ok.txt
pause
