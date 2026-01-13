import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime

# --- SETUP & DESIGN ---
st.set_page_config(page_title="Zeus Production Cockpit", layout="wide")

# Zeus Design Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    h1, h2, h3 { color: #f1c40f !important; }
    .stButton>button { background-color: #f1c40f; color: black; font-weight: bold; width: 100%; }
    .stTextInput>div>div>input { background-color: #262730; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- DATENBANK INITIALISIERUNG ---
DB_FILE = 'zeus_data.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS projekte 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, kunde TEXT, typ TEXT, 
                  status TEXT, notiz TEXT, datum TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- HAUPT NAVIGATION ---
st.title("⚡ ZEUS PRODUCTION CLOUD")

tabs = st.tabs(["📊 Dashboard & Kommunikation", "📂 Archiv", "⚙️ Einstellungen"])

with tabs[0]:
    col_left, col_right = st.columns([2, 1])
    
    with col_right:
        st.subheader("Neuer Auftrag")
        with st.form("new_project"):
            k_name = st.text_input("Kunde")
            k_typ = st.selectbox("Typ", ["Social Media", "LED-Wall", "Video/Foto", "Grafik"])
            if st.form_submit_button("Projekt anlegen"):
                if k_name:
                    conn = sqlite3.connect(DB_FILE)
                    c = conn.cursor()
                    c.execute("INSERT INTO projekte (kunde, typ, status, notiz, datum) VALUES (?, ?, ?, ?, ?)",
                              (k_name, k_typ, "Briefing", "", datetime.now().strftime("%d.%m.%Y")))
                    conn.commit()
                    conn.close()
                    st.success(f"{k_name} angelegt!")
                    st.rerun()

    with col_left:
        st.subheader("Aktuelle Projekte")
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql_query("SELECT * FROM projekte ORDER BY id DESC", conn)
        conn.close()

        for index, row in df.iterrows():
            with st.expander(f"📌 {row['kunde']} - {row['status']}"):
                c1, c2 = st.columns([3, 1])
                with c1:
                    new_notiz = st.text_area("Kommunikation / Updates:", value=row['notiz'], key=f"n_{row['id']}")
                with c2:
                    new_status = st.selectbox("Status:", ["Briefing", "In Arbeit", "Review", "Fertig"], 
                                             index=["Briefing", "In Arbeit", "Review", "Fertig"].index(row['status']),
                                             key=f"s_{row['id']}")
                    if st.button("Speichern", key=f"b_{row['id']}"):
                        conn = sqlite3.connect(DB_FILE)
                        c = conn.cursor()
                        c.execute("UPDATE projekte SET status=?, notiz=? WHERE id=?", (new_status, new_notiz, row['id']))
                        conn.commit()
                        conn.close()
                        st.toast("Synchronisiert!")
                        st.rerun()
                
                # Datei-Sektion
                st.divider()
                st.write("🖼️ **Logos & Grafiken:**")
                uploaded_file = st.file_uploader(f"Asset für {row['kunde']} hochladen", key=f"f_{row['id']}")
                if uploaded_file:
                    st.info(f"Datei {uploaded_file.name} empfangen (Wird in v2 dauerhaft gespeichert)")
