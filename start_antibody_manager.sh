#!/usr/bin/env bash
set -e

# Always work from the folder containing this launcher.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="$SCRIPT_DIR/.venv"
PYTHON_CMD="python3"

printf '\n============================================================\n'
printf ' Antibody Inventory Manager - Setup and Launch\n'
printf '============================================================\n\n'

# Check that Python 3 is available.
if ! command -v "$PYTHON_CMD" >/dev/null 2>&1; then
    echo "[Error] Python 3 is not installed."
    echo "Install it with: sudo apt install python3 python3-venv"
    read -r -p "Press Enter to close..."
    exit 1
fi

# Check that the main program exists.
if [ ! -f "$SCRIPT_DIR/gate.py" ]; then
    echo "[Error] gate.py was not found in:"
    echo "$SCRIPT_DIR"
    echo
    echo "Put this launcher in the same folder as gate.py."
    read -r -p "Press Enter to close..."
    exit 1
fi

# Create the virtual environment on first launch.
if [ ! -d "$VENV_DIR" ]; then
    echo "[1/3] Creating virtual environment..."
    if ! "$PYTHON_CMD" -m venv "$VENV_DIR"; then
        echo
        echo "[Error] Could not create the virtual environment."
        echo "On Ubuntu, install venv support with:"
        echo "sudo apt install python3-venv"
        read -r -p "Press Enter to close..."
        exit 1
    fi
else
    echo "[1/3] Virtual environment already exists."
fi

# Activate the environment.
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# Install/update required packages only when missing.
echo "[2/3] Checking required Python packages..."
if ! python -c "import pandas, openpyxl" >/dev/null 2>&1; then
    echo "Installing pandas and openpyxl..."
    python -m pip install --upgrade pip
    python -m pip install pandas openpyxl
else
    echo "Required packages are already installed."
fi

# Start the program.
echo "[3/3] Starting Antibody Inventory Manager..."
echo
python gate.py

EXIT_CODE=$?
echo
if [ "$EXIT_CODE" -ne 0 ]; then
    echo "The program closed with error code: $EXIT_CODE"
    read -r -p "Press Enter to close..."
fi
