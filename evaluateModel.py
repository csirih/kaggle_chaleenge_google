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
def evaluateTrainedModel():
     BASEDIR = os.path.abspath(os.path.dirname(__file__))
     load_dotenv(os.path.join(BASEDIR, '.env'))
     GOOGLE_API_KEY = os.getenv("SECRET_KEY")
     client = genai.Client(api_key=GOOGLE_API_KEY)
     file = open('askAopsModel', 'r')
     tuned_model = file.read()
     client = genai.Client(api_key=GOOGLE_API_KEY)
     judgePrompt="""
     Please first list down the instructions in the user query.
     Please highlight such specific keywords.
     After listing down instructions, you should rank the instructions in the order of importance.
     """
     low_temp_config = types.GenerateContentConfig(temperature=0.1,system_instruction=judgePrompt)
     response = client.models.generate_content(

          model=tuned_model,
          config=low_temp_config,
          contents='Internal Server Error: Unexpected null value'
     )
     print(response.text)


