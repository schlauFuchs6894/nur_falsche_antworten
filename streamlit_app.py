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
if "stop" not in st.session_state:
    st.session_state.stop = False

# --- SPIELSETUP ---
if not st.session_state.spielgestartet:
    st.header("🧑‍🤝‍🧑 Wie viele Spieler seid ihr?")
    anzahl = st.number_input("Anzahl Spieler", min_value=2, max_value=10, step=1)

    namen = []
    for i in range(int(anzahl)):
        name = st.text_input(f"Name von Spieler {i+1}")
        namen.append(name)

    if st.button("🎬 Spiel starten"):
        if all(namen):
            st.session_state.spieler = namen
            st.session_state.spielgestartet = True
            st.session_state.stop = False
        else:
            st.warning("Bitte tragt alle Namen ein!")

# --- SPIEL LAUFEND ---
else:
    spieler = st.session_state.spieler
    aktueller = spieler[st.session_state.aktiver_spieler]
    st.subheader(f"🔔 {aktueller} ist dran!")

    # Balkenfarbe abwechselnd rot / blau / rot / blau ...
    farben = ["#ff4b4b", "#4b8bff"]  # Rot / Blau
    farbe = farben[st.session_state.aktiver_spieler % 2]

    zeitlimit = 10  # Sekunden pro Runde
    platzhalter = st.empty()
    startzeit = time.time()

    # Button sofort anzeigen
    if st.button(f"❌ {aktueller} hat eine richtige Antwort gesagt!"):
        st.session_state.verloren = aktueller
        st.session_state.spielgestartet = False
        st.session_state.stop = True
        st.rerun()

    # Laufender Balken
    while time.time() - startzeit < zeitlimit:
        if st.session_state.stop:
            break
        verstrichen = time.time() - startzeit
        fortschritt = max(0, 1 - verstrichen / zeitlimit)

        # HTML-basierten Balken anzeigen (damit wir Farbe ändern können)
        balken_html = f"""
        <div style='width: 100%; background-color: #ddd; border-radius: 10px; height: 25px;'>
            <div style='width: {fortschritt*100}%;
                        background-color: {farbe};
                        height: 25px;
                        border-radius: 10px;
                        transition: width 0.1s linear;'>
            </div>
        </div>
        """
        platzhalter.markdown(balken_html, unsafe_allow_html=True)
        time.sleep(0.1)

    # Wenn der Timer abgelaufen ist und niemand verloren hat
    if not st.session_state.stop:
        st.session_state.aktiver_spieler = (st.session_state.aktiver_spieler + 1) % len(spieler)
        st.rerun()

# --- VERLOREN BILDSCHIRM ---
if st.session_state.verloren:
    st.error(f"💥 {st.session_state.verloren} hat verloren!")
    if st.button("🔁 Neues Spiel starten"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
