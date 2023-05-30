from DomainModel.entities.UserGroup import UserGroup
from tests.dummies import (
    generate_dummy_user_list,
    generate_dummy_group_list,
)
from repositories import (
    user_repository,
    group_repository,
    user_group_repository,
)
from bson.objectid import ObjectId
import pytest


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
    assert type(result._id) == ObjectId
    assert result.line_user_id == dummy_user_group.line_user_id
    assert result.line_group_id == dummy_user_group.line_group_id

    record_on_db = user_group_repository.find()
    assert len(record_on_db) == 1
    assert type(record_on_db[0]._id) == ObjectId
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
