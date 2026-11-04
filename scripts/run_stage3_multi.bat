
@echo off
cd /d "%~dp0.."
py src/main.py --vfs scripts/vfs_multi.json
pause
