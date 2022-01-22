from Domains.Entities.Hanchan import Hanchan
from tests.dummies import (
    generate_dummy_hanchan_list,
    generate_dummy_match_list,
)
from Repositories import session_scope, hanchan_repository, match_repository


def test_success():
    # Arrange
    dummy_hanchan = generate_dummy_hanchan_list()[0]
    dummy_match = generate_dummy_match_list()[0]
    with session_scope() as session:
        match_repository.create(
            session,
            dummy_match,
        )

    # Act
    with session_scope() as session:
        result = hanchan_repository.create(
            session,
            dummy_hanchan,
        )

    # Assert
    assert isinstance(result, Hanchan)
    assert result._id == dummy_hanchan._id
    assert result.line_group_id == dummy_hanchan.line_group_id
    assert result.raw_scores == dummy_hanchan.raw_scores
    assert result.converted_scores == dummy_hanchan.converted_scores
    assert result.match_id == dummy_hanchan.match_id
    assert result.status == dummy_hanchan.status

    with session_scope() as session:
        record_on_db = hanchan_repository.find_all(
            session,
        )
        assert len(record_on_db) == 1
        assert record_on_db[0]._id == dummy_hanchan._id
        assert record_on_db[0].line_group_id == dummy_hanchan.line_group_id
        assert record_on_db[0].raw_scores == dummy_hanchan.raw_scores
        assert record_on_db[0].converted_scores == dummy_hanchan.converted_scores
        assert record_on_db[0].match_id == dummy_hanchan.match_id
        assert record_on_db[0].status == dummy_hanchan.status
