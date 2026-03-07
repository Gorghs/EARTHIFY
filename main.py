import json
import mimetypes
import os
import tempfile

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, Response
from google import genai
from google.genai import types

load_dotenv()

HF_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"  # Free model for basic image gen
app = FastAPI()


@app.get("/get-msg")
async def read_root():
    return {"Message": "Congrats this is hte first step:"}


def generate(image_path: str) -> str:
    """
    Generates DIY project JSON based on a provided image.
    """

    # --- 1. Set up the API Client ---
    api_key = os.getenv("GOOGLE_API_KEY")  # safer than hardcoding

    client = genai.Client(api_key=api_key)
    model_name = "models/gemini-2.5-flash"  # latest stable version

    # --- 2. Prepare the Image Part ---
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        raise ValueError(f"Could not determine mime type for {image_path}")

    print(f"Loading image: {image_path} (MIME type: {mime_type})")
    with open(image_path, "rb") as f:
        image_data = f.read()

    image_part = types.Part.from_bytes(data=image_data, mime_type=mime_type)

    # --- 3. Prepare the Text Instruction Part ---
    text_part = types.Part.from_text(
        text="""
### Instruction

Based on the provided image of an item, please generate the following DIY project information for three different difficulty levels: Easy, Medium, and Hard.

For each difficulty level, include the following details:

1. **DIY Product Description**: Describe the product that can be made using the item in the image. Explain its purpose and potential uses. Incorporate details from the image such as color, texture, and shape to create a vivid description.

2. **Materials Required**: List all materials needed to create the product, specifying the quantity and type. Be specific about the materials shown in the image and any additional items that may be necessary.

3. **Steps**: Provide a detailed step-by-step guide on how to create the product. Ensure each step is clear and actionable, including:
   - **Preparation**: Any preparation needed before starting (e.g., gathering materials, workspace setup).
   - **Instructions**: Detailed instructions for each step, including how to cut, assemble, or apply materials. Reference any specific techniques or tools that relate to the item in the image.
   - **Safety Tips**: Any safety precautions to keep in mind while working on the project, especially those relevant to the materials and methods shown.
   - **Estimated Time**: Provide an estimate of how long each step might take.

4. **Difficulty Level**: Indicate the difficulty level (Easy, Medium, Hard) and explain why it fits that category, considering factors such as required skills, time commitment, and complexity.

5. **Image Generation Prompt**: Provide a detailed text prompt that can be used to generate an image of the finished product for each difficulty level. This description should include visual details such as shape, color, size, materials used, decorative features, and how it relates to the item in the original image.

The output should be structured in JSON format as follows:

"{
    "Projects": {
        "Easy": {
            "DIY_Product": "Description of the easy product.",
            "Materials_Required": [
                {
                    "Material": "Material 1",
                    "Quantity": "1 unit or specific amount"
                },
                {
                    "Material": "Material 2",
                    "Quantity": "2 units or specific amount"
                }
            ],
            "Steps": [
                {
                    "Step_Number": 1,
                    "Description": "Detailed instructions for the first step.",
                    "Estimated_Time": "5 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 2,
                    "Description": "Detailed instructions for the second step.",
                    "Estimated_Time": "10 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 3,
                    "Description": "Detailed instructions for the third step.",
                    "Estimated_Time": "5 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                }
                // Add more steps as needed
            ],
            "Difficulty_Level": {
                "Level": "Easy",
                "Explanation": "Explain why the project is categorized as easy."
            },
            "Image_Generation_Prompt": "Provide a detailed description of the easy product, its colors, shape, and materials used."
        },
        "Medium": {
            "DIY_Product": "Description of the medium product.",
            "Materials_Required": [
                {
                    "Material": "Material 1",
                    "Quantity": "1 unit or specific amount"
                },
                {
                    "Material": "Material 2",
                    "Quantity": "2 units or specific amount"
                }
            ],
            "Steps": [
                {
                    "Step_Number": 1,
                    "Description": "Detailed instructions for the first step.",
                    "Estimated_Time": "10 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 2,
                    "Description": "Detailed instructions for the second step.",
                    "Estimated_Time": "15 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 3,
                    "Description": "Detailed instructions for the third step.",
                    "Estimated_Time": "10 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 4,
                    "Description": "Detailed instructions for the fourth step.",
                    "Estimated_Time": "10 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 5,
                    "Description": "Detailed instructions for the fifth step.",
                    "Estimated_Time": "10 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                }
                // Add more steps as needed
            ],
            "Difficulty_Level": {
                "Level": "Medium",
                "Explanation": "Explain why the project is categorized as medium."
            },
            "Image_Generation_Prompt": "Provide a detailed description of the medium product, its colors, shape, and materials used."
        },
        "Hard": {
            "DIY_Product": "Description of the hard product.",
            "Materials_Required": [
                {
                    "Material": "Material 1",
                    "Quantity": "1 unit or specific amount"
                },
                {
                    "Material": "Material 2",
                    "Quantity": "2 units or specific amount"
                }
            ],
            "Steps": [
                {
                    "Step_Number": 1,
                    "Description": "Detailed instructions for the first step.",
                    "Estimated_Time": "20 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 2,
                    "Description": "Detailed instructions for the second step.",
                    "Estimated_Time": "30 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 3,
                    "Description": "Detailed instructions for the third step.",
                    "Estimated_Time": "15 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 4,
                    "Description": "Detailed instructions for the fourth step.",
                    "Estimated_Time": "25 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 5,
                    "Description": "Detailed instructions for the fifth step.",
                    "Estimated_Time": "20 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                },
                {
                    "Step_Number": 6,
                    "Description": "Detailed instructions for the sixth step.",
                    "Estimated_Time": "15 minutes",
                    "Safety_Tips": "Include any relevant safety tips."
                }
                // Add more steps as needed
            ],
            "Difficulty_Level": {
                "Level": "Hard",
                "Explanation": "Explain why the project is categorized as hard."
            },
            "Image_Generation_Prompt": "Provide a detailed description of the hard product, its colors, shape, and materials used."
        }
    }
}"
"""
    )

    # --- 4. Combine Parts ---
    contents = [
        types.Content(
            role="user",
            parts=[text_part, image_part],
        ),
    ]

    print("Sending request to Gemini...")

    # --- 5. Generate Response ---
    response = client.models.generate_content(
        model=model_name,
        contents=contents,
    )

    # --- 6. Extract and Clean JSON ---
    try:
        cleaned_json = response.text.strip().lstrip("```json").rstrip("```").strip()
        print("Successfully received and cleaned JSON response.")
        return cleaned_json
    except Exception as e:
        print(f"Error extracting text from response: {e}")
        print(f"Full response object: {response}")
        return '{"Projects": {}}'


def generate_ecotips(image_path: str, user_ailments: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")

    client = genai.Client(api_key=api_key)
    model_name = "models/gemini-2.5-flash"  # latest stable version

    # --- 2. Prepare the Image Part ---
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        raise ValueError(f"Could not determine mime type for {image_path}")

    print(f"Loading image: {image_path} (MIME type: {mime_type})")
    with open(image_path, "rb") as f:
        image_data = f.read()

    image_part = types.Part.from_bytes(data=image_data, mime_type=mime_type)

    # --- 3. Prepare the Text Instruction Part ---
    text_part = types.Part.from_text(
        text=f"""
You are an expert AI assistant specializing in product analysis for health and environmental impact. Your task is to analyze the provided product image and return a detailed JSON object.

A specific user has the following health considerations: "{user_ailments}". You *must* use this information when generating the health analysis.

Extract all information directly from the text and visuals in the image (labels, packaging, etc.). 
- If a piece of information (e.g., 'manufacturing_location', 'ingredients') is not visible on the image, you *must* use `null` for that field.
- If a list field (e.g., 'ingredients') is not visible or applicable, return an empty list `[]`.
- Do not invent or infer information that is not present.

Respond *only* with a valid JSON object matching the schema below. Do not include any explanatory text before or after the JSON block.

{{
  "product_info": {{
    "product_name": "...",
    "product_description": "...",
    "product_appearance": "A brief visual description of the product itself, if visible.",
    "manufacturing_location": "...",
    "packaging_details": "Description of the packaging material (e.g., 'Plastic bottle', 'Cardboard box')."
  }},
  "extraction_data": {{
    "ingredients": ["...", "..."],
    "nutritional_information": ["e.g., 'Calories: 150', 'Total Fat: 8g', 'Sodium: 200mg'"],
    "allergen_information": ["...", "..."],
    "cautions_and_warnings": ["...", "..."]
  }},
  "health_analysis": {{
    "positive_points": ["General health benefits, e.g., 'High in fiber'"],
    "negative_points": ["General health concerns AND specific concerns related to the user ailments: '{user_ailments}'"]
  }},
  "environmental_analysis": {{
    "positive_points": ["e.g., 'Recyclable packaging', 'Organic ingredients'"],
    "negative_points": ["e.g., 'Single-use plastic', 'High food miles']
  }},
  "alternatives_to_consider": ["List of healthier or more eco-friendly alternative products or product types."]
}}
"""
    )

    # --- 4. Combine Parts ---
    contents = [
        types.Content(
            role="user",
            parts=[text_part, image_part],
        ),
    ]

    print("Sending request to Gemini...")

    # --- 5. Generate Response ---
    response = client.models.generate_content(
        model=model_name,
        contents=contents,
    )

    # --- 6. Extract and Clean JSON ---
    try:
        cleaned_json = response.text.strip().lstrip("```json").rstrip("```").strip()
        print("Successfully received and cleaned JSON response.")
        return cleaned_json
    except Exception as e:
        print(f"Error extracting text from response: {e}")
        print(f"Full response object: {response}")
        return '{"Projects": {}}'


def generate_images_with_huggingface(prompt: str):
    """Generate images using Hugging Face Stable Diffusion API."""
    api_key = os.getenv("HF_TOKEN")
    if not api_key:
        raise SystemExit("❌ Missing HF_TOKEN environment variable.")

    headers = {"Authorization": f"Bearer {api_key}"}

    print("\n✨ Generating image for")
    print(f"🧠 Prompt: {prompt[:120]}...")

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers,
        json={"inputs": prompt},
    )

    if response.status_code == 200:
        return response.content
    elif response.status_code == 503:
        print("⏳ Model is loading on Hugging Face — please wait and retry.")
    else:
        print(f"❌ Error ({response.status_code}): {response.text[:200]}...")


@app.post("/diy")
async def diy(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(file.filename)[1]
        ) as temp_file:
            temp_path = temp_file.name
            temp_file.write(await file.read())

        try:
            # Step 2: Call your generate() function with the temp file path
            data = json.loads(generate(temp_path))
        finally:
            # Step 4: Clean up
            os.remove(temp_path)

        # Return a JSON response
        return JSONResponse(data)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/scan")
async def scan(file: UploadFile = File(...), user_ailments: str = "none"):
    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(file.filename)[1]
        ) as temp_file:
            temp_path = temp_file.name
            temp_file.write(await file.read())

        try:
            # Step 2: Call your generate() function with the temp file path
            data = json.loads(generate_ecotips(temp_path, user_ailments))
        finally:
            # Step 4: Clean up
            os.remove(temp_path)

        # Return a JSON response
        return JSONResponse(data)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/generate-image")
async def generate_image(prompt: str):
    image_bytes = generate_images_with_huggingface(prompt)
    return Response(content=image_bytes, media_type="image/png")
