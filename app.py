import streamlit as st

from creative_director import create_design_plan
from image_generator import generate_hero_image
from poster_composer import create_poster


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Poster Studio",
    page_icon="🎨",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM UI
# --------------------------------------------------

st.markdown(
    """
<style>

/* ================================
   MAIN APP
================================ */

.stApp {
    background:
        radial-gradient(
            circle at 5% 5%,
            rgba(255, 105, 180, 0.18),
            transparent 28%
        ),
        radial-gradient(
            circle at 95% 10%,
            rgba(130, 90, 255, 0.20),
            transparent 30%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(0, 210, 255, 0.08),
            transparent 35%
        ),
        #0b0811;

    color: #ffffff;
}


/* ================================
   REMOVE EXTRA TOP SPACE
================================ */

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1250px;
}


/* ================================
   HERO
================================ */

.hero {
    padding: 45px 0 35px 0;
}

.hero-title {
    font-size: 64px;
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1.05;

    background: linear-gradient(
        90deg,
        #ffffff,
        #f5b8ff,
        #bca7ff
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom: 15px;
}

.hero-subtitle {
    font-size: 20px;
    line-height: 1.6;
    color: #cfc8d8;
    max-width: 760px;
}


/* ================================
   SECTION TITLES
================================ */

.section-title {
    font-size: 25px;
    font-weight: 750;
    color: #ffffff;

    margin-top: 30px;
    margin-bottom: 14px;
}


/* ================================
   LABELS
================================ */

label {
    color: #ded7e8 !important;
    font-weight: 600 !important;
}


/* ================================
   TEXT AREA
================================ */

.stTextArea textarea {
    background: rgba(24, 18, 32, 0.95) !important;

    color: #ffffff !important;

    border: 1px solid #51465d !important;

    border-radius: 16px !important;

    padding: 16px !important;

    font-size: 16px !important;
}


/* TEXT AREA PLACEHOLDER */

.stTextArea textarea::placeholder {
    color: #8f8799 !important;
    opacity: 1 !important;
}


/* ================================
   TEXT INPUT
================================ */

.stTextInput input {
    background: rgba(24, 18, 32, 0.95) !important;

    color: #ffffff !important;

    border: 1px solid #51465d !important;

    border-radius: 13px !important;

    padding: 13px !important;

    font-size: 15px !important;
}


/* INPUT PLACEHOLDER */

.stTextInput input::placeholder {
    color: #8f8799 !important;
    opacity: 1 !important;
}


/* ================================
   INPUT FOCUS
================================ */

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #c084fc !important;

    box-shadow:
        0 0 0 1px #c084fc,
        0 0 18px rgba(192, 132, 252, 0.18) !important;
}


/* ================================
   SELECT BOX
================================ */

div[data-baseweb="select"] > div {
    background: rgba(24, 18, 32, 0.95) !important;

    border: 1px solid #51465d !important;

    border-radius: 13px !important;

    min-height: 48px !important;
}


/* SELECTED TEXT */

div[data-baseweb="select"] span {
    color: #ffffff !important;
}


/* ================================
   BUTTON
================================ */

.stButton > button {
    width: 100%;

    min-height: 54px;

    border-radius: 15px;

    border: 1px solid rgba(255,255,255,0.12);

    background:
        linear-gradient(
            90deg,
            #c026d3,
            #7c3aed,
            #4f46e5
        );

    color: white !important;

    font-size: 17px;

    font-weight: 700;

    box-shadow:
        0 10px 30px rgba(124, 58, 237, 0.25);

    transition: all 0.2s ease;
}


.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 14px 35px rgba(168, 85, 247, 0.35);
}


/* ================================
   DOWNLOAD BUTTON
================================ */

.stDownloadButton > button {
    border-radius: 13px !important;

    background:
        linear-gradient(
            90deg,
            #f472b6,
            #a855f7
        ) !important;

    color: white !important;

    border: none !important;

    font-weight: 700 !important;
}


/* ================================
   STATUS BOX
================================ */

div[data-testid="stStatusWidget"] {
    background: rgba(25, 19, 33, 0.85);
    border: 1px solid #3e3448;
    border-radius: 14px;
}


/* ================================
   EXPANDER
================================ */

div[data-testid="stExpander"] {
    background: rgba(20, 15, 27, 0.75);

    border: 1px solid #3e3448;

    border-radius: 15px;
}


/* ================================
   POSTER IMAGE
================================ */

img {
    border-radius: 18px;
}


/* ================================
   MOBILE
================================ */

@media (max-width: 768px) {

    .hero-title {
        font-size: 42px;
    }

    .hero-subtitle {
        font-size: 16px;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# --------------------------------------------------
# HERO
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-title">
        AI POSTER STUDIO
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# EVENT DESCRIPTION
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Tell us about your event</div>',
    unsafe_allow_html=True
)

idea = st.text_area(
    "Event description",
    placeholder=(
        "Example: Organizing a Dandiya Night for college "
        "students with traditional dance, music, lights "
        "and a festive atmosphere..."
    ),
    height=150,
    label_visibility="collapsed"
)


# --------------------------------------------------
# DESIGN CONTROLS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    design_style = st.selectbox(
        "Design Style",
        [
            "Creative",
            "Dominant",
            "Professional",
            "Minimal"
        ]
    )

with col2:

    color_mood = st.selectbox(
        "Color Mood",
        [
            "Pastel",
            "Dark"
        ]
    )

with col3:

    poster_format = st.selectbox(
        "Poster Format",
        [
            "Portrait 4:5",
            "Instagram Square 1:1",
            "Story 9:16"
        ]
    )


# --------------------------------------------------
# EVENT DETAILS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Event Details</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    title = st.text_input(
        "Event Title",
        placeholder="Dandiya Night"
    )

    date = st.text_input(
        "Date",
        placeholder="18 October"
    )

    venue = st.text_input(
        "Venue",
        placeholder="Malla Reddy Engineering College"
    )

with col2:

    subtitle = st.text_input(
        "Subtitle",
        placeholder="A Night of Dance, Music & Celebration"
    )

    time = st.text_input(
        "Time",
        placeholder="6:00 PM"
    )

    cta = st.text_input(
        "Call to Action",
        placeholder="Join the Celebration"
    )


# --------------------------------------------------
# GENERATE
# --------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

generate = st.button(
    "✨ Generate Professional Poster",
    use_container_width=True
)


# --------------------------------------------------
# GENERATION PIPELINE
# --------------------------------------------------

if generate:

    if not idea.strip():

        st.warning(
            "Please describe your event first."
        )

        st.stop()


    if not title.strip():

        st.warning(
            "Please enter an event title."
        )

        st.stop()


    if not date.strip():
        date = "Date"

    if not time.strip():
        time = "Time"

    if not venue.strip():
        venue = "Venue"

    if not cta.strip():
        cta = "Join Now"

    if not subtitle.strip():
        subtitle = ""


    # ----------------------------------------------
    # CREATIVE DIRECTOR
    # ----------------------------------------------

    with st.status(
        "🎨 AI is developing your creative direction...",
        expanded=True
    ) as status:

        st.write(
            "Understanding the event, audience, "
            "visual story and design style..."
        )

        try:

            plan = create_design_plan(
                idea,
                design_style,
                color_mood,
                poster_format
            )

        except ValueError as e:

            st.error(
                f"Creative direction could not be created: {e}"
            )

            st.stop()

        st.write(
            "Creative direction created."
        )

        status.update(
            label="🎨 Creative direction ready",
            state="complete"
        )


    # ----------------------------------------------
    # IMAGE GENERATION
    # ----------------------------------------------

    with st.status(
        "🖼️ Creating the hero artwork...",
        expanded=True
    ) as status:

        st.write(
            "Generating an event-specific visual..."
        )

        try:
            hero_path = generate_hero_image(
                plan["image_prompt"],
                plan.get("negative_prompt", "")
            )

        except RuntimeError as e:
            st.error(str(e))
            st.stop()

        st.write(
            "Hero artwork generated."
        )

        status.update(
            label="🖼️ Hero artwork ready",
            state="complete"
        )


    # ----------------------------------------------
    # POSTER COMPOSITION
    # ----------------------------------------------

    with st.status(
        "✨ Composing your poster...",
        expanded=True
    ) as status:

        st.write(
            "Applying typography, colors, layout "
            "and decorative elements..."
        )

        poster_path = create_poster(
            image_path=hero_path,
            plan=plan,
            title=title,
            subtitle=subtitle,
            date=date,
            time=time,
            venue=venue,
            cta=cta,
            poster_format=poster_format,
            color_mood=color_mood,
            design_style=design_style
)

        status.update(
            label="✨ Poster complete",
            state="complete"
        )


    # ----------------------------------------------
    # RESULT
    # ----------------------------------------------

    st.markdown(
        '<div class="section-title">Your Poster</div>',
        unsafe_allow_html=True
    )

    st.image(
        poster_path,
        use_container_width=True
    )


    # ----------------------------------------------
    # DOWNLOAD
    # ----------------------------------------------

    with open(
        poster_path,
        "rb"
    ) as file:

        st.download_button(
            label="⬇️ Download Poster",
            data=file,
            file_name="ai_poster.png",
            mime="image/png",
            use_container_width=True
        )


    # ----------------------------------------------
    # CREATIVE PLAN
    # ----------------------------------------------

    with st.expander(
        "View AI Creative Direction"
    ):

        st.json(plan)