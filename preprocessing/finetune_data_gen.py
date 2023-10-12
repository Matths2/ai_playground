import json
import csv
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(
    script_dir, "..", "datasets", "sensitive_data", "standardized_data_delux.json"
)
output_file = os.path.join(
    script_dir, "..", "datasets", "sensitive_data", "prompts.jsonl"
)

with open(input_file, "r") as json_file:
    data = json.load(json_file)

prompts = []

# Iterate through the JSON data
for item in data:
    part = item["part"]
    mpn = part["mpn"]
    name = part["name"]
    shortDescription = part["shortDescription"]
    # handle lists
    specs = part["specs"]
    spec_info = map(
        lambda spec: (spec["attribute"]["name"], spec["value"], spec["units"]), specs
    )
    datasheet = part["bestDatasheet"]
    datasheet_req_keys = ["name", "pageCount", "url", "creditString", "creditUrl"]
    document_collections = part["documentCollections"]
    document_info = list(
        map(
            lambda collection: list(
                map(
                    lambda document: f"Collection Name: {collection['name']}\n   * Document Name: {document.get('name', 'N/A')}\n   * Page Count: {document.get('pageCount', 'N/A')}\n   * URL: {document.get('url', 'N/A')}\n   * Credit String: {document.get('creditString', 'N/A')}\n   * Credit URL: {document.get('creditUrl', 'N/A')}",
                    collection["documents"],
                )
            ),
            document_collections,
        )
    )
    document_info = [item for sublist in document_info for item in sublist]
    formatted_document_info = "\n   * " + "\n   * ".join(document_info)

    # Now 'formatted_document_info' contains the formatted document information

    # Create the input prompts and outputs based on the extracted information
    # Prompt 1: Specs
    input_spec_prompt = f"What are the specs for mpn {mpn}?"
    output_spec_prompt = (
        f"{name} description: {shortDescription}\n"
        "Here are some additional specs:\n"
        "   * "
        + "\n   * ".join(
            [f"{name}: {value} {units}" for name, value, units in spec_info]
        )
    )

    # Prompt 2: Documentation
    input_datasheet_prompt = f"What documentation is available for mpn {mpn}?"
    output_datasheet_prompt = f"\nDatasheet available for {name}:\n"
    if datasheet is not None and isinstance(datasheet, dict):
        output_datasheet_prompt += "\n".join(
            [f"   * {key}: {datasheet.get(key, 'N/A')}" for key in datasheet_req_keys]
        )
    output_datasheet_prompt += (
        "\n\nAdditional documents:" + "\n   * " + "\n   * ".join(document_info)
    )

    # Prompt ...
    # ...

    prompts.append({"instruction": input_spec_prompt, "response": output_spec_prompt})
    prompts.append(
        {"instruction": input_datasheet_prompt, "response": output_datasheet_prompt}
    )

# Iterate through the prompts and write them to the JSONL file
with open(output_file, mode="w") as jsonl_file:
    for prompt in prompts:
        entry = {
            "instruction": prompt["instruction"],
            "context": "",
            "response": prompt["response"],
        }
        jsonl_file.write(json.dumps(entry) + "\n")

print(f"Prompts have been written to {output_file}")
