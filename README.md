# Antibody Inventory Manager User Guide

This program is used to manage antibody inventory in the laboratory.

It can be used to:

- Take antibodies out of inventory and automatically reduce stock
- Add, return, or register antibodies
- Search the antibody inventory
- Record every inventory change
- Automatically create backups

---

# 1. How to Open the Program

## Windows

Find this file in the project folder:

```text
Start Antibody Manager.bat
```

Double-click it.

### Please wait while the program starts

The first time the program is used, it needs to create its working environment and install the required components. This may take several minutes. Do not repeatedly double-click the file, and do not close the window early.

After the first setup is complete, later launches will usually still take about **6–10 seconds**. During this time, the program is loading. It is not frozen. Please wait until the main menu appears.

When you see the following menu, the program has started successfully:

```text
1. Take antibody
2. Add / Register antibody
3. Search / Preview inventory
4. Exit
```

---

## Mac

Find this file in the project folder:

```text
Start Antibody Manager.command
```

The first time you use it, follow these steps.

### Step 1: Open Terminal

1. Press:

```text
Command + Space
```

2. Type:

```text
Terminal
```

3. Press Enter.

### Step 2: Give the file permission to run

In Terminal, type:

```bash
chmod +x 
```

Important: leave one space after `+x`, and do not press Enter yet.

Now drag this file from Finder into the Terminal window:

```text
Start Antibody Manager.command
```

Terminal will automatically add the full file path.

It may look similar to:

```bash
chmod +x /Users/username/Desktop/AntibodyManager/Start\ Antibody\ Manager.command
```

Press Enter.

### Step 3: Open the program

Return to the project folder and double-click:

```text
Start Antibody Manager.command
```

If macOS still blocks the file:

1. Right-click `Start Antibody Manager.command`
2. Select **Open**
3. Click **Open** again in the warning window

After this first approval, you should normally be able to double-click the file in the future.

### Please wait while the program starts

The first launch may take longer because the program needs to create its working environment and install the required components.

After the first setup, later launches will usually still take about **6–10 seconds**. This does not mean the program is frozen. Please wait until the main menu appears.

---

## Ubuntu / Linux

Find this file in the project folder:

```text
start_antibody_manager.sh
```

Open a terminal in the project folder and run:

```bash
./start_antibody_manager.sh
```

---

# 2. Understanding the Main Screen

After the program starts, you will see something similar to:

```text
======================================================================
                    Antibody Inventory Manager
                              v1.0
======================================================================
Database file:         Antibody Inventory Master.xlsx
Antibody entries:      85
Total bottles/tubes:   112
Last inventory update: 2026-07-12 21:48:30
Session started:       2026-07-12 22:00:00
======================================================================

Main Menu
----------------------------------------------------------------------
1. Take antibody
2. Add / Register antibody
3. Search / Preview inventory
4. Exit
----------------------------------------------------------------------
Select an option:
```

### Antibody entries

The total number of antibody records in the inventory table.

### Total bottles/tubes

The total number of bottles or tubes currently listed in inventory.

### Last inventory update

The last time the Excel inventory file was modified.

### Session started

The time when the current program session started.

---

# 3. Function 1: Take Antibody

At the main menu, enter:

```text
1
```

This opens:

```text
Take antibody
```

The program will show:

```text
1. Catalog number
2. Marker + Fluorophore
3. Cancel
```

---

## 3.1 Take an Antibody by Catalog Number

Select:

```text
1. Catalog number
```

Enter the Catalog number printed on the antibody label, for example:

```text
557741
300328
612564
78-0441-82
```

### Input requirements

- The field cannot be empty
- Enter the complete Catalog number whenever possible
- Spaces before or after the entry are removed automatically
- Searching is case-insensitive
- Searching ignores spaces, hyphens, and underscores
- `Unknown` should not be used for Catalog-based searching

If you enter:

```text
Unknown
```

the program will ask you to search using:

```text
Marker + Fluorophore
```

### Correct examples

```text
557741
300328
612564
78-0441-82
```

### Incorrect or discouraged examples

```text
blank
Unknown
```

---

## 3.2 Take an Antibody by Marker + Fluorophore

Select:

```text
2. Marker + Fluorophore
```

Example:

```text
Marker / Target: CD4
Fluorophore: AF700
```

The Marker field searches both:

- CD Marker
- Common Name

The Fluorophore field searches:

- Fluorophore

### Marker input requirements

- The field cannot be empty
- You may enter a CD Marker
- You may also enter a Common Name
- Searching is case-insensitive
- Searching ignores spaces, hyphens, and underscores

For example, the following entries are treated as similar searches:

```text
PD-1
pd1
PD_1
PD 1
```

### Fluorophore input requirements

- The field cannot be empty
- Enter the full fluorophore name
- Searching is case-insensitive
- Searching ignores spaces, hyphens, and underscores
- For some unusual fluorophore names, you may need to confirm how they were originally entered. 
    For example, eF506 may have been recorded under its full name, eFluor506.

For example:

```text
PE-Cy7
PE Cy7
PE_Cy7
pecy7
```

will be treated as similar searches.

---

## 3.3 After the Antibody Is Found

If one unique result is found, the program displays:

```text
Box
CD Marker
Common Name
Fluorophore
Catalog
Manufacturer
Container Type
Remaining
Recommended Channel
Box Position
Recommended Dilution
Notes
```

Check the information carefully.

The program will ask:

```text
Is this the antibody you want to take? (Y/N)
```

If correct, enter:

```text
Y
```

If incorrect, enter:

```text
N
```

---

## 3.4 Enter the Quantity to Take

The program shows the current stock and asks:

```text
How many bottles/tubes do you want to take?
```

Only positive whole numbers are accepted.

### Correct examples

```text
1
2
5
```

### Incorrect examples

```text
0
-1
1.5
one
blank
```

If the requested quantity is greater than the current stock, the program will not change the inventory.

---

## 3.5 Multiple Search Results

If the results contain multiple different Catalog numbers, the program will recommend searching by Catalog.

If the same Catalog appears in more than one record, the program may ask you to choose between:

```text
Aliquot
Standard_vial
```

Enter the container type exactly as shown by the program.

---

## 3.6 Taking the Last Bottle

If the remaining stock becomes 0, the program displays:

```text
LAST BOTTLE REMOVED
This antibody is now OUT OF STOCK.
```

This means no stock remains for that antibody.

---

# 4. Function 2: Add, Return, or Register Antibody

At the main menu, enter:

```text
2
```

This opens:

```text
Add / Register antibody
```

Then select:

```text
1. Add by catalog / register new antibody
```

The program will first ask for a Catalog number.

---

## 4.1 Catalog Input Requirements

Enter the product number printed on the antibody label.

### Correct examples

```text
557741
300328
612564
```

### Common Invitrogen Catalog Format

Some Invitrogen Catalog numbers commonly use the format:

```text
two digits-four digits-two digits
```

Examples:

```text
69-0458-42
12-0038-42
17-0199-42
```

Keep both hyphens and enter the complete number exactly as shown on the label.

Do not enter:

```text
69045842
69 0458 42
69-045842
```

### If the Catalog Is Truly Unavailable

Enter:

```text
Unknown
```

The program will ask whether you want to register a new antibody with Catalog marked as Unknown.

### Input rules

- The field cannot be empty
- Spaces before or after the entry are removed
- Searching is case-insensitive
- The program repeats the Catalog you entered so you can check for typing mistakes

---

# 5. Add Stock to an Existing Antibody

If the Catalog already exists, the program displays the antibody information.

It will ask:

```text
Is this the antibody you want to add / return? (Y/N)
```

If correct, enter:

```text
Y
```

---

## 5.1 Enter the Quantity to Add

The program asks:

```text
How many bottles/tubes do you want to add / return?
```

Only positive whole numbers are accepted.

### Correct examples

```text
1
2
5
```

### Incorrect examples

```text
0
-1
1.5
two
blank
```

---

## 5.2 Re-enter the Complete Box Position

The program asks for all Box Positions after the operation.

This replaces the old Box Position completely. It does not simply add one new position.

For example, if the current positions are:

```text
1A;2A
```

and a new bottle is placed at:

```text
3A
```

you must enter:

```text
1A;2A;3A
```

Do not enter only:

```text
3A
```

---

## 5.3 Box Position Input Requirements

Each position must follow:

```text
number + one letter
```

### Correct examples

```text
1A
10B
100D
01D
1A;2B
1A;2B;10C
```

### Automatic formatting

The program automatically:

- Removes spaces
- Converts lowercase letters to uppercase
- Converts Chinese semicolons `；` to English semicolons `;`

For example:

```text
1a; 2b；3c
```

is saved as:

```text
1A;2B;3C
```

And:

```text
100d
```

is saved as:

```text
100D
```

### Incorrect examples

```text
01
1211221
AD
D1
1A;D1
1A;;2B
```

Reasons:

- `01`: numbers only, no letter
- `1211221`: numbers only, no letter
- `AD`: letters only, no number
- `D1`: letter appears before the number
- `1A;D1`: the second position has the wrong format
- `1A;;2B`: an empty position appears between two semicolons

---

## 5.4 Confirm Before Saving

The program displays something similar to:

```text
Remaining:     2 -> 3
Box Position:  1A;2A -> 1A;2A;3A
```

Then asks:

```text
Save this update? (Y/N)
```

If correct, enter:

```text
Y
```

---

# 6. Register a New Antibody

If the Catalog does not exist, the program displays:

```text
No existing antibody found with this catalog.
```

Then select:

```text
1. Register this as a new antibody
```

The program will explain each field before asking for input.

---

# 7. New Antibody Registration Fields and Input Rules

## 7.1 Box

Required.

The program displays a numbered list of existing boxes, for example:

```text
1. BV-eFluor-RB-Red
2. BUV
3. PE-APC
```

Enter the corresponding number.

### Input requirements

- You must choose a number from the list
- Do not type the box name directly
- The field cannot be left blank
- Numbers outside the available range are rejected

---

## 7.2 CD Marker

Optional.

Enter a CD designation when one exists.

The required format is:

```text
CD + number
```

Letters may appear after the number.

### Correct examples

```text
CD3
CD4
CD45RA
CD197
CD279
CD307E
```

### Capitalization

Any capitalization is accepted:

```text
cd3
Cd4
cD45ra
CD45RA
```

The program saves them as:

```text
CD3
CD4
CD45RA
CD45RA
```

### May be left blank

If there is no CD Marker, press Enter.

### Incorrect examples

```text
CD
3
3CD
CD-3
CD 3
ABC
CD45-RA
```

Reasons:

- `CD`: a number must follow CD
- `3`: must begin with CD
- `3CD`: incorrect order
- `CD-3`: no hyphen is allowed between CD and the number
- `CD 3`: spaces are not allowed
- `ABC`: not a valid CD Marker format
- `CD45-RA`: no hyphen is allowed inside the letter suffix

---

## 7.3 Common Name

Optional.

This field may contain:

- Common target name
- Antigen name
- Gene name
- Protein name
- Cytokine name

### Correct examples

```text
PD-1
IL7RA
IFN-g
IL-7
TGF-b
HLA-DR
Fas
```

### May be left blank

If there is no Common Name, press Enter.

### Input requirements

- Spaces are not allowed
- Greek letters are not accepted
- Hyphens are recommended
- Underscores are discouraged

### Correct examples

```text
IFN-g
TGF-b
IL-1b
HLA-DR
PD-1
```

### Incorrect examples

```text
IFN g
TGF β
IL 7
HLA DR
```

### Underscores

The current system does not actively reject underscores, for example:

```text
IFN_g
HLA_DR
```

However, to keep the Excel file consistent, underscores should not be used.

Recommended:

```text
IFN-g
HLA-DR
```

---

## 7.4 Fluorophore

Required.

Enter the fluorophore conjugated to the antibody.

### Correct examples

```text
BV605
PE-Cy7
AF700
APC-H7
BUV395
PerCP-eFluor710
```

### Input requirements

- The field cannot be empty
- Spaces are not allowed
- Greek letters are not accepted
- Standard hyphens are allowed
- Capitalization is not corrected automatically, so use the laboratory's standard format

### Correct examples

```text
PE-Cy7
APC-H7
PerCP-eFluor710
```

### Incorrect examples

```text
PE Cy7
APC H7
PerCP eFluor710
```

---

## 7.5 Catalog

Required.

Enter the product number printed on the label.

### Correct examples

```text
557741
300328
612564
69-0458-42
```

### Invitrogen Catalog

Some Invitrogen Catalog numbers commonly use:

```text
two digits-four digits-two digits
```

Examples:

```text
69-0458-42
12-0038-42
```

Keep the hyphens and enter the complete format exactly as shown on the label.

### Input requirements

- The field cannot be empty
- Do not add extra spaces
- Standard hyphens should be kept when they are part of the Catalog
- Greek letters are not accepted
- Enter the Catalog exactly as shown on the label

---

## 7.6 Manufacturer

Optional.

### Correct examples

```text
BD
BioLegend
Invitrogen
ThermoFisher
eBioscience
```

### May be left blank

If unknown, press Enter.

### Input requirements

- Spaces are not allowed
- Greek letters are not accepted

If a manufacturer name normally contains spaces, use the laboratory's standard abbreviation.

---

## 7.7 Container Type

Required.

The program provides:

```text
1. Aliquot
2. Standard_vial
```

Only enter:

```text
1
```

or:

```text
2
```

### Aliquot

A laboratory-prepared aliquot.

### Standard_vial

The original manufacturer vial or standard antibody vial.

---

## 7.8 Initial Remaining

Required.

Enter the number of bottles or tubes currently being registered.

### Correct examples

```text
1
2
5
```

### Incorrect examples

```text
0
-1
1.5
two
```

Only positive whole numbers are accepted.

---

## 7.9 Recommended Channel

Optional.

### Correct examples

```text
V595
R680
B510
YG585
```

If unknown, press Enter.

The current system stores the value exactly as entered and does not validate the channel format.

---

## 7.10 Recommended Dilution

Optional, but if entered, the source of the recommendation should also be recorded for traceability.

The recommended format is:

```text
dilution + space + source initials
```

For example, if the recommended dilution `1:50` was found in SR's notebook or records, enter:

```text
1:50 SR
```

Other examples:

```text
1:100 BK
1:20 SZ
1:1000 CL
5uL/test RA
```

The initials should identify the person who provided or recorded the recommendation.

This source information is important because the same antibody may not use the same dilution in every experiment, cell type, staining panel, instrument, or experimental condition.

Do not write only:

```text
1:50
```

Prefer:

```text
1:50 SR
```

If the dilution is unknown, press Enter.

The current system stores the input exactly as entered and does not automatically validate the dilution or initials.

---

## 7.11 Box Position

Required.

The format is:

```text
number + one letter
```

Use English semicolons between multiple positions.

### Correct examples

```text
1A
01D
10B
100D
1A;2B;10C
```

### Automatic conversion

```text
100d -> 100D
1a; 2b -> 1A;2B
```

### Incorrect examples

```text
01
D1
AD
1A;;2B
```

---

## 7.12 Notes

Optional.

This field may contain additional information, for example:

```text
Clone-UCHT1
Lot-123456
Opened-2026-07-12
Protect-from-light
```

It may be left blank.

The Notes field is not strictly validated.

---

# 8. Function 3: Search / Preview Inventory

At the main menu, enter:

```text
3
```

This opens:

```text
Search / Preview inventory
```

This function is read-only. It does not change inventory.

The program provides:

```text
1. Search by marker
2. Search by marker + fluorophore
3. Search by catalog
4. General keyword search
5. Show all inventory
6. Cancel
```

---

## 8.1 Search by Marker

Select:

```text
1. Search by marker
```

You may enter:

```text
CD3
PD-1
IL7RA
IFN-g
HLA-DR
```

### Input requirements

- The field cannot be empty
- You may enter a CD Marker
- You may enter a Common Name
- Partial keywords are accepted
- Searching is case-insensitive
- Searching ignores spaces, hyphens, and underscores

For example, entering:

```text
PD
```

may find:

```text
PD-1
PD-L1
```

---

## 8.2 Search by Marker + Fluorophore

Select:

```text
2. Search by marker + fluorophore
```

Example:

```text
Marker / Target: CD4
Fluorophore: AF700
```

### Input requirements

- Marker cannot be empty
- Fluorophore cannot be empty
- Both entries should be relatively complete
- Searching is case-insensitive
- Searching ignores spaces, hyphens, and underscores

---

## 8.3 Search by Catalog

Select:

```text
3. Search by catalog
```

### Input requirements

- The field cannot be empty
- Enter the complete Catalog whenever possible
- Searching is case-insensitive
- Searching ignores spaces, hyphens, and underscores

---

## 8.4 General Keyword Search

Select:

```text
4. General keyword search
```

You may enter:

```text
BD
BioLegend
Aliquot
BV605
CD3
```

The program searches:

- Box
- CD Marker
- Common Name
- Fluorophore
- Catalog
- Manufacturer
- Container Type
- Notes

### Input requirements

- The field cannot be empty
- Full words or partial keywords may be used
- Searching is case-insensitive

---

## 8.5 Show All Inventory

Select:

```text
5. Show all inventory
```

This displays all inventory records.

If the inventory is large, the terminal output may be long.

---

# 9. Standard Naming Rules

## 9.1 Do Not Use Greek Letters

Do not enter:

```text
α
β
γ
```

Use:

```text
a
b
g
```

Recommended:

```text
IFN-g
TGF-b
TNF-a
IL-1b
```

Do not write:

```text
IFN-γ
TGF-β
TNF-α
IL-1β
```

---

## 9.2 Use Hyphens for Cytokine Names

Recommended:

```text
IL-2
IL-7
IL-17A
IFN-g
TNF-a
TGF-b
```

Gene names should follow their standard form, for example:

```text
IL7RA
TNFRSF7
KLRB1
```

---

## 9.3 Do Not Use Spaces in Key Names

Recommended:

```text
PE-Cy7
APC-H7
IFN-g
HLA-DR
```

Do not write:

```text
PE Cy7
APC H7
IFN g
HLA DR
```

---

## 9.4 Avoid Underscores

Recommended:

```text
IFN-g
HLA-DR
PD-1
```

Discouraged:

```text
IFN_g
HLA_DR
PD_1
```

---

# 10. Where Are Inventory Changes Recorded?

Every Take, Add, or Register action is recorded in the Excel worksheet:

```text
Log
```

The log includes:

```text
Time
Action
CD Marker
Common Name
Fluorophore
Catalog
Container_Type
Change
Before
After
Notes
```

Common Action values:

```text
Take
Add
Register
```

For example:

```text
Change = -1
```

means one bottle was taken.

```text
Change = 2
```

means two bottles were added.

---

# 11. Where Are Backups Saved?

Before every inventory modification, the program creates a backup.

Backups are saved in:

```text
backups
```

A backup file may look like:

```text
Antibody Inventory Master_backup_20260712_214830.xlsx
```

---

## 11.1 How to Restore After a Mistake

1. Close the program
2. Close Excel
3. Open the `backups` folder
4. Find the most recent backup created before the mistake
5. Copy that file
6. Rename the copied file to:

```text
Antibody Inventory Master.xlsx
```

7. Replace the current database file in the project folder

Keep the incorrect version until the recovery has been confirmed.

---

# 12. Important Rules for Daily Use

## Close Excel Before Changing Inventory

If the Excel file is open, the program may be unable to save.

Before changing inventory, close:

```text
Antibody Inventory Master.xlsx
```

---

## Prefer Catalog Search

Catalog is usually the most accurate way to identify an antibody.

---

## Check Carefully Before Saving

Pay special attention to:

```text
Catalog
Fluorophore
Container Type
Remaining
Box Position
```

---

## Enter All Positions When Adding Stock

Do not enter only the newly added position.

Enter the complete Box Position after the operation.

---

## Do Not Edit the Log Without a Clear Reason

The Log is used to track inventory changes.

---

## Check Inventory Regularly

Compare:

```text
Remaining
Number of Box Positions
Actual number of bottles in the box
```

For example:

```text
Remaining = 3
Box Position = 1A;1B;1C
```

These should match.

---


# 13. Using a Different Antibody Inventory

This program is not limited to one specific antibody collection.

The Excel inventory file may be replaced with another antibody inventory, for example:

- Rabbit antibody inventory
- Mouse antibody inventory
- Human antibody inventory
- Flow cytometry antibody inventory
- Histology antibody inventory
- A separate inventory for another laboratory group

The replacement Excel file must keep the same:

```text
Filename
Worksheet name
Column names
Column structure
```

The required filename is:

```text
Antibody Inventory Master.xlsx
```

The required inventory worksheet name is:

```text
Sheet1
```

The inventory worksheet must contain these columns:

```text
box
CD Marker
Common Name
Fluorophore
Catalog
Manufacturer
Container_Type
Remaining
Notes
Recommended Channel
Box Position
Recommended dilution
```

The order and spelling should remain consistent with the existing template.

For example, a rabbit antibody inventory may replace the current inventory as long as it is renamed:

```text
Antibody Inventory Master.xlsx
```

and uses the same worksheet and column layout.

The program will then read and manage the replacement inventory in the same way.

Important:

- Keep a backup of the original Excel file before replacing it
- Do not change the required filename
- Do not change the required worksheet name
- Do not rename or remove required columns
- Make sure `Remaining` contains whole numbers
- Keep the replacement Excel file in the same folder as `gate.py`

---

# 14. Using the Program with Box Drive


The project folder may be stored in a shared Box Drive folder.

If the Excel inventory file is saved inside Box Drive, changes made by the program should normally sync automatically to Box after the file is saved.

For example:

```text
Box/
└── Shared Lab Folder/
    └── Antibody Inventory Manager/
        ├── gate.py
        ├── add_antibody.py
        ├── take_antibody.py
        ├── search_inventory.py
        ├── Antibody Inventory Master.xlsx
        └── README.md
```

After the program updates:

```text
Antibody Inventory Master.xlsx
```

Box Drive should upload the new version automatically.

---

## 14.1 Important: Only One Person at a Time

This program uses one Excel file as the inventory database.

It is not designed for multiple people to edit at the same time.

Only one person should use or modify the inventory at a time.

Do not:

- Run the program on two computers at the same time
- Edit the Excel file while someone else is using the program
- Start a new inventory operation before Box Drive has finished syncing
- Keep the Excel file open while the program is trying to save

Simultaneous changes may cause:

- One person's changes to overwrite another person's changes
- Conflicted copies
- Different versions of the Excel file
- Inventory and Log records becoming inconsistent

---

## 14.2 Recommended Box Drive Workflow

Before using the program:

1. Confirm that no one else is using the inventory
2. Wait for Box Drive to finish syncing
3. Open the program
4. Complete the inventory operation
5. Exit the program
6. Wait for Box Drive to finish syncing again
7. The next person may then open the program

---

## 14.3 Box Drive Does Not Make the Program Multi-user

Storing the folder in Box Drive allows the file to be shared and synchronized.

It does not turn the Excel file into a multi-user database.

The correct description is:

```text
Shared through Box Drive, but used by one person at a time.
```

---

# 15. Common Problems

## The Program Says `openpyxl` Is Missing

Example error:

```text
ModuleNotFoundError: No module named 'openpyxl'
```

Try:

1. Delete the `.venv` folder in the project folder
2. Double-click the startup file again
3. Wait for the environment to be recreated

---

## The Excel File Cannot Be Found

Example error:

```text
Antibody Inventory Master.xlsx was not found
```

Check:

- The Excel file is in the same folder as `gate.py`
- The filename is exactly correct
- It has not been renamed to:

```text
Antibody Inventory Master (1).xlsx
```

---

## The Program Reports Missing Columns

Do not change the first-row column names in Excel:

```text
box
CD Marker
Common Name
Fluorophore
Catalog
Manufacturer
Container_Type
Remaining
Notes
Recommended Channel
Box Position
Recommended dilution
```

---

## The Excel File Cannot Be Saved

The most common reason is that the Excel file is still open.

Close Excel and try again.

---

## There Is No Common Name

Press Enter.

Common Name is optional.

---

## There Is No CD Marker

Press Enter.

CD Marker is optional.

---

## Can Lowercase `cd` Be Entered?

Yes.

```text
cd3 -> CD3
cD45ra -> CD45RA
```

---

## Why Does `CD` Alone Cause an Error?

A number must follow CD.

Incorrect:

```text
CD
```

Correct:

```text
CD3
CD45RA
```

---

## What Happens If Box Position Uses a Lowercase Letter?

```text
100d -> 100D
```

The program converts it automatically.

---

## Why Does `01` Cause an Error?

A Box Position must include both a number and a letter.

Incorrect:

```text
01
```

Correct:

```text
01D
```

---

# 16. Do Not Delete Project Files

The project folder should contain:

```text
gate.py
add_antibody.py
take_antibody.py
search_inventory.py
data_io.py
utils.py
config.py
Antibody Inventory Master.xlsx
README.md
```

Windows also needs:

```text
Start Antibody Manager.bat
```

Mac also needs:

```text
Start Antibody Manager.command
```

Ubuntu / Linux also needs:

```text
start_antibody_manager.sh
```

The program creates:

```text
.venv
backups
```

Do not delete `backups`.

Only delete `.venv` when the program cannot start and the environment needs to be rebuilt.

---

# 17. Quick Operation Guide

## Take an Antibody

```text
Open the program
-> Enter 1
-> Choose Catalog or Marker + Fluorophore
-> Check the antibody information
-> Enter Y
-> Enter the quantity
```

## Add an Existing Antibody

```text
Open the program
-> Enter 2
-> Enter 1
-> Enter the Catalog
-> Check the antibody information
-> Enter Y
-> Enter the quantity to add
-> Enter all Box Positions after the operation
-> Enter Y to save
```

## Register a New Antibody

```text
Open the program
-> Enter 2
-> Enter 1
-> Enter the Catalog
-> Choose Register this as a new antibody
-> Complete each field
-> Review the final entry
-> Enter Y to save
```

## Search the Inventory

```text
Open the program
-> Enter 3
-> Choose a search method
-> Enter a Marker, Fluorophore, Catalog, or keyword
```

---

# 18. When to Stop and Contact the Maintainer

Do not continue modifying inventory if:

- The program cannot start
- The Excel file cannot be found
- The program reports incorrect Excel headers
- The same Catalog appears in multiple records that cannot be distinguished
- Remaining does not match the actual stock
- Box Position does not match the actual location
- The Log cannot be written
- No backup is created
- The program closes unexpectedly
- You are not sure whether the last change was saved

Take a screenshot of the error and contact the maintainer.
- Chenyu Li
- CHENYU200211@OUTLOOK.COM
