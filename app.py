import streamlit as st
from datetime import datetime
# Assurez-vous d'avoir votre fichier scraper.py dans le même dossier
from scraper import get_flight_data

# --- CONFIGURATION PAGE ---
st.set_page_config(
    page_title="Suivi de Vol | Royal Air Maroc",
    page_icon="🇲🇦",
    layout="centered"
)

# --- CSS CORRIGÉ (DESIGN ET CORRECTIFS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        color: #333;
    }

    /* Fond de l'application */
    .stApp {
        background-color: #F4F6F9;
    }

    /* --- SIDEBAR (FOND ROUGE FONCÉ) --- */
    section[data-testid="stSidebar"] {
        background-color: #8A0021;
    }
    section[data-testid="stSidebar"] * {
        color: white;
    }
    section[data-testid="stSidebar"] input {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] .stTextInput input, 
    section[data-testid="stSidebar"] .stDateInput input {
        background-color: #1a1a1a !important; 
        border: 1px solid #b03045 !important;
        border-radius: 8px;
    }
    section[data-testid="stSidebar"] [data-testid="stDateInput"] svg {
        fill: white !important;
    }

    /* BOUTON RECHERCHE */
    section[data-testid="stSidebar"] .stButton button,
    section[data-testid="stSidebar"] .stButton button p {
        background-color: #FFFFFF !important;
        color: #8A0021 !important;
        font-weight: 800 !important;
        border: none !important;
        text-transform: uppercase;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: #f0f0f0 !important;
        transform: scale(1.02);
    }

    /* --- CARTE DE RÉSULTAT --- */
    .flight-card {
        background-color: #ffffff; /* Fond blanc forcé */
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        overflow: hidden;
        margin-top: 20px;
        border-top: 6px solid #C2002F;
        padding-bottom: 20px;
    }

    /* En-tête de la carte (AT200 + Date) */
    .card-header-strip {
        background-color: #fff;
        padding: 15px 25px;
        display: flex; 
        justify-content: space-between; 
        align-items: center;
        border-bottom: 1px solid #f0f0f0;
    }
    .flight-num-big { 
        font-size: 1.8rem; 
        font-weight: 800; 
        color: #C2002F; 
        letter-spacing: 1px; 
    }
    .flight-date-small {
        color: #888;
        font-weight: 600;
        font-size: 0.9rem;
    }

    .card-body { 
        padding: 20px 30px; 
    }

    /* Alignement aéroports (CMN -> JFK) */
    .route-flex { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        margin-bottom: 30px; 
        margin-top: 10px;
    }
    .airport-block {
        text-align: center;
        min-width: 80px;
    }
    .airport-code { 
        font-size: 3rem; 
        font-weight: 800; 
        color: #222; 
        line-height: 1; 
    }
    .airport-label { 
        font-size: 0.85rem; 
        color: #777; 
        font-weight: 600;
        text-transform: uppercase; 
        margin-top: 5px;
    }
    .plane-icon {
        font-size: 1.5rem;
        color: #C2002F;
    }

    /* Badge central */
    .status-container {
        text-align: center;
        margin-bottom: 40px;
    }
    .status-badge { 
        display: inline-block; 
        padding: 10px 30px; 
        border-radius: 50px; 
        font-weight: 700; 
        font-size: 0.9rem;
        text-transform: uppercase; 
        letter-spacing: 1px;
    }
    .status-green { background-color: #DEF7EC; color: #03543F; border: 1px solid #bcf0da; }
    .status-red { background-color: #FDE8E8; color: #9B1C1C; border: 1px solid #fbd5d5; }

    /* Grille Horaires (FLEXBOX pour centrage parfait) */
    .times-flex { 
        display: flex; 
        justify-content: space-around; /* Espace égal autour */
        align-items: flex-start;
        border-top: 1px solid #eee; 
        padding-top: 25px; 
    }

    .time-column {
        display: flex;
        flex-direction: column;
        align-items: center; /* Centrage horizontal des textes */
        width: 45%;
    }

    .time-big { font-size: 2rem; font-weight: 700; color: #222; margin: 5px 0; }
    .time-label { font-size: 0.75rem; color: #999; text-transform: uppercase; font-weight: 700; letter-spacing: 1px;}

    .text-red { color: #DC2626; font-size: 0.9rem; font-weight: 700; margin-top: 5px; }
    .text-green { color: #28a745; font-size: 0.9rem; font-weight: 700; margin-top: 5px; }

    </style>
""", unsafe_allow_html=True)

# --- LOGO EN HAUT ---
st.markdown("""
    <div style="text-align: center; padding-bottom: 20px; margin-bottom: 20px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Logo_Royal_Air_Maroc.svg/2560px-Logo_Royal_Air_Maroc.svg.png" width="220" alt="Logo RAM">
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## ✈️ MON VOL")
    st.markdown("Recherchez le statut de votre vol.")

    # Inputs
    flight_number_input = st.text_input("N° de Vol", value="AT200", placeholder="Ex: AT200")
    date_vol = st.date_input("Date de départ", datetime.now())

    st.markdown("<br>", unsafe_allow_html=True)

    # BOUTON RECHERCHE
    search_btn = st.button("RECHERCHER LE VOL")

    st.markdown(
        "<br><br><div style='font-size: 0.7em; opacity: 0.7; text-align:center'>© Royal Air Maroc 2025<br>Application Client</div>",
        unsafe_allow_html=True)

# --- LOGIQUE ---
if search_btn:
    code = flight_number_input.replace(" ", "").upper()
    if not code.startswith("AT") and code.isdigit():
        code = f"AT{code}"
    date_str = date_vol.strftime("%Y-%m-%d")

    with st.spinner('Connexion aux serveurs RAM...'):
        try:
            data = get_flight_data(code, date_str)

            if "Vol non trouvé" in data.get("status", ""):
                st.error("❌ Vol introuvable. Vérifiez le numéro.")
            elif "Erreur" in data.get("status", ""):
                st.error(f"⚠️ Erreur: {data['status']}")
            else:
                # Préparation variables
                statut_txt = data['status'].upper()
                css_badge = "status-green"
                icon = "✅"

                if "RETARD" in statut_txt or "DELAYED" in statut_txt:
                    css_badge = "status-red"
                    icon = "⚠️"

                # Gestion Retard > 15min
                dep_delay = data['departure']['delay_min']
                if dep_delay and dep_delay > 15:
                    css_badge = "status-red"
                    icon = "⚠️"
                    statut_txt = f"RETARDÉ (+{dep_delay}min)"


                # Helpers HTML
                def get_delay_html(delay, actual):
                    if delay and delay > 0:
                        return f'<div class="text-red">Estimé: {actual} (+{delay}m)</div>'
                    return '<div class="text-green">À l\'heure</div>'


                sub_dep = get_delay_html(data['departure']['delay_min'], data['departure']['actual'])
                sub_arr = get_delay_html(data['arrival']['delay_min'], data['arrival']['actual'])

                # HTML FINAL (SANS INDENTATION pour éviter le bug d'affichage code)
                html_content = f"""
<div class="flight-card">
    <div class="card-header-strip">
        <div class="flight-num-big">{code}</div>
        <div class="flight-date-small">{date_vol.strftime('%d %B %Y')}</div>
    </div>

    <div class="card-body">

        <div class="route-flex">
            <div class="airport-block" style="text-align:left;">
                <div class="airport-code">{data['origin']}</div>
                <div class="airport-label">DÉPART</div>
            </div>
            <div class="plane-icon">✈</div>
            <div class="airport-block" style="text-align:right;">
                <div class="airport-code">{data['destination']}</div>
                <div class="airport-label">ARRIVÉE</div>
            </div>
        </div>

        <div class="status-container">
            <span class="status-badge {css_badge}">
                {icon} {statut_txt}
            </span>
        </div>

        <div class="times-flex">
            <div class="time-column">
                <div class="time-label">HEURE DE DÉPART</div>
                <div class="time-big">{data['departure']['planned']}</div>
                {sub_dep}
            </div>
            <div class="time-column">
                <div class="time-label">HEURE D'ARRIVÉE</div>
                <div class="time-big">{data['arrival']['planned']}</div>
                {sub_arr}
            </div>
        </div>

    </div>
</div>
"""
                st.markdown(html_content, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erreur technique : {e}")
else:
    st.info("👋 Entrez un numéro de vol dans le menu rouge à gauche.")