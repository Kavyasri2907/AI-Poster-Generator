from creative_director import create_design_plan


idea = """
We are organizing a Dandiya Night for college students.
It is a vibrant Navratri celebration with traditional
Gujarati Dandiya and Garba dancing, music, lights,
food and a festive atmosphere.
"""


plan = create_design_plan(
    idea,
    "Creative",
    "Pastel",
    "Portrait 4:5"
)


print("\n==============================")
print("AI CREATIVE PLAN")
print("==============================\n")


for key, value in plan.items():

    print(f"\n{key.upper()}:")
    print(value)