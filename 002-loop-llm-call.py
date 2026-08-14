import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# load environment variables from .env file
load_dotenv()

#set Parameters
model_id = "gemini-2.5-flash" #or "gemini-1.5-pro"

#initialize Gemini client
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
    query = input("👤 Enter your query: ")
    if query.lower() == 'exit':
        print("Exiting the program.")
        break

    #make the API call using Gemini
    try:
        print("🤖 System call")
        # 2. Send the message through the chat session
        response = chat.send_message(
            message=query,
            config=types.GenerateContentConfig(
                max_output_tokens=200,
            ),
        )

        print(f"👤 Query: {query}")
        print(f"\nResponse:\n{response.text}")

    except Exception as e:
        print(f"Error calling Gemini: {e}")