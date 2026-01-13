import streamlit as st
import pandas as pd

# --- ZEUS BRANDING (ECHTER LOOK) ---
def apply_zeus_branding():
    st.markdown("""
        <style>
        /* Hintergrund auf echtes Schwarz setzen */
        .stApp {
            background-color: #000000;
        }
        /* Alle Texte in cleanem Weiß */
        [data-testid="stMarkdownContainer"] p, h1, h2, h3 {
            color: #FFFFFF !important;
            font-family: 'Inter', sans-serif;
        }
        /* Tabellen-Styling: Minimalistisch & Silberne Linien */
        .stTable {
            border: 1px solid #333333;
            border-radius: 4px;
            background-color: #0A0A0A;
        }
        /* Button-Styling: Dezent, kein grelles Gelb */
        div.stButton > button:first-child {
            background-color: #FFFFFF;
            color: #000000;
            border-radius: 2px;
            border: none;
            padding: 0.5rem 2rem;
        }
        /* Input Felder anpassen */
        input {
            background-color: #111111 !important;
            color: white !important;
            border: 1px solid #333333 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# --- LOGIN ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True

    st.set_page_config(page_title="Zeus Cockpit | Login", page_icon="⚪")
    apply_zeus_branding()
    
    st.write(" ") # Abstand
    st.markdown("<h2 style='text-align: center; letter-spacing: 2px;'>ZEUS PRODUCTION</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Internal Production Cockpit</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        password = st.text_input("ACCESS CODE", type="password")
        if st.button("ENTER"):
            if password == "zeus2026":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Invalid Code")
    return False

# --- MAIN DASHBOARD ---
if check_password():
    st.set_page_config(layout="wide", page_title="Zeus Cockpit")
    apply_zeus_branding()
    
    # Header
    st.markdown("<h1 style='letter-spacing: 3px;'>COCKPIT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888;'>Übersicht der aktuellen Produktionen</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Beispiel-Daten
    data = {
        'PROJEKT': ['Commercial Reel', 'Social Content Drive', 'Brand Photography'],
        'STATUS': ['🎥 In Progress', '⏳ Review', '✅ Done'],
        'DEADLINE': ['22.01.2026', '28.01.2026', '15.01.2026'],
        'TEAM': ['Philipp', 'Team A', 'Philipp']
    }
    df = pd.DataFrame(data)
    st.table(df)
