from dummies import generate_dummy_text_message_event_from_group

from application_service import (
    reply_service,
    request_info_service,
)
from domain_service import guest_service
from use_cases.group_line.guest_remove_confirm_use_case import (
    GuestRemoveConfirmUseCase,
)

_LINE_GROUP_ID = "G0123456789abcdefghijklmnopqrstu1"


def _setup_request(params=None):
    event = generate_dummy_text_message_event_from_group()
    event.group_id = _LINE_GROUP_ID
    request_info_service.set_req_info(event=event)
    if params:
        request_info_service.params = params


def test_execute_removes_existing_guest():
    guest_service.register_next(_LINE_GROUP_ID)
    _setup_request(params={"number": "1"})

    GuestRemoveConfirmUseCase().execute()

    assert len(reply_service.texts) == 1
    assert "削除しました" in reply_service.texts[0].text
    assert guest_service.list_by_group(_LINE_GROUP_ID) == []


def test_execute_nonexistent_number():
    _setup_request(params={"number": "999"})

    GuestRemoveConfirmUseCase().execute()

    assert len(reply_service.texts) == 1
    assert "見つかりません" in reply_service.texts[0].text


def test_execute_missing_number():
    _setup_request(params={})

    GuestRemoveConfirmUseCase().execute()

    assert len(reply_service.texts) == 1
    assert "指定されていません" in reply_service.texts[0].text


def test_execute_non_numeric_number():
    _setup_request(params={"number": "not-a-number"})

    GuestRemoveConfirmUseCase().execute()

    assert len(reply_service.texts) == 1
    assert "指定されていません" in reply_service.texts[0].text
