import os
import time
import UtilClass
import csv
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv
import random
from difflib import get_close_matches
def trainData():
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(BASEDIR, '.env'))
    GOOGLE_API_KEY = os.getenv("SECRET_KEY")
    client = genai.Client(api_key=GOOGLE_API_KEY)
    def filterErrors(log:str):

        file = open("issues.csv", "r")
        datapoints=sum(list(csv.reader(file,delimiter=",")),[])
        if "code=\"200\"" not in log and len(get_close_matches( re.search(r"details=\s*(\D+)", log).group(1) , datapoints, cutoff=0.4))>0:
            return [log,"issue"]
        else:
            return [log,"not issue"]

    def read_logs(filepath):
        """Reads a file line by line and returns a list of lines."""
        try:
            with open(filepath, 'r') as file:
                lines = file.readlines()
                temp = [filterErrors(l) for l in lines if  re.search(r"details=\s*(\D+)", l)]
                logs = [log for log in temp if log is not None]

            return logs
        except FileNotFoundError:
            return f"Error: File not found at {filepath}"

    log_entries=read_logs("logs.txt")

    training_dataset=types.TuningDataset(
            examples=[
                types.TuningExample(
                    text_input=i,
                    output=o,
                )
                for i,o in log_entries
            ],
        )
    id=f"askAop-classifier-{random.randint(10000, 99999)}"
    system_instruct =[
    "You are a classification service. You will be passed input that represents",
    "a log snippet and you must respond if the log has an issue"
    ]
    tuning_job = client.tunings.tune(
        base_model='models/gemini-1.5-flash-001-tuning',
        training_dataset=training_dataset,
        # system_instruction=system_instruct,
        config=types.CreateTuningJobConfig(
            epoch_count= 3,
            tuned_model_display_name="AskaOPSmodel"
        )
    )


    while not tuning_job.has_ended:
        print(tuning_job.name)
        tuning_job = client.tunings.get(name=tuning_job.name)
        time.sleep(10)


    tuning_job = client.tunings.get(name=tuning_job.name)
    tuned_model = tuning_job.tuned_model.endpoint


    file_path = "askAopsModel"


    file = open(file_path, "w")
    file.write(tuned_model)
    file.close()



