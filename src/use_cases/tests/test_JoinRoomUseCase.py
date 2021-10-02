from tests.dummies import (
    generate_dummy_join_event,
)
from use_cases import JoinRoomUseCase
from services import (
    request_info_service,
)
from repositories import session_scope, RoomRepository


def test_execute(mocker):
    # Arrage
    dummy_event = generate_dummy_join_event()
    request_info_service.set_req_info(event=dummy_event)

    use_case = JoinRoomUseCase()

    # Act
    use_case.execute()

    # Assert
    with session_scope() as session:
        result = RoomRepository.find_all(session)
        assert len(result) == 0
