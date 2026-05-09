from database import create_table, add_credential, get_all_credentials, search_credentials, delete_credential, update_password


def show_menu():
    print("\n=== PASSWORD MANAGER ===")
    print("1. Aggiungi credenziale")
    print("2. Mostra credenziali")
    print("3. Cerca credenziale")
    print("4. Elimina credenziale")
    print("5. Modifica password")
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

    elif choice == "3": 
        search = input("Cerca sito/app: ")
        credentials = search_credentials(search)
        print_credentials(credentials)

    elif choice == "4": 
        credential_id = input("ID credenziale da eliminare: ")

        if credential_id.isdigit(): 
            deleted = delete_credential(int(credential_id))

            if deleted:
                print("Credenziale eliminata correttamente.")
            else:
                print("Nessuna credenziale trovata con questo ID.")
        else: 
            print("ID non valido")

    elif choice == "5": 
        credential_id = input("ID credenziale da modificare: ")

        if credential_id.isdigit(): 
            new_password = input("Nuova password: ")

            updated = update_password(int(credential_id), new_password)

            if updated:
                print("Password aggiornata correttamente.")
            else:
                print("Nessuna credenziale trovata con questo ID.")
        else: 
            print("ID non valido.")
    

    elif choice == "0":
        print("Uscita dal programma.")
        break

    else:
        print("Opzione non valida.")