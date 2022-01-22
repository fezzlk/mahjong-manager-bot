from tests.dummies import generate_dummy_match_list
from db_setting import Session
from repositories import session_scope, match_repository
from Entities.Match import Match

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
        result = match_repository.update_one_hanchan_ids_by_id(
            session=session,
            match_id=target_match._id,
            hanchan_ids=[0, 1, 2],
        )

    # Assert
        assert isinstance(result, Match)
        assert result._id == target_match._id
        assert result.line_group_id == target_match.line_group_id
        assert result.hanchan_ids == [0, 1, 2]
        assert result.users == target_match.users
        assert result.status == target_match.status


def test_hit_0_record():
    # Arrange
    dummy_matchs = generate_dummy_match_list()[:2]
    with session_scope() as session:
        for dummy_match in dummy_matchs:
            match_repository.create(
                session,
                dummy_match,
            )
    target_match = generate_dummy_match_list()[2]

    # Act
    with session_scope() as session:
        result = match_repository.update_one_hanchan_ids_by_id(
            session=session,
            match_id=target_match._id,
            hanchan_ids=[0, 1, 2],
        )

    # Assert
        assert result is None
