#%% CSS der Film-Vorhersage-App
"""Baut aus einer Genre-Palette (movie_theme.GENRES) das komplette Stylesheet."""

from movie_theme import FONT_IMPORT


def build_css(p: dict) -> str:
    """Farben und Schrift eines Themas -> fertiger <style>-Block."""
    if p.get("dark", True):
        shadow = "0 24px 60px rgba(0,0,0,.55)"
        ghost = "rgba(255,255,255,.05)"
        header_bg = "rgba(10,11,14,.72)"
        btn_text = "#0b0d12"
    else:
        shadow = "0 20px 50px rgba(120,80,40,.18)"
        ghost = "rgba(0,0,0,.04)"
        header_bg = "rgba(255,247,239,.82)"
        btn_text = "#ffffff"

    return f"""
<style>
@import url('{FONT_IMPORT}');

:root {{
  --surface: {p['surface']};
  --border: {p['border']};
  --text: {p['text']};
  --muted: {p['muted']};
  --accent: {p['accent']};
  --accent-soft: {p['accent_soft']};
  --glow: {p['glow']};
  --radius: {p['radius']};
  --font-head: {p['font_head']}, sans-serif;
  --font-body: {p['font_body']}, sans-serif;
}}

/* ---------- Grundfläche ---------- */
.stApp {{
  color: var(--text);
  font-family: var(--font-body);
  background:
    radial-gradient(1100px 620px at 78% -12%, rgba(var(--glow), .20), transparent 62%),
    radial-gradient(880px 520px at -8% 8%, rgba(var(--glow), .10), transparent 60%),
    linear-gradient(170deg, {p['bg']} 0%, {p['bg2']} 55%, {p['bg']} 100%);
  background-attachment: fixed;
}}
header[data-testid="stHeader"] {{ background: {header_bg}; backdrop-filter: blur(14px); }}
#MainMenu, footer {{ visibility: hidden; }}
.block-container {{ padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1160px; }}

h1, h2, h3, h4 {{ font-family: var(--font-head); color: var(--text); letter-spacing: .4px; }}
p, span, label, li, div {{ font-family: var(--font-body); }}
a {{ color: var(--accent-soft); }}

/* ---------- Hero ---------- */
.hero {{
  position: relative;
  border-radius: calc(var(--radius) + 6px);
  border: 1px solid var(--border);
  background:
    linear-gradient(120deg, rgba(var(--glow), .18), transparent 55%),
    linear-gradient(0deg, var(--surface), var(--surface));
  box-shadow: {shadow};
  padding: 2.4rem 2.2rem 2rem;
  margin-bottom: 1.6rem;
  overflow: hidden;
}}
.hero::before {{  /* Lichtstrahl wie auf dem Kinoplakat */
  content: "";
  position: absolute; inset: -40% -10% auto -10%; height: 200%;
  background: linear-gradient(100deg, transparent 40%, rgba(var(--glow), .16) 50%, transparent 60%);
  transform: rotate(-6deg);
  pointer-events: none;
}}
.hero-kicker {{
  text-transform: uppercase; letter-spacing: .34em; font-size: .70rem;
  color: var(--accent-soft); margin-bottom: .9rem;
}}
.hero h1 {{
  font-size: clamp(2.1rem, 5.4vw, 3.9rem);
  line-height: 1.02; margin: 0 0 .5rem;
  text-shadow: 0 0 42px rgba(var(--glow), .38);
}}
.hero h1 em {{ color: var(--accent); font-style: normal; }}
.hero p {{ color: var(--muted); max-width: 46rem; margin: 0; font-size: 1rem; }}

/* ---------- Filmkarten ---------- */
.movie-card {{
  display: flex; gap: 1.5rem; align-items: flex-start;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: linear-gradient(150deg, var(--surface) 0%, {p['bg2']} 130%);
  box-shadow: {shadow};
  padding: 1.5rem 1.6rem;
  margin-bottom: 1.05rem;
  transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease;
  animation: rise .5s ease both;
}}
.movie-card:hover {{
  transform: translateY(-4px);
  border-color: rgba(var(--glow), .55);
  box-shadow: 0 30px 70px rgba(var(--glow), .22), {shadow};
}}
@keyframes rise {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: none; }} }}

.rank {{
  flex: 0 0 auto; min-width: 3.4rem;
  font-family: var(--font-head); font-size: 2.6rem; line-height: 1;
  color: transparent; -webkit-text-stroke: 1.5px rgba(var(--glow), .75);
}}
.movie-body {{ flex: 1 1 auto; min-width: 0; }}
.movie-title {{ font-family: var(--font-head); font-size: 1.45rem; line-height: 1.15; margin: 0 0 .35rem; }}
.movie-title .year {{ color: var(--muted); font-size: .95rem; font-weight: 400; }}
.crew {{ color: var(--muted); font-size: .93rem; margin: .18rem 0; }}
.crew b {{ color: var(--text); font-weight: 600; }}

.chips {{ margin-top: .7rem; display: flex; flex-wrap: wrap; gap: .38rem; }}
.chip {{
  font-size: .78rem; padding: .22rem .62rem; border-radius: 999px;
  border: 1px solid var(--border); background: rgba(var(--glow), .10); color: var(--text);
}}
.badge {{
  display: inline-block; font-size: .72rem; letter-spacing: .12em; text-transform: uppercase;
  color: {btn_text}; background: var(--accent);
  padding: .18rem .6rem; border-radius: 999px; font-weight: 700;
}}

/* ---------- Formularelemente ---------- */
.stTextArea textarea, .stTextInput input {{
  background: var(--surface) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  font-family: var(--font-body) !important;
}}
.stTextArea textarea:focus, .stTextInput input:focus {{
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(var(--glow), .22) !important;
}}
.stTextArea label, .stTextInput label, .stSlider label, .stRadio label {{
  color: var(--muted) !important; font-size: .88rem !important;
}}
.stButton > button, .stFormSubmitButton > button {{
  background: linear-gradient(120deg, var(--accent) 0%, var(--accent-soft) 100%);
  color: {btn_text}; border: none; border-radius: 999px;
  font-family: var(--font-body); font-weight: 700; letter-spacing: .06em;
  padding: .62rem 1.6rem;
  box-shadow: 0 10px 30px rgba(var(--glow), .32);
  transition: transform .18s ease, box-shadow .18s ease;
}}
.stButton > button:hover, .stFormSubmitButton > button:hover {{
  transform: translateY(-2px);
  box-shadow: 0 16px 40px rgba(var(--glow), .45);
}}

/* Slider / Expander / Alerts / Sidebar */
[data-baseweb="slider"] div[role="slider"] {{ background: var(--accent) !important; }}
[data-testid="stExpander"] {{
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  background: {ghost} !important;
}}
[data-testid="stExpander"] summary {{ color: var(--muted) !important; }}
[data-testid="stAlert"] {{ border-radius: var(--radius) !important; }}
[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, {p['bg2']} 0%, {p['bg']} 100%);
  border-right: 1px solid var(--border);
}}
[data-testid="stSidebar"] h3 {{ color: var(--accent-soft); }}

/* ---------- Footer ---------- */
.footer {{
  margin-top: 2.6rem; padding-top: 1.1rem;
  border-top: 1px solid var(--border);
  color: var(--muted); font-size: .82rem; text-align: center;
}}
</style>
"""


def movie_card(index: int, titel: str, jahr, regie: str, actors: list) -> str:
    """HTML einer Filmkarte im Kinostil."""
    chips = "".join(f"<span class='chip'>{a}</span>" for a in actors)
    chips_html = f"<div class='chips'>{chips}</div>" if chips else ""
    return f"""
    <div class="movie-card" style="animation-delay:{index * 0.06:.2f}s">
      <div class="rank">{index:02d}</div>
      <div class="movie-body">
        <div class="movie-title">{titel} <span class="year">({jahr})</span></div>
        <div class="crew"><b>Regie:</b> {regie}</div>
        {chips_html}
      </div>
    </div>
    """


def hero(kicker: str, title_html: str, text: str) -> str:
    """HTML des Hero-Bereichs."""
    return f"""
    <div class="hero">
      <div class="hero-kicker">{kicker}</div>
      <h1>{title_html}</h1>
      <p>{text}</p>
    </div>
    """
