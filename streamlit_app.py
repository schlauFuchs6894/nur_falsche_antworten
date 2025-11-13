import streamlit as st
import time

st.set_page_config(page_title="Nur falsche Antworten", page_icon="🎯", layout="centered")

# --- SPIELSETUP ---
st.title("🎯 Nur falsche Antworten – Das Spiel")

# Anzahl der Spieler festlegen
if "spieler" not in st.session_state:
    st.session_state.spieler = []
if "aktiver_spieler" not in st.session_state:
    st.session_state.aktiver_spieler = 0
if "spielgestartet" not in st.session_state:
    st.session_state.spielgestartet = False
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None
if "verloren" not in st.session_state:
    st.session_state.verloren = None

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
            st.session_state.timer_start = time.time()
        else:
            st.warning("Bitte tragt alle Namen ein!")

else:
    spieler = st.session_state.spieler
    aktueller = spieler[st.session_state.aktiver_spieler]

    st.subheader(f"🔔 {aktueller} ist dran!")
    zeitlimit = 10  # Sekunden pro Spieler

    # Timer-Balken
    verstrichen = time.time() - st.session_state.timer_start
    fortschritt = max(0, 1 - verstrichen / zeitlimit)
    st.progress(fortschritt)

    # Wenn der Timer abgelaufen ist → Nächster Spieler
    if verstrichen >= zeitlimit:
        st.session_state.aktiver_spieler = (st.session_state.aktiver_spieler + 1) % len(spieler)
        st.session_state.timer_start = time.time()
        st.rerun()

    # Wenn der Spieler „eine richtige Antwort“ sagt
    if st.button(f"❌ {aktueller} hat eine richtige Antwort gesagt!"):
        st.session_state.verloren = aktueller
        st.session_state.spielgestartet = False
        st.rerun()

# Wenn jemand verloren hat
if st.session_state.verloren:
    st.error(f"💥 {st.session_state.verloren} hat verloren!")
    if st.button("🔁 Neues Spiel starten"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

