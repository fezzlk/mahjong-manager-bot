from DomainModel.entities.Hanchan import Hanchan
from DomainService import (
    hanchan_service,
)
from repositories import hanchan_repository

dummy_hanchans = [
    Hanchan(
        match_id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        status=2,
    ),
]


def test_ok(mocker):
    # Arrange
    mock_create = mocker.patch.object(
        hanchan_repository,
        "create",
        return_value=dummy_hanchans[0],
    )

    # Act
    hanchan_service.create_with_line_group_id_and_match_id(
        "G0123456789abcdefghijklmnopqrstu1",
        1,
    )

    # Assert
    mock_create.assert_called_once_with(dummy_hanchans[0])
