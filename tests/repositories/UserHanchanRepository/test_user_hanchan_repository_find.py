from typing import List

from dummies import (
    generate_dummy_hanchan_list,
    generate_dummy_user_list,
)
from pymongo import DESCENDING

from DomainModel.entities.Hanchan import Hanchan
from DomainModel.entities.User import User
from DomainModel.entities.UserHanchan import UserHanchan
from repositories import (
    hanchan_repository,
    user_hanchan_repository,
    user_repository,
)

dummy_users = generate_dummy_user_list()
dummy_hanchans = generate_dummy_hanchan_list()


def test_success():
    # Arrange
    users: List[User] = []
    hanchans: List[Hanchan] = []
    for dummy_user in dummy_users:
        users.append(
            user_repository.create(dummy_user),
        )
    for dummy_hanchan in dummy_hanchans:
        hanchans.append(
            hanchan_repository.create(dummy_hanchan),
        )
    dummy_user_hanchans = [
        UserHanchan(
            line_user_id=users[0].line_user_id,
            hanchan_id=hanchans[0]._id,
            point=40000,
            rank=1,
        ),
        UserHanchan(
            line_user_id=users[1].line_user_id,
            hanchan_id=hanchans[0]._id,
            point=30000,
            rank=2,
        ),
        UserHanchan(
            line_user_id=users[0].line_user_id,
            hanchan_id=hanchans[1]._id,
            point=20000,
            rank=3,
        ),
    ]
    for dummy_user_hanchan in dummy_user_hanchans:
        user_hanchan_repository.create(
            dummy_user_hanchan,
        )

    # Act
    result = user_hanchan_repository.find()

    # Assert
    assert len(result) == len(dummy_user_hanchans)
    for i in range(len(result)):
        assert result[i].line_user_id == dummy_user_hanchans[i].line_user_id
        assert result[i].hanchan_id == dummy_user_hanchans[i].hanchan_id


def test_success_with_filter():
    # Arrange
    users: List[User] = []
    hanchans: List[Hanchan] = []
    for dummy_user in dummy_users:
        users.append(
            user_repository.create(dummy_user),
        )
    for dummy_hanchan in dummy_hanchans:
        hanchans.append(
            hanchan_repository.create(dummy_hanchan),
        )
    dummy_user_hanchans = [
        UserHanchan(
            line_user_id=users[0].line_user_id,
            hanchan_id=hanchans[0]._id,
            point=40000,
            rank=1,
        ),
        UserHanchan(
            line_user_id=users[1].line_user_id,
            hanchan_id=hanchans[0]._id,
            point=30000,
            rank=2,
        ),
        UserHanchan(
            line_user_id=users[0].line_user_id,
            hanchan_id=hanchans[1]._id,
            point=20000,
            rank=3,
        ),
    ]
    for dummy_user_hanchan in dummy_user_hanchans:
        user_hanchan_repository.create(
            dummy_user_hanchan,
        )
    target = dummy_user_hanchans[0]

    # Act
    result = user_hanchan_repository.find(
        query={
            "line_user_id": target.line_user_id,
            "hanchan_id": target.hanchan_id,
        },
    )

    # Assert
    assert result[0].line_user_id == target.line_user_id
    assert result[0].hanchan_id == target.hanchan_id


def test_success_with_sort():
    # Arrange
    users: List[User] = []
    hanchans: List[Hanchan] = []
    for dummy_user in dummy_users:
        users.append(
            user_repository.create(dummy_user),
        )
    for dummy_hanchan in dummy_hanchans:
        hanchans.append(
            hanchan_repository.create(dummy_hanchan),
        )
    dummy_user_hanchans = [
        UserHanchan(
            line_user_id=users[0].line_user_id,
            hanchan_id=hanchans[0]._id,
            point=40000,
            rank=1,
        ),
        UserHanchan(
            line_user_id=users[1].line_user_id,
            hanchan_id=hanchans[0]._id,
            point=30000,
            rank=2,
        ),
        UserHanchan(
            line_user_id=users[0].line_user_id,
            hanchan_id=hanchans[1]._id,
            point=20000,
            rank=3,
        ),
    ]
    for dummy_user_hanchan in dummy_user_hanchans:
        user_hanchan_repository.create(
            dummy_user_hanchan,
        )

    # Act
    result = user_hanchan_repository.find(
        query={
            "line_user_id": dummy_user_hanchans[0].line_user_id,
        },
        sort=[("hanchan_id", DESCENDING)],
    )

    # Assert
    expected = [
        UserHanchan(
            line_user_id=users[0].line_user_id,
            hanchan_id=hanchans[1]._id,
            point=40000,
            rank=1,
        ),
        UserHanchan(
            line_user_id=users[0].line_user_id,
            hanchan_id=hanchans[0]._id,
            point=20000,
            rank=3,
        ),
    ]
    assert len(result) == len(expected)
    for i in range(len(result)):
        assert result[i].line_user_id == expected[i].line_user_id
        assert result[i].hanchan_id == expected[i].hanchan_id
