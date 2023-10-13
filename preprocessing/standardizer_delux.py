import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the directory containing your datasheet files
data_directory = os.path.join(
    script_dir, "..", "datasets", "sensitive_data", "octopart-subset"
)

# Initialize an empty list to store standardized data
standardized_data = []
excluded = 0

# Loop through each file in the directory
for filename in os.listdir(data_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(data_directory, filename)

        try:
            with open(file_path, "r") as file:
                datasheets = json.load(file)
                if isinstance(datasheets, list):
                    for datasheet in datasheets:
                        part = datasheet.get("part", {})

                        id = part.get("id", "")
                        slug = part.get("slug", "")
                        mpn = part.get("mpn", "")
                        genericMpn = part.get("genericMpn", "")
                        name = part.get("name", "")
                        shortDescription = part.get("shortDescription", "")
                        octopartUrl = part.get("octopartUrl", "")
                        v3uid = part.get("v3uid", "")
                        counts = part.get("counts", {})
                        totalAvail = part.get("totalAvail", 0)
                        avgAvail = part.get("avgAvail", 0)
                        manufacturer = part.get("manufacturer", {})
                        specs = part.get("specs", [])
                        descriptions = part.get("descriptions", [])
                        estimatedFactoryLeadDays = part.get(
                            "estimatedFactoryLeadDays", 0
                        )
                        similarParts = part.get("similarParts", [])
                        category = part.get("category", {})
                        bestDatasheet = part.get("bestDatasheet", {})
                        documentCollections = part.get("documentCollections", [])
                        medianPrice1000 = part.get("medianPrice1000", {})

                        # Add the extracted data to the standardized_data list
                        standardized_data.append(
                            {
                                "part": {
                                    "id": id,
                                    "slug": slug,
                                    "mpn": mpn,
                                    "genericMpn": genericMpn,
                                    "name": name,
                                    "shortDescription": shortDescription,
                                    "octopartUrl": octopartUrl,
                                    "v3uid": v3uid,
                                    "counts": counts,
                                    "totalAvail": totalAvail,
                                    "avgAvail": avgAvail,
                                    "manufacturer": manufacturer,
                                    "specs": specs,
                                    "similarParts": similarParts,
                                    "descriptions": descriptions,
                                    "estimatedFactoryLeadDays": estimatedFactoryLeadDays,
                                    "category": category,
                                    "bestDatasheet": bestDatasheet,
                                    "documentCollections": documentCollections,
                                    "medianPrice1000": medianPrice1000,
                                }
                            }
                        )
                else:
                    print(
                        f"Skipping {filename}: JSON data is not in the expected list format"
                    )
                    excluded += 1

        except Exception as e:
            # Handle errors or exceptions here (e.g., skip the file)
            print(f"Error processing {filename}: {e}")
            excluded += 1
            continue

print(f"Excluded {excluded} files due to errors.")

# Write the standardized_data list to a JSON file in the script's directory
output_file_name = "standardized_data_delux.json"
output_file_path = os.path.join(
    script_dir, "..", "datasets", "sensitive_data", output_file_name
)
with open(output_file_path, "w") as output_file:
    json.dump(standardized_data, output_file, indent=2)

print(f"Data has been written to {output_file_name}")
