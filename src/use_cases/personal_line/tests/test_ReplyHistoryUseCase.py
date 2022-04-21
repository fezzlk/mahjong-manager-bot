from use_cases.personal_line.ReplyHistoryUseCase import ReplyHistoryUseCase
from ApplicationService import (
    reply_service,
    request_info_service,
)
from DomainModel.entities.User import User, UserMode
from repositories import session_scope, user_repository

dummy_user = User(
    line_user_name="test_user1",
    line_user_id="U0123456789abcdefghijklmnopqrstu1",
    zoom_url="https://us00web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz",
    mode=UserMode.wait,
    jantama_name="jantama_user1",
    matches=[],
    _id=1,
)


def test_execute_not_match():
    # Arrage
    with session_scope() as session:
        user_repository.create(session, dummy_user)

    request_info_service.req_line_user_id = dummy_user.line_user_id
    use_case = ReplyHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == '対局履歴がありません。'
