import hashlib
import secrets
from base64 import b64encode, b64decode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
from app.core.config import settings


def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()


def verify_api_key(api_key: str, hashed_key: str) -> bool:
    return hash_api_key(api_key) == hashed_key


def generate_api_key() -> str:
    return secrets.token_urlsafe(32)


def encrypt_secret(secret: str) -> str:
    """Encrypt a secret using the encryption key from settings"""
    try:
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"cloud-companion",
            iterations=100000,
            backend=default_backend(),
        )
        key = b64encode(kdf.derive(settings.ENCRYPTION_KEY.encode()))
        fernet = Fernet(key)
        encrypted = fernet.encrypt(secret.encode())
        return encrypted.decode()
    except Exception as e:
        raise ValueError(f"Encryption failed: {str(e)}")


def decrypt_secret(encrypted_secret: str) -> str:
    """Decrypt a secret using the encryption key from settings"""
    try:
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"cloud-companion",
            iterations=100000,
            backend=default_backend(),
        )
        key = b64encode(kdf.derive(settings.ENCRYPTION_KEY.encode()))
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_secret.encode())
        return decrypted.decode()
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")
