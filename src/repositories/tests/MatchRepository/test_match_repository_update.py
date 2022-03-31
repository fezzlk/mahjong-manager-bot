from DomainModel.entities.Match import Match
from repositories import session_scope, match_repository


dummy_matchs = [
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        hanchan_ids=[1, 2, 3, 6, 7],
        users=[],
        status=1,
        _id=1,
    ),
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        hanchan_ids=[4],
        users=[],
        status=2,
        _id=1,
    ),
]


def test_hit_1_record():
    # Arrange
    with session_scope() as session:
        match_repository.create(session, dummy_matchs[0])

    # Act
    with session_scope() as session:
        result = match_repository.update(
            session=session,
            target=dummy_matchs[1],
        )

    # Assert
    assert result == 1

    with session_scope() as session:
        record_on_db = match_repository.find_all(
            session,
        )
        assert len(record_on_db) == 1
        assert record_on_db[0]._id == dummy_matchs[1]._id
        assert record_on_db[0].line_group_id == dummy_matchs[1].line_group_id
        assert record_on_db[0].hanchan_ids == dummy_matchs[1].hanchan_ids
        assert record_on_db[0].users == dummy_matchs[1].users
        assert record_on_db[0].status == dummy_matchs[1].status


def test_hit_0_record():
    # Arrange

    # Act
    with session_scope() as session:
        result = match_repository.update(
            session,
            dummy_matchs[0],
        )

    # Assert
    assert result == 0
