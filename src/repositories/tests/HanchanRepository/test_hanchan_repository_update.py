from DomainModel.entities.Match import Match
from DomainModel.entities.Hanchan import Hanchan
from repositories import session_scope, hanchan_repository, match_repository

dummy_match = Match(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    hanchan_ids=[1, 2, 3, 6, 7],
    users=[],
    status=1,
    _id=1,
),

dummy_hanchans = [
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        raw_scores={},
        converted_scores={},
        match_id=1,
        status=1,
        _id=1,
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        raw_scores={},
        converted_scores={},
        match_id=1,
        status=2,
        _id=1,
    ),
]


def test_hit_1_record():
    # Arrange
    with session_scope() as session:
        match_repository.create(session, dummy_match[0])
        hanchan_repository.create(session, dummy_hanchans[0])

    # Act
    with session_scope() as session:
        result = hanchan_repository.update(
            session=session,
            target=dummy_hanchans[1],
        )

    # Assert
    assert result == 1

    with session_scope() as session:
        record_on_db = hanchan_repository.find_all(
            session,
        )
        assert len(record_on_db) == 1
        assert record_on_db[0]._id == dummy_hanchans[1]._id
        assert record_on_db[0].line_group_id == dummy_hanchans[1].line_group_id
        assert record_on_db[0].raw_scores == dummy_hanchans[1].raw_scores
        assert record_on_db[0].converted_scores == dummy_hanchans[1].converted_scores
        assert record_on_db[0].match_id == dummy_hanchans[1].match_id
        assert record_on_db[0].status == dummy_hanchans[1].status


def test_hit_0_record():
    # Arrange

    # Act
    with session_scope() as session:
        result = hanchan_repository.update(
            session,
            dummy_hanchans[0],
        )

    # Assert
    assert result == 0
