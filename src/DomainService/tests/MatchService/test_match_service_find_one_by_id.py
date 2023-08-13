from DomainService import (
    match_service,
)
from repositories import match_repository
from DomainModel.entities.Match import Match

dummy_matches = [
    Match(
        _id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=1,
    )
]


def test_ok_hit_match(mocker):
    # Arrange
    mocker.patch.object(
        match_repository,
        'find',
        return_value=dummy_matches,
    )

    # Act
    result = match_service.find_one_by_id(1)

    # Assert
    assert isinstance(result, Match)
    assert result.line_group_id == "G0123456789abcdefghijklmnopqrstu1"
    assert result.status == 1


def test_ok_no_match(mocker):
    # Arrange
    mocker.patch.object(
        match_repository,
        'find',
        return_value=[],
    )

    # Act
    result = match_service.find_one_by_id(1)

    # Assert
    assert result is None
