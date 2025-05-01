from typing import List

from DomainModel.entities.Match import Match
from repositories import match_repository
from tests.dummies import (
    generate_dummy_match_list,
)


def test_hit_with_line_group_id():
    # Arrange
    dummy_matches = generate_dummy_match_list()
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )
    other_match = dummy_matches[2]
    target_match = dummy_matches[0]

    # Act
    result = match_repository.delete(
        query={"line_group_id": {"$in": [target_match.line_group_id]}},
    )

    # Assert
    assert result == 3
    record_on_db = match_repository.find()
    assert len(record_on_db) == 0


def test_hit_0_record():
    # Arrange
    dummy_matches = generate_dummy_match_list()[:3]
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )
    target_matches:List[Match] = []
    target_matches.append(dummy_matches[0])
    target_matches.append(dummy_matches[2])


    # Act
    result = match_repository.delete(
        query={"line_group_id": {"$in": []}},
    )

    # Assert
    assert result == 0
    record_on_db = match_repository.find()
    assert len(record_on_db) == len(target_matches)
    for i in range(len(record_on_db)):
        assert isinstance(record_on_db[i], Match)
        assert record_on_db[i].line_group_id == target_matches[i].line_group_id
        assert record_on_db[i].status == target_matches[i].status
