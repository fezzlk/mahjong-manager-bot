import pytest
from tests.dummies import generate_dummy_match_list
from db_setting import Session
from repositories import session_scope, match_repository
from domains.Match import Match

session = Session()


def test_hit_records():
    # Arrange
    dummy_matchs = generate_dummy_match_list()[:4]
    with session_scope() as session:
        for dummy_match in dummy_matchs:
            match_repository.create(
                session,
                dummy_match,
            )
    target_matches = dummy_matchs[2:4]

    # Act
    with session_scope() as session:
        result = match_repository.find_many_by_room_id_and_status(
            session,
            target_matches[0].line_room_id,
            target_matches[0].status,
        )

    # Assert
        assert len(result) == len(target_matches)
        for i in range(len(result)):
            assert isinstance(result[i], Match)
            assert result[i].line_room_id == target_matches[i].line_room_id
            assert result[i].hanchan_ids == target_matches[i].hanchan_ids
            assert result[i].users == target_matches[i].users
            assert result[i].status == target_matches[i].status


def test_hit_0_record_with_not_exist_line_room_id():
    # Arrange
    with session_scope() as session:
        dummy_matchs = generate_dummy_match_list()[:3]
        for dummy_match in dummy_matchs:
            match_repository.create(
                session,
                dummy_match,
            )
    target_match = generate_dummy_match_list()[4]

    # Act
    with session_scope() as session:
        result = match_repository.find_many_by_room_id_and_status(
            session=session,
            line_room_id=target_match.line_room_id,
            status=target_match.status,
        )

    # Assert
        assert len(result) == 0


def test_hit_0_record_with_not_exist_status():
    # Arrange
    with session_scope() as session:
        dummy_matchs = generate_dummy_match_list()[:2]
        for dummy_match in dummy_matchs:
            match_repository.create(
                session,
                dummy_match,
            )
    target_match = generate_dummy_match_list()[2]

    # Act
    with session_scope() as session:
        result = match_repository.find_many_by_room_id_and_status(
            session=session,
            line_room_id=target_match.line_room_id,
            status=target_match.status,
        )

    # Assert
        assert len(result) == 0

