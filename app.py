import streamlit as st
from datetime import datetime
# Assurez-vous que votre fichier s'appelle bien scraper.py
from scraper import get_flight_data

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Suivi de Vol - Royal Air Maroc",
    page_icon="🇲🇦",
    layout="centered"
)

# --- CSS PERSONNALISÉ (CORRECTIFS & THEME RAM) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap');

    /* 1. FORCER LE MODE CLAIR (Evite le blanc sur blanc) */
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        color: #333333; /* Couleur de texte par défaut forcée en gris foncé */
    }

    .stApp {
        background-color: #f4f6f9;
    }

    /* 2. CORRECTION DU SPINNER (Texte de chargement) */
    .stSpinner > div > div {
        color: #C2002F !important; /* Texte du spinner en Rouge RAM */
        font-weight: 600;
    }

    /* HEADER PAGE */
    .ram-header {
        text-align: center;
        padding-bottom: 20px;
        margin-bottom: 30px;
        border-bottom: 3px solid #C2002F;
    }

    /* BOUTONS */
    div.stButton > button:first-child {
        background-color: #C2002F;
        color: white;
        border-radius: 50px;
        border: none;
        font-weight: 700;
        text-transform: uppercase;
        padding: 12px 30px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(194, 0, 47, 0.2);
    }
    div.stButton > button:first-child:hover {
        background-color: #960024;
        transform: translateY(-2px);
    }

    /* --- NOUVEAU DESIGN DE LA CARTE DE VOL --- */

    /* Bloc du haut (Numéro de vol) */
    .flight-header-strip {
        background-color: white;
        color: #C2002F;
        font-size: 2rem;
        font-weight: 800;
        text-align: center;
        padding: 15px;
        border-top-left-radius: 20px;
        border-top-right-radius: 20px;
        border-bottom: 2px solid #f0f0f0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }

    /* Bloc principal (Contenu) */
    .flight-card-body {
        background-color: #ffffff; /* Fond blanc comme sur le site RAM */
        padding: 30px;
        border-bottom-left-radius: 20px;
        border-bottom-right-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    /* Aéroports (Style très gros) */
    .airport-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
    }
    .airport-block {
        text-align: center;
        width: 40%;
    }
    .airport-code {
        font-size: 3.5rem; /* Très gros */
        font-weight: 800;
        color: #222;
        line-height: 1;
    }
    .airport-city {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        margin-top: 5px;
        font-weight: 600;
    }

    /* Flèche centrale animée */
    .flight-arrow {
        font-size: 2rem;
        color: #C2002F;
        font-weight: bold;
    }

    /* Badges Statut */
    .status-container {
        text-align: center;
        margin: -15px auto 30px auto;
    }
    .status-badge {
        padding: 8px 25px;
        border-radius: 30px;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.9rem;
        letter-spacing: 1px;
    }
    .status-ok { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    .status-late { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    .status-wait { background-color: #e2e6ea; color: #333; border: 1px solid #ccc; }

    /* Horaires */
    .time-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        border-top: 1px solid #eee;
        padding-top: 20px;
    }
    .time-col-left { text-align: left; }
    .time-col-right { text-align: right; }

    .time-label { font-size: 0.75rem; color: #999; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;}
    .time-huge { font-size: 2rem; font-weight: 700; color: #333; }
    .time-real { font-size: 1rem; color: #e67e22; font-weight: 600; margin-top: 5px;}
    .delay-alert { color: #C2002F; font-weight: 800; font-size: 0.9rem; }

    </style>
""", unsafe_allow_html=True)

# --- HEADER LOGO ---
st.markdown("""
    <div class="ram-header">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Logo_Royal_Air_Maroc.svg/2560px-Logo_Royal_Air_Maroc.svg.png" width="220">
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("✈️ Recherche")
    flight_number = st.text_input("Numéro de Vol", value="AT200")
    date_vol = st.date_input("Date de départ", datetime.now())
    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button("VOIR LE STATUT")
    st.markdown("---")
    st.caption("Données indicatives AirportInfo.")

# --- LOGIQUE ---
if search_btn:
    code = flight_number.replace(" ", "").upper()
    if not code.startswith("AT") and code.isdigit():
        code = f"AT{code}"
    date_str = date_vol.strftime("%Y-%m-%d")

    # Spinner avec texte coloré par CSS
    with st.spinner(f"📡 Connexion satellite pour {code}..."):
        try:
            data = get_flight_data(code, date_str)

            if "Vol non trouvé" in data.get("status", ""):
                st.error("❌ Vol introuvable.")
            elif "Erreur" in data.get("status", ""):
                st.error(f"⚠️ Erreur: {data['status']}")
            else:
                # --- LOGIQUE STATUT ---
                statut = data['status']
                css_status = "status-wait"
                icon = "✈️"

                if any(x in statut.lower() for x in ["atterri", "landed", "arrivé"]):
                    css_status = "status-ok"
                    icon = "✅"
                elif "retard" in statut.lower() or "delayed" in statut.lower():
                    css_status = "status-late"
                    icon = "⚠️"

                dep_delay = data['departure']['delay_min']
                if dep_delay and dep_delay > 15:
                    css_status = "status-late"

                # --- AFFICHAGE DE LA CARTE ---
                with st.container():
                    # 1. BANDEAU SUPÉRIEUR (Numéro de Vol)
                    st.markdown(f'<div class="flight-header-strip">{code}</div>', unsafe_allow_html=True)

                    # 2. CORPS DE LA CARTE
                    st.markdown('<div class="flight-card-body">', unsafe_allow_html=True)

                    # Ligne Aéroports (CMN -> JFK)
                    st.markdown(f"""
                        <div class="airport-row">
                            <div class="airport-block">
                                <div class="airport-code">{data['origin']}</div>
                                <div class="airport-city">DÉPART</div>
                            </div>
                            <div class="flight-arrow">➝</div>
                            <div class="airport-block">
                                <div class="airport-code">{data['destination']}</div>
                                <div class="airport-city">ARRIVÉE</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    # Badge Statut Centré
                    st.markdown(f"""
                        <div class="status-container">
                            <span class="status-badge {css_status}">{icon} {statut}</span>
                        </div>
                    """, unsafe_allow_html=True)

                    # Grille Horaires
                    col1, col2 = st.columns(2)

                    with col1:
                        # DÉPART
                        st.markdown(f"""
                            <div style="text-align:left; border-right: 1px solid #eee;">
                                <div class="time-label">Heure de départ</div>
                                <div class="time-huge">{data['departure']['planned']}</div>
                        """, unsafe_allow_html=True)

                        act = data['departure']['actual']
                        dly = data['departure']['delay_min']

                        if dly and dly > 0:
                            st.markdown(f'<div class="time-real">Réel : {act}</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="delay-alert">Retard : +{dly} min</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(
                                '<div style="color:#28a745; font-size:0.9rem; margin-top:5px;">À l\'heure</div>',
                                unsafe_allow_html=True)

                        st.markdown("</div>", unsafe_allow_html=True)

                    with col2:
                        # ARRIVÉE
                        st.markdown(f"""
                            <div style="text-align:right;">
                                <div class="time-label">Heure d'arrivée</div>
                                <div class="time-huge">{data['arrival']['planned']}</div>
                        """, unsafe_allow_html=True)

                        act_arr = data['arrival']['actual']
                        dly_arr = data['arrival']['delay_min']

                        if dly_arr and dly_arr > 0:
                            st.markdown(f'<div class="time-real">Estimé : {act_arr}</div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="delay-alert">Retard : +{dly_arr} min</div>',
                                        unsafe_allow_html=True)
                        else:
                            st.markdown(
                                '<div style="color:#28a745; font-size:0.9rem; margin-top:5px;">À l\'heure</div>',
                                unsafe_allow_html=True)

                        st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)  # Fin body

        except Exception as e:
            st.error(f"Erreur: {e}")

else:
    st.info("Entrez un numéro de vol pour commencer.")