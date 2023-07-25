from tests.dummies import (
    generate_dummy_match_list,
)
from repositories import match_repository
from DomainModel.entities.Match import Match


def test_hit_with_line_group_id():
    # Arrange
    dummy_matches = generate_dummy_match_list()[:5]
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )
    other_matches = dummy_matches[4:5]
    target_matches = dummy_matches[0:4]
    line_group_ids = [target_match.line_group_id for target_match in target_matches]

    # Act
    result = match_repository.delete(
        query={'line_group_id': {'$in': line_group_ids}},
    )

    # Assert
    assert result == len(target_matches)
    record_on_db = match_repository.find()
    assert len(record_on_db) == len(other_matches)
    for i in range(len(record_on_db)):
        assert isinstance(record_on_db[i], Match)
        assert record_on_db[i].line_group_id == other_matches[i].line_group_id
        assert record_on_db[i].hanchan_ids == other_matches[i].hanchan_ids
        assert record_on_db[i].status == other_matches[i].status


def test_hit_0_record():
    # Arrange
    dummy_matches = generate_dummy_match_list()[:3]
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )

    # Act
    result = match_repository.delete(
        query={'line_group_id': {'$in': []}},
    )

    # Assert
    assert result == 0
    record_on_db = match_repository.find()
    assert len(record_on_db) == len(dummy_matches)
    for i in range(len(record_on_db)):
        assert isinstance(record_on_db[i], Match)
        assert record_on_db[i].line_group_id == dummy_matches[i].line_group_id
        assert record_on_db[i].hanchan_ids == dummy_matches[i].hanchan_ids
        assert record_on_db[i].status == dummy_matches[i].status
