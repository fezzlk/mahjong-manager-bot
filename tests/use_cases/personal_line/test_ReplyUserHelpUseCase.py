from ApplicationService import (
    reply_service,
    request_info_service,
)
from dummies import (
    generate_dummy_text_message_event_from_user,
)
from use_cases.personal_line.ReplyUserHelpUseCase import ReplyUserHelpUseCase


def test_execute():
    # Arrange
    dummy_event = generate_dummy_text_message_event_from_user()
    request_info_service.set_req_info(event=dummy_event)

    use_case = ReplyUserHelpUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
