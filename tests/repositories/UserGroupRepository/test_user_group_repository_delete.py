from typing import List

from dummies import (
    generate_dummy_group_list,
    generate_dummy_user_list,
)

from DomainModel.entities.Group import Group
from DomainModel.entities.User import User
from DomainModel.entities.UserGroup import UserGroup
from repositories import (
    group_repository,
    user_group_repository,
    user_repository,
)

dummy_users = generate_dummy_user_list()
dummy_groups = generate_dummy_group_list()


def test_success():
    # Arrange
    users: List[User] = []
    groups: List[Group] = []
    for dummy_user in dummy_users:
        users.append(
            user_repository.create(dummy_user),
        )
    for dummy_group in dummy_groups:
        groups.append(
            group_repository.create(dummy_group),
        )
    dummy_user_groups = [
        UserGroup(
            line_user_id=users[0]._id,
            line_group_id=groups[0]._id,
        ),
        UserGroup(
            line_user_id=users[1]._id,
            line_group_id=groups[0]._id,
        ),
        UserGroup(
            line_user_id=users[0]._id,
            line_group_id=groups[1]._id,
        ),
    ]
    for dummy_user_group in dummy_user_groups:
        user_group_repository.create(
            dummy_user_group,
        )

    # Act
    result = user_group_repository.delete()

    # Assert
    assert result == 3

    record_on_db = user_group_repository.find()
    assert len(record_on_db) == 0


def test_success_with_filter():
    # Arrange
    users: List[User] = []
    groups: List[Group] = []
    for dummy_user in dummy_users:
        users.append(
            user_repository.create(dummy_user),
        )
    for dummy_group in dummy_groups:
        groups.append(
            group_repository.create(dummy_group),
        )
    dummy_user_groups = [
        UserGroup(
            line_user_id=users[0]._id,
            line_group_id=groups[0]._id,
        ),
        UserGroup(
            line_user_id=users[1]._id,
            line_group_id=groups[0]._id,
        ),
        UserGroup(
            line_user_id=users[0]._id,
            line_group_id=groups[1]._id,
        ),
    ]
    for dummy_user_group in dummy_user_groups:
        user_group_repository.create(
            dummy_user_group,
        )
    target = dummy_user_groups[0]

    # Act
    result = user_group_repository.delete(
        query={
            "line_user_id": target.line_user_id,
        },
    )

    # Assert
    assert result == 2

    record_on_db = user_group_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0].line_user_id == dummy_user_groups[1].line_user_id
    assert record_on_db[0].line_group_id == dummy_user_groups[1].line_group_id
