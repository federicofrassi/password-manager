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

    table_frame = tk.Frame(root)
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    credentials_table = ttk.Treeview(table_frame, columns=columns, show="headings")

    vertical_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=credentials_table.yview)
    credentials_table.configure(yscrollcommand=vertical_scrollbar.set)

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

    credentials_table.pack(side="left", fill="both", expand=True)
    vertical_scrollbar.pack(side="right", fill="y")

    def load_credentials():
        for row in credentials_table.get_children():
            credentials_table.delete(row)

        credentials = get_all_credentials()

        for credential in credentials:
            masked_credential = (
                credential[0],
                credential[1],
                credential[2],
                "********",
                credential[4]
            )
            credentials_table.insert("", "end", values=masked_credential, tags=(credential[3], "hidden"))

        refresh_button.config(text="Aggiorna")

    def has_open_popup():
        return any(isinstance(window, tk.Toplevel) for window in root.winfo_children())

    def setup_popup_window(popup):
        popup.transient(root)
        popup.grab_set()
        popup.focus_force()

    def open_add_credential_window():
        if has_open_popup():
            messagebox.showerror("Errore", "Chiudi la finestra aperta prima di aprirne un'altra.")
            return
        add_window = tk.Toplevel(root)
        add_window.title("Aggiungi credenziale")
        add_window.geometry("400x350")
        setup_popup_window(add_window)

        site_label = tk.Label(add_window, text="Sito/App")
        site_label.pack(pady=5)
        site_entry = tk.Entry(add_window)
        site_entry.pack(pady=5)
        site_entry.focus_set()

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
        if has_open_popup():
            messagebox.showerror("Errore", "Chiudi la finestra aperta prima di continuare.")
            return
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
        if has_open_popup():
            messagebox.showerror("Errore", "Chiudi la finestra aperta prima di aprirne un'altra.")
            return
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
        setup_popup_window(update_window)

        title_label = tk.Label(update_window, text=f"Modifica password per {site}", font=("Arial", 14))
        title_label.pack(pady=15)

        password_label = tk.Label(update_window, text="Nuova password")
        password_label.pack(pady=5)

        password_entry = tk.Entry(update_window, show="*")
        password_entry.pack(pady=5)
        password_entry.focus_set()

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
        if has_open_popup():
            messagebox.showerror("Errore", "Chiudi la finestra aperta prima di aprirne un'altra.")
            return
        search_window = tk.Toplevel(root)
        search_window.title("Cerca credenziale")
        search_window.geometry("400x180")
        setup_popup_window(search_window)

        search_label = tk.Label(search_window, text="Cerca sito/app")
        search_label.pack(pady=10)

        search_entry = tk.Entry(search_window)
        search_entry.pack(pady=5)
        search_entry.focus_set()

        def search():
            search_text = search_entry.get()

            for row in credentials_table.get_children():
                credentials_table.delete(row)

            credentials = search_credentials(search_text)

            for credential in credentials:
                masked_credential = (
                    credential[0],
                    credential[1],
                    credential[2],
                    "********",
                    credential[4]
                )
                credentials_table.insert("", "end", values=masked_credential, tags=(credential[3], "hidden"))

            refresh_button.config(text="Mostra tutte")

            search_window.destroy()

        search_button = tk.Button(search_window, text="Cerca", command=search)
        search_button.pack(pady=15)
        search_window.bind("<Return>", lambda event: search())

    def toggle_selected_password():
        selected_item = credentials_table.selection()

        if not selected_item:
            messagebox.showerror("Errore", "Seleziona una credenziale.")
            return

        item_id = selected_item[0]
        credential = credentials_table.item(item_id, "values")
        tags = credentials_table.item(item_id, "tags")

        real_password = tags[0]
        password_state = tags[1]

        if password_state == "hidden":
            updated_credential = (
                credential[0],
                credential[1],
                credential[2],
                real_password,
                credential[4]
            )
            credentials_table.item(item_id, values=updated_credential, tags=(real_password, "visible"))
            toggle_password_button.config(text="Nascondi password")
        else:
            updated_credential = (
                credential[0],
                credential[1],
                credential[2],
                "********",
                credential[4]
            )
            credentials_table.item(item_id, values=updated_credential, tags=(real_password, "hidden"))
            toggle_password_button.config(text="Mostra password")

    actions_frame = tk.Frame(root)
    actions_frame.pack(pady=10)

    refresh_button = tk.Button(actions_frame, text="Aggiorna", command=load_credentials)
    refresh_button.grid(row=0, column=0, padx=5)

    buttons_frame = tk.Frame(actions_frame)
    buttons_frame.grid(row=0, column=1, padx=5)

    add_button = tk.Button(buttons_frame, text="Aggiungi credenziale", command=open_add_credential_window)
    add_button.grid(row=0, column=0, padx=5)

    delete_button = tk.Button(buttons_frame, text="Elimina credenziale", command=delete_selected_credential)
    delete_button.grid(row=0, column=1, padx=5)

    update_button = tk.Button(buttons_frame, text="Modifica password", command=open_update_password_window)
    update_button.grid(row=0, column=2, padx=5)

    search_button = tk.Button(buttons_frame, text="Cerca credenziale", command=open_search_window)
    search_button.grid(row=0, column=3, padx=5)

    toggle_password_button = tk.Button(buttons_frame, text="Mostra password", command=toggle_selected_password)
    toggle_password_button.grid(row=0, column=4, padx=5)

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
    root.after(100, password_entry.focus_force)

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
            password_entry.delete(0, tk.END)
            confirm_entry.delete(0, tk.END)
            password_entry.focus_force()
            return

        save_master_password(password)
        messagebox.showinfo("Successo", "Master password creata correttamente.")
        open_main_window(root)

    create_button = tk.Button(root, text="Crea", command=create_master_password)
    create_button.pack(pady=15)
    root.bind("<Return>", lambda event: create_master_password())


def show_login_screen(root):
    root.title("Login")
    root.geometry("400x220")

    title_label = tk.Label(root, text="Login", font=("Arial", 16))
    title_label.pack(pady=20)

    password_label = tk.Label(root, text="Master Password")
    password_label.pack()

    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=10)
    root.after(100, password_entry.focus_force)

    def login():
        password = password_entry.get()

        if verify_master_password(password):
            open_main_window(root)
        else:
            messagebox.showerror("Errore", "Master password errata.")
            password_entry.delete(0, tk.END)
            password_entry.focus_force()

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