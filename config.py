from google import genai
from dotenv import load_dotenv
import os
def gemini_client():
    load_dotenv("api_key.env")
    return genai.Client(api_key=os.getenv("api_key"))