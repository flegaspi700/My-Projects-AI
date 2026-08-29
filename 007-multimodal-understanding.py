import os
from dotenv import load_dotenv
from google import genai
import base64
from pathlib import Path

#load environment variables
load_dotenv()

# image path relative to this script
base_dir = Path(__file__).resolve().parent
image_path = base_dir / "images" / "20250316.jpg"

#audio path relative to this script
audio_path = base_dir / "audio" / "sample.wav"

#set parameters
model = "gemini-2.5-flash"

#initialize Gemini client
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("GENAI_API_KEY is not set in the environment variables")
    exit(1)

client = genai.Client(api_key=api_key)


#load image for multimodal understanding
with open(image_path, "rb") as image_file:
    image_bytes = image_file.read()
image_b64 = base64.b64encode(image_bytes).decode("utf-8")

#load audio for multimodal understanding
with open(audio_path, "rb") as audio_file:
    audio_bytes = audio_file.read()
audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

interaction = client.interactions.create(
    model=model,
    input=[
        {"type": "text", "text": "Can you describe the image and the audio?"},
        {
            "type": "image",
            "data": image_b64,
            "mime_type": "image/jpeg"
        },
        {
            "type": "audio",
            "data": audio_b64,
            "mime_type": "audio/wav"
       }
    ]
)
print(interaction.output_text)