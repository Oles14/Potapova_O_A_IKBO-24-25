
@echo off
cd /d "%~dp0.."
py src/main.py --vfs scripts/does_not_exist.json
pause
