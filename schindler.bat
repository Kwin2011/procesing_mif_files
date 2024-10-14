@echo off
cd /d "%~dp0" || exit /b 1
poetry run python main.py || exit /b 1
