from creative_director import create_design_plan
from image_generator import generate_hero_image


idea = """
Organizing a Dandiya Night for college students.
A vibrant cultural celebration with traditional
dance, music, food and festive decorations.
The event should feel energetic, colorful,
traditional and exciting.
"""


plan = create_design_plan(
    idea,
    "Creative",
    "Pastel",
    "Portrait 4:5"
)


print("\n==============================")
print("CREATIVE PLAN")
print("==============================\n")

for key, value in plan.items():
    print(f"{key}: {value}")


print("\n==============================")
print("GENERATING HERO ARTWORK...")
print("==============================\n")


path = generate_hero_image(
    plan["image_prompt"],
    plan.get("negative_prompt", "")
)


print("\n==============================")
print("SUCCESS!")
print("==============================")
print(f"Generated image: {path}")