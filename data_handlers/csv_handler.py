import csv
import os
import shutil

import config


def copy_source_csv(WARTHUNDER_DIR):
    """
    Copies the source CSV file (e.g., units.csv) from the War Thunder directory
    to the script's working directory. Uses paths from config.py.
    Returns the path to the copied file or None on error.
    """
    source_csv_path = os.path.join(WARTHUNDER_DIR, config.SOURCE_LANG_SUBDIR, config.SOURCE_CSV_FILENAME)
    working_copy_path = config.get_working_directory_path(config.OUTPUT_CSV_FILENAME)

    print(f"Attempting to locate original CSV at: {source_csv_path}")
    if not os.path.exists(source_csv_path):
        print(f"ERROR: Original CSV not found at '{source_csv_path}'.")
        return None

    try:
        shutil.copyfile(source_csv_path, working_copy_path)
        return working_copy_path
    except IOError as e:
        print(f"ERROR: Could not copy file. {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during copy: {e}")
        return None


def extract_data(csv_filepath):
    """
    Reads the specified CSV file and extracts the ID and English Name columns.
    Uses column indices from config.py.
    """
    extracted_data = []

    try:
        with open(csv_filepath, mode='r', encoding='utf-8', newline='') as infile:
            reader = csv.reader(infile, delimiter=';', quotechar='"')
            header = next(reader, None)

            if header:
                extracted_data.append(["OriginalID", "EnglishName"])
            else:
                print("Warning: CSV file appears to be empty or has no header.")
                extracted_data.append(["OriginalID", "EnglishName"]) # Fallback header

            for row_number, row in enumerate(reader, 1):
                if len(row) > max(config.ID_COLUMN_INDEX, config.ENGLISH_COLUMN_INDEX):
                    item_id = row[config.ID_COLUMN_INDEX]
                    language_text = row[config.ENGLISH_COLUMN_INDEX]
                    extracted_data.append([item_id, language_text])
                else:
                    print(
                        f"Warning: Row {row_number} in '{os.path.basename(csv_filepath)}' has too few columns. Skipping.")

        if len(extracted_data) <= 1 and header is None:
            print(f"No data rows extracted from '{csv_filepath}'.")
        elif len(extracted_data) <= 1 and header is not None:
            print(f"Only header processed from '{csv_filepath}'. No data rows extracted.")

    except FileNotFoundError:
        print(f"ERROR: File '{csv_filepath}' not found for processing.")
        return []
    except Exception as e:
        print(f"ERROR: An error occurred while reading '{csv_filepath}'. {e}")
        return []
    return extracted_data


def save_data_to_csv(data_rows, output_filename):
    """
    Saves the provided data_rows to a new CSV file.
    The output path is constructed using config.get_working_directory_path.
    """
    output_filepath = config.get_working_directory_path(output_filename)

    if not data_rows or (len(data_rows) == 1 and data_rows[0] == ["OriginalID", "EnglishName"]):
        print(f"No actual data (or only header) to save to '{output_filepath}'. Skipping save.")
        return False

    try:
        with open(output_filepath, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerows(data_rows)
        print(f"Successfully created new '{os.path.basename(output_filepath)}' with BRs.")
        return True
    except Exception as e:
        print(f"ERROR: An error occurred while writing '{output_filepath}'. {e}")
        return False