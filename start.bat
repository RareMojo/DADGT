@echo off
setlocal EnableDelayedExpansion

set SCRIPT_DIR=%~dp0

set PATH=%SCRIPT_DIR%;%PATH%

python src\main\main.py -m 1

pause
