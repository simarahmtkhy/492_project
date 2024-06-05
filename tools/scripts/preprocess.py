import os
import json

output_file = "./data/caption.json"
input_directory = "/Users/yigit/dev/projects/cmpe/cmpe492/pairs"
directories = os.listdir(input_directory)

output = []
for domain in directories:
    if domain.endswith('.DS_Store'):
        continue
    
    combined_directory = os.path.join(input_directory, domain)
    books = os.listdir(combined_directory)
    
    domain_output = []
    for book in books:
        if book.endswith('.DS_Store'):
            continue
        
        full_path = os.path.join(combined_directory, book)
        pairs = os.listdir(full_path)
        txt_files = [f for f in pairs if f.endswith('.txt')] 

        for txt_file in txt_files:
            with open(os.path.join(full_path, txt_file)) as f:
                lines = f.readlines()
                if len(lines) == 0:
                    continue
                
                caption = lines[0].strip().replace("\u2002", "").replace("\u00d7", "").replace("\u00b4", "").replace("\u2003", "")
                file_content = {
                    "fig_label": txt_file,
                    "fig_caption": caption,
                    "pair_id": book+"_"+txt_file,
                    "domain": domain
                }
                domain_output.append(file_content)
    output.append({domain: domain_output})
        
with open(output_file, 'w') as f:
    f.write(json.dumps(output, indent=2))