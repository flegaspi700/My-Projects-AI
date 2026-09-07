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

interaction = client.interactions.create(
    agent="antigravity-preview-05-2026",
    input="Read Hacker News, summarize the top 10 stories, and save the results as a PDF.",
    environment="remote",
    agent_config={
        "type": "antigravity",
        "max_total_tokens": 50000,
        "model": "gemini-3.5-flash-lite",
    }
)

print(f"Status: {interaction.status}") #'incomplete' - if budget was hit. 
print(f"Tokens used: {interaction.usage.total_tokens}")