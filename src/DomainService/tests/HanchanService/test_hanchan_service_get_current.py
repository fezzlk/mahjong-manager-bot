from DomainService import (
    hanchan_service,
)
from repositories import hanchan_repository
from DomainModel.entities.Hanchan import Hanchan

dummy_hanchans = [
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=1,
        match_id=1
    )
]


def test_ok_hit_match(mocker):
    # Arrange
    mocker.patch.object(
        hanchan_repository,
        'find',
        return_value=dummy_hanchans,
    )

    # Act
    result = hanchan_service.get_current('G0123456789abcdefghijklmnopqrstu1')

    # Assert
    assert isinstance(result, Hanchan)
    assert result.line_group_id == "G0123456789abcdefghijklmnopqrstu1"
    assert result.status == 1


def test_ok_no_match(mocker):
    # Arrange
    mocker.patch.object(
        hanchan_repository,
        'find',
        return_value=[],
    )

    # Act
    result = hanchan_service.get_current('G0123456789abcdefghijklmnopqrstu1')

    # Assert
    assert result is None
