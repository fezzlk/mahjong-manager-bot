from DomainService import (
    group_service,
)
from repositories import group_repository
from DomainModel.entities.Group import Group, GroupMode

dummy_groups = [
    Group(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        mode=GroupMode.wait.value,
    )
]


def test_ok(mocker):
    # Arrange
    mock_update = mocker.patch.object(
        group_repository,
        'update',
    )

    # Act
    group_service.update(dummy_groups[0])

    # Assert
    mock_update.assert_called_once_with(
        {'_id': 999},
        {
            '_id': 999,
            'line_group_id': 'G0123456789abcdefghijklmnopqrstu1',
            'mode': 'wait',
            'active_match_id': None,
        },
    )