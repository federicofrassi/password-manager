from database import create_table, add_credential, get_all_credentials


def show_menu():
    print("\n=== PASSWORD MANAGER ===")
    print("1. Aggiungi credenziale")
    print("2. Mostra credenziali")
    print("0. Esci")


def print_credentials(credentials):
    if not credentials:
        print("Nessuna credenziale salvata.")
        return

    for credential in credentials:
        print("\n----------------------")
        print(f"ID: {credential[0]}")
        print(f"Sito: {credential[1]}")
        print(f"Username: {credential[2]}")
        print(f"Password: {credential[3]}")
        print(f"Note: {credential[4]}")


create_table()

while True:
    show_menu()
    choice = input("Scegli un'opzione: ")

    if choice == "1":
        site = input("Sito/app: ")
        username = input("Username/email: ")
        password = input("Password: ")
        notes = input("Note: ")

        add_credential(site, username, password, notes)
        print("Credenziale aggiunta correttamente.")

    elif choice == "2":
        credentials = get_all_credentials()
        print_credentials(credentials)

    elif choice == "0":
        print("Uscita dal programma.")
        break

    else:
        print("Opzione non valida.")