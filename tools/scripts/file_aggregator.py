from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--output_path', type=str, default='data/generated_captions.json')
args = parser.parse_args()

input_files = [
    'data/gen_gemini_1_filtered.jsonl',
    'data/gen_gemini_2_filtered.jsonl',
    'data/gen_groq_filtered.jsonl',
]

with open(args.output_path, 'w') as f:
    for input_file in input_files:
        with open(input_file) as f_in:
            f.writelines(f_in.readlines())