import os

from google import genai
from google.genai import types
from dotenv import load_dotenv
import pandas as pd
from vertexai.evaluation import EvalTask
import vertexai
file = open('askAopsModel', 'r')
tuned_model = file.read()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "my_service_account.json"

def custom_model_fn(input: str) -> str:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(BASEDIR, '.env'))
    GOOGLE_API_KEY = os.getenv("SECRET_KEY")
    client = genai.Client(api_key=GOOGLE_API_KEY)

    low_temp_config = types.GenerateContentConfig(temperature=0.1)
    response =client.models.generate_content(

        model=tuned_model,
        config=low_temp_config,
        contents='Internal Server Error: Unexpected null value'
    )
    return response.text
eval_dataset = pd.DataFrame({
        "prompt"  : ['host="ivapp03" code="200" env="prod" timestamp="2024-06-02T08:05:18Z" sourceIP="192.0.2.123" details="Successful login for user: customer_jane"'],
        "reference": ['Not Issue'],
  },
{
        "prompt"  : ['host="ivapp01" code="500" env="prod" timestamp="2024-06-13T11:50:00Z" sourceIP="203.0.113.8" details="Database connection error during user session retrieval"'],
        "reference": ['Issue'],
  }
)
vertexai.init(project='peak-sorter-411617')

result = EvalTask(
      dataset=eval_dataset,
      metrics=["rouge_1", "rouge_l"],
      experiment="my-experiment",
  ).evaluate(
      model=tuned_model,
      experiment_run_name="gpt-eval-run"
  )
