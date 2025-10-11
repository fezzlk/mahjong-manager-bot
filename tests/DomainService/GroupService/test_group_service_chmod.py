import pytest

from DomainModel.entities.Group import GroupMode
from DomainService import (
    group_service,
)
from repositories import group_repository


def test_ok(mocker):
    # Arrange
    mock = mocker.patch.object(
        group_repository,
        "update",
        return_value=1,
    )

    # Act
    group_service.chmod(line_group_id="hoge", mode=GroupMode.wait)

    # Assert
    mock.assert_called_once_with({"line_group_id": "hoge"}, {"mode": "wait"})


def test_ng_invalid_mode():
    with pytest.raises(ValueError):
        # Arrange

        # Act, Assert
        group_service.chmod(line_group_id="hoge", mode="hoge")


def test_ng_no_group_id():
    with pytest.raises(ValueError):
        # Arrange

        # Act, Assert
        group_service.chmod(line_group_id=None, mode=GroupMode.wait)
