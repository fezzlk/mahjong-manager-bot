from typing import List

from bson.objectid import ObjectId

from DomainModel.entities.Hanchan import Hanchan
from repositories import hanchan_repository, match_repository
from dummies import (
    generate_dummy_hanchan_list,
    generate_dummy_match_list,
)


def test_success_find_records():
    # Arrange
    dummy_matches = generate_dummy_match_list()
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )
    dummy_hanchans = generate_dummy_hanchan_list()
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(
            dummy_hanchan,
        )
    target_hanchans: List[Hanchan] = []
    target_hanchans.append(dummy_hanchans[0])
    target_hanchans.append(dummy_hanchans[2])

    # Act
    result = hanchan_repository.find()

    # Assert
    assert len(result) == len(target_hanchans)
    for i in range(len(result)):
        assert isinstance(result[i], Hanchan)
        assert type(result[0]._id) is ObjectId
        assert result[i].line_group_id == target_hanchans[i].line_group_id
        assert result[i].match_id == target_hanchans[i].match_id
        assert result[i].raw_scores == target_hanchans[i].raw_scores
        assert result[i].converted_scores == target_hanchans[i].converted_scores
        assert result[i].status == target_hanchans[i].status


def test_hit_1_record():
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
    target_hanchan = dummy_hanchans[0]

    # Act
    result = hanchan_repository.find(
        query={
            "line_group_id": target_hanchan.line_group_id,
            "status": target_hanchan.status,
        },
    )

    # Assert
    assert len(result) == 1
    assert isinstance(result[0], Hanchan)
    assert type(result[0]._id) is ObjectId
    assert result[0].line_group_id == target_hanchan.line_group_id
    assert result[0].match_id == target_hanchan.match_id
    assert result[0].raw_scores == target_hanchan.raw_scores
    assert result[0].converted_scores == target_hanchan.converted_scores
    assert result[0].status == target_hanchan.status


def test_hit_0_record_with_not_exist_line_group_id():
    # Arrange
    dummy_matches = generate_dummy_match_list()[:3]
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )
    dummy_hanchans = generate_dummy_hanchan_list()[:4]
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(
            dummy_hanchan,
        )

    # Act
    result = hanchan_repository.find(
        query={
            "line_group_id": "dummy",
        },
    )

    # Assert
    assert len(result) == 0


def test_hit_0_record_with_not_exist_status():
    # Arrange
    dummy_matches = generate_dummy_match_list()[:3]
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )
    dummy_hanchans = generate_dummy_hanchan_list()[:2]
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(
            dummy_hanchan,
        )
    target_hanchan = generate_dummy_hanchan_list()[2]

    # Act
    result = hanchan_repository.find(
        query={
            "line_group_id": target_hanchan.line_group_id,
            "status": target_hanchan.status,
        },
    )

    # Assert
    assert len(result) == 0
