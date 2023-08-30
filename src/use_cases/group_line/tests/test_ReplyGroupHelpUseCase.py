from tests.dummies import (
    generate_dummy_text_message_event_from_group,
)
from use_cases.group_line.ReplyGroupHelpUseCase import ReplyGroupHelpUseCase
from ApplicationService import (
    request_info_service,
    reply_service,
)


def test_execute():
    # Arrange
    dummy_event = generate_dummy_text_message_event_from_group()
    request_info_service.set_req_info(event=dummy_event)

    use_case = ReplyGroupHelpUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 2
