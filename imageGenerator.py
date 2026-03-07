#!/usr/bin/env python3
"""
imageGenerator.py
-----------------
This script parses a structured JSON file containing DIY project data,
extracts image generation prompts for each project (Easy, Medium, Hard),
and generates corresponding images using Hugging Face's Stable Diffusion API (free tier).

Dependencies:
    pip install requests

Environment Variables:
    export HF_TOKEN="your_huggingface_token_here"

Get a free token from:
    https://huggingface.co/settings/tokens
"""

import json
import os
import requests
from datetime import datetime

# ========== CONFIGURATION ==========
JSON_FILE = "output_prod.json"  # Input file
OUTPUT_DIR = "generated_images"  # Output directory
HF_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"  # Free model for basic image gen
# ===================================


def save_image(file_path: str, data: bytes):
    """Save image data to file."""
    with open(file_path, "wb") as f:
        f.write(data)
    print(f"🖼️ Image saved → {file_path}")


def load_json(filepath: str):
    """Load JSON data safely."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise SystemExit(f"❌ JSON file not found: {filepath}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"❌ Error decoding JSON: {e}")


def extract_prompts(data: dict):
    """Extract image generation prompts from JSON."""
    if "Projects" not in data:
        raise KeyError("❌ JSON missing 'Projects' key.")
    prompts = {}
    for difficulty, project in data["Projects"].items():
        name = project.get("DIY_Product", "Unnamed Project").split(".")[0].strip()
        prompt = project.get("Image_Generation_Prompt", "").strip()
        prompts[difficulty] = {"Project_Name": name, "Prompt": prompt}
    return prompts


def generate_images_with_huggingface(prompts: dict):
    """Generate images using Hugging Face Stable Diffusion API."""
    api_key = os.getenv("HF_TOKEN", "your api")
    if not api_key:
        raise SystemExit("❌ Missing HF_TOKEN environment variable.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    headers = {"Authorization": f"Bearer {api_key}"}

    for difficulty, info in prompts.items():
        project_name = info["Project_Name"]
        prompt = info["Prompt"]

        print(f"\n✨ Generating image for [{difficulty}] → {project_name}")
        print(f"🧠 Prompt: {prompt[:120]}...")

        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=headers,
            json={"inputs": prompt},
        )

        if response.status_code == 200:
            safe_name = project_name.replace(" ", "_").replace("/", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(
                OUTPUT_DIR, f"{difficulty.lower()}_{safe_name}_{timestamp}.png"
            )
            save_image(file_path, response.content)
        elif response.status_code == 503:
            print("⏳ Model is loading on Hugging Face — please wait and retry.")
        else:
            print(f"❌ Error ({response.status_code}): {response.text[:200]}...")


def main():
    data = load_json(JSON_FILE)
    prompts = extract_prompts(data)
    generate_images_with_huggingface(prompts)


if __name__ == "__main__":
    main()
