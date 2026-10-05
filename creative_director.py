from ollama import chat
import json
import re


def extract_json(text):
    text = text.strip()

    # Remove markdown code fences if Llama adds them
    text = re.sub(
        r"```(?:json)?",
        "",
        text,
        flags=re.IGNORECASE
    ).replace("```", "").strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            "No JSON object found in AI response."
        )

    json_text = text[start:end + 1]

    try:
        return json.loads(json_text)

    except json.JSONDecodeError as e:

        # Show useful debugging information
        print("\n==============================")
        print("INVALID JSON FROM AI")
        print("==============================")
        print(json_text)
        print("==============================")
        print("JSON ERROR:", e)
        print("==============================\n")

        raise ValueError(
            "AI returned malformed JSON. "
            "Please try generating again."
        ) from e


def create_design_plan(
    idea,
    design_style,
    color_mood,
    poster_format
):

    system_prompt = """
You are an expert creative director, graphic designer,
art director and visual communication strategist.

Your job is to transform an event or promotional idea
into a complete professional poster design specification.

You must understand WHAT the event is before deciding
how it should look.

The design must feel specific to the event.
Never create a generic poster concept.

IMPORTANT CULTURAL GUIDANCE:

For Dandiya / Garba / Navratri:
- authentic Gujarati cultural celebration
- women in chaniya choli / ghagra choli
- mirror-work embroidery
- traditional Gujarati jewelry
- men in Gujarati kediyu
- churidar or dhoti-style pants for men
- decorated dandiya sticks
- active Garba/Dandiya dancing
- circular dance formations
- Navratri decorations
- rangoli
- diyas
- Gujarati decorative patterns
- festive Indian lighting

Men must NEVER wear lehenga, ghagra,
chaniya choli, skirts, gowns or women's dresses.

For AI / Hackathon / Technology:
- artificial intelligence
- futuristic technology
- digital interfaces
- neural networks
- circuitry
- glowing data
- innovation
- cyber/digital atmosphere

For business / product events:
- premium visual language
- elegant composition
- sophisticated lighting
- controlled decoration
- product-focused imagery
- professional corporate aesthetic

DESIGN STYLE MEANINGS:

Minimal:
- intentional whitespace
- clean hierarchy
- restrained decoration
- one strong visual
- elegant typography

Dominant:
- hero artwork is visually powerful
- oversized typography
- dramatic composition
- strong contrast

Professional:
- precise alignment
- grid-based structure
- restrained visual treatment
- premium typography
- polished corporate appearance

Creative:
- expressive typography
- asymmetric composition
- layered visual elements
- artistic decoration
- dynamic composition

COLOR MOOD:

Pastel does NOT mean washed-out white.

Pastel can use:
- coral
- rose
- peach
- lavender
- warm cream
- soft pink
- muted gold

Dark can use:
- deep navy
- charcoal
- black
- violet
- electric blue
- cyan
- magenta

VERY IMPORTANT:

Every field must contain a useful, specific answer.

NEVER leave any field empty.

Do not use:
""
null
"not specified"
"none"

For every design decision, make a concrete choice.

The typography and layout fields are especially important.

TITLE_STYLE must describe the visual character of the
main event title, such as:
"large expressive festive typography with bold rounded
letterforms and decorative gold accents"

TITLE_POSITION must specify where the title should be placed,
such as:
"upper third, centered with clear breathing room"

SUBTITLE_STYLE must describe the subtitle treatment.

DETAILS_POSITION must specify where date, time and venue
should appear.

ACCENT_STYLE must describe how decorative visual accents
should be used.

Think like a professional graphic designer making an
actual finished poster, not merely describing an idea.

Return ONLY valid JSON.

Use EXACTLY these keys:

{
    "event_type": "",
    "theme": "",
    "mood": "",
    "visual_subject": "",
    "secondary_visuals": [],
    "background_concept": "",

    "color_palette": [],

    "composition": "",
    "visual_emphasis": "",

    "title_style": "",
    "title_position": "",

    "subtitle_style": "",
    "details_position": "",

    "decorative_elements": [],

    "accent_style": "",

    "image_prompt": "",
    "negative_prompt": ""
}
"""

    user_prompt = f"""
USER EVENT IDEA:

{idea}

DESIGN STYLE:

{design_style}

COLOR MOOD:

{color_mood}

POSTER FORMAT:

{poster_format}


Create a complete professional creative direction.

Think like a real art director.

First understand:
- What is the event?
- Who is it for?
- What emotion should it create?
- What visual would immediately communicate the event?
- What cultural or subject-specific elements are important?
- Where should the viewer's eye go first?
- How should the typography interact with the artwork?

The final design should NOT look like a generic
template.

The image_prompt must describe ONLY the visual artwork.

Do NOT put:
- event title
- dates
- venue
- logos
- typography
- readable text

inside the generated artwork.

The artwork must be visually specific to the event.

The negative_prompt must explicitly describe
visual mistakes that the image generator should avoid.

Return ONLY JSON.
"""

    response = chat(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            format="json",
            options={
                "temperature": 0.2
            }
        )

    plan = extract_json(
            response["message"]["content"]
        )

    return plan


    # --------------------------------------------------
    # FALLBACK DESIGN VALUES
    # --------------------------------------------------

    if not plan.get("title_style"):
        plan["title_style"] = (
            "Large expressive typography with strong "
            "visual presence and excellent readability"
        )


    if not plan.get("title_position"):
        plan["title_position"] = (
            "Upper third of the poster with clear "
            "breathing room around the title"
        )


    if not plan.get("subtitle_style"):
        plan["subtitle_style"] = (
            "Smaller clean typography that supports "
            "the main title without competing with it"
        )


    if not plan.get("details_position"):
        plan["details_position"] = (
            "Lower section of the poster in a clean "
            "and easily readable information group"
        )


    if not plan.get("accent_style"):
        plan["accent_style"] = (
            "Subtle decorative accents inspired by "
            "the event theme and color palette"
        )


    return plan