import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
GOOGLE_API_KEY = os.getenv("SECRET_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)
high_temp_config = types.GenerateContentConfig(temperature=2.0)
prompt='''
You are a log generator for a ecommerce application . Create log sample data for 30 days which has both positive and negative scenarios. Generate output in a text file . Log entries should have below fields:
  - host (should start with ivapp)
  - code (HTML response codes)
  - env (prod)
  - timestamp
  - source IP
  -  details
  - severity ( should display log level)
'''
response = client.models.generate_content(
      model='gemini-2.0-flash',
      config=high_temp_config,
      contents=prompt)
n=0
for n in range(10):
    if response.text:
          with open("Output.txt", "w") as text_file:
             text_file.write(response.parsed)
