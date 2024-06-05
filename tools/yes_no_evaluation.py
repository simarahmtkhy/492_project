import json

# Paths to the input files
answer_key_file_path = ''
generated_answers_file_path = ''
inspection_output_file_path = ''
# Initialize dictionaries to store question IDs with "yes" and "no" answers
yes_question_ids = set()
no_question_ids = set()
labels = ['yes', 'no']
results_file = ''
results = open(results_file, 'w')

# Open and read the answer key JSONL file
with open(answer_key_file_path, 'r') as file:
    for line in file:
        entry = json.loads(line.strip())
        question_id = entry['question_id']
        answer_text = entry['text'].strip().lower()
        
        if answer_text == 'yes':
            yes_question_ids.add(question_id)
        elif answer_text == 'no':
            no_question_ids.add(question_id)

results.write(f'Found {len(yes_question_ids)} "yes" question IDs and {len(no_question_ids)} "no" question IDs.\n')
results.write(f'Total: {len(yes_question_ids) + len(no_question_ids)}\n')
# Initialize a list to store question IDs for later inspection
inspection_list = []

# Function to check if the generated answers start with the label
def check_generated_answers(question_ids, label):
    matches = 0
    total = 0
    
    with open(generated_answers_file_path, 'r') as file:
        for line in file:
            entry = json.loads(line.strip())
            question_id = entry['question_id']
            generated_answer = entry['text'].strip().lower()
            
            if question_id in question_ids:
                if generated_answer.startswith(labels[0]) or generated_answer.startswith(labels[1]):
                    total += 1
                    if generated_answer.startswith(label):
                        matches += 1
                else:
                    inspection_list.append({
                        "question_id": question_id,
                        "question": entry["prompt"],
                        "correct_answer": label,
                        "generated_answer": generated_answer
                    })



    return matches, total

# Check the generated answers for "yes" and "no" question IDs
yes_matches, yes_total = check_generated_answers(yes_question_ids, 'yes')
no_matches, no_total = check_generated_answers(no_question_ids, 'no')

# Print the results
results.write(f'Matches for "yes" answers: {yes_matches}/{yes_total} ({yes_matches/yes_total:.2%})\n')
results.write(f'Matches for "no" answers: {no_matches}/{no_total} ({no_matches/no_total:.2%})\n')
results.write(f'Total matches: {yes_matches + no_matches}/{yes_total + no_total} ({(yes_matches + no_matches)/(yes_total + no_total):.2%})\n')

# Print the list of question IDs for later inspection
if inspection_list:
    with open(inspection_output_file_path, 'w') as outfile:
        json.dump(inspection_list, outfile, indent=4)
    results.write(f'Wrote {len(inspection_list)} question IDs to {inspection_output_file_path} for inspection.\n')
else:
    results.write('All generated answers are in the correct format.\n')
