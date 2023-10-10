from DomainService import (
    match_service,
)
from repositories import match_repository
from pymongo import ASCENDING
from DomainModel.entities.Match import Match

dummy_matches = [
    Match(
        _id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
    ),
    Match(
        _id=2,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
    ),
]

def test_ok(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        match_repository,
        'find',
        return_value=dummy_matches,
    )

    # Act
    result = match_service.find_all_archived_by_line_group_id(line_group_id="G0123456789abcdefghijklmnopqrstu1")

    # Assert
    assert len(result) == 2
    mock_find.assert_called_once_with(query={'line_group_id': 'G0123456789abcdefghijklmnopqrstu1', 'sum_prices_with_tip': {"$ne": {}}}, sort=[('created_at', ASCENDING)])