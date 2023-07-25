from DomainModel.entities.User import User
from DomainModel.entities.Match import Match
from DomainModel.entities.UserMatch import UserMatch
from repositories import (
    user_repository,
    match_repository,
    user_match_repository,
)
from typing import List
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
    result = user_match_repository.delete()

    # Assert
    assert result == 3
    
    record_on_db = user_match_repository.find()
    assert len(record_on_db) == 0


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
    result = user_match_repository.delete(
        query={
            'user_id': target.user_id,
        },
    )

    # Assert
    assert result == 2
    
    record_on_db = user_match_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0].user_id == dummy_user_matches[1].user_id
    assert record_on_db[0].match_id == dummy_user_matches[1].match_id
