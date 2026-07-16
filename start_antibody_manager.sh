from pathlib import Path

output = Path("/mnt/data/start_antibody_manager_local.sh")

script = r'''#!/usr/bin/env bash

# Antibody Inventory Manager launcher for Ubuntu / Linux
# Uses a per-user virtual environment stored outside the shared project folder.
# This prevents Box Drive from uploading thousands of .venv files.

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

PYTHON_CMD="python3"
APP_FILE="$SCRIPT_DIR/app/gate.py"
LOCAL_ENV_BASE="${XDG_DATA_HOME:-$HOME/.local/share}/Antibody Inventory Manager"
VENV_DIR="$LOCAL_ENV_BASE/venv"

pause_before_close() {
    echo
    read -r -p "Press Enter to close..."
}

printf '\n============================================================\n'
printf ' Antibody Inventory Manager - Ubuntu / Linux\n'
printf '============================================================\n\n'

# Check that Python 3 is available.
if ! command -v "$PYTHON_CMD" >/dev/null 2>&1; then
    echo "[Error] Python 3 is not installed."
    echo
    echo "Install it with:"
    echo "sudo apt install python3 python3-venv"
    pause_before_close
    exit 1
fi

echo "Python being used:"
command -v "$PYTHON_CMD"
"$PYTHON_CMD" --version
echo

# Check that the application file exists.
if [ ! -f "$APP_FILE" ]; then
    echo "[Error] app/gate.py was not found."
    echo
    echo "Expected location:"
    echo "$APP_FILE"
    echo
    echo "Keep this launcher in the main project folder,"
    echo "with gate.py inside the app folder."
    pause_before_close
    exit 1
fi

# Create the local application folder outside Box Drive.
if ! mkdir -p "$LOCAL_ENV_BASE"; then
    echo "[Error] Could not create the local application folder:"
    echo "$LOCAL_ENV_BASE"
    pause_before_close
    exit 1
fi

# Create a per-user virtual environment only when missing.
if [ ! -x "$VENV_DIR/bin/python" ]; then
    echo "Creating the local Python environment..."
    echo "Location: $VENV_DIR"
    echo

    if ! "$PYTHON_CMD" -m venv "$VENV_DIR"; then
        echo
        echo "[Error] Could not create the local Python environment."
        echo
        echo "On Ubuntu, install virtual environment support with:"
        echo "sudo apt install python3-venv"
        pause_before_close
        exit 1
    fi
fi

LOCAL_PYTHON="$VENV_DIR/bin/python"

echo "Checking required packages..."

if ! "$LOCAL_PYTHON" -c "import pandas, openpyxl" >/dev/null 2>&1; then
    echo "Installing pandas and openpyxl into the local user environment..."
    echo

    if ! "$LOCAL_PYTHON" -m pip install --upgrade pip; then
        echo
        echo "[Error] pip could not be updated."
        pause_before_close
        exit 1
    fi

    if ! "$LOCAL_PYTHON" -m pip install pandas openpyxl; then
        echo
        echo "[Error] Required packages could not be installed."
        echo "Check the internet connection and try again."
        pause_before_close
        exit 1
    fi
else
    echo "Required packages are already installed."
fi

echo
echo "Starting Antibody Inventory Manager..."
echo

"$LOCAL_PYTHON" "$APP_FILE"
EXIT_CODE=$?

echo
if [ "$EXIT_CODE" -ne 0 ]; then
    echo "[Error] The program stopped with exit code $EXIT_CODE."
    pause_before_close
fi

exit "$EXIT_CODE"
'''

output.write_text(script, encoding="utf-8", newline="\n")
output.chmod(0o755)

print(f"Created: {output}")
