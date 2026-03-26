from domain_model.entities.hanchan import Hanchan
from domain_service import (
    hanchan_service,
)
from repositories import hanchan_repository

dummy_hanchans = [
    Hanchan(
        _id=1,
        match_id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
    ),
]


def test_ok_hit(mocker):
    # Arrange
    mock_update_many = mocker.patch.object(
        hanchan_repository,
        "update_many",
        return_value=1,
    )

    # Act
    hanchan_service.disable_by_match_id(dummy_hanchans[0].match_id)

    # Assert
    mock_update_many.assert_called_once_with(
        {"match_id": 1},
        {"is_deleted": True},
    )
