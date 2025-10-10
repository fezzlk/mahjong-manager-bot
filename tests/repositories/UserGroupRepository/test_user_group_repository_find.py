from typing import List

from pymongo import DESCENDING

from DomainModel.entities.Group import Group
from DomainModel.entities.User import User
from DomainModel.entities.UserGroup import UserGroup
from repositories import (
    group_repository,
    user_group_repository,
    user_repository,
)
from dummies import (
    generate_dummy_group_list,
    generate_dummy_user_list,
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
    result = user_group_repository.find()

    # Assert
    assert len(result) == len(dummy_user_groups)
    for i in range(len(result)):
        assert result[i].line_user_id == dummy_user_groups[i].line_user_id
        assert result[i].line_group_id == dummy_user_groups[i].line_group_id


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
    result = user_group_repository.find(
        query={
            "line_user_id": target.line_user_id,
            "line_group_id": target.line_group_id,
        },
    )

    # Assert
    assert result[0].line_user_id == target.line_user_id
    assert result[0].line_group_id == target.line_group_id


def test_success_with_sort():
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
    result = user_group_repository.find(
        query={
            "line_user_id": dummy_user_groups[0].line_user_id,
        },
        sort=[("line_group_id", DESCENDING)],
    )

    # Assert
    expected = [
        UserGroup(
            line_user_id=users[0]._id,
            line_group_id=groups[1]._id,
        ),
        UserGroup(
            line_user_id=users[0]._id,
            line_group_id=groups[0]._id,
        ),
    ]
    assert len(result) == len(expected)
    for i in range(len(result)):
        assert result[i].line_user_id == expected[i].line_user_id
        assert result[i].line_group_id == expected[i].line_group_id
