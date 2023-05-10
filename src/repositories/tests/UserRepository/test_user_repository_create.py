from DomainModel.entities.User import User
from tests.dummies import generate_dummy_user_list
from repositories import session_scope, user_repository


def test_success():
    # Arrange
    dummy_user = generate_dummy_user_list()[0]

    # Act
    with session_scope() as session:
        result = user_repository.create(
            session,
            dummy_user,
        )

    # Assert
    assert isinstance(result, User)
    assert result._id == dummy_user._id
    assert result.line_user_name == dummy_user.line_user_name
    assert result.line_user_id == dummy_user.line_user_id
    assert result.mode == dummy_user.mode
    assert result.jantama_name == dummy_user.jantama_name

    with session_scope() as session:
        record_on_db = user_repository.find(
            session,
        )
        assert len(record_on_db) == 1
        assert record_on_db[0]._id == dummy_user._id
        assert record_on_db[0].line_user_name == dummy_user.line_user_name
        assert record_on_db[0].line_user_id == dummy_user.line_user_id
        assert record_on_db[0].mode == dummy_user.mode
        assert record_on_db[0].jantama_name == dummy_user.jantama_name
