# fast_zero/application/use_cases/delete_user.py
from fast_zero.application.interfaces.user_repository import UserRepository
from fast_zero.domain.exceptions.user_exceptions import UserNotFoundError


class DeleteUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user_id: int) -> None:
        deleted = self.repository.delete(user_id)
        if not deleted:
            raise UserNotFoundError(user_id)