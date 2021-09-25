from tests.dummies import generate_dummy_match
from db_setting import Session
from repositories import session_scope, match_repository

session = Session()


def test_success():
    # Arrange
    dummy_match = generate_dummy_match()

    # Act
    with session_scope() as session:
        match_repository.create(
            session,
            dummy_match,
        )

    # Assert
    with session_scope() as session:
        result = match_repository.find_all(
            session,
        )
        assert len(result) == 1
        assert result[0].line_room_id == dummy_match.line_room_id
        assert result[0].hanchan_ids == dummy_match.hanchan_ids
        assert result[0].users == dummy_match.users
        assert result[0].status == dummy_match.status
