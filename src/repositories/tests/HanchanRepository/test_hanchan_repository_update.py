from DomainModel.entities.Match import Match
from DomainModel.entities.Hanchan import Hanchan
from repositories import hanchan_repository, match_repository
from tests.dummies import (
    generate_dummy_hanchan_list,
    generate_dummy_match_list,
)

dummy_match = Match(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    hanchan_ids=[1, 2, 3, 6, 7],
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
    match_repository.create(dummy_match[0])
    hanchan_repository.create(dummy_hanchans[0])

    # Act
    result = hanchan_repository.update(
        query={'line_group_id': dummy_hanchans[0].line_group_id},
        new_values={'status': dummy_hanchans[1].status},
    )

    # Assert
    assert result == 1
    record_on_db = hanchan_repository.find()
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
    result = hanchan_repository.update(
        query={},
        new_values={'status': dummy_hanchans[1].status},
    )

    # Assert
    assert result == 0


def test_update_raw_scores():
    # Arrange
    dummy_matches = generate_dummy_match_list()[:3]
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )
    dummy_hanchans = generate_dummy_hanchan_list()[:3]
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(
            dummy_hanchan,
        )
    dummy_raw_scores = {'a': 10000}

    # Act
    result = hanchan_repository.update(
        query={'_id': dummy_hanchans[0]._id},
        new_values={'raw_scores': dummy_raw_scores},
    )

    # Assert
    assert result == 1
    record_on_db = hanchan_repository.find()
    assert len(record_on_db) == len(dummy_hanchans)
    assert record_on_db[0]._id == dummy_hanchans[0]._id
    assert record_on_db[0].line_group_id == dummy_hanchans[0].line_group_id
    assert record_on_db[0].raw_scores == dummy_raw_scores
    assert record_on_db[0].converted_scores == dummy_hanchans[0].converted_scores
    assert record_on_db[0].match_id == dummy_hanchans[0].match_id
    assert record_on_db[0].status == dummy_hanchans[0].status


def test_update_converted_scores():
    # Arrange
    dummy_matches = generate_dummy_match_list()[:3]
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )
    dummy_hanchans = generate_dummy_hanchan_list()[:3]
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(
            dummy_hanchan,
        )
    dummy_converted_scores = {'a': 100}

    # Act
    result = hanchan_repository.update(
        query={'_id': dummy_hanchans[0]._id},
        new_values={'converted_scores': dummy_converted_scores},
    )

    # Assert
    assert result == 1
    record_on_db = hanchan_repository.find()
    assert len(record_on_db) == len(dummy_hanchans)
    assert record_on_db[0]._id == dummy_hanchans[0]._id
    assert record_on_db[0].line_group_id == dummy_hanchans[0].line_group_id
    assert record_on_db[0].raw_scores == dummy_hanchans[0].raw_scores
    assert record_on_db[0].converted_scores == dummy_converted_scores
    assert record_on_db[0].match_id == dummy_hanchans[0].match_id
    assert record_on_db[0].status == dummy_hanchans[0].status
