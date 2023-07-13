from DomainService import (
    group_service,
)
from repositories import group_repository
from DomainModel.entities.Group import Group, GroupMode

dummy_groups = [
    Group(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        mode=GroupMode.wait.value,
    )
]


def test_ok_hit_group(mocker):
    # Arrange
    mocker.patch.object(
        group_repository,
        'find',
        return_value=dummy_groups,
    )
    mock_create = mocker.patch.object(
        group_repository,
        'create',
        return_value=dummy_groups[0],
    )

    # Act
    result = group_service.find_or_create('G0123456789abcdefghijklmnopqrstu1')

    # Assert
    assert isinstance(result, Group)
    assert result.line_group_id == "G0123456789abcdefghijklmnopqrstu1"
    assert result.mode == 'wait'
    mock_create.assert_not_called()


def test_ok_no_group(mocker):
    # Arrange
    mocker.patch.object(
        group_repository,
        'find',
        return_value=[],
    )

    mocker.patch.object(
        group_repository,
        'create',
        return_value=dummy_groups[0],
    )

    # Act
    result = group_service.find_or_create('G0123456789abcdefghijklmnopqrstu1')

    # Assert
    assert isinstance(result, Group)
    assert result.line_group_id == "G0123456789abcdefghijklmnopqrstu1"
    assert result.mode == 'wait'
