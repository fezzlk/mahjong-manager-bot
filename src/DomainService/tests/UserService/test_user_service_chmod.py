from DomainService import (
    user_service,
)
from repositories import user_repository
from DomainModel.entities.User import UserMode
import pytest


def test_ok(mocker):
    # Arrange
    mock = mocker.patch.object(
        user_repository,
        'update',
    )

    # Act
    user_service.chmod(line_user_id='hoge', mode=UserMode.wait)

    # Assert
    mock.assert_called_once_with(query={'line_user_id': 'hoge'}, new_values={'mode': 'wait'})


def test_ng_invalid_mode():
    with pytest.raises(ValueError):
        # Arrange

        # Act, Assert
        user_service.chmod(line_user_id='hoge', mode='hoge')
