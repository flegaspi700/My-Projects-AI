import os
from dotenv import load_dotenv
from google import genai
import base64
from pathlib import Path

#load environment variables
load_dotenv()

#set parameters
model = "gemini-2.5-flash-image"
output_file = "generated_image.png"

api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the GENAI_API_KEY environment variable.")
    #exit(1)

#initialize the GenAI client
client = genai.Client(api_key=api_key) 

#generate the image and save it in the images directory
try:
    os.makedirs("images", exist_ok=True)
    output_file = os.path.join("images", output_file)

    interaction = client.interactions.create(
        model=model,
        input="Generate an image of a futuristic city skyline at sunset",
    )

    with open(output_file, "wb") as f:
        f.write(base64.b64decode(interaction.output_image.data))

    print(f"Image generated and saved to {output_file}")
except Exception as e:
    print(f"Failed to generate image: {e}")