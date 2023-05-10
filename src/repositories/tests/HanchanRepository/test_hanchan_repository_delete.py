from tests.dummies import (
    generate_dummy_hanchan_list,
    generate_dummy_match_list,
)
from repositories import hanchan_repository, match_repository


def test_hit_with_line_group_id():
    # Arrange
    dummy_matches = generate_dummy_match_list()[:3]
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )
    dummy_hanchans = generate_dummy_hanchan_list()[:7]
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(
            dummy_hanchan,
        )
    other_hanchans = dummy_hanchans[0:1]
    target_hanchans = dummy_hanchans[1:3]
    line_group_ids = [target_hanchan.line_group_id for target_hanchan in target_hanchans]

    # Act
    result = hanchan_repository.delete(
        query={'line_group_id': {'$in': line_group_ids}},
    )

    # Assert
    assert result == len(target_hanchans)
    record_on_db = hanchan_repository.find()
    assert len(record_on_db) == len(other_hanchans)
    for i in range(len(record_on_db)):
        assert record_on_db[i].line_group_id == other_hanchans[i].line_group_id
        assert record_on_db[i].line_group_id == other_hanchans[i].line_group_id
        assert record_on_db[i].raw_scores == other_hanchans[i].raw_scores
        assert record_on_db[i].converted_scores == other_hanchans[i].converted_scores
        assert record_on_db[i].match_id == other_hanchans[i].match_id
        assert record_on_db[i].status == other_hanchans[i].status


def test_hit_0_record():
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
    other_hanchans = dummy_hanchans

    # Act
    result = hanchan_repository.delete(
        query={'line_group_id': {'$in': []}},
    )

    # Assert
    assert result == 0
    record_on_db = hanchan_repository.find()
    assert len(record_on_db) == len(other_hanchans)
    for i in range(len(record_on_db)):
        assert record_on_db[i].line_group_id == other_hanchans[i].line_group_id
        assert record_on_db[i].line_group_id == other_hanchans[i].line_group_id
        assert record_on_db[i].raw_scores == other_hanchans[i].raw_scores
        assert record_on_db[i].converted_scores == other_hanchans[i].converted_scores
        assert record_on_db[i].match_id == other_hanchans[i].match_id
        assert record_on_db[i].status == other_hanchans[i].status
