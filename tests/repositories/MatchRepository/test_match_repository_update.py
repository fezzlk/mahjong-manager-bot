from DomainModel.entities.Match import Match
from repositories import match_repository

dummy_matches = [
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        active_hanchan_id=1,
    ),
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        active_hanchan_id=2,
    ),
]


def test_hit_1_record():
    # Arrange
    match_repository.create(dummy_matches[0])

    # Act
    result = match_repository.update(
        query={"line_group_id": dummy_matches[0].line_group_id},
        new_values={
            "active_hanchan_id": dummy_matches[1].active_hanchan_id,
        },
    )

    # Assert
    assert result == 1
    record_on_db = match_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0].line_group_id == dummy_matches[1].line_group_id
    assert record_on_db[0].active_hanchan_id == dummy_matches[1].active_hanchan_id


def test_hit_0_record():
    # Arrange

    # Act
    result = match_repository.update(
        query={"line_group_id": "dummy"},
        new_values={"active_hanchan_id": dummy_matches[1].active_hanchan_id},
    )

    # Assert
    assert result == 0
