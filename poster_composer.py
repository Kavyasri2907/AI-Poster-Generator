from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import re


# ==================================================
# FONT SETUP
# ==================================================

FONT_REGULAR = "C:/Windows/Fonts/arial.ttf"
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"


def get_font(size, bold=False):
    path = FONT_BOLD if bold else FONT_REGULAR

    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()


# ==================================================
# COLOR UTILITIES
# ==================================================

def extract_hex_colors(palette):
    colors = []

    for item in palette:
        match = re.search(r"#[0-9A-Fa-f]{6}", str(item))

        if match:
            hex_color = match.group()
            colors.append(hex_color)

    return colors


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")

    return tuple(
        int(hex_color[i:i + 2], 16)
        for i in (0, 2, 4)
    )


def contrast_color(rgb):
    brightness = (
        0.299 * rgb[0]
        + 0.587 * rgb[1]
        + 0.114 * rgb[2]
    )

    if brightness > 150:
        return (35, 25, 35)

    return (255, 255, 255)


# ==================================================
# IMAGE CROPPING
# ==================================================

def crop_to_ratio(image, target_ratio):

    width, height = image.size
    current_ratio = width / height

    if current_ratio > target_ratio:

        new_width = int(height * target_ratio)

        left = (width - new_width) // 2

        image = image.crop(
            (
                left,
                0,
                left + new_width,
                height
            )
        )

    else:

        new_height = int(width / target_ratio)

        top = (height - new_height) // 2

        image = image.crop(
            (
                0,
                top,
                width,
                top + new_height
            )
        )

    return image


# ==================================================
# GRADIENT
# ==================================================

def add_gradient(image, dark=True):

    width, height = image.size

    overlay = Image.new(
        "RGBA",
        (width, height),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(overlay)

    for y in range(height):

        progress = y / height

        if dark:
            alpha = int(165 * progress)
        else:
            alpha = int(90 * progress)

        draw.line(
            [(0, y), (width, y)],
            fill=(0, 0, 0, alpha)
        )

    return Image.alpha_composite(
        image.convert("RGBA"),
        overlay
    )


# ==================================================
# TEXT WRAPPING
# ==================================================

def wrap_text(text, font, max_width, draw):

    words = text.split()

    lines = []
    current = ""

    for word in words:

        test = current + " " + word

        bbox = draw.textbbox(
            (0, 0),
            test.strip(),
            font=font
        )

        width = bbox[2] - bbox[0]

        if width <= max_width:

            current = test.strip()

        else:

            if current:
                lines.append(current)

            current = word

    if current:
        lines.append(current)

    return lines


# ==================================================
# TITLE FITTING
# ==================================================

def fit_title(
    title,
    max_width,
    starting_size=105
):

    size = starting_size

    while size >= 45:

        font = get_font(
            size,
            bold=True
        )

        bbox = font.getbbox(
            title.upper()
        )

        width = bbox[2] - bbox[0]

        if width <= max_width:
            return font

        size -= 5

    return get_font(
        45,
        bold=True
    )


# ==================================================
# DECORATIVE GLOW
# ==================================================

def add_glow(
    image,
    position,
    radius,
    color,
    blur=35
):

    glow = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(glow)

    x, y = position

    draw.ellipse(
        (
            x - radius,
            y - radius,
            x + radius,
            y + radius
        ),
        fill=(*color, 80)
    )

    glow = glow.filter(
        ImageFilter.GaussianBlur(blur)
    )

    return Image.alpha_composite(
        image,
        glow
    )


# ==================================================
# DECORATIVE DOTS
# ==================================================

def add_decorative_dots(
    image,
    color,
    positions
):

    draw = ImageDraw.Draw(image)

    for x, y, radius in positions:

        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ),
            fill=(*color, 190)
        )

    return image

    

# ==================================================
# MAIN POSTER COMPOSER
# ==================================================

def create_poster(
    image_path,
    plan,
    title,
    subtitle,
    date,
    time,
    venue,
    cta,
    poster_format="Story 9:16",
    color_mood ="Pastel",
    design_style ="Minimal"
):

    # ------------------------------------------------
    # CANVAS
    # ------------------------------------------------

    if poster_format == "Portrait 4:5":
        W, H = 1080, 1350

    elif poster_format == "Instagram Square 1:1":
        W, H = 1080, 1080

    elif poster_format == "Story 9:16":
        W, H = 1080, 1920

    else:
        W, H = 1080, 1350

    width = W
    height = H

    target_ratio = width / height  


    artwork = Image.open(
        image_path
    ).convert("RGB")

    artwork = crop_to_ratio(
        artwork,
        target_ratio
    )

    artwork = artwork.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    poster = artwork.convert(
        "RGBA"
    )

    # ------------------------------------------------
    # CREATIVE PLAN
    # ------------------------------------------------

    palette = plan.get(
        "color_palette",
        []
    )

    palette_colors = extract_hex_colors(
        palette
    )

    if palette_colors:

        accent_hex = palette_colors[
            min(1, len(palette_colors) - 1)
        ]

        accent = hex_to_rgb(
            accent_hex
        )

    else:

        accent = (230, 80, 120)

    # ------------------------------------------------
    # DETECT MOOD
    # ------------------------------------------------

    mood = str(
        plan.get(
            "mood",
            ""
        )
    ).lower()

    is_dark = color_mood.lower() == "dark"

    style = design_style.lower()

    if style == "minimal":
        title_size = 90
        gradient_strength = True
        panel_alpha = 150

    elif style == "dominant":
        title_size = 125
        gradient_strength = True
        panel_alpha = 190

    elif style == "professional":
        title_size = 92
        gradient_strength = True
        panel_alpha = 175

    else:  # Creative
        title_size = 112
        gradient_strength = True
        panel_alpha = 185

    # ------------------------------------------------
    # IMAGE TREATMENT
    # ------------------------------------------------

    poster = add_gradient(
    poster,
    dark=is_dark
)

    # ------------------------------------------------
    # GLOW
    # ------------------------------------------------

    if is_dark:

        poster = add_glow(
            poster,
            (850, 220),
            170,
            accent,
            55
        )

        poster = add_glow(
            poster,
            (180, 1100),
            130,
            accent,
            50
        )

    # ------------------------------------------------
    # DRAW
    # ------------------------------------------------

    draw = ImageDraw.Draw(
        poster
    )

        # ------------------------------------------------
    # RESPONSIVE LAYOUT
    # ------------------------------------------------

    if poster_format == "Portrait 4:5":
        title_y = 95
        panel_y = 1040
        panel_height = 175
        side_margin = 40
        content_margin = 75

    elif poster_format == "Instagram Square 1:1":
        title_y = 65
        panel_y = 790
        panel_height = 210
        side_margin = 40
        content_margin = 65

    elif poster_format == "Story 9:16":
        title_y = 120
        panel_y = 1580
        panel_height = 220
        side_margin = 40
        content_margin = 70

    else:
        title_y = 95
        panel_y = 1040
        panel_height = 175
        side_margin = 40
        content_margin = 75

    # ------------------------------------------------
    # TITLE
    # ------------------------------------------------

    title_max_width = width - 2 * content_margin

    title_font = fit_title(
        title,
        max_width=title_max_width,
        starting_size=title_size
    )

    title_bbox = draw.textbbox(
        (0, 0),
        title.upper(),
        font=title_font
    )

    title_width = (
        title_bbox[2]
        - title_bbox[0]
    )

    title_x = (
        width - title_width
    ) // 2

    

    # Small accent line

    draw.rounded_rectangle(
        (
            title_x,
            title_y - 20,
            title_x + min(title_width, 180),
            title_y - 8
        ),
        radius=6,
        fill=accent
    )

    # Title

    text_color = (
        (255, 255, 255)
        if is_dark
        else (255, 250, 245)
    )

    draw.text(
        (title_x, title_y),
        title.upper(),
        font=title_font,
        fill=text_color,
        stroke_width=2,
        stroke_fill=(20, 15, 20)
    )

    # ------------------------------------------------
    # SUBTITLE
    # ------------------------------------------------

    subtitle_font = get_font(
        34,
        bold=False
    )

    subtitle_lines = wrap_text(
        subtitle,
        subtitle_font,
        width - 2 * content_margin,
        draw
    )

    subtitle_y = (
        title_y
        + title_bbox[3]
        - title_bbox[1]
        + 35
    )

    for line in subtitle_lines:

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=subtitle_font
        )

        line_width = (
            bbox[2]
            - bbox[0]
        )

        x = (
            width
            - line_width
        ) // 2

        draw.text(
            (x, subtitle_y),
            line,
            font=subtitle_font,
            fill=(255, 255, 255)
        )

        subtitle_y += 45

    # ------------------------------------------------
    # INFORMATION PANEL
    # ------------------------------------------------

    

    panel = Image.new(
        "RGBA",
        (width, panel_height),
        (0, 0, 0, 0)
    )

    panel_draw = ImageDraw.Draw(
        panel
    )

    panel_draw.rounded_rectangle(
        (
    side_margin,
    10,
    width - side_margin,
    panel_height - 10
),
        radius=28,
        fill=(
    (15, 10, 20, panel_alpha)
    if is_dark
    else (255, 255, 255, panel_alpha // 2)
)
    )

    poster.alpha_composite(
        panel,
        (0, panel_y)
    )

    draw = ImageDraw.Draw(
        poster
    )

    # ------------------------------------------------
    # DATE / TIME
    # ------------------------------------------------

    detail_font = get_font(
        32,
        bold=True
    )

    detail_text = (
        f"{date}   •   {time}"
    )

    draw.text(
    (content_margin, panel_y + 40),
        detail_text,
        font=detail_font,
        fill=accent
    )

    # ------------------------------------------------
    # VENUE
    # ------------------------------------------------

    venue_font = get_font(
        28
    )

    venue_lines = wrap_text(
    venue,
    venue_font,
    width - content_margin * 2,
    draw
)

    venue_y = panel_y + 88

    for line in venue_lines:

        draw.text(
            (content_margin, venue_y),
            line,
            font=venue_font,
            fill=(255, 255, 255)
        )

        venue_y += 36

    # ------------------------------------------------
    # CTA
    # ------------------------------------------------

    cta_font = get_font(
        27,
        bold=True
    )

    cta_bbox = draw.textbbox(
        (0, 0),
        cta.upper(),
        font=cta_font
    )

    cta_width = (
        cta_bbox[2]
        - cta_bbox[0]
    )

    cta_padding = 38

    button_width = (
        cta_width
        + cta_padding * 2
    )

    button_x = (
        width
        - button_width
        - 65
    )

    button_y = (
        panel_y
        + 48
    )

    button_height = 70

    draw.rounded_rectangle(
        (
            button_x,
            button_y,
            button_x + button_width,
            button_y + button_height
        ),
        radius=35,
        fill=accent
    )

    draw.text(
        (
            button_x + cta_padding,
            button_y + 19
        ),
        cta.upper(),
        font=cta_font,
        fill=(255, 255, 255)
    )

    
    # ------------------------------------------------
    # DECORATIVE ACCENTS
    # ------------------------------------------------

    

    decorative = plan.get(
        "decorative_elements",
        []
    )

    # Minimal style keeps decoration extremely restrained.
    if style == "minimal":
        decorative = []

    decorative_text = " ".join(
        str(x).lower()
        for x in decorative
    )

    # Festival / cultural accents

    if (
    style != "minimal"
    and (
        "rangoli" in decorative_text
        or "gujarati" in decorative_text
        or "diya" in decorative_text
        or "festival" in decorative_text
    )
):

        positions = [
            (65, 65, 7),
            (1015, 65, 7),
            (65, 970, 6),
            (1015, 970, 6)
        ]

        poster = add_decorative_dots(
            poster,
            accent,
            positions
        )

        draw = ImageDraw.Draw(
            poster
        )

        # Small ornamental diamonds

        for x, y in [
            (55, 900),
            (1025, 900),
            (55, 310),
            (1025, 310)
        ]:

            draw.polygon(
                [
                    (x, y - 9),
                    (x + 9, y),
                    (x, y + 9),
                    (x - 9, y)
                ],
                fill=accent
            )

    # ------------------------------------------------
    # CREATIVE / ASYMMETRIC ACCENTS
    # ------------------------------------------------

    composition = str(
        plan.get(
            "composition",
            ""
        )
    ).lower()

    if (
    style == "creative"
    and (
        "asymmetric" in composition
        or "dynamic" in composition
        or "creative" in composition
    )
):

        draw = ImageDraw.Draw(
            poster
        )

        draw.arc(
            (
                -180,
                850,
                260,
                1290
            ),
            200,
            350,
            fill=accent,
            width=5
        )

        draw.arc(
            (
                850,
                -120,
                1200,
                300
            ),
            20,
            170,
            fill=accent,
            width=5
        )

    # ------------------------------------------------
    # SAVE
    # ------------------------------------------------

    os.makedirs(
        "generated",
        exist_ok=True
    )

    output_path = os.path.join(
    "generated",
    "final_poster.png"
)

    poster.convert(
        "RGB"
    ).save(
        output_path,
        quality=95
    )

    return output_path