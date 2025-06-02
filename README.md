# War Thunder Enhanced Aircraft Names

This mod enhances in-game aircraft names in War Thunder by adding their Realistic Battle Rating (BR) and ensuring name consistency across different spotting distance. By default you can see full name of the aircraft only within 0.5 km distance, which is pretty inconvenient, because there are many aircraft with the same names but different capabilities. However, this mod solves the problem, making an aircraft's full name visible within maximum range.

## Screenshots

![Discord_p59vW0udnX](https://github.com/user-attachments/assets/badb9810-1ede-4588-91ea-b81132cbd919)

## How to Use

Make sure you've enabled "Custom localization" in "Options" -> "Main parameters" (restart required to 'lang' folder to be created)

There are a few ways to use this mod:

### Option 1: Download Pre-Generated `units.csv` (Easiest)

I will provide an updated `units.csv` file after each major game patch, incorporating these name enhancements.
1.  Go to the [**Releases**](https://github.com/The-sky-of-tears/WarThunder-Aircrafts-With-BRs/releases/tag/main) page of this GitHub repository.
2.  Download the latest `units.csv` file.
3.  Navigate to your War Thunder installation folder, then into the `lang` subfolder.
4.  Copy the `units.csv` file you downloaded into your `WarThunder/lang/` directory, replacing the existing one.
5.  Launch War Thunder.

### Option 2: Run the Script from a Release

If you prefer to generate the file yourself using a ready-to-run version of the script:
1.  Go to the [**Releases**](https://github.com/The-sky-of-tears/WarThunder-Aircrafts-With-BRs/releases/tag/main) page.
2.  Download the latest release EXE file.
3.  Run `WT_with_BRs.exe`
4.  When prompted, enter the full path to your War Thunder game installation directory.
5.  A modified `units.csv` will be created in the script's directory.
6.  Copy the generated `units.csv` into your `WarThunder/lang/` directory.
7.  Launch War Thunder.

## Option 3: Run from Source Code (Advanced)

If you want to run the script directly from the source code:
1.  **Clone or Download**:
    * Clone this repository: `git clone https://github.com/The-sky-of-tears/WarThunder-Aircrafts-With-BRs.git`
    * Or, download the source code ZIP and extract it.
2.  **Requirements**:
    * Python 3.x
    * requests 2.32.x
3.  **Run the Script**:
    * Navigate to the project's root directory in your terminal.
    * Run `main.py`:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        pip install requests
        python main.py
        ```
    * When prompted, enter the full path to your War Thunder game installation directory.
4.  **Apply the Mod**:
    * A modified `units.csv` will be generated in the script's directory.
    * Copy the generated `units.csv` into your `WarThunder/lang/` directory.

## Disclaimer

* This script relies on a [third-party API](https://github.com/Sgambe33/WarThunder-Vehicles-API) for vehicle data. Its availability is not guaranteed.
* Modifying game files is done at your own risk. Always back up original game files. This project is not affiliated with Gaijin Entertainment or War Thunder.

---
