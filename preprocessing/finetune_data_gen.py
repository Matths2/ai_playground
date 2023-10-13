import json
import os
import random

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
alt_intro_phrases = [
    "I'm glad you asked, let me explain.",
    "That's an excellent question, let me guide you through it.",
    "Fantastic question! Allow me to clarify.",
    "Great question! Let me break it down for you.",
    "I'm excited you asked! Here's the explanation.",
]

# Iterate through the JSON data
for item in data:
    part = item["part"]
    mpn = part["mpn"]
    name = part["name"]
    shortDescription = part["shortDescription"]
    estimatedFactoryLeadDays = part["estimatedFactoryLeadDays"]
    category = part["category"]
    if category:
        category_blurb = part["category"]["blurb"]

    # handle lists
    # Be advised to check that they're not empty, they may be at this stage.
    specs = part["specs"]
    if specs:
        spec_info = map(
            lambda spec: (spec["attribute"]["name"], spec["value"], spec["units"]),
            specs,
        )
    similarParts = part["similarParts"]
    if similarParts:
        similarParts_info = map(lambda part: (part["mpn"]), similarParts)

    # Create the input prompts and outputs based on the extracted information

    # Prompt 1: Specs
    if specs and spec_info:
        input_spec_prompt = f"What are the specs for mpn {mpn}?"
        output_spec_prompt = (
            f"\n{name} description: {shortDescription}\n"
            "Here are some additional specs:\n"
            "   * "
            + "\n   * ".join(
                [f"{name}: {value} {units}" for name, value, units in spec_info]
            )
        )
        prompts.append(
            {"instruction": input_spec_prompt, "response": output_spec_prompt}
        )

    # Prompt 2: similarParts
    if similarParts and similarParts_info:
        input_similarParts_prompt = (
            f"Can you suggest some parts that are similar to {mpn}?"
        )
        output_similarParts_prompt = (
            f"\n Sure thing, here is a list of parts that are similar to {name}\n"
            "   * " + "\n   * ".join([f"{mpn}" for mpn in similarParts_info])
        )
        prompts.append(
            {
                "instruction": input_similarParts_prompt,
                "response": output_similarParts_prompt,
            }
        )

    # Prompt 3: blurb
    intro_phrase = random.choice(alt_intro_phrases)
    if category and category_blurb:
        input_blurb_prompt = f"What are {category_blurb['name']}?"
        output_blurb_prompt = (
            f"{intro_phrase}\n{category_blurb['description']}.\n"
            f"And {category_blurb['content']}"
        )
        prompts.append(
            {"instruction": input_blurb_prompt, "response": output_blurb_prompt}
        )

    # Prompt 4: estimatedFactoryLeadDays
    if estimatedFactoryLeadDays:
        input_estimatedFactoryLeadDays_prompt = (
            f"What is the estimated factory lead time in days for {mpn}?"
        )
        output_estimatedFactoryLeadDays_prompt = f"The estimated factory lead time for {name} is {estimatedFactoryLeadDays} days"
        prompts.append(
            {
                "instruction": input_estimatedFactoryLeadDays_prompt,
                "response": output_estimatedFactoryLeadDays_prompt,
            }
        )

    # Prompt ...
    # ...

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
