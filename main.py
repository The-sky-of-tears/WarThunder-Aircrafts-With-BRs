import os
import config
from data_handlers import data_processor, csv_handler, api_handler


def run_script():
    print("\nWar Thunder Aircrafts with BRs  v0.1")
    print("-------------------------------------------------------------")

    copied_csv_path = csv_handler.copy_source_csv(WARTHUNDER_DIR)
    if not copied_csv_path:
        print("Halting: Error copying source CSV.")
        return

    extracted_data = csv_handler.extract_data(copied_csv_path)
    if not extracted_data or len(extracted_data) <= 1:
        print("Halting: No data extracted from CSV or only header found.")
        return

    api_fetch_successful = api_handler.fetch_and_save_api_data()
    if not api_fetch_successful:
        print("Halting: Error fetching or saving API data.")
        return

    api_data_dict = api_handler.load_api_data_as_dict()
    if not api_data_dict:
        print("Halting: Could not load API data for modifications.")
        return


    data_with_consistent_names = data_processor.apply_aircraft_name_consistency(extracted_data, api_data_dict)

    final_modified_data = data_processor.add_br_to_aircraft_names(data_with_consistent_names, api_data_dict)

    csv_handler.save_data_to_csv(final_modified_data, config.OUTPUT_CSV_FILENAME)

    os.remove(config.get_working_directory_path(config.API_JSON_DATA_FILENAME))

    print("-------------------------------------------------------------")
    print(f"Remember to place new '{config.OUTPUT_CSV_FILENAME}' in your War Thunder 'lang' folder")


if __name__ == "__main__":
    print("-------------------------------------------------------------")
    print("This script modifies 'units.csv' to include Battle Ratings for aircraft.")
    print("The output 'units.csv' will be saved in the script's directory.")

    WARTHUNDER_DIR = input("Enter path to War Thunder folder"
                                  "\nExample: \"D:\\5_Games\\Steam\\steamapps\\common\\War Thunder\""
                                  "\nPath: ")

    if not os.path.isdir(WARTHUNDER_DIR):
        print("[Error] This path does not seem to exist or is not a directory.")
    else:
        run_script()