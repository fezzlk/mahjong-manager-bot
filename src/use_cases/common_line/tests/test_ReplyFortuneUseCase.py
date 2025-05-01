from ApplicationService import (
    message_service,
    reply_service,
    request_info_service,
)
from DomainModel.entities.User import User
from line_models.Event import Event
from repositories import user_repository
from use_cases.common_line.ReplyFortuneUseCase import ReplyFortuneUseCase

dummy_event = Event(
    type="join",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
)

def test_execute(mocker):
    # Arrange
    mocker.patch.object(
        message_service,
        "get_random_hai",
        return_value="中",
    )
    user_repository.create(User("U0123456789abcdefghijklmnopqrstu1", line_user_name="test"))
    request_info_service.set_req_info(event=dummy_event)

    use_case = ReplyFortuneUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "testさんの今日のラッキー牌は「中」です。"


def test_execute_no_user():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)

    use_case = ReplyFortuneUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "ユーザーが登録されていません。友達追加してください。"
