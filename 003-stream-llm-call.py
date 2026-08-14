import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# load environment variables from .env file
load_dotenv()

# Set Parameters
model_id = "gemini-2.5-flash" #or "gemini-1.5-pro"

# Initialize Gemini client
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    print("Error: GENAI_API_KEY not found in environment variables.")
    exit(1)

client = genai.Client(api_key=api_key)

#create a chat session outside the loop to maintain context across multiple queries
chat = client.chats.create(model=model_id)

print("🤖 Chatbot initialized! Type 'exit' to quit.\n" + "-" * 40)

while True:
    #query to send to Gemini
    query = input("\n 👤 Enter your query: ")
    if query.lower().strip() == 'exit':
        print("Exiting the program.")
        break

    try:
        print("\n 🤖 System call", end='', flush=True)
        # 2. use send_message_stream to stream the response from the model
        response_stream = chat.send_message_stream(
            message=query,
            config=types.GenerateContentConfig(
                max_output_tokens=500,
            ),
        )

        # iterate over the streamed response and print it in real-time
        for chunk in response_stream:
            print(chunk.text, end='', flush=True)

    except Exception as e:
        print(f"Error calling Gemini: {e}")