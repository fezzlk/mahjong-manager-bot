from ApplicationService.RequestInfoService import RequestInfoService
from tests.dummies import (
    generate_dummy_follow_event,
)


def test_success():
    # Arrange
    request_info_service = RequestInfoService()
    follow_event = generate_dummy_follow_event()
    request_info_service.set_req_info(follow_event)

    # Act
    request_info_service.delete_req_info()

    # Assert
    assert request_info_service.req_line_user_id is None
    assert request_info_service.req_line_group_id is None
