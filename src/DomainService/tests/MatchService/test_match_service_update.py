from DomainService import (
    match_service,
)
from repositories import match_repository
from DomainModel.entities.Match import Match

dummy_matches = [
    Match(
        _id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
    )
]


def test_ok_hit_match(mocker):
    # Arrange
    mock_update = mocker.patch.object(
        match_repository,
        'update',
        return_value=1,
    )

    # Act
    match_service.update(dummy_matches[0])

    # Assert
    mock_update.assert_called_once()
