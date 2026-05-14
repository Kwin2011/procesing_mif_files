@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo.
echo  ╔══════════════════════════════════╗
echo  ║   MIF Rule Admin — rule tester   ║
echo  ╚══════════════════════════════════╝
echo.

python rule_admin.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Program exited with error code %errorlevel%
)
pause
