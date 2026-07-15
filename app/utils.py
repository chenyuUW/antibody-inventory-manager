# utils.py
# Utility functions for Antibody Inventory Manager
import re

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

def validate_cd_marker(value):
    """
    Validate and normalize CD Marker.

    Rules:
    - Empty is allowed.
    - Input is case-insensitive: cd3, Cd4, cD45ra are accepted.
    - Valid input is automatically converted to uppercase.
    - If not empty, it must start with CD.
    - After CD, it must contain numbers.
    - Letters after numbers are allowed, e.g. CD45RA, CD294, CD3.
    """
    value = str(value).strip()

    if value == "":
        return value

    validate_no_space(value, "CD Marker")
    validate_no_greek_letters(value, "CD Marker")

    # Accept any capitalization and store the final value consistently.
    value = value.upper()

    pattern = r"^CD[0-9]+[A-Z]*$"

    if not re.fullmatch(pattern, value):
        raise ValueError(
            "CD Marker must look like CD3, CD4, CD45RA, CD197, etc. "
            "Uppercase and lowercase input are both accepted. "
            "Or leave it empty if there is no CD marker."
        )

    return value

def validate_box_positions(value):
    """
    Validate and normalize Box Position.

    Accepted formats:
        3A
        10A
        20A
        1A;1B
        1A;2B;10C

    Rules:
    - Each position must be numbers followed by exactly one letter.
    - Multiple positions must be separated by semicolons.
    - Lowercase letters are automatically converted to uppercase.
    - Spaces are automatically removed.
    - Chinese semicolons are automatically converted to English semicolons.

    Invalid examples:
        1211221
        AD
        D1
        1A;D1
        1A;;2B
    """

    value = str(value).strip()

    # Remove all spaces
    value = value.replace(" ", "")

    # Convert Chinese semicolon to English semicolon
    value = value.replace("；", ";")

    # Convert letters to uppercase
    value = value.upper()

    if value == "":
        raise ValueError("Box Position cannot be empty.")

    pattern = r"^[0-9]+[A-Z](;[0-9]+[A-Z])*$"

    if not re.fullmatch(pattern, value):
        raise ValueError(
            "Invalid Box Position format. "
            "Each position must contain numbers followed by one letter. "
            "Use semicolons between multiple positions. "
            "Examples: 3A, 10A, 1A;1B."
        )

    return value

def choose_from_existing_values(prompt, values, allow_empty=False):
    """
    Let user choose from existing values by number.

    This is used for fields like Box.
    """
    clean_values = []

    for value in values:
        value = str(value).strip()
        if value == "" or value.lower() == "nan":
            continue
        if value not in clean_values:
            clean_values.append(value)

    if not clean_values:
        raise ValueError("No existing values found.")

    while True:
        print(f"\n{prompt}")
        print("-" * 70)

        if allow_empty:
            print("0. Leave empty")

        for i, value in enumerate(clean_values, start=1):
            print(f"{i}. {value}")

        choice = input("Select an option: ").strip()

        if allow_empty and choice == "0":
            return ""

        try:
            choice_number = int(choice)

            if 1 <= choice_number <= len(clean_values):
                return clean_values[choice_number - 1]

            print("Invalid option. Please choose a number from the list.")

        except ValueError:
            print("Please enter a valid number.")


def choose_container_type():
    """
    Container_Type is controlled vocabulary.
    """
    options = ["Aliquot", "Standard_vial"]

    while True:
        print("\nContainer_Type")
        print("-" * 70)
        print("1. Aliquot")
        print("2. Standard_vial")

        choice = input("Select container type: ").strip()

        if choice == "1":
            return "Aliquot"

        if choice == "2":
            return "Standard_vial"

        print("Invalid option. Please choose 1 or 2.")

def normalize_for_search(value):
    """
    Normalize text for flexible searching.

    Search should ignore:
    - case
    - spaces
    - hyphens
    - underscores

    Examples:
        PD-1     -> PD1
        pd1      -> PD1
        IFN-g    -> IFNG
        IFN G    -> IFNG
        PE-Cy7   -> PECY7
        PE Cy7   -> PECY7
    """
    if value is None:
        return ""

    value = str(value)

    if value.lower() == "nan":
        return ""

    return (
        value.upper()
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
        .replace("Α", "A")
        .replace("Β", "B")
        .replace("Γ", "G")
        .replace("α", "A")
        .replace("β", "B")
        .replace("γ", "G")
    )


def is_empty(value):
    """
    Check whether a cell value should be considered empty.
    """
    if value is None:
        return True

    value = str(value).strip()

    return value == "" or value.lower() == "nan"


def validate_no_space(value, field_name):
    """
    Strict validation for registration/add mode.
    Spaces are not allowed in key fields.
    """
    if " " in str(value):
        raise ValueError(
            f"{field_name} contains spaces. Please remove spaces and try again."
        )


def validate_no_greek_letters(value, field_name):
    """
    Strict validation for registration/add mode.
    Greek letters should not be used.
    Use a/b/g instead.
    """
    greek_letters = ["α", "β", "γ", "Α", "Β", "Γ"]

    for letter in greek_letters:
        if letter in str(value):
            raise ValueError(
                f"{field_name} contains Greek letter '{letter}'. "
                "Please use a/b/g instead."
            )


def validate_registration_field(value, field_name, allow_empty=False):
    """
    Validate a field during Add/Register mode.

    Rules:
    - No spaces
    - No Greek letters
    - Empty fields are only allowed if allow_empty=True
    """
    value = str(value).strip()

    if not allow_empty and value == "":
        raise ValueError(f"{field_name} cannot be empty.")

    if value == "":
        return value

    validate_no_space(value, field_name)
    validate_no_greek_letters(value, field_name)

    return value


def ask_yes_no(prompt):
    """
    Ask a yes/no question.
    Return True for yes, False for no.
    """
    while True:
        answer = input(f"{prompt} (Y/N): ").strip().lower()

        if answer in ["y", "yes"]:
            return True

        if answer in ["n", "no"]:
            return False

        print("Please enter Y or N.")


def ask_positive_integer(prompt):
    """
    Ask user for a positive integer.
    """
    while True:
        value = input(prompt).strip()

        try:
            value = int(value)

            if value <= 0:
                print("Please enter a positive integer.")
                continue

            return value

        except ValueError:
            print("Please enter a valid integer.")


def safe_cell(row, column_name):
    """
    Safely get a value from a pandas row.
    """
    try:
        value = row[column_name]

        if is_empty(value):
            return ""

        return str(value)

    except Exception:
        return ""


def print_antibody_details(row):
    """
    Print full antibody information for human visual confirmation.
    """
    print("-" * 70)
    print("Antibody information")
    print("-" * 70)
    print(f"Box:                  {safe_cell(row, COL_BOX)}")
    print(f"CD Marker:            {safe_cell(row, COL_CD_MARKER)}")
    print(f"Common Name:          {safe_cell(row, COL_COMMON_NAME)}")
    print(f"Fluorophore:          {safe_cell(row, COL_FLUOROPHORE)}")
    print(f"Catalog:              {safe_cell(row, COL_CATALOG)}")
    print(f"Manufacturer:         {safe_cell(row, COL_MANUFACTURER)}")
    print(f"Container Type:       {safe_cell(row, COL_CONTAINER_TYPE)}")
    print(f"Remaining:            {safe_cell(row, COL_REMAINING)}")
    print(f"Recommended Channel:  {safe_cell(row, COL_RECOMMENDED_CHANNEL)}")
    print(f"Box Position:         {safe_cell(row, COL_BOX_POSITION)}")
    print(f"Recommended Dilution: {safe_cell(row, COL_RECOMMENDED_DILUTION)}")
    print(f"Notes:                {safe_cell(row, COL_NOTES)}")
    print("-" * 70)


def print_multiple_results(df):
    """
    Print multiple matching results.
    Used when search returns more than one row.
    """
    print("\nMultiple matches found:")
    print("=" * 70)

    for i, (_, row) in enumerate(df.iterrows(), start=1):
        print(f"\n[{i}]")
        print(f"CD Marker:      {safe_cell(row, COL_CD_MARKER)}")
        print(f"Common Name:    {safe_cell(row, COL_COMMON_NAME)}")
        print(f"Fluorophore:    {safe_cell(row, COL_FLUOROPHORE)}")
        print(f"Catalog:        {safe_cell(row, COL_CATALOG)}")
        print(f"Manufacturer:   {safe_cell(row, COL_MANUFACTURER)}")
        print(f"Container Type: {safe_cell(row, COL_CONTAINER_TYPE)}")
        print(f"Remaining:      {safe_cell(row, COL_REMAINING)}")
        print(f"Box:            {safe_cell(row, COL_BOX)}")

    print("\n" + "=" * 70)


def print_last_bottle_warning():
    """
    Print a strong warning when the last bottle is removed.
    This does not block the action.
    """
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    message = """
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!                                        !!!
!!!          LAST BOTTLE REMOVED          !!!
!!!                                        !!!
!!!    This antibody is now OUT OF STOCK. !!!
!!!                                        !!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

    try:
        print(f"{RED}{BOLD}{message}{RESET}")
    except Exception:
        print(message)