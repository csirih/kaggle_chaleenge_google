import os
from google import genai
from google.genai import types
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from flask import Flask, jsonify
import subprocess
from flask import request, make_response
import chromadb

DB_NAME = "logsdb"
def checkIssues(log:str)-> str:
    # Set up the API key
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(BASEDIR, '.env'))
    GOOGLE_API_KEY = os.getenv("SECRET_KEY")
    client = genai.Client(api_key=GOOGLE_API_KEY)

    # Generate embeddings
    response = client.models.embed_content(
        model='models/text-embedding-004',
        contents=texts,
        config=types.EmbedContentConfig(task_type='semantic_similarity')
    )

@app.route('/askAops', methods =['POST'])
@token_required
def get_contextdata(log:str)-> str:
  file = open("issues.csv", "r")
  chroma_client = chromadb.Client()
  db = chroma_client.get_or_create_collection(name=DB_NAME, embedding_function=checkIssues(log))
  db.add(documents=documents, ids=[str(i) for i in range(len(documents))])
  datapoints=sum(list(csv.reader(file,delimiter=",")),[])
  datapoints_as_string = ', '.join(datapoints)
  prompt=f"""You are a helpful and informative bot that check if the health of the application is good.
  strike a friendly and converstional tone. If the passage is irrelevant to the answer, you may ignore it.
  QUESTION: {datapoints_as_string}
  """
  result = db.query(query_texts=[log], n_results=1)
  [all_passages] = result["documents"]
  answer = client.models.generate_content(
           model="gemini-2.0-flash",
           contents=prompt)

  responseStr = "{" + '"answer"' + ":" + response.text + "}"
  return responseStr
