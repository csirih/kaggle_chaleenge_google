import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def evaluateTrainedModel():
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(BASEDIR, '.env'))

    GOOGLE_API_KEY = os.getenv("SECRET_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("SECRET_KEY not found in .env file")

    client = genai.Client(api_key=GOOGLE_API_KEY)

    model_path = os.path.join(BASEDIR, 'askAopsModel')
    with open(model_path, 'r') as file:
        tuned_model = file.read()

    judgePrompt = """
    Please first list down the instructions in the user query.
    Please highlight such specific keywords.
    After listing down instructions, you should rank the instructions in the order of importance.
    """

    low_temp_config = types.GenerateContentConfig(
        temperature=0.1,
        system_instruction=judgePrompt
    )

    try:
        response = client.models.generate_content(
            model=tuned_model,
            config=low_temp_config,
            contents=[types.ContentPart(text="Internal Server Error: Unexpected null value")]
        )
        print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")
