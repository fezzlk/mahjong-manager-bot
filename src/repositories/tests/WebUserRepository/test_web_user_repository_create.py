from tests.dummies import generate_dummy_web_user_list
from DomainModel.entities.WebUser import WebUser
from repositories import web_user_repository
from bson.objectid import ObjectId


def test_success():
    # Arrange
    dummy_web_user = generate_dummy_web_user_list()[0]

    # Act
    result = web_user_repository.create(
        dummy_web_user,
    )

    # Assert
    assert isinstance(result, WebUser)
    assert type(result._id) == ObjectId
    assert result.user_code == dummy_web_user.user_code
    assert result.name == dummy_web_user.name
    assert result.email == dummy_web_user.email
    assert result.linked_line_user_id == dummy_web_user.linked_line_user_id
    assert result.is_approved_line_user == dummy_web_user.is_approved_line_user
    assert result.created_at == dummy_web_user.created_at
    assert result.updated_at == dummy_web_user.updated_at

    record_on_db = web_user_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0].user_code == dummy_web_user.user_code
    assert record_on_db[0].name == dummy_web_user.name
    assert record_on_db[0].email == dummy_web_user.email
    assert record_on_db[0].linked_line_user_id == dummy_web_user.linked_line_user_id
    assert record_on_db[0].is_approved_line_user == dummy_web_user.is_approved_line_user
