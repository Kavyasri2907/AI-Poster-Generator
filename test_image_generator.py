from image_generator import generate_hero_image


prompt = """
A cinematic movie pre-release event,
grand film premiere atmosphere,
dramatic red carpet,
powerful stage with glowing spotlights,
large cinema screens,
elegant crowd,
premium entertainment industry atmosphere,
deep cinematic lighting,
dramatic composition,
high-end professional photography
"""

image_path = generate_hero_image(prompt)

print("\n==============================")
print("IMAGE GENERATION SUCCESSFUL")
print("==============================")
print(image_path)