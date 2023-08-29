from DomainService import (
    hanchan_service,
)
from repositories import hanchan_repository
from DomainModel.entities.Hanchan import Hanchan

dummy_hanchans = [
    Hanchan(
        _id=1,
        match_id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
    )
]


def test_ok_hit_hanchan(mocker):
    # Arrange
    mock_update = mocker.patch.object(
        hanchan_repository,
        'update',
        return_value=1,
    )

    # Act
    hanchan_service.update(dummy_hanchans[0])

    # Assert
    mock_update.assert_called_once()
