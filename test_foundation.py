# test_foundation.py

from data_io import load_inventory
from utils import normalize_for_search, print_antibody_details

df = load_inventory()

print("Inventory loaded successfully.")
print(f"Total rows: {len(df)}")

print("\nNormalize test:")
print("PD-1 ->", normalize_for_search("PD-1"))
print("IFN-g ->", normalize_for_search("IFN-g"))
print("PE Cy7 ->", normalize_for_search("PE Cy7"))

print("\nFirst antibody:")
print_antibody_details(df.iloc[0])