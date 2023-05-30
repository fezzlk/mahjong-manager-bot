from tests.dummies import (
    generate_dummy_join_event,
)
from use_cases.common_line.ReplyFortuneUseCase import ReplyFortuneUseCase
from ApplicationService import (
    request_info_service,
)


def test_execute():
    # Arrange
    dummy_event = generate_dummy_join_event()
    request_info_service.set_req_info(event=dummy_event)

    use_case = ReplyFortuneUseCase()

    # Act
    use_case.execute()

    # Assert
