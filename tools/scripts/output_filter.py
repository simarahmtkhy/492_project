from argparse import ArgumentParser
import json

parser = ArgumentParser()
parser.add_argument('--input_path', type=str, default='caption.json')
parser.add_argument('--output_path', type=str, default='gen.jsonl')
args = parser.parse_args()

filtered_lines = []
with open(args.input_path) as f:
    for line in f.readlines():
        line_data = json.loads(line)
        
        if line_data['result'] != 'error' and line_data['result'] != "":
            filtered_lines.append(line)

with open(args.output_path, 'w') as f:
    f.writelines(filtered_lines)        