# utils.py
import streamlit as st
import pandas as pd
import sqlite3
from config import DB_PATH

def handle_username_input():
    """Handle username input from query params and text input"""
    qp = st.query_params
    username_qp = qp.get("user", "")

    if username_qp and "username" not in st.session_state:
        st.session_state["username"] = username_qp

    user_input = st.text_input("👤 Elige tu usuario (único)",
                            value=st.session_state.get("username", username_qp),
                            max_chars=20)

    if user_input:
        st.session_state["username"] = user_input
        if qp.get("user", "") != user_input:
            qp["user"] = user_input

    return user_input

def save_score(username, score, table_name, score_column, is_better_func):
    """
    Save score if it's better than previous best
    
    Args:
        username: User identifier
        score: Score to save
        table_name: Database table name
        score_column: Column name for the score
        is_better_func: Function that returns True if new score is better
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    
    cur = conn.execute(f"SELECT {score_column} FROM {table_name} WHERE username=?", (username,))
    row = cur.fetchone()
    
    if row is None or is_better_func(score, row[0]):
        conn.execute(
            f"INSERT OR REPLACE INTO {table_name}(username, {score_column}) VALUES(?,?)",
            (username, score)
        )
        conn.commit()
        st.balloons()
        return True
    return False

def display_leaderboard(table_name, score_column, ascending=True, limit=20):
    """Display leaderboard for a challenge"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    order = "ASC" if ascending else "DESC"
    
    df_lb = pd.read_sql_query(
        f"SELECT username, {score_column} FROM {table_name} ORDER BY {score_column} {order} LIMIT {limit}", 
        conn
    )
    
    if not df_lb.empty:
        st.dataframe(df_lb, use_container_width=True)
    else:
        st.info("No submissions yet!")