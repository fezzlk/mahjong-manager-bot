from use_cases.personal_line.SetZoomUrlToUserUseCase import (
    SetZoomUrlToUserUseCase,
)
from DomainModel.entities.User import User, UserMode
from ApplicationService import (
    request_info_service,
)
from repositories import (
    session_scope,
    user_repository,
)

dummy_user = User(
    line_user_name="test_user1",
    line_user_id="U0123456789abcdefghijklmnopqrstu1",
    zoom_url="",
    mode=UserMode.wait,
    jantama_name="jantama_user1",
    matches=[],
    _id=1,
)


def test_execute():
    # Arrange
    request_info_service.req_line_user_id = dummy_user.line_user_id
    with session_scope() as session:
        user_repository.create(session, dummy_user)

    use_case = SetZoomUrlToUserUseCase()

    # Act
    use_case.execute(
        "https://us00web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz")

    # Assert
    with session_scope() as session:
        user = user_repository.find_all(session)[0]
        assert user.zoom_url == "https://us00web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz"
