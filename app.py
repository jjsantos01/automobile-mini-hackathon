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

URL_TEST_Y = "https://s3.us-east-2.amazonaws.com/jjsantoso.com/datasets/automobile_test_y_real.csv"
y_true = pd.read_csv(URL_TEST_Y)["price"].to_numpy()

# ---------- UI ----------
st.title("🚗💰   Vakav Price Hackathon")
username = st.text_input("👤 Elige tu usuario (único)", max_chars=20)

uploaded = st.file_uploader("📤 Sube tu CSV de predicciones", type="csv")

if uploaded and username:
    preds = pd.read_csv(uploaded)["price"].to_numpy()
    if len(preds) != len(y_true):
        st.error(f"Número de filas incorrecto: {len(preds)} vs {len(y_true)}")
    else:
        rmse = np.sqrt(mean_squared_error(y_true, preds))
        st.success(f"Tu RMSE: {rmse:,.2f}")

        # Guarda solo si es la mejor marca personal
        cur = conn.execute("SELECT rmse FROM scores WHERE username=?", (username,))
        row = cur.fetchone()
        if row is None or rmse < row[0]:
            conn.execute(
                "INSERT OR REPLACE INTO scores(username, rmse) VALUES(?,?)",
                (username, rmse)
            )
            conn.commit()
            st.balloons()

# ---------- Ranking ----------
st.subheader("🏆 Ranking (mejor RMSE por usuario)")
df_lb = pd.read_sql_query(
    "SELECT username, rmse FROM scores ORDER BY rmse ASC LIMIT 20", conn
)
st.dataframe(df_lb, use_container_width=True)
