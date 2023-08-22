from DomainService import (
    user_service,
)
from repositories import user_repository
from DomainModel.entities.User import User, UserMode

dummy_users = [
    User(
        line_user_name="test_user1",
        line_user_id="U0123456789abcdefghijklmnopqrstu1",
        mode=UserMode.wait.value,
        jantama_name="jantama_user1",
    )
]


def test_ok(mocker):
    # Arrange
    mocker.patch.object(
        user_repository,
        'find',
        return_value=dummy_users,
    )

    # Act
    result = user_service.find_one_by_line_user_id(line_user_id='hoge')

    # Assert
    assert isinstance(result, User)
    assert result.line_user_name == dummy_users[0].line_user_name
    assert result.line_user_id == dummy_users[0].line_user_id
    assert result.mode == dummy_users[0].mode
    assert result.jantama_name == dummy_users[0].jantama_name


def test_ng_no_user(mocker):
    # Arrange
    mocker.patch.object(
        user_repository,
        'find',
        return_value=[],
    )

    # Act
    result = user_service.find_one_by_line_user_id(line_user_id='hoge')

    # Assert
    assert result is None