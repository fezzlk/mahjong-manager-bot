import pytest
from DomainModel.entities.Group import Group, GroupMode
from datetime import datetime
from bson.objectid import ObjectId


def test_success():
    # Arrange

    # Act
    group = Group(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
        mode=GroupMode.input.value,
        active_match_id=2,
        _id=1,
        created_at=datetime(2022, 1, 2, 3, 4, 5),
        updated_at=datetime(2023, 1, 2, 3, 4, 5),
    )
    
    # Assert
    assert group._id == 1
    assert group.line_group_id == "G0123456789abcdefghijklmnopqrstu2"
    assert group.mode == GroupMode.input.value
    assert group.active_match_id == 2
    assert group.created_at == datetime(2022, 1, 2, 3, 4, 5)
    assert group.updated_at == datetime(2023, 1, 2, 3, 4, 5)

def test_success_default():
    # Arrange

    # Act
    group = Group(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
    )
    
    # Assert
    assert group._id is None
    assert group.line_group_id == "G0123456789abcdefghijklmnopqrstu2"
    assert group.mode == GroupMode.wait.value
    assert group.active_match_id is None
    assert group.created_at.date() == datetime.now().date()
    assert group.updated_at.date() == datetime.now().date()


def test_error_invalid_mode():
    with pytest.raises(ValueError):
        # Arrange

        # Act
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu2",
            mode='',
        )
        # Assert
