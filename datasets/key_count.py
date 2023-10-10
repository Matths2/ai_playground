import json
import os
import sys
from collections import defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def count_key_occurrences(files, depth=1):
    key_count = defaultdict(int)

    def count_keys_recursive(data, current_depth):
        if current_depth <= depth:
            if isinstance(data, dict):  # Check if it's a dictionary
                for key, value in data.items():
                    key_count[key] += 1
                    count_keys_recursive(value, current_depth + 1)
            elif isinstance(data, list):  # Check if it's a list
                for item in data:
                    count_keys_recursive(item, current_depth)

    # Iterate through JSON objects within the list
    for file_data in files:
        count_keys_recursive(file_data, 1)

    return key_count


# Specify the directory containing JSON files
directory = os.path.join(script_dir, 'sensitive_data', 'octopart-subset')

# Get a list of JSON files in the specified directory
json_files = [os.path.join(directory, filename) for filename in os.listdir(
    directory) if filename.endswith('.json')]

if len(json_files) < 2:
    sys.stdout.write("There are not enough JSON files for comparison.\n")
else:
    json_data_list = [load_json(file_path) for file_path in json_files]

    # Set the depth you want to explore (e.g., 2 for two levels deep)
    depth_to_explore = 3

    key_occurrences = count_key_occurrences(
        json_data_list, depth=depth_to_explore)

    if not key_occurrences:
        sys.stdout.write("No keys found among JSON files.")
    else:
        print("Key occurrences:")
        for key, count in key_occurrences.items():
            sys.stdout.write(f"{key}: {count + 1}\n")
