import hashlib

from config import settings


class CipherRepository:
    def __init__(self):
        self.salt = settings.cipher_settings.salt

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(self.salt.encode() + password.encode()).hexdigest()
