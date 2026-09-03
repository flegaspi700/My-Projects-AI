import os
from google import genai
from dotenv import load_dotenv

#load environment variables
load_dotenv()

#set parameters
# don't need the model parameter for managed agents.
#model = "gemini-2.5-flash"

api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("API key is not set in environment variables")

#initialize the client
client = genai.Client(api_key=api_key)

interaction = client.interactions.create(
    agent="antigravity-preview-05-2026",
    input="Write a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt. Save the file locally. Then read the file and print its contents.",
    environment="remote", #files will be created inside the agent’s remote environment
)
print(f"Interaction ID: {interaction.id}")
print(f"Environment: {interaction.environment_id}")
print(f"Output: {interaction.output_text}")