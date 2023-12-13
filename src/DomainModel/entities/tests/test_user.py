import pytest
from DomainModel.entities.User import User, UserMode
from datetime import datetime
from bson.objectid import ObjectId

def test_success():
    # Arrange

    # Act
    user = User(
        line_user_id="U0123456789abcdefghijklmnopqrstu2",
        line_user_name='dummy',
        mode=UserMode.wait.value,
        _id=1,
        jantama_name='jan',
        created_at=datetime(2022, 1, 2, 3, 4, 5),
        updated_at=datetime(2023, 1, 2, 3, 4, 5),
        original_id=2
    )
    
    # Assert
    assert user._id == 1
    assert user.line_user_id == "U0123456789abcdefghijklmnopqrstu2"
    assert user.line_user_name == 'dummy'
    assert user.mode == UserMode.wait.value
    assert user.jantama_name == 'jan'
    assert user.created_at == datetime(2022, 1, 2, 3, 4, 5)
    assert user.updated_at == datetime(2023, 1, 2, 3, 4, 5)
    assert user.original_id == 2


def test_success_default():
    # Arrange

    # Act
    user = User(
        line_user_id="U0123456789abcdefghijklmnopqrstu2",
    )
    
    # Assert
    assert user._id is None
    assert user.line_user_id == "U0123456789abcdefghijklmnopqrstu2"
    assert user.line_user_name is None
    assert user.mode == UserMode.wait.value
    assert user.jantama_name is None
    assert user.created_at.date() == datetime.now().date()
    assert user.updated_at.date() == datetime.now().date()
    assert user.original_id is None


def test_error_invalid_mode():
    with pytest.raises(ValueError):
        # Arrange

        # Act
        User(
            line_user_id="G0123456789abcdefghijklmnopqrstu2",
            mode='',
        )
        # Assert
