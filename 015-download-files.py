import os
from google import genai
from dotenv import load_dotenv
import requests
import tarfile
from pathlib import Path

#load environment variables
load_dotenv()
output_dir = Path("output_files")
output_dir.mkdir(exist_ok=True)

snapshot_path = output_dir / "snapshot.tar"
extracted_path = output_dir / "extracted_snapshot"

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

interaction_2 = client.interactions.create(
    agent="antigravity-preview-05-2026",
    input="Now plot the sequence as a line chart",
    environment=interaction.environment_id, #use the same environment as the previous interaction
    previous_interaction_id=interaction.id, #link to the previous interaction,
)
print(f"Interaction ID: {interaction_2.id}")
print(f"Output: {interaction_2.output_text}")

env_id = interaction.environment_id

response = requests.get(
    f"https://generativelanguage.googleapis.com/v1beta/files/environment-{env_id}:download",
    params={"alt": "media"},
    headers={"x-goog-api-key": api_key},
    allow_redirects=True,
    timeout=60
)

print(response.status_code)
print(response.headers)
print(response.text[:500] if not response.content else f"{len(response.content)} bytes")

response.raise_for_status()

with snapshot_path.open("wb") as f:
    f.write(response.content)

if not response.content:
    raise RuntimeError("The download response was empty")

with tarfile.open(snapshot_path) as tar:
    tar.extractall(path=extracted_path, filter='fully_trusted') # extract the contents of the tar file to a directory named "extracted_snapshot"