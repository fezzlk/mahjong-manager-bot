from DomainModel.entities.User import User, UserMode
from repositories import user_repository
from tests.dummies import generate_dummy_user_list
from bson.objectid import ObjectId
import pytest


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
    assert type(record_on_db[0]._id) == ObjectId
    assert record_on_db[0].line_user_name == dummy_user.line_user_name
    assert record_on_db[0].line_user_id == dummy_user.line_user_id
    assert record_on_db[0].mode == dummy_user.mode
    assert record_on_db[0].jantama_name == dummy_user.jantama_name


def test_success_with_id():
    # Arrange
    dummy_user = User(
        line_user_name="test_user1",
        line_user_id="U0123456789abcdefghijklmnopqrstu1",
        mode=UserMode.wait.value,
        jantama_name="jantama_user1",
        _id=ObjectId('644c838186bbd9e20a91b783'),
    )

    # Act
    result = user_repository.create(
        dummy_user,
    )

    # Assert
    assert isinstance(result, User)
    assert result._id == dummy_user._id
    assert result.line_user_name == dummy_user.line_user_name
    assert result.line_user_id == dummy_user.line_user_id
    assert result.mode == dummy_user.mode
    assert result.jantama_name == dummy_user.jantama_name

    record_on_db = user_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0]._id == dummy_user._id
    assert record_on_db[0].line_user_name == dummy_user.line_user_name
    assert record_on_db[0].line_user_id == dummy_user.line_user_id
    assert record_on_db[0].mode == dummy_user.mode
    assert record_on_db[0].jantama_name == dummy_user.jantama_name


def test_error_duplicate_line_line_id():
    with pytest.raises(Exception):
        # Arrange
        dummy_users = [
            User(
                line_user_name="test_user1",
                line_user_id="U0123456789abcdefghijklmnopqrstu1",
                mode=UserMode.wait.value,
                jantama_name="jantama_user1",
            ),
            User(
                line_user_name="test_user2",
                line_user_id="U0123456789abcdefghijklmnopqrstu1",
                mode=UserMode.wait.value,
                jantama_name="jantama_user2",
            ),
        ]
        user_repository.create(
            dummy_users[0],
        )

        # Act
        user_repository.create(
            dummy_users[1],
        )

    # Assert
    record_on_db = user_repository.find()
    assert len(record_on_db) == 1
    