# config.py
import sqlite3

DB_PATH = "leaderboard.db"

def init_database():
    """Initialize database with tables for all challenges"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    
    # Car price prediction - best scores only
    conn.execute("""
    CREATE TABLE IF NOT EXISTS car_scores (
        username TEXT PRIMARY KEY,
        rmse REAL,
        uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Car price prediction - all attempts
    conn.execute("""
    CREATE TABLE IF NOT EXISTS car_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        rmse REAL,
        uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Wine quality classification - best scores only
    conn.execute("""
    CREATE TABLE IF NOT EXISTS wine_scores (
        username TEXT PRIMARY KEY,
        accuracy REAL,
        uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Wine quality classification - all attempts
    conn.execute("""
    CREATE TABLE IF NOT EXISTS wine_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        accuracy REAL,
        uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # PISA math performance - best scores only
    conn.execute("""
    CREATE TABLE IF NOT EXISTS pisa_scores (
        username TEXT PRIMARY KEY,
        mae REAL,
        uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # PISA math performance - all attempts
    conn.execute("""
    CREATE TABLE IF NOT EXISTS pisa_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        mae REAL,
        uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    return conn