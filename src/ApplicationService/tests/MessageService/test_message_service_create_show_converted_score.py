from ApplicationService.MessageService import MessageService, wait_messages
from DomainService import (
    user_service,
)

converted_score={
    'U0123456789abcdefghijklmnopqrstu1': 50,
    'U0123456789abcdefghijklmnopqrstu3': -40,
    'U0123456789abcdefghijklmnopqrstu2': 10,
    'U0123456789abcdefghijklmnopqrstu4': -20,
}


def test_success_with_unknown_users(mocker):
    # Arrange
    mocker.patch.object(
        user_service,
        'get_name_by_line_user_id',
        return_value=None,
    )
    message_service = MessageService()

    # Act
    result = message_service.create_show_converted_scores(converted_scores=converted_score)

    # Assert
    assert result == "友達未登録: +50\n友達未登録: +10\n友達未登録: -20\n友達未登録: -40"


def test_success(mocker):
    # Arrange
    def mock_behavior(arg):
        if arg == 'U0123456789abcdefghijklmnopqrstu1':
            return 'test_user_1'
        if arg == 'U0123456789abcdefghijklmnopqrstu2':
            return 'test_user_2'
        if arg == 'U0123456789abcdefghijklmnopqrstu3':
            return 'test_user_3'
        if arg == 'U0123456789abcdefghijklmnopqrstu4':
            return 'test_user_4'
        
    mocker.patch.object(
        user_service,
        'get_name_by_line_user_id',
        side_effect=mock_behavior,
    )
    message_service = MessageService()
    
    # Act
    result = message_service.create_show_converted_scores(converted_scores=converted_score)

    # Assert
    assert result == "test_user_1: +50\ntest_user_2: +10\ntest_user_4: -20\ntest_user_3: -40"


sum_scores={
    'U0123456789abcdefghijklmnopqrstu1': 10,
    'U0123456789abcdefghijklmnopqrstu3': -10,
    'U0123456789abcdefghijklmnopqrstu2': 20,
}

def test_success_with_sum_scores(mocker):
    # Arrange
    def mock_behavior(arg):
        if arg == 'U0123456789abcdefghijklmnopqrstu1':
            return 'test_user_1'
        if arg == 'U0123456789abcdefghijklmnopqrstu2':
            return 'test_user_2'
        if arg == 'U0123456789abcdefghijklmnopqrstu3':
            return 'test_user_3'
        if arg == 'U0123456789abcdefghijklmnopqrstu4':
            return 'test_user_4'
        
    mocker.patch.object(
        user_service,
        'get_name_by_line_user_id',
        side_effect=mock_behavior,
    )
    message_service = MessageService()
    
    # Act
    result = message_service.create_show_converted_scores(
        converted_scores=converted_score,
        sum_scores=sum_scores,
    )

    # Assert
    assert result == "test_user_1: +50 (+10)\ntest_user_2: +10 (+20)\ntest_user_4: -20 (-20)\ntest_user_3: -40 (-10)"

