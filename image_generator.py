from gradio_client import Client
from PIL import Image
from dotenv import load_dotenv
import os


load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")


def generate_hero_image(image_prompt, negative_prompt=""):

    print("\nConnecting to FLUX image generator...")

    client = Client(
    "black-forest-labs/FLUX.1-dev",
    token=HF_TOKEN
)

    print("Connected to FLUX.")

    final_prompt = f"""
{image_prompt}

Create a high-quality professional poster hero artwork.

The artwork must have strong visual storytelling,
a clear focal subject, realistic human anatomy,
rich depth, cinematic lighting and professional
event-poster composition.

The visual subject must be culturally and visually
specific to the event.

Do NOT generate generic imagery.

Do NOT include:
text,
letters,
words,
logos,
watermarks,
dates,
UI elements,
posters,
signboards.

Negative visual instructions:
{negative_prompt}
"""

    print("\nGenerating artwork...")
    print("This may take some time...\n")

    try:
        result = client.predict(
            prompt=final_prompt,
            seed=42,
            randomize_seed=True,
            width=768,
            height=1024,
            guidance_scale=3.5,
            num_inference_steps=20,
            api_name="/infer"
        )

    except Exception as e:
        error_message = str(e)

        if "ZeroGPU" in error_message or "quota" in error_message.lower():
            raise RuntimeError(
                "Image generation is temporarily unavailable because "
                "the Hugging Face ZeroGPU quota has been reached. "
                "Please try again later."
            )

        raise

    print("Artwork generated!")

    # First item contains the generated image path
    generated_image_path = result[0]

    print(
        "Temporary image:",
        generated_image_path
    )

    # Create generated folder
    os.makedirs(
        "generated",
        exist_ok=True
    )

    output_path = (
        "generated/hero_artwork.png"
    )

    # Open generated image
    image = Image.open(
        generated_image_path
    )

    # Convert to PNG
    image.save(
        output_path,
        format="PNG"
    )

    print(
        "Hero artwork saved:",
        output_path
    )

    return output_path

