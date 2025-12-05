import streamlit as st
from datetime import datetime
# On importe directement notre fonction de scraping
from scraper import get_flight_data

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="RAM Flight Tracker", page_icon="✈️", layout="centered")

st.markdown("""
    <style>
    .status-box { padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; color: white;}
    .status-ok { background-color: #28a745; }
    .status-late { background-color: #dc3545; }
    .status-wait { background-color: #17a2b8; }
    .status-err { background-color: #6c757d; }
    </style>
""", unsafe_allow_html=True)

st.title("✈️ RAM Live Tracker")
st.markdown("Suivi des vols Royal Air Maroc en temps réel.")

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.header("Paramètres")
    flight_number = st.text_input("Numéro de Vol", value="AT200")
    date_vol = st.date_input("Date du vol", datetime.now())
    search_btn = st.button("Rechercher 🔍", type="primary")

# --- LOGIQUE ---
if search_btn:
    # Nettoyage Code Vol
    code = flight_number.replace(" ", "").upper()
    if not code.startswith("AT") and code.isdigit():
        code = f"AT{code}"

    date_str = date_vol.strftime("%Y-%m-%d")

    with st.spinner(f"📡 Connexion satellite vers le vol {code}..."):
        # APPEL DIRECT DE LA FONCTION (Pas d'API nécessaire)
        data = get_flight_data(code, date_str)

        if "Vol non trouvé" in data.get("status", ""):
            st.error(f"❌ {data['status']}")
        else:
            # A. En-tête
            c1, c2, c3 = st.columns([2, 1, 2])
            c1.markdown(f"<div style='text-align:center'><h2>{data['origin']}</h2><small>Origine</small></div>",
                        unsafe_allow_html=True)
            c2.markdown("<h1 style='text-align:center; color:gray'>➝</h1>", unsafe_allow_html=True)
            c3.markdown(
                f"<div style='text-align:center'><h2>{data['destination']}</h2><small>Destination</small></div>",
                unsafe_allow_html=True)

            st.divider()

            # B. Statut
            statut = data['status']
            color = "status-wait"
            if "atterri" in statut.lower() or "landed" in statut.lower():
                color = "status-ok"
            elif data['departure']['delay_min'] is not None and data['departure']['delay_min'] > 15:
                color = "status-late"

            st.markdown(f'<div class="status-box {color}"><h3>{statut}</h3></div>', unsafe_allow_html=True)

            # C. Horaires
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🛫 Décollage")
                st.text(f"Prévu : {data['departure']['planned']}")
                dep_delay = data['departure']['delay_min']
                d_col = "inverse" if dep_delay and dep_delay > 0 else "normal"
                st.metric("Réel", data['departure']['actual'], delta=f"{dep_delay} min" if dep_delay else None,
                          delta_color=d_col)

            with col2:
                st.subheader("🛬 Atterrissage")
                st.text(f"Prévu : {data['arrival']['planned']}")
                arr_delay = data['arrival']['delay_min']
                a_col = "inverse" if arr_delay and arr_delay > 0 else "normal"
                st.metric("Réel", data['arrival']['actual'], delta=f"{arr_delay} min" if arr_delay else None,
                          delta_color=a_col)

            st.caption(f"Source: {data['url']}")