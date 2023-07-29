from DomainService import (
    match_service,
)
from repositories import match_repository
from DomainModel.entities.Match import Match

dummy_matches = [
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=1,
    )
]


def test_ok_hit_group(mocker):
    # Arrange
    mocker.patch.object(
        match_repository,
        'find',
        return_value=dummy_matches,
    )
    mock_create = mocker.patch.object(
        match_repository,
        'create',
        return_value=dummy_matches[0],
    )

    # Act
    result = match_service.find_or_create_current('G0123456789abcdefghijklmnopqrstu1')

    # Assert
    assert isinstance(result, Match)
    assert result.line_group_id == "G0123456789abcdefghijklmnopqrstu1"
    assert result.status == 1
    mock_create.assert_not_called()


def test_ok_no_group(mocker):
    # Arrange
    mocker.patch.object(
        match_repository,
        'find',
        return_value=[],
    )
    mock_create = mocker.patch.object(
        match_repository,
        'create',
        return_value=dummy_matches[0],
    )

    # Act
    result = match_service.find_or_create_current('G0123456789abcdefghijklmnopqrstu1')

    # Assert
    assert isinstance(result, Match)
    assert result.line_group_id == "G0123456789abcdefghijklmnopqrstu1"
    assert result.status == 1
    mock_create.assert_called_once()
