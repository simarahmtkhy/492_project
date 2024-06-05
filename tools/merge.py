import glob
import re

# Path to the directory containing the generated answer files
generated_files_path = ''

# Pattern to match the generated answer files
file_pattern = generated_files_path + 'generated_answers_*.jsonl'

# Output file path
merged_output_file = generated_files_path + 'merged_generated_answers.jsonl'

# Function to extract the numerical part from the filename
def extract_part_number(file_name):
    match = re.search(r'(\d+)\.jsonl', file_name)
    return int(match.group(1)) if match else float('inf')

# Find all files that match the pattern
file_list = glob.glob(file_pattern)

# Sort the files numerically by the part number
file_list.sort(key=extract_part_number)

# Open the output file in write mode
with open(merged_output_file, 'w') as output_file:
    # Iterate over each file in the file list
    for file_name in file_list:
        # Open each file and write its contents to the output file
        with open(file_name, 'r') as input_file:
            for line in input_file:
                output_file.write(line)

print(f'Merged {len(file_list)} files into {merged_output_file}')
