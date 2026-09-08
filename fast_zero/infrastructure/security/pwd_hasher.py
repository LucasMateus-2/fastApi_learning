# fast_zero/infrastructure/security/pwd_hasher.py
from pwdlib import PasswordHash

_password_hash = PasswordHash.recommended()


class PwdlibHasher:
    def hash(self, plain_password: str) -> str:
        return _password_hash.hash(plain_password)