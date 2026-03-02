from domain_model.entities.hanchan import Hanchan
from domain_service import (
    hanchan_service,
)
from repositories import hanchan_repository

dummy_hanchans = [
    Hanchan(
        match_id=1,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
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
    mock_create.assert_called_once()
    call_args = mock_create.call_args[0][0]
    assert call_args.line_group_id == dummy_hanchans[0].line_group_id
    assert call_args.match_id == dummy_hanchans[0].match_id
