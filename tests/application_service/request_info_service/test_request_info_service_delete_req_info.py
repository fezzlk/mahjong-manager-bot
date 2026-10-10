from dummies import (
    generate_dummy_follow_event,
    generate_dummy_text_message_event_from_group,
    generate_dummy_text_message_event_from_user,
)

from application_service.request_info_service import RequestInfoService
from line_models.event import Event


def test_success_follow():
    # Arrange
    request_info_service = RequestInfoService()
    follow_event = generate_dummy_follow_event()
    request_info_service.set_req_info(follow_event)

    # Act
    request_info_service.delete_req_info()

    # Assert
    assert request_info_service.req_line_user_id is None
    assert request_info_service.req_line_group_id is None
    assert request_info_service.mention_line_ids == []
    assert request_info_service.message is None
    assert request_info_service.command is None
    assert request_info_service.params == {}
    assert request_info_service.body is None


def test_success_message_from_user():
    # Arrange
    request_info_service = RequestInfoService()
    message_event = generate_dummy_text_message_event_from_user()
    request_info_service.set_req_info(message_event)

    # Act
    request_info_service.delete_req_info()

    # Assert
    assert request_info_service.req_line_user_id is None
    assert request_info_service.req_line_group_id is None
    assert request_info_service.mention_line_ids == []
    assert request_info_service.message is None
    assert request_info_service.command is None
    assert request_info_service.params == {}
    assert request_info_service.body is None


def test_success_message_with_mention_self():
    # Arrange
    request_info_service = RequestInfoService()
    message_event = Event(
        type="message",
        source_type="group",
        user_id="U0123456789abcdefghijklmnopqrstu1",
        group_id="G0123456789abcdefghijklmnopqrstu1",
        message_type="text",
        text="dummy_text",
        mention_self=True,
    )
    request_info_service.set_req_info(message_event)

    # Act
    request_info_service.delete_req_info()

    # Assert
    assert request_info_service.is_mention_self is False


def test_success_message_from_group():
    # Arrange
    request_info_service = RequestInfoService()
    message_event = generate_dummy_text_message_event_from_group()
    request_info_service.set_req_info(message_event)

    # Act
    request_info_service.delete_req_info()

    # Assert
    assert request_info_service.req_line_user_id is None
    assert request_info_service.req_line_group_id is None
    assert request_info_service.mention_line_ids == []
    assert request_info_service.message is None
    assert request_info_service.command is None
    assert request_info_service.params == {}
    assert request_info_service.body is None
