from tests.dummies import generate_dummy_user
from db_setting import Session
from repositories import session_scope
from repositories.UserRepository import UserRepository

session = Session()


def test_success():
    # Arrange
    dummy_user = generate_dummy_user()

    # Act
    with session_scope() as session:
        UserRepository.create(
            session,
            dummy_user,
        )

    # Assert
    with session_scope() as session:
        result = UserRepository.find_all(
            session,
        )
        assert len(result) == 1
        assert result[0].name == dummy_user.name
        assert result[0].line_user_id == dummy_user.line_user_id
        assert result[0].zoom_url == dummy_user.zoom_url
        assert result[0].mode == dummy_user.mode
        assert result[0].jantama_name == dummy_user.jantama_name
