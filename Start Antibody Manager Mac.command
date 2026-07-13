#!/bin/bash

# Antibody Inventory Manager launcher for macOS
# Always run from the folder containing this file.
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

VENV_DIR="$SCRIPT_DIR/.venv"
PYTHON_BIN="$VENV_DIR/bin/python"

# Keep Python and Terminal output in UTF-8.
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
export LC_ALL="${LC_ALL:-en_US.UTF-8}"
export LANG="${LANG:-en_US.UTF-8}"

pause_before_close() {
    echo
    read -r -p "Press Enter to close this window..."
}

printf '\n============================================================\n'
printf ' Antibody Inventory Manager - macOS\n'
printf '============================================================\n\n'

# Confirm that the launcher is beside the main program.
if [ ! -f "$SCRIPT_DIR/gate.py" ]; then
    echo "[Error] gate.py was not found."
    echo
    echo "This launcher must be placed in the same folder as:"
    echo "  gate.py"
    echo "  config.py"
    echo "  data_io.py"
    echo "  add_antibody.py"
    echo "  take_antibody.py"
    echo "  search_inventory.py"
    echo "  utils.py"
    echo "  Antibody Inventory Master.xlsx"
    pause_before_close
    exit 1
fi

# Locate Python 3. macOS does not reliably include Python by default.
if command -v python3 >/dev/null 2>&1; then
    SYSTEM_PYTHON="$(command -v python3)"
else
    echo "[Error] Python 3 is not installed or cannot be found."
    echo
    echo "Install Python 3 from python.org, then open this file again."
    pause_before_close
    exit 1
fi

# Create an isolated virtual environment on first launch.
if [ ! -x "$PYTHON_BIN" ]; then
    echo "[1/3] Creating the Mac virtual environment..."

    if ! "$SYSTEM_PYTHON" -m venv "$VENV_DIR"; then
        echo
        echo "[Error] The virtual environment could not be created."
        echo "Please reinstall Python 3 and try again."
        pause_before_close
        exit 1
    fi
else
    echo "[1/3] Virtual environment already exists."
fi

# Install dependencies only when they are missing.
echo "[2/3] Checking required packages..."
if ! "$PYTHON_BIN" -c "import pandas, openpyxl" >/dev/null 2>&1; then
    echo "Installing pandas and openpyxl..."

    if ! "$PYTHON_BIN" -m pip install --upgrade pip; then
        echo
        echo "[Error] pip could not be updated."
        echo "Check the internet connection and try again."
        pause_before_close
        exit 1
    fi

    if ! "$PYTHON_BIN" -m pip install pandas openpyxl; then
        echo
        echo "[Error] Required packages could not be installed."
        echo "Check the internet connection and try again."
        pause_before_close
        exit 1
    fi
else
    echo "Required packages are already installed."
fi

# Start the application.
echo "[3/3] Starting Antibody Inventory Manager..."
echo
"$PYTHON_BIN" -X utf8 "$SCRIPT_DIR/gate.py"
EXIT_CODE=$?

echo
if [ "$EXIT_CODE" -ne 0 ]; then
    echo "[Error] The program closed with error code: $EXIT_CODE"
else
    echo "Antibody Inventory Manager has closed."
fi

pause_before_close
exit "$EXIT_CODE"
