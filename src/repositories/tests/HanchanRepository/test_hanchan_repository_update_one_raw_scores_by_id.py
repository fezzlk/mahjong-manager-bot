from tests.dummies import (
    generate_dummy_hanchan_list,
    generate_dummy_match_list,
)
from repositories import session_scope, hanchan_repository, match_repository
from entities.Hanchan import Hanchan


def test_hit():
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
    dummy_raw_scores = {'a': 10000}

    # Act
    with session_scope() as session:
        result = hanchan_repository.update_one_raw_scores_by_id(
            session=session,
            hanchan_id=target_hanchan._id,
            raw_scores=dummy_raw_scores,
        )

    # Assert
        assert isinstance(result, Hanchan)
        assert result._id == target_hanchan._id
        assert result.line_group_id == target_hanchan.line_group_id
        assert result.match_id == target_hanchan.match_id
        assert result.raw_scores == dummy_raw_scores
        assert result.converted_scores == target_hanchan.converted_scores
        assert result.status == target_hanchan.status


def test_hit_0_record_with_not_exist_id():
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
    target_hanchan = generate_dummy_hanchan_list()[4]
    dummy_raw_scores = {'a': 10000}

    # Act
    with session_scope() as session:
        result = hanchan_repository.update_one_raw_scores_by_id(
            session=session,
            hanchan_id=target_hanchan._id,
            raw_scores=dummy_raw_scores,
        )

    # Assert
        assert result is None
