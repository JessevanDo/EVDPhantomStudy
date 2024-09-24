import os
import pandas as pd
import json

# Load the Database_Main.xlsx file and extract the necessary columns
db_main = pd.read_excel(
    r"C:\Users\Jesse\Augmedit Dropbox\Research\Project_EVD\Database\Series2\Main database\Database_Main.xlsx",
    sheet_name='MeasurementDatabase')

# Extract relevant columns: ExperimentID, Side, and PhantomType
db_main_filtered = db_main[['ExperimentID', 'Side', 'PhantomType']].copy()

# Ensure ExperimentID is an integer to avoid format issues
db_main_filtered['ExperimentID'] = db_main_filtered['ExperimentID'].astype(int)

# Add columns for Target coordinates (X, Y, Z)
db_main_filtered['Target_X'] = None
db_main_filtered['Target_Y'] = None
db_main_filtered['Target_Z'] = None


# Function to map PhantomType to Phantom directories
def get_phantom_directory(phantom_type):
    mapping = {
        'A1': 'Phantom1', 'A2': 'Phantom1',
        'B1': 'Phantom2', 'B2': 'Phantom2',
        'C1': 'Phantom3', 'C2': 'Phantom3',
        'D1': 'Phantom4', 'D2': 'Phantom4',
        'E1': 'Phantom5', 'E2': 'Phantom5',
        'F1': 'Phantom6', 'F2': 'Phantom6'
    }
    return mapping.get(phantom_type, None)


# Function to read the target coordinates from the appropriate JSON file
def extract_target_coordinates(phantom_dir, side):
    # Correctly use "L" for "Left" and "R" for "Right"
    if side == "Left":
        target_file = 'Target_L.mrk.json'
    elif side == "Right":
        target_file = 'Target_R.mrk.json'
    else:
        print(f"Unknown side: {side} for Phantom")
        return None

    target_path = os.path.join(phantom_dir, target_file)

    try:
        with open(target_path, 'r') as file:
            data = json.load(file)
            for markup in data.get('markups', []):
                for control_point in markup.get('controlPoints', []):
                    return control_point['position']
    except Exception as e:
        print(f"Error reading {target_path}: {e}")
        return None


# Iterate over the filtered database and fetch coordinates
def process_phantom_coordinates(db_main_filtered, phantom_base):
    for index, row in db_main_filtered.iterrows():
        phantom_type = row['PhantomType']
        side = row['Side']

        # Get the directory for the PhantomType
        phantom_dir = get_phantom_directory(phantom_type)
        if not phantom_dir:
            print(f"Invalid PhantomType: {phantom_type} for ExperimentID: {row['ExperimentID']}")
            continue

        # Construct the full path for the phantom directory
        phantom_dir_full = os.path.join(phantom_base, phantom_dir, 'OriginalSegmentation')

        # Fetch the target coordinates
        target_coords = extract_target_coordinates(phantom_dir_full, side)

        # Update DataFrame with target coordinates if found
        if target_coords:
            db_main_filtered.at[index, 'Target_X'] = target_coords[0]
            db_main_filtered.at[index, 'Target_Y'] = target_coords[1]
            db_main_filtered.at[index, 'Target_Z'] = target_coords[2]
        else:
            print(f"Target coordinates not found for ExperimentID: {row['ExperimentID']}")


# Define the base path for Phantom directories
phantom_base_path = r"C:/Users/Jesse/Augmedit Dropbox/Research/Project_EVD/Models/Phantom_Line2"

# Process the database to fetch the target coordinates
process_phantom_coordinates(db_main_filtered, phantom_base_path)

# Log final DataFrame preview before saving
print("Final DataFrame Preview:")
print(db_main_filtered.head(20))

# Export the updated DataFrame with target coordinates to an Excel file
output_path = r'Updated_Database_with_Target_Coordinates.xlsx'
db_main_filtered.to_excel(output_path, index=False)

print(f"Updated database saved to {output_path}")
