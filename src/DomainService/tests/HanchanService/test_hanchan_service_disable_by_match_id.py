from DomainModel.entities.Hanchan import Hanchan
from DomainService import (
    hanchan_service,
)
from repositories import hanchan_repository

dummy_hanchans = [
    Hanchan(
        _id=1,
        match_id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
    ),
]


def test_ok_hit(mocker):
    # Arrange
    mock_update = mocker.patch.object(
        hanchan_repository,
        "update",
        return_value=1,
    )

    # Act
    hanchan_service.disable_by_match_id(dummy_hanchans[0].match_id)

    # Assert
    mock_update.assert_called_once_with(
        {"match_id": 1},
        {"status": 0},
    )
