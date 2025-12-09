import streamlit as st
from datetime import datetime
# Import du scraper
from scraper import get_flight_data

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Suivi de Vol | Royal Air Maroc",
    page_icon="🇲🇦",
    layout="centered"
)

# --- CSS CORRIGÉ (DESIGN DARK RED & CONTRASTE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800&display=swap');

    /* Reset global */
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    /* Fond de l'application (partie droite) */
    .stApp {
        background-color: #F4F6F9;
        color: #333;
    }

    /* --- SIDEBAR STYLE (Rouge Très Foncé) --- */
    section[data-testid="stSidebar"] {
        background-color: #8A0021; /* Rouge Bordeaux Profond */
    }

    /* TOUS les textes de la sidebar en BLANC */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] span {
        color: #FFFFFF !important;
    }

    /* --- CHAMPS DE SAISIE (INPUTS) --- */
    /* Fond NOIR, Texte BLANC, Bordure Rouge/Blanche */
    section[data-testid="stSidebar"] .stTextInput input, 
    section[data-testid="stSidebar"] .stDateInput input {
        background-color: #1E1E1E !important; /* Fond noir */
        color: #FFFFFF !important; /* Texte blanc */
        border: 1px solid #B03045 !important; /* Bordure rouge discret */
        border-radius: 8px;
    }

    /* Icône calendrier dans le DateInput */
    section[data-testid="stSidebar"] [data-testid="stDateInput"] svg {
        fill: white !important;
    }

    /* --- BOUTON DE RECHERCHE --- */
    /* Fond BLANC, Texte ROUGE FONCÉ (pour contraste max) */
    section[data-testid="stSidebar"] .stButton button {
        background-color: #FFFFFF !important;
        color: #8A0021 !important; /* Texte couleur Sidebar */
        font-weight: 800 !important;
        border: none !important;
        padding: 15px 20px !important;
        text-transform: uppercase;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        transform: scale(1.03);
        background-color: #F0F0F0 !important;
    }

    /* --- CARTE DE RÉSULTAT (Maintien du design propre) --- */
    .flight-card {
        background: white;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        overflow: hidden;
        margin-top: 20px;
        border-top: 6px solid #8A0021;
    }
    .card-header {
        background-color: #fff;
        padding: 15px 20px;
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 1px dashed #ddd;
    }
    .flight-num { font-size: 1.5rem; font-weight: 800; color: #8A0021; letter-spacing: 1px; }
    .card-body { padding: 30px 20px; text-align: center; }
    .route-container { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
    .airport-code { font-size: 2.8rem; font-weight: 700; color: #1F2937; line-height: 1; }
    .status-badge { display: inline-block; padding: 6px 16px; border-radius: 50px; font-weight: 700; text-transform: uppercase; margin-bottom: 25px; }
    .status-green { background-color: #DEF7EC; color: #03543F; }
    .status-red { background-color: #FDE8E8; color: #9B1C1C; }
    .times-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; text-align: center; border-top: 1px solid #F3F4F6; padding-top: 20px; }
    .time-big { font-size: 1.8rem; font-weight: 700; color: #111; }
    .time-label { font-size: 0.75rem; color: #9CA3AF; text-transform: uppercase; font-weight: 600; }
    .text-red { color: #DC2626; font-size: 0.85rem; font-weight: 600; }
    .text-green { color: #059669; font-size: 0.85rem; font-weight: 600; }

    </style>
""", unsafe_allow_html=True)

# --- LOGO ---
st.markdown("""
    <div style="text-align: center; padding-bottom: 20px; margin-bottom: 20px; border-bottom: 2px solid #E5E7EB;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Logo_Royal_Air_Maroc.svg/2560px-Logo_Royal_Air_Maroc.svg.png" width="200" alt="Logo RAM">
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## ✈️ MON VOL")
    st.markdown("Recherchez le statut de votre vol en temps réel.")

    # Inputs (Maintenant sur fond noir)
    flight_number_input = st.text_input("N° de Vol", value="AT200", placeholder="Ex: AT200")
    date_vol = st.date_input("Date de départ", datetime.now())

    st.markdown("<br>", unsafe_allow_html=True)

    # Bouton (Blanc texte rouge)
    search_btn = st.button("RECHERCHER LE VOL")

    st.markdown(
        "<div style='margin-top: 50px; font-size: 0.8em; opacity: 0.8; color: white;'>© Royal Air Maroc 2025<br>Support Client</div>",
        unsafe_allow_html=True)

# --- LOGIQUE PRINCIPALE ---
if search_btn:
    code = flight_number_input.replace(" ", "").upper()
    if not code.startswith("AT") and code.isdigit():
        code = f"AT{code}"
    date_str = date_vol.strftime("%Y-%m-%d")

    with st.spinner('Chargement des données...'):
        try:
            data = get_flight_data(code, date_str)

            if "Vol non trouvé" in data.get("status", ""):
                st.error("❌ Vol introuvable. Vérifiez le numéro.")
            elif "Erreur" in data.get("status", ""):
                st.error(f"⚠️ Erreur: {data['status']}")
            else:
                # Logique Statut
                statut_raw = data['status']
                css_status = "status-green"
                icon = "✅"
                text_status = "À L'HEURE / ARRIVÉ"

                if "retard" in statut_raw.lower() or "delayed" in statut_raw.lower():
                    css_status = "status-red"
                    icon = "⚠️"
                    text_status = "RETARDÉ"

                # Check retard > 15min
                if (data['departure']['delay_min'] and data['departure']['delay_min'] > 15):
                    css_status = "status-red"
                    icon = "⚠️"
                    text_status = "RETARDÉ"


                # Helpers HTML
                def render_time(planned, actual, delay):
                    if delay and delay > 0:
                        return f'<div class="time-big">{planned}</div><div class="text-red">Estimé: {actual} (+{delay}m)</div>'
                    return f'<div class="time-big">{planned}</div><div class="text-green">À l\'heure</div>'


                html_dep = render_time(data['departure']['planned'], data['departure']['actual'],
                                       data['departure']['delay_min'])
                html_arr = render_time(data['arrival']['planned'], data['arrival']['actual'],
                                       data['arrival']['delay_min'])

                # Rendu Carte
                st.markdown(f"""
                <div class="flight-card">
                    <div class="card-header">
                        <div class="flight-num">{code}</div>
                        <div style="color:#666;">{date_vol.strftime('%d %B %Y')}</div>
                    </div>
                    <div class="card-body">
                        <div class="route-container">
                            <div><div class="airport-code">{data['origin']}</div><small>DÉPART</small></div>
                            <div style="color:#8A0021; font-size:2rem;">✈</div>
                            <div><div class="airport-code">{data['destination']}</div><small>ARRIVÉE</small></div>
                        </div>
                        <span class="status-badge {css_status}">{icon} {text_status}</span>
                        <div class="times-grid">
                            <div><div class="time-label">DÉPART</div>{html_dep}</div>
                            <div><div class="time-label">ARRIVÉE</div>{html_arr}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erreur : {e}")
else:
    st.info("👋 Bienvenue. Veuillez entrer un numéro de vol à gauche.")