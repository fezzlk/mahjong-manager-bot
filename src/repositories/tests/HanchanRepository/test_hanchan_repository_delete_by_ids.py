from tests.dummies import generate_dummy_hanchan_list, generate_dummy_match_list
from db_setting import Session
from repositories import session_scope, hanchan_repository, match_repository
from domains.Hanchan import Hanchan

session = Session()


def test_hit_with_ids():
    # Arrange
    dummy_matches = generate_dummy_match_list()[:3]
    with session_scope() as session:
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
    other_hanchans = dummy_hanchans[:1]
    target_hanchans = dummy_hanchans[1:3]
    ids = [target_hanchan._id for target_hanchan in target_hanchans]

    # Act
    with session_scope() as session:
        hanchan_repository.delete_by_ids(
            session,
            ids,
        )

    # Assert
    with session_scope() as session:
        result = hanchan_repository.find_all(
            session,
        )
        assert len(result) == len(other_hanchans)
        for i in range(len(result)):
            assert isinstance(result[i], Hanchan)
            assert result[i].line_room_id == other_hanchans[i].line_room_id
            assert result[i].match_id == other_hanchans[i].match_id
            assert result[i].raw_scores == other_hanchans[i].raw_scores
            assert result[i].converted_scores == other_hanchans[i].converted_scores
            assert result[i].status == other_hanchans[i].status


def test_hit_with_an_id_as_not_list():
    # Arrange
    dummy_matches = generate_dummy_match_list()[:3]
    with session_scope() as session:
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
    other_hanchans = dummy_hanchans[:2]
    target_hanchan = dummy_hanchans[2]
    target_hanchan_id = target_hanchan._id

    # Act
    with session_scope() as session:
        result = hanchan_repository.delete_by_ids(
            session,
            target_hanchan_id,
        )

    # Assert
    with session_scope() as session:
        result = hanchan_repository.find_all(
            session,
        )
        assert len(result) == len(other_hanchans)
        for i in range(len(result)):
            assert isinstance(result[i], Hanchan)
            assert result[i].line_room_id == other_hanchans[i].line_room_id
            assert result[i].match_id == other_hanchans[i].match_id
            assert result[i].raw_scores == other_hanchans[i].raw_scores
            assert result[i].converted_scores == other_hanchans[i].converted_scores
            assert result[i].status == other_hanchans[i].status


def test_hit_0_record():
    # Arrange
    dummy_matches = generate_dummy_match_list()[:3]
    with session_scope() as session:
        for dummy_match in dummy_matches:
            match_repository.create(
                session,
                dummy_match,
            )
    with session_scope() as session:
        dummy_hanchans = generate_dummy_hanchan_list()[:3]
        for dummy_hanchan in dummy_hanchans:
            hanchan_repository.create(
                session,
                dummy_hanchan,
            )

    # Act
    with session_scope() as session:
        result = hanchan_repository.delete_by_ids(
            session,
            [4, 5],
        )

    # Assert
    with session_scope() as session:
        result = hanchan_repository.find_all(
            session,
        )
        assert len(result) == len(dummy_hanchans)
        for i in range(len(result)):
            assert isinstance(result[i], Hanchan)
            assert result[i].line_room_id == dummy_hanchans[i].line_room_id
            assert result[i].match_id == dummy_hanchans[i].match_id
            assert result[i].raw_scores == dummy_hanchans[i].raw_scores
            assert result[i].converted_scores == dummy_hanchans[i].converted_scores
            assert result[i].status == dummy_hanchans[i].status
