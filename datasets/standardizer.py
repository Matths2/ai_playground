import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the directory containing your datasheet files
data_directory = os.path.join(script_dir, "sensitive_data", "octopart-subset")

# Initialize an empty list to store standardized data
standardized_data = []

# Loop through each file in the directory
for filename in os.listdir(data_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(data_directory, filename)

        try:
            with open(file_path, "r") as file:
                datasheet = json.load(file)

                # Extract relevant fields and perform error handling
                # Example:
                part_name = datasheet.get("part", {}).get("name", "")
                manufacturer_name = (
                    datasheet.get("part", {}).get("manufacturer", {}).get("name", "")
                )

                # Add the extracted data to the standardized_data list
                standardized_data.append(
                    {
                        "PartName": part_name,
                        "Manufacturer": manufacturer_name,
                        # Add more fields as needed
                    }
                )

        except Exception as e:
            # Handle errors or exceptions here (e.g., skip the file)
            print(f"Error processing {filename}: {e}")
            continue
