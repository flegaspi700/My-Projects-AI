import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Set Parameters
model_id = "gemini-2.5-flash"

#initialize Gemini client
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    print("Error: GENAI_API_KEY not found in environment variables.")
    exit(1)

client = genai.Client(api_key=api_key)

#query = "Explain how AI works in a few words"
#query = input("👤 Enter your query: ")
# Server-side state

interaction1 = client.interactions.create(
    model=model_id,
    input="I have 2 dogs in my house.",
)
print("🤖 Response 1:", interaction1.output_text)

interaction2 = client.interactions.create(
    model=model_id,
    input="what kind of mammals are they?",
    previous_interaction_id=interaction1.id
)
print("🤖 Response 2:", interaction2.output_text)

interaction3 = client.interactions.create(
    model=model_id,
    input="How can i take care of them?",
    previous_interaction_id=interaction1.id
)
print("🤖 Response 3:", interaction3.output_text)