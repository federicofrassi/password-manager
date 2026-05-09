import tkinter as tk
from tkinter import messagebox, ttk

from auth import (
    create_auth_table,
    master_password_exists,
    save_master_password,
    verify_master_password
)
from crypto_utils import initialize_key
from database import create_table, get_all_credentials, add_credential, delete_credential, update_password, search_credentials


def open_main_window(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.unbind("<Return>")

    root.title("Password Manager")
    root.geometry("900x500")

    title_label = tk.Label(root, text="Password Manager", font=("Arial", 20))
    title_label.pack(pady=20)

    columns = ("id", "site", "username", "password", "notes")

    credentials_table = ttk.Treeview(root, columns=columns, show="headings")

    credentials_table.heading("id", text="ID")
    credentials_table.heading("site", text="Sito/App")
    credentials_table.heading("username", text="Username/Email")
    credentials_table.heading("password", text="Password")
    credentials_table.heading("notes", text="Note")

    credentials_table.column("id", width=50)
    credentials_table.column("site", width=150)
    credentials_table.column("username", width=200)
    credentials_table.column("password", width=200)
    credentials_table.column("notes", width=250)

    credentials_table.pack(fill="both", expand=True, padx=20, pady=10)

    def load_credentials():
        for row in credentials_table.get_children():
            credentials_table.delete(row)

        credentials = get_all_credentials()

        for credential in credentials:
            credentials_table.insert("", "end", values=credential)

        refresh_button.config(text="Aggiorna")

    def open_add_credential_window():
        add_window = tk.Toplevel(root)
        add_window.title("Aggiungi credenziale")
        add_window.geometry("400x350")

        site_label = tk.Label(add_window, text="Sito/App")
        site_label.pack(pady=5)
        site_entry = tk.Entry(add_window)
        site_entry.pack(pady=5)

        username_label = tk.Label(add_window, text="Username/Email")
        username_label.pack(pady=5)
        username_entry = tk.Entry(add_window)
        username_entry.pack(pady=5)

        password_label = tk.Label(add_window, text="Password")
        password_label.pack(pady=5)
        password_entry = tk.Entry(add_window, show="*")
        password_entry.pack(pady=5)

        notes_label = tk.Label(add_window, text="Note")
        notes_label.pack(pady=5)
        notes_entry = tk.Entry(add_window)
        notes_entry.pack(pady=5)

        def save_credential():
            site = site_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            notes = notes_entry.get()

            if not site or not username or not password:
                messagebox.showerror("Errore", "Sito, username e password sono obbligatori.")
                return

            add_credential(site, username, password, notes)
            messagebox.showinfo("Successo", "Credenziale aggiunta correttamente.")
            add_window.destroy()
            load_credentials()

        save_button = tk.Button(add_window, text="Salva", command=save_credential)
        save_button.pack(pady=20)
        add_window.bind("<Return>", lambda event: save_credential())

    def delete_selected_credential():
        selected_item = credentials_table.selection()

        if not selected_item:
            messagebox.showerror("Errore", "Seleziona una credenziale da eliminare.")
            return

        credential = credentials_table.item(selected_item[0], "values")
        credential_id = credential[0]

        confirm = messagebox.askyesno(
            "Conferma eliminazione",
            "Sei sicuro di voler eliminare questa credenziale?"
        )

        if confirm:
            deleted = delete_credential(int(credential_id))

            if deleted:
                messagebox.showinfo("Successo", "Credenziale eliminata correttamente.")
                load_credentials()
            else:
                messagebox.showerror("Errore", "Credenziale non trovata.")

    def open_update_password_window():
        selected_item = credentials_table.selection()

        if not selected_item:
            messagebox.showerror("Errore", "Seleziona una credenziale da modificare.")
            return

        credential = credentials_table.item(selected_item[0], "values")
        credential_id = credential[0]
        site = credential[1]

        update_window = tk.Toplevel(root)
        update_window.title("Modifica password")
        update_window.geometry("400x220")

        title_label = tk.Label(update_window, text=f"Modifica password per {site}", font=("Arial", 14))
        title_label.pack(pady=15)

        password_label = tk.Label(update_window, text="Nuova password")
        password_label.pack(pady=5)

        password_entry = tk.Entry(update_window, show="*")
        password_entry.pack(pady=5)

        def save_new_password():
            new_password = password_entry.get()

            if not new_password:
                messagebox.showerror("Errore", "La password non può essere vuota.")
                return

            updated = update_password(int(credential_id), new_password)

            if updated:
                messagebox.showinfo("Successo", "Password aggiornata correttamente.")
                update_window.destroy()
                load_credentials()
            else:
                messagebox.showerror("Errore", "Credenziale non trovata.")

        save_button = tk.Button(update_window, text="Salva", command=save_new_password)
        save_button.pack(pady=15)
        update_window.bind("<Return>", lambda event: save_new_password())

    def open_search_window():
        search_window = tk.Toplevel(root)
        search_window.title("Cerca credenziale")
        search_window.geometry("400x180")

        search_label = tk.Label(search_window, text="Cerca sito/app")
        search_label.pack(pady=10)

        search_entry = tk.Entry(search_window)
        search_entry.pack(pady=5)

        def search():
            search_text = search_entry.get()

            for row in credentials_table.get_children():
                credentials_table.delete(row)

            credentials = search_credentials(search_text)

            for credential in credentials:
                credentials_table.insert("", "end", values=credential)

            refresh_button.config(text="Mostra tutte")

            search_window.destroy()

        search_button = tk.Button(search_window, text="Cerca", command=search)
        search_button.pack(pady=15)
        search_window.bind("<Return>", lambda event: search())

    refresh_button = tk.Button(root, text="Aggiorna", command=load_credentials)
    refresh_button.pack(pady=10)

    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=10)

    add_button = tk.Button(buttons_frame, text="Aggiungi credenziale", command=open_add_credential_window)
    add_button.grid(row=0, column=0, padx=5)

    delete_button = tk.Button(buttons_frame, text="Elimina credenziale", command=delete_selected_credential)
    delete_button.grid(row=0, column=1, padx=5)

    update_button = tk.Button(buttons_frame, text="Modifica password", command=open_update_password_window)
    update_button.grid(row=0, column=2, padx=5)

    search_button = tk.Button(buttons_frame, text="Cerca credenziale", command=open_search_window)
    search_button.grid(row=0, column=3, padx=5)

    load_credentials()


def show_create_master_password_screen(root):
    root.title("Create Master Password")
    root.geometry("400x250")

    title_label = tk.Label(root, text="Crea Master Password", font=("Arial", 16))
    title_label.pack(pady=20)

    password_label = tk.Label(root, text="Master Password")
    password_label.pack()

    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    confirm_label = tk.Label(root, text="Confirm Master Password")
    confirm_label.pack()

    confirm_entry = tk.Entry(root, show="*")
    confirm_entry.pack(pady=5)

    def create_master_password():
        password = password_entry.get()
        confirm_password = confirm_entry.get()

        if not password:
            messagebox.showerror("Errore", "La master password non può essere vuota.")
            return

        if password != confirm_password:
            messagebox.showerror("Errore", "Le password non coincidono.")
            return

        save_master_password(password)
        messagebox.showinfo("Successo", "Master password creata correttamente.")
        open_main_window(root)

    create_button = tk.Button(root, text="Crea", command=create_master_password)
    create_button.pack(pady=15)


def show_login_screen(root):
    root.title("Login")
    root.geometry("400x220")

    title_label = tk.Label(root, text="Login", font=("Arial", 16))
    title_label.pack(pady=20)

    password_label = tk.Label(root, text="Master Password")
    password_label.pack()

    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=10)

    def login():
        password = password_entry.get()

        if verify_master_password(password):
            open_main_window(root)
        else:
            messagebox.showerror("Errore", "Master password errata.")

    login_button = tk.Button(root, text="Accedi", command=login)
    login_button.pack(pady=10)
    root.bind("<Return>", lambda event: login())


def main():
    create_table()
    create_auth_table()
    initialize_key()

    root = tk.Tk()

    if master_password_exists():
        show_login_screen(root)
    else:
        show_create_master_password_screen(root)

    root.mainloop()


if __name__ == "__main__":
    main()