from tests.dummies import generate_dummy_match_list
from repositories import match_repository
from DomainModel.entities.Match import Match
from bson.objectid import ObjectId


def test_success_find_records():
    # Arrange
    dummy_matches = generate_dummy_match_list()
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )

    # Act
    result = match_repository.find()

    # Assert
    assert len(result) == len(dummy_matches)
    for i in range(len(result)):
        assert isinstance(result[i], Match)
        assert type(result[i]._id) == ObjectId
        assert result[i].line_group_id == dummy_matches[i].line_group_id
        assert result[i].hanchan_ids == dummy_matches[i].hanchan_ids
        assert result[i].status == dummy_matches[i].status


def test_success_find_0_record():
    # Arrange
    # Do nothing

    # Act
    result = match_repository.find()

    # Assert
    assert len(result) == 0


def test_hit_1_record():
    # Arrange
    dummy_matches = generate_dummy_match_list()[:3]
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )
    target_match = dummy_matches[0]

    # Act
    result = match_repository.find(
        query={
            'line_group_id': target_match.line_group_id,
            'status': target_match.status,
        },
    )

    # Assert
    assert len(result) == 1
    assert isinstance(result[0], Match)
    assert type(result[0]._id) == ObjectId
    assert result[0].line_group_id == target_match.line_group_id
    assert result[0].hanchan_ids == target_match.hanchan_ids
    assert result[0].status == target_match.status


def test_hit_records():
    # Arrange
    dummy_matches = generate_dummy_match_list()[:4]
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )
    target_matches = dummy_matches[2:4]
    target_matches.reverse()

    # Act
    result = match_repository.find(
        query={
            'line_group_id': target_matches[0].line_group_id,
            'status': target_matches[0].status,
        },
    )

    # Assert
    assert len(result) == len(target_matches)
    for i in range(len(result)):
        assert isinstance(result[i], Match)
        assert type(result[i]._id) == ObjectId
        assert result[i].line_group_id == target_matches[i].line_group_id
        assert result[i].hanchan_ids == target_matches[i].hanchan_ids
        assert result[i].status == target_matches[i].status


def test_hit_0_record_with_not_exist_line_group_id():
    # Arrange
    dummy_matches = generate_dummy_match_list()[:3]
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )
    target_match = generate_dummy_match_list()[4]

    # Act
    result = match_repository.find(
        query={
            'line_group_id': target_match.line_group_id,
            'status': target_match.status,
        },
    )

    # Assert
    assert len(result) == 0


def test_hit_0_record_with_not_exist_status():
    # Arrange
    dummy_matches = generate_dummy_match_list()[:2]
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )
    target_match = generate_dummy_match_list()[2]

    # Act
    result = match_repository.find(
        query={
            'line_group_id': target_match.line_group_id,
            'status': target_match.status,
        },
    )

    # Assert
    assert len(result) == 0
