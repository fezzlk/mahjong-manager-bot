from DomainService import (
    match_service,
)
from repositories import match_repository
from DomainModel.entities.Match import Match

dummy_matches = [
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=1,
        _id=1,
    )
]


def test_ok_hit_match(mocker):
    # Arrange
    mocker.patch.object(
        match_repository,
        'find',
        return_value=dummy_matches,
    )
    mock_update = mocker.patch.object(
        match_repository,
        'update',
        return_value=1,
    )

    # Act
    result = match_service.update_status_active_match(
        'G0123456789abcdefghijklmnopqrstu1',
        0,
    )

    # Assert
    assert isinstance(result, Match)
    assert result.line_group_id == "G0123456789abcdefghijklmnopqrstu1"
    assert result.status == 0
    mock_update.assert_called_once_with(
        {'_id': 1},
        {'status': 0},
    )


def test_ok_no_match(mocker):
    # Arrange
    mocker.patch.object(
        match_repository,
        'find',
        return_value=[],
    )
    mock_update = mocker.patch.object(
        match_repository,
        'update',
        return_value=1,
    )

    # Act
    result = match_service.update_status_active_match(
        'G0123456789abcdefghijklmnopqrstu1',
        0,
    )

    # Assert
    assert result is None
    mock_update.assert_not_called()
