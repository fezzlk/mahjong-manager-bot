import pytest
from DomainModel.entities.Group import Group, GroupMode


def test_success():
    # Arrange

    # Act
    Group(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
        mode=GroupMode.wait.value,
    )
    
    # Assert


def test_error_invalid_mode():
    with pytest.raises(ValueError):
        # Arrange

        # Act
        Group(
            line_group_id="G0123456789abcdefghijklmnopqrstu2",
            mode='',
        )
        # Assert
