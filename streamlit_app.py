import streamlit as st
import pandas as pd

# --- ZEUS BRANDING (Eure Website-Ästhetik) ---
def apply_zeus_branding():
    st.markdown("""
        <style>
        .stApp { background-color: #000000; }
        [data-testid="stMarkdownContainer"] p, h1, h2, h3, span { color: #FFFFFF !important; }
        .stDataFrame { border: 1px solid #333333; }
        /* Der 'Baukasten' Button */
        div.stButton > button {
            background-color: #FFFFFF;
            color: #000000;
            border-radius: 0px;
            font-weight: bold;
            border: none;
        }
        /* Eingabefelder */
        input { background-color: #111111 !important; color: white !important; border: 1px solid #333333 !important; }
        </style>
    """, unsafe_allow_html=True)

# --- LOGIN ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True

    st.set_page_config(page_title="Zeus Cockpit", page_icon="⚪")
    apply_zeus_branding()
    st.markdown("<h2 style='text-align: center; letter-spacing: 5px; padding-top: 50px;'>ZEUS PRODUCTION</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        pw = st.text_input("ACCESS CODE", type="password")
        if st.button("ENTER"):
            if pw == "zeus2026":
                st.session_state["password_correct"] = True
                st.rerun()
    return False

# --- HAUPTPROGRAMM (Der Baukasten) ---
if check_password():
    st.set_page_config(layout="wide", page_title="Zeus Cockpit")
    apply_zeus_branding()
    
    st.markdown("<h1 style='letter-spacing: 2px;'>COCKPIT CONTROL</h1>", unsafe_allow_html=True)
    
    # --- DATEN-SPEICHERUNG (Simulierter Baukasten) ---
    # In einer Profi-Version würden wir hier Google Sheets verknüpfen
    if 'projekt_daten' not in st.session_state:
        st.session_state.projekt_daten = pd.DataFrame([
            {'PROJEKT': 'Commercial Reel', 'STATUS': 'In Progress', 'DEADLINE': '2026-01-22'},
            {'PROJEKT': 'Social Content', 'STATUS': 'Done', 'DEADLINE': '2026-01-15'}
        ])

    # --- BAUKASTEN-INTERFACE ---
    with st.expander("➕ NEUES PROJEKT HINZUFÜGEN"):
        with st.form("neues_projekt"):
            name = st.text_input("Projekt Name")
            status = st.selectbox("Status", ["Planung", "In Produktion", "Post-Production", "Done"])
            deadline = st.date_input("Deadline")
            submit = st.form_submit_button("PROJEKT SPEICHERN")
            
            if submit:
                new_row = {'PROJEKT': name, 'STATUS': status, 'DEADLINE': str(deadline)}
                st.session_state.projekt_daten = pd.concat([st.session_state.projekt_daten, pd.DataFrame([new_row])], ignore_index=True)
                st.success("Projekt hinzugefügt!")
                st.rerun()

    st.markdown("---")

    # --- DIE ÜBERSICHT ---
    st.subheader("Aktuelle Produktionen")
    
    # Interaktive Tabelle (wie Excel)
    edited_df = st.data_editor(st.session_state.projekt_daten, use_container_width=True, num_rows="dynamic")
    
    if st.button("ÄNDERUNGEN ÜBERNEHMEN"):
        st.session_state.projekt_daten = edited_df
        st.toast("Daten wurden aktualisiert!")

    # Logout Button in der Ecke
    if st.sidebar.button("Logout"):
        st.session_state["password_correct"] = False
        st.rerun()
