from DomainModel.entities.UserMatch import UserMatch
from repositories import (
    user_repository,
    match_repository,
    user_match_repository,
)
from bson.objectid import ObjectId
from tests.dummies import (
    generate_dummy_user_list,
    generate_dummy_match_list,
)
import pytest

dummy_user = generate_dummy_user_list()[0]
dummy_match = generate_dummy_match_list()[0]


def test_success():
    # Arrange
    new_user = user_repository.create(
        dummy_user,
    )
    new_match = match_repository.create(
        dummy_match,
    )
    dummy_user_match = UserMatch(
        user_id=new_user._id,
        match_id=new_match._id,
    )

    # Act
    result = user_match_repository.create(
        dummy_user_match,
    )

    # Assert
    assert isinstance(result, UserMatch)
    assert type(result._id) == ObjectId
    assert result.user_id == dummy_user_match.user_id
    assert result.match_id == dummy_user_match.match_id

    record_on_db = user_match_repository.find()
    assert len(record_on_db) == 1
    assert type(record_on_db[0]._id) == ObjectId
    assert record_on_db[0].user_id == dummy_user_match.user_id
    assert record_on_db[0].match_id == dummy_user_match.match_id


def test_error_duplicate_line_group_id():
    with pytest.raises(Exception):
        # Arrange
        new_user = user_repository.create(
            dummy_user,
        )
        new_match = match_repository.create(
            dummy_match,
        )
        dummy_user_match = UserMatch(
            user_id=new_user._id,
            match_id=new_match._id,
        )

        user_match_repository.create(
            dummy_user_match,
        )

        # Act
        user_match_repository.create(
            dummy_user_match,
        )

        # Assert
        record_on_db = user_match_repository.find()
        assert len(record_on_db) == 1
