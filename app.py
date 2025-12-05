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

# --- CSS PERSONNALISÉ (THEME RAM) ---
st.markdown("""
    <style>
    /* Importation d'une police propre */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    /* Couleur de fond générale */
    .stApp {
        background-color: #f8f9fa;
    }

    /* Header avec Logo */
    .ram-header {
        text-align: center;
        padding-bottom: 30px;
        border-bottom: 2px solid #C2002F;
        margin-bottom: 20px;
    }

    /* Boutons style RAM (Rouge) */
    div.stButton > button:first-child {
        background-color: #C2002F;
        color: white;
        border-radius: 5px;
        border: none;
        font-weight: 600;
        text-transform: uppercase;
        padding: 10px 24px;
        width: 100%;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #a00026;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    /* Carte de vol (Card Design) */
    .flight-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-top: 5px solid #C2002F;
    }

    /* Aéroports (GROS) */
    .airport-code {
        font-size: 2.5rem;
        font-weight: 800;
        color: #333;
        margin: 0;
    }
    .airport-name {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
    }

    /* Flèche centrale */
    .route-arrow {
        color: #C2002F;
        font-size: 2rem;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }

    /* Badges de statut */
    .status-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 50px;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.9rem;
        margin-top: 15px;
        margin-bottom: 25px;
    }
    .status-ok { background-color: #e6f9e9; color: #28a745; border: 1px solid #28a745; }
    .status-late { background-color: #fbeaea; color: #dc3545; border: 1px solid #dc3545; }
    .status-wait { background-color: #eefbff; color: #17a2b8; border: 1px solid #17a2b8; }

    /* Métriques horaires */
    .time-label { font-size: 0.8rem; color: #888; text-transform: uppercase; letter-spacing: 1px; }
    .time-value { font-size: 1.4rem; font-weight: 600; color: #222; }
    .delay-warn { color: #dc3545; font-size: 0.9rem; font-weight: bold; }

    </style>
""", unsafe_allow_html=True)

# --- HEADER (LOGO RAM) ---
# Utilisation du logo Wikimedia officiel
st.markdown("""
    <div class="ram-header">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Royal_Air_Maroc_logo.svg/800px-Royal_Air_Maroc_logo.svg.png" width="200">
        <h3 style="margin-top:10px; color:#555;">Suivi de Vol en Temps Réel</h3>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR (INPUTS) ---
with st.sidebar:
    st.markdown("### ✈️ Recherche de Vol")
    st.markdown("Entrez les détails ci-dessous pour suivre un vol Royal Air Maroc.")

    flight_number = st.text_input("Numéro de Vol", value="AT200", placeholder="Ex: AT200")
    date_vol = st.date_input("Date du départ", datetime.now())

    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button("Rechercher le Vol", type="primary")

    st.markdown("---")
    st.caption("© 2025 - Outil de suivi non-officiel basé sur données publiques.")

# --- LOGIQUE PRINCIPALE ---
if search_btn:
    # Nettoyage
    code = flight_number.replace(" ", "").upper()
    if not code.startswith("AT") and code.isdigit():
        code = f"AT{code}"

    date_str = date_vol.strftime("%Y-%m-%d")

    # Spinner personnalisé
    with st.spinner(f"📡 Interrogation des satellites pour le vol {code}..."):
        # Appel du Scraper
        data = get_flight_data(code, date_str)

        # Gestion des erreurs
        if "Vol non trouvé" in data.get("status", ""):
            st.error(f"❌ Impossible de trouver le vol {code} pour cette date.")
        elif "Erreur" in data.get("status", ""):
            st.error(f"⚠️ Une erreur technique est survenue : {data['status']}")
        else:
            # --- AFFICHAGE STYLE "CARTE D'EMBARQUEMENT" ---

            # Détermination de la couleur du statut
            statut_brut = data['status']
            css_class = "status-wait"
            icon = "🕒"

            if any(x in statut_brut.lower() for x in ["atterri", "landed", "arrived"]):
                css_class = "status-ok"
                icon = "✅"
            elif any(x in statut_brut.lower() for x in ["vol", "en route", "flying"]):
                css_class = "status-wait"
                icon = "✈️"

            # Vérification retard important (>15min)
            dep_delay = data['departure']['delay_min']
            if dep_delay and dep_delay > 15:
                css_class = "status-late"
                icon = "⚠️"

            # 1. Conteneur Principal (La Carte)
            with st.container():
                st.markdown('<div class="flight-card">', unsafe_allow_html=True)

                # En-tête de la carte : Route
                c1, c2, c3 = st.columns([3, 1, 3])

                with c1:
                    st.markdown(f"""
                        <div style='text-align:left'>
                            <p class='airport-code'>{data['origin']}</p>
                            <p class='airport-name'>Départ</p>
                        </div>
                    """, unsafe_allow_html=True)

                with c2:
                    st.markdown(f"<div class='route-arrow'>➝</div>", unsafe_allow_html=True)

                with c3:
                    st.markdown(f"""
                        <div style='text-align:right'>
                            <p class='airport-code'>{data['destination']}</p>
                            <p class='airport-name'>Arrivée</p>
                        </div>
                    """, unsafe_allow_html=True)

                # Statut Centré
                st.markdown(f"""
                    <div style='text-align:center'>
                        <span class='status-badge {css_class}'>{icon} {statut_brut}</span>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("---")

                # Détails Horaires (Grid)
                col_dep, col_arr = st.columns(2)

                # --- BLOC DÉPART ---
                with col_dep:
                    st.markdown("<p class='time-label'>🛫 HEURE DÉPART</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='time-value'>{data['departure']['planned']}</p>", unsafe_allow_html=True)

                    # Logique Retard Départ
                    actual = data['departure']['actual']
                    delay = data['departure']['delay_min']

                    if delay and delay > 0:
                        st.markdown(f"<p style='color:#666; font-size:0.9rem;'>Réel : <b>{actual}</b></p>",
                                    unsafe_allow_html=True)
                        st.markdown(f"<p class='delay-warn'>Retard : +{delay} min</p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='color:#28a745; font-size:0.9rem;'>À l'heure</p>",
                                    unsafe_allow_html=True)

                # --- BLOC ARRIVÉE ---
                with col_arr:
                    st.markdown("<p style='text-align:right' class='time-label'>🛬 HEURE ARRIVÉE</p>",
                                unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align:right' class='time-value'>{data['arrival']['planned']}</p>",
                                unsafe_allow_html=True)

                    # Logique Retard Arrivée
                    actual_arr = data['arrival']['actual']
                    delay_arr = data['arrival']['delay_min']

                    if delay_arr and delay_arr > 0:
                        st.markdown(
                            f"<p style='text-align:right; color:#666; font-size:0.9rem;'>Estimé : <b>{actual_arr}</b></p>",
                            unsafe_allow_html=True)
                        st.markdown(
                            f"<p style='text-align:right' class='delay-warn'>Retard à l'arrivée : +{delay_arr} min</p>",
                            unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='text-align:right; color:#28a745; font-size:0.9rem;'>À l'heure</p>",
                                    unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)  # Fin de la card

            # Lien Source discret
            st.markdown(
                f"<div style='text-align:center; margin-top:20px;'><a href='{data['url']}' target='_blank' style='color:#C2002F; text-decoration:none;'>Voir les détails complets sur AirportInfo ></a></div>",
                unsafe_allow_html=True)

else:
    # Message d'accueil (État vide)
    st.info("👋 Bienvenue. Veuillez entrer un numéro de vol dans le menu latéral pour commencer.")