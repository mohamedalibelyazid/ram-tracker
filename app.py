import streamlit as st
from datetime import datetime
# Import du scraper (Renommez votre fichier scraping.py en scraper.py si besoin)
from scraper import get_flight_data

# --- CONFIGURATION PAGE ---
st.set_page_config(
    page_title="Suivi de Vol - Royal Air Maroc",
    page_icon="🇲🇦",
    layout="centered"
)

# --- CSS PERSONNALISÉ (DESIGN EXACT) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700;800&display=swap');

    /* Fond général */
    .stApp {
        background-color: #f4f6f9;
    }

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        color: #333;
    }

    /* HEADER PAGE */
    .ram-header {
        text-align: center;
        padding-bottom: 20px;
        margin-bottom: 30px;
        border-bottom: 3px solid #C2002F;
    }

    /* BOUTON RECHERCHE */
    div.stButton > button:first-child {
        background-color: #C2002F;
        color: white;
        border-radius: 50px;
        font-weight: 700;
        text-transform: uppercase;
        padding: 12px 30px;
        width: 100%;
        border: none;
        box-shadow: 0 4px 10px rgba(194, 0, 47, 0.2);
        transition: all 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #960024;
        transform: scale(1.02);
    }

    /* --- CARTE DE VOL --- */

    /* 1. Bandeau Numéro de Vol (AT200) */
    .flight-header-strip {
        background-color: #ffffff;
        color: #C2002F; /* Texte Rouge RAM */
        font-size: 2.2rem;
        font-weight: 800;
        text-align: center;
        padding: 15px;
        border-radius: 15px 15px 0 0;
        border-bottom: 1px solid #eee;
        box-shadow: 0 -5px 15px rgba(0,0,0,0.03); /* Légère ombre vers le haut */
        letter-spacing: 1px;
    }

    /* 2. Corps de la carte */
    .flight-card-body {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 0 0 15px 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    /* Aéroports */
    .airport-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
    }
    .airport-block {
        text-align: center;
        width: 40%;
    }
    .airport-code {
        font-size: 3rem;
        font-weight: 800;
        color: #222;
        line-height: 1;
        margin-bottom: 5px;
    }
    .airport-label {
        font-size: 0.8rem;
        color: #777;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .flight-arrow {
        font-size: 1.5rem;
        color: #C2002F;
        font-weight: bold;
    }

    /* Badge Statut (Pillule) */
    .status-container {
        text-align: center;
        margin-bottom: 35px;
    }
    .status-badge {
        padding: 8px 30px;
        border-radius: 50px;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
    }
    .status-ok { background-color: #fbecec; color: #C2002F; border: 1px solid #fadbd8; } /* Style RAM En route */
    .status-landed { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    .status-late { background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; }

    /* Horaires - CENTRÉS */
    .time-grid {
        display: flex;
        justify-content: space-between;
        border-top: 1px solid #f0f0f0;
        padding-top: 25px;
    }
    .time-col {
        width: 48%;
        text-align: center; /* CENTRAGE FORCÉ ICI */
    }

    .time-label {
        font-size: 0.7rem;
        color: #aaa;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .time-main {
        font-size: 2rem;
        font-weight: 700;
        color: #222;
        margin-bottom: 5px;
    }

    /* Textes additionnels (Réel, Retard, À l'heure) */
    .info-sub {
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 5px;
    }
    .color-green { color: #28a745; }
    .color-orange { color: #e67e22; }
    .color-red { color: #C2002F; }

    /* --- SIDEBAR --- */
    section[data-testid="stSidebar"] {
        background-color: #C2002F !important;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] .stTextInput input, section[data-testid="stSidebar"] .stDateInput input {
        border: 2px solid #960024;
        border-radius: 5px;
        color: #333 !important; /* Keep text inside input dark */
    }

    section[data-testid="stSidebar"] .stButton button {
        background-color: white !important;
        color: #C2002F !important;
        border: 1px solid #C2002F;
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: #f0f0f0 !important;
    }

    </style>
""", unsafe_allow_html=True)

# --- LOGO ---
st.markdown("""
    <div class="ram-header">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Logo_Royal_Air_Maroc.svg/2560px-Logo_Royal_Air_Maroc.svg.png" width="220">
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("✈️ Recherche de vol")
    flight_number = st.text_input("Numéro de Vol", value="AT200")
    date_vol = st.date_input("Date de départ", datetime.now())
    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button("VOIR LE STATUT")
    st.markdown("---")
    st.caption("© 2025 Royal Air Maroc. Tous les droits réservés")

# --- LOGIQUE ---
if search_btn:
    code = flight_number.replace(" ", "").upper()
    if not code.startswith("AT") and code.isdigit():
        code = f"AT{code}"
    date_str = date_vol.strftime("%Y-%m-%d")

    with st.spinner(f"Connexion au vol {code}..."):
        try:
            data = get_flight_data(code, date_str)

            if "Vol non trouvé" in data.get("status", ""):
                st.error("❌ Vol introuvable.")
            elif "Erreur" in data.get("status", ""):
                st.error(f"⚠️ Erreur: {data['status']}")
            else:
                # --- STATUT ---
                statut = data['status']
                css_status = "status-ok"  # Par défaut rouge clair (En route)
                icon = "✈️"

                # Logique couleur
                if any(x in statut.lower() for x in ["atterri", "landed", "arrivé"]):
                    css_status = "status-landed"
                    icon = "✅"
                elif "retard" in statut.lower() or "delayed" in statut.lower():
                    css_status = "status-late"
                    icon = "⚠️"

                # Override si retard détecté > 15min
                dep_delay = data['departure']['delay_min']
                if dep_delay and dep_delay > 15:
                    css_status = "status-late"
                    icon = "⚠️"

                # --- AFFICHAGE CARTE ---
                with st.container():

                    # 1. HEADER (AT200 en Rouge sur Blanc)
                    st.markdown(f'<div class="flight-header-strip">{code}</div>', unsafe_allow_html=True)

                    # 2. BODY
                    st.markdown('<div class="flight-card-body">', unsafe_allow_html=True)

                    # Aéroports
                    st.markdown(f"""
                        <div class="airport-row">
                            <div class="airport-block">
                                <div class="airport-code">{data['origin']}</div>
                                <div class="airport-label">DÉPART</div>
                            </div>
                            <div class="flight-arrow">➝</div>
                            <div class="airport-block">
                                <div class="airport-code">{data['destination']}</div>
                                <div class="airport-label">ARRIVÉE</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    # Pillule Statut
                    st.markdown(f"""
                        <div class="status-container">
                            <span class="status-badge {css_status}">{icon} {statut}</span>
                        </div>
                    """, unsafe_allow_html=True)

                    # Grille Horaires (CENTRÉE)
                    col1, col2 = st.columns(2)

                    # DÉPART (Gauche)
                    with col1:
                        st.markdown(f"""
                            <div style="text-align:center;">
                                <div class="time-label">HEURE DE DÉPART</div>
                                <div class="time-main">{data['departure']['planned']}</div>
                        """, unsafe_allow_html=True)

                        act = data['departure']['actual']
                        dly = data['departure']['delay_min']

                        if dly and dly > 0:
                            st.markdown(f'<div class="info-sub color-orange">Réel : {act}</div>',
                                        unsafe_allow_html=True)
                            st.markdown(f'<div class="info-sub color-red">Retard : +{dly} min</div>',
                                        unsafe_allow_html=True)
                        elif act != "N/A":
                            st.markdown('<div class="info-sub color-green">À l\'heure</div>', unsafe_allow_html=True)

                        st.markdown("</div>", unsafe_allow_html=True)

                    # ARRIVÉE (Droite)
                    with col2:
                        st.markdown(f"""
                            <div style="text-align:center;">
                                <div class="time-label">HEURE D'ARRIVÉE</div>
                                <div class="time-main">{data['arrival']['planned']}</div>
                        """, unsafe_allow_html=True)

                        act_arr = data['arrival']['actual']
                        dly_arr = data['arrival']['delay_min']

                        if dly_arr and dly_arr > 0:
                            st.markdown(f'<div class="info-sub color-orange">Estimé : {act_arr}</div>',
                                        unsafe_allow_html=True)
                            st.markdown(f'<div class="info-sub color-red">Retard : +{dly_arr} min</div>',
                                        unsafe_allow_html=True)
                        elif act_arr != "N/A":
                            # C'EST ICI QUE CA SERA MAINTENANT PARFAITEMENT CENTRÉ
                            st.markdown('<div class="info-sub color-green">À l\'heure</div>', unsafe_allow_html=True)

                        st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)  # Fin Body

        except Exception as e:
            st.error(f"Erreur: {e}")

else:
    st.info("Entrez un numéro de vol (ex: AT200) pour commencer.")