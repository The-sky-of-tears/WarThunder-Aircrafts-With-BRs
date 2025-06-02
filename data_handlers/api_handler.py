import json
import time
import config
import requests


def fetch_and_save_api_data():
    """
    Fetches vehicle data from the API for specified aircraft types and saves it to a JSON file.
    Uses constants from the config.py file.
    """

    all_aircraft_data = []
    print("Fetching vehicle data from API for specified aircraft types...")

    output_json_path = config.get_working_directory_path(config.API_JSON_DATA_FILENAME)

    for aircraft_type in config.AIRCRAFT_TYPES_TO_FETCH:

        page = 0
        limit = 100
        current_type_data_count = 0

        while True:
            current_params = config.API_COMMON_PARAMS.copy()
            current_params["type"] = aircraft_type
            current_params["page"] = page
            current_params["limit"] = limit

            try:
                response = requests.get(config.API_BASE_URL, params=current_params)
                response.raise_for_status()  # Raise an exception for HTTP errors
                data_batch = response.json()
                if not data_batch:
                    print(f"  No more data from API for type '{aircraft_type}' on page {page}.")
                    break
                all_aircraft_data.extend(data_batch)
                current_type_data_count += len(data_batch)
                if len(data_batch) < limit:
                    break
                page += 1
                time.sleep(0.5)  # Be respectful to the API server
            except requests.exceptions.HTTPError as e:
                print(f"  HTTP error fetching page {page} for type '{aircraft_type}': {e}\n  Response: {response.text}")
                return False
            except requests.exceptions.RequestException as e:
                print(f"  Request error fetching page {page} for type '{aircraft_type}': {e}")
                return False
            except ValueError as e:  # Includes JSONDecodeError
                print(
                    f"  JSON decode error fetching page {page} for type '{aircraft_type}': {e}\n  Response: {response.text}")
                return False

    if not all_aircraft_data:
        print("No data fetched from the API across all specified types.")
        return False

    print(f"Total aircraft items fetched from API: {len(all_aircraft_data)}")
    try:
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(all_aircraft_data, f, indent=4)
        return True
    except IOError as e:
        print(f"ERROR: Could not write API data to JSON file. {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while saving API data to JSON: {e}")
        return False

def load_api_data_as_dict():
    """
    Loads the API JSON data from the file specified in config.py and converts it
    into a dictionary keyed by aircraft 'identifier'.
    """
    json_filepath = config.get_working_directory_path(config.API_JSON_DATA_FILENAME)
    api_data_dict = {}
    try:
        with open(json_filepath, 'r', encoding='utf-8') as f:
            api_list = json.load(f)
            for vehicle in api_list:
                if 'identifier' in vehicle:
                    api_data_dict[vehicle['identifier']] = vehicle
                else:
                    print(f"Warning: API vehicle found without 'identifier': {vehicle.get('name', 'N/A')}")
        return api_data_dict
    except FileNotFoundError:
        print(f"ERROR: API JSON file not found at '{json_filepath}'. Cannot perform name modifications.")
        return None
    except json.JSONDecodeError:
        print(f"ERROR: Could not decode API JSON file '{json_filepath}'.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred loading API JSON '{json_filepath}': {e}")
        return None