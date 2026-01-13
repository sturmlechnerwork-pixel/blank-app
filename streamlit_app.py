import streamlit as st
import pandas as pd

# --- LOGIN FUNKTION ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # Login-Maske anzeigen
    st.set_page_config(page_title="Zeus Login", page_icon="🔒")
    st.title("⚡ Zeus Production - Intern")
    password = st.text_input("Bitte Passwort eingeben", type="password")
    
    # Hier euer Passwort ändern:
    Richtiges_Passwort = "zeus2026" 

    if st.button("Einloggen"):
        if password == Richtiges_Passwort:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Passwort falsch")
    return False

# --- HAUPTPROGRAMM ---
if check_password():
    # AB HIER DEIN BESTEHENDER DASHBOARD-CODE
    st.set_page_config(layout="wide", page_title="Zeus Cockpit")
    st.title("⚡ Zeus Production Dashboard")
    
    # Beispiel-Daten (hier kommen eure echten Daten hin)
    data = {
        'Projekt': ['Image-Film', 'Social Ads', 'Branding'],
        'Status': ['In Produktion', 'Abgeschlossen', 'Planung'],
        'Deadline': ['20.01.2026', '12.01.2026', '05.02.2026']
    }
    df = pd.DataFrame(data)
    st.table(df)
