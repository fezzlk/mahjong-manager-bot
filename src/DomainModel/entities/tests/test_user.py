import pytest
from DomainModel.entities.User import User, UserMode


def test_success():
    # Arrange

    # Act
    User(
        line_user_id="G0123456789abcdefghijklmnopqrstu2",
        mode=UserMode.wait.value,
    )
    
    # Assert


def test_error_invalid_mode():
    with pytest.raises(ValueError):
        # Arrange

        # Act
        User(
            line_user_id="G0123456789abcdefghijklmnopqrstu2",
            mode='',
        )
        # Assert
