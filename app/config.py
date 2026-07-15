# config.py
# Configuration file for Antibody Inventory Manager

from pathlib import Path


APP_NAME = "Antibody Inventory Manager"
VERSION = "v1.0"

# app/config.py 所在目录
APP_DIR = Path(__file__).resolve().parent

# 项目最外层目录
PROJECT_DIR = APP_DIR.parent

# Excel inventory file
INVENTORY_FILE = PROJECT_DIR / "Antibody Inventory Master.xlsx"

# Backup folder
BACKUP_DIR = PROJECT_DIR / "backups"

# Sheet names
INVENTORY_SHEET = "Sheet1"
LOG_SHEET = "Log"

# Inventory column names
COL_BOX = "box"
COL_CD_MARKER = "CD Marker"
COL_COMMON_NAME = "Common Name"
COL_FLUOROPHORE = "Fluorophore"
COL_CATALOG = "Catalog"
COL_MANUFACTURER = "Manufacturer"
COL_CONTAINER_TYPE = "Container_Type"
COL_REMAINING = "Remaining"
COL_RECOMMENDED_CHANNEL = "Recommended Channel"
COL_BOX_POSITION = "Box Position"
COL_RECOMMENDED_DILUTION = "Recommended dilution"
COL_NOTES = "Notes"

INVENTORY_COLUMNS = [
    COL_BOX,
    COL_CD_MARKER,
    COL_COMMON_NAME,
    COL_FLUOROPHORE,
    COL_CATALOG,
    COL_MANUFACTURER,
    COL_CONTAINER_TYPE,
    COL_REMAINING,
    COL_NOTES,
    COL_RECOMMENDED_CHANNEL,
    COL_BOX_POSITION,
    COL_RECOMMENDED_DILUTION,
]

# Log column names
LOG_COLUMNS = [
    "Time",
    "Action",
    "CD Marker",
    "Common Name",
    "Fluorophore",
    "Catalog",
    "Container_Type",
    "Change",
    "Before",
    "After",
    "Notes",
]