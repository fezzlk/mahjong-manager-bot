from DomainModel.entities.User import User, UserMode
from DomainModel.entities.WebUser import WebUser
from use_cases.personal_line.RequestLinkLineWebUseCase import RequestLinkLineWebUseCase
from ApplicationService import (
    request_info_service,
    reply_service,
)
from line_models.Event import Event
from datetime import datetime
from repositories import web_user_repository
import pytest

dummy_user = User(
    line_user_name="test_user1",
    line_user_id="U0123456789abcdefghijklmnopqrstu1",
    mode=UserMode.wait.value,
    jantama_name="jantama_user1",
)

dummy_event = Event(
    event_type='message',
    source_type='user',
    user_id="U0123456789abcdefghijklmnopqrstu1",
    message_type='text',
    text='dummy_text',
)


@pytest.fixture(params=[
    (''),
    ('messeage'),
    ('messeage 1 2'),
])
def text_case(request) -> int:
    return request.param


def test_fail_mismatch_massage_format(mocker, text_case):
    # Arrange
    dummy_event = Event(
        event_type='message',
        source_type='user',
        user_id="U0123456789abcdefghijklmnopqrstu1",
        message_type='text',
        text=text_case,
    )
    request_info_service.set_req_info(event=dummy_event)
    use_case = RequestLinkLineWebUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == 'Web アカウントと紐付けするには "アカウント連携 [メールアドレス]" と送ってください。'


def test_fail_no_web_user(mocker):
    # Arrange
    dummy_event = Event(
        event_type='message',
        source_type='user',
        user_id="U0123456789abcdefghijklmnopqrstu1",
        message_type='text',
        text='アカウント連携 dummy@example.com',
    )
    request_info_service.set_req_info(event=dummy_event)
    use_case = RequestLinkLineWebUseCase()
    web_user_repository.create(WebUser(
        user_code="code1",
        name="name1",
        email="email1",
        linked_line_user_id=None,
        is_approved_line_user=False,
        created_at=datetime(2022, 1, 1, 12, 0, 0),
        updated_at=datetime(2022, 1, 1, 12, 0, 0),
    ))

    mocker.patch(
        'use_cases.personal_line.RequestLinkLineWebUseCase.url_for',
        return_value='',
    )
    # Act
    use_case.execute()

    # Assert
    print(reply_service.texts[0])
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].text == 'dummy@example.com は登録されていません。一度ブラウザでログインしてください。'


def test_fail_have_linked_user(mocker):
    # Arrange
    dummy_event = Event(
        event_type='message',
        source_type='user',
        user_id="U0123456789abcdefghijklmnopqrstu1",
        message_type='text',
        text='アカウント連携 email1',
    )
    request_info_service.set_req_info(event=dummy_event)
    use_case = RequestLinkLineWebUseCase()
    web_user_repository.create(WebUser(
        user_code="code1",
        name="name1",
        email="email1",
        linked_line_user_id=None,
        is_approved_line_user=True,
        created_at=datetime(2022, 1, 1, 12, 0, 0),
        updated_at=datetime(2022, 1, 1, 12, 0, 0),
    ))

    mocker.patch(
        'use_cases.personal_line.RequestLinkLineWebUseCase.url_for',
        return_value='',
    )
    # Act
    use_case.execute()

    # Assert
    print(reply_service.texts[0])
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].text == 'email1 はすでに LINE アカウントと紐付けされています。'


def test_fail_update_web_user(mocker):
    # Arrange
    dummy_event = Event(
        event_type='message',
        source_type='user',
        user_id="U0123456789abcdefghijklmnopqrstu1",
        message_type='text',
        text='アカウント連携 email1',
    )
    request_info_service.set_req_info(event=dummy_event)
    use_case = RequestLinkLineWebUseCase()
    web_user_repository.create(WebUser(
        user_code="code1",
        name="name1",
        email="email1",
        linked_line_user_id=None,
        is_approved_line_user=False,
        created_at=datetime(2022, 1, 1, 12, 0, 0),
        updated_at=datetime(2022, 1, 1, 12, 0, 0),
    ))
    mocker.patch.object(
        web_user_repository,
        'update',
        return_value=0,
    )

    # Act
    use_case.execute()

    # Assert
    print(reply_service.texts[0])
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == 'アカウント連携リクエストに失敗しました。'


def test_success(mocker):
    # Arrange
    dummy_event = Event(
        event_type='message',
        source_type='user',
        user_id="U0123456789abcdefghijklmnopqrstu1",
        message_type='text',
        text='アカウント連携 email1',
    )
    request_info_service.set_req_info(event=dummy_event)
    use_case = RequestLinkLineWebUseCase()
    web_user_repository.create(WebUser(
        user_code="code1",
        name="name1",
        email="email1",
        linked_line_user_id=None,
        is_approved_line_user=False,
        created_at=datetime(2022, 1, 1, 12, 0, 0),
        updated_at=datetime(2022, 1, 1, 12, 0, 0),
    ))

    mocker.patch(
        'use_cases.personal_line.RequestLinkLineWebUseCase.url_for',
        return_value='',
    )
    # Act
    use_case.execute()

    # Assert
    print(reply_service.texts[0])
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].text == 'アカウント連携リクエストを送信しました。ブラウザでログインし、承認してください。'
