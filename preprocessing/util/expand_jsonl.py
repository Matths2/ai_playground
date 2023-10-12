import json
from termcolor import colored
import argparse

# Create an argument parser
parser = argparse.ArgumentParser(description="Read and format JSONL data.")

# Add an argument for the JSONL file path
parser.add_argument("jsonl_file", help="Path to the JSONL file")

# Parse the command-line arguments
args = parser.parse_args()

with open(args.jsonl_file, "r") as file:
    for line in file:
        data = json.loads(line)
        print(colored("instruction:", "green"), colored(data["instruction"], "blue"))
        print(colored("context:", "green"), colored(data["context"], "blue"))
        print(colored("response:", "green"), colored(data["response"], "blue"))
        print()  # Add an empty line for separation
