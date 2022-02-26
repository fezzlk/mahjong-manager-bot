from tests.dummies import generate_dummy_match_list
from db_setting import Session
from repositories import session_scope, match_repository
from DomainModel.entities.Match import Match

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
    target_matches.reverse()

    # Act
    with session_scope() as session:
        result = match_repository.find_many_by_line_group_id_and_status(
            session,
            line_group_id=target_matches[0].line_group_id,
            status=target_matches[0].status,
        )

    # Assert
        assert len(result) == len(target_matches)
        for i in range(len(result)):
            assert isinstance(result[i], Match)
            assert result[i]._id == target_matches[i]._id
            assert result[i].line_group_id == target_matches[i].line_group_id
            assert result[i].hanchan_ids == target_matches[i].hanchan_ids
            assert result[i].users == target_matches[i].users
            assert result[i].status == target_matches[i].status


def test_hit_0_record_with_not_exist_line_group_id():
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
        result = match_repository.find_many_by_line_group_id_and_status(
            session=session,
            line_group_id=target_match.line_group_id,
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
        result = match_repository.find_many_by_line_group_id_and_status(
            session=session,
            line_group_id=target_match.line_group_id,
            status=target_match.status,
        )

    # Assert
        assert len(result) == 0
