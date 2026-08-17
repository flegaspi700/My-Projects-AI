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

#query = "Explain how AI works in a few words"
query = input("👤 Enter your query: ")

stream = client.interactions.create(
    model=model_id,
    input=query,
    stream=True
)

for event in stream:
    if event.event_type == "step.delta":
        if event.delta.type == "text":
            print(event.delta.text, end="", flush=True)