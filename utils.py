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

def save_score(username, score, scores_table, attempts_table, score_column, is_better_func):
    """
    Save score if it's better than previous best and always log attempt
    
    Args:
        username: User identifier
        score: Score to save
        scores_table: Best scores table name
        attempts_table: All attempts table name
        score_column: Column name for the score
        is_better_func: Function that returns True if new score is better
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    
    # Always save attempt
    conn.execute(
        f"INSERT INTO {attempts_table}(username, {score_column}) VALUES(?,?)",
        (username, score)
    )
    
    # Check if it's a new best score
    cur = conn.execute(f"SELECT {score_column} FROM {scores_table} WHERE username=?", (username,))
    row = cur.fetchone()
    
    is_new_best = False
    if row is None or is_better_func(score, row[0]):
        conn.execute(
            f"INSERT OR REPLACE INTO {scores_table}(username, {score_column}) VALUES(?,?)",
            (username, score)
        )
        is_new_best = True
        st.balloons()
    
    conn.commit()
    return is_new_best

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

def display_user_attempts(username, attempts_table, score_column):
    """Display all attempts for a specific user"""
    if not username:
        return
        
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    
    df_attempts = pd.read_sql_query(
        f"""SELECT {score_column}, uploaded_at 
           FROM {attempts_table} 
           WHERE username=? 
           ORDER BY uploaded_at DESC""", 
        conn, 
        params=(username,)
    )
    
    if not df_attempts.empty:
        st.subheader(f"📈 Your Submission History ({username})")
        
        # Format datetime for better display
        df_attempts['uploaded_at'] = pd.to_datetime(df_attempts['uploaded_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
        df_attempts.columns = [score_column.upper(), 'Submitted At']
        
        st.dataframe(df_attempts, use_container_width=True)
        
        # Show some stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Attempts", len(df_attempts))
        with col2:
            best_score = df_attempts[score_column.upper()].min() if score_column in ['rmse', 'mae'] else df_attempts[score_column.upper()].max()
            st.metric("Best Score", f"{best_score:.4f}")
        with col3:
            latest_score = df_attempts[score_column.upper()].iloc[0]
            st.metric("Latest Score", f"{latest_score:.4f}")
    else:
        st.info(f"No submissions yet for {username}")