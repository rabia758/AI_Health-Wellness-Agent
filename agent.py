import os
import openai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables!")

openai.api_key = api_key

def list_available_models():
    models = openai.Model.list()
    print("Available models:")
    for model in models["data"]:
        print(f"- {model['id']}")

if __name__ == "__main__":
    list_available_models()
