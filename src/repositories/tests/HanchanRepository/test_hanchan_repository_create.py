from tests.dummies import (
    generate_dummy_hanchan_list,
    generate_dummy_match_list,
)
from repositories import session_scope, hanchan_repository, match_repository


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
        hanchan_repository.create(
            session,
            dummy_hanchan,
        )

    # Assert
    with session_scope() as session:
        result = hanchan_repository.find_all(
            session,
        )
        assert len(result) == 1
        assert result[0].line_group_id == dummy_hanchan.line_group_id
        assert result[0].raw_scores == dummy_hanchan.raw_scores
        assert result[0].converted_scores == dummy_hanchan.converted_scores
        assert result[0].match_id == dummy_hanchan.match_id
        assert result[0].status == dummy_hanchan.status
