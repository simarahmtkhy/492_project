import json

# Path to your input JSON file
json_file_path = ''

# Load the JSON data
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Paths to the output JSONL files
questions_file_path = ''
answers_file_path = ''

# Initialize the question ID
question_id = 0

# Open the output files in write mode
with open(questions_file_path, 'w') as questions_file, open(answers_file_path, 'w') as answers_file:
    for entry in data:
        # Create the question entry
        question_entry = {
            "question_id": question_id,
            "image": entry["image_path"].split('/')[-1],
            "text": entry["question"]
        }
        
        # Create the answer entry
        answer_entry = {
            "question_id": question_id,
            "text": entry["answer"]
        }
        
        # Write the entries to the respective JSONL files
        questions_file.write(json.dumps(question_entry) + '\n')
        answers_file.write(json.dumps(answer_entry) + '\n')
        
        # Increment the question ID
        question_id += 1

print(f'Questions and answers have been written to {questions_file_path} and {answers_file_path}')
