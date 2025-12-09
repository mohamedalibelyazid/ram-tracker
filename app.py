import streamlit as st
from datetime import datetime
# Assurez-vous d'avoir votre fichier scraper.py
from scraper import get_flight_data

# --- CONFIGURATION PAGE ---
st.set_page_config(
    page_title="Suivi de Vol | Royal Air Maroc",
    page_icon="🇲🇦",
    layout="centered"
)

# --- CSS CORRECTIF (DESIGN DARK & CONTRASTE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800&display=swap');

    /* Global Font */
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    /* Fond principal de l'app (Zone de droite) */
    .stApp {
        background-color: #F4F6F9;
        color: #333;
    }

    /* --- SIDEBAR STYLE (Rouge Très Foncé / Bordeaux) --- */
    section[data-testid="stSidebar"] {
        background-color: #6d071a; /* Rouge très foncé pour le fond */
    }

    /* Couleur des textes génériques dans la sidebar (Titres, labels) */
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
    /* Fond NOIR, Texte BLANC */
    section[data-testid="stSidebar"] .stTextInput input, 
    section[data-testid="stSidebar"] .stDateInput input {
        background-color: #000000 !important; /* Fond noir strict */
        color: #FFFFFF !important; /* Texte blanc */
        border: 1px solid #8e2b3e !important; /* Bordure discrète */
        border-radius: 8px;
    }

    /* Correction de l'icône calendrier (la mettre en blanc) */
    section[data-testid="stSidebar"] [data-testid="stDateInput"] svg {
        fill: white !important;
    }

    /* --- BOUTON DE RECHERCHE --- */
    /* Fond BLANC, Texte ROUGE FONCÉ */
    section[data-testid="stSidebar"] .stButton button {
        background-color: #FFFFFF !important;
        color: #8A0021 !important; /* C'est ici qu'on corrige le blanc sur blanc */
        font-weight: 800 !important;
        border: none !important;
        padding: 15px 20px !important;
        width: 100%;
        text-transform: uppercase;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        transform: scale(1.02);
        background-color: #f0f0f0 !important;
        color: #C2002F !important; /* Devient rouge plus vif au survol */
    }

    /* --- ESTHÉTIQUE DE LA CARTE DE RÉSULTAT (À DROITE) --- */
    .flight-card {
        background: white;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        overflow: hidden;
        margin-top: 20px;
        border-top: 6px solid #C2002F;
    }
    .card-header {
        background-color: #fff;
        padding: 15px 20px;
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 1px dashed #ddd;
    }
    .flight-num { font-size: 1.5rem; font-weight: 800; color: #C2002F; letter-spacing: 1px; }
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

# --- LOGO PRINCIPAL ---
st.markdown("""
    <div style="text-align: center; padding-bottom: 20px; margin-bottom: 20px; border-bottom: 2px solid #E5E7EB;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Logo_Royal_Air_Maroc.svg/2560px-Logo_Royal_Air_Maroc.svg.png" width="200" alt="Logo RAM">
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTENU ---
with st.sidebar:
    st.markdown("## ✈️ MON VOL")
    st.markdown("Recherchez le statut de votre vol en temps réel.")

    # Inputs (Fond Noir / Texte Blanc grâce au CSS)
    flight_number_input = st.text_input("N° de Vol", value="AT200", placeholder="Ex: AT200")
    date_vol = st.date_input("Date de départ", datetime.now())

    st.markdown("<br>", unsafe_allow_html=True)

    # Bouton (Fond Blanc / Texte Rouge grâce au CSS)
    search_btn = st.button("RECHERCHER LE VOL")

    st.markdown(
        "<div style='margin-top: 50px; font-size: 0.8em; opacity: 0.7; color: white;'>© Royal Air Maroc 2025<br>Support Client</div>",
        unsafe_allow_html=True)

# --- LOGIQUE ---
if search_btn:
    code = flight_number_input.replace(" ", "").upper()
    if not code.startswith("AT") and code.isdigit():
        code = f"AT{code}"
    date_str = date_vol.strftime("%Y-%m-%d")

    with st.spinner('Connexion aux serveurs...'):
        try:
            data = get_flight_data(code, date_str)

            if "Vol non trouvé" in data.get("status", ""):
                st.error("❌ Vol introuvable. Vérifiez le numéro et la date.")
            elif "Erreur" in data.get("status", ""):
                st.error(f"⚠️ Erreur: {data['status']}")
            else:
                # --- AFFICHAGE CARTE ---
                # Logique simplifiée pour les couleurs
                statut_txt = data['status'].upper()
                css_badge = "status-green"
                icon = "✅"

                if "RETARD" in statut_txt or "DELAYED" in statut_txt:
                    css_badge = "status-red"
                    icon = "⚠️"


                # HTML Helpers
                def time_html(planned, actual, delay):
                    if delay and delay > 0:
                        return f'<div class="time-big">{planned}</div><div class="text-red">Estimé: {actual} (+{delay}m)</div>'
                    return f'<div class="time-big">{planned}</div><div class="text-green">À l\'heure</div>'


                html_dep = time_html(data['departure']['planned'], data['departure']['actual'],
                                     data['departure']['delay_min'])
                html_arr = time_html(data['arrival']['planned'], data['arrival']['actual'],
                                     data['arrival']['delay_min'])

                st.markdown(f"""
                <div class="flight-card">
                    <div class="card-header">
                        <div class="flight-num">{code}</div>
                        <div style="color:#666;">{date_vol.strftime('%d %B %Y')}</div>
                    </div>
                    <div class="card-body">
                        <div class="route-container">
                            <div><div class="airport-code">{data['origin']}</div><small>DÉPART</small></div>
                            <div style="color:#C2002F; font-size:2rem;">✈</div>
                            <div><div class="airport-code">{data['destination']}</div><small>ARRIVÉE</small></div>
                        </div>

                        <span class="status-badge {css_badge}">{icon} {statut_txt}</span>

                        <div class="times-grid">
                            <div><div class="time-label">DÉPART</div>{html_dep}</div>
                            <div><div class="time-label">ARRIVÉE</div>{html_arr}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erreur technique : {e}")
else:
    st.info("Entrez un numéro de vol dans le menu latéral pour commencer.")