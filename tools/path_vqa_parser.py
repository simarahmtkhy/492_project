import pandas as pd
import json
import os
from PIL import Image
import io


# Create directories to store images if they do not exist
images_dir = 'path_vqa_images'
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

# Initialize a list to store questions and answers
qa_list = []

# Loop through the dataframe to save images and collect Q&A
for file in os.listdir(''):
    if file.endswith('.parquet') and file.startswith('test'):
        df = pd.read_parquet(f'{file}')
    else:
        continue
    for index, row in df.iterrows():
        image_data = row['image']  # Assuming 'image' column contains binary image data
        question = row['question']
        answer = row['answer']
        
        # Save image
        image = Image.open(io.BytesIO(image_data['bytes']))
        image_file_path = image_data['path']
        image.save(image_file_path)
        
        # Append question and answer to the list
        qa_list.append({
            'question': question,
            'answer': answer,
            'image_path': image_file_path
        })

# Save questions and answers to a JSON file
qa_json_file_path = 'questions_answers.json'
with open(qa_json_file_path, 'w') as json_file:
    json.dump(qa_list, json_file, indent=4)

print(f'Images saved to {images_dir} and Q&A saved to {qa_json_file_path}')
