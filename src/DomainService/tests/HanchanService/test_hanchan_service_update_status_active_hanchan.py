from DomainService import (
    hanchan_service,
)
from repositories import hanchan_repository
from DomainModel.entities.Hanchan import Hanchan

dummy_hanchans = [
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=1,
        match_id=1,
        _id=1,
    )
]


def test_ok_hit_hanchan(mocker):
    # Arrange
    mocker.patch.object(
        hanchan_repository,
        'find',
        return_value=dummy_hanchans,
    )
    mock_update = mocker.patch.object(
        hanchan_repository,
        'update',
        return_value=1,
    )

    # Act
    hanchan_service.update_status_active_hanchan(
        'G0123456789abcdefghijklmnopqrstu1',
        0,
    )

    # Assert
    mock_update.assert_called_once_with(
        {'_id': 1},
        {'status': 0},
    )


def test_ok_no_hanchan(mocker):
    # Arrange
    mocker.patch.object(
        hanchan_repository,
        'find',
        return_value=[],
    )
    mock_update = mocker.patch.object(
        hanchan_repository,
        'update',
        return_value=1,
    )

    # Act
    hanchan_service.update_status_active_hanchan(
        'G0123456789abcdefghijklmnopqrstu1',
        0,
    )

    # Assert
    mock_update.assert_not_called()
