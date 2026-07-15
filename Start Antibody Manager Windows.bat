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
".venv\Scripts\python.exe" app\gate.py
if not exist "app\gate.py" (
    echo.
    echo [Error] app\gate.py was not found.
    echo Please make sure the app folder is complete.
    pause
    exit /b 1
)
echo.
pause