import pytest
from DomainService.UserService import UserService
from repositories import session_scope, user_repository
from tests.dummies import generate_dummy_user_list
from DomainModel.entities.Group import GroupMode


# def test_success(): 現在 UserMode が一種類しかないため
def test_fail_with_invalid_mode():
    with pytest.raises(BaseException):
        # Arrange
        user_service = UserService()
        dummy_user = generate_dummy_user_list()[4]
        with session_scope() as session:
            user_repository.create(session, dummy_user)

        # Act
        user_service.chmod(
            line_user_id=dummy_user.line_user_id,
            mode=GroupMode.input
        )

        # Assert
