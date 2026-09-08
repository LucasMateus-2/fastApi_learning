# fast_zero/application/use_cases/list_users.py
from fast_zero.application.interfaces.user_repository import UserRepository
from fast_zero.schemas import UserDb


class ListUsersUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self) -> list[UserDb]:
        return self.repository.list_all()