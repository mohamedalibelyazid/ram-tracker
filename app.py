import streamlit as st
from datetime import datetime
import textwrap  # Permet de nettoyer l'indentation HTML
from scraper import get_flight_data

# --- CONFIGURATION PAGE ---
st.set_page_config(
    page_title="Suivi de Vol | Royal Air Maroc",
    page_icon="🇲🇦",
    layout="centered"
)

# --- CSS (DESIGN ET CORRECTIFS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    /* Force le fond de l'app en gris clair */
    .stApp {
        background-color: #F4F6F9;
    }

    /* --- SIDEBAR SOMBRE (Comme sur votre image) --- */
    section[data-testid="stSidebar"] {
        background-color: #1E1E24; /* Gris très foncé / Noir */
    }

    /* Texte sidebar en blanc */
    section[data-testid="stSidebar"] .stMarkdown h1, 
    section[data-testid="stSidebar"] .stMarkdown h2, 
    section[data-testid="stSidebar"] .stMarkdown h3, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    /* Inputs sidebar (Fond sombre) */
    section[data-testid="stSidebar"] .stTextInput input, 
    section[data-testid="stSidebar"] .stDateInput input {
        background-color: #2B2D35 !important; 
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 8px;
    }

    /* BOUTON ROUGE RAM */
    div.stButton > button:first-child {
        background-color: #C2002F !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        padding: 12px 20px !important;
        border: none !important;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    div.stButton > button:first-child:hover {
        background-color: #A00026 !important;
        transform: translateY(-2px);
    }

    /* --- CARTE DE VOL (Design Blanc pur) --- */
    .flight-card {
        background-color: #ffffff;
        border-radius: 20px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.08);
        overflow: hidden;
        margin-top: 20px;
        border-top: 8px solid #C2002F;
        color: #333333; /* Force le texte en noir */
    }

    .card-header-strip {
        background-color: #fff;
        padding: 20px 30px;
        border-bottom: 1px solid #f0f0f0;
        text-align: center;
    }

    .flight-num-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #C2002F;
        margin: 0;
        line-height: 1.2;
    }

    .card-body {
        padding: 30px 40px;
    }

    /* Aéroports (Ligne CMN -> JFK) */
    .route-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 40px;
    }
    .airport-group {
        text-align: center;
        flex: 1;
    }
    .airport-code {
        font-size: 3.5rem;
        font-weight: 800;
        color: #111;
        line-height: 1;
    }
    .airport-label {
        font-size: 0.85rem;
        color: #666;
        font-weight: 600;
        text-transform: uppercase;
        margin-top: 5px;
        letter-spacing: 1px;
    }
    .plane-icon {
        font-size: 2rem;
        color: #C2002F;
        flex: 0.5;
        text-align: center;
    }

    /* Badge Statut */
    .status-wrapper {
        display: flex;
        justify-content: center;
        margin-bottom: 40px;
    }
    .status-pill {
        padding: 10px 30px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    /* Couleurs Badges */
    .bg-green { background-color: #E6F4EA; color: #1E8E3E; border: 1px solid #CEEAD6; }
    .bg-red { background-color: #FCE8E6; color: #C5221F; border: 1px solid #FAD2CF; }
    .bg-grey { background-color: #F1F3F4; color: #5F6368; border: 1px solid #E0E0E0; }

    /* Grille Horaires (Flexbox pour Centrage parfait) */
    .times-container {
        display: flex;
        justify-content: space-between;
        padding-top: 20px;
        border-top: 1px solid #f5f5f5;
    }

    .time-col {
        display: flex;
        flex-direction: column;
        align-items: center; /* C'est ICI que ça centre tout verticalement */
        width: 48%;
    }

    .time-title {
        font-size: 0.75rem;
        color: #999;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    .time-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #222;
        margin-bottom: 5px;
    }
    .time-sub {
        font-size: 0.9rem;
        font-weight: 600;
    }
    .text-ok { color: #28a745; }
    .text-late { color: #dc3545; }
    .text-warn { color: #e67e22; }

    </style>
""", unsafe_allow_html=True)

# --- LOGO EN HAUT ---
st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Royal_Air_Maroc_logo.svg/800px-Royal_Air_Maroc_logo.svg.png" width="220" alt="Logo RAM">
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## ✈️ RECHERCHE")
    st.markdown("Suivez votre vol en temps réel.")

    # Inputs
    flight_number_input = st.text_input("N° de Vol", value="AT200", placeholder="Ex: AT200")
    date_vol = st.date_input("Date de départ", datetime.now())

    st.markdown("<br>", unsafe_allow_html=True)

    # Bouton
    search_btn = st.button("VOIR LE STATUT")

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.caption("© Royal Air Maroc 2025 (Unofficial)")

# --- LOGIQUE ---
if search_btn:
    code = flight_number_input.replace(" ", "").upper()
    if not code.startswith("AT") and code.isdigit():
        code = f"AT{code}"
    date_str = date_vol.strftime("%Y-%m-%d")

    with st.spinner('Interrogation satellite en cours...'):
        try:
            data = get_flight_data(code, date_str)

            if "Vol non trouvé" in data.get("status", ""):
                st.error("❌ Vol introuvable. Vérifiez le numéro et la date.")
            elif "Erreur" in data.get("status", ""):
                st.error(f"⚠️ Erreur technique : {data['status']}")
            else:
                # --- PRÉPARATION DES DONNÉES ---

                # Statut global
                statut_raw = data['status'].upper()
                css_status = "bg-green"
                icon = "✅"

                if any(x in statut_raw for x in ["RETARD", "DELAY", "CANCEL"]):
                    css_status = "bg-red"
                    icon = "⚠️"
                elif any(x in statut_raw for x in ["PRÉVU", "SCHEDULED"]):
                    css_status = "bg-grey"
                    icon = "🕒"

                # Override si retard > 15min
                dep_delay = data['departure']['delay_min']
                if dep_delay and dep_delay > 15:
                    css_status = "bg-red"
                    icon = "⚠️"
                    statut_raw = f"RETARD (+{dep_delay}min)"


                # Sous-titres (Retard/À l'heure)
                def get_sub_html(delay, actual):
                    if delay and delay > 0:
                        return f'<div class="time-sub text-late">Estimé: {actual} (+{delay}m)</div>'
                    elif actual != "N/A":
                        return '<div class="time-sub text-ok">À l\'heure</div>'
                    return ''


                sub_dep = get_sub_html(data['departure']['delay_min'], data['departure']['actual'])
                sub_arr = get_sub_html(data['arrival']['delay_min'], data['arrival']['actual'])

                # --- GÉNÉRATION HTML (SANS INDENTATION POUR CORRIGER LE BUG) ---
                # Nous utilisons textwrap.dedent pour supprimer l'indentation Python
                # afin que Streamlit ne pense pas que c'est un bloc de code.

                html_code = textwrap.dedent(f"""
                    <div class="flight-card">
                        <div class="card-header-strip">
                            <h1 class="flight-num-title">{code}</h1>
                        </div>

                        <div class="card-body">

                            <div class="route-container">
                                <div class="airport-group">
                                    <div class="airport-code">{data['origin']}</div>
                                    <div class="airport-label">DÉPART</div>
                                </div>
                                <div class="plane-icon">✈</div>
                                <div class="airport-group">
                                    <div class="airport-code">{data['destination']}</div>
                                    <div class="airport-label">ARRIVÉE</div>
                                </div>
                            </div>

                            <div class="status-wrapper">
                                <span class="status-pill {css_status}">
                                    {icon} {statut_raw}
                                </span>
                            </div>

                            <div class="times-container">
                                <div class="time-col">
                                    <div class="time-title">HEURE DE DÉPART</div>
                                    <div class="time-value">{data['departure']['planned']}</div>
                                    {sub_dep}
                                </div>
                                <div class="time-col">
                                    <div class="time-title">HEURE D'ARRIVÉE</div>
                                    <div class="time-value">{data['arrival']['planned']}</div>
                                    {sub_arr}
                                </div>
                            </div>

                        </div>
                    </div>
                """)

                st.markdown(html_code, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")
else:
    st.info("👋 Utilisez le menu à gauche pour chercher un vol.")