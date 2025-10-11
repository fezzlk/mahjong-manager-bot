from DomainModel.entities.Group import Group, GroupMode
from DomainService import (
    group_service,
)
from repositories import group_repository

dummy_groups = [
    Group(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        mode=GroupMode.wait.value,
    ),
]


def test_ok(mocker):
    # Arrange
    mocker.patch.object(
        group_repository,
        "find",
        return_value=dummy_groups,
    )

    # Act
    result = group_service.get_mode(line_group_id="hoge")

    # Assert
    assert result == "wait"


def test_ng_no_group(mocker):
    # Arrange
    mocker.patch.object(
        group_repository,
        "find",
        return_value=[],
    )

    # Act
    mode = group_service.get_mode(line_group_id="hoge")

    # Assert
    assert mode is None
