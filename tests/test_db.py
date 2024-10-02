from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='lucas', email='lucas@email', password='minha_senha-legal'
    )
    session.add(user)
    session.commit()
    result = session.scalar(select(User).where(User.email == 'lucas@email'))

    assert result.username == 'lucas'
    assert user.id == 1
