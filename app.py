import streamlit as st
from datetime import datetime


# --- FONCTION MOCK (Pour tester sans ton scraper, à remplacer par ton import) ---
# Remplace ceci par: from scraper import get_flight_data
def get_flight_data(code, date):
    # Simulation de données pour l'exemple
    return {
        "status": "RETARDÉ (+28min)",
        "origin": "CMN",
        "destination": "JFK",
        "url": "https://www.royalairmaroc.com",
        "departure": {"planned": "15:50", "actual": "16:18", "delay_min": 28},
        "arrival": {"planned": "17:55", "actual": "18:12", "delay_min": 17}
    }


# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="RAM Flight Tracker", page_icon="✈️", layout="centered")

# --- CSS PERSONNALISÉ (Pour le look "Image") ---
st.markdown("""
    <style>
    /* Conteneur principal style carte sombre */
    .flight-card {
        background-color: #161b22; /* Couleur sombre de l'image */
        color: white;
        padding: 25px;
        border-radius: 12px;
        font-family: 'Helvetica', sans-serif;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }

    /* En-tête avec Code Vol et Date */
    .card-header {
        display: flex;
        justify-content: space-between;
        border-bottom: 1px dashed #444;
        padding-bottom: 10px;
        margin-bottom: 20px;
        color: #d03027; /* Rouge RAM */
        font-weight: bold;
        font-size: 1.2em;
    }
    .date-label { color: #888; font-size: 0.8em; font-weight: normal; align-self: center;}

    /* Route (CMN - JFK) */
    .route-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .plane-icon { font-size: 0.6em; color: #d03027; transform: rotate(90deg); }
    .city-label { font-size: 0.3em; color: #888; display: block; text-align: center; font-weight: normal;}

    /* Badge Statut */
    .status-badge {
        text-align: center;
        margin-bottom: 25px;
        padding: 8px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 0.9em;
    }
    .status-red { background-color: rgba(220, 53, 69, 0.2); color: #ff6b6b; border: 1px solid #ff6b6b; }
    .status-green { background-color: rgba(40, 167, 69, 0.2); color: #5ddc79; border: 1px solid #5ddc79; }

    /* Grille des horaires (Times Grid) */
    .times-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        text-align: center;
        gap: 20px;
    }
    .time-label { color: #aaa; font-size: 0.75em; letter-spacing: 1px; margin-bottom: 5px; text-transform: uppercase;}
    .time-big { font-size: 1.8em; font-weight: bold; color: white; }
    .text-red { color: #ff6b6b; font-size: 0.9em; margin-top: 5px; }
    .text-green { color: #5ddc79; font-size: 0.9em; margin-top: 5px; }

    /* Cacher les éléments natifs Streamlit qui gênent */
    .stApp { background-color: #f0f2f6; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER AVEC LOGO (Simulé) ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    # Tu peux mettre le logo RAM ici via st.image()
    st.markdown("<h3 style='text-align:center; color:#d03027;'>ROYAL AIR MAROC</h3>", unsafe_allow_html=True)

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.header("Paramètres")
    flight_number = st.text_input("Numéro de Vol", value="AT200")
    date_vol = st.date_input("Date du vol", datetime.now())
    search_btn = st.button("Rechercher 🔍", type="primary")

# --- LOGIQUE PRINCIPALE ---
if search_btn:
    # Nettoyage Code Vol
    code = flight_number.replace(" ", "").upper()
    if not code.startswith("AT") and code.isdigit():
        code = f"AT{code}"

    date_str = date_vol.strftime("%Y-%m-%d")
    date_display = date_vol.strftime("%d %B %Y")

    with st.spinner(f"📡 Recherche du vol {code}..."):
        # APPEL DE LA FONCTION
        data = get_flight_data(code, date_str)

        if "Vol non trouvé" in str(data.get("status", "")):
            st.error(f"❌ {data['status']}")
        else:
            # 1. Calculs pour le style (Logique Python)
            is_delayed = data['departure']['delay_min'] is not None and data['departure']['delay_min'] > 15

            # Statut CSS
            status_class = "status-red" if is_delayed else "status-green"
            status_icon = "⚠️" if is_delayed else "✅"

            # Textes d'estimation
            dep_est_html = ""
            if data['departure']['delay_min']:
                dep_est_html = f"<div class='text-red'>Estimé: {data['departure']['actual']} (+{data['departure']['delay_min']}m)</div>"

            arr_est_html = ""
            if data['arrival']['delay_min']:
                arr_est_html = f"<div class='text-red'>Estimé: {data['arrival']['actual']} (+{data['arrival']['delay_min']}m)</div>"

            # 2. Construction du HTML (Le visuel Carte Noire)
            html_card = f"""
            <div class="flight-card">
                <div class="card-header">
                    <div>{code}</div>
                    <div class="date-label">{date_display}</div>
                </div>

                <div class="route-row">
                    <div>
                        {data['origin']}
                        <span class="city-label">DÉPART</span>
                    </div>
                    <div class="plane-icon">✈</div>
                    <div>
                        {data['destination']}
                        <span class="city-label">ARRIVÉE</span>
                    </div>
                </div>

                <div class="status-badge {status_class}">
                    {status_icon} {data['status'].upper()}
                </div>

                <div class="times-grid">
                    <div>
                        <div class="time-label">HEURE DE DÉPART</div>
                        <div class="time-big">{data['departure']['planned']}</div>
                        {dep_est_html}
                    </div>
                    <div>
                        <div class="time-label">HEURE D'ARRIVÉE</div>
                        <div class="time-big">{data['arrival']['planned']}</div>
                        {arr_est_html}
                    </div>
                </div>
            </div>
            """

            # 3. Affichage
            st.markdown(html_card, unsafe_allow_html=True)

            st.caption(f"Source: Données en temps réel via {data['url']}")