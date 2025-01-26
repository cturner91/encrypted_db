from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64


def _derive_key(key: str, salt: int) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=(salt).to_bytes(16, byteorder='big'),
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(key.encode()))


def encrypt_data(key: str, salt: int, data: str) -> str:
    fernet_key = _derive_key(key, salt)
    fernet = Fernet(fernet_key)
    encrypted_data = fernet.encrypt(data.encode())
    encrypted_base64 = base64.b64encode(encrypted_data).decode('utf-8')
    return encrypted_base64


def decrypt_data(key: str, salt: int, encrypted_data: str) -> str:
    fernet_key = _derive_key(key, salt)
    fernet = Fernet(fernet_key)
    content = base64.b64decode(encrypted_data.encode('utf-8'))
    return fernet.decrypt(content).decode()
