#!/bin/bash

# Antibody Inventory Manager launcher for macOS
# Runs directly with the user's Python installation.
# Required packages are stored locally for each user and Python version,
# outside the shared Box folder.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

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

# Confirm that the application files exist.
if [ ! -f "$SCRIPT_DIR/app/gate.py" ]; then
    echo "[Error] app/gate.py was not found."
    echo
    echo "Please make sure the project folder contains:"
    echo "  app/"
    echo "    gate.py"
    echo "    config.py"
    echo "    data_io.py"
    echo "    add_antibody.py"
    echo "    take_antibody.py"
    echo "    search_inventory.py"
    echo "    utils.py"
    pause_before_close
    exit 1
fi

# Confirm that the Excel inventory file exists.
if [ ! -f "$SCRIPT_DIR/Antibody Inventory Master.xlsx" ]; then
    echo "[Error] Antibody Inventory Master.xlsx was not found."
    echo
    echo "The Excel inventory file must be in the main project folder:"
    echo "  $SCRIPT_DIR"
    pause_before_close
    exit 1
fi

# Locate Python 3.
if command -v python3 >/dev/null 2>&1; then
    SYSTEM_PYTHON="$(command -v python3)"
else
    echo "[Error] Python 3 is not installed or cannot be found."
    echo
    echo "Install Python 3 from python.org, then open this file again."
    pause_before_close
    exit 1
fi

# Detect the Python version, such as 3.9 or 3.14.
PYTHON_VERSION="$(
    "$SYSTEM_PYTHON" -c \
    'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")'
)"

if [ -z "$PYTHON_VERSION" ]; then
    echo "[Error] The Python version could not be detected."
    pause_before_close
    exit 1
fi

echo "[1/3] Using Python $PYTHON_VERSION"
echo "Python location: $SYSTEM_PYTHON"

# Store dependencies outside Box.
#
# Examples:
# Python 3.9:
# ~/Library/Application Support/Antibody Inventory Manager/python3.9/site-packages
#
# Python 3.14:
# ~/Library/Application Support/Antibody Inventory Manager/python3.14/site-packages
USER_PACKAGE_DIR="$HOME/Library/Application Support/Antibody Inventory Manager/python${PYTHON_VERSION}/site-packages"

mkdir -p "$USER_PACKAGE_DIR"

# Tell Python where the locally installed packages are stored.
if [ -n "${PYTHONPATH:-}" ]; then
    export PYTHONPATH="$USER_PACKAGE_DIR:$PYTHONPATH"
else
    export PYTHONPATH="$USER_PACKAGE_DIR"
fi

# Install dependencies only when they are missing.
echo "[2/3] Checking required packages..."

if ! "$SYSTEM_PYTHON" -c "import pandas, openpyxl" >/dev/null 2>&1; then
    echo "Installing pandas and openpyxl for this user..."
    echo "This normally happens only on the first launch."

    # Confirm that pip is available.
    if ! "$SYSTEM_PYTHON" -m pip --version >/dev/null 2>&1; then
        echo "pip was not found. Attempting to install pip..."

        if ! "$SYSTEM_PYTHON" -m ensurepip --upgrade; then
            echo
            echo "[Error] pip could not be installed."
            echo "Please reinstall Python 3 from python.org."
            pause_before_close
            exit 1
        fi
    fi

    # Install packages into this user's local application folder.
    if ! "$SYSTEM_PYTHON" -m pip install \
        --upgrade \
        --target "$USER_PACKAGE_DIR" \
        pandas openpyxl; then

        echo
        echo "[Error] Required packages could not be installed."
        echo "Check the internet connection and try again."
        pause_before_close
        exit 1
    fi

    # Verify that installation succeeded.
    if ! "$SYSTEM_PYTHON" -c "import pandas, openpyxl" >/dev/null 2>&1; then
        echo
        echo "[Error] pandas or openpyxl could not be loaded after installation."
        pause_before_close
        exit 1
    fi
else
    echo "Required packages are already installed."
fi

# Start the application.
echo "[3/3] Starting Antibody Inventory Manager..."
echo

"$SYSTEM_PYTHON" -X utf8 "$SCRIPT_DIR/app/gate.py"
EXIT_CODE=$?

echo
if [ "$EXIT_CODE" -ne 0 ]; then
    echo "[Error] The program closed with error code: $EXIT_CODE"
else
    echo "Antibody Inventory Manager has closed."
fi

pause_before_close
exit "$EXIT_CODE"