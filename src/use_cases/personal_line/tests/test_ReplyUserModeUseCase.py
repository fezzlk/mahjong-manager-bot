from ApplicationService import (
    reply_service,
    request_info_service,
)
from DomainModel.entities.User import User, UserMode
from line_models.Event import Event
from repositories import user_repository
from use_cases.personal_line.ReplyUserModeUseCase import ReplyUserModeUseCase

dummy_user = User(
    line_user_name="test_user1",
    line_user_id="U0123456789abcdefghijklmnopqrstu1",
    mode=UserMode.wait.value,
    jantama_name="jantama_user1",
)

dummy_event = Event(
    type="message",
    source_type="user",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="dummy_text",
)


def test_execute():
    # Arrange
    user_repository.create(dummy_user)
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyUserModeUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "wait"



def test_execute_no_user():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyUserModeUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "ユーザーを認識できませんでした。当アカウントを一度ブロックし、ブロック解除してください。"
