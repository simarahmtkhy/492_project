# Built in
import time
import json
import itertools
import os
import asyncio

# Local
import instruct_few_shot_examples

# Third Party
import argparse
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()
api_keys = [
    os.getenv("API_KEY_2"),
    os.getenv("API_KEY_3"),
    os.getenv("API_KEY_4"),
    os.getenv("API_KEY_5"),
    os.getenv("API_KEY_6"),
    os.getenv("API_KEY_7"),
]

class InstructGenerator:
    def __init__(self):
        model_args = {
            "temperature": 0,
            "model_name": "llama3-8b-8192",
            "max_tokens": 200
        }
        
        self.models = [
            ChatGroq(groq_api_key=key, **model_args) for key in api_keys
        ]
        self.messages = []
        
        self.system_message = """
            You are an AI assistant specialized in biomedical topics.

            You are provided with a text description (Figure Caption) of a figure image from a biomedical research paper. In some cases, you may have additional text (Figure Context) that mentions the image. Unfortunately, you don't have access to the actual image.

            Your task is to generate a conversation between a person (User) inquiring about the image and you (Assistant) responding to their questions. The conversation should proceed as though both the User and Assistant are viewing the image, while not referring to the text information (Figure Caption and Figure Context). 

            Below are requirements for generating the questions and answers in the conversation:
            - Avoid quoting or referring to specific facts, terms, abbreviations, dates, numbers, or names, as these may reveal the conversation is based on the text information, rather than the image itself. Focus on the visual aspects of the image that can be inferred without the text information.
            - Do not use phrases like "mentioned", "caption", "context" in the conversation. Instead, refer to the information as being "in the image."
            - Ensure that questions are diverse and cover a range of visual aspects of the image.
            - The conversation should include at least 2-3 turns of questions and answers about the visual aspects of the image.
            - Answer responsibly, avoiding overconfidence, and do not provide medical advice or diagnostic information. Encourage the user to consult a healthcare professional for advice.
                        
            Caption:
        """
        self.messages.append(SystemMessage(self.system_message))
        
        for ex in instruct_few_shot_examples.fs:
            user_message = self.context_gen(ex)
            self.messages.append(HumanMessage(user_message))
            
            assistant_message = self.conv_to_str(ex['conversations'])
            self.messages.append(AIMessage(assistant_message))

    def context_gen(self, sample):
        return f"Figure Caption: {sample['fig_caption']}"

    def conv_to_str(self, conv):
        return "\n\n".join([("User: " if x["from"] == "human" else "Assistant: ") + x["value"] for x in conv])
        
    async def process_tasks(self, tasks, output_path):
        results = await asyncio.gather(*tasks)
        flatten_results = list(itertools.chain(*results))
        with open(output_path, 'a') as f:
            for line in flatten_results:
                f.write(json.dumps(line)+'\n')
            print("Batch processed.")
    
    async def process_batch(self, batch, switch_count=0):
        humman_messages = [ HumanMessage(self.context_gen(sample)) for sample in batch ]
        inputs = [self.messages + [message] for message in humman_messages]
        try:
            predictions = await self.models[switch_count].abatch(inputs)
            for sample, prediction in zip(batch, predictions):
                sample['result'] = prediction.content
            print(f"Batch is processed by key {switch_count}")
        except Exception as e:
            print(f"Error: {e}")
            for sample in batch:
                sample['result'] = "error"
        return batch
        
    async def generate_instructions(self, max_size, input_path='data/input.json', output_path='data/gen.jsonl', batch_size=10):        
        with open(input_path) as f:
            data = json.load(f)
        
        counter = 0
        sample_list = []
        
        for item in data:
            for domain_name, samples in item.items():
                for sample in samples:
                    if counter >= max_size:
                        break
                    sample_list.append(sample)
                    counter += 1
            if counter >= max_size:
                break
            
        switch_count = 0
        batched_samples = [sample_list[i:i+batch_size] for i in range(0, len(sample_list), batch_size)]
        tasks = []
        start_time = time.time()
        for batch in batched_samples:
            tasks.extend([self.process_batch(batch, switch_count)])
            switch_count += 1
            print("Batch is sent.")

            if switch_count % len(api_keys) == 0:
                await self.process_tasks(tasks, output_path)
                with open("logs.txt", "a") as f:
                    f.write("Batch processed\n")
                tasks = []
                switch_count = 0
                
                elapsed_time = time.time() - start_time
                if elapsed_time < 60:   
                    sleep_time = 60 - elapsed_time                 
                    print(f"Sleeping for {sleep_time} seconds.")
                    time.sleep(sleep_time)
                    start_time = time.time()
                
        if tasks:
            await self.process_tasks(tasks, output_path)
                    
async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, default='caption.json')
    parser.add_argument('--output_path', type=str, default='gen.jsonl')
    parser.add_argument('--max_size', type=int, default=130000)
    parser.add_argument('--batch_size', type=int, default=10)
    args = parser.parse_args()

    start_time = time.time() 
    generator = InstructGenerator()
    await generator.generate_instructions(
        input_path=args.input_path,
        output_path=args.output_path,
        max_size=args.max_size,
        batch_size=args.batch_size
    )
    end_time = time.time()
    
    print(f"Time taken: {end_time - start_time} seconds")
    
if __name__ == '__main__':
    asyncio.run(main())