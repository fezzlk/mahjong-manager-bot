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


def test_ok(mocker):
    # Arrange
    mock_delete = mocker.patch.object(
        group_repository,
        'delete',
    )

    # Act
    group_service.delete_by_line_group_id(line_group_id='hoge')

    # Assert
    mock_delete.assert_called_once_with({
        'line_group_id': 'hoge'
    })