from DomainModel.entities.Match import Match
from DomainService import (
    match_service,
)
from repositories import match_repository

dummy_matches = [
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
    ),
]


def test_ok_no_group(mocker):
    # Arrange
    mock_create = mocker.patch.object(
        match_repository,
        "create",
        return_value=dummy_matches[0],
    )

    # Act
    result = match_service.create_with_line_group_id("G0123456789abcdefghijklmnopqrstu1")

    # Assert
    assert isinstance(result, Match)
    assert result.line_group_id == "G0123456789abcdefghijklmnopqrstu1"
    mock_create.assert_called_once()
