from typing import List

from bson.objectid import ObjectId

from DomainModel.entities.Match import Match
from repositories import match_repository
from tests.dummies import generate_dummy_match_list


def test_success_find_records():
    # Arrange
    dummy_matches = generate_dummy_match_list()
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )
    target_matches: List[Match] = []
    target_matches.append(dummy_matches[0])
    target_matches.append(dummy_matches[2])

    # Act
    result = match_repository.find()

    # Assert
    assert len(result) == len(target_matches)
    for i in range(len(result)):
        assert isinstance(result[i], Match)
        assert type(result[i]._id) is ObjectId
        assert result[i].line_group_id == target_matches[i].line_group_id
        assert result[i].status == target_matches[i].status


def test_success_find_0_record():
    # Arrange
    # Do nothing

    # Act
    result = match_repository.find()

    # Assert
    assert len(result) == 0


def test_hit_records():
    # Arrange
    dummy_matches = generate_dummy_match_list()
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )
    target_matches: List[Match] = []
    target_matches.append(dummy_matches[0])
    target_matches.append(dummy_matches[2])

    # Act
    result = match_repository.find(
        query={
            "line_group_id": target_matches[0].line_group_id,
        },
    )

    # Assert
    assert len(result) == len(target_matches)
    for i in range(len(result)):
        assert isinstance(result[i], Match)
        assert type(result[i]._id) is ObjectId
        assert result[i].line_group_id == target_matches[i].line_group_id
        assert result[i].status == target_matches[i].status


def test_hit_0_record_with_not_exist_line_group_id():
    # Arrange
    dummy_matches = generate_dummy_match_list()
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )

    # Act
    result = match_repository.find(
        query={
            "line_group_id": "dummy",
        },
    )

    # Assert
    assert len(result) == 0
