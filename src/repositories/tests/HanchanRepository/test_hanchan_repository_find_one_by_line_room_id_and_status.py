import pytest
from tests.dummies import generate_dummy_hanchan_list, generate_dummy_match_list
from db_setting import Session
from repositories import session_scope, hanchan_repository, match_repository
from domains.Hanchan import Hanchan

session = Session()


def test_hit_1_record():
    # Arrange
    with session_scope() as session:
        dummy_matches = generate_dummy_match_list()[:3]
        for dummy_match in dummy_matches:
            match_repository.create(
                session,
                dummy_match,
            )
    dummy_hanchans = generate_dummy_hanchan_list()[:3]
    with session_scope() as session:
        for dummy_hanchan in dummy_hanchans:
            hanchan_repository.create(
                session,
                dummy_hanchan,
            )
    target_hanchan = dummy_hanchans[0]

    # Act
    with session_scope() as session:
        result = hanchan_repository.find_one_by_line_room_id_and_status(
            session=session,
            line_room_id=target_hanchan.line_room_id,
            status=target_hanchan.status,
        )

    # Assert
        assert isinstance(result, Hanchan)
        assert result.line_room_id == target_hanchan.line_room_id
        assert result.match_id == target_hanchan.match_id
        assert result.raw_scores == target_hanchan.raw_scores
        assert result.converted_scores == target_hanchan.converted_scores
        assert result.status == target_hanchan.status


def test_hit_0_record_with_not_exist_line_room_id():
    # Arrange
    with session_scope() as session:
        dummy_matches = generate_dummy_match_list()[:3]
        for dummy_match in dummy_matches:
            match_repository.create(
                session,
                dummy_match,
            )
    dummy_hanchans = generate_dummy_hanchan_list()[:4]
    with session_scope() as session:
        for dummy_hanchan in dummy_hanchans:
            hanchan_repository.create(
                session,
                dummy_hanchan,
            )
    target_hanchan = generate_dummy_hanchan_list()[4]

    # Act
    with session_scope() as session:
        result = hanchan_repository.find_one_by_line_room_id_and_status(
            session=session,
            line_room_id=target_hanchan.line_room_id,
            status=target_hanchan.status,
        )

    # Assert
        assert result is None


def test_hit_0_record_with_not_exist_status():
    # Arrange
    with session_scope() as session:
        dummy_matches = generate_dummy_match_list()[:3]
        for dummy_match in dummy_matches:
            match_repository.create(
                session,
                dummy_match,
            )
    dummy_hanchans = generate_dummy_hanchan_list()[:2]
    with session_scope() as session:
        for dummy_hanchan in dummy_hanchans:
            hanchan_repository.create(
                session,
                dummy_hanchan,
            )
    target_hanchan = generate_dummy_hanchan_list()[2]

    # Act
    with session_scope() as session:
        result = hanchan_repository.find_one_by_line_room_id_and_status(
            session=session,
            line_room_id=target_hanchan.line_room_id,
            status=target_hanchan.status,
        )

    # Assert
        assert result is None


def test_NG_with_id_none():
    with pytest.raises(ValueError):
        # Arrange
        with session_scope() as session:
            dummy_matches = generate_dummy_match_list()[:3]
            for dummy_match in dummy_matches:
                match_repository.create(
                    session,
                    dummy_match,
                )
        dummy_hanchans = generate_dummy_hanchan_list()[:3]
        with session_scope() as session:
            for dummy_hanchan in dummy_hanchans:
                hanchan_repository.create(
                    session,
                    dummy_hanchan,
                )
        target_hanchan = dummy_hanchans[0]

        # Act
        with session_scope() as session:
            hanchan_repository.find_one_by_line_room_id_and_status(
                session=session,
                line_room_id=None,
                status=target_hanchan.status,
            )

        # Assert
        # Do nothing


def test_NG_with_line_room_id_none():
    with pytest.raises(ValueError):
        # Arrange
        with session_scope() as session:
            dummy_matches = generate_dummy_match_list()[:3]
            for dummy_match in dummy_matches:
                match_repository.create(
                    session,
                    dummy_match,
                )
        dummy_hanchans = generate_dummy_hanchan_list()[:3]
        with session_scope() as session:
            for dummy_hanchan in dummy_hanchans:
                hanchan_repository.create(
                    session,
                    dummy_hanchan,
                )
        target_hanchan = dummy_hanchans[0]

        # Act
        with session_scope() as session:
            hanchan_repository.find_one_by_line_room_id_and_status(
                session=session,
                line_room_id=target_hanchan.line_room_id,
                status=None
            )

        # Assert
        # Do nothing
