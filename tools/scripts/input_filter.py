from argparse import ArgumentParser
import json

parser = ArgumentParser()
parser.add_argument('--input_path', type=str, required=True)
parser.add_argument('--used_output_path', type=str, required=True)
parser.add_argument('--output_path', type=str, required=True)
args = parser.parse_args()

used_captions = set()
with open(args.used_output_path) as f:
    for line in f.readlines():
        line_data = json.loads(line)
        used_captions.add(line_data['pair_id'])

with open(args.input_path) as f:
    data = json.load(f)

filtered_data = []
for item in data:
    is_empty = True
    keys_to_remove = []
    
    for domain_name, samples in item.items():
        filtered_samples = [sample for sample in samples if sample['pair_id'] not in used_captions]
        if filtered_samples:
            item[domain_name] = filtered_samples
            is_empty = False
        else:
            keys_to_remove.append(domain_name)
    
    for key in keys_to_remove:
        del item[key]
    
    if not is_empty:
        filtered_data.append(item)

with open(args.output_path, 'w') as f:
    json.dump(filtered_data, f, indent=4)