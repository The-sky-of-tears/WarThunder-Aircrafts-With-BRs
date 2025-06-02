def get_base_identifier(unit_id_from_csv):
    """
    Removes common suffixes like _shop, _0, _1, _2 from the unit ID
    to get a base identifier for matching with API data.
    Example: 'f_14a_early_shop' -> 'f_14a_early'
    """
    suffixes_to_remove = ["_shop", "_0", "_1", "_2"]
    for suffix in suffixes_to_remove:
        if unit_id_from_csv.endswith(suffix):
            return unit_id_from_csv[:-len(suffix)]
    return unit_id_from_csv


def apply_aircraft_name_consistency(data_rows, api_data_dict):
    """
    Ensures _0, _1, _2 variants of aircraft use the name from the corresponding _shop variant.
    Modifies names only for entries that are identified as aircraft via api_data_dict.
    """
    print("Applying name consistency for aircraft...")
    if not api_data_dict:
        print("API data dictionary is empty or not loaded. Skipping name consistency.")
        return data_rows
    if not data_rows or len(data_rows) <= 1:
        print("No data rows to process for name consistency.")
        return data_rows

    modified_data_rows = [data_rows[0]]
    shop_names_map = {}

    # First pass: collect all _shop names for known aircraft
    for row in data_rows[1:]:
        original_id, original_name = row
        base_id = get_base_identifier(original_id)

        if base_id in api_data_dict:
            if original_id.endswith("_shop"):
                shop_names_map[base_id] = original_name

    # Second pass: apply _shop names to _0, _1, _2 variants
    for row in data_rows[1:]:
        original_id, current_name = row
        base_id = get_base_identifier(original_id)
        new_name = current_name

        if base_id in api_data_dict:
            if any(original_id.endswith(s) for s in ["_0", "_1", "_2"]):
                if base_id in shop_names_map:
                    new_name = shop_names_map[base_id]
        modified_data_rows.append([original_id, new_name])

    return modified_data_rows


def add_br_to_aircraft_names(data_rows, api_data_dict):
    """
    Appends Realistic Battle Rating
    to aircraft names for _shop, _0, _1, _2 variants.
    Modifies names only for entries identified as aircraft via api_data_dict.
    """
    print("Adding Realistic BR to aircraft names...")
    if not api_data_dict:
        print("API data dictionary is empty or not loaded. Skipping BR addition.")
        return data_rows
    if not data_rows or len(data_rows) <= 1: # Check for empty or header-only data
        print("No data rows to process for BR addition.")
        return data_rows

    modified_data_rows = [data_rows[0]]

    for row in data_rows[1:]:
        original_id, current_name = row
        base_id = get_base_identifier(original_id)
        new_name = current_name

        if base_id in api_data_dict:  # It's an aircraft
            if any(original_id.endswith(s) for s in ["_shop", "_0", "_1", "_2"]):
                vehicle_info = api_data_dict.get(base_id)
                if vehicle_info:
                    br_value = vehicle_info.get("realistic_br")
                    if br_value is not None:
                        try:
                            br_float = float(br_value)
                            formatted_br = f"{br_float:.1f}"
                            new_name = f"{current_name} [{formatted_br}]"
                        except ValueError:
                            print(f"  Warning: BR value '{br_value}' for {base_id} is not a number. Appending as is.")
                            new_name = f"{current_name} [{br_value}]"
        modified_data_rows.append([original_id, new_name])
    return modified_data_rows