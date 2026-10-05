from poster_composer import create_poster

plan = {
    "mood": "Vibrant festive",
    "color_palette": [
        "Warm Cream #FFF4E6",
        "Coral Pink #E76F51",
        "Maroon #8B1E3F",
        "Golden Yellow #F4C95D"
    ],
    "decorative_elements": [
        "Rangoli",
        "Gujarati motifs",
        "Festival lights",
        "Diyas"
    ],
    "composition": "Creative asymmetric dynamic composition"
}

poster_path = create_poster(
    image_path="generated/hero_artwork.png",
    plan=plan,
    title="Dandiya Night",
    subtitle="A Night of Dance, Music & Celebration",
    date="18 OCTOBER",
    time="6:00 PM",
    venue="Malla Reddy Engineering College",
    cta="Join the Celebration",
    poster_format="Story 9:16",
    color_mood="Pastel",
    design_style="Dominant"
)

print("Poster created:", poster_path)