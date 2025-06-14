# utils/crypto.py
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_text(text, key):
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()

def decrypt_text(cipher_text, key):
    f = Fernet(key)
    return f.decrypt(cipher_text.encode()).decode()