from services.RequestInfoService import RequestInfoService
from tests.dummies import (
    generate_dummy_follow_event,
    generate_dummy_text_message_event_from_user,
    generate_dummy_text_message_event_from_room,
)


def test_follow_event():
    # Arrange
    request_info_service = RequestInfoService()
    follow_event = generate_dummy_follow_event()

    # Act
    request_info_service.set_req_info(follow_event)

    # Assert
    assert request_info_service.req_line_user_id == follow_event.source.user_id


def test_message_event_from_user():
    # Arrange
    request_info_service = RequestInfoService()
    message_event = generate_dummy_text_message_event_from_user()

    # Act
    request_info_service.set_req_info(message_event)

    # Assert
    assert request_info_service.req_line_user_id == message_event.source.user_id


def test_message_event_from_room():
    # Arrange
    request_info_service = RequestInfoService()
    message_event = generate_dummy_text_message_event_from_room()

    # Act
    request_info_service.set_req_info(message_event)

    # Assert
    assert request_info_service.req_line_user_id == message_event.source.user_id
    assert request_info_service.req_line_room_id == message_event.source.room_id