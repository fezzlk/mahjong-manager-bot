from Domains.Entities.Match import Match
from tests.dummies import generate_dummy_match_list
from db_setting import Session
from Repositories import session_scope, match_repository

session = Session()


def test_success():
    # Arrange
    dummy_match = generate_dummy_match_list()[0]

    # Act
    with session_scope() as session:
        result = match_repository.create(
            session,
            dummy_match,
        )

    # Assert
    assert isinstance(result, Match)
    assert result._id == dummy_match._id
    assert result.line_group_id == dummy_match.line_group_id
    assert result.hanchan_ids == dummy_match.hanchan_ids
    assert result.users == dummy_match.users
    assert result.status == dummy_match.status

    with session_scope() as session:
        record_on_db = match_repository.find_all(
            session,
        )
        assert len(record_on_db) == 1
        assert record_on_db[0]._id == dummy_match._id
        assert record_on_db[0].line_group_id == dummy_match.line_group_id
        assert record_on_db[0].hanchan_ids == dummy_match.hanchan_ids
        assert record_on_db[0].users == dummy_match.users
        assert record_on_db[0].status == dummy_match.status
