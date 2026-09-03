import os
from google import genai
from dotenv import load_dotenv
import time

#load environment variables
load_dotenv()

#set parameters
model = "gemini-2.5-flash"

api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("API key is not set in environment variables")

#initialize the client
client = genai.Client(api_key=api_key)
