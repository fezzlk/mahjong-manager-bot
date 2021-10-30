from tests.dummies import (
    generate_dummy_join_event,
)
from use_cases import JoinGroupUseCase
from services import (
    request_info_service,
    reply_service,
)
from repositories import session_scope, group_repository


def test_execute(mocker):
    # Arrage
    dummy_event = generate_dummy_join_event()
    request_info_service.set_req_info(event=dummy_event)

    use_case = JoinGroupUseCase()

    # Act
    use_case.execute()

    # Assert
    with session_scope() as session:
        result = group_repository.find_all(session)
        assert len(result) == 1
    reply_service.reset()
