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

#aggiunge una nuova riga alla tabella 
def add_credential(site, username, password, notes=""): 
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO credentials (site, username, password, notes)

        VALUES (?, ?, ?, ?)

    """, (site, username, password, notes))
    conn.commit() 
    conn.close()

#legge tutte le righe della tabella credentials
def get_all_credentials():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, site, username, password, notes
        FROM credentials
    """)

    credentials = cursor.fetchall() #prende i risultati della query e li trasforma in una lista python

    conn.close()

    return credentials



#ricerca credenziali per sito 
def search_credentials(site): 
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT id, site, username, password, notes

        FROM credentials

        WHERE site LIKE ?

    """, (f"{site}%",))
    credentials = cursor.fetchall()

    conn.close()

    return credentials

#elimina credenziali
def delete_credential(credential_id): 
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM credentials

        WHERE id = ?

    """, (credential_id,))

    deleted_rows = cursor.rowcount
    
    conn.commit()
    conn.close()
    return deleted_rows > 0

#modifica password
def update_password(credential_id, new_password):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""

        UPDATE credentials

        SET password = ?

        WHERE id = ?

    """, (new_password, credential_id))

    updated_rows = cursor.rowcount

    conn.commit()
    conn.close()
    return updated_rows > 0


