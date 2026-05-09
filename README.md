# Password Manager

A local password manager written in Python.

## Features

- Add credentials
- View saved credentials
- Search credentials
- Delete credentials
- Update credential passwords
- SQLite local storage
- Master password authentication
- SHA-256 master password hashing
- Password encryption using Fernet
- Hide/show password in GUI
- Copy password to clipboard
- Integrated real-time search bar
- Interactive CLI interface
- Modern CustomTkinter GUI

## Technologies

- Python
- SQLite
- Cryptography (Fernet)
- Git & GitHub
- Tkinter
- CustomTkinter

## Security Features

- Master password is not stored in plain text
- Stored credentials are encrypted
- Password input hidden using `getpass`

## Current Status

The project currently supports:
- Local encrypted credential storage
- Authentication system
- Password encryption/decryption
- Full CRUD operations through CLI
- Functional CustomTkinter GUI
- Password masking/unmasking
- Clipboard password copy
- Integrated search system

## Planned Improvements

- Password generator
- Better input validation
- Improve CustomTkinter GUI layout and styling
- Stronger key derivation (Argon2/PBKDF2)
- AES-GCM encryption
- Auto-lock system

## Note

This project was created for fun and learning purposes and is still under development.