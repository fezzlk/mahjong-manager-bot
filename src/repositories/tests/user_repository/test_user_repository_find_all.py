from tests.dummies import generate_dummy_user_list
from db_setting import Session
from repositories import session_scope
from repositories.user_repository import UserRepository
from domains.user import User

session = Session()


def test_success_find_records():
    # Arrange
    with session_scope() as session:
        dummy_users = generate_dummy_user_list()
        for dummy_user in dummy_users:
            UserRepository.create(
                session,
                dummy_user,
            )

    # Act
    with session_scope() as session:
        result = UserRepository.find_all(
            session,
        )

    # Assert
        assert len(result) == len(dummy_users)
        for i in range(len(result)):
            assert isinstance(result[i], User)
            assert result[i].line_user_id == dummy_users[i].line_user_id
            assert result[i].zoom_url == dummy_users[i].zoom_url
            assert result[i].mode == dummy_users[i].mode


def test_success_find_0_record():
    # Arrange
    # Do nothing

    # Act
    with session_scope() as session:
        result = UserRepository.find_all(
            session,
        )

    # Assert
        assert len(result) == 0
