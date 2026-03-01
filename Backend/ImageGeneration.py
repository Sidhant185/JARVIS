import asyncio
import aiohttp
from random import randint
from PIL import Image
import os
import re
from time import sleep
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

USERNAME = os.getenv("Username")
ASSISTANT_NAME = os.getenv("AssistantName")
HUGGINGFACE_API_KEY = os.getenv("HuggingFaceAPIKey")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# -----------------------------
# Image folder setup
# -----------------------------
IMAGE_FOLDER = r"Data/Images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# -----------------------------
# Function to open and display images
# -----------------------------
def open_images(prompt):
    safe_prompt = re.sub(r'[^a-zA-Z0-9_]', '_', prompt.replace(" ", "_"))
    files = [os.path.join(IMAGE_FOLDER, f"{safe_prompt}{i}.jpg") for i in range(1, 5)]

    for image_path in files:
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")

# -----------------------------
# Async function to query Hugging Face API
# -----------------------------
async def query(payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=HEADERS, json=payload) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"Error {resp.status}: {text}")
            return await resp.read()

# -----------------------------
# Async function to generate images
# -----------------------------
async def generate_images(prompt: str):
    tasks = []
    safe_prompt = re.sub(r'[^a-zA-Z0-9_]', '_', prompt.replace(" ", "_"))

    for _ in range(4):
        payload = {
            "inputs": prompt,
            "options": {"wait_for_model": True},
            "parameters": {
                "seed": randint(0, 1000000),
                "width": 1024,
                "height": 1024,
                "num_inference_steps": 50,
            }
        }
        tasks.append(asyncio.create_task(query(payload)))

    image_bytes_list = await asyncio.gather(*tasks)

    # Save images
    for i, image_bytes in enumerate(image_bytes_list):
        image_path = os.path.join(IMAGE_FOLDER, f"{safe_prompt}{i+1}.jpg")
        with open(image_path, "wb") as f:
            f.write(image_bytes)
        print(f"Saved image: {image_path}")

# -----------------------------
# Wrapper to generate and open images
# -----------------------------
def GenerateImages(prompt: str):
    print(f"Starting image generation for: {prompt}")
    asyncio.run(generate_images(prompt))
    open_images(prompt)
    print("All images generated and opened successfully!\n")

# -----------------------------
# Interactive test function
# -----------------------------
def test_image_generation():
    print(f"Hello {USERNAME}, I am {ASSISTANT_NAME}. Let's test your image generation!")
    while True:
        prompt = input("Enter a prompt (or 'exit' to quit): ").strip()
        if prompt.lower() == "exit":
            print("Exiting test. Goodbye!")
            break
        elif prompt == "":
            print("Prompt cannot be empty. Try again.")
            continue

        try:
            GenerateImages(prompt)
        except Exception as e:
            print(f"An error occurred: {e}")

# -----------------------------
# Main entry point
# -----------------------------
if __name__ == "__main__":
    test_image_generation()
