from tests.dummies import (
    generate_dummy_unfollow_event,
    generate_dummy_user_list,
)
from use_cases.personal_line.UnfollowUseCase import UnfollowUseCase
from ApplicationService import (
    request_info_service,
)
from repositories import session_scope, UserRepository


def test_execute():
    # Arrange
    dummy_event = generate_dummy_unfollow_event()
    request_info_service.set_req_info(event=dummy_event)

    dummy_user = generate_dummy_user_list()[0]
    user_repository = UserRepository()
    with session_scope() as session:
        user_repository.create(session, dummy_user)

    use_case = UnfollowUseCase()

    # Act
    use_case.execute()

    # Assert
    with session_scope() as session:
        result = user_repository.find_all(session)
        assert len(result) == 0
