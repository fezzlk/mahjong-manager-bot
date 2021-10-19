from tests.dummies import generate_dummy_match_list
from db_setting import Session
from repositories import session_scope, match_repository
from domains.Match import Match

session = Session()


def test_hit_with_ids():
    # Arrange
    with session_scope() as session:
        dummy_matchs = generate_dummy_match_list()[:3]
        for dummy_match in dummy_matchs:
            match_repository.create(
                session,
                dummy_match,
            )
    target_matchs = generate_dummy_match_list()[1:3]
    ids = [target_match._id for target_match in target_matchs]

    # Act
    with session_scope() as session:
        result = match_repository.find_by_ids(
            session,
            ids,
        )

    # Assert
        assert len(result) == len(target_matchs)
        for i in range(len(result)):
            assert isinstance(result[i], Match)
            assert result[i].line_room_id == target_matchs[i].line_room_id
            assert result[i].hanchan_ids == target_matchs[i].hanchan_ids
            assert result[i].users == target_matchs[i].users
            assert result[i].status == target_matchs[i].status


def test_hit_0_record():
    # Arrange
    with session_scope() as session:
        dummy_matchs = generate_dummy_match_list()[:3]
        for dummy_match in dummy_matchs:
            match_repository.create(
                session,
                dummy_match,
            )
    target_matchs = generate_dummy_match_list()[3:6]
    ids = [target_match._id for target_match in target_matchs]

    # Act
    with session_scope() as session:
        result = match_repository.find_by_ids(
            session,
            ids,
        )

    # Assert
        assert len(result) == 0
