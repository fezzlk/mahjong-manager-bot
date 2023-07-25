from DomainModel.entities.User import User
from DomainModel.entities.Match import Match
from DomainModel.entities.UserMatch import UserMatch
from repositories import (
    user_repository,
    match_repository,
    user_match_repository,
)
from typing import List
from pymongo import DESCENDING
from tests.dummies import (
    generate_dummy_user_list,
    generate_dummy_match_list,
)

dummy_users = generate_dummy_user_list()
dummy_matches = generate_dummy_match_list()


def test_success():
    # Arrange
    users: List[User] = []
    matches: List[Match] = []
    for dummy_user in dummy_users:
        users.append(
            user_repository.create(dummy_user)
        )
    for dummy_match in dummy_matches:
        matches.append(
            match_repository.create(dummy_match)
        )
    dummy_user_matches = [
        UserMatch(
            user_id=users[0]._id,
            match_id=matches[0]._id,
        ),
        UserMatch(
            user_id=users[1]._id,
            match_id=matches[0]._id,
        ),
        UserMatch(
            user_id=users[0]._id,
            match_id=matches[1]._id,
        ),
    ]
    for dummy_user_match in dummy_user_matches:
        user_match_repository.create(
            dummy_user_match,
        )

    # Act
    result = user_match_repository.find()

    # Assert
    assert len(result) == len(dummy_user_matches)
    for i in range(len(result)):
        assert result[i].user_id == dummy_user_matches[i].user_id
        assert result[i].match_id == dummy_user_matches[i].match_id


def test_success_with_filter():
    # Arrange
    users: List[User] = []
    matches: List[Match] = []
    for dummy_user in dummy_users:
        users.append(
            user_repository.create(dummy_user)
        )
    for dummy_match in dummy_matches:
        matches.append(
            match_repository.create(dummy_match)
        )
    dummy_user_matches = [
        UserMatch(
            user_id=users[0]._id,
            match_id=matches[0]._id,
        ),
        UserMatch(
            user_id=users[1]._id,
            match_id=matches[0]._id,
        ),
        UserMatch(
            user_id=users[0]._id,
            match_id=matches[1]._id,
        ),
    ]
    for dummy_user_match in dummy_user_matches:
        user_match_repository.create(
            dummy_user_match,
        )
    target = dummy_user_matches[0]

    # Act
    result = user_match_repository.find(
        query={
            'user_id': target.user_id,
            'match_id': target.match_id,
        },
    )

    # Assert
    assert result[0].user_id == target.user_id
    assert result[0].match_id == target.match_id


def test_success_with_sort():
    # Arrange
    users: List[User] = []
    matches: List[Match] = []
    for dummy_user in dummy_users:
        users.append(
            user_repository.create(dummy_user)
        )
    for dummy_match in dummy_matches:
        matches.append(
            match_repository.create(dummy_match)
        )
    dummy_user_matches = [
        UserMatch(
            user_id=users[0]._id,
            match_id=matches[0]._id,
        ),
        UserMatch(
            user_id=users[1]._id,
            match_id=matches[0]._id,
        ),
        UserMatch(
            user_id=users[0]._id,
            match_id=matches[1]._id,
        ),
    ]
    for dummy_user_match in dummy_user_matches:
        user_match_repository.create(
            dummy_user_match,
        )

    # Act
    result = user_match_repository.find(
        query={
            'user_id': dummy_user_matches[0].user_id,
        },
        sort=[('match_id', DESCENDING)]
    )
    
    # Assert
    expected = [
        UserMatch(
            user_id=users[0]._id,
            match_id=matches[1]._id,
        ),
        UserMatch(
            user_id=users[0]._id,
            match_id=matches[0]._id,
        ),
    ]
    assert len(result) == len(expected)
    for i in range(len(result)):
        assert result[i].user_id == expected[i].user_id
        assert result[i].match_id == expected[i].match_id
