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
            st.session_state.stop = False
            st.rerun()
        else:
            st.warning("Bitte tragt alle Namen ein!")

# --- SPIEL LAUFEND ---
elif st.session_state.spielgestartet and not st.session_state.verloren:
    spieler = st.session_state.spieler
    aktueller = spieler[st.session_state.aktiver_spieler]
    st.subheader(f"🔔 {aktueller} ist dran!")

    # Farben nach Spieleranzahl
    farben_dict = {
        2: ["#ff4b4b", "#4b8bff"],  # rot, blau
        3: ["#ff4b4b", "#4b8bff", "#36d67c"],  # rot, blau, grün
        4: ["#ff4b4b", "#4b8bff", "#36d67c", "#ffd93d"],  # rot, blau, grün, gelb
        5: ["#ff4b4b", "#4b8bff", "#36d67c", "#ffd93d", "#ff4bf0"],  # rot, blau, grün, gelb, pink
    }
    farben = farben_dict.get(len(spieler), ["#ff4b4b", "#4b8bff"])  # Fallback auf rot/blau
    farbe = farben[st.session_state.aktiver_spieler % len(farben)]

    zeitlimit = 10  # Sekunden pro Runde
    platzhalter = st.empty()
    startzeit = time.time()

    # --- Laufender Balken (animiert) ---
    while True:
        if st.session_state.stop:
            break

        verstrichen = time.time() - startzeit
        fortschritt = max(0, 1 - verstrichen / zeitlimit)

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
        platzhalter.markdown(balken_html, unsafe_allow_html=True)
        time.sleep(0.1)

        if verstrichen >= zeitlimit:
            break

    # --- Wenn Zeit vorbei ist → nächster Spieler ---
    if not st.session_state.stop:
        st.session_state.aktiver_spieler = (st.session_state.aktiver_spieler + 1) % len(spieler)
        st.rerun()

    # --- Knopf unten anzeigen ---
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
    if st.button(f"❌ {aktueller} hat eine richtige Antwort gesagt!"):
        st.session_state.verloren = aktueller
        st.session_state.spielgestartet = False
        st.session_state.stop = True
        st.rerun()

# --- VERLOREN BILDSCHIRM ---
elif st.session_state.verloren:
    st.error(f"💥 {st.session_state.verloren} hat verloren!")
    if st.button("🔁 Neues Spiel starten"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
