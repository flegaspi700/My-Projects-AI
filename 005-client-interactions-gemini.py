import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Set Parameters
model_id = "gemini-2.5-flash"

# Initialize Gemini client
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    print("Error: GENAI_API_KEY not found in environment variables.")
    exit(1)

client = genai.Client(api_key=api_key)

stream = client.interactions.create(
    model=model_id,
    input="Explain how AI works?",
    stream=True
)

for events in stream:
    print(events, end="", flush=True)