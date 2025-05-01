import pytest
from bson.objectid import ObjectId

from DomainModel.entities.UserGroup import UserGroup
from repositories import (
    group_repository,
    user_group_repository,
    user_repository,
)
from tests.dummies import (
    generate_dummy_group_list,
    generate_dummy_user_list,
)

dummy_users = generate_dummy_user_list()
dummy_groups = generate_dummy_group_list()


def test_success():
    # Arrange
    new_user = user_repository.create(
        dummy_users[0],
    )
    new_group = group_repository.create(
        dummy_groups[0],
    )
    dummy_user_group = UserGroup(
        line_user_id=new_user._id,
        line_group_id=new_group._id,
    )

    # Act
    result = user_group_repository.create(
        dummy_user_group,
    )

    # Assert
    assert isinstance(result, UserGroup)
    assert type(result._id) is ObjectId
    assert result.line_user_id == dummy_user_group.line_user_id
    assert result.line_group_id == dummy_user_group.line_group_id

    record_on_db = user_group_repository.find()
    assert len(record_on_db) == 1
    assert type(record_on_db[0]._id) is ObjectId
    assert record_on_db[0].line_user_id == dummy_user_group.line_user_id
    assert record_on_db[0].line_group_id == dummy_user_group.line_group_id


def test_success_with_id():
    # Arrange
    new_user = user_repository.create(
        dummy_users[0],
    )
    new_group = group_repository.create(
        dummy_groups[0],
    )
    dummy_user_group = UserGroup(
        line_user_id=new_user._id,
        line_group_id=new_group._id,
        _id=ObjectId("644c838186bbd9e20a91b783"),
    )

    # Act
    result = user_group_repository.create(
        dummy_user_group,
    )

    # Assert
    assert isinstance(result, UserGroup)
    assert result._id == dummy_user_group._id
    assert result.line_user_id == dummy_user_group.line_user_id
    assert result.line_group_id == dummy_user_group.line_group_id

    record_on_db = user_group_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0]._id == dummy_user_group._id
    assert record_on_db[0].line_user_id == dummy_user_group.line_user_id
    assert record_on_db[0].line_group_id == dummy_user_group.line_group_id


def test_error_duplicate_line_group_id():
    with pytest.raises(Exception):
        # Arrange
        new_user = user_repository.create(
            dummy_users[0],
        )
        new_group = group_repository.create(
            dummy_groups[0],
        )
        dummy_user_group = UserGroup(
            line_user_id=new_user._id,
            line_group_id=new_group._id,
        )
        user_group_repository.create(
            dummy_user_group,
        )

        # Act
        user_group_repository.create(
            dummy_user_group,
        )

    # Assert
    record_on_db = user_group_repository.find()
    assert len(record_on_db) == 1
