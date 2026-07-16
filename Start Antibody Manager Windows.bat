@echo off
setlocal
cd /d "%~dp0"

chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

echo ============================================================
echo Antibody Inventory Manager - Windows
echo ============================================================
echo.

if not exist "app\gate.py" (
    echo [Error] app\gate.py was not found.
    echo Please make sure this launcher is beside the app folder.
    echo.
    pause
    exit /b 1
)

set "PYTHON_CMD="
where py >nul 2>&1
if not errorlevel 1 set "PYTHON_CMD=py -3"

if not defined PYTHON_CMD (
    where python >nul 2>&1
    if not errorlevel 1 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
    echo [Error] Python 3 was not found.
    echo Please install Python 3 and enable Add Python to PATH.
    echo.
    pause
    exit /b 1
)

echo Python being used:
%PYTHON_CMD% -c "import sys; print(sys.executable); print(sys.version)"
echo.

echo Checking required packages...
%PYTHON_CMD% -c "import pandas, openpyxl" >nul 2>&1
if errorlevel 1 (
    echo Required packages are missing. Installing them for this Windows user...
    %PYTHON_CMD% -m pip install --user pandas openpyxl
    if errorlevel 1 (
        echo.
        echo [Error] Failed to install pandas or openpyxl.
        pause
        exit /b 1
    )
) else (
    echo Required packages are already installed.
)

echo.
echo Starting Antibody Inventory Manager...
echo.

rem Run the script directly so Python automatically adds the app folder to sys.path.
%PYTHON_CMD% -u "app\gate.py"
set "APP_EXIT_CODE=%errorlevel%"

if not "%APP_EXIT_CODE%"=="0" (
    echo.
    echo [Error] The program stopped with exit code %APP_EXIT_CODE%.
)

echo.
pause
endlocal
