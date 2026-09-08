# fast_zero/application/use_cases/update_user.py
from fast_zero.application.interfaces.password_hasher import PasswordHasher
from fast_zero.application.interfaces.user_repository import UserRepository
from fast_zero.domain.exceptions.user_exceptions import UserNotFoundError
from fast_zero.schemas import UserCreate, UserDb, UserSchema


class UpdateUserUseCase:
    def __init__(self, repository: UserRepository, hasher: PasswordHasher):
        self.repository = repository
        self.hasher = hasher

    def execute(self, user_id: int, user: UserSchema) -> UserDb:
        user_create = UserCreate(
            username=user.username,
            email=user.email,
            password_hash=self.hasher.hash(user.password),
        )
        updated = self.repository.update(user_id, user_create)
        if updated is None:
            raise UserNotFoundError(user_id)
        return updated