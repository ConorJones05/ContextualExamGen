from openai import OpenAI
from tools import write_to_file

client = OpenAI()


def upload_file(batch_jsonl_file):
    batch_input_file = client.files.create(
        file=open(batch_jsonl_file, "rb"),
        purpose="batch"
    )
    print("Sucessfully created jsonl file.")

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
    
