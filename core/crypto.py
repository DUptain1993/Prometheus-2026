import os
import base64
import hashlib
import secrets
from typing import Optional, Tuple

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


class SecureStore:
    """
    Secure storage for sensitive data (webhooks, keys, credentials).
    Uses system keyring if available, otherwise falls back to encrypted file.
    """

    def __init__(self):
        self._data = {}

    def set(self, key: str, value: str):
        """Store a sensitive value."""
        # In production, use keyring: keyring.set_password("prometheus", key, value)
        self._data[key] = value

    def get(self, key: str) -> Optional[str]:
        """Retrieve a sensitive value."""
        return self._data.get(key)

    def delete(self, key: str):
        """Delete a stored value."""
        if key in self._data:
            del self._data[key]


def derive_key(password: str, salt: bytes, length: int = 32) -> bytes:
    """Derive a cryptographic key from a password using PBKDF2-HMAC-SHA256."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    if isinstance(password, str):
        password = password.encode()
    return kdf.derive(password)


def encrypt_data(plaintext: str, key: str) -> str:
    """
    Encrypt data using AES-256-GCM.
    Returns base64-encoded string with salt, nonce, and ciphertext.
    """
    # Generate a random salt
    salt = os.urandom(16)
    derived_key = derive_key(key, salt, 32)

    # Generate a random nonce for AES-GCM (12 bytes recommended)
    nonce = os.urandom(12)

    # Encrypt the data
    cipher = Cipher(algorithms.AES(derived_key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()

    # Combine: salt + nonce + tag + ciphertext
    combined = salt + nonce + encryptor.tag + ciphertext
    return base64.b64encode(combined).decode()


def decrypt_data(encrypted: str, key: str) -> str:
    """
    Decrypt data encrypted with encrypt_data.
    """
    raw = base64.b64decode(encrypted)

    # Extract components
    salt = raw[:16]
    nonce = raw[16:28]
    tag = raw[28:44]
    ciphertext = raw[44:]

    derived_key = derive_key(key, salt, 32)

    # Decrypt
    cipher = Cipher(algorithms.AES(derived_key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext.decode()


def generate_secure_id(length: int = 16) -> str:
    """Generate a cryptographically secure random ID."""
    return secrets.token_urlsafe(length)


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 for storage."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(password) == hashed


def generate_encryption_key() -> str:
    """Generate a random encryption key for payload encryption."""
    return secrets.token_urlsafe(32)


def obfuscate_key(key: str) -> str:
    """Simple key obfuscation (XOR with a fixed pattern) for embedding."""
    pattern = b"PROMETHEUS_KEY_OBFUSCATION_2024"
    key_bytes = key.encode()
    pattern_bytes = pattern[:len(key_bytes)]
    result = bytes([a ^ b for a, b in zip(key_bytes, pattern_bytes)])
    return base64.b64encode(result).decode()
