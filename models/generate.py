import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # API key from environment variables
)

def generate_image_from_prompt(prompt):
    """Generate a Ghibli-style image from a text prompt"""
    try:
        response = client.images.generate(
            model="dall-e-2",  # Specify DALL-E model
            prompt=prompt,
            n=1,
            size="512x512"
        )
        return response.data[0].url
    except Exception as e:
        print(f"Error generating from prompt: {e}")
        return None

def convert_image_to_ghibli(image_path):
    """Convert an uploaded image into Ghibli style"""
    try:
        with open(image_path, "rb") as image_file:
            response = client.images.create_variation(
                image=image_file,
                model="dall-e-2",  # Specify model
                n=1,
                size="512x512"
            )
        return response.data[0].url
    except Exception as e:
        print(f"Error converting image: {e}")
        return None
