import json

input_file = "./formatted.json"
output_file = "./clear_formatted.json"
data = json.load(open(input_file, encoding="utf-8"))

object_count = len(data)
print(f"Object count: {object_count}")

skipped_count = 0
new_data = []
for i, obj in enumerate(data):
    if len(obj["conversations"]) == 0:
        skipped_count += 1
    else:
        new_data.append(obj)

print(f"Skipped count: {skipped_count}")
with open(output_file, "w") as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)