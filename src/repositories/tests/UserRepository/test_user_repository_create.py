from DomainModel.entities.User import User
from repositories import user_repository
from tests.dummies import generate_dummy_user_list
from bson.objectid import ObjectId


def test_success():
    # Arrange
    dummy_user = generate_dummy_user_list()[0]

    # Act
    result = user_repository.create(
        dummy_user,
    )

    # Assert
    assert isinstance(result, User)
    assert type(result._id) == ObjectId
    assert result.line_user_name == dummy_user.line_user_name
    assert result.line_user_id == dummy_user.line_user_id
    assert result.mode == dummy_user.mode
    assert result.jantama_name == dummy_user.jantama_name

    record_on_db = user_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0].line_user_name == dummy_user.line_user_name
    assert record_on_db[0].line_user_id == dummy_user.line_user_id
    assert record_on_db[0].mode == dummy_user.mode
    assert record_on_db[0].jantama_name == dummy_user.jantama_name
