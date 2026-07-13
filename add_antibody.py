# add_antibody.py
# Add / Register antibody function for Antibody Inventory Manager

from datetime import datetime

import pandas as pd

from config import (
    INVENTORY_COLUMNS,
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

from data_io import load_inventory, save_inventory, append_log

from utils import (
    normalize_for_search,
    ask_yes_no,
    ask_positive_integer,
    print_antibody_details,
    print_multiple_results,
    safe_cell,
    validate_registration_field,
    validate_cd_marker,
    validate_box_positions,
    choose_from_existing_values,
    choose_container_type,
)


def add_antibody():
    """
    Main Add / Register Antibody workflow.

    Logic:
    1. Ask for catalog.
    2. If catalog exists:
        - add quantity to existing inventory entry.
    3. If catalog does not exist:
        - register a new antibody entry.
    """

    while True:
        print("=" * 70)
        print("Add / Register Antibody")
        print("=" * 70)
        print("1. Add by catalog / register new antibody")
        print("2. Cancel")
        print("-" * 70)

        choice = input("Select an option: ").strip()

        if choice == "1":
            result = add_by_catalog_flow()

            if result == "done":
                return

        elif choice == "2":
            print("\nAdd / Register cancelled.")
            return

        else:
            print("\nInvalid option. Please enter 1 or 2.\n")


def add_by_catalog_flow():
    """
    Ask for catalog first.

    If catalog exists uniquely:
        add to that entry.

    If catalog exists in multiple rows:
        resolve by Container_Type.

    If catalog does not exist:
        register a new antibody.
    """

    print("\nCatalog number")
    print("-" * 70)
    print("Enter the catalog/product number printed on the antibody label.")
    print("Examples: 557741, 300328, 612564")
    print("If the catalog is genuinely unavailable, enter: Unknown")
    print("Do not add extra spaces.")
    catalog = input("Catalog number: ").strip()

    print("-" * 70)
    print(f"You entered: {catalog}")
    print("-" * 70)

    if catalog == "":
        print("\nCatalog cannot be empty.")
        return "retry"

    df = load_inventory()

    # If the catalog is Unknown, ask the user what to do.
    if normalize_for_search(catalog) == "UNKNOWN":
        print('\nCatalog is "Unknown".')

        while True:
            print("\nWhat would you like to do?")
            print("1. Register a new antibody with catalog marked as Unknown")
            print("2. Re-enter catalog number")
            print("3. Cancel")
            print("-" * 70)

            choice = input("Select an option: ").strip()

            if choice == "1":
                return register_new_antibody(
                    df,
                    preset_catalog=catalog,
                )

            if choice == "2":
                return "retry"

            if choice == "3":
                print("\nAdd / Register cancelled.")
                return "done"

            print("\nInvalid option. Please enter 1, 2, or 3.")

    matched = search_by_catalog(df, catalog)

    if len(matched) == 0:
        print("\nNo existing antibody found with this catalog.")
        print(f"Catalog entered: {catalog}")

        while True:
            print("\nWhat would you like to do?")
            print("1. Register this as a new antibody")
            print("2. Re-enter catalog number")
            print("3. Cancel")
            print("-" * 70)

            choice = input("Select an option: ").strip()

            if choice == "1":
                return register_new_antibody(
                    df,
                    preset_catalog=catalog,
                )

            if choice == "2":
                return "retry"

            if choice == "3":
                print("\nAdd / Register cancelled.")
                return "done"

            print("\nInvalid option. Please enter 1, 2, or 3.")

    if len(matched) == 1:
        matched_index = matched.index[0]
        return confirm_and_add_to_existing(df, matched_index)

    print_multiple_results(matched)
    print("\nMultiple inventory entries found with this catalog.")
    print("This may be due to Standard_vial and Aliquot entries.")

    return resolve_existing_by_container_type(df, matched)


def search_by_catalog(df, catalog):
    """
    Return rows matching catalog exactly after normalization.
    """

    catalog_query = normalize_for_search(catalog)
    catalog_series = df[COL_CATALOG].apply(normalize_for_search)

    matched = df[catalog_series == catalog_query].copy()

    return matched


def resolve_existing_by_container_type(df, matched):
    """
    If catalog matches multiple rows, ask for Container_Type.
    If Container_Type makes the match unique, add to that row.
    """

    container_types = get_display_unique_values(matched, COL_CONTAINER_TYPE)

    if container_types:
        print("\nAvailable container types:")
        for container in container_types:
            print(f"- {container}")

    while True:
        print("\nPlease specify container type.")
        print("Examples: Aliquot, Standard_vial")
        print("Or type 'back' to enter another catalog.")
        print("Or type 'cancel' to cancel.")

        container_input = input("Container type: ").strip()

        if container_input.lower() == "back":
            return "retry"

        if container_input.lower() == "cancel":
            print("\nAdd / Register cancelled.")
            return "done"

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
            return confirm_and_add_to_existing(df, matched_index)

        print_multiple_results(narrowed)
        print("\nStill multiple matches after specifying container type.")
        print("Inventory was NOT changed.")
        print("Please check the inventory table manually before adding stock.")

        return "done"


def confirm_and_add_to_existing(df, row_index):
    """
    Show existing antibody details and ask user to confirm before adding stock.

    For an existing catalog:
    - Increase Remaining
    - Ask the user to enter all current box positions
    - Completely replace the old Box Position value
    """

    row = df.loc[row_index]

    print("\nExisting antibody found:\n")
    print_antibody_details(row)
    print(
        "\nNote: Box Position may include positions of bottles currently in use."
    )

    confirm = ask_yes_no("Is this the antibody you want to add / return?")

    if not confirm:
        print("\nOkay. Returning to catalog input.")
        return "retry"

    current_remaining = int(df.loc[row_index, COL_REMAINING])
    current_positions = safe_cell(row, COL_BOX_POSITION)

    print(f"\nCurrent remaining: {current_remaining}")

    if current_positions:
        print(f"Current recorded positions: {current_positions}")
    else:
        print("Current recorded positions: None")

    quantity = ask_positive_integer(
        "How many bottles/tubes do you want to add / return? "
    )

    before = current_remaining
    after = current_remaining + quantity

    print(f"\nRemaining after this operation: {after}")
    print(f"Previous recorded positions: {current_positions or 'None'}")
    print()
    print("Enter the complete box positions after this operation.")
    print("This new entry will completely replace the previous Box Position.")
    print("Use semicolons to separate multiple positions.")
    print("Example: 1B;2B;3B")

    while True:
        try:
            new_positions_raw = input("All current box positions: ").strip()
            new_positions = validate_box_positions(new_positions_raw)
            break

        except ValueError as error:
            print(f"Input error: {error}")
            print("Please try again.")

    print("\nPlease confirm the inventory update:")
    print("-" * 70)
    print(f"Remaining:     {before} -> {after}")
    print(f"Box Position:  {current_positions or 'None'} -> {new_positions}")
    print("-" * 70)

    final_confirm = ask_yes_no("Save this update?")

    if not final_confirm:
        print("\nInventory was NOT changed.")
        return "done"

    df.loc[row_index, COL_REMAINING] = after
    df.loc[row_index, COL_BOX_POSITION] = new_positions

    save_inventory(df)

    log_notes = (
        f"Added to existing entry; "
        f"Box Position: {current_positions or 'None'} -> {new_positions}"
    )

    write_add_log(
        row_after=df.loc[row_index],
        change=quantity,
        before=before,
        after=after,
        notes=log_notes,
    )

    print("\nInventory updated.")
    print(f"Before: {before}")
    print(f"After:  {after}")
    print(f"Box Position: {new_positions}")
    print("Log saved.")

    return "done"

def register_new_antibody(df, preset_catalog=None):
    """
    Register a completely new antibody entry.

    Every field is explained before the user is asked to enter it.
    Registration mode is strict:
    - No spaces in key fields
    - No Greek letters
    - Standard hyphens are allowed
    """

    print("\n" + "=" * 70)
    print("New Antibody Registration")
    print("=" * 70)
    print("You will be shown what each field means before entering it.")
    print("General naming rules:")
    print("- Greek letters are NOT accepted. Use a, b, or g instead of alpha, beta, or gamma symbols.")
    print("  Examples: IFN-g, TGF-b, IL-1b (not IFN-γ, TGF-β, or IL-1β).")
    print("- Use a hyphen to connect names and numbers/letter suffixes for cytokines.")
    print("  Examples: IL-2, IL-7, IL-17A, IFN-g, TNF-a.")
    print("- Do not use spaces in key names.")
    print("  Examples: IL-7, IFN-g, PE-Cy7 (not IL 7, IFN g, or PE Cy7).")
    print("- CD markers may be typed in any letter case; they are saved in uppercase.")
    print("  Examples: cd3 -> CD3; cD45ra -> CD45RA.")
    print("=" * 70)

    while True:
        try:
            existing_boxes = get_display_unique_values(df, COL_BOX)

            print_field_instruction(
                "Box",
                "Choose the physical antibody box where this item will be stored.",
                "Select one of the existing box names from the numbered list.",
                required=True,
            )
            box = choose_from_existing_values(
                prompt="Available boxes",
                values=existing_boxes,
                allow_empty=False,
            )

            print_field_instruction(
                "CD Marker",
                "Enter the official CD designation only when the target has one.",
                "Examples: CD3, CD4, CD45RA, CD279. Leave empty for targets such as IFN-g or HLA-DR.",
                required=False,
            )
            cd_marker_raw = input("CD Marker: ").strip()
            cd_marker = validate_cd_marker(cd_marker_raw)

            common_name = prompt_registration_field(
                field_name="Common Name",
                explanation="Enter the target/common antigen name when one is available.",
                example=(
                    "Examples: PD-1, IL7RA, IFN-g, IL-7, TGF-b, HLA-DR. "
                    "Use a/b/g instead of Greek letters, and use hyphens in cytokine names. "
                    "Leave empty if there is no common name."
                ),
                allow_empty=True,
            )

            fluorophore = prompt_registration_field(
                field_name="Fluorophore",
                explanation="Enter the fluorophore conjugated to this antibody.",
                example="Examples: BV605, PE-Cy7, AF700, APC-H7. Do not insert spaces.",
                allow_empty=False,
            )

            if preset_catalog is not None:
                catalog = preset_catalog.strip()
                print_field_instruction(
                    "Catalog",
                    "This catalog number was entered on the previous screen and will be used for the new record.",
                    f"Current value: {catalog}",
                    required=True,
                )
                validate_registration_field(catalog, "Catalog", allow_empty=False)
            else:
                catalog = prompt_registration_field(
                    field_name="Catalog",
                    explanation="Enter the manufacturer catalog/product number printed on the label.",
                    example="Examples: 557741, 300328. Enter Unknown only when no catalog is available.",
                    allow_empty=False,
                )

            manufacturer = prompt_registration_field(
                field_name="Manufacturer",
                explanation="Enter the company that made the antibody.",
                example="Examples: BD, BioLegend, Invitrogen, ThermoFisher. Leave empty if unknown.",
                allow_empty=True,
            )

            print_field_instruction(
                "Container Type",
                "Choose whether this item is an original manufacturer vial or a laboratory aliquot.",
                "Aliquot = transferred portion; Standard_vial = original/standard vial.",
                required=True,
            )
            container_type = choose_container_type()

            print_field_instruction(
                "Initial Remaining",
                "Enter how many bottles or tubes are currently being registered.",
                "Enter a positive whole number, such as 1, 2, or 5.",
                required=True,
            )
            remaining = ask_positive_integer("Initial remaining number: ")

            print_field_instruction(
                "Recommended Channel",
                "Enter the detector/channel normally used for this fluorophore.",
                "Examples: V595, R680, B510. Leave empty if unknown.",
                required=False,
            )
            recommended_channel = input("Recommended Channel: ").strip()

            print_field_instruction(
                "Recommended Dilution",
                "Enter the usual staining dilution or working concentration.",
                "Examples: 1:50, 1:100, 5 uL/test. Leave empty if unknown.",
                required=False,
            )
            recommended_dilution = input("Recommended Dilution: ").strip()

            print_field_instruction(
                "Box Position",
                "Enter the position of every bottle/tube currently in stock.",
                "Each position must be numbers followed by one letter. Separate multiple positions with semicolons, e.g. 1B;2B;10C. Spaces are removed and letters become uppercase automatically.",
                required=True,
            )
            while True:
                try:
                    box_position_raw = input("Box Position: ").strip()
                    box_position = validate_box_positions(box_position_raw)
                    break
                except ValueError as error:
                    print(f"Input error: {error}")
                    print("Please try again.")

            print_field_instruction(
                "Notes",
                "Enter any extra information that does not belong in the other fields.",
                "Examples: clone name, lot information, opened date, special storage note. Leave empty if none.",
                required=False,
            )
            notes = input("Notes: ").strip()

            new_record = {
                COL_BOX: box,
                COL_CD_MARKER: cd_marker,
                COL_COMMON_NAME: common_name,
                COL_FLUOROPHORE: fluorophore,
                COL_CATALOG: catalog,
                COL_MANUFACTURER: manufacturer,
                COL_CONTAINER_TYPE: container_type,
                COL_REMAINING: remaining,
                COL_NOTES: notes,
                COL_RECOMMENDED_CHANNEL: recommended_channel,
                COL_BOX_POSITION: box_position,
                COL_RECOMMENDED_DILUTION: recommended_dilution,
            }

            print("\nPlease review the new antibody entry:")
            print("-" * 70)
            for column in INVENTORY_COLUMNS:
                print(f"{column}: {new_record.get(column, '')}")
            print("-" * 70)

            confirm = ask_yes_no("Register this new antibody?")

            if not confirm:
                retry = ask_yes_no("Do you want to re-enter the information?")
                if retry:
                    continue
                print("\nNew antibody registration cancelled.")
                return "done"

            df = append_new_inventory_row(df, new_record)
            save_inventory(df)

            write_new_registration_log(
                new_record=new_record,
                change=remaining,
                before=0,
                after=remaining,
                notes="New antibody registered",
            )

            print("\nNew antibody registered.")
            print("Inventory updated.")
            print("Log saved.")
            return "done"

        except ValueError as error:
            print(f"\nInput error: {error}")
            print("Please re-enter the new antibody information.\n")


def print_field_instruction(field_name, explanation, example, required):
    """Print a short field guide before requesting user input."""
    requirement = "Required" if required else "Optional"
    print("\n" + "-" * 70)
    print(f"{field_name} [{requirement}]")
    print(explanation)
    print(example)
    print("-" * 70)


def prompt_registration_field(
    field_name,
    explanation,
    example,
    allow_empty=False,
):
    """Explain a registration field first, then request and validate it."""
    print_field_instruction(
        field_name=field_name,
        explanation=explanation,
        example=example,
        required=not allow_empty,
    )

    value = input(f"{field_name}: ").strip()
    return validate_registration_field(
        value,
        field_name,
        allow_empty=allow_empty,
    )


def append_new_inventory_row(df, new_record):
    """
    Append a new antibody row to the inventory DataFrame.
    """

    new_df = pd.DataFrame([new_record], columns=INVENTORY_COLUMNS)

    combined = pd.concat([df, new_df], ignore_index=True)

    combined[COL_REMAINING] = pd.to_numeric(
        combined[COL_REMAINING],
        errors="coerce"
    ).fillna(0).astype(int)

    return combined


def write_add_log(row_after, change, before, after, notes=""):
    """
    Write Add action for existing antibody to Log sheet.
    """

    log_record = {
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Action": "Add",
        "CD Marker": safe_cell(row_after, COL_CD_MARKER),
        "Common Name": safe_cell(row_after, COL_COMMON_NAME),
        "Fluorophore": safe_cell(row_after, COL_FLUOROPHORE),
        "Catalog": safe_cell(row_after, COL_CATALOG),
        "Container_Type": safe_cell(row_after, COL_CONTAINER_TYPE),
        "Change": change,
        "Before": before,
        "After": after,
        "Notes": notes,
    }

    append_log(log_record)


def write_new_registration_log(new_record, change, before, after, notes=""):
    """
    Write Register action for a new antibody to Log sheet.
    """

    log_record = {
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Action": "Register",
        "CD Marker": new_record.get(COL_CD_MARKER, ""),
        "Common Name": new_record.get(COL_COMMON_NAME, ""),
        "Fluorophore": new_record.get(COL_FLUOROPHORE, ""),
        "Catalog": new_record.get(COL_CATALOG, ""),
        "Container_Type": new_record.get(COL_CONTAINER_TYPE, ""),
        "Change": change,
        "Before": before,
        "After": after,
        "Notes": notes,
    }

    append_log(log_record)


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
    add_antibody()