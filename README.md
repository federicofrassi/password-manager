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
- Interactive CLI interface

## Technologies

- Python
- SQLite
- Cryptography (Fernet)
- Git & GitHub

## Security Features

- Master password is not stored in plain text
- Stored credentials are encrypted
- Password input hidden using `getpass`

## Current Status

The project currently supports:
- Local encrypted credential storage
- Authentication system
- Password encryption/decryption
- CRUD operations through CLI

## Planned Improvements

- Password generator
- Hide/show password option
- Clipboard support
- Better input validation
- GUI interface
- Stronger key derivation (Argon2/PBKDF2)
- AES-GCM encryption
- Auto-lock system

## Note

This project was created for fun and learning purposes and is still under development.