# search_inventory.py
# Search / Preview inventory function for Antibody Inventory Manager

import pandas as pd

from config import (
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
)

from data_io import load_inventory

from utils import normalize_for_search, safe_cell


DISPLAY_COLUMNS = [
    COL_BOX,
    COL_CD_MARKER,
    COL_COMMON_NAME,
    COL_FLUOROPHORE,
    COL_CATALOG,
    COL_MANUFACTURER,
    COL_CONTAINER_TYPE,
    COL_REMAINING,
    COL_RECOMMENDED_CHANNEL,
    COL_BOX_POSITION,
    COL_RECOMMENDED_DILUTION,
    COL_NOTES,
]


def search_inventory():
    """
    Search / Preview Inventory workflow.

    This function is read-only:
    - It does not modify inventory.
    - It does not write log.
    - It does not create backups.
    """

    while True:
        print("=" * 70)
        print("Search / Preview Inventory")
        print("=" * 70)
        print("1. Search by marker")
        print("2. Search by marker + fluorophore")
        print("3. Search by catalog")
        print("4. General keyword search")
        print("5. Show all inventory")
        print("6. Cancel")
        print("-" * 70)

        choice = input("Select an option: ").strip()

        if choice == "1":
            search_by_marker_flow()

        elif choice == "2":
            search_by_marker_fluorophore_flow()

        elif choice == "3":
            search_by_catalog_flow()

        elif choice == "4":
            general_keyword_search_flow()

        elif choice == "5":
            show_all_inventory_flow()

        elif choice == "6":
            print("\nSearch cancelled.")
            return

        else:
            print("\nInvalid option. Please enter 1, 2, 3, 4, 5, or 6.\n")


def search_by_marker_flow():
    """
    Search by marker.

    Marker is matched against:
    - CD Marker
    - Common Name

    This search uses flexible contains matching.
    """

    marker = input("\nMarker / Target keyword: ").strip()

    if marker == "":
        print("\nMarker cannot be empty.")
        return

    df = load_inventory()

    marker_query = normalize_for_search(marker)

    cd_series = df[COL_CD_MARKER].apply(normalize_for_search)
    common_series = df[COL_COMMON_NAME].apply(normalize_for_search)

    matched = df[
        cd_series.str.contains(marker_query, na=False)
        | common_series.str.contains(marker_query, na=False)
    ].copy()

    print_search_results(matched)


def search_by_marker_fluorophore_flow():
    """
    Search by marker + fluorophore.

    Marker is matched against:
    - CD Marker
    - Common Name

    Fluorophore is matched against:
    - Fluorophore

    This search uses flexible exact matching after normalization.
    """

    marker = input("\nMarker / Target: ").strip()
    fluorophore = input("Fluorophore: ").strip()

    if marker == "":
        print("\nMarker cannot be empty.")
        return

    if fluorophore == "":
        print("\nFluorophore cannot be empty.")
        return

    df = load_inventory()

    marker_query = normalize_for_search(marker)
    fluor_query = normalize_for_search(fluorophore)

    cd_series = df[COL_CD_MARKER].apply(normalize_for_search)
    common_series = df[COL_COMMON_NAME].apply(normalize_for_search)
    fluor_series = df[COL_FLUOROPHORE].apply(normalize_for_search)

    matched = df[
        (
            (cd_series == marker_query)
            | (common_series == marker_query)
        )
        &
        (fluor_series == fluor_query)
    ].copy()

    print_search_results(matched)


def search_by_catalog_flow():
    """
    Search by catalog.

    This uses flexible exact matching after normalization.
    """

    catalog = input("\nCatalog number: ").strip()

    if catalog == "":
        print("\nCatalog cannot be empty.")
        return

    df = load_inventory()

    catalog_query = normalize_for_search(catalog)
    catalog_series = df[COL_CATALOG].apply(normalize_for_search)

    matched = df[catalog_series == catalog_query].copy()

    print_search_results(matched)


def general_keyword_search_flow():
    """
    General keyword search across major columns.

    This uses flexible contains matching.
    """

    keyword = input("\nKeyword: ").strip()

    if keyword == "":
        print("\nKeyword cannot be empty.")
        return

    df = load_inventory()

    query = normalize_for_search(keyword)

    search_columns = [
        COL_BOX,
        COL_CD_MARKER,
        COL_COMMON_NAME,
        COL_FLUOROPHORE,
        COL_CATALOG,
        COL_MANUFACTURER,
        COL_CONTAINER_TYPE,
        COL_NOTES,
    ]

    mask = pd.Series(False, index=df.index)

    for column in search_columns:
        series = df[column].apply(normalize_for_search)
        mask = mask | series.str.contains(query, na=False)

    matched = df[mask].copy()

    print_search_results(matched)


def show_all_inventory_flow():
    """
    Show all inventory records.
    """

    df = load_inventory()

    print("\nShowing all inventory records.")
    print_search_results(df)


def print_search_results(df):
    """
    Print search results in a readable table-like format.
    """

    if len(df) == 0:
        print("\nNo matching antibody found.\n")
        return

    print(f"\nFound {len(df)} matching record(s).\n")

    # Sort results for easier reading
    df = df.copy()
    df["_sort_marker"] = df[COL_COMMON_NAME].astype(str)
    df["_sort_fluor"] = df[COL_FLUOROPHORE].astype(str)
    df = df.sort_values(by=["_sort_marker", "_sort_fluor"], na_position="last")

    # Print compact table
    print("-" * 120)
    header = (
        f"{'#':<4}"
        f"{'Box':<18}"
        f"{'CD Marker':<12}"
        f"{'Common Name':<16}"
        f"{'Fluorophore':<16}"
        f"{'Catalog':<16}"
        f"{'Manufacturer':<14}"
        f"{'Container':<16}"
        f"{'Remain':<8}"
    )
    print(header)
    print("-" * 120)

    for display_index, (_, row) in enumerate(df.iterrows(), start=1):
        line = (
            f"{display_index:<4}"
            f"{truncate(safe_cell(row, COL_BOX), 17):<18}"
            f"{truncate(safe_cell(row, COL_CD_MARKER), 11):<12}"
            f"{truncate(safe_cell(row, COL_COMMON_NAME), 15):<16}"
            f"{truncate(safe_cell(row, COL_FLUOROPHORE), 15):<16}"
            f"{truncate(safe_cell(row, COL_CATALOG), 15):<16}"
            f"{truncate(safe_cell(row, COL_MANUFACTURER), 13):<14}"
            f"{truncate(safe_cell(row, COL_CONTAINER_TYPE), 15):<16}"
            f"{safe_cell(row, COL_REMAINING):<8}"
        )

        print(line)
        print("-" * 120)

        # Secondary information table
        print()
        print("    " + "-" * 76)

        secondary_header = (
            f"    "
            f"{'Recommended Channel':<24}"
            f"{'Recommended Dilution':<26}"
            f"{'Box Position':<20}"
        )
        print(secondary_header)

        print("    " + "-" * 76)

        secondary_values = (
            f"    "
            f"{truncate(safe_cell(row, COL_RECOMMENDED_CHANNEL), 23):<24}"
            f"{truncate(safe_cell(row, COL_RECOMMENDED_DILUTION), 25):<26}"
            f"{truncate(safe_cell(row, COL_BOX_POSITION), 19):<20}"
        )
        print(secondary_values)

        print("    " + "-" * 76)
        print()

    if len(df) > 30:
        print("\nNote: Many records were found. Consider using a more specific search term.")

    print("")


def truncate(value, max_length):
    """
    Truncate long text for table display.
    """

    value = str(value)

    if len(value) <= max_length:
        return value

    return value[: max_length - 3] + "..."


if __name__ == "__main__":
    search_inventory()