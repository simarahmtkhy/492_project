import json

def split_jsonl(input_file_path, output_prefix, lines_per_file=100):
    # Read the input file
    with open(input_file_path, 'r') as input_file:
        lines = input_file.readlines()
    
    # Calculate the number of output files needed
    total_lines = len(lines)
    num_files = (total_lines // lines_per_file) + (1 if total_lines % lines_per_file else 0)

    # Split the lines into smaller files
    for i in range(num_files):
        start_index = i * lines_per_file
        end_index = start_index + lines_per_file
        output_lines = lines[start_index:end_index]
        
        # Write the output file
        output_file_path = f'{output_prefix}_part_{i + 1}.jsonl'
        with open(output_file_path, 'w') as output_file:
            output_file.writelines(output_lines)
        
        print(f'Created {output_file_path} with {len(output_lines)} lines.')

# Paths to your input JSONL files
questions_file_path = ''
answers_file_path = ''

# Split the questions file
split_jsonl(questions_file_path, '', lines_per_file=100)

# Split the answers file
split_jsonl(answers_file_path, '', lines_per_file=100)
