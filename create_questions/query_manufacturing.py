from openai import OpenAI
from tools import *
import os
from dotenv import load_dotenv
import json
import regex as re 

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def upload_file(batch_jsonl_file, path_for_for_key):
    batch_input_file = client.files.create(
        file=open(batch_jsonl_file, "rb"),
        purpose="batch"
    )
    write_to_file(f'{path_for_for_key}/key_for_batch', batch_input_file.id)
    print("Sucessfully created jsonl file.")
    print(f"Batch job {batch_input_file}")
    return batch_input_file


def create_batch_job(batch_input_file: str):
    batch_input_file_id = batch_input_file.id
    client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
            "description": "Batch job for test creation"
        }
)
    

def check_status(batch_input_file_id: str):
    batch = client.batches.retrieve("batch_abc123")
    print(batch)


def create_jsonl_file(path: str, model: str, context):
    files = os.scandir(f"{path}/preprocessed_files")
    file_list = []
    for x in files:
        file_list.append(x)
    
    json_list = []
    
    for file in file_list:
        code = ""
            
        with open(os.path.join(f"{path}/preprocessed_files", file.name), 'r', encoding='utf-8') as f:
            code += f.read()

        data = {f"custom_id": file.name, 
            "method": "POST", 
            "url": "/v1/chat/completions", 
            "body": {"model": model, "messages": [{"role": "system", "content": context},
                                                                {"role": "user", "content": code}],"max_tokens": 500}}
        
        json_list.append(data)

        print(f"Finished JSON {file.name}")
                
    with open("output.jsonl", 'w', encoding='utf-8') as f:
        for i in json_list:
            f.write(json.dumps(i) + '\n') 
    print(f"Finished {file}")


def create_prompt(questions: int, learned: str, base: str):
    base_query = read_file(base)
    return base_query.replace("<questions>", str(questions)).replace("<topics>", learned)

    


# create_jsonl_file(r"C:\Users\conor\LLM_Question_Gen\test_files\data\testing", "gpt-3.5-turbo-0125", "hello")
print(create_prompt(1, "dsfg", r"C:\Users\conor\LLM_Question_Gen\create_questions\premade_querys\what_if.txt"))