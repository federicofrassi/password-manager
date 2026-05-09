

import tkinter as tk
from tkinter import messagebox, ttk

from auth import (
    create_auth_table,
    master_password_exists,
    save_master_password,
    verify_master_password
)
from crypto_utils import initialize_key
from database import create_table, get_all_credentials


def open_main_window(root):
    for widget in root.winfo_children():
        widget.destroy()

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

    refresh_button = tk.Button(root, text="Aggiorna lista", command=load_credentials)
    refresh_button.pack(pady=10)

    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=10)

    add_button = tk.Button(buttons_frame, text="Aggiungi credenziale")
    add_button.grid(row=0, column=0, padx=5)

    delete_button = tk.Button(buttons_frame, text="Elimina credenziale")
    delete_button.grid(row=0, column=1, padx=5)

    update_button = tk.Button(buttons_frame, text="Modifica password")
    update_button.grid(row=0, column=2, padx=5)

    search_button = tk.Button(buttons_frame, text="Cerca credenziale")
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