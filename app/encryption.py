from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import os


def derive_key(password: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=(123).to_bytes(2, byteorder='big'),
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_data(password: str, data: str) -> str:
    key = derive_key(password)
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    encrypted_base64 = base64.b64encode(encrypted_data).decode('utf-8')
    return encrypted_base64


def decrypt_data(password: str, encrypted_data: str) -> str:
    key = derive_key(password)
    fernet = Fernet(key)
    content = base64.b64decode(encrypted_data.encode('utf-8'))
    return fernet.decrypt(content).decode()
