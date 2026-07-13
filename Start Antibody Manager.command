@echo off
cd /d "%~dp0"

rem Force Windows terminal and Python to use UTF-8
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

echo ==============================================
echo Antibody Inventory Manager
echo ==============================================

if not exist ".venv\Scripts\python.exe" (
    echo Creating Windows virtual environment...
    py -3 -m venv .venv

    if errorlevel 1 (
        echo.
        echo Failed to create the virtual environment.
        echo Please install Python 3 for Windows.
        pause
        exit /b 1
    )
)

echo Checking required packages...
".venv\Scripts\python.exe" -m pip install pandas openpyxl

echo.
echo Starting Antibody Inventory Manager...
".venv\Scripts\python.exe" -X utf8 gate.py

echo.
pause