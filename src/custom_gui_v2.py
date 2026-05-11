import customtkinter as ctk
from tkinter import messagebox

from database import (
    create_table,
    get_all_credentials,
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


class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.selected_credential = None
        self.selected_card = None
        self.selected_index = -1
        self.credential_cards = []

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_layout(self):
        self.clear_window()

        main_container = ctk.CTkFrame(self.root, corner_radius=0)
        main_container.pack(fill="both", expand=True)

        sidebar = ctk.CTkFrame(main_container, width=300, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo_label = ctk.CTkLabel(
            sidebar,
            text="Password Manager",
            font=("Arial", 24, "bold")
        )
        logo_label.pack(pady=(40, 10), padx=20)

        subtitle_label = ctk.CTkLabel(
            sidebar,
            text="Vault sicuro locale",
            text_color="#A0A0A0",
            font=("Arial", 14)
        )
        subtitle_label.pack(pady=(0, 35))

        all_button = ctk.CTkButton(
            sidebar,
            text="Tutte le credenziali",
            height=42,
            command=lambda: load_credentials()
        )
        all_button.pack(fill="x", padx=20, pady=8)

        recent_button = ctk.CTkButton(
            sidebar,
            text="Recenti",
            height=42,
            fg_color="#2b2b2b",
            hover_color="#3a3a3a",
            command=lambda: show_recent_credentials()
        )
        recent_button.pack(fill="x", padx=20, pady=8)

        weak_button = ctk.CTkButton(
            sidebar,
            text="Password deboli",
            height=42,
            fg_color="#2b2b2b",
            hover_color="#3a3a3a",
            command=lambda: show_weak_passwords()
        )
        weak_button.pack(fill="x", padx=20, pady=8)

        settings_button = ctk.CTkButton(
            sidebar,
            text="Impostazioni",
            height=42,
            fg_color="#2b2b2b",
            hover_color="#3a3a3a",
            command=lambda: show_settings_placeholder()
        )
        settings_button.pack(fill="x", padx=20, pady=8)

        logout_button = ctk.CTkButton(
            sidebar,
            text="Logout",
            height=42,
            fg_color="#b23b3b",
            hover_color="#8f2f2f",
            command=self.show_login_screen
        )
        logout_button.pack(side="bottom", fill="x", padx=20, pady=25)

        content_area = ctk.CTkFrame(main_container, fg_color="transparent")
        content_area.pack(side="left", fill="both", expand=True)

        topbar = ctk.CTkFrame(content_area, height=90)
        topbar.pack(fill="x", padx=25, pady=25)
        topbar.pack_propagate(False)

        search_entry = ctk.CTkEntry(
            topbar,
            placeholder_text="Cerca sito/app...",
            height=44,
            width=420
        )
        search_entry.pack(side="left", padx=20, pady=20)

        def load_credentials(credentials=None):
            for widget in credentials_list.winfo_children():
                widget.destroy()

            self.selected_credential = None
            self.selected_card = None
            self.selected_index = -1
            self.credential_cards = []

            self.detail_site.configure(text="Seleziona una credenziale")
            self.detail_username.configure(text="Username:")
            self.detail_password.configure(text="Password: ********")
            self.detail_notes.configure(text="Note:")
            show_button.configure(text="Mostra password")

            if credentials is None:
                credentials = get_all_credentials()

            if not credentials:
                empty_label = ctk.CTkLabel(
                    credentials_list,
                    text="Nessuna credenziale trovata.",
                    text_color="#A0A0A0"
                )
                empty_label.pack(pady=30)
                return

            for credential in credentials:
                add_credential_card(credential)

        def show_recent_credentials():
            search_entry.delete(0, "end")

            credentials = get_all_credentials()
            recent_credentials = sorted(
                credentials,
                key=lambda credential: credential[0],
                reverse=True
            )[:5]

            load_credentials(recent_credentials)

        def is_weak_password(password):
            if len(password) < 8:
                return True

            has_digit = any(char.isdigit() for char in password)
            has_upper = any(char.isupper() for char in password)
            has_lower = any(char.islower() for char in password)
            has_symbol = any(not char.isalnum() for char in password)

            return not (has_digit and has_upper and has_lower and has_symbol)

        def show_weak_passwords():
            credentials = get_all_credentials()
            weak_credentials = [
                credential for credential in credentials
                if is_weak_password(credential[3])
            ]
            load_credentials(weak_credentials)

        def show_settings_placeholder():
            for widget in credentials_list.winfo_children():
                widget.destroy()

            self.selected_credential = None
            self.selected_card = None
            self.selected_index = -1
            self.credential_cards = []

            self.detail_site.configure(text="Impostazioni")
            self.detail_username.configure(text="")
            self.detail_password.configure(text="")
            self.detail_notes.configure(text="Qui potrai configurare auto-lock, tema, clipboard e backup.")

            settings_label = ctk.CTkLabel(
                credentials_list,
                text="Impostazioni in sviluppo",
                font=("Arial", 20, "bold")
            )
            settings_label.pack(pady=(40, 10))

            settings_info = ctk.CTkLabel(
                credentials_list,
                text="In questa sezione aggiungeremo preferenze, sicurezza e backup.",
                text_color="#A0A0A0"
            )
            settings_info.pack(pady=10)

        def search_credentials_from_entry(event=None):
            search_text = search_entry.get().strip().lower()
            all_credentials = get_all_credentials()

            if search_text:
                filtered_credentials = [
                    credential for credential in all_credentials
                    if credential[1].lower().startswith(search_text)
                ]
                load_credentials(filtered_credentials)
            else:
                load_credentials(all_credentials)

        def add_credential_card(credential):
            credential_id = credential[0]
            site = credential[1]
            username = credential[2]
            password = credential[3]
            notes = credential[4] if credential[4] else "Nessuna nota"

            card = ctk.CTkFrame(credentials_list, corner_radius=14)
            card.pack(fill="x", padx=10, pady=8)

            site_label = ctk.CTkLabel(
                card,
                text=site,
                font=("Arial", 18, "bold")
            )
            site_label.pack(anchor="w", padx=18, pady=(16, 4))

            username_label = ctk.CTkLabel(
                card,
                text=username,
                text_color="#B0B0B0"
            )
            username_label.pack(anchor="w", padx=18)

            password_label = ctk.CTkLabel(
                card,
                text="********",
                font=("Arial", 15)
            )
            password_label.pack(anchor="w", padx=18, pady=(8, 16))

            card_info = {
                "card": card,
                "credential": credential
            }
            self.credential_cards.append(card_info)

            def select_card(event=None, info=card_info):
                if self.selected_card is not None and self.selected_card.winfo_exists():
                    self.selected_card.configure(border_width=0)

                card_widget = info["card"]
                cred = info["credential"]

                self.selected_card = card_widget
                self.selected_index = self.credential_cards.index(info)

                card_widget.configure(border_width=2, border_color="#1f6aa5")

                self.selected_credential = {
                    "id": cred[0],
                    "site": cred[1],
                    "username": cred[2],
                    "password": cred[3],
                    "notes": cred[4] if cred[4] else "Nessuna nota",
                    "visible": False
                }

                self.detail_site.configure(text=cred[1])
                self.detail_username.configure(text=f"Username: {cred[2]}")
                self.detail_password.configure(text="Password: ********")

                note_text = cred[4] if cred[4] else "Nessuna nota"
                self.detail_notes.configure(text=f"Note: {note_text}")
                show_button.configure(text="Mostra password")

            card.bind("<Button-1>", select_card)
            site_label.bind("<Button-1>", select_card)
            username_label.bind("<Button-1>", select_card)
            password_label.bind("<Button-1>", select_card)
        def move_selection(direction):
            if not self.credential_cards:
                return

            if direction == "down":
                if self.selected_index == -1:
                    next_index = 0
                else:
                    next_index = min(self.selected_index + 1, len(self.credential_cards) - 1)
            else:
                if self.selected_index == -1:
                    next_index = 0
                else:
                    next_index = max(self.selected_index - 1, 0)

            card_info = self.credential_cards[next_index]
            card = card_info["card"]
            credential = card_info["credential"]

            if self.selected_card is not None and self.selected_card.winfo_exists():
                self.selected_card.configure(border_width=0)

            self.selected_card = card
            self.selected_index = next_index
            card.configure(border_width=2, border_color="#1f6aa5")

            self.selected_credential = {
                "id": credential[0],
                "site": credential[1],
                "username": credential[2],
                "password": credential[3],
                "notes": credential[4] if credential[4] else "Nessuna nota",
                "visible": False
            }

            self.detail_site.configure(text=credential[1])
            self.detail_username.configure(text=f"Username: {credential[2]}")
            self.detail_password.configure(text="Password: ********")

            note_text = credential[4] if credential[4] else "Nessuna nota"
            self.detail_notes.configure(text=f"Note: {note_text}")
            show_button.configure(text="Mostra password")

            if len(self.credential_cards) > 1:
                scroll_position = next_index / (len(self.credential_cards) - 1)
                credentials_list._parent_canvas.yview_moveto(scroll_position)

        credentials_section = ctk.CTkFrame(content_area)
        credentials_section.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        credentials_list = ctk.CTkScrollableFrame(
            credentials_section,
            width=520
        )
        credentials_list.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        detail_panel = ctk.CTkFrame(credentials_section, width=360)
        detail_panel.pack(side="right", fill="y", padx=(0, 20), pady=20)
        detail_panel.pack_propagate(False)

        self.detail_site = None
        self.detail_username = None
        self.detail_password = None
        self.detail_notes = None

        detail_title = ctk.CTkLabel(
            detail_panel,
            text="Dettagli credenziale",
            font=("Arial", 22, "bold")
        )
        detail_title.pack(anchor="w", padx=25, pady=(30, 25))

        self.detail_site = ctk.CTkLabel(
            detail_panel,
            text="Seleziona una credenziale",
            font=("Arial", 20, "bold")
        )
        self.detail_site.pack(anchor="w", padx=25, pady=(0, 10))

        self.detail_username = ctk.CTkLabel(
            detail_panel,
            text="Username:",
            text_color="#B0B0B0"
        )
        self.detail_username.pack(anchor="w", padx=25, pady=6)

        self.detail_password = ctk.CTkLabel(
            detail_panel,
            text="Password: ********"
        )
        self.detail_password.pack(anchor="w", padx=25, pady=6)

        self.detail_notes = ctk.CTkLabel(
            detail_panel,
            text="Note:",
            wraplength=280,
            justify="left"
        )
        self.detail_notes.pack(anchor="w", padx=25, pady=(6, 25))

        def toggle_password_visibility():
            if self.selected_credential is None:
                messagebox.showerror("Errore", "Seleziona una credenziale.")
                return

            if self.selected_credential["visible"]:
                self.detail_password.configure(text="Password: ********")
                self.selected_credential["visible"] = False
                show_button.configure(text="Mostra password")
            else:
                self.detail_password.configure(text=f"Password: {self.selected_credential['password']}")
                self.selected_credential["visible"] = True
                show_button.configure(text="Nascondi password")

        def copy_selected_password():
            if self.selected_credential is None:
                messagebox.showerror("Errore", "Seleziona una credenziale.")
                return

            self.root.clipboard_clear()
            self.root.clipboard_append(self.selected_credential["password"])
            self.root.update()
            messagebox.showinfo("Successo", "Password copiata negli appunti.")

        def open_add_credential_window():
            add_window = ctk.CTkToplevel(self.root)
            add_window.title("Aggiungi credenziale")
            add_window.geometry("420x420")
            add_window.transient(self.root)
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

            self.root.after(100, site_entry.focus_force)

            def save_credential():
                site = site_entry.get().strip()
                username = username_entry.get().strip()
                password = password_entry.get().strip()
                notes = notes_entry.get().strip()

                if not site or not username or not password:
                    messagebox.showerror("Errore", "Sito, username e password sono obbligatori.")
                    return

                add_credential(site, username, password, notes)
                messagebox.showinfo("Successo", "Credenziale aggiunta correttamente.")
                add_window.destroy()
                load_credentials()

            save_button = ctk.CTkButton(add_window, text="Salva", command=save_credential, width=320, height=40)
            save_button.pack(pady=22)
            add_window.bind("<Return>", lambda event: save_credential())

        def delete_selected_credential():
            if self.selected_credential is None:
                messagebox.showerror("Errore", "Seleziona una credenziale da eliminare.")
                return

            confirm = messagebox.askyesno(
                "Conferma eliminazione",
                "Sei sicuro di voler eliminare questa credenziale?"
            )

            if confirm:
                deleted = delete_credential(int(self.selected_credential["id"]))

                if deleted:
                    messagebox.showinfo("Successo", "Credenziale eliminata correttamente.")
                    load_credentials()
                else:
                    messagebox.showerror("Errore", "Credenziale non trovata.")

        def open_update_password_window():
            if self.selected_credential is None:
                messagebox.showerror("Errore", "Seleziona una credenziale da modificare.")
                return

            update_window = ctk.CTkToplevel(self.root)
            update_window.title("Modifica password")
            update_window.geometry("420x250")
            update_window.transient(self.root)
            update_window.grab_set()
            update_window.focus_force()

            title = ctk.CTkLabel(update_window, text="Modifica password", font=("Arial", 22, "bold"))
            title.pack(pady=(28, 18))

            password_entry = ctk.CTkEntry(
                update_window,
                placeholder_text="Nuova password",
                show="*",
                width=320,
                height=40
            )
            password_entry.pack(pady=10)

            self.root.after(100, password_entry.focus_force)

            def save_new_password():
                new_password = password_entry.get().strip()

                if not new_password:
                    messagebox.showerror("Errore", "La password non può essere vuota.")
                    return

                updated = update_password(int(self.selected_credential["id"]), new_password)

                if updated:
                    messagebox.showinfo("Successo", "Password aggiornata correttamente.")
                    update_window.destroy()
                    load_credentials()
                else:
                    messagebox.showerror("Errore", "Credenziale non trovata.")

            save_button = ctk.CTkButton(update_window, text="Salva", command=save_new_password, width=320, height=40)
            save_button.pack(pady=20)
            update_window.bind("<Return>", lambda event: save_new_password())

        show_button = ctk.CTkButton(
            detail_panel,
            text="Mostra password",
            height=42,
            command=toggle_password_visibility
        )
        show_button.pack(fill="x", padx=25, pady=8)

        copy_button = ctk.CTkButton(
            detail_panel,
            text="Copia password",
            height=42,
            command=copy_selected_password
        )
        copy_button.pack(fill="x", padx=25, pady=8)

        update_button = ctk.CTkButton(
            detail_panel,
            text="Modifica password",
            height=42,
            command=open_update_password_window
        )
        update_button.pack(fill="x", padx=25, pady=8)

        delete_button = ctk.CTkButton(
            detail_panel,
            text="Elimina",
            height=42,
            fg_color="#b23b3b",
            hover_color="#8f2f2f",
            command=delete_selected_credential
        )
        delete_button.pack(fill="x", padx=25, pady=8)

        add_button = ctk.CTkButton(
            topbar,
            text="+ Aggiungi",
            width=140,
            height=44,
            command=open_add_credential_window
        )
        add_button.pack(side="right", padx=20, pady=20)

        search_entry.bind("<KeyRelease>", search_credentials_from_entry)
        self.root.bind("<Down>", lambda event: move_selection("down"))
        self.root.bind("<Up>", lambda event: move_selection("up"))

        load_credentials()

    def show_create_master_password_screen(self):
        self.clear_window()

        auth_container = ctk.CTkFrame(self.root, fg_color="transparent")
        auth_container.pack(fill="both", expand=True)

        auth_frame = ctk.CTkFrame(auth_container, corner_radius=20)
        auth_frame.place(relx=0.5, rely=0.5, anchor="center")

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

        self.root.after(100, password_entry.focus_force)

        def create_master_password():
            password = password_entry.get()
            confirm_password = confirm_entry.get()

            if not password or not confirm_password:
                messagebox.showerror("Errore", "Compila tutti i campi.")
                return

            if password != confirm_password:
                messagebox.showerror("Errore", "Le password non coincidono.")
                return

            save_master_password(password)

            messagebox.showinfo(
                "Successo",
                "Master password creata correttamente."
            )

            self.show_main_layout()

        create_button = ctk.CTkButton(
            auth_frame,
            text="Crea vault",
            command=create_master_password,
            width=320,
            height=42
        )
        create_button.pack(pady=(22, 35))

        self.root.bind("<Return>", lambda event: create_master_password())

    def show_login_screen(self):
        self.clear_window()

        auth_container = ctk.CTkFrame(self.root, fg_color="transparent")
        auth_container.pack(fill="both", expand=True)

        auth_frame = ctk.CTkFrame(auth_container, corner_radius=20)
        auth_frame.place(relx=0.5, rely=0.5, anchor="center")

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

        self.root.after(100, password_entry.focus_force)

        def login():
            password = password_entry.get()

            if verify_master_password(password):
                self.show_main_layout()

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

        self.root.bind("<Return>", lambda event: login())


def main():
    create_table()
    create_auth_table()
    initialize_key()

    root = ctk.CTk()

    root.title("Password Manager")
    root.geometry("1300x750")
    root.minsize(1200, 700)

    app = PasswordManagerApp(root)

    if master_password_exists():
        app.show_login_screen()
    else:
        app.show_create_master_password_screen()

    root.mainloop()


if __name__ == "__main__":
    main()