from DomainService import (
    group_service,
)
from repositories import group_repository
from DomainModel.entities.Group import Group, GroupMode
from datetime import datetime

dummy_groups = [
    Group(
        _id=999,
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        mode=GroupMode.wait.value,
        created_at=datetime(2010,1,2,3,4,0,0),
        updated_at=datetime(2010,1,2,3,4,0,0),
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
            'created_at': datetime(2010,1,2,3,4,0,0),
            'updated_at': datetime(2010,1,2,3,4,0,0),
        },
    )