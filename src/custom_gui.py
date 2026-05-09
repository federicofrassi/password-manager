import customtkinter as ctk
from tkinter import messagebox

from database import (
    create_table,
    get_all_credentials,
    search_credentials,
    add_credential,
    delete_credential,
    update_password
)
from auth import (
    create_auth_table,
    master_password_exists,
    save_master_password,
    verify_master_password
)
from crypto_utils import initialize_key


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()


def open_main_window(root):
    clear_window(root)
    root.unbind("<Return>")

    root.geometry("1000x650")

    main_frame = ctk.CTkFrame(root, corner_radius=20)
    main_frame.pack(expand=True, fill="both", padx=30, pady=30)

    header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    header_frame.pack(fill="x", padx=25, pady=(25, 10))

    title_label = ctk.CTkLabel(
        header_frame,
        text="Password Manager",
        font=("Arial", 30, "bold")
    )
    title_label.pack(anchor="w")

    subtitle_label = ctk.CTkLabel(
        header_frame,
        text="Gestisci le tue credenziali in modo sicuro",
        font=("Arial", 15),
        text_color="#A0A0A0"
    )
    subtitle_label.pack(anchor="w", pady=(4, 0))

    search_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    search_frame.pack(fill="x", padx=25, pady=(15, 10))

    search_entry = ctk.CTkEntry(
        search_frame,
        placeholder_text="Cerca sito/app...",
        height=40
    )
    search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

    credentials_frame = ctk.CTkScrollableFrame(main_frame, corner_radius=15)
    credentials_frame.pack(fill="both", expand=True, padx=25, pady=10)

    buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    buttons_frame.pack(fill="x", padx=25, pady=(10, 25))

    selected_credential = {
        "id": None,
        "password": None,
        "row": None,
        "password_label": None,
        "visible": False
    }

    def clear_credentials_list():
        for widget in credentials_frame.winfo_children():
            widget.destroy()

    def reset_selected_credential():
        row = selected_credential["row"]

        if row is not None and row.winfo_exists():
            row.configure(border_width=0)

        selected_credential["id"] = None
        selected_credential["password"] = None
        selected_credential["row"] = None
        selected_credential["password_label"] = None
        selected_credential["visible"] = False
        show_password_button.configure(text="Mostra password")

    def select_credential(row_frame, credential_id, password, password_label):
        if selected_credential["row"] is not None:
            selected_credential["row"].configure(border_width=0)

        selected_credential["id"] = credential_id
        selected_credential["password"] = password
        selected_credential["row"] = row_frame
        selected_credential["password_label"] = password_label
        selected_credential["visible"] = False

        show_password_button.configure(text="Mostra password")
        row_frame.configure(border_width=2, border_color="#1f6aa5")

    def add_credential_row(credential):
        credential_id = credential[0]
        site = credential[1]
        username = credential[2]
        password = credential[3]
        notes = credential[4] if credential[4] else "-"

        row_frame = ctk.CTkFrame(credentials_frame, corner_radius=10)
        row_frame.pack(fill="x", padx=8, pady=6)

        site_label = ctk.CTkLabel(
            row_frame,
            text=site,
            font=("Arial", 14, "bold"),
            width=170,
            anchor="w"
        )
        site_label.grid(row=0, column=0, padx=12, pady=12, sticky="w")

        username_label = ctk.CTkLabel(
            row_frame,
            text=username,
            width=220,
            anchor="w"
        )
        username_label.grid(row=0, column=1, padx=8, pady=12, sticky="w")

        password_label = ctk.CTkLabel(
            row_frame,
            text="********",
            width=130,
            anchor="w"
        )
        password_label.grid(row=0, column=2, padx=8, pady=12, sticky="w")

        notes_label = ctk.CTkLabel(
            row_frame,
            text=notes,
            width=220,
            anchor="w",
            text_color="#A0A0A0"
        )
        notes_label.grid(row=0, column=3, padx=8, pady=12, sticky="w")

        row_frame.grid_columnconfigure(3, weight=1)

        def on_select(event=None):
            select_credential(row_frame, credential_id, password, password_label)

        row_frame.bind("<Button-1>", on_select)
        site_label.bind("<Button-1>", on_select)
        username_label.bind("<Button-1>", on_select)
        password_label.bind("<Button-1>", on_select)
        notes_label.bind("<Button-1>", on_select)

    def load_credentials():
        reset_selected_credential()
        clear_credentials_list()
        search_entry.delete(0, "end")

        credentials = get_all_credentials()

        if not credentials:
            empty_label = ctk.CTkLabel(
                credentials_frame,
                text="Nessuna credenziale salvata.",
                text_color="#A0A0A0"
            )
            empty_label.pack(pady=30)
            return

        for credential in credentials:
            add_credential_row(credential)

    def search_from_entry(event=None):
        reset_selected_credential()
        clear_credentials_list()

        search_text = search_entry.get().strip().lower()
        all_credentials = get_all_credentials()

        if search_text:
            credentials = [
                credential for credential in all_credentials
                if credential[1].lower().startswith(search_text)
            ]
            empty_message = "Nessun risultato trovato."
        else:
            credentials = all_credentials
            empty_message = "Nessuna credenziale salvata."

        if not credentials:
            empty_label = ctk.CTkLabel(
                credentials_frame,
                text=empty_message,
                text_color="#A0A0A0"
            )
            empty_label.pack(pady=30)
            return

        for credential in credentials:
            add_credential_row(credential)

    def clear_search():
        search_entry.delete(0, "end")
        load_credentials()

    def copy_selected_password():
        if selected_credential["id"] is None:
            messagebox.showerror("Errore", "Seleziona una credenziale.")
            return

        root.clipboard_clear()
        root.clipboard_append(selected_credential["password"])
        root.update()
        messagebox.showinfo("Successo", "Password copiata negli appunti.")

    def toggle_selected_password():
        if selected_credential["id"] is None:
            messagebox.showerror("Errore", "Seleziona una credenziale.")
            return

        password_label = selected_credential["password_label"]

        if selected_credential["visible"]:
            password_label.configure(text="********")
            selected_credential["visible"] = False
            show_password_button.configure(text="Mostra password")
        else:
            password_label.configure(text=selected_credential["password"])
            selected_credential["visible"] = True
            show_password_button.configure(text="Nascondi password")

    def open_add_credential_window():
        add_window = ctk.CTkToplevel(root)
        add_window.title("Aggiungi credenziale")
        add_window.geometry("420x420")
        add_window.transient(root)
        add_window.grab_set()
        add_window.focus_force()

        title = ctk.CTkLabel(
            add_window,
            text="Aggiungi credenziale",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=(25, 20))

        site_entry = ctk.CTkEntry(add_window, placeholder_text="Sito/App", width=320, height=40)
        site_entry.pack(pady=8)

        username_entry = ctk.CTkEntry(add_window, placeholder_text="Username/Email", width=320, height=40)
        username_entry.pack(pady=8)

        password_entry = ctk.CTkEntry(add_window, placeholder_text="Password", show="*", width=320, height=40)
        password_entry.pack(pady=8)

        notes_entry = ctk.CTkEntry(add_window, placeholder_text="Note", width=320, height=40)
        notes_entry.pack(pady=8)

        root.after(100, site_entry.focus_force)

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

        save_button = ctk.CTkButton(
            add_window,
            text="Salva",
            command=save_credential,
            width=320,
            height=40
        )
        save_button.pack(pady=22)
        add_window.bind("<Return>", lambda event: save_credential())

    def delete_selected_credential():
        if selected_credential["id"] is None:
            messagebox.showerror("Errore", "Seleziona una credenziale da eliminare.")
            return

        confirm = messagebox.askyesno(
            "Conferma eliminazione",
            "Sei sicuro di voler eliminare questa credenziale?"
        )

        if confirm:
            deleted = delete_credential(int(selected_credential["id"]))

            if deleted:
                messagebox.showinfo("Successo", "Credenziale eliminata correttamente.")
                load_credentials()
            else:
                messagebox.showerror("Errore", "Credenziale non trovata.")

    def open_update_password_window():
        if selected_credential["id"] is None:
            messagebox.showerror("Errore", "Seleziona una credenziale da modificare.")
            return

        update_window = ctk.CTkToplevel(root)
        update_window.title("Modifica password")
        update_window.geometry("420x250")
        update_window.transient(root)
        update_window.grab_set()
        update_window.focus_force()

        title = ctk.CTkLabel(
            update_window,
            text="Modifica password",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=(28, 18))

        password_entry = ctk.CTkEntry(
            update_window,
            placeholder_text="Nuova password",
            show="*",
            width=320,
            height=40
        )
        password_entry.pack(pady=10)

        root.after(100, password_entry.focus_force)

        def save_new_password():
            new_password = password_entry.get()

            if not new_password:
                messagebox.showerror("Errore", "La password non può essere vuota.")
                return

            updated = update_password(int(selected_credential["id"]), new_password)

            if updated:
                messagebox.showinfo("Successo", "Password aggiornata correttamente.")
                update_window.destroy()
                load_credentials()
            else:
                messagebox.showerror("Errore", "Credenziale non trovata.")

        save_button = ctk.CTkButton(
            update_window,
            text="Salva",
            command=save_new_password,
            width=320,
            height=40
        )
        save_button.pack(pady=20)
        update_window.bind("<Return>", lambda event: save_new_password())

    reset_button = ctk.CTkButton(search_frame, text="Reset", command=clear_search, width=90, height=40)
    reset_button.pack(side="right")

    search_entry.bind("<KeyRelease>", search_from_entry)

    add_button = ctk.CTkButton(buttons_frame, text="Aggiungi", command=open_add_credential_window, width=140, height=40)
    add_button.pack(side="left", padx=6)

    refresh_button = ctk.CTkButton(buttons_frame, text="Aggiorna", command=load_credentials, width=140, height=40)
    refresh_button.pack(side="left", padx=6)

    copy_button = ctk.CTkButton(buttons_frame, text="Copia password", command=copy_selected_password, width=150, height=40)
    copy_button.pack(side="left", padx=6)

    show_password_button = ctk.CTkButton(buttons_frame, text="Mostra password", command=toggle_selected_password, width=160, height=40)
    show_password_button.pack(side="left", padx=6)

    update_button = ctk.CTkButton(buttons_frame, text="Modifica", command=open_update_password_window, width=140, height=40)
    update_button.pack(side="left", padx=6)

    delete_button = ctk.CTkButton(
        buttons_frame,
        text="Elimina",
        command=delete_selected_credential,
        fg_color="#b23b3b",
        hover_color="#8f2f2f",
        width=140,
        height=40
    )
    delete_button.pack(side="left", padx=6)

    load_credentials()


def show_create_master_password_screen(root):
    clear_window(root)

    root.geometry("520x420")

    auth_frame = ctk.CTkFrame(root, corner_radius=20)
    auth_frame.pack(expand=True, padx=40, pady=40)

    title_label = ctk.CTkLabel(
        auth_frame,
        text="Crea Master Password",
        font=("Arial", 24, "bold")
    )
    title_label.pack(pady=(35, 8))

    subtitle_label = ctk.CTkLabel(
        auth_frame,
        text="Imposta la password principale del vault",
        font=("Arial", 14),
        text_color="#A0A0A0"
    )
    subtitle_label.pack(pady=(0, 25))

    password_entry = ctk.CTkEntry(
        auth_frame,
        placeholder_text="Master Password",
        show="*",
        width=320,
        height=42
    )
    password_entry.pack(pady=8)

    confirm_entry = ctk.CTkEntry(
        auth_frame,
        placeholder_text="Conferma Master Password",
        show="*",
        width=320,
        height=42
    )
    confirm_entry.pack(pady=8)

    root.after(100, password_entry.focus_force)

    def create_master_password():
        password = password_entry.get()
        confirm_password = confirm_entry.get()

        if not password or not confirm_password:
            messagebox.showerror("Errore", "Compila tutti i campi.")
            return

        if password != confirm_password:
            messagebox.showerror("Errore", "Le password non coincidono.")

            password_entry.delete(0, "end")
            confirm_entry.delete(0, "end")

            password_entry.focus_force()
            return

        save_master_password(password)

        messagebox.showinfo(
            "Successo",
            "Master password creata correttamente."
        )

        open_main_window(root)

    create_button = ctk.CTkButton(
        auth_frame,
        text="Crea vault",
        command=create_master_password,
        width=320,
        height=42
    )
    create_button.pack(pady=(22, 35))

    root.bind("<Return>", lambda event: create_master_password())


def show_login_screen(root):
    clear_window(root)

    root.geometry("520x380")

    auth_frame = ctk.CTkFrame(root, corner_radius=20)
    auth_frame.pack(expand=True, padx=40, pady=40)

    title_label = ctk.CTkLabel(
        auth_frame,
        text="Login",
        font=("Arial", 26, "bold")
    )
    title_label.pack(pady=(40, 8))

    subtitle_label = ctk.CTkLabel(
        auth_frame,
        text="Accedi al tuo vault sicuro",
        font=("Arial", 14),
        text_color="#A0A0A0"
    )
    subtitle_label.pack(pady=(0, 28))

    password_entry = ctk.CTkEntry(
        auth_frame,
        placeholder_text="Inserisci master password",
        show="*",
        width=320,
        height=42
    )
    password_entry.pack(pady=10)

    root.after(100, password_entry.focus_force)

    def login():
        password = password_entry.get()

        if verify_master_password(password):
            open_main_window(root)

        else:
            messagebox.showerror(
                "Errore",
                "Master password errata."
            )

            password_entry.delete(0, "end")
            password_entry.focus_force()

    login_button = ctk.CTkButton(
        auth_frame,
        text="Accedi",
        command=login,
        width=320,
        height=42
    )
    login_button.pack(pady=(22, 35))

    root.bind("<Return>", lambda event: login())


def main():
    create_table()
    create_auth_table()
    initialize_key()

    root = ctk.CTk()

    root.title("Password Manager")
    root.geometry("900x600")

    if master_password_exists():
        show_login_screen(root)
    else:
        show_create_master_password_screen(root)

    root.mainloop()


if __name__ == "__main__":
    main()