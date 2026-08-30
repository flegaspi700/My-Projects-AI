import os
from dotenv import load_dotenv
from google import genai

#load environment variables
load_dotenv()

model = "gemini-2.5-flash"

api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the GENAI_API_KEY environment variable.")

#initialize the GenAI client
client = genai.Client(api_key=api_key)

#call tools
interaction = client.interactions.create(
    model=model,
    input="Who is the NBA champion in 2026?",
    tools=[{"type": "google_search"}]
)

print(interaction.output_text)

#print citations
for step in interaction.steps:
    if step.type == "model_output":
        for content_block in step.content:
            if content_block.type == "text" and content_block.annotations:
                print("\nCitations:")
                for annotation in content_block.annotations:
                    if annotation.type == "url_citation":
                        print(f"  [{annotation.title}]({annotation.url})")