from tests.dummies import (
    generate_dummy_text_message_event_from_user,
    generate_dummy_profile,
)
from use_cases import FollowUseCase
from services import (
    request_info_service,
    rich_menu_service,
    reply_service,
)
from messaging_api_setting import line_bot_api


def test_execute(mocker):
    # Arrage
    dummy_event = generate_dummy_text_message_event_from_user()
    request_info_service.set_req_info(event=dummy_event)
    use_case = FollowUseCase()
    mocker.patch.object(
        rich_menu_service,
        'create_and_link',
        return_value=None,
    )
    mocker.patch.object(
        line_bot_api,
        'get_profile',
        return_value=generate_dummy_profile(),
    )

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    reply_service.reset()
