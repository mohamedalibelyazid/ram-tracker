import streamlit as st
from datetime import datetime
# Import du scraper (Assurez-vous que le fichier scraper.py existe bien dans le même dossier)
from scraper import get_flight_data

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Suivi de Vol | Royal Air Maroc",
    page_icon="🇲🇦",
    layout="centered"
)

# --- ESTHÉTIQUE RAM (CSS AVANCÉ) ---
st.markdown("""
    <style>
    /* Import de la police Montserrat (proche de Museo Sans, la police RAM) */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800&display=swap');

    /* Reset global */
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        color: #4A4A4A;
    }

    /* Fond de l'application */
    .stApp {
        background-color: #F9FAFB;
    }

    /* --- SIDEBAR STYLE (Rouge RAM) --- */
    section[data-testid="stSidebar"] {
        background-color: #C2002F; /* Rouge RAM */
    }

    /* Textes dans la sidebar en blanc */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: white !important;
    }

    /* Inputs dans la sidebar */
    section[data-testid="stSidebar"] input {
        color: #333 !important;
        border-radius: 4px;
        border: none;
    }

    /* Bouton Sidebar */
    section[data-testid="stSidebar"] button {
        background-color: white !important;
        color: #C2002F !important;
        font-weight: 700 !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    section[data-testid="stSidebar"] button:hover {
        background-color: #f0f0f0 !important;
        transform: scale(1.02);
    }

    /* --- HEADER PRINCIPAL --- */
    .ram-logo-container {
        text-align: center;
        padding-bottom: 20px;
        margin-bottom: 20px;
        border-bottom: 2px solid #E5E7EB;
    }

    /* --- CARTE DE RÉSULTAT (Style Boarding Pass) --- */
    .flight-card {
        background: white;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        overflow: hidden;
        margin-top: 20px;
        border-top: 6px solid #C2002F;
    }

    /* En-tête de la carte (Numéro de vol) */
    .card-header {
        background-color: #fff;
        padding: 15px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px dashed #ddd;
    }
    .flight-num {
        font-size: 1.5rem;
        font-weight: 800;
        color: #C2002F;
        letter-spacing: 1px;
    }
    .flight-date {
        color: #888;
        font-size: 0.9rem;
        font-weight: 500;
    }

    /* Corps de la carte (Trajet) */
    .card-body {
        padding: 30px 20px;
        text-align: center;
    }

    .route-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
    }

    .airport-code {
        font-size: 2.8rem;
        font-weight: 700;
        color: #1F2937;
        line-height: 1;
    }
    .airport-name {
        font-size: 0.8rem;
        text-transform: uppercase;
        color: #6B7280;
        margin-top: 5px;
        letter-spacing: 0.5px;
    }

    /* Icône avion animée ou fixe au milieu */
    .plane-icon {
        color: #C2002F;
        font-size: 1.5rem;
        padding: 0 10px;
    }

    /* --- STATUT ET HORAIRES --- */
    .status-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 25px;
    }

    .status-green { background-color: #DEF7EC; color: #03543F; }
    .status-red { background-color: #FDE8E8; color: #9B1C1C; }
    .status-yellow { background-color: #FDF6B2; color: #723B13; }
    .status-neutral { background-color: #F3F4F6; color: #374151; }

    /* Grille Horaires */
    .times-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        text-align: center;
        border-top: 1px solid #F3F4F6;
        padding-top: 20px;
    }
    .time-big {
        font-size: 1.8rem;
        font-weight: 700;
        color: #111;
    }
    .time-label {
        font-size: 0.75rem;
        color: #9CA3AF;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .delay-info {
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 4px;
    }
    .text-green { color: #059669; }
    .text-red { color: #DC2626; }

    /* Footer discret */
    .footer-note {
        text-align: center;
        font-size: 0.75rem;
        color: #9CA3AF;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGO EN HAUT DE PAGE ---
st.markdown("""
    <div class="ram-logo-container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Logo_Royal_Air_Maroc.svg/2560px-Logo_Royal_Air_Maroc.svg.png" width="200" alt="Logo RAM">
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR (BARRE DE RECHERCHE) ---
with st.sidebar:
    st.markdown("## ✈️ MON VOL")
    st.markdown("Recherchez le statut de votre vol en temps réel.")

    # Inputs
    flight_number_input = st.text_input("N° de Vol", value="AT200", placeholder="Ex: AT200")
    date_vol = st.date_input("Date de départ", datetime.now())

    st.markdown("<br>", unsafe_allow_html=True)

    # Le bouton est stylisé par CSS pour être Blanc sur fond Rouge
    search_btn = st.button("RECHERCHER LE VOL")

    st.markdown(
        "<div style='margin-top: 50px; font-size: 0.8em; opacity: 0.8'>© Royal Air Maroc 2025<br>Support Client</div>",
        unsafe_allow_html=True)

# --- LOGIQUE PRINCIPALE ---
if search_btn:
    # Nettoyage de l'input
    code = flight_number_input.replace(" ", "").upper()
    if not code.startswith("AT") and code.isdigit():
        code = f"AT{code}"  # Ajoute AT si l'utilisateur met juste "200"

    date_str = date_vol.strftime("%Y-%m-%d")

    # Spinner standard Streamlit
    with st.spinner('Chargement des données de vol...'):
        try:
            # Appel au scraper
            data = get_flight_data(code, date_str)

            # Gestion des erreurs renvoyées par le scraper
            if "Vol non trouvé" in data.get("status", ""):
                st.error("❌ Nous n'avons pas trouvé ce vol. Vérifiez le numéro et la date.")
            elif "Erreur" in data.get("status", ""):
                st.error(f"⚠️ Une erreur technique est survenue : {data['status']}")

            else:
                # --- PRÉPARATION DES DONNÉES D'AFFICHAGE ---
                statut_raw = data['status']
                statut_lower = statut_raw.lower()

                # Logique Couleurs et Icones
                status_class = "status-neutral"
                icon_status = "ℹ️"

                if any(x in statut_lower for x in ["atterri", "landed", "arrivé"]):
                    status_class = "status-green"
                    icon_status = "✅"
                    status_display = "VOL ARRIVÉ"
                elif "en vol" in statut_lower or "en route" in statut_lower:
                    status_class = "status-green"  # En vert ou neutre selon préférence
                    icon_status = "✈️"
                    status_display = "EN VOL"
                elif any(x in statut_lower for x in ["retard", "delayed"]):
                    status_class = "status-red"
                    icon_status = "⚠️"
                    status_display = f"RETARDÉ ({statut_raw})"
                elif "annulé" in statut_lower:
                    status_class = "status-red"
                    icon_status = "🚫"
                    status_display = "VOL ANNULÉ"
                else:
                    status_display = statut_raw.upper()

                # Vérification retard horaire
                dep_delay = data['departure']['delay_min']
                arr_delay = data['arrival']['delay_min']

                # Si retard > 15min détecté numériquement, on force le statut jaune/rouge
                if (dep_delay and dep_delay > 15) or (arr_delay and arr_delay > 15):
                    status_class = "status-red"
                    status_display = "RETARDÉ"


                # Construction HTML du "Delay Text"
                def get_time_html(planned, actual, delay):
                    if delay and delay > 0:
                        return f"""
                            <div class="time-big">{planned}</div>
                            <div class="delay-info text-red">Estimé : {actual} (+{delay}m)</div>
                        """
                    elif actual != "N/A":
                        return f"""
                            <div class="time-big">{planned}</div>
                            <div class="delay-info text-green">À l'heure</div>
                        """
                    else:
                        return f"""<div class="time-big">{planned}</div>"""


                html_dep = get_time_html(data['departure']['planned'], data['departure']['actual'],
                                         data['departure']['delay_min'])
                html_arr = get_time_html(data['arrival']['planned'], data['arrival']['actual'],
                                         data['arrival']['delay_min'])

                # --- RENDU DE LA CARTE HTML ---
                st.markdown(f"""
                <div class="flight-card">
                    <div class="card-header">
                        <div class="flight-num">{code}</div>
                        <div class="flight-date">{date_vol.strftime('%d %B %Y')}</div>
                    </div>

                    <div class="card-body">
                        <div class="route-container">
                            <div style="text-align:left;">
                                <div class="airport-code">{data['origin']}</div>
                                <div class="airport-name">Départ</div>
                            </div>
                            <div class="plane-icon">
                                ✈ &nbsp;-----------------&nbsp; ✈
                            </div>
                            <div style="text-align:right;">
                                <div class="airport-code">{data['destination']}</div>
                                <div class="airport-name">Arrivée</div>
                            </div>
                        </div>

                        <div class="{status_class} status-badge">
                            {icon_status} &nbsp; {status_display}
                        </div>

                        <div class="times-grid">
                            <div>
                                <div class="time-label">Heure de départ</div>
                                {html_dep}
                            </div>
                            <div>
                                <div class="time-label">Heure d'arrivée</div>
                                {html_arr}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown('<div class="footer-note">Les horaires sont affichés en heure locale.</div>',
                            unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Une erreur est survenue lors de la récupération des données : {e}")

else:
    # État vide (avant recherche)
    st.info("Veuillez saisir votre numéro de vol dans le menu latéral (ex: AT200) pour afficher les détails.")