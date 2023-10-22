from DomainService import (
    match_service,
)
from repositories import match_repository
from pymongo import DESCENDING
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
    result = match_service.find_latest_one('G0123456789abcdefghijklmnopqrstu1')

    # Assert
    assert isinstance(result, Match)
    mock_find.assert_called_once_with(query={'line_group_id': 'G0123456789abcdefghijklmnopqrstu1'}, sort=[('created_at', DESCENDING)])


def test_ok(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        match_repository,
        'find',
        return_value=[],
    )

    # Act
    result = match_service.find_latest_one('G0123456789abcdefghijklmnopqrstu1')

    # Assert
    assert result is None
    mock_find.assert_called_once_with(query={'line_group_id': 'G0123456789abcdefghijklmnopqrstu1'}, sort=[('created_at', DESCENDING)])