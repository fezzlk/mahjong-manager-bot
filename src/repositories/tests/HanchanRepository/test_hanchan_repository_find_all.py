from tests.dummies import generate_dummy_hanchan_list, generate_dummy_match_list
from db_setting import Session
from repositories import session_scope
from repositories.HanchanRepository import HanchanRepository
from repositories.MatchRepository import MatchRepository
from domains.Hanchan import Hanchan

session = Session()


def test_success_find_records():
    # Arrange
    with session_scope() as session:
        dummy_matches = generate_dummy_match_list()
        for dummy_match in dummy_matches:
            MatchRepository.create(
                session,
                dummy_match,
            )
    with session_scope() as session:
        dummy_hanchans = generate_dummy_hanchan_list()
        for dummy_hanchan in dummy_hanchans:
            HanchanRepository.create(
                session,
                dummy_hanchan,
            )

    # Act
    with session_scope() as session:
        result = HanchanRepository.find_all(
            session,
        )

    # Assert
        assert len(result) == len(dummy_hanchans)
        for i in range(len(result)):
            assert isinstance(result[i], Hanchan)
            assert result[i].line_room_id == dummy_hanchans[i].line_room_id
            assert result[i].match_id == dummy_hanchans[i].match_id
            assert result[i].raw_scores == dummy_hanchans[i].raw_scores
            assert result[i].converted_scores == dummy_hanchans[i].converted_scores
            assert result[i].status == dummy_hanchans[i].status


def test_success_find_0_record():
    # Arrange
    # Do nothing

    # Act
    with session_scope() as session:
        result = HanchanRepository.find_all(
            session,
        )

    # Assert
        assert len(result) == 0
