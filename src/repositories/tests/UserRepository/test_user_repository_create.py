from tests.dummies import generate_dummy_user_list
from db_setting import Session
from repositories import session_scope, user_repository

session = Session()


def test_success():
    # Arrange
    dummy_user = generate_dummy_user_list()[0]

    # Act
    with session_scope() as session:
        user_repository.create(
            session,
            dummy_user,
        )

    # Assert
    with session_scope() as session:
        result = user_repository.find_all(
            session,
        )
        assert len(result) == 1
        assert result[0].name == dummy_user.name
        assert result[0].line_user_id == dummy_user.line_user_id
        assert result[0].zoom_url == dummy_user.zoom_url
        assert result[0].mode == dummy_user.mode
        assert result[0].jantama_name == dummy_user.jantama_name
