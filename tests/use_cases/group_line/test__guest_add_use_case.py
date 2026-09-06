from dummies import generate_dummy_text_message_event_from_group

from application_service import (
    reply_service,
    request_info_service,
)
from domain_service import guest_service
from use_cases.group_line.guest_add_use_case import GuestAddUseCase

_LINE_GROUP_ID = "G0123456789abcdefghijklmnopqrstu1"


def _setup_request():
    event = generate_dummy_text_message_event_from_group()
    event.group_id = _LINE_GROUP_ID
    request_info_service.set_req_info(event=event)


def test_execute_registers_first_guest():
    _setup_request()

    GuestAddUseCase().execute()

    assert len(reply_service.texts) == 1
    assert "ゲスト1" in reply_service.texts[0].text
    assert [g.guest_number for g in guest_service.list_by_group(_LINE_GROUP_ID)] == [1]


def test_execute_increments_on_repeated_calls():
    _setup_request()

    GuestAddUseCase().execute()
    GuestAddUseCase().execute()

    assert "ゲスト2" in reply_service.texts[1].text
