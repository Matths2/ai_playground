import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))

input_file = os.path.join(
    script_dir, "..", "..", "datasets", "sensitive_data", "example.json"
)
output_file = os.path.join(
    script_dir, "..", "..", "datasets", "sensitive_data", "_example.json"
)

with open(input_file, "r") as json_file:
    data = json.load(json_file)


# scrub all data from json file
def replace_with_none(obj):
    if isinstance(obj, dict):
        for key in obj:
            obj[key] = replace_with_none(obj[key])
    elif isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = replace_with_none(obj[i])
    else:
        obj = None
    return obj


data = replace_with_none(data)

with open(output_file, "w") as json_file:
    json.dump(data, json_file, indent=2)
