from tests.dummies import generate_dummy_match_list
from db_setting import Session
from repositories import session_scope, match_repository
from Entities.Match import Match

session = Session()


def test_success_find_records():
    # Arrange
    with session_scope() as session:
        dummy_matchs = generate_dummy_match_list()
        for dummy_match in dummy_matchs:
            match_repository.create(
                session,
                dummy_match,
            )

    # Act
    with session_scope() as session:
        result = match_repository.find_all(
            session,
        )

    # Assert
        assert len(result) == len(dummy_matchs)
        for i in range(len(result)):
            assert isinstance(result[i], Match)
            assert result[i]._id == dummy_matchs[i]._id
            assert result[i].line_group_id == dummy_matchs[i].line_group_id
            assert result[i].hanchan_ids == dummy_matchs[i].hanchan_ids
            assert result[i].users == dummy_matchs[i].users
            assert result[i].status == dummy_matchs[i].status


def test_success_find_0_record():
    # Arrange
    # Do nothing

    # Act
    with session_scope() as session:
        result = match_repository.find_all(
            session,
        )

    # Assert
        assert len(result) == 0
