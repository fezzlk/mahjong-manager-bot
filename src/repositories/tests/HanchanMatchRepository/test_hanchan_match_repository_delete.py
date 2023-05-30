from DomainModel.entities.Hanchan import Hanchan
from DomainModel.entities.Match import Match
from DomainModel.entities.HanchanMatch import HanchanMatch
from repositories import (
    hanchan_repository,
    match_repository,
    hanchan_match_repository,
)
from typing import List
from tests.dummies import (
    generate_dummy_hanchan_list,
    generate_dummy_match_list,
)

dummy_hanchans = generate_dummy_hanchan_list()
dummy_matches = generate_dummy_match_list()


def test_success():
    # Arrange
    hanchans: List[Hanchan] = []
    matches: List[Match] = []
    for dummy_hanchan in dummy_hanchans:
        hanchans.append(
            hanchan_repository.create(dummy_hanchan)
        )
    for dummy_match in dummy_matches:
        matches.append(
            match_repository.create(dummy_match)
        )
    dummy_hanchan_matches = [
        HanchanMatch(
            hanchan_id=hanchans[0]._id,
            match_id=matches[0]._id,
        ),
        HanchanMatch(
            hanchan_id=hanchans[1]._id,
            match_id=matches[0]._id,
        ),
        HanchanMatch(
            hanchan_id=hanchans[0]._id,
            match_id=matches[1]._id,
        ),
    ]
    for dummy_hanchan_match in dummy_hanchan_matches:
        hanchan_match_repository.create(
            dummy_hanchan_match,
        )

    # Act
    result = hanchan_match_repository.delete()

    # Assert
    assert result == 3
    
    record_on_db = hanchan_match_repository.find()
    assert len(record_on_db) == 0


def test_success_with_filter():
    # Arrange
    hanchans: List[Hanchan] = []
    matches: List[Match] = []
    for dummy_hanchan in dummy_hanchans:
        hanchans.append(
            hanchan_repository.create(dummy_hanchan)
        )
    for dummy_match in dummy_matches:
        matches.append(
            match_repository.create(dummy_match)
        )
    dummy_hanchan_matches = [
        HanchanMatch(
            hanchan_id=hanchans[0]._id,
            match_id=matches[0]._id,
        ),
        HanchanMatch(
            hanchan_id=hanchans[1]._id,
            match_id=matches[0]._id,
        ),
        HanchanMatch(
            hanchan_id=hanchans[0]._id,
            match_id=matches[1]._id,
        ),
    ]
    for dummy_hanchan_match in dummy_hanchan_matches:
        hanchan_match_repository.create(
            dummy_hanchan_match,
        )
    target = dummy_hanchan_matches[0]

    # Act
    result = hanchan_match_repository.delete(
        query={
            'hanchan_id': target.hanchan_id,
        },
    )

    # Assert
    assert result == 2
    
    record_on_db = hanchan_match_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0].hanchan_id == dummy_hanchan_matches[1].hanchan_id
    assert record_on_db[0].match_id == dummy_hanchan_matches[1].match_id

