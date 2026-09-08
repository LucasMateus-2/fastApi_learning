# fast_zero/application/use_cases/get_user_by_id.py
from fast_zero.application.interfaces.user_repository import UserRepository
from fast_zero.domain.exceptions.user_exceptions import UserNotFoundError
from fast_zero.schemas import UserDb


class GetUserByIdUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user_id: int) -> UserDb:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user