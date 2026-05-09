from cryptography.fernet import Fernet

#file per salvare la chiave di cifratura
KEY_FILE = "secret.key"

#crea una chiave e salva nel file
def generate_key():
    key = Fernet.generate_key()

    with open(KEY_FILE, "wb") as file:
        file.write(key)

#leggi la chiave dal file
def load_key():
    with open(KEY_FILE, "rb") as file:
        return file.read()

#controlla se secret.key esiste già
def key_exists():
    try:
        with open(KEY_FILE, "rb"):
            return True
    except FileNotFoundError:
        return False


def initialize_key():
    if not key_exists():
        generate_key()

#cripta una password
def encrypt_password(password):
    key = load_key()
    fernet = Fernet(key)

    encrypted_password = fernet.encrypt(password.encode())

    return encrypted_password.decode()

#decripta una password
def decrypt_password(encrypted_password):
    key = load_key()
    fernet = Fernet(key)

    decrypted_password = fernet.decrypt(encrypted_password.encode())

    return decrypted_password.decode()