from tests.dummies import generate_dummy_user_list
from db_setting import Session
from repositories import session_scope, user_repository
from domains.User import User

session = Session()


def test_success_find_records():
    # Arrange
    with session_scope() as session:
        dummy_users = generate_dummy_user_list()
        for dummy_user in dummy_users:
            user_repository.create(
                session,
                dummy_user,
            )

    # Act
    with session_scope() as session:
        result = user_repository.find_all(
            session,
        )

    # Assert
        assert len(result) == len(dummy_users)
        for i in range(len(result)):
            assert isinstance(result[i], User)
            assert result[i].name == dummy_users[i].name
            assert result[i].line_user_id == dummy_users[i].line_user_id
            assert result[i].zoom_url == dummy_users[i].zoom_url
            assert result[i].mode == dummy_users[i].mode
            assert result[i].jantama_name == dummy_users[i].jantama_name


def test_success_find_0_record():
    # Arrange
    # Do nothing

    # Act
    with session_scope() as session:
        result = user_repository.find_all(
            session,
        )

    # Assert
        assert len(result) == 0
