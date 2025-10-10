from ApplicationService.MessageService import MessageService, yaku_list
from tests.dummies import generate_dummy_user_list


def test_success():
    # Arrange
    message_service = MessageService()
    dummy_user = generate_dummy_user_list()[0]

    # Act
    result = message_service.get_random_yaku(dummy_user.line_user_id)

    # Assert
    assert result in yaku_list
