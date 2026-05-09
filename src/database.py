import sqlite3

DB_NAME = "password_manager.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   site TEXT NOT NULL,
                   username TEXT NOT NULL,
                   password TEXT NOT NULL,
                   notes TEXT
                )
    """)

    conn.commit()
    conn.close()

    