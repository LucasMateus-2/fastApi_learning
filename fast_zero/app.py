# fast_zero/app.py
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from fast_zero.application.interfaces.password_hasher import PasswordHasher
from fast_zero.application.interfaces.user_repository import UserRepository
from fast_zero.application.use_cases.create_user import CreateUserUseCase
from fast_zero.application.use_cases.delete_user import DeleteUserUseCase
from fast_zero.application.use_cases.get_user_by_id import GetUserByIdUseCase
from fast_zero.application.use_cases.list_users import ListUsersUseCase
from fast_zero.application.use_cases.update_user import UpdateUserUseCase
from fast_zero.domain.exceptions.user_exceptions import UserNotFoundError
from fast_zero.infrastructure.database.session import get_session
from fast_zero.infrastructure.repositories.sql_alchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from fast_zero.infrastructure.security.pwd_hasher import PwdlibHasher
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()


# ---------------------------------------------------------------------------
# Dependências de infraestrutura
# ---------------------------------------------------------------------------
def get_repository(
    session: Session = Depends(get_session),
) -> UserRepository:
    return SQLAlchemyUserRepository(session)


def get_password_hasher() -> PasswordHasher:
    return PwdlibHasher()


# ---------------------------------------------------------------------------
# Factories dos Use Cases
# ---------------------------------------------------------------------------
def get_create_user_use_case(
    repository: UserRepository = Depends(get_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
) -> CreateUserUseCase:
    return CreateUserUseCase(repository, hasher)


def get_list_users_use_case(
    repository: UserRepository = Depends(get_repository),
) -> ListUsersUseCase:
    return ListUsersUseCase(repository)


def get_user_by_id_use_case(
    repository: UserRepository = Depends(get_repository),
) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(repository)


def get_update_user_use_case(
    repository: UserRepository = Depends(get_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
) -> UpdateUserUseCase:
    return UpdateUserUseCase(repository, hasher)


def get_delete_user_use_case(
    repository: UserRepository = Depends(get_repository),
) -> DeleteUserUseCase:
    return DeleteUserUseCase(repository)


# ---------------------------------------------------------------------------
# Rotas
# ---------------------------------------------------------------------------
@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(
    user: UserSchema,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
):
    return use_case.execute(user)


@app.get('/users/', response_model=UserList)
def read_users(
    use_case: ListUsersUseCase = Depends(get_list_users_use_case),
):
    return {'users': use_case.execute()}


@app.get('/users/{user_id}', response_model=UserPublic)
def get_username_by_id(
    user_id: int,
    use_case: GetUserByIdUseCase = Depends(get_user_by_id_use_case),
):
    try:
        return use_case.execute(user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    use_case: UpdateUserUseCase = Depends(get_update_user_use_case),
):
    try:
        return use_case.execute(user_id, user)
    except UserNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='USER NOT FOUND'
        )


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    use_case: DeleteUserUseCase = Depends(get_delete_user_use_case),
):
    try:
        use_case.execute(user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='USER NOT FOUND'
        )
    return {'message': 'user deleted'}