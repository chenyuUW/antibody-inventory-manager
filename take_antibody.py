# take_antibody.py
# Take antibody function for Antibody Inventory Manager

from datetime import datetime

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
)

from data_io import (
    load_inventory,
    save_inventory,
    append_log,
    get_latest_take_log,
)

from utils import (
    normalize_for_search,
    ask_yes_no,
    ask_positive_integer,
    print_antibody_details,
    print_multiple_results,
    print_last_bottle_warning,
    safe_cell,
)


def take_antibody():
    """
    Main Take Antibody workflow.

    User can search by:
    1. Catalog
    2. Marker + Fluorophore

    Inventory is only updated when one unique antibody entry is confirmed.
    """

    while True:
        print("=" * 70)
        print("Take Antibody")
        print("=" * 70)
        print("Search by:")
        print("1. Catalog number")
        print("2. Marker + Fluorophore")
        print("3. Cancel")
        print("-" * 70)

        choice = input("Select an option: ").strip()

        if choice == "1":
            result = search_by_catalog_flow()

            if result == "done":
                return

        elif choice == "2":
            result = search_by_marker_fluorophore_flow()

            if result == "done":
                return

        elif choice == "3":
            print("\nTake antibody cancelled.")
            return

        else:
            print("\nInvalid option. Please enter 1, 2, or 3.\n")


def search_by_catalog_flow():
    """
    Search inventory by catalog number.
    """

    catalog = input("\nCatalog number: ").strip()

    if catalog == "":
        print("\nCatalog cannot be empty.")
        return "retry"

    if normalize_for_search(catalog) == "UNKNOWN":
        print('\n"Unknown" is not a useful catalog search term.')
        print("Please search by Marker + Fluorophore instead.")
        return "retry"

    df = load_inventory()

    matched = search_by_catalog(df, catalog)

    return handle_search_results(df, matched, search_context="catalog")


def search_by_marker_fluorophore_flow():
    """
    Search inventory by marker + fluorophore.

    Marker is matched against both:
    - CD Marker
    - Common Name

    Fluorophore is matched against:
    - Fluorophore
    """

    marker = input("\nMarker / Target: ").strip()
    fluorophore = input("Fluorophore: ").strip()

    if marker == "":
        print("\nMarker cannot be empty.")
        return "retry"

    if fluorophore == "":
        print("\nFluorophore cannot be empty.")
        return "retry"

    df = load_inventory()

    matched = search_by_marker_and_fluorophore(df, marker, fluorophore)

    return handle_search_results(df, matched, search_context="marker_fluorophore")


def search_by_catalog(df, catalog):
    """
    Return rows matching catalog exactly after normalization.
    """

    catalog_query = normalize_for_search(catalog)

    catalog_series = df[COL_CATALOG].apply(normalize_for_search)

    matched = df[catalog_series == catalog_query].copy()

    return matched


def search_by_marker_and_fluorophore(df, marker, fluorophore):
    """
    Return rows where:

    (CD Marker matches OR Common Name matches)
    AND Fluorophore matches

    All matching is normalized.
    """

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

    return matched


def handle_search_results(df, matched, search_context):
    """
    Handle 0, 1, or multiple search results.

    If exactly one result:
        show full details
        ask visual confirmation
        take quantity
        update inventory
        log action

    If multiple:
        show results
        route based on catalog/container logic
    """

    result_count = len(matched)

    if result_count == 0:
        print("\nNo matching antibody found.")
        print("Please check spelling or try another search method.\n")
        return "retry"

    if result_count == 1:
        matched_index = matched.index[0]
        return confirm_and_take(df, matched_index)

    print_multiple_results(matched)
    return handle_multiple_results(df, matched, search_context)


def handle_multiple_results(df, matched, search_context):
    """
    Handle cases where search returns multiple rows.

    Logic:
    - If multiple rows have different catalog numbers:
        ask user to search by catalog.
    - If same catalog appears in multiple rows:
        ask user to specify Container_Type.
    - If Container_Type reduces to one row:
        proceed to confirmation.
    - If still not unique:
        stop and ask user to check inventory table.
    """

    unique_catalogs = get_unique_normalized_values(matched, COL_CATALOG)

    if len(unique_catalogs) > 1:
        print("\nMultiple antibodies were found with different catalog numbers.")
        print("Please use the catalog number to take the antibody.")

        while True:
            print("\nNext step:")
            print("1. Search by catalog")
            print("2. Search again")
            print("3. Cancel")

            choice = input("Select an option: ").strip()

            if choice == "1":
                return search_by_catalog_flow()

            if choice == "2":
                return "retry"

            if choice == "3":
                print("\nTake antibody cancelled.")
                return "done"

            print("Invalid option. Please enter 1, 2, or 3.")

    print("\nMultiple entries were found for the same catalog.")
    print("This may be due to Standard_vial and Aliquot entries.")

    return resolve_by_container_type(df, matched)


def resolve_by_container_type(df, matched):
    """
    Ask user to specify Container_Type when catalog alone is not enough.
    """

    container_types = get_display_unique_values(matched, COL_CONTAINER_TYPE)

    if container_types:
        print("\nAvailable container types:")
        for container in container_types:
            print(f"- {container}")

    while True:
        print("\nPlease specify container type.")
        print("Examples: Aliquot, Standard_vial")
        print("Or type 'back' to search again.")

        container_input = input("Container type: ").strip()

        if container_input.lower() == "back":
            return "retry"

        if container_input == "":
            print("Container type cannot be empty.")
            continue

        container_query = normalize_for_search(container_input)
        container_series = matched[COL_CONTAINER_TYPE].apply(normalize_for_search)

        narrowed = matched[container_series == container_query].copy()

        if len(narrowed) == 0:
            print("\nNo matching entry found with that container type.")
            print("Please try again.")
            continue

        if len(narrowed) == 1:
            matched_index = narrowed.index[0]
            return confirm_and_take(df, matched_index)

        print_multiple_results(narrowed)
        print("\nStill multiple matches after specifying container type.")
        print("Inventory was NOT changed.")
        print("Please check the inventory table manually before taking this antibody.")

        return "done"


def confirm_and_take(df, row_index):
    """
    Show antibody details, ask user to confirm identity,
    then ask quantity and update inventory.

    The user may optionally enter their name or an operation note.
    This note is saved only in the Log sheet and does not change
    the antibody's permanent Notes field in the inventory table.
    """

    row = df.loc[row_index]

    print("\nOne matching antibody found:\n")
    print_antibody_details(row)

    confirm = ask_yes_no("Is this the antibody you want to take?")

    if not confirm:
        print("\nOkay. Returning to search.")
        return "retry"

    current_remaining = int(df.loc[row_index, COL_REMAINING])

    if current_remaining <= 0:
        print("\nThis antibody is already marked as OUT OF STOCK.")

        latest_take = get_latest_take_log(
            catalog=safe_cell(row, COL_CATALOG),
            container_type=safe_cell(row, COL_CONTAINER_TYPE),
        )

        if latest_take:
            print("\nLatest recorded take operation:")
            print("-" * 70)
            print(f"Time: {latest_take['Time'] or 'Unknown'}")
            print(f"Note: {latest_take['Notes'] or 'No note recorded'}")
            print("-" * 70)
        else:
            print("\nNo previous take record was found in the Log sheet.")

        print("Inventory was NOT changed.")
        return "done"

    print(f"\nCurrent remaining: {current_remaining}")

    quantity = ask_positive_integer(
        "How many bottles/tubes do you want to take? "
    )

    if quantity > current_remaining:
        print("\nNot enough inventory.")
        print(f"Current remaining: {current_remaining}")
        print(f"Requested quantity: {quantity}")
        print("Inventory was NOT changed.")
        return "done"

    print("\nOptional log information")
    print("-" * 70)
    print("Enter your name, initials, or any note for this operation.")
    print("Examples: CL, Suzie, CL - TFH experiment")
    print("Press Enter to skip.")
    operation_note = input("Taken by / optional note: ").strip()

    before = current_remaining
    after = current_remaining - quantity

    print("\nPlease confirm the inventory update:")
    print("-" * 70)
    print(f"Remaining: {before} -> {after}")
    print(f"Log note:  {operation_note or 'None'}")
    print("-" * 70)

    final_confirm = ask_yes_no("Save this update?")

    if not final_confirm:
        print("\nInventory was NOT changed.")
        return "done"

    df.loc[row_index, COL_REMAINING] = after

    save_inventory(df)

    log_notes = operation_note

    if after == 0:
        print_last_bottle_warning()

        if log_notes:
            log_notes = f"{log_notes}; Last bottle removed"
        else:
            log_notes = "Last bottle removed"

    write_take_log(
        row_before=row,
        change=-quantity,
        before=before,
        after=after,
        notes=log_notes,
    )

    print("\nInventory updated.")
    print(f"Before: {before}")
    print(f"After:  {after}")

    if log_notes:
        print(f"Log Notes: {log_notes}")

    print("Log saved.")

    return "done"


def write_take_log(row_before, change, before, after, notes=""):
    """
    Write Take action to Log sheet.
    """

    log_record = {
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Action": "Take",
        "CD Marker": safe_cell(row_before, COL_CD_MARKER),
        "Common Name": safe_cell(row_before, COL_COMMON_NAME),
        "Fluorophore": safe_cell(row_before, COL_FLUOROPHORE),
        "Catalog": safe_cell(row_before, COL_CATALOG),
        "Container_Type": safe_cell(row_before, COL_CONTAINER_TYPE),
        "Change": change,
        "Before": before,
        "After": after,
        "Notes": notes,
    }

    append_log(log_record)


def get_unique_normalized_values(df, column_name):
    """
    Get unique normalized values from a DataFrame column.
    Empty values are ignored.
    """

    values = set()

    for value in df[column_name]:
        normalized = normalize_for_search(value)

        if normalized != "":
            values.add(normalized)

    return values


def get_display_unique_values(df, column_name):
    """
    Get unique display values from a DataFrame column.
    Empty values are ignored.
    """

    values = []

    for value in df[column_name]:
        value = str(value).strip()

        if value == "" or value.lower() == "nan":
            continue

        if value not in values:
            values.append(value)

    return values



if __name__ == "__main__":
    take_antibody()