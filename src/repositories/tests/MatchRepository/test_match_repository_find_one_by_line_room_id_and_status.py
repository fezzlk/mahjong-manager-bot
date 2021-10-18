import pytest
from tests.dummies import generate_dummy_match_list
from db_setting import Session
from repositories import session_scope, match_repository
from domains.Match import Match

session = Session()


def test_hit_1_record():
    # Arrange
    dummy_matchs = generate_dummy_match_list()[:3]
    with session_scope() as session:
        for dummy_match in dummy_matchs:
            match_repository.create(
                session,
                dummy_match,
            )
    target_match = dummy_matchs[0]

    # Act
    with session_scope() as session:
        result = match_repository.find_one_by_line_room_id_and_status(
            session=session,
            line_room_id=target_match.line_room_id,
            status=target_match.status,
        )

    # Assert
        assert isinstance(result, Match)
        assert result.line_room_id == target_match.line_room_id
        assert result.hanchan_ids == target_match.hanchan_ids
        assert result.users == target_match.users
        assert result.status == target_match.status


def test_hit_0_record():
    # Arrange
    dummy_matchs = generate_dummy_match_list()[1:3]
    with session_scope() as session:
        for dummy_match in dummy_matchs:
            match_repository.create(
                session,
                dummy_match,
            )
    target_match = generate_dummy_match_list()[0]

    # Act
    with session_scope() as session:
        result = match_repository.find_one_by_line_room_id_and_status(
            session=session,
            line_room_id=target_match.line_room_id,
            status=target_match.status,
        )

    # Assert
        assert result is None
