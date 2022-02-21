from tests.dummies import (
    generate_dummy_join_event,
)
from use_cases.group_line.JoinGroupUseCase import JoinGroupUseCase
from services import (
    request_info_service,
    reply_service,
)
from repositories import session_scope, group_repository
from linebot.models import TextSendMessage


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
    assert len(reply_service.texts) == 1
    assert isinstance(reply_service.texts[0], TextSendMessage)
    assert reply_service.texts[0].text == 'こんにちは、今日は麻雀日和ですね。'
    reply_service.reset()
