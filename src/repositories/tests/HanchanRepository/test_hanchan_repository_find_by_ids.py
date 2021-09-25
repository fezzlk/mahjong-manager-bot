from tests.dummies import generate_dummy_hanchan_list, generate_dummy_match_list
from db_setting import Session
from repositories import session_scope, hanchan_repository, match_repository
from domains.Hanchan import Hanchan

session = Session()


def test_hit_with_ids():
    # Arrange
    with session_scope() as session:
        dummy_matches = generate_dummy_match_list()[:3]
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
    target_hanchans = generate_dummy_hanchan_list()[1:3]
    ids = [target_hanchan._id for target_hanchan in target_hanchans]

    # Act
    with session_scope() as session:
        result = hanchan_repository.find_by_ids(
            session,
            ids,
        )

    # Assert
        assert len(result) == len(target_hanchans)
        for i in range(len(result)):
            assert isinstance(result[i], Hanchan)
            assert result[i].line_room_id == target_hanchans[i].line_room_id
            assert result[i].match_id == target_hanchans[i].match_id
            assert result[i].raw_scores == target_hanchans[i].raw_scores
            assert result[i].converted_scores == target_hanchans[i].converted_scores
            assert result[i].status == target_hanchans[i].status


def test_hit_with_an_id_as_not_list():
    # Arrange
    with session_scope() as session:
        dummy_matches = generate_dummy_match_list()[:3]
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
    target_hanchan = generate_dummy_hanchan_list()[2]
    target_hanchan_id = target_hanchan._id

    # Act
    with session_scope() as session:
        result = hanchan_repository.find_by_ids(
            session,
            target_hanchan_id,
        )

    # Assert
        assert len(result) == 1
        assert result[0].line_room_id == dummy_hanchan.line_room_id
        assert result[0].match_id == dummy_hanchan.match_id
        assert result[0].raw_scores == dummy_hanchan.raw_scores
        assert result[0].converted_scores == dummy_hanchan.converted_scores
        assert result[0].status == dummy_hanchan.status


def test_hit_0_record():
    # Arrange
    with session_scope() as session:
        dummy_matches = generate_dummy_match_list()[:3]
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
    ids = [4, 5]

    # Act
    with session_scope() as session:
        result = hanchan_repository.find_by_ids(
            session,
            ids,
        )

    # Assert
        assert len(result) == 0
