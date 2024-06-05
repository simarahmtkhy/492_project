#!/bin/bash

# Paths to your split JSONL files
questions_prefix=""
extension=".jsonl"
image_folder="/path_vqa_images"
model_path=""
output_folder=""

# Create the output folder if it does not exist
mkdir -p $output_folder

# Get the number of split files by counting the question parts
num_files=$(ls ${questions_prefix}*${extension} | wc -l)

# Loop through each file and execute the Python command
for i in $(seq 1 $num_files)
do
    questions_file="${questions_prefix}${i}${extension}"
    answers_file="${output_folder}/generated_answers_${i}${extension}"
    
    echo "Processing $questions_file"
    
    # Execute the Python command
    python model_vqa.py \
        --model-path $model_path \
        --question-file $questions_file \
        --image-folder $image_folder \
        --answers-file $answers_file
    
    # Check if the Python script executed successfully
    if [ $? -ne 0 ]; then
        echo "Error processing $questions_file"
        exit 1
    fi
done

echo "All files processed successfully."

