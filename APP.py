#%% streamlit app: CINE·PREDICT — Film-Vorhersage
"""Web-App zur Film-Vorhersage auf Basis von open_router_structured_outcome.py.

Handlungsbeschreibung eingeben -> Top 5 Filme als strukturiertes Ergebnis.
Farben, Schrift und Atmosphäre der Seite folgen dem in der Sidebar gewählten
Lieblingsgenre (Krimi Noir, Science-Fiction, Animation, Action, Fantasy).

Start:  streamlit run APP.py
"""
import streamlit as st

from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

#%% Wie soll das strukturierte Ergebnis aussehen? (wie im Skript)
class MyMovieOutput(BaseModel):
    title: str
    director: str = Field(description="Der Regisseur des Films", examples=["Spielberg, Steven", "Nolan, Christopher"])
    actors: list[str]
    release_year: int


class MyMoviesOutput(BaseModel):
    movies: list[MyMovieOutput]


#%% API-Key: wird im Browser eingegeben und nur in der Session gehalten
def api_key_eingabe() -> str:
    """Sidebar-Eingabe für den OpenRouter-API-Key; gibt den Key zurück.

    Der Key liegt ausschließlich in st.session_state und wird nirgends
    gespeichert oder geloggt. Widget-Key bleibt konstant, damit die Eingabe
    einen Rerun übersteht.
    """
    with st.sidebar:
        st.markdown("### 🔑 API-Key")
        key = st.text_input(
            "OpenRouter-API-Key",
            type="password",
            key="OPENROUTER_API_KEY",
            placeholder="sk-or-...",
            help="Wird nur für diese Sitzung gehalten und nicht gespeichert.",
        )
    return key.strip()


#%% Chain aufbauen (nur einmal laden)
@st.cache_resource(show_spinner=False)
def build_chain(api_key: str):
    parser = JsonOutputParser(pydantic_object=MyMoviesOutput)

    messages = [
        ("system", """
            Du bist ein Hobby Cineast und kennst die meisten Filme.
            Der Nutzer übergibt dir eine Beschreibung der Handlung und lieferst strukturiert die Ergebnisse zurück.
            Gib mir die Top 5 zurück.
            Halte dich strikt an die Formatinstruktionen {format_instructions}.
        """),
        ("user", "Beschreibung des Films: {description}")
    ]
    prompt_template = ChatPromptTemplate.from_messages(messages).partial(
        format_instructions=parser.get_format_instructions()
    )

    model = ChatOpenRouter(model="anthropic/claude-haiku-5.5", api_key=api_key)

    return prompt_template | model | parser


# ---------------------------------------------------------------------------
# Favoriten: Genre -> Thema (Farben, Schrift, Atmosphäre)
# ---------------------------------------------------------------------------
# Paletten liegen in movie_theme.py, das Stylesheet in movie_styles.py
from movie_theme import GENRES, GENRE_ORDER
from movie_styles import build_css, hero, movie_card


def favoriten_sidebar(paletten, reihenfolge):
    """Sidebar mit den Favoriten; gibt (genre, stimmung, ton, anzahl) zurück.

    Die Widgets laufen über feste Keys. Dadurch bleibt die Auswahl des Nutzers
    erhalten und wird bei einem Rerun nicht durch einen Default überschrieben.
    """
    defaults = {
        "fav_genre": "Neutral",
        "fav_stimmung": "Kino-Abend",
        "fav_ton": "Neugierig",
        "fav_anzahl": 5,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)

    with st.sidebar:
        st.markdown("### ⭐ Deine Favoriten")
        st.caption("Farben, Schrift und Atmosphäre der Seite folgen deiner Auswahl.")

        genre = st.radio(
            "Lieblingsgenre",
            reihenfolge,
            key="fav_genre",
            format_func=lambda g: f"{paletten[g]['emoji']}  {g}",
        )

        st.markdown("---")
        stimmung = st.select_slider(
            "Stimmung",
            options=["Kino-Abend", "Film-Marathon", "Nachdenklich", "Popcorn & Spaß"],
            key="fav_stimmung",
        )
        ton = st.select_slider(
            "Ton der Vorschläge",
            options=["Neugierig", "Gefühlvoll", "Knallhart"],
            key="fav_ton",
        )

        st.markdown("---")
        anzahl = st.slider("Anzahl der Vorschläge", 1, 10, key="fav_anzahl")

        with st.expander("Aktives Thema"):
            p = paletten[genre]
            st.markdown(
                f"**{p['emoji']} {genre}**  \n"
                f"Schrift: `{p['font_head'].strip(chr(39))}`  \n"
                f"Akzentfarbe: `{p['accent']}`"
            )

    return genre, stimmung, ton, anzahl


#%% Oberfläche
st.set_page_config(page_title="CINE·PREDICT – Film-Vorhersage", page_icon="🎬", layout="wide")

genre, stimmung, ton, anzahl = favoriten_sidebar(GENRES, GENRE_ORDER)
api_key = api_key_eingabe()
st.markdown(build_css(GENRES[genre]), unsafe_allow_html=True)
st.markdown(
    hero(
        kicker=f"{GENRES[genre]['emoji']} {genre} &nbsp;·&nbsp; {stimmung}",
        title_html="Beschreib die Handlung.<br>Wir finden <em>deinen Film</em>.",
        text="Erzähl in eigenen Worten, worum es geht — das Modell liefert die "
             "passendsten Filme mit Regie, Besetzung und Erscheinungsjahr.",
    ),
    unsafe_allow_html=True,
)

if not api_key:
    st.warning(
        "Kein OpenRouter-API-Key hinterlegt – bitte in der Seitenleiste eintragen."
    )

description = st.text_area(
    "Beschreibung der Handlung",
    value="Ein Lehrer der Krebs bekomt wandelt nach der Diagnose sein ganzes Leben um",
    height=130,
    placeholder="z. B. Ein Dieb plant den perfekten Coup, während seine Tochter in Gefahr gerät ...",
)

links, rechts = st.columns([1, 3])
with links:
    starten = st.button("Vorhersage starten", type="primary", use_container_width=True)
with rechts:
    st.caption(
        f"Favoriten aktiv: **{genre}** · {stimmung} · Ton *{ton}* — "
        "diese Vorgaben fließen in die Anfrage an das Modell ein."
    )

if starten:
    if not description.strip():
        st.error("Bitte eine Handlungsbeschreibung eingeben.")
    elif not api_key:
        st.error("Bitte zuerst den OpenRouter-API-Key in der Seitenleiste eintragen.")
    else:
        try:
            with st.spinner("Projektor läuft ... das Modell sichtet die Handlung."):
                result = build_chain(api_key).invoke({
                    "description": (
                        f"{description}\n\n"
                        f"Rahmen für deine Auswahl: Genre {genre}, Stimmung {stimmung}, Ton {ton}. "
                        f"Bevorzuge Filme, die zu diesem Rahmen passen."
                    )
                })

            movies = (result.get("movies") or [])[:anzahl]
            if not movies:
                st.info("Das Modell hat keine Filme zurückgegeben.")
            else:
                st.markdown(f"<span class='badge'>{len(movies)} Treffer</span>", unsafe_allow_html=True)
            for i, movie in enumerate(movies, start=1):
                st.markdown(
                    movie_card(
                        index=i,
                        titel=str(movie.get("title", "–")),
                        jahr=movie.get("release_year", "?"),
                        regie=str(movie.get("director", "–")),
                        actors=[str(a) for a in (movie.get("actors") or [])],
                    ),
                    unsafe_allow_html=True,
                )

            with st.expander("Rohantwort (JSON)"):
                st.json(result)
        except Exception as exc:  # API-Fehler, Rate-Limit, ungültiges JSON ...
            st.error(f"Vorhersage fehlgeschlagen: {exc}")

st.markdown(
    '<div class="footer">CINE·PREDICT · Vorhersagen sind Vorschläge, keine Fakten · '
    'Modell: claude-haiku-5.5 via OpenRouter</div>',
    unsafe_allow_html=True,
)
