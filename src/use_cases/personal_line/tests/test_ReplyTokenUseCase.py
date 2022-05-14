from DomainModel.entities.User import User, UserMode
from use_cases.personal_line.ReplyTokenUseCase import ReplyTokenUseCase
from ApplicationService import (
    request_info_service,
    reply_service,
)
from line_models.Event import Event
from repositories import session_scope, user_repository
import requests

dummy_user = User(
    line_user_name="test_user1",
    line_user_id="U0123456789abcdefghijklmnopqrstu1",
    zoom_url="https://us00web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz",
    mode=UserMode.wait,
    jantama_name="jantama_user1",
    matches=[],
    _id=1,
)

dummy_event = Event(
    event_type='message',
    source_type='user',
    user_id="U0123456789abcdefghijklmnopqrstu1",
    message_type='text',
    text='dummy_text',
)


class Dummy:
    def json(self):
        return


def test_execute(mocker):
    # Arrage
    with session_scope() as session:
        user_repository.create(session, dummy_user)
    request_info_service.set_req_info(event=dummy_event)
    use_case = ReplyTokenUseCase()
    dummy_response = Dummy()
    mocker.patch.object(
        requests,
        'post',
        return_value=dummy_response,
    )
    mocker.patch.object(
        dummy_response,
        'json',
        return_value={'access_token': 'hoge'},
    )

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
