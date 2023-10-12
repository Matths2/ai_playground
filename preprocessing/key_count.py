import json
import os
import sys
from collections import defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))


def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def count_key_occurrences(files, depth=1):
    key_info = defaultdict(list)

    def count_keys_recursive(data, current_depth):
        if current_depth <= depth:
            if isinstance(data, dict):  # Check if it's a dictionary
                for key, value in data.items():
                    if current_depth == 2 and (value is not None and value != []):
                        key_info[key].append(current_depth)
                    elif current_depth != 2:
                        key_info[key].append(current_depth)
                    count_keys_recursive(value, current_depth + 1)
            elif isinstance(data, list):  # Check if it's a list
                for item in data:
                    if current_depth == 2 and (item is not None and item != []):
                        key_info["list"].append(current_depth)  # Track lists at level 2
                    count_keys_recursive(item, current_depth)

    # Iterate through JSON objects within the list
    for file_data in files:
        count_keys_recursive(file_data, 1)

    key_depth_counts = {}
    for key, depths in key_info.items():
        depth_count = {}
        for depth in depths:
            depth_count[depth] = depth_count.get(depth, 0) + 1
        key_depth_counts[key] = depth_count

    # Remove entries where the key is 'list'
    if "list" in key_depth_counts:
        del key_depth_counts["list"]

    return key_depth_counts


# Specify the directory containing JSON files
directory = os.path.join(
    script_dir, "..", "datasets", "sensitive_data", "octopart-subset"
)

# Get a list of JSON files in the specified directory
json_files = [
    os.path.join(directory, filename)
    for filename in os.listdir(directory)
    if filename.endswith(".json")
]

if len(json_files) < 2:
    sys.stdout.write("There are not enough JSON files for comparison.\n")
else:
    json_data_list = [load_json(file_path) for file_path in json_files]

depth_to_explore = 5  # Adjust the depth as needed

key_depth_counts = count_key_occurrences(json_data_list, depth=depth_to_explore)

if not key_depth_counts:
    sys.stdout.write("No keys found among JSON files.")
else:
    # Sort keys by depth and then by total count within each depth
    sorted_keys = sorted(
        key_depth_counts.keys(),
        key=lambda key: (
            min(key_depth_counts[key].keys()),
            sum(key_depth_counts[key].values()),
        ),
    )

    for key in sorted_keys:
        sys.stdout.write(f"{key}:\n")
        depth_counts = key_depth_counts[key]
        sorted_depths = sorted(depth_counts.keys())
        for depth in sorted_depths:
            count = depth_counts[depth]
            sys.stdout.write(f"  Depth {depth}: Count - {count}\n")
