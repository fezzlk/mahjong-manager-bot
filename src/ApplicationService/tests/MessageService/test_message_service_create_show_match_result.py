from ApplicationService.MessageService import MessageService, wait_messages
from DomainModel.entities.Match import Match
from DomainService import (
    user_service,
)


dummy_match = Match(
    line_group_id='G0123456789abcdefghijklmnopqrstu1',
    status=2,
    sum_scores={
        'U0123456789abcdefghijklmnopqrstu1': 100,
        'U0123456789abcdefghijklmnopqrstu2': 20,
        'U0123456789abcdefghijklmnopqrstu3': -40,
        'U0123456789abcdefghijklmnopqrstu4': -40,
        'U0123456789abcdefghijklmnopqrstu5': -40,
    },
    sum_prices_with_tip={
        'U0123456789abcdefghijklmnopqrstu1': 3100,
        'U0123456789abcdefghijklmnopqrstu2': 600,
        'U0123456789abcdefghijklmnopqrstu3': -1300,
        'U0123456789abcdefghijklmnopqrstu4': -1200,
        'U0123456789abcdefghijklmnopqrstu5': -1200,
    },
    tip_scores={
        'U0123456789abcdefghijklmnopqrstu1': 10,
        'U0123456789abcdefghijklmnopqrstu3': -10,
    },
    _id=1,
)


def test_success(mocker):
    # Arrange
    mocker.patch.object(
        user_service,
        'get_name_by_line_user_id',
        return_value=None,
    )
    message_service = MessageService()

    # Act
    result = message_service.create_show_match_result(dummy_match)

    # Assert
    assert result == '友達未登録: 3100円 (+100(+10枚))\n友達未登録: 600円 (+20(0枚))\n友達未登録: -1300円 (-40(-10枚))\n友達未登録: -1200円 (-40(0枚))\n友達未登録: -1200円 (-40(0枚))'


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
        if arg == 'U0123456789abcdefghijklmnopqrstu5':
            return 'test_user_5'
        
    mocker.patch.object(
        user_service,
        'get_name_by_line_user_id',
        side_effect=mock_behavior,
    )
    message_service = MessageService()

    # Act
    result = message_service.create_show_match_result(dummy_match)

    # Assert
    assert result == 'test_user_1: 3100円 (+100(+10枚))\ntest_user_2: 600円 (+20(0枚))\ntest_user_3: -1300円 (-40(-10枚))\ntest_user_4: -1200円 (-40(0枚))\ntest_user_5: -1200円 (-40(0枚))'