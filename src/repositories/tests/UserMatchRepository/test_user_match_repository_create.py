from DomainModel.entities.User import User, UserMode
from DomainModel.entities.Match import Match
from DomainModel.entities.UserMatch import UserMatch
from repositories import (
    user_repository,
    match_repository,
    user_match_repository,
)
from bson.objectid import ObjectId


dummy_user = User(
    line_user_name="test_user1",
    line_user_id="U0123456789abcdefghijklmnopqrstu1",
    mode=UserMode.wait.value,
    jantama_name="jantama_user1",
)
dummy_match = Match(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    hanchan_ids=[1, 2, 3, 6, 7],
    status=1,
)


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
    assert record_on_db[0].user_id == dummy_user_match.user_id
    assert record_on_db[0].match_id == dummy_user_match.match_id
