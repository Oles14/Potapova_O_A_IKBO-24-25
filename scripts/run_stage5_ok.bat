
@echo off
cd /d "%~dp0.."
py src/main.py --vfs scripts/vfs_stage5.json --script scripts/stage5_ok.txt
pause
