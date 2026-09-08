# fast_zero/infrastructure/repositories/sqlalchemy_user_repository.py
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.models import User
from fast_zero.schemas import UserCreate, UserDb


class SQLAlchemyUserRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: UserCreate) -> UserDb:
        db_user = User(
            username=user.username,
            email=user.email,
            password=user.password_hash,  # já vem hasheada
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return self._to_user_db(db_user)

    def list_all(self) -> list[UserDb]:
        db_users = self.session.scalars(select(User)).all()
        return [self._to_user_db(db_user) for db_user in db_users]

    def get_by_id(self, user_id: int) -> UserDb | None:
        db_user = self.session.scalar(select(User).where(User.id == user_id))
        if db_user is None:
            return None
        return self._to_user_db(db_user)

    def update(self, user_id: int, user: UserCreate) -> UserDb | None:
        db_user = self.session.scalar(select(User).where(User.id == user_id))
        if db_user is None:
            return None

        db_user.username = user.username
        db_user.email = user.email
        db_user.password = user.password_hash

        self.session.commit()
        self.session.refresh(db_user)
        return self._to_user_db(db_user)

    def delete(self, user_id: int) -> bool:
        db_user = self.session.scalar(select(User).where(User.id == user_id))
        if db_user is None:
            return False

        self.session.delete(db_user)
        self.session.commit()
        return True

    @staticmethod
    def _to_user_db(db_user: User) -> UserDb:
        return UserDb(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            password_hash=db_user.password,
        )