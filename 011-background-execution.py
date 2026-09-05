import os
from google import genai
from dotenv import load_dotenv
import time

#load environment variables
load_dotenv()

#set parameters 
#model = "gemini-2.5-flash" #gemini-2.5-flash does not support background execution.
model = "gemini-3.7-flash" #gemini-3.7-flash supports background execution.

api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("API key is not set in environment variables")

#initialize the client
client = genai.Client(api_key=api_key)

interaction = client.interactions.create(
    model=model,
    input="Write ananalysis of the impact of artificial intelligence on modern healthcare.",
    background=True,
) 

print(f"Started background execution with interaction ID: {interaction.id}")
print(f"Status: {interaction.status}")

#Poll for completion
while True:
    result = client.interactions.get(interaction.id)
    print(f"Current status: {result.status}")
    if result.status == "completed":
        print("Background execution completed.")
        print(f"Output: {result.output_text}")
        break
    elif result.status == "failed":
        print("Background execution failed.")
        print(f"Error: {result.error}")
        break
    time.sleep(5)  # Wait for 5 seconds before polling again