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
    input="Search for the latest AI research papers on reasoning and summarize them.",
    environment="remote",
    agent_config={
        "type": "antigravity",
        "max_total_tokens": 50000,
        "model": "gemini-3.5-flash-lite",
    },
    tools=[
        {"type": "google_search"},
        {"type": "url_context"},
    ],
)

print(interaction.output_text)