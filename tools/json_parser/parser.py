import json
import uuid
import re

def read_and_format_jsonl(file_path):
    """
    Reads a JSONL file where each line is a separate JSON object.
    Converts each line into a dictionary and appends it to a list.
    
    Args:
    file_path (str): The path to the JSONL file.
    
    Returns:
    list: A list of dictionaries, each parsed from a line in the file.
    """
    data_list = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Parse each line as a JSON object and append to the list
                json_obj = json.loads(line.strip())
                data_list.append(json_obj)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Please check the file's formatting.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return data_list

def clean_text(text):
    """
    Cleans the text by removing unnecessary markdown characters.
    """
    text = re.sub(r'\*\*|\#\#', '', text)
    return text.strip()

def parse_result(result):
    conversations = []
    lines = result.split('\n\n')
    
    for line in lines:
        # Match lines containing "User" or "Assistant"
        match = re.search(r'\b(User|Assistant)\b:', line, re.IGNORECASE)
        if match:
            # Determine where the actual text starts after the match
            text_start = match.end()
            text = line[text_start:].strip()
            
            cleaned_text = clean_text(text)

            if not conversations:  # This is the first conversation entry
                cleaned_text = "<image>\n" + cleaned_text
            
            # Check the specific role and handle text accordingly
            if match.group(1).lower() == "user":
                conversations.append({"from": "human", "value": cleaned_text})
            elif match.group(1).lower() == "assistant":
                conversations.append({"from": "gpt", "value": cleaned_text})

    return conversations

def convert_data(input_data):
    data = input_data
    transformed_data = []

    for entry in data:
        unique_id = str(uuid.uuid4())
        folder_name = "_".join(entry['pair_id'].split('_')[:-2])
        image_name = entry['fig_label'].replace('.txt', '.jpg')
        image_path = f"{entry['domain']}/{folder_name}/{image_name}"
        
        new_entry = {
            "id": unique_id,
            "image": image_path,
            "conversations": parse_result(entry['result'])
        }

        transformed_data.append(new_entry)
    
    return json.dumps(transformed_data, indent=2, ensure_ascii=False)

input_json_data = read_and_format_jsonl('')
output_json_data = convert_data(input_json_data)

# Write the output to a file
with open('data.json', 'w', encoding='utf-8') as f:
    f.write(output_json_data)
