import os
import ast

def merge_texts_in_directory(input_dir):
    # Iterate over each file in the input directory
    for filename in os.listdir(input_dir):
        if os.path.isdir(os.path.join(input_dir, filename)):
            merge_texts_in_directory(os.path.join(input_dir, filename))
        if filename.endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            
            # Read the content of the text file
            with open(input_path, 'r') as file:
                # Assume the content is a JSON array of strings
                content = file.read()
                lst = ast.literal_eval(content)
            # Merge the array of strings into a single string
            merged_text = ' '.join(lst)
            
            # Write the merged text to a new file in the output directory
            with open(input_path, 'w') as file:
                file.write(merged_text)
            # print(f"Merged text saved to {input_path}")

# Example usage
input_directory = ''  # Update with the path to your input directory

merge_texts_in_directory(input_directory)
