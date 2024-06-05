import os

def delete_files_without_pairs(directory):
    # Get all files in the directory
    files = os.listdir(directory)

    # Create sets for txt and jpg files
    txt_files = set()
    jpg_files = set()

    # Populate sets with file names without extensions
    for file in files:
        filename, extension = os.path.splitext(file)
        if extension == '.txt':
            txt_files.add(filename)
        elif extension == '.jpg':
            jpg_files.add(filename)

    # Find files without pairs and delete them
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isdir(file_path):
            delete_files_without_pairs(file_path)  # Recursively call function for subdirectories
        else:
            filename, extension = os.path.splitext(file)
            if extension == '.txt' and filename not in jpg_files:
                os.remove(file_path)
            elif extension == '.jpg' and filename not in txt_files:
                os.remove(file_path)

    print(f"Files without pairs in {directory} have been deleted.")

# Example usage:
delete_files_without_pairs('')