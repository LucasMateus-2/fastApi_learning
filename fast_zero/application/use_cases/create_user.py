# fast_zero/application/use_cases/create_user.py
from fast_zero.application.interfaces.password_hasher import PasswordHasher
from fast_zero.application.interfaces.user_repository import UserRepository
from fast_zero.schemas import UserCreate, UserDb, UserSchema


class CreateUserUseCase:
    def __init__(self, repository: UserRepository, hasher: PasswordHasher):
        self.repository = repository
        self.hasher = hasher

    def execute(self, user: UserSchema) -> UserDb:
        user_create = UserCreate(
            username=user.username,
            email=user.email,
            password_hash=self.hasher.hash(user.password),
        )
        return self.repository.add(user_create)