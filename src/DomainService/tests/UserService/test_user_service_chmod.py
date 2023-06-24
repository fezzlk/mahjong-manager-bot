from DomainService import (
    user_service,
)
from repositories import user_repository
from DomainModel.entities.User import User, UserMode
import pytest

dummy_users = [
    User(
        line_user_name="test_user1",
        line_user_id="U0123456789abcdefghijklmnopqrstu1",
        mode=UserMode.wait.value,
        jantama_name="jantama_user1",
    )
]


# UserModeが1種類のため呼び出しのテストのみ
def test_ok(mocker):
    # Arrange
    mocker.patch.object(
        user_repository,
        'update',
    )

    # Act
    user_service.chmod(line_user_id='hoge', mode=UserMode.wait)

    # Assert


def test_ng_invalid_mode():
    with pytest.raises(ValueError):
        # Arrange

        # Act, Assert
        user_service.chmod(line_user_id='hoge', mode='hoge')
