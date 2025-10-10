import pytest
from bson.objectid import ObjectId
from dummies import (
    generate_dummy_hanchan_list,
    generate_dummy_user_list,
)

from DomainModel.entities.UserHanchan import UserHanchan
from repositories import (
    hanchan_repository,
    user_hanchan_repository,
    user_repository,
)

dummy_user = generate_dummy_user_list()[0]
dummy_hanchan = generate_dummy_hanchan_list()[0]


def test_success():
    # Arrange
    new_user = user_repository.create(
        dummy_user,
    )
    new_hanchan = hanchan_repository.create(
        dummy_hanchan,
    )
    dummy_user_hanchan = UserHanchan(
        line_user_id=new_user.line_user_id,
        hanchan_id=new_hanchan._id,
        point=40000,
        rank=1,
    )

    # Act
    result = user_hanchan_repository.create(
        dummy_user_hanchan,
    )

    # Assert
    assert isinstance(result, UserHanchan)
    assert type(result._id) is ObjectId
    assert result.line_user_id == dummy_user_hanchan.line_user_id
    assert result.hanchan_id == dummy_user_hanchan.hanchan_id

    record_on_db = user_hanchan_repository.find()
    assert len(record_on_db) == 1
    assert type(record_on_db[0]._id) is ObjectId
    assert record_on_db[0].line_user_id == dummy_user_hanchan.line_user_id
    assert record_on_db[0].hanchan_id == dummy_user_hanchan.hanchan_id


def test_success_with_id():
    # Arrange
    new_user = user_repository.create(
        dummy_user,
    )
    new_hanchan = hanchan_repository.create(
        dummy_hanchan,
    )
    dummy_user_hanchan = UserHanchan(
        line_user_id=new_user.line_user_id,
        hanchan_id=new_hanchan._id,
        point=10000,
        rank=4,
        yakuman_count=False,
        _id=ObjectId("644c838186bbd9e20a91b783"),
    )

    # Act
    result = user_hanchan_repository.create(
        dummy_user_hanchan,
    )

    # Assert
    assert isinstance(result, UserHanchan)
    assert result._id == dummy_user_hanchan._id
    assert result.line_user_id == dummy_user_hanchan.line_user_id
    assert result.hanchan_id == dummy_user_hanchan.hanchan_id

    record_on_db = user_hanchan_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0]._id == dummy_user_hanchan._id
    assert record_on_db[0].line_user_id == dummy_user_hanchan.line_user_id
    assert record_on_db[0].hanchan_id == dummy_user_hanchan.hanchan_id


def test_error_duplicate():
    with pytest.raises(Exception):
        # Arrange
        new_user = user_repository.create(
            dummy_user,
        )
        new_hanchan = hanchan_repository.create(
            dummy_hanchan,
        )
        dummy_user_hanchan = UserHanchan(
            line_user_id=new_user.line_user_id,
            hanchan_id=new_hanchan._id,
            point=1000,
            rank=4,
        )

        user_hanchan_repository.create(
            dummy_user_hanchan,
        )

        # Act
        user_hanchan_repository.create(
            dummy_user_hanchan,
        )

    # Assert
    record_on_db = user_hanchan_repository.find()
    assert len(record_on_db) == 1
