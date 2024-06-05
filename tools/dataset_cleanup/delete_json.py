import os

def delete_json_files(directory):
    # Get all files in the directory
    files = os.listdir(directory)

    # Iterate through the files
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isdir(file_path):
            delete_json_files(file_path)  # Recursively call function for subdirectories
        else:
            filename, extension = os.path.splitext(file)
            if extension == '.json':
                os.remove(file_path)

    print(f"JSON files in {directory} have been deleted.")

# Example usage:
delete_json_files('')
