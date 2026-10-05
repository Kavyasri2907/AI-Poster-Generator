from creative_director import create_design_plan
from image_generator import generate_hero_image
from poster_composer import create_poster


idea = """
We are organizing a Dandiya Night for college students.
It is a vibrant Navratri celebration with traditional
Gujarati Dandiya and Garba dancing, music, lights,
food and a festive atmosphere.
"""


# --------------------------------------------
# 1. AI CREATIVE DIRECTOR
# --------------------------------------------

plan = create_design_plan(
    idea,
    "Creative",
    "Pastel",
    "Portrait 4:5"
)


print("\nCREATIVE PLAN CREATED")


# --------------------------------------------
# 2. GENERATE HERO ARTWORK
# --------------------------------------------

hero_path = generate_hero_image(
    plan["image_prompt"],
    plan.get("negative_prompt", "")
)


print("HERO ARTWORK CREATED")


# --------------------------------------------
# 3. COMPOSE FINAL POSTER
# --------------------------------------------

poster_path = create_poster(
    image_path=hero_path,
    plan=plan,
    title="Dandiya Night",
    subtitle="A Night of Dance, Music & Celebration",
    date="18 OCTOBER",
    time="6:00 PM",
    venue="Malla Reddy Engineering College",
    cta="Join the Celebration",
    poster_format="Portrait 4:5",
    color_mood="Pastel",
    design_style="Creative"
)


print("\n==============================")
print("FINAL POSTER CREATED!")
print("==============================")

print(f"Saved at: {poster_path}")