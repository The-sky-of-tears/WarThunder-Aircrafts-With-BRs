import os

SOURCE_LANG_SUBDIR = "lang"
SOURCE_CSV_FILENAME = "units.csv"
OUTPUT_CSV_FILENAME = "units.csv"
API_JSON_DATA_FILENAME = "all_aircraft_data.json"

# --- API Configuration ---
API_BASE_URL = "https://www.wtvehiclesapi.sgambe.serv00.net/api/vehicles"
AIRCRAFT_TYPES_TO_FETCH = ["fighter", "assault", "bomber"]
API_COMMON_PARAMS = {
    "excludeKillstreak": True,
}

# --- CSV Column Configuration ---
ID_COLUMN_INDEX = 0
ENGLISH_COLUMN_INDEX = 1

# --- Helper Function for Paths ---
def get_working_directory_path(filename):
    """Returns the absolute path for a file in the current working directory."""
    return os.path.join(os.getcwd(), filename)