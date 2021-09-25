from services.RequestInfoService import RequestInfoService
from tests.dummies import generate_dummy_text_message_event_from_room


def test_success():
    # Arrange
    request_info_service = RequestInfoService()
    dummy_event = generate_dummy_text_message_event_from_room()
    request_info_service.req_line_user_id = dummy_event.source.user_id
    request_info_service.req_line_room_id = dummy_event.source.room_id

    # Act
    request_info_service.delete_req_info()

    # Assert
    assert request_info_service.req_line_user_id is None
    assert request_info_service.req_line_room_id is None
