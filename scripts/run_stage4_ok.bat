
@echo off
cd /d "%~dp0.."
py src/main.py --vfs scripts/vfs_stage4.json --script scripts/stage4_ok.txt
pause
