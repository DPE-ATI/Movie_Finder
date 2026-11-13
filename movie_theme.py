#%% Theme der Film-Vorhersage-App
"""Farben und Schriften für APP.py — je Lieblingsgenre ein eigenes Thema.

Nutzung in APP.py:
    from movie_theme import GENRES, GENRE_ORDER, build_css
    st.markdown(build_css(GENRES[genre]), unsafe_allow_html=True)
"""

# Alle Schriftfamilien in einem Request; umgeschaltet wird danach über CSS-Variablen.
FONT_IMPORT = (
    "https://fonts.googleapis.com/css2"
    "?family=Bebas+Neue"
    "&family=Cinzel:wght@500;700"
    "&family=Inter:wght@300;400;600"
    "&family=Playfair+Display:ital,wght@0,600;0,800;1,600"
    "&family=Poppins:wght@300;400;600;700"
    "&family=Space+Grotesk:wght@400;500;700"
    "&display=swap"
)

GENRES = {
    "Neutral": dict(
        emoji="🎬", font_head="'Inter'", font_body="'Inter'", radius="16px",
        bg="#0b0d12", bg2="#141821", surface="#171c26", border="rgba(255,255,255,.10)",
        text="#f2f4f8", muted="#98a2b3", accent="#e50914", accent_soft="#ff5a63",
        glow="229,9,20",
    ),
    "Krimi / Noir": dict(
        emoji="🕵️", font_head="'Playfair Display'", font_body="'Inter'", radius="8px",
        bg="#0a0a0b", bg2="#141415", surface="#161617", border="rgba(255,255,255,.09)",
        text="#e8e6e1", muted="#8d8a84", accent="#d4af37", accent_soft="#f0d67a",
        glow="212,175,55",
    ),
    "Science-Fiction": dict(
        emoji="🚀", font_head="'Space Grotesk'", font_body="'Inter'", radius="6px",
        bg="#04070f", bg2="#0a1526", surface="#0d1b2e", border="rgba(90,200,255,.22)",
        text="#e6f6ff", muted="#7fa6c4", accent="#00e0ff", accent_soft="#7cf0ff",
        glow="0,224,255",
    ),
    "Animation / Familie": dict(
        emoji="🧸", font_head="'Poppins'", font_body="'Poppins'", radius="26px",
        bg="#fff7ef", bg2="#ffe9d6", surface="#ffffff", border="rgba(0,0,0,.10)",
        text="#2b2118", muted="#8a7563", accent="#ff5a3c", accent_soft="#ffb02e",
        glow="255,90,60", dark=False,
    ),
    "Action": dict(
        emoji="💥", font_head="'Bebas Neue'", font_body="'Inter'", radius="10px",
        bg="#0a0505", bg2="#1d0b06", surface="#1a0e09", border="rgba(255,120,40,.25)",
        text="#fff2ea", muted="#b99a86", accent="#ff7a18", accent_soft="#ffc93c",
        glow="255,122,24",
    ),
    "Fantasy / Epos": dict(
        emoji="🐉", font_head="'Cinzel'", font_body="'Playfair Display'", radius="12px",
        bg="#0b0a14", bg2="#181231", surface="#161129", border="rgba(180,150,255,.24)",
        text="#f0eaff", muted="#a495c9", accent="#a77bff", accent_soft="#d9c2ff",
        glow="167,123,255",
    ),
}

# Reihenfolge für die Sidebar (Neutral zuerst = Default)
GENRE_ORDER = ["Neutral", "Krimi / Noir", "Science-Fiction", "Animation / Familie", "Action", "Fantasy / Epos"]
