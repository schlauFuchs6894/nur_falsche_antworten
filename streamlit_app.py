import streamlit as st
import time

st.set_page_config(page_title="Nur falsche Antworten", page_icon="🎯", layout="centered")

st.title("🎯 Nur falsche Antworten – Das Spiel")

# --- SESSION STATE INITIALISIERUNG ---
if "spieler" not in st.session_state:
    st.session_state.spieler = []
if "aktiver_spieler" not in st.session_state:
    st.session_state.aktiver_spieler = 0
if "spielgestartet" not in st.session_state:
    st.session_state.spielgestartet = False
if "verloren" not in st.session_state:
    st.session_state.verloren = None
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None

# --- SPIELSETUP ---
if not st.session_state.spielgestartet and not st.session_state.verloren:
    st.header("🧑‍🤝‍🧑 Wie viele Spieler seid ihr?")
    anzahl = st.number_input("Anzahl Spieler", min_value=2, max_value=10, step=1)

    namen = []
    for i in range(int(anzahl)):
        name = st.text_input(f"Name von Spieler {i+1}", key=f"name_{i}")
        namen.append(name)

    if st.button("🎬 Spiel starten"):
        if all(namen):
            st.session_state.spieler = namen
            st.session_state.spielgestartet = True
            st.session_state.timer_start = time.time()
            st.rerun()
        else:
            st.warning("❗ Bitte tragt alle Namen ein!")

# --- SPIEL LAUFEND ---
elif st.session_state.spielgestartet and not st.session_state.verloren:
    spieler = st.session_state.spieler
    aktueller_index = st.session_state.aktiver_spieler
    aktueller = spieler[aktueller_index]

    st.subheader(f"🔔 {aktueller} ist dran!")

    # --- Farbrotation ---
    farben_dict = {
        2: ["#ff4b4b", "#4b8bff"],
        3: ["#ff4b4b", "#4b8bff", "#36d67c"],
        4: ["#ff4b4b", "#4b8bff", "#36d67c", "#ffd93d"],
        5: ["#ff4b4b", "#4b8bff", "#36d67c", "#ffd93d", "#ff4bf0"],
    }
    farben = farben_dict.get(len(spieler), ["#ff4b4b", "#4b8bff"])
    farbe = farben[aktueller_index % len(farben)]

    zeitlimit = 10
    verstrichen = time.time() - st.session_state.timer_start
    fortschritt = max(0, 1 - verstrichen / zeitlimit)

    # --- Fortschrittsbalken (HTML, für Farbe) ---
    balken_html = f"""
    <div style='width: 100%; background-color: #ddd; border-radius: 10px; height: 25px; margin-top: 30px;'>
        <div style='width: {fortschritt*100}%;
                    background-color: {farbe};
                    height: 25px;
                    border-radius: 10px;
                    transition: width 0.1s linear;'>
        </div>
    </div>
    """
    st.markdown(balken_html, unsafe_allow_html=True)

    # --- Countdown-Zahl ---
    restzeit = int(max(0, zeitlimit - verstrichen))
    st.markdown(f"<h4 style='text-align:center;'>⏳ Noch {restzeit} Sekunden</h4>", unsafe_allow_html=True)

    # --- Button unten ---
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
    if st.button(f"❌ {aktueller} hat eine richtige Antwort gesagt!"):
        st.session_state.verloren = aktueller
        st.session_state.spielgestartet = False
        st.rerun()

    # --- Wenn Zeit abgelaufen ist → nächster Spieler ---
    if verstrichen >= zeitlimit:
        st.session_state.aktiver_spieler = (aktueller_index + 1) % len(spieler)
        st.session_state.timer_start = time.time()
        st.rerun()

# --- VERLOREN BILDSCHIRM ---
elif st.session_state.verloren:
    st.error(f"💥 {st.session_state.verloren} hat verloren!")
    if st.button("🔁 Neues Spiel starten"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
