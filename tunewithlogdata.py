import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
GOOGLE_API_KEY = os.getenv("SECRET_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)
def read_logs(filepath):
    """Reads a file line by line and returns a list of lines."""
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        return f"Error: File not found at {filepath}"

log_entries=read_logs('logs.txt')
training_dataset=types.TuningDataset(
        examples=[
            types.TuningExample(
                text_input=i,
                output=o,
            )
            for i,o in log_entries
        ],
    )
tuning_job = client.tunings.tune(
    base_model='models/gemini-1.5-flash-001-tuning',
    training_dataset=training_dataset,
    config=types.CreateTuningJobConfig(
        epoch_count= 5,
        batch_size=4,
        learning_rate=0.001,
        tuned_model_display_name="test tuned model"
    )
)
response = client.models.generate_content(
    model=tuning_job.tuned_model.model,
    contents='What is the peak time for errors',
)


