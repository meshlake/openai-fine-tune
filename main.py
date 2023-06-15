import os
import time
import openai
from openai import cli

openai.api_key = os.getenv("OPENAI_API_KEY")

training_file_name = './data/training_data_1.jsonl'

training_file_id = cli.FineTune._get_or_upload(training_file_name, True)

upload_status = openai.File.retrieve(training_file_id)["status"]

print(f'File ID: {training_file_id}, Status: {upload_status}')

create_args = {
    "training_file": training_file_id,
    # "validation_file": validation_file_id,
    "model": "davinci",
    "n_epochs": 15,
    "batch_size": 3,
    "learning_rate_multiplier": 0.3
}

response = openai.FineTune.create(**create_args)
job_id = response["id"]
status = response["status"]

print(f'Fine-tunning model with jobID: {job_id}.')
print(f"Training Response: {response}")
print(f"Training Status: {status}")