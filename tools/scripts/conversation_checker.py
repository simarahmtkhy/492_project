import json

input_file = "./data/clean_data.json"
output_file = "./checked_captions.json"
data = json.load(open(input_file, encoding="utf-8"))

skipped_count = 0
new_data = []
bad_data_count = 0
for i, obj in enumerate(data):
    conversations = obj["conversations"]
    is_human = True
    is_bad = False
    for conversation in conversations:
        if is_human == True and conversation["from"] == "human":
            is_human = False
        elif is_human == False and conversation["from"] == "gpt":
            is_human = True
        else:
            bad_data_count += 1
            is_bad = True
            break
        
    if is_bad == False:
        new_data.append(obj)
        
print(f"Bad data count: {bad_data_count}")
with open(output_file, "w") as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)