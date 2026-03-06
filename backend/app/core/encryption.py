"""
app/core/encryption.py
AES-256-GCM field-level encryption for PDPA-sensitive data.
Encrypts: email, full_name, biometric tokens.
"""
import os
import base64
import hmac as _hmac
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.core.config import settings


class FieldEncryptor:
    def __init__(self) -> None:
        if not settings.ENCRYPTION_KEY_B64:
            raise ValueError("ENCRYPTION_KEY_B64 must be set in .env — never use a random key in any environment")
        self._key = base64.b64decode(settings.ENCRYPTION_KEY_B64)
        assert len(self._key) == 32, "ENCRYPTION_KEY_B64 must decode to exactly 32 bytes"

    def encrypt(self, plaintext: str) -> str:
        nonce = os.urandom(12)
        aesgcm = AESGCM(self._key)
        ct = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
        return base64.b64encode(nonce + ct).decode("utf-8")

    def decrypt(self, ciphertext_b64: str) -> str:
        data = base64.b64decode(ciphertext_b64)
        nonce, ct = data[:12], data[12:]
        aesgcm = AESGCM(self._key)
        return aesgcm.decrypt(nonce, ct, None).decode("utf-8")


# Singleton
encryptor = FieldEncryptor()


def hmac_email(email: str) -> str:
    """Deterministic keyed hash for email lookups. Never used for display."""
    key = settings.SECRET_KEY.encode()
    return _hmac.new(key, email.strip().lower().encode(), hashlib.sha256).hexdigest()
