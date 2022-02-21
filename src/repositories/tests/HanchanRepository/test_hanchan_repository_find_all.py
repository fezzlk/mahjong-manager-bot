from tests.dummies import (
    generate_dummy_hanchan_list,
    generate_dummy_match_list,
)
from repositories import session_scope, hanchan_repository, match_repository
from entities.Hanchan import Hanchan


def test_success_find_records():
    # Arrange
    with session_scope() as session:
        dummy_matches = generate_dummy_match_list()
        for dummy_match in dummy_matches:
            match_repository.create(
                session,
                dummy_match,
            )
    with session_scope() as session:
        dummy_hanchans = generate_dummy_hanchan_list()
        for dummy_hanchan in dummy_hanchans:
            hanchan_repository.create(
                session,
                dummy_hanchan,
            )

    # Act
    with session_scope() as session:
        result = hanchan_repository.find_all(
            session,
        )

    # Assert
        assert len(result) == len(dummy_hanchans)
        for i in range(len(result)):
            assert isinstance(result[i], Hanchan)
            assert result[i]._id == dummy_hanchans[i]._id
            assert result[i].line_group_id == dummy_hanchans[i].line_group_id
            assert result[i].match_id == dummy_hanchans[i].match_id
            assert result[i].raw_scores == dummy_hanchans[i].raw_scores
            assert result[i].converted_scores == dummy_hanchans[i].converted_scores
            assert result[i].status == dummy_hanchans[i].status


def test_success_find_0_record():
    # Arrange
    # Do nothing

    # Act
    with session_scope() as session:
        result = hanchan_repository.find_all(
            session,
        )

    # Assert
        assert len(result) == 0
