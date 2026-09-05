import os
from google import genai
from dotenv import load_dotenv

#load environment variables
load_dotenv()

#set parameters
model = "gemini-2.5-flash"

#get the API key from environment variables
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("API key is not set in environment variables")

#create a client instance
client = genai.Client(api_key=api_key)

# Create an interaction with the model
# Set Instructions to specify the behavior of the model
# Set configurations to customize the model's behavior
interaction = client.interactions.create(
    model=model,
    input="Explain how AI works in simple terms.",
    system_instruction="You are an AI assistant that explains complex concepts in simple terms for beginners.",
    generation_config={
        "temperature": 1.0, # Controls the randomness of the output. Higher values (e.g., 1.0) make the output more random, while lower values (e.g., 0.2) make it more deterministic.  
        "max_output_tokens": 1500, #Limits the maximum number of tokens in the output. This helps control the length of the response.
        "top_p": 0.9, # Implements nucleus sampling. The model considers only the most probable tokens whose cumulative probability exceeds the top_p value. This helps in generating more focused and coherent responses.  
        "stop_sequences": ["\n"], # Specifies sequences where the model should stop generating further tokens. This can be useful to prevent the model from producing overly long responses or to enforce a specific format.    
    }   
)

print(interaction.output_text)