
@echo off
cd /d "%~dp0.."
py src/main.py --vfs scripts/vfs_deep.json
pause
