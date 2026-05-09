import hashlib
from database import connect

#hash della master password
def hash_master_password(master_password):
    return hashlib.sha256(master_password.encode()).hexdigest()

#crea una tabella per salvare l'hash della master password
def create_auth_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            master_password_hash TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

#controlla se esiste già una master password
def master_password_exists():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM auth")
    count = cursor.fetchone()[0]

    conn.close()

    return count > 0

#salva SOLO l'hash della master password 
def save_master_password(master_password):
    conn = connect()
    cursor = conn.cursor()

    password_hash = hash_master_password(master_password)

    cursor.execute("""
        INSERT INTO auth (master_password_hash)
        VALUES (?)
    """, (password_hash,))

    conn.commit()
    conn.close()

#controlla se la master password inserita è corretta
def verify_master_password(master_password):
    conn = connect()
    cursor = conn.cursor()

    password_hash = hash_master_password(master_password)

    cursor.execute("""
        SELECT master_password_hash
        FROM auth
        LIMIT 1
    """)

    saved_hash = cursor.fetchone()[0]

    conn.close()

    return password_hash == saved_hash

