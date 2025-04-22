# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from sklearn.metrics import mean_squared_error

# ---------- Configuración ----------

DB_PATH = "leaderboard.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.execute("""
CREATE TABLE IF NOT EXISTS scores (
    username TEXT PRIMARY KEY,
    rmse REAL,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

URL_TEST_Y = st.secrets["URL_TEST_Y"]
y_true = pd.read_csv(URL_TEST_Y)["price"].to_numpy()

# ---------- UI ----------
st.title("🚗💰   Vakav Price Hackathon")
qp = st.query_params
username_qp = qp.get("user", "")

if username_qp and "username" not in st.session_state:
    st.session_state["username"] = username_qp

user_input = st.text_input("👤 Elige tu usuario (único)",
                        value=st.session_state.get("username", username_qp),
                        max_chars=20)

if user_input:
    st.session_state["username"] = user_input
    # Evita que se disparen bucles infinitos comprobando valor actual
    if qp.get("user", "") != user_input:
        qp["user"] = user_input         # esto provoca un rerun limpio

uploaded = st.file_uploader("📤 Sube tu CSV de predicciones", type="csv")

if uploaded:
    if user_input:
        preds = pd.read_csv(uploaded)["price"].to_numpy()
        if len(preds) != len(y_true):
            st.error(f"Número de filas incorrecto: {len(preds)} vs {len(y_true)}")
        else:
            rmse = np.sqrt(mean_squared_error(y_true, preds))
            st.success(f"Tu RMSE: {rmse:,.2f}")

            # Guarda solo si es la mejor marca personal
            cur = conn.execute("SELECT rmse FROM scores WHERE username=?", (user_input,))
            row = cur.fetchone()
            if row is None or rmse < row[0]:
                conn.execute(
                    "INSERT OR REPLACE INTO scores(username, rmse) VALUES(?,?)",
                    (user_input, rmse)
                )
                conn.commit()
                st.balloons()
    else:
        st.error("Introduzca su usuario")

# ---------- Ranking ----------
st.subheader("🏆 Ranking (mejor RMSE por usuario)")
df_lb = pd.read_sql_query(
    "SELECT username, rmse FROM scores ORDER BY rmse ASC LIMIT 20", conn
)
st.dataframe(df_lb, use_container_width=True)
