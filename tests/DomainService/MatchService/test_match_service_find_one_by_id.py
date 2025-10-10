from DomainModel.entities.Match import Match
from DomainService import (
    match_service,
)
from repositories import match_repository

dummy_matches = [
    Match(
        _id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
    ),
]


def test_ok_hit_match(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        match_repository,
        "find",
        return_value=dummy_matches,
    )

    # Act
    result = match_service.find_one_by_id(1)

    # Assert
    assert isinstance(result, Match)
    assert result.line_group_id == "G0123456789abcdefghijklmnopqrstu1"
    assert result.status == 2
    mock_find.assert_called_once_with({"_id": 1})


def test_no_hit(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        match_repository,
        "find",
        return_value=[],
    )

    # Act
    result = match_service.find_one_by_id(1)

    # Assert
    assert result is None
    mock_find.assert_called_once_with({"_id": 1})
