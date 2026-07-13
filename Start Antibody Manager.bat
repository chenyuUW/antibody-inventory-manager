@echo off
cd /d "%~dp0"

echo ==============================================
echo Antibody Inventory Manager
echo ==============================================

if not exist ".venv\Scripts\python.exe" (
    echo Creating Windows virtual environment...
    py -3 -m venv .venv

    if errorlevel 1 (
        echo.
        echo Failed to create the virtual environment.
        echo Please make sure Python is installed on Windows.
        pause
        exit /b 1
    )
)

echo Installing/checking required packages...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install pandas openpyxl

echo.
echo Starting Antibody Inventory Manager...
".venv\Scripts\python.exe" gate.py

echo.
pause