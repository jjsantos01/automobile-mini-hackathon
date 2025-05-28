# config.py
import sqlite3

DB_PATH = "leaderboard.db"

def init_database():
    """Initialize database with tables for all challenges"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    
    # Car price prediction table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS car_scores (
        username TEXT PRIMARY KEY,
        rmse REAL,
        uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Wine quality classification table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS wine_scores (
        username TEXT PRIMARY KEY,
        accuracy REAL,
        uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    return conn