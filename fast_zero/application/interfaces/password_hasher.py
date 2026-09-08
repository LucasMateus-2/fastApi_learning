# fast_zero/application/interfaces/password_hasher.py
from typing import Protocol


class PasswordHasher(Protocol):
    def hash(self, plain_password: str) -> str: ...