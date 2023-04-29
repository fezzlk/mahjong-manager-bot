from DomainModel.entities.Match import Match
from repositories import match_repository


dummy_matches = [
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        hanchan_ids=[1, 2, 3, 6, 7],
        status=1,
    ),
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        hanchan_ids=[4],
        status=2,
    ),
]


def test_hit_1_record():
    # Arrange
    match_repository.create(dummy_matches[0])

    # Act
    result = match_repository.update(
        query={'line_group_id': dummy_matches[0].line_group_id},
        new_values={
            'hanchan_ids': dummy_matches[1].hanchan_ids,
            'status': dummy_matches[1].status,
        },
    )

    # Assert
    assert result == 1
    record_on_db = match_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0].line_group_id == dummy_matches[1].line_group_id
    assert record_on_db[0].hanchan_ids == dummy_matches[1].hanchan_ids
    assert record_on_db[0].status == dummy_matches[1].status


def test_hit_0_record():
    # Arrange

    # Act
    result = match_repository.update(
        query={'line_group_id': 'dummy'},
        new_values={'status': dummy_matches[1].status},
    )

    # Assert
    assert result == 0
