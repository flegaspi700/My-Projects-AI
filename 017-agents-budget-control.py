import os
from google import genai
from dotenv import load_dotenv

#load environment variables
load_dotenv()

api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("API key is not set in environment variables")

#initialize the client
client = genai.Client(api_key=api_key)

#For antigravity-preview-05-2026, the default model is Gemini 3.8 Flash (gemini-3.8-flash). 
interaction = client.interactions.create(
    agent="antigravity-preview-05-2026",
    input="Read Hacker News, summarize the top 10 stories.",
    environment="remote",
    agent_config={
        "type": "antigravity",
        "max_total_tokens": 50000,
        "model": "gemini-3.5-flash-lite",
    }
)

print(interaction.output_text)
print(f"Status: {interaction.status}") #'incomplete' - if budget was hit. 
print(f"Tokens used: {interaction.usage.total_tokens}")