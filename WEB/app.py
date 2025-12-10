import streamlit as st

st.set_page_config(
    page_title="Music Recommender",
    layout="wide"
)

custom_css = """
<style>

/* -- GLOBAL --------------------------------------------------- */

body {
    font-family: 'Inter', sans-serif;
    background: #f5f7fa !important;
}

/* Conteneur principal Streamlit */
.main {
    background: #f5f7fa !important;
    padding: 20px;
}

/* -- TITRES --------------------------------------------------- */

h1 {
    font-size: 2.6rem !important;
    font-weight: 800 !important;
    color: #222 !important;
}

h2, h3 {
    color: #2c7a7b !important; /* bleu-vert doux */
    font-weight: 700 !important;
}

/* -- CARDS (colonnes) ---------------------------------------- */

.card {
    background: #ffffffcc;               /* blanc léger transparent */
    backdrop-filter: blur(8px);          /* effet glassmorphism */
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e3e7ec;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.06);
    transition: 0.25s ease-in-out;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0px 8px 28px rgba(0,0,0,0.1);
}

/* -- INPUTS ---------------------------------------------------- */

input, textarea, select {
    background-color: #ffffff !important;
    color: #333 !important;
    border-radius: 12px !important;
    border: 1px solid #d0d7df !important;
    padding: 10px !important;
    font-size: 15px !important;
    transition: 0.2s;
}

/* Inputs focus */
input:focus, textarea:focus, select:focus {
    border: 1px solid #2c7a7b !important;
    box-shadow: 0 0 0 3px rgba(44, 122, 123, 0.2) !important;
    outline: none !important;
}

/* Multiselect correction */
.stMultiSelect div {
    background-color: #ffffff !important;
    border-radius: 12px !important;
}

/* -- BUTTON ---------------------------------------------------- */

.stButton > button {
    background: #2c7a7b;
    color: white;
    font-size: 18px;
    padding: 12px 38px;
    border-radius: 30px;
    border: none;
    font-weight: 600;
    transition: 0.25s ease-in-out;
    box-shadow: 0px 6px 16px rgba(44, 122, 123, 0.3);
}

.stButton > button:hover {
    background: #349ea2;
    transform: translateY(-3px);
    box-shadow: 0px 8px 22px rgba(44, 122, 123, 0.35);
}

/* -- DIVISEUR -------------------------------------------------- */

hr {
    border: none;
    height: 1px;
    background: #e3e7ec;
    margin: 30px 0;
}

</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# header
st.markdown("<h1>Music Mood Recommender</h1>", unsafe_allow_html=True)
st.write("Découvrez les musiques qui correspondent à votre mood, vos goûts et votre univers musical.")

st.markdown("---")

left, right = st.columns(2)

# colonne gauche
with left:
    st.markdown("## Mood actuel")
    mood = st.text_input("Mood actuel ou mood désiré (ex: motivé, chill, concentré, triste, soirée…)")

    st.markdown("## Tes goûts musicaux")
    preferences = st.text_area(
        "Artistes, chansons, ambiances ou types de sons que tu apprécies.",
        height=160,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# colonne droite
with right:
    st.markdown("## Genres préférés")
    genres_list = [
        "Pop", "Rap", "RnB", "Rock", "Metal", "Jazz", "Classique", "Techno",
        "Electro", "K-pop", "Reggaeton", "Afrobeat", "LoFi", "Indie"
    ]
    selected_genres = st.multiselect("Choisissez vos genres favoris :", genres_list)

    st.markdown("## Infos complémentaires")
    extra = st.text_area(
        "Moments où tu écoutes de la musique (sport, travail, soirée…), instruments aimés, BPM préféré…",
        height=140,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# btn recherche 
st.markdown("<br>", unsafe_allow_html=True)
center = st.columns([1, 1, 1])[1]

with center:
    search_button = st.button("Rechercher")

st.markdown("---")

# resultat
if search_button:
    if not mood.strip() and not preferences.strip():
        st.error("Merci de renseigner au minimum votre mood **et** vos goûts musicaux.")
    else:
        st.success("Analyse en cours…")
        st.markdown("### Recommandations personnalisées :")

        sample_tracks = [
            "*test1",
            "*test2",
            "*test3",
            "*test4"
        ]

        for track in sample_tracks:
            st.markdown(f"- {track}")
        st.markdown("</div>", unsafe_allow_html=True)
